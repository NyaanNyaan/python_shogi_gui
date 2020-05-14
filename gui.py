from PIL import Image, ImageTk
import tkinter as tk
import time
import shogi
import common.imgset as imgset
import common.infoparser as infoparser
import iolib.usi as usi
import common.board as board
from common.vec2d import Vec
from config import *


class BoardDisplay(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=GUI_SIZE[0], height=GUI_SIZE[1])
        self.master.title('Shogi Board')
        self.pack()

        self.board = board.ShogiBoard(master=self)
        self.board.place(x=BOARD_POS[0], y=BOARD_POS[1])
        self.exe = None
        self.sfen = None

        self.buttonMatta = tk.Button(
            text='待った', width=10,
            command=self.push_matta
        )
        self.buttonMatta.place(x=MATTA_POS[0], y=MATTA_POS[1])

        self.buttonExec = tk.Button(
            text='解析', width=15,
            command=self.push_exec
        )
        self.buttonExec.place(x=EXEC_POS[0], y=EXEC_POS[1])

        self.buttonKill = tk.Button(
            text='中断', width=15,
            command=self.kill_exec
        )
        self.buttonKill.place(x=KILL_POS[0], y=KILL_POS[1])

        self.InfoBox = tk.Text(font=('', 15))
        self.InfoBox.mark_set(tk.INSERT, '1.0')
        self.InfoBox.mark_gravity(tk.INSERT, tk.LEFT)
        self.InfoBox.place(
            x=INFO_POS[0], y=INFO_POS[1], width=INFO_SIZE[0], height=INFO_SIZE[1])

    def push_matta(self):
        try:
            last_move = self.board.board.pop()
            self.board.komaDelete()
            print('Undo : ' + last_move.usi())
            self.board.komaDisplay()
        except IndexError:
            pass

    def push_exec(self):
        if(self.exe != None):
            return
        self.exe = usi.UsiWrapper(soft_name, soft_dir, setoption)
        self.sfen = self.board.board.sfen()
        self.read_exec()
        self.exe.go(self.sfen)

    def read_exec(self):
        if(self.exe == None):
            return
        buf = self.exe.receive()
        if(buf != None):
            Info = infoparser.info_parser(buf, self.sfen)
            if(Info != None):
                self.InfoBox.delete(tk.INSERT, tk.END)
                self.InfoBox.insert(tk.INSERT, (Info + '\n'))
        if(self.sfen != self.board.board.sfen()):
            self.exe.stop()
            self.sfen = self.board.board.sfen()
            self.exe.go(self.sfen)
        self.after(10, self.read_exec)

    def kill_exec(self):
        if(self.exe == None):
            return
        self.exe.kill()
        self.exe = None
        print('Terminated Exec')
        time.sleep(0.01)


if __name__ == '__main__':
    boardDisplay = BoardDisplay()
    boardDisplay.mainloop()
