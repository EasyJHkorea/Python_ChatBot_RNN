import tensorflow as tf
import numpy as np
import math
import sys
from tkinter import *
from tkinter.simpledialog import *  # 기본 대화 상자와 편리 함수
from tkinter import messagebox # 표준 Tk 대화 상자에 액세스
import textwrap # for 문 사용하는 코딩의 양을 줄일 수 있음
from datetime import datetime
import image
import pdb
from config_la import FLAGS
from model_la import Seq2Seq
from dialog_la import Dialog
class ChatBot:
    global input_msg,canvas,bubbles,entry,root
    def __init__(self, voc_path, train_dir):
        
        self.dialog = Dialog()
        self.dialog.load_vocab(voc_path)

        self.model = Seq2Seq(self.dialog.vocab_size,output_keep_prob=0.9)
        config = tf.ConfigProto(
            device_count={'GPU': 1}
        )
        self.sess = tf.Session(config=config)
        #self.sess = tf.Session()
        #pdb.set_trace()
        ckpt = tf.train.get_checkpoint_state(train_dir)
        print (ckpt.model_checkpoint_path)
        self.model.saver.restore(self.sess, ckpt.model_checkpoint_path)
    def draw_triangle_S(self, master,widget):
        x1, y1, x2, y2 = master.bbox(widget)
        return x1, y2 - 10, x1 - 15, y2 + 10, x1, y2
    def draw_triangle_R(self, master, widget):
           x1, y1, x2, y2 = master.bbox(widget)
           return x2, y2 -10, x2 + 15, y2 + 10, x2, y2
    def send_message(self):
        global input_msg,canvas,bubbles,entry,root
        if bubbles:
            canvas.move(ALL, 0, -85)
        master = canvas
        message=entry.get()
        # 말풍선 테두리 부분 
        frame = Frame(master,bg="light gray")
        i = master.create_window(100, 490, window=frame)

        Label(frame, text=textwrap.fill(message, 8), font=("경기천년제목 Light", 12),
              bg="light gray").grid(row=1, column=0, sticky="w",padx=12, pady=5)
        Label(frame,text=datetime.now().strftime("%Y-%m-%d %H:%m"),font=("Helvetica", 7),bg="light gray").grid(row=0,column=0,sticky="e",padx=5)
        root.update_idletasks()
        # 말풍선 뾰족한 부분
        master.create_polygon(self.draw_triangle_S(master,i), fill="light gray", outline="light gray")
##        a = BotBubble(canvas,message=entry.get())
        
##        print('######################',bubbles)
        input_msg=entry.get()
        bubbles.append(message)
        if len(bubbles)>=1:
            self.receive_message(input_msg)
        
    def receive_message(self, msg):
        global canvas,root
##        print(msg)
##        line = msg.readline()
        message=self._get_replay(input_msg.strip())
        canvas.move(ALL, 0, -85)
        frame = Frame(canvas,bg="#79ABFF")
        i = canvas.create_window(300, 490, window=frame)
        Label(frame, text=textwrap.fill(message, 8), font=("경기천년제목 Light", 12),
                   bg="#79ABFF").grid(row=1, column=0, sticky="w",padx=12, pady=5)
        Label(frame,text=datetime.now().strftime("%Y-%m-%d %H:%m"),font=("Helvetica", 7),bg="#79ABFF").grid(row=0,column=0,sticky="w",padx=5)
        root.update_idletasks()
        canvas.create_polygon(self.draw_triangle_R(canvas,i), fill="#79ABFF", outline="#79ABFF")
##        a = BotBubble_bot(canvas,message=self._get_replay(line.strip()))
    def R_send_message(self,event):
        global input_msg,canvas,bubbles,entry,root
        if bubbles:
            canvas.move(ALL, 0, -85)
        master = canvas
        message=entry.get()
        # 말풍선 테두리 부분 
        frame = Frame(master,bg="light gray")
        i = master.create_window(100, 490, window=frame)

        Label(frame, text=textwrap.fill(message, 8), font=("경기천년제목 Light", 12),
              bg="light gray").grid(row=1, column=0, sticky="w",padx=12, pady=5)
        Label(frame,text=datetime.now().strftime("%Y-%m-%d %H:%m"),font=("Helvetica", 7),bg="light gray").grid(row=0,column=0,sticky="e",padx=5)
        root.update_idletasks()
        # 말풍선 뾰족한 부분
        master.create_polygon(self.draw_triangle_S(master,i), fill="light gray", outline="light gray")
        input_msg=entry.get()
        bubbles.append(message)
        if len(bubbles)>=1:
            self.receive_message(input_msg)
    def run(self):
        global input_msg,canvas,bubbles,entry,root
        root = Tk()
        root.title("Chatbot")
        root.config(bg="lightblue")

        canvas = Canvas(root, width=400, height=550,bg="white")
        canvas.grid(row=0,column=0,columnspan=2)

        bubbles = []
        entry = Entry(root,width=26, font=("경기천년제목 Light", 13))
        entry.grid(row=1,column=0)
        Button(root,text="Send",command=self.send_message).grid(row=1,column=1)
        root.bind('<Return>', self.R_send_message)
        root.mainloop()
    def _decode(self, enc_input, dec_input):
        if type(dec_input) is np.ndarray:
            dec_input = dec_input.tolist()

        input_len = 20 #int(math.ceil((len(enc_input) + 1) * 1.5))

        enc_forward_input, enc_reverse_input, dec_input, _ = self.dialog.transform(enc_input, dec_input,
                                                        input_len,
                                                        FLAGS.max_decode_len)

        return self.model.predict(self.sess, [enc_forward_input],[enc_reverse_input],  [dec_input])
    def _get_replay(self, msg): # 실제 Reply(응답) 구성하는 부분
        enc_input = self.dialog.tokenizer(msg)
        enc_input = self.dialog.tokens_to_ids(enc_input)
        dec_input = []


        curr_seq = 0
        for i in range(FLAGS.max_decode_len):
            outputs = self._decode(enc_input,dec_input)
            if self.dialog.is_eos(outputs[0][curr_seq]):
                break
            elif self.dialog.is_defined(outputs[0][curr_seq]) is not True:
                dec_input.append(outputs[0][curr_seq])
                curr_seq+=1

        reply = self.dialog.decode([dec_input], True)

        return reply
###########################################################################################

def main():
    print("잠시만 기다려주세요...\n")

    chatbot = ChatBot(FLAGS.voc_path, FLAGS.train_dir)
    chatbot.run()
##if __name__ == "__main__":
##    tf.app.run()
