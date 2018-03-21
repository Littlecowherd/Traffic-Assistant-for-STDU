#!usr/bin/env python3
# -*- coding:utf-8 -*-
"""
- author  : 小么小儿郎EL
- email   : Littlecowherd@protonmail.com
- date    : 2018年3月19日
- version : beta2.0
— update  : UI全面优化，功能更加完善，解决关闭后不能进程不会接受的历史遗留问题
# 目标功能：记住密码，并设计一个简单的保存密码的算法（已实现：2018年3月19日15:07:43）
"""
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import string
import requests
from tkinter.ttk import *
import getpass
import random

try:
    import cookielib
except:
    import http.cookiejar as cookielib
from bs4 import *
import re

# 获取当前系统用户名
user_name = getpass.getuser()
# 获取系统桌面目录
desktop_dir = 'C:\\Users\\' + user_name + '\\Desktop'

# 构造request headers
agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'

headers = {
    "Host": "info.stdu.edu.cn",
    "Referer": "http://info.stdu.edu.cn/",
    'User-Agent': agent
}

# 使用登录cookie信息
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='td_cookies')
try:
    session.cookies.load(filename='td_cookies', ignore_discard=True)
except Exception as error:
    info = "Cookie 未能加载"
    # messagebox.showerror("提示", info)
    # print('error %s ' % error)


# 获取网页中的动态参数variable
def get_variable():
    '''<input name="cfea68414735a52fc6070a1a78226d1b
                    93a12d69fd0c7d1185f78db176806d56
                    eee0c6762f9f608d9e0fee6ca377c053
                    " type="hidden" value="1"> 是一个动态变化的参数'''
    index_url = 'http://info.stdu.edu.cn/'
    # 获取登录时需要用到的variable
    index_page = session.get(index_url, headers=headers)
    html = index_page.text
    pattern = r'name="(\w*)" value="1"'
    # 这里的variable 返回的是一个list
    variable = re.findall(pattern, html)
    # print(variable[0])
    return variable[0]


# 登录
def login():
    # 通过输入的用户名判断是否是学号
    flag = 1
    if re.match(r"\d{8}$", username.get()):
        post_url = 'http://info.stdu.edu.cn/index.php'
        # print(username.get())
        # print(password.get())
        postdata = {
            'username': username.get(),
            'password': password.get(),
            'Submit': '登录',
            'option': 'com_users',
            'task': 'user.login',
            'return': 'aW5kZXgucGhwP0l0ZW1pZD0xMDE=',
            get_variable(): 1,
        }
    else:
        info = "你的账号输入有误，请重新登录"
        messagebox.showerror(title='提示信息', message=info)
        flag = 0

    if flag:
        with open('cookies', 'w') as fp:
            fp.write(username.get())
            if password_check.get():
                confuse = []
                for i in range(150):
                    num = random.randint(000000, 999999)
                    confuse.append(str(num))
                # fp.write(confuse)
                key = random.randint(10, 99)
                # print(key)
                confuse[key] = password.get()
                key_e = key * 10000 + key * 66 + key * 4
                confuse.append(str(key_e))
                w_confuse = ','.join(confuse)
                fp.write('-'+w_confuse)
    login_page = session.post(post_url, data=postdata, headers=headers)
    # print(login_page)
    session.cookies.save()

    # 隐藏窗口
    root.withdraw()
    if check():
        pass
        """1、不带括号时，调用的是这个函数本身 
           2、带括号（此时必须传入需要的参数），调用的是函数的return结果"""
        root.destroy()  # 登录成功之后将登录窗口关闭
        get_info()  # 调用主函数，显示主面板
    else:
        info = '账号或密码错误，请重新登录'
        messagebox.showerror(title='错误', message=info)
        # 重新显示登录窗口
        root.deiconify()


def check():
    """把检查登录是否成功单独拿出来做一个函数"""
    url_wg = 'http://info.stdu.edu.cn/index.php/component/gatewayinformation/?view=gatewayinformation'
    s = session.get(url_wg)
    soup = BeautifulSoup(s.content, 'html.parser')

    try:
        title = soup.select('h2')[0].get_text()
        # title = soup.select('h2')返回的是一个列表，没有get_text()方法，必须指定元素
        return 1
    except:
        """在这里弹出提示框的话，会出现一个不相干的窗口，浪费了大量时间
        解决方法：返回0.在上层的判断出弹出提示，还可以实现重新登录"""
        # info = '账号或密码错误，请重新登录'
        # messagebox.showinfo(title='错误', message=info)
        return 0


# 抓取信息
def get_info():
    url_wg = 'http://info.stdu.edu.cn/index.php/component/gatewayinformation/?view=gatewayinformation'
    s = session.get(url_wg)
    soup = BeautifulSoup(s.content, 'html.parser')
    # 获取相关信息
    user = soup.select('#login-form > div.login-greeting')[0].get_text()
    user_name = user.split(" ")[1].strip(string.whitespace).strip('，')
    # 不要忽视掉末尾的空白字符，另外string.punctuation不包含中文标点
    money_left = soup.select('#remain_fee')[0].get_text().strip(
        string.whitespace)
    data_left = soup.select('#remain_flow')[0].get_text().strip(
        string.whitespace)
    money_used = soup.select('#this_month_consume')[0].get_text().strip(
        string.whitespace)
    usergroup = soup.select('#curr_group_info')[0].get_text().strip(
        string.whitespace)
    phone = soup.select('#phone')[0].get_text().strip(string.whitespace)
    ip = soup.select('#ip_address')[0].get_text().strip(string.whitespace)
    netmask = soup.select('#gateway')[0].get_text().strip(string.whitespace)  # 网站上掩码和网关的英文名称搞混了
    gateway = soup.select('#netmask')[0].get_text().strip(string.whitespace)
    dns = soup.select('#mailserver')[0].get_text().strip(string.whitespace)
    wifi = soup.select('#wifi_status')[0].get_text().strip(
        string.whitespace).rstrip('【关闭】')
    roaming_ip = soup.select('#ip_address2')[0].get_text().strip(
        string.whitespace)
    last_login = soup.select('#last_active_time')[0].get_text().strip(
        string.whitespace)
    paylog = soup.select('#last_three_playlog')[0].get_text().strip(
        string.whitespace).split("在")

    # 生成改IP脚本
    def set_ip():
        path = desktop_dir + '\\改IP(右键管理员运行).bat'
        fp = open(path, 'w', encoding='gbk')
        content = '''
    netsh interface IP set address  "以太网"  static %s %s\n\
    netsh interface ip add address  "以太网"  %s gwmetric=1\n\
    netsh interface IP set dns "以太网"  static 114.114.114.114\n\
    netsh interface ip add dns "以太网"  202.206.32.1  index=2
    ''' % (ip, netmask, gateway)
        try:
            fp.write(content)
        finally:
            fp.close()
            messagebox.showinfo(title='提示', message='请到桌面查看！')

    # 恢复U盘隐藏文件
    def recover_u():
        path = desktop_dir + '\\恢复U盘隐藏文件.bat'
        fp = open(path, 'w')
        input_content = '''
    for /f "delims=" %%i in ('dir /ah /s/b') do attrib "%%i" -s -h
    
    goto tips
    
    命令的意思解释：
    for /f "delims=" %%i in 循环
    dir /s显示当前目录及子目录中所有文件
    参数 /ah具有隐藏属性的文件
    参数 /b用短文件名的方式显示
    do attrib "%%i" -s -h 取消这个文件/文件夹的 系统属性 隐藏属性

    :tips'''
        try:
            fp.write(input_content)
        finally:
            fp.close()
            messagebox.showinfo(title='提示', message='请到桌面查看！')

    # 隐藏快捷方式小箭头脚本
    def hide_mark():
        path = desktop_dir + '\\隐藏快捷方式小箭头.bat'
        fp = open(path, 'w')
        command = '''
    reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Icons" /v 29 /d "%systemroot%\system32\imageres.dll,197" /t reg_sz /f
　　taskkill /f /im explorer.exe
　　attrib -s -r -h "%userprofile%\AppData\Local\iconcache.db"
　   del "%userprofile%\AppData\Local\iconcache.db" /f /q
　　start explorer
　　pause'''
        try:
            # content_byte = \
            fp.write(command)
        finally:
            fp.close()
            messagebox.showinfo(title='提示', message='请到桌面查看！')

    # 短信获取相关信息
    def sendSM():
        sm_url = 'http://info.stdu.edu.cn/index.php/component/gatewayinformation/index.php'
        post_data = {
            'userInfo[phone]': phone,
            'userInfo[FreeFee]': money_left,
            'userInfo[roam]': roaming_ip,
            'userInfo[Wifi]': wifi,
            'userInfo[netmask]': netmask,
            'userInfo[gateway]': gateway,
            'userInfo[ip]': ip,
            'option': 'com_gatewayinformation',
            'task': 'SendSM'
        }
        session.post(sm_url, data=post_data, headers=headers)  # 发送请求

    # 使用说明
    def tips():
        info = '改IP脚本目前只支持Win10，需要右键以管理员身份运行。' + '\n' + '恢复U盘脚本需要放到问题U盘里，然后双击即可。'
        messagebox.showinfo(title='提示', message=info)

    # ************************************主界面-详细信息*****************************************
    main = Tk()
    main.title("流量小助手 Beta2.0")
    w = 380
    h = 460
    ws = main.winfo_screenwidth()
    hs = main.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    main.resizable(False, False)
    main.geometry('%dx%d+%d+%d' % (w, h, x, y))

    Label(main, text=user_name + '的计费网关信息', font=('微软雅黑', 12)).pack(ipadx=10, ipady=10)
    """pack的option：-after, -anchor, -before, -expand, -fill, -in, -ipadx, -ipady, -padx, -pady, or -side"""

    traffic = [('剩余金额', money_left),
               ('剩余流量', data_left),
               ('已用金额', money_used),
               ('用户组别', usergroup),
               ('手机号码', phone),
               ('IP地址', ip),
               ('子网掩码', netmask),
               ('默认网关', gateway),
               ('首选DNS', dns),
               ('WiFi开通情况', wifi),
               ('漫游IP地址', roaming_ip),
               ('最近登录', last_login)]
    info_frame = Frame(main)  # info 容器
    info_frame.pack()
    tree = Treeview(info_frame, columns=['info', 'detail'], show='headings', height=12)
    tree.heading('info', text='信息')
    tree.heading('detail', text='详情')
    for item in traffic:
        tree.insert('', 'end', values=item)
    tree.pack(padx=10, pady=10)

    tool_frame = LabelFrame(main, text='实用工具')
    tool_frame.pack()

    top_frame = Frame(tool_frame)
    bot_frame = Frame(tool_frame)
    top_frame.pack(side='top')
    bot_frame.pack()

    left_frame = Frame(bot_frame)
    right_frame = Frame(bot_frame)
    left_frame.pack(side='left')
    right_frame.pack(side='right')

    Button(top_frame, text="短信获取相关信息", command=sendSM, width=25).pack()

    Button(left_frame, text="一键改IP脚本", command=set_ip, width=20).pack()
    Button(left_frame, text="恢复U盘隐藏文件", command=recover_u, width=20).pack()
    Button(right_frame, text="隐藏小箭头", command=hide_mark, width=20).pack()
    Button(right_frame, text="使用说明", command=tips, width=20).pack()

    main.mainloop()


# 根据屏幕大小，调整窗口位置
def center_window(w=300, h=200):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


# 使用说明
def readme():
    info = "账户为学号，密码为校园卡密码" + '\n' \
                              "使用前提 : 连接至校园内网" + '\n 不要随意删除生成的两个文件'\
           '\n\n' + "如有问题请联系：" + \
           '\n' + 'Littlecowherd@protonmail.com'
    messagebox.showinfo(title='使用说明', message=info)


# ******************************登录窗口************************************
root = Tk()
center_window(350, 200)
# 固定窗口大小
root.resizable(False, False)

root.title("流量小助手 Beta2.0")
# frame
login_frame = Frame(root, padding=20)
label_frame = Frame(login_frame)  # label的容器
entry_frame = Frame(login_frame)  # entry的容器
check_frame = Frame(root)
button_frame = Frame(root, padding=10)  # button的容器
login_frame.pack()
label_frame.pack(side='left')
entry_frame.pack(side='right')
check_frame.pack()
button_frame.pack()
# label
Label(label_frame, text='账户名称:', font=('微软雅黑', 11)).pack()
Label(label_frame, text='  ', font=('微软雅黑', 11)).pack()  # 占位
Label(label_frame, text='账户密码:', font=('微软雅黑', 11)).pack()

# 读取密码
try:
    with open('cookies', 'r') as fp:
        ff = fp.read()
    f = ff.split('-')
    account = f[0]
    confuse = f[1].split(',')
    key_d = confuse[-1]
    key = int(key_d[0:2])
    passw = confuse[key]
except Exception as error:
    # print(error)
    account=''
    passw = ''

# entry
e = StringVar()
username = Entry(entry_frame, font=('微软雅黑', 11), textvariable=e)
e.set(account)
username.pack()
Label(entry_frame, text='  ', font=('微软雅黑', 11)).pack()  # 占位
p = StringVar()
password = Entry(entry_frame, show='*', font=('微软雅黑', 11), textvariable=p)
p.set(passw)
password.pack()
password.bind("<Return>", lambda event: login())  # 注意，绑定回车的是密码输入框，而不是登录按钮

# checkbox
password_check = IntVar()  # 通过get来获取状态，0表示未选取
check_ = tk.Checkbutton(check_frame, text='记住密码', variable=password_check)
check_.select()
check_.pack()
# 按钮
Button(button_frame, text='登录', command=login, width=15).pack(side='left')
Label(button_frame, text='      ').pack(side='left')  # 占位
Button(button_frame, text='使用说明', command=readme, width=15).pack(side='right')

root.mainloop()
