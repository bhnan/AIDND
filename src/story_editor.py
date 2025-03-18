import json
import os
from typing import List, Dict, Any
import networkx as nx
from story_loader import load_story_from_json, save_story_to_json
from game_engine import StoryNode

class StoryEditor:
    def __init__(self, file_path: str = None):
        self.file_path = file_path
        self.nodes: List[StoryNode] = []
        self.graph = nx.DiGraph()
        
        if file_path and os.path.exists(file_path):
            self.load_story(file_path)
    
    def load_story(self, file_path: str):
        """加载故事文件"""
        self.nodes = load_story_from_json(file_path)
        self.file_path = file_path
        
        # 构建图
        for node in self.nodes:
            self.graph.add_node(node.node_id, content=node.content, choices=node.choices)
            
        # 添加边
        for node in self.nodes:
            for choice in node.choices:
                self.graph.add_edge(node.node_id, choice['next_node'], text=choice['text'])
    
    def save_story(self, file_path: str = None):
        """保存故事到文件"""
        if file_path:
            self.file_path = file_path
        
        if not self.file_path:
            raise ValueError("需要指定保存文件路径")
            
        save_story_to_json(self.nodes, self.file_path)
        print(f"故事已保存到：{self.file_path}")
    
    def add_node(self, node_id: str, content: str, choices: List[Dict[str, str]] = None):
        """添加新节点"""
        if choices is None:
            choices = []
            
        # 检查节点ID是否已存在
        for node in self.nodes:
            if node.node_id == node_id:
                raise ValueError(f"节点ID '{node_id}' 已存在")
        
        # 创建并添加节点
        node = StoryNode(node_id, content, choices)
        self.nodes.append(node)
        self.graph.add_node(node_id, content=content, choices=choices)
        
        return node
    
    def edit_node(self, node_id: str, content: str = None, choices: List[Dict[str, str]] = None):
        """编辑现有节点"""
        # 查找节点
        found = False
        for i, node in enumerate(self.nodes):
            if node.node_id == node_id:
                found = True
                if content is not None:
                    node.content = content
                    self.graph.nodes[node_id]['content'] = content
                
                if choices is not None:
                    # 移除旧的边
                    for old_choice in node.choices:
                        if self.graph.has_edge(node_id, old_choice['next_node']):
                            self.graph.remove_edge(node_id, old_choice['next_node'])
                    
                    # 添加新的选项和边
                    node.choices = choices
                    self.graph.nodes[node_id]['choices'] = choices
                    
                    # 添加新边
                    for choice in choices:
                        self.graph.add_edge(node_id, choice['next_node'], text=choice['text'])
                break
        
        if not found:
            raise ValueError(f"找不到节点 '{node_id}'")
    
    def delete_node(self, node_id: str):
        """删除节点"""
        # 查找并删除节点
        for i, node in enumerate(self.nodes):
            if node.node_id == node_id:
                del self.nodes[i]
                self.graph.remove_node(node_id)
                
                # 更新其他节点的选项，删除指向此节点的选项
                for other_node in self.nodes:
                    new_choices = []
                    for choice in other_node.choices:
                        if choice['next_node'] != node_id:
                            new_choices.append(choice)
                    other_node.choices = new_choices
                    self.graph.nodes[other_node.node_id]['choices'] = new_choices
                return
        
        raise ValueError(f"找不到节点 '{node_id}'")
    
    def validate_story(self) -> List[str]:
        """验证故事的完整性和一致性"""
        errors = []
        node_ids = set(node.node_id for node in self.nodes)
        
        # 检查所有引用的节点是否存在
        for node in self.nodes:
            for i, choice in enumerate(node.choices):
                if choice['next_node'] not in node_ids:
                    errors.append(f"节点 '{node.node_id}' 的选项 {i+1} 引用了不存在的节点 '{choice['next_node']}'")
        
        # 检查是否有孤立的节点（没有指向它的节点）
        for node_id in node_ids:
            if node_id != "start" and not any(
                choice['next_node'] == node_id 
                for node in self.nodes 
                for choice in node.choices
            ):
                errors.append(f"节点 '{node_id}' 是孤立的，没有其他节点指向它")
        
        # 检查是否有循环依赖
        try:
            cycles = list(nx.simple_cycles(self.graph))
            if cycles:
                for cycle in cycles:
                    errors.append(f"发现循环依赖: {' -> '.join(cycle)} -> {cycle[0]}")
        except:
            pass  # 忽略可能的错误
            
        return errors
    
def interactive_editor():
    """交互式故事编辑器"""
    print("=" * 50)
    print("交互式故事编辑器")
    print("=" * 50)
    
    # 选择操作模式
    while True:
        print("\n请选择操作：")
        print("1. 创建新故事")
        print("2. 加载已有故事")
        print("q. 退出")
        
        choice = input("请选择：").strip().lower()
        
        if choice == 'q':
            print("再见！")
            break
        
        editor = StoryEditor()
        
        if choice == '1':
            # 创建新故事
            file_path = input("请输入新故事文件路径：").strip()
            if not file_path:
                print("文件路径不能为空！")
                continue
                
            # 添加开始节点
            editor.add_node(
                "start",
                input("请输入起始节点的内容：").strip(),
                []
            )
            
        elif choice == '2':
            # 加载已有故事
            file_path = input("请输入故事文件路径：").strip()
            try:
                editor.load_story(file_path)
                print(f"成功加载了 {len(editor.nodes)} 个节点")
            except Exception as e:
                print(f"加载故事失败：{e}")
                continue
        else:
            print("无效的选择！")
            continue
        
        # 故事编辑循环
        while True:
            print("\n当前故事包含的节点：")
            for i, node in enumerate(editor.nodes):
                print(f"{i+1}. {node.node_id}: {node.content[:30]}...")
            
            print("\n请选择操作：")
            print("1. 添加新节点")
            print("2. 编辑节点")
            print("3. 删除节点")
            print("4. 验证故事")
            print("5. 保存故事")
            print("q. 返回上级菜单")
            
            op = input("请选择：").strip().lower()
            
            if op == 'q':
                break
                
            elif op == '1':
                # 添加节点
                node_id = input("请输入新节点ID：").strip()
                content = input("请输入节点内容：").strip()
                
                choices = []
                while True:
                    choice_text = input("请输入选项文本（留空结束）：").strip()
                    if not choice_text:
                        break
                        
                    next_node = input("请输入选项指向的节点ID：").strip()
                    choices.append({"text": choice_text, "next_node": next_node})
                
                try:
                    editor.add_node(node_id, content, choices)
                    print(f"成功添加节点 '{node_id}'")
                except Exception as e:
                    print(f"添加节点失败：{e}")
            
            elif op == '2':
                # 编辑节点
                node_id = input("请输入要编辑的节点ID：").strip()
                
                # 查找节点
                found = False
                for node in editor.nodes:
                    if node.node_id == node_id:
                        found = True
                        print(f"当前内容: {node.content}")
                        content = input("请输入新内容（留空保持不变）：").strip()
                        content = content if content else node.content
                        
                        print("当前选项：")
                        for i, choice in enumerate(node.choices):
                            print(f"{i+1}. {choice['text']} -> {choice['next_node']}")
                        
                        edit_choices = input("是否编辑选项？(y/n)：").strip().lower() == 'y'
                        
                        if edit_choices:
                            choices = []
                            while True:
                                choice_text = input("请输入选项文本（留空结束）：").strip()
                                if not choice_text:
                                    break
                                    
                                next_node = input("请输入选项指向的节点ID：").strip()
                                choices.append({"text": choice_text, "next_node": next_node})
                        else:
                            choices = node.choices
                        
                        try:
                            editor.edit_node(node_id, content, choices)
                            print(f"成功编辑节点 '{node_id}'")
                        except Exception as e:
                            print(f"编辑节点失败：{e}")
                        break
                
                if not found:
                    print(f"找不到节点 '{node_id}'")
            
            elif op == '3':
                # 删除节点
                node_id = input("请输入要删除的节点ID：").strip()
                
                try:
                    editor.delete_node(node_id)
                    print(f"成功删除节点 '{node_id}'")
                except Exception as e:
                    print(f"删除节点失败：{e}")
            
            elif op == '4':
                # 验证故事
                errors = editor.validate_story()
                
                if errors:
                    print("\n故事存在以下问题：")
                    for error in errors:
                        print(f"- {error}")
                else:
                    print("\n故事验证通过，没有发现问题！")
            
            elif op == '5':
                # 保存故事
                file_path = input(f"请输入保存路径（默认：{editor.file_path}）：").strip()
                file_path = file_path if file_path else editor.file_path
                
                try:
                    editor.save_story(file_path)
                except Exception as e:
                    print(f"保存故事失败：{e}")
            
            else:
                print("无效的选择！")

if __name__ == "__main__":
    interactive_editor() 