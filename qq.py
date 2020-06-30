from selenium import webdriver
from bs4 import BeautifulSoup
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
import time
import re
import win32api
import win32con
import tkinter
 
 
class Gui(object):
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry("320x400+800+400")
        self.root.title('自动发送邮件')
        # 标签控件
        # 邮件号
        self.label_yj = tkinter.Label(master=self.root, text='邮件号:')
        self.label_yj.grid(row=0, column=0)
        # 间谍号
        self.label_jd = tkinter.Label(master=self.root, text='间谍号:')
        self.label_jd.grid(row=1, column=0)
        # 目标群
        self.label_mb = tkinter.Label(master=self.root, text='目标群:')
        self.label_mb.grid(row=2, column=0)
        # 授权码
        self.label_sq = tkinter.Label(master=self.root, text='授权码:')
        self.label_sq.grid(row=3, column=0)
        # 邮件标题
        self.label_bt = tkinter.Label(master=self.root, text='邮件标题:')
        self.label_bt.grid(row=4, column=0)
        # 邮件内容
        self.label_nr = tkinter.Label(master=self.root, text='邮件内容:')
        self.label_nr.grid(row=5, column=0)
        # 发送记录
        self.label = tkinter.Label(master=self.root, text='发送记录:')
        self.label.grid(row=7, column=0)
 
        # 输入控件
        # 邮件号
        self.entry_yj = tkinter.Entry(master=self.root)
        self.entry_yj.grid(row=0, column=1)
        # 间谍号
        self.entry_jd = tkinter.Entry(master=self.root)
        self.entry_jd.grid(row=1, column=1)
        # 目标群
        self.entry_mb = tkinter.Entry(master=self.root)
        self.entry_mb.grid(row=2, column=1)
        # 授权码
        self.entry_sq = tkinter.Entry(master=self.root)
        self.entry_sq.grid(row=3, column=1)
        # 邮件标题
        self.entry_bt = tkinter.Entry(master=self.root)
        self.entry_bt.grid(row=4, column=1)
        # 邮件内容
        self.entry_nr = tkinter.Entry(master=self.root)
        self.entry_nr.grid(row=5, column=1)
 
        # 按钮控件
        # 提交信息按钮
        self.button_tj = tkinter.Button(master=self.root, text='开始运行', command=(self.entry, self.delete))
        self.button_tj.grid(row=6, column=0)
        # 停止按钮
        self.button_tz = tkinter.Button(master=self.root, text='停止发送', command=self.root.quit)
        self.button_tz.grid(row=6, column=1)
        # 清空内容
        self.button_tz = tkinter.Button(master=self.root, text='清空', command=self.delete)
        self.button_tz.grid(row=6, column=2)
 
        # 列表框控件
        self.listbox = tkinter.Listbox(master=self.root, width=45, height=10)
        self.listbox.grid(rowspan=4, columnspan=4)
 
        self.root.mainloop()
 
    # 清空输入框
    def delete(self):
        self.entry_yj.delete(0, 'end')
        self.entry_jd.delete(0, 'end')
        self.entry_mb.delete(0, 'end')
        self.entry_sq.delete(0, 'end')
        self.entry_bt.delete(0, 'end')
        self.entry_nr.delete(0, 'end')
 
    # 发送邮件
    def entry(self):
        win32api.MessageBox(0, "点击确定之后开始获取信息\n请安静等待浏览器自动关闭", "谢谢合作", win32con.MB_ICONASTERISK)
        oneself = self.entry_yj.get()
        jd = self.entry_jd.get()
        mb = self.entry_mb.get()
        pwd = self.entry_sq.get()
        sub = self.entry_bt.get()
        txt = self.entry_nr.get()
 
        # 调用浏览器并窗口最大化
        driver = webdriver.Chrome()
        driver.maximize_window()
        driver.get('https://qun.qq.com/member.html#gid=%s' % mb)
        # 全局隐式等待30秒
        driver.implicitly_wait(30)
        # 切入
        driver.switch_to.frame('login_frame')
        # 自动登录
        driver.find_element_by_id('img_out_%s' % jd).click()
        # 切出
        driver.switch_to.default_content()
        time.sleep(6)
        # # 控制屏幕滑动，获取更多群员信息
        for ai in range(60):
            print(ai)
            if ai <= 60:
                driver.execute_script("window.scrollTo(0,50000)")
                ai += 10
                time.sleep(1)
        # 获取源码
        res = driver.page_source
        # 关闭浏览器
        driver.quit()
        # 将源代码存入txt文本
        with open(r'.html.txt', 'w', encoding='utf-8') as f:
            f.write(res)
        f.close()
        # 读取txt文本
        with open(r'.html.txt', 'r', encoding='utf-8') as f:
            res = f.read()
        # 遍历文档
        soup = BeautifulSoup(res, "html.parser")
 
        # # 取QQ号码
        fall = soup.find_all(class_='td-user-nick')
        tyt = re.findall(';nk=([1-9]\d*)&amp;', '%s' % fall)
 
        # 迭代输出所有群员QQ号码
        for i in range(len(tyt)):
 
            with open(r'.html.txt', 'w', encoding='utf-8') as f:
                f.write(res)
            f.close()
            email_from = "%s@qq.com" % oneself  # 改为自己的发送邮箱
            email_to = "%s@qq.com" % tyt[i]  # 接收邮箱
 
            hostname = "smtp.qq.com"  # 不变，QQ邮箱的smtp服务器地址
            login = "%s@qq.com" % oneself  # 发送邮箱的用户名
            password = pwd  # 发送邮箱的密码，即开启smtp服务得到的授权码。注：不是QQ密码。
            subject = sub  # 邮件主题
            text = txt  # 邮件正文内容
 
            smtp = SMTP_SSL(hostname)  # SMTP_SSL默认使用465端口
            smtp.login(login, password)
 
            msg = MIMEText(text, "plain", "utf-8")
            msg["Subject"] = Header(subject, "utf-8")
            msg["from"] = email_from
            msg["to"] = email_to
 
            smtp.sendmail(email_from, email_to, msg.as_string())
            smtp.quit()
            self.listbox.insert('end', '%s@qq.com发送邮件成功' % tyt[i])
            self.listbox.see('end')
            self.listbox.update()
            time.sleep(1)
 
 
if __name__ == '__main__':
    Gui().entry()
