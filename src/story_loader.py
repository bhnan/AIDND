import json
import os
from typing import List, Dict, Any
from game_engine import StoryNode

def load_story_from_json(file_path: str) -> List[StoryNode]:
    """
    从JSON文件加载故事节点
    
    JSON格式应为：
    {
        "nodes": [
            {
                "id": "节点ID",
                "content": "节点内容描述",
                "choices": [
                    {
                        "text": "选项文本",
                        "next_node": "下一节点ID"
                    },
                    ...
                ]
            },
            ...
        ]
    }
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"故事文件未找到: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        nodes = []
        for node_data in data.get("nodes", []):
            node = StoryNode(
                node_id=node_data["id"],
                content=node_data["content"],
                choices=node_data["choices"]
            )
            nodes.append(node)
        
        return nodes
    except json.JSONDecodeError:
        raise ValueError(f"无法解析JSON文件: {file_path}")
    except KeyError as e:
        raise ValueError(f"JSON文件格式不正确，缺少关键字段: {e}")

def save_story_to_json(nodes: List[StoryNode], file_path: str) -> None:
    """
    将故事节点保存到JSON文件
    """
    data = {
        "nodes": [
            {
                "id": node.node_id,
                "content": node.content,
                "choices": node.choices
            }
            for node in nodes
        ]
    }
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4) 