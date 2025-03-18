import networkx as nx
from typing import Dict, List, Optional
import json
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class StoryNode:
    def __init__(self, node_id: str, content: str, choices: List[Dict[str, str]]):
        self.node_id = node_id
        self.content = content
        self.choices = choices  # List of dicts with 'text' and 'next_node' keys

class GameEngine:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.current_node: Optional[str] = None
        self.story_state: Dict = {
            "inventory": [],
            "visited_nodes": [],
            "player_stats": {},
            "flags": {}
        }
        self.history: List[str] = []  # 保存玩家经历的故事内容
        
    def add_node(self, node: StoryNode):
        """添加故事节点到图中"""
        self.graph.add_node(node.node_id, content=node.content, choices=node.choices)
        
    def add_edge(self, from_node: str, to_node: str, choice_text: str):
        """添加节点之间的连接"""
        self.graph.add_edge(from_node, to_node, choice=choice_text)
        
    def get_current_content(self) -> str:
        """获取当前节点的内容"""
        if not self.current_node:
            return "游戏尚未开始"
        
        # 记录这个节点到历史中
        if self.current_node not in self.story_state["visited_nodes"]:
            self.story_state["visited_nodes"].append(self.current_node)
        
        content = self.graph.nodes[self.current_node]['content']
        self.history.append(content)
        
        # 只保留最近的10条历史记录，避免上下文过长
        if len(self.history) > 10:
            self.history = self.history[-10:]
            
        return content
    
    def get_choices(self) -> List[Dict[str, str]]:
        """获取当前节点的选项"""
        if not self.current_node:
            return []
        return self.graph.nodes[self.current_node]['choices']
    
    def make_choice(self, choice_index: int) -> bool:
        """玩家做出选择"""
        if not self.current_node:
            return False
            
        choices = self.get_choices()
        if 0 <= choice_index < len(choices):
            next_node = choices[choice_index]['next_node']
            self.current_node = next_node
            return True
        return False
    
    def save_game(self, filename: str):
        """保存游戏状态"""
        game_state = {
            'current_node': self.current_node,
            'story_state': self.story_state,
            'history': self.history
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(game_state, f, ensure_ascii=False, indent=4)
            
    def load_game(self, filename: str):
        """加载游戏状态"""
        with open(filename, 'r', encoding='utf-8') as f:
            game_state = json.load(f)
            self.current_node = game_state['current_node']
            self.story_state = game_state['story_state']
            self.history = game_state.get('history', [])
    
    def get_node_connections(self):
        """获取当前节点的所有连接，用于可视化"""
        if not self.current_node:
            return []
        
        connections = []
        for _, neighbor, data in self.graph.edges(self.current_node, data=True):
            connections.append({
                'target': neighbor,
                'choice': data.get('choice', '')
            })
        return connections 