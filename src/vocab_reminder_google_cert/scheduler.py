import datetime
import threading
import schedule  # type: ignore
import time
import logging
from tkinter import Tk, Toplevel, Label, Button, messagebox, simpledialog
from tkinter.ttk import Progressbar
from typing import Optional
from .main import VocabReminder
import sys
# 邮箱配置（启用请填写真实信息）
"""
EMAIL_CONFIG = {
    'smtp_server': 'smtp.example.com',
    'port': 587,
    'username': 'your_email@example.com',
    'password': 'your_app_password',
    'from': 'vocab_reminder@example.com',
    'to': 'user@example.com'
}
"""
# 配置日志
logging.basicConfig(
    filename='data/reminder.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class ReminderGUI:
    def __init__(self, master: Tk):
        self.master = master
        self.master.title("单词提醒 ⏰")
        self.master.attributes('-topmost', True)
        try:
            self.vr = VocabReminder()
        except Exception as e:
            logging.error("初始化失败", exc_info=True)
            messagebox.showerror(
                "初始化错误",
                f"系统启动失败，请查看日志文件 data/reminder.log\n\n错误详情: {str(e)}"
            )
            sys.exit(1)
        self.create_widgets()
        self.master.deiconify()  # 确保窗口显示

    def create_widgets(self) -> None:
        """创建界面组件"""
        self.label = Label(self.master, text="⏰ 背诵时间到！", font=('Arial', 16))
        self.btn_review = Button(self.master, text="立即复习", command=self.start_review, width=15)
        self.btn_snooze = Button(self.master, text="推迟提醒", command=self.snooze, width=15)
        self.btn_exit = Button(self.master, text="退出程序", command=self.exit_program, width=15)
        self.progress = Progressbar(self.master, length=200, mode='indeterminate')

        self.label.pack(pady=10)
        self.progress.pack(pady=5)
        self.btn_review.pack(pady=5)
        self.btn_snooze.pack(pady=5)
        self.btn_exit.pack(pady=5)

        self.progress.start()
        self.master.after(2000, lambda: self.progress.stop())

    def start_review(self) -> None:
        """开始复习流程"""
        self.master.destroy()
        root = Tk()
        app = VocabGUI(root, self.vr)
        root.mainloop()

    def snooze(self) -> None:
        """推迟提醒"""
        self.master.withdraw()
        minutes = simpledialog.askinteger(
            "推迟提醒",
            "请输入推迟分钟数（1-1440）:",
            parent=self.master,
            minvalue=1,
            maxvalue=1440
        )
        self.master.deiconify()

        if minutes:
            self.reschedule_reminder(minutes)

    def reschedule_reminder(self, minutes: int) -> None:
        """重新调度提醒"""
        global job
        if job:
            job.cancel()

        new_time = (datetime.datetime.now() + datetime.timedelta(minutes=minutes))
        schedule.every().day.at(new_time.strftime("%H:%M")).do(send_reminder).tag('snoozed')
        messagebox.showinfo("已推迟", f"下次提醒将在 {new_time.strftime('%H:%M')}")

    def exit_program(self) -> None:
        """退出程序"""
        global keep_running
        keep_running = False
        self.master.destroy()

class VocabGUI:
    def __init__(self, master: Tk, vr: VocabReminder):
        self.master = master
        self.vr = vr
        self.current_word: Optional[str] = None
        self.create_widgets()
        self.load_word()

    def create_widgets(self) -> None:
        """创建复习界面组件"""
        self.master.title("单词背诵助手")
        self.master.geometry("500x300")
        
        self.word_frame = Label(self.master, text="", font=('Arial', 24), wraplength=400)
        self.def_frame = Label(self.master, text="", font=('Arial', 14), wraplength=400, justify='left')
        self.btn_correct = Button(
            self.master,
            text="✅ 记住了",
            command=self.mark_correct,
            width=15,
            bg='#4CAF50',
            fg='white'
        )
        self.btn_wrong = Button(
            self.master,
            text="❌ 没记住",
            command=self.mark_wrong,
            width=15,
            bg='#f44336',
            fg='white'
        )

        self.word_frame.pack(pady=30)
        self.def_frame.pack(pady=10)
        self.btn_correct.pack(side='left', padx=30)
        self.btn_wrong.pack(side='right', padx=30)

    def load_word(self) -> None:
        """加载新单词（添加数据验证）"""
        try:
            if self.vr.get_reviewable_count() == 0:
                messagebox.showinfo("提示", 
                    f"所有单词已安排复习！\n"
                    f"首次复习将在 1 分钟后开始\n"
                    f"（总单词数: {self.vr.get_word_count()}）")
                self.master.destroy()
                return
                
            self.current_word, self.current_def = self.vr.get_random_word()
            self.word_frame.config(text=self.current_word.upper())
            self.def_frame.config(text=self.current_def)
            
        except Exception as e:
            logging.error("加载单词失败", exc_info=True)
            messagebox.showerror("错误", f"初始化失败: {str(e)}")
            self.master.destroy()

    def mark_correct(self) -> None:
        """标记为正确"""
        self.vr.update_review_stats(self.current_word, True)
        self.load_word()

    def mark_wrong(self) -> None:
        """标记为错误"""
        self.vr.update_review_stats(self.current_word, False)
        self.load_word()
 """
    # 已注释的邮件发送功能（保留代码结构）
    def send_email(self, is_correct):
        msg = MIMEText(f"单词: {self.current_word}\n结果: {'正确' if is_correct else '错误'}")
        msg['Subject'] = f"单词复习报告 - {'成功' if is_correct else '需加强'}"
        msg['From'] = EMAIL_CONFIG['from']
        msg['To'] = EMAIL_CONFIG['to']
 
        try:
            with smtplib.SMTP(
                EMAIL_CONFIG['smtp_server'], 
                EMAIL_CONFIG['port']
            ) as server:
                server.starttls()
                server.login(
                    EMAIL_CONFIG['username'],
                    EMAIL_CONFIG['password']
                )
                server.sendmail(
                    EMAIL_CONFIG['from'],
                    [EMAIL_CONFIG['to']],
                    msg.as_string()
                )
            logging.info(f"邮件发送成功: {self.current_word}")
        except Exception as e:
            logging.error(f"邮件发送失败: {str(e)}")
    """
def send_reminder() -> None:
    """发送桌面提醒"""
    try:
        logging.info("尝试发送提醒")
        root = Tk()
        root.withdraw()
        app = ReminderGUI(root)
        root.deiconify()  # 确保窗口显示
        root.mainloop()
    except Exception as e:
        logging.error("提醒失败", exc_info=True)

def remind_to_review() -> None:
    """每分钟提醒测试"""
    logging.info("触发每分钟提醒")
    send_reminder()

def run_scheduler() -> None:
    """运行调度程序"""
    global job, keep_running
    schedule.every(1).minutes.do(remind_to_review)
    keep_running = True

    def schedule_loop() -> None:
        """调度循环"""
        while keep_running:
            schedule.run_pending()
            time.sleep(60)

    # 启动调度线程
    thread = threading.Thread(target=schedule_loop, daemon=True)
    thread.start()

    # 主线程保持运行
    logging.info("单词背诵系统已启动! 每分钟自动提醒（测试模式）")
    print("单词背诵系统已启动! 每分钟自动提醒（测试模式）")
    print("正在运行...（界面自动弹出时请勿关闭终端）")
    
    while keep_running:
        time.sleep(3600)

if __name__ == "__main__":
    run_scheduler()