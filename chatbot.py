from tkinter import *
from tkinter.simpledialog import *  # 기본 대화 상자와 편리 함수
from tkinter import messagebox # 표준 Tk 대화 상자에 액세스
import textwrap # for 문 사용하는 코딩의 양을 줄일 수 있음
global input_msg
##global chat
##chat = []
## 함수 선언 부분 ##

class Chatting:

      def __init__(self,master,message="입력하시오."):
         self.master = master
         # 말풍선 테두리 부분 
         self.frame = Frame(master,bg="#79ABFF")
         self.i = self.master.create_window(80, 490, window=self.frame)
        
         # 말풍선 네모칸 부분
         # sticky = 차지하는 공간 내의 위치 (E,W,S,N,NE,NW,SF,SW)
         Label(self.frame, text=textwrap.fill(message, 30), font=("경기천년제목 Light", 10),
               bg="#79ABFF").grid(row=1, column=0, sticky="w",padx=5, pady=3)
         
         window.update_idletasks()
         # 말풍선 뾰족한 부분
         self.master.create_polygon(self.draw_triangle(self.i), fill="#79ABFF", outline="#79ABFF")
            
      def draw_triangle(self, widget) :
           x1, y1, x2, y2 = self.master.bbox(widget)
           return x1, y2 -10, x1 - 15, y2 + 10, x1, y2
## 영화 선택 부분 ##
def send_message() :
     global input_msg
     if chat:
         canvas.move(ALL, 0, -80) 
     a = Chatting(canvas, message=entry.get())
     chat.append(a)
     input_msg=entry.get()
# Enter 키
def R_send_message(event):
    global input_msg
    if chat:
        canvas.move(ALL, 0, -80) 
    a = Chatting(canvas, message=entry.get())
    chat.append(a)
    input_msg=entry.get()
window = Tk()
window.title("Chatbot")
window.geometry("500x600")
window.config(bg = "white")
# 윈도우 창 크기 조절 가능
window.resizable(True, True)

## 대화 창 부분 ##

#채팅 바탕을 선, 다각형, 원등을 그릴 수 있는 canvas 이용
canvas = Canvas(window, width=200, height=200, bg="#D3FFFF")
canvas.place(x=50, y=10, width=390, height=530)

     
# 마우스 왼쪽 키

entry = Entry(window,width=26, font=("경기천년제목 Light", 13), relief ="solid")
entry.place(x=50, y=550, width=290, height=40)

# 클릭과 Enter 키 둘다 이용가능
buton = Button(window, width=9, height=2, relief='raised', command = send_message)
window.bind('<Return>', R_send_message)

buton.config(text='SEND', bg="#8BBDFF", font=("경기천년제목 Light",10 ,"bold"))
buton.place(x=360, y=550)

window.mainloop()
