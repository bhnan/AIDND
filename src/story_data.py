from game_engine import StoryNode

def create_demo_story():
    # 创建初始节点
    nodes = [
        StoryNode(
            "start",
            "你醒来发现自己在一个陌生的房间里。房间里有一张床、一张桌子和一把椅子。桌子上放着一封信。",
            [
                {"text": "查看信件", "next_node": "read_letter"},
                {"text": "检查房间", "next_node": "check_room"}
            ]
        ),
        StoryNode(
            "read_letter",
            "信件上写着：'亲爱的杰洛特，如果你看到这封信，说明你已经安全到达了。请尽快前往白果园村，那里有重要的事情等着你。'",
            [
                {"text": "立即出发", "next_node": "leave_room"},
                {"text": "继续检查房间", "next_node": "check_room"}
            ]
        ),
        StoryNode(
            "check_room",
            "在仔细检查房间后，你发现了一些有用的物品：一把银剑、一些金币和一张地图。",
            [
                {"text": "拿起物品", "next_node": "take_items"},
                {"text": "查看信件", "next_node": "read_letter"}
            ]
        ),
        StoryNode(
            "take_items",
            "你拿起了所有物品。现在你准备离开房间。",
            [
                {"text": "离开房间", "next_node": "leave_room"}
            ]
        ),
        StoryNode(
            "leave_room",
            "你离开了房间，发现自己在一个小旅馆里。楼下传来喧闹声。",
            [
                {"text": "下楼查看", "next_node": "downstairs"},
                {"text": "从窗户观察", "next_node": "window"}
            ]
        )
    ]
    return nodes 