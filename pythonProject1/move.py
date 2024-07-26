import os.path
import threading
import tkinter
from idlelib import tree
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog, ttk
import shutil
import pandas as pd
import datetime
import uuid

# 变量定义区域
MAC_num = 1  # MAC地址
NAME_num = 2  # 文件名称
PATH_num = 3  # 文件路径
USERNAME_num = 4  # 用户全名
TYPE_num = 5  # 文档类型

# 主窗口
root = Tk()
root.title("我的窗口")
# root.iconbitmap("my_icon.ico")
root.geometry("1000x750")  # 宽度*高度
root.resizable(False, False)

var = tkinter.StringVar()
var.set("导入文件")
var1 = tkinter.StringVar()
var1.set("移动文件")

frame = tkinter.Frame(root)
frame.pack(fill="both", expand=True)

# 创建Treeview控件
tree = ttk.Treeview(frame)

# 创建垂直滚动条
vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
vsb.pack(side="right", fill="y")

# 创建水平滚动条
hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
tree.configure(xscrollcommand=hsb.set)
hsb.pack(side="bottom", fill="x")

# 将Treeview放入Frame中
tree.pack(fill="both", expand=True)

# 定义路径标签
path = tkinter.Label(root, text="")
folder_path2 = ""  # 存放文件路径所在文件夹
data = []  # 存放excel数据，二维列表
title = []  # excel字段名
use_data = []  # excel数据  一边是源文件路径，另一边是移动后的路径
MAC = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2 * 6, 2)][::-1])
MAC = MAC.upper()
back_bool = False  # false说明不能回退，true说明可回退
type_name = []  # 存放文件类型,没有重复
selected_options = []  # 筛选过后的文件类型


def load():
    # 打开文件对话框选择Excel文件
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        print("123")
        # 清空Treeview
        for item in tree.get_children():
            tree.delete(item)
        # 设置Treeview的列
        tree["column"] = list(df.columns)
        tree["show"] = "headings"
        global title, data
        title.clear()
        data.clear()
        for index, col in enumerate(tree["columns"]):  # tree存放excel字段名
            tree.heading(col, text=col)
            title.append(col)
            # print(col)
        print(title)
        global MAC_num, NAME_num, PATH_num, USERNAME_num, new_path1, TYPE_num
        for i in range(len(title)):
            if title[i] == "MAC地址":
                MAC_num = i
            elif title[i] == "文件名称":
                NAME_num = i
            elif title[i] == "文件路径":
                PATH_num = i
            elif title[i] == "用户全名":
                USERNAME_num = i
            elif title[i] == "文档类型":
                TYPE_num = i
        # 插入数据到Treeview中
        for index, row in df.iterrows():
            if row.iloc[MAC_num] != MAC:
                continue
            tree.insert("", "end", values=list(row))
            # print(index, " ", list(row))
            data.append(list(row))  # 保存数据到data
            if row.iloc[TYPE_num] not in type_name:
                type_name.append(row.iloc[TYPE_num])
        print("自动识别---")
        print("mac:", MAC_num + 1, "path:", PATH_num + 1, "name:", NAME_num + 1, "文档类型列数: ", TYPE_num + 1)
        print("文档类型:", type_name)


def select():
    folder_path = filedialog.askdirectory()
    global folder_path2
    if folder_path:
        path.config(text="当前路径为:" + folder_path)
        folder_path2 = folder_path


def copy():
    f: bool = False
    print("当前选择的文件类型:", selected_options)
    res = messagebox.askyesno("警告", "是否确认将文件移动到新文件夹？")
    if res:
        global use_data, new_path1, back_bool

        print("-----------------------------------------")
        txt = str(datetime.datetime.now())
        txt += "\n"
        for i in range(len(data)):
            path = str(data[i][PATH_num])  # 文件路径
            res = str(data[i][NAME_num])  # 文件名称
            file = os.path.join(path, res)  # 文件具体路径
            # folder path是准备存放的文件夹路径
            name = str(data[i][MAC_num])
            name = name.replace(":", "")
            name = data[i][USERNAME_num] + name  # name : 用户名称+mac地址

            new_path1 = os.path.join(folder_path2, str(name))  # 新文件夹路径
            new_path1 = os.path.normpath(new_path1)
            new_path1 = new_path1.replace("\\", "/")
            new_path1 = new_path1.replace("//", "/")

            new_path = os.path.join(new_path1, res)  # 新文件路径
            new_path = os.path.normpath(new_path)
            new_path = new_path.replace("\\", "/")

            # print("MAC：" + str(data[i][MAC_num]))
            print(new_path1)
            print("当前文件路径为：" + new_path, end="\n")
            if data[i][TYPE_num] not in selected_options:
                print("文件: " + file + "不属于您选择的文件类型")
                print("-----------------------------------------")
                continue
            if not os.path.exists(file):
                print("文件: " + file + "不存在！")
                messagebox.showwarning("警告", "文件: " + file + "不存在！")
                print("-----------------------------------------")
                txt += "文件: " + file + "不存在！" + "\n"
                txt += "-----------------------------------------" + "\n"
                continue
            if os.path.exists(new_path):
                filename = res.split(".")[0]
                print("文件发生重名，文件名为：" + filename)
                c = 1
                new_path = new_path1 + "/" + filename + "(" + str(c) + ")." + res.split(".")[1]
                while os.path.exists(new_path):
                    c += 1
                    new_path = new_path1 + "/" + filename + "(" + str(c) + ")." + res.split(".")[1]
                shutil.move(file, new_path)
                txt += "检查到目标文件夹已存在，已为您重新创建，路径为：" + new_path + "\n"
                txt += "-----------------------------------------" + "\n"
                print("检查到目标文件夹已存在，已为您重新创建，路径为：" + new_path)
                print("-----------------------------------------")
                # 加载撤回数据
                use_data.append([])
                use_data[len(use_data) - 1].append(file)
                use_data[len(use_data) - 1].append(new_path)
                continue
            if not os.path.exists(new_path1):
                os.makedirs(new_path1)
                print("检查到没有目标文件夹，已为您重新创建")
                txt += "检查到没有目标文件夹，已为您重新创建" + "\n"

            try:
                if not f:
                    use_data.clear()
                    f = True
                shutil.move(file, new_path)
                print("文件: " + res + "已移动到" + new_path)
                use_data.append([])
                use_data[len(use_data) - 1].append(file)
                use_data[len(use_data) - 1].append(new_path)
            except Exception as e:
                messagebox.showerror("出现错误", e)
                txt += "出现错误" + "\n"
                print(e)
            print("-----------------------------------------")
            txt += "文件:" + file + " 已为您移动到:" + new_path1 + "  路径下" + "\n"
            txt += "-----------------------------------------" + "\n"
            print("开始输出txt:")
            print(txt)
            with open("log.txt", 'a', encoding='utf-8') as fi:
                print("开始编辑log----")
                fi.write(txt)
        messagebox.showinfo("提示", "操作已经完成，请查看具体路径")
        back_bool = True
    else:
        print("选择了取消")


def open_log():
    if not os.path.exists("log.txt"):
        # 创建并打开一个文件以进行写入
        with open('log.txt', 'w') as file:
            # 向文件写入内容
            file.write(' ')
            print("日志文件不存在，已为您创建")
            os.startfile("log.txt")
    else:
        os.startfile("log.txt")


def backevent():
    global use_data, back_bool
    res = messagebox.askyesno("警告", "是否确认回退上一次移动？")
    if res:
        print(use_data)
        if not back_bool or use_data == []:
            messagebox.showwarning("警告", "没有可回退的文件！")
            return
        else:  # back_bool = TRUE
            back_bool = False
            for i in range(len(use_data)):
                origin_file = use_data[i][0]
                remove_file = use_data[i][1]
                shutil.move(remove_file, origin_file)
            messagebox.showinfo("提示", "文件已为您回退上一次移动")
            use_data.clear()
    else:
        print("选择了取消")


# 清空日志
def clear_log():
    with open("log.txt", 'w', encoding='utf-8') as f:
        f.write("")


# 筛选框部分代码
class FilterFrame:
    def __init__(self, master, options):
        self.master = master
        self.options = options
        self.check_vars = []  # 用来存储每个 Checkbutton 的 IntVar
        self.filter_window = None  # 用于存储弹窗的引用

    def create_filter(self):
        # 创建新窗口以显示筛选框
        self.filter_window = Toplevel(self.master)
        self.filter_window.title("筛选选项")
        self.filter_window.geometry("300x300")
        self.check_vars.clear()
        # 创建 Checkbutton
        for option in self.options:
            var = IntVar()  # 创建 IntVar 变量
            var.set(1)
            self.check_vars.append(var)  # 存储 IntVar
            cb = Checkbutton(self.filter_window, text=option, variable=var)
            cb.pack(anchor='w')  # 最左侧对齐

        # 提交按钮
        confirm_button = tkinter.Button(self.filter_window, text="确认选择", command=self.confirm_selection)
        confirm_button.pack(pady=10)

    def confirm_selection(self):
        global selected_options
        selected_options = []
        for i, var in enumerate(self.check_vars):
            if var.get() == 1:
                selected_options.append(self.options[i])
        print("您选择了:", selected_options)
        print("-------")

        # 销毁弹窗
        if self.filter_window is not None:
            self.filter_window.destroy()
            self.filter_window = None  # 清空引用


# 测试代码
filter_frame = FilterFrame(root, type_name)  # 创建 FilterFrame 对象

Bu1 = Button(root, text="导入文件", cursor="hand2", command=load)
Bu2 = Button(root, text="开始移动", cursor="hand2", command=copy)
Bu3 = Button(root, text="选择存放文件路径", cursor="hand2", command=select)
Bu4 = Button(root, text="回退上一次移动", cursor="hand2", command=backevent)
Bu5 = Button(root, text="打开日志", cursor="hand2", command=open_log)
Bu6 = Button(root, text="清空日志", cursor="hand2", command=clear_log)
Bu7 = Button(root, text="开始筛选", cursor="hand2", command=filter_frame.create_filter)
tree.place(y=200, x=0, width=1000, height=500)
Bu1.place(x=100, y=100)
Bu2.place(x=520, y=100)
Bu3.place(x=250, y=100)
Bu4.place(x=700, y=100)
Bu5.place(x=700, y=50)
Bu6.place(x=800, y=50)
Bu7.place(x=400, y=100)
path.place(x=300, y=150)

mainloop()
