from game_engine import GameEngine
from story_loader import load_story_from_json
import os
import sys

def main():
    # 默认故事文件路径
    default_story_path = os.path.join("data", "witcher_chapter1.json")
    
    # 如果命令行参数提供了故事文件，使用它
    story_path = sys.argv[1] if len(sys.argv) > 1 else default_story_path
    
    # 打印欢迎信息
    print("=" * 50)
    print("欢迎来到巫师3第一章的互动故事游戏！")
    print("=" * 50)
    
    try:
        # 创建游戏引擎
        game = GameEngine()
        
        # 加载故事数据
        print(f"正在加载故事文件: {story_path}")
        nodes = load_story_from_json(story_path)
        print(f"成功加载了 {len(nodes)} 个故事节点")
        
        # 将节点添加到游戏中
        for node in nodes:
            game.add_node(node)
        
        # 设置起始节点
        game.current_node = "start"
        
        print("\n输入命令说明:")
        print("- 输入数字选择对应选项")
        print("- 输入 'q' 退出游戏")
        print("- 输入 's' 保存游戏")
        print("- 输入 'l' 加载游戏")
        print("- 输入 'h' 查看帮助")
        print("=" * 50)
        
        while True:
            print("\n" + "="*50)
            print(game.get_current_content())
            print("\n可选项：")
            
            choices = game.get_choices()
            for i, choice in enumerate(choices):
                print(f"{i+1}. {choice['text']}")
                
            user_input = input("\n请选择（输入数字或命令）: ").strip().lower()
            
            if user_input == 'q':
                print("感谢游玩！")
                break
            elif user_input == 's':
                save_path = input("请输入保存文件名（默认为 save_game.json）: ").strip()
                save_path = save_path if save_path else 'save_game.json'
                game.save_game(save_path)
                print(f"游戏已保存至 {save_path}！")
                continue
            elif user_input == 'l':
                load_path = input("请输入加载文件名（默认为 save_game.json）: ").strip()
                load_path = load_path if load_path else 'save_game.json'
                try:
                    game.load_game(load_path)
                    print(f"游戏已从 {load_path} 加载！")
                except FileNotFoundError:
                    print(f"错误：找不到保存文件 {load_path}")
                continue
            elif user_input == 'h':
                print("\n命令说明:")
                print("- 输入数字选择对应选项")
                print("- 输入 'q' 退出游戏")
                print("- 输入 's' 保存游戏")
                print("- 输入 'l' 加载游戏")
                print("- 输入 'h' 查看帮助")
                continue
                
            try:
                choice_index = int(user_input) - 1
                if game.make_choice(choice_index):
                    continue
                else:
                    print("无效的选择，请重试！")
            except ValueError:
                print("请输入有效的数字或命令！")
    
    except FileNotFoundError as e:
        print(f"错误：{e}")
        print(f"请确保故事文件 '{story_path}' 存在并可访问")
    except ValueError as e:
        print(f"错误：{e}")
    except Exception as e:
        print(f"发生未知错误：{e}")

if __name__ == "__main__":
    main() 