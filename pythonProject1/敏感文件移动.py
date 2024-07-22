import os.path
import tkinter
from idlelib import tree
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog, ttk
import shutil
import pandas as pd

# 变量定义区域

MAC_num = 1
NAME_num = 2
PATH_num = 3
USERNAME_num = 4

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

# macVariable = tkinter.StringVar()
# macVariable.set("mac列数")
# 创建下拉菜单
# mac = ttk.Combobox(root, textvariable=macVariable)

# nameVariable = tkinter.StringVar()
# nameVariable.set("文件名列数")
# name = ttk.Combobox(root, textvariable=nameVariable)
# 放置下拉菜单


# fileVariable = tkinter.StringVar()
# fileVariable.set("路径列数")
# 创建下拉菜单
# filecol = ttk.Combobox(root, textvariable=fileVariable)
#
# mac.pack()
# name.pack()
# filecol.pack()
# mac.place(x=100, y=200)
# name.place(x=300, y=10)
# file.place(x=500, y=10)
# 创建一个Frame来包含Treeview和滚动条
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
use_data = []  # excel数据根据mac筛选后的结果


def init():
    with open("/config.txt", "r") as f:
        data = f.read()
        print(data)


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

        # mac['values'] = title
        # filecol['values'] = title
        # name['values'] = title
        # 插入数据到Treeview中
        for index, row in df.iterrows():
            tree.insert("", "end", values=list(row))
            # print(index, " ", list(row))
            data.append(list(row))  # 保存数据到data
        global MAC_num, NAME_num, PATH_num, USERNAME_num, new_path1
        # MAC_num = int(mac.get())
        # PATH_num = int(filecol.get())
        # NAME_num = int(name.get())
        for i in range(len(title)):
            if title[i] == "MAC地址":
                MAC_num = i
            elif title[i] == "文件名称":
                NAME_num = i
            elif title[i] == "文件路径":
                PATH_num = i
            elif title[i] == "用户全名":
                USERNAME_num = i
        print("自动识别---")
        print("mac:", MAC_num + 1, "path:", PATH_num + 1, "name:", NAME_num + 1)
        # for i in range(len(data)):
        # for j in range(len(data[i])):
        #     print(data[i][j], end=" ")
        # print(data[i])


def select():
    folder_path = filedialog.askdirectory()
    global folder_path2
    if folder_path:
        path.config(text="当前路径为:" + folder_path)
        folder_path2 = folder_path


def copy():
    print("-----------------------------------------")
    for i in range(len(data)):
        path = str(data[i][PATH_num])  # 文件路径
        res = str(data[i][NAME_num])  # 文件名称
        file = os.path.join(path, res)  # 文件具体路径
        # folder path是准备存放的文件夹路径
        name = str(data[i][MAC_num])
        name = name.replace(":", "")
        name = data[i][USERNAME_num] + name  #name : 用户名称+mac地址

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
        if not os.path.exists(file):
            print("文件: " + file + "不存在！")
            messagebox.showwarning("警告", "文件: " + file + "不存在！")
            print("-----------------------------------------")
            continue
        if os.path.exists(new_path):
            print("文件: " + new_path + "已存在！")
            print("-----------------------------------------")
            continue
        if not os.path.exists(new_path1):
            os.makedirs(new_path1)
            print("检查到没有目标文件夹，已为您重新创建")
        try:

            shutil.copy(file, new_path)
            print("文件: " + res + "已移动到" + new_path)
        except Exception as e:
            messagebox.showerror("出现错误", e)
            print(e)
        print("-----------------------------------------")
        os.remove(file)
    messagebox.showinfo("提示", "文件已为您移动到:" + new_path1 + "  路径下")


Bu1 = Button(root, text="导入文件", cursor="hand2", command=load)
Bu2 = Button(root, text="开始移动", cursor="hand2", command=copy)
Bu3 = Button(root, text="选择存放文件路径", cursor="hand2", command=select)
Bu4 = Button(root, text="回退上一次移动", cursor="hand2")
Bu5 = Button(root, text="打开日志", cursor="hand2")
tree.place(y=200, x=0, width=1000, height=500)
Bu1.place(x=100, y=100)
Bu2.place(x=500, y=100)
Bu3.place(x=280, y=100)
Bu4.place(x=700, y=100)
Bu5.place(x=700, y=50)
path.place(x=300, y=150)

mainloop()
