from tkinter import *
from tkinter.simpledialog import *  # 기본 대화 상자와 편리 함수
from tkinter import messagebox # 표준 Tk 대화 상자에 액세스
import textwrap # for 문 사용하는 코딩의 양을 줄일 수 있음
from datetime import datetime

root = Tk()
root.title("Chatbot")
root.config(bg="lightblue")

canvas = Canvas(root, width=400, height=550,bg="white")
canvas.grid(row=0,column=0,columnspan=2)

bubbles = []

class BotBubble:
    def __init__(self,master,message="입력하시오."):
         self.master = master
         # 말풍선 테두리 부분 
         self.frame = Frame(master,bg="light gray")
         self.i = self.master.create_window(100, 490, window=self.frame)
        
         # 말풍선 네모칸 부분
         # sticky = 차지하는 공간 내의 위치 (E,W,S,N,NE,NW,SF,SW)
         Label(self.frame, text=textwrap.fill(message, 8), font=("경기천년제목 Light", 12),
               bg="light gray").grid(row=1, column=0, sticky="w",padx=12, pady=5)
         Label(self.frame,text=datetime.now().strftime("%Y-%m-%d %H:%m"),font=("Helvetica", 7),bg="light gray").grid(row=0,column=0,sticky="e",padx=5)
         root.update_idletasks()
         # 말풍선 뾰족한 부분
         self.master.create_polygon(self.draw_triangle(self.i), fill="light gray", outline="light gray")

    def draw_triangle(self,widget):
        x1, y1, x2, y2 = self.master.bbox(widget)
        return x1, y2 - 10, x1 - 15, y2 + 10, x1, y2
class BotBubble_bot:
    def __init__(self,master,message="입력하시오."):
         self.master = master
         # 말풍선 테두리 부분 
         self.frame = Frame(master,bg="#79ABFF")
         self.i = self.master.create_window(300, 490, window=self.frame)
        
         # 말풍선 네모칸 부분
         # sticky = 차지하는 공간 내의 위치 (E,W,S,N,NE,NW,SF,SW)
         Label(self.frame, text=textwrap.fill(message, 8), font=("경기천년제목 Light", 12),
               bg="#79ABFF").grid(row=1, column=0, sticky="w",padx=12, pady=5)
         Label(self.frame,text=datetime.now().strftime("%Y-%m-%d %H:%m"),font=("Helvetica", 7),bg="#79ABFF").grid(row=0,column=0,sticky="w",padx=5)
         root.update_idletasks()
         # 말풍선 뾰족한 부분
         self.master.create_polygon(self.draw_triangle(self.i), fill="#79ABFF", outline="#79ABFF")
            
    def draw_triangle(self, widget):
           x1, y1, x2, y2 = self.master.bbox(widget)
           return x2, y2 -10, x2 + 15, y2 + 10, x2, y2
def send_message():
    if bubbles:
        canvas.move(ALL, 0, -85)
    a = BotBubble(canvas,message=entry.get())
    bubbles.append(a)
    receive_message(bubbles)
def receive_message(msg):
    canvas.move(ALL, 0, -85)
    a = BotBubble_bot(canvas,message='안녕하세요')
def R_send_message(event):
    if bubbles:
        canvas.move(ALL, 0, -85) 
    a = BotBubble(canvas, message=entry.get())
    bubbles.append(a)
    receive_message(bubbles)
entry = Entry(root,width=26, font=("경기천년제목 Light", 13))
entry.grid(row=1,column=0)
Button(root,text="Send",command=send_message).grid(row=1,column=1)
root.bind('<Return>', R_send_message)
root.mainloop()
