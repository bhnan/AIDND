# AI Dungeon 风格的互动故事游戏

这是一个基于图结构的互动故事游戏引擎，使用巫师3第一章作为示例故事。

## 功能特点

- 基于图结构的故事节点系统
- 支持从JSON文件加载故事
- 提供交互式故事编辑器
- 游戏状态保存和加载
- 简单的命令行界面

## 安装

1. 克隆项目到本地
2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### 运行游戏

```bash
python src/main.py [故事文件路径]
```

如果不指定故事文件路径，默认会加载 `data/witcher_chapter1.json`。

### 游戏控制

- 输入数字选择选项
- 输入 'q' 退出游戏
- 输入 's' 保存游戏
- 输入 'l' 加载游戏
- 输入 'h' 查看帮助

### 使用故事编辑器

```bash
python src/story_editor.py
```

编辑器提供以下功能：
- 创建新故事
- 加载已有故事
- 添加、编辑、删除故事节点
- 验证故事结构
- 保存故事

## 项目结构

- `src/game_engine.py`: 游戏引擎核心逻辑
- `src/story_loader.py`: 故事数据加载工具
- `src/story_editor.py`: 交互式故事编辑器
- `src/main.py`: 主程序入口
- `data/`: 存储故事JSON文件
- `requirements.txt`: 项目依赖

## 故事JSON格式

故事以JSON格式存储，结构如下：

```json
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
```

## 扩展开发

要添加新的故事内容，可以：
1. 使用交互式编辑器创建和编辑故事
2. 手动编辑JSON文件
3. 修改 `data/witcher_chapter1.json` 文件 