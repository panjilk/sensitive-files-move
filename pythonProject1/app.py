import tkinter as tk
from tkinter import Toplevel, Checkbutton, IntVar


class FilterFrame:
    def __init__(self, master, options):
        self.master = master
        self.options = options
        self.check_vars = []  # 用来存储每个 Checkbutton 的 IntVar

    def create_filter(self):
        # 创建新窗口以显示筛选框
        filter_window = Toplevel(self.master)
        filter_window.title("筛选选项")
        self.check_vars.clear()
        # 创建 Checkbutton
        for option in self.options:
            var = IntVar()  # 创建 IntVar 变量
            self.check_vars.append(var)  # 存储 IntVar
            cb = Checkbutton(filter_window, text=option, variable=var)
            cb.pack(anchor='w')  # 最左侧对齐

        # 提交按钮
        confirm_button = tk.Button(filter_window, text="确认选择", command=self.confirm_selection)
        confirm_button.pack(pady=10)

    def confirm_selection(self):
        selected_options = []
        for i, var in enumerate(self.check_vars):
            if var.get() == 1:
                selected_options.append(self.options[i])

        print("您选择了:", selected_options)
        print("-------")
    # 主程序


if __name__ == "__main__":
    root = tk.Tk()
    root.title("筛选框示例")
    root.geometry("750x500")

    options = ["选项 1", "选项 2", "选项 3", "选项 4", "选项 5"]
    filter_frame = FilterFrame(root, options)

    # 打开筛选框的按钮
    button = tk.Button(root, text="打开筛选框", command=filter_frame.create_filter)
    button.pack(pady=20)

    root.mainloop()
