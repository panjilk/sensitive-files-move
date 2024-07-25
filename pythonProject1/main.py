import tqdm
import  time

def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    for i in tqdm.tqdm(range(100)):
        time.sleep(0.1)

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
