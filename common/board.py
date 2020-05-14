from PIL import Image, ImageTk
import tkinter as tk
import time
import shogi
import common.imgset as imgset
import common.infoparser as infoparser
import iolib.usi as usi
from common.vec2d import Vec
from config import *

# todo : 実装をマシにする
class ShogiBoard(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, width=CANVAS_SIZE[0], height=CANVAS_SIZE[1])

        # 盤面の駒画像
        self.img = [[0] * 10 for i in range(11)]
        # 先手の持ち駒の駒画像
        self.senteImg = [0] * 7
        # 後手の持ち駒の駒画像
        self.goteImg = [0] * 7
        # 盤面
        self.board = shogi.Board()
        self.komaimg = imgset.komaimgset()
        self.Value1 = None
        self.Value2 = None
        self.Value3 = None
        self.banDisplay()
        self.komaDisplay()

    def valueToVector(self, val):
        if(val < 100):
            cx = val // 10
            cy = val % 10
            return [(9-cx) * KOMA_SIZE[0], (cy-1) * KOMA_SIZE[1]] + BANMEN_POS
        elif(val // 100 == 1):
            cy = val % 100
            return SENTEMOCHI_POS + [0, (6 - cy) * KOMA_SIZE[1]]
        elif(val // 100 == 2):
            cy = val % 100
            return GOTEMOCHI_POS + [0, cy * KOMA_SIZE[1]]
        else:
            raise ValueError('ValueToVector(): incorrect value')

    def piece(self, x, y):
        koma = self.board.piece_at(9 - x + (y - 1) * 9)
        if(koma != None):
            return koma.symbol()
        else:
            return None
    # 手番　先手番 0 後手番 1

    def banDisplay(self):
        BAN_COLOR = '#F9C270'
        self.create_rectangle(
            BANMEN_POS - [10, 10],
            BANMEN_POS + KOMA_SIZE * 9 + [10, 10],
            fill=BAN_COLOR, width=0,
            tag='Board'
        )
        self.create_rectangle(
            SENTEMOCHI_POS,
            SENTEMOCHI_POS + [KOMA_SIZE[0] + MOCHI_LABEL_X, KOMA_SIZE[1] * 7],
            fill=BAN_COLOR, width=0
        )
        self.create_rectangle(
            GOTEMOCHI_POS,
            GOTEMOCHI_POS + [KOMA_SIZE[0] + MOCHI_LABEL_X, KOMA_SIZE[1] * 7],
            fill=BAN_COLOR, width=0
        )
        self.tag_bind('Board', '<Button-1>', self.clickBan)

        for i in range(10):
            self.create_line(
                BANMEN_POS + [i * KOMA_SIZE[0], 0],
                BANMEN_POS + [i * KOMA_SIZE[0], 9 * KOMA_SIZE[1]]
            )
            self.create_line(
                BANMEN_POS + [0, i * KOMA_SIZE[1]],
                BANMEN_POS + [9 * KOMA_SIZE[0], i * KOMA_SIZE[1]]
            )

    def komaDisplay(self):
        if (self.board == None):
            raise ValueError('self.board is empty.')
        # 盤面 i 横軸 j 縦軸
        for i in range(1, 10, 1):
            for j in range(1, 10, 1):
                koma = self.piece(i, j)
                if(koma != None):
                    img_resize = self.komaimg[koma].resize(
                        (KOMA_SIZE[0], KOMA_SIZE[1]), Image.LANCZOS)
                    self.img[i][j] = ImageTk.PhotoImage(img_resize)
                    self.create_image(
                        *([(9 - i) * KOMA_SIZE[0], (j - 1)
                           * KOMA_SIZE[1]] + BANMEN_POS),
                        image=self.img[i][j],
                        tag='koma',
                        anchor=tk.NW
                    )
        list_Mochi = [
            ['P', 'L', 'N', 'S', 'G', 'B', 'R'],
            ['p', 'l', 'n', 's', 'g', 'b', 'r']
        ]
        # 先手の駒台
        for i in range(7):
            if(self.board.pieces_in_hand[0][i + 1]):
                koma = list_Mochi[0][i]
                count = self.board.pieces_in_hand[0][i + 1]
                img_resize = self.komaimg[koma].resize(
                    (KOMA_SIZE[0], KOMA_SIZE[1]), Image.LANCZOS)
                self.senteImg[i] = ImageTk.PhotoImage(img_resize)
                self.create_image(
                    *(SENTEMOCHI_POS + [0, (6 - i) * KOMA_SIZE[1]]),
                    image=self.senteImg[i],
                    tag='smochi',
                    anchor=tk.NW
                )
                self.create_text(
                    *(SENTEMOCHI_POS + [KOMA_SIZE[0], (6 - i)
                                        * KOMA_SIZE[1] + MOCHI_TEXT_SIZE]),
                    text=' x' + str(count),
                    tag='smochi'
                )

        # 後手の持駒
        for i in range(7):
            if(self.board.pieces_in_hand[1][i + 1]):
                koma = list_Mochi[1][i]
                count = self.board.pieces_in_hand[1][i + 1]
                img_resize = self.komaimg[koma].resize(
                    (KOMA_SIZE[0], KOMA_SIZE[1]), Image.LANCZOS)
                self.goteImg[i] = ImageTk.PhotoImage(img_resize)
                self.create_image(
                    *(GOTEMOCHI_POS + [0, i * KOMA_SIZE[1]]),
                    image=self.goteImg[i],
                    tag='gmochi',
                    anchor=tk.NW
                )
                self.create_text(
                    *(GOTEMOCHI_POS + [KOMA_SIZE[0], (i + 1)
                                       * KOMA_SIZE[1] - MOCHI_TEXT_SIZE]),
                    text=' x' + str(count),
                    tag='gmochi'
                )

        # 紐づけ
        self.tag_bind('koma', '<Button-1>', self.clickBan)
        self.tag_bind('smochi', '<Button-1>', self.clickSmochi)
        self.tag_bind('gmochi', '<Button-1>', self.clickGmochi)

    def komaDelete(self):
        self.delete('koma')
        self.delete('smochi')
        self.delete('gmochi')
        self.delete('selection')
        self.delete('Nari')
        self.delete('Nama')

    def clickBan(self, event):
        cx, cy = self.canvasx(event.x), self.canvasy(event.y)
        cx = int(9 - (cx - BANMEN_POS[0]) // KOMA_SIZE[0])
        cy = int((cy - BANMEN_POS[1]) // KOMA_SIZE[1] + 1)
        if(1 <= cx <= 9 and 1 <= cy <= 9):
            if(not ((self.Value1 == None) and (self.board.piece_at(9 - cx + (cy - 1) * 9) == None))):
                self.clickGetValue(cx * 10 + cy)

    def clickSmochi(self, event):
        cy = self.canvasy(event.y)
        cy = int(6 - ((cy - SENTEMOCHI_POS[1]) // KOMA_SIZE[1]))
        print(cy)
        if(0 <= cy <= 6 and self.board.pieces_in_hand[0][cy + 1]):
            self.clickGetValue(100 + cy)

    def clickGmochi(self, event):
        cy = self.canvasy(event.y)
        cy = int((cy - GOTEMOCHI_POS[1]) // KOMA_SIZE[1])
        print(cy)
        if(0 <= cy <= 6 and self.board.pieces_in_hand[1][cy + 1]):
            self.clickGetValue(200 + cy)

    def create_selection(self, val):
        koma_pos = self.valueToVector(val)
        self.create_rectangle(
            koma_pos + [1, 1],
            koma_pos + KOMA_SIZE,
            fill='#E60000', width=0,
            tag='selection'
        )
        self.komaDisplay()

    def create_narinama(self, val):
        koma_pos = self.valueToVector(val)
        self.create_rectangle(
            koma_pos + [1, 1],
            koma_pos + [int(KOMA_SIZE[0] / 2), KOMA_SIZE[1]],
            fill='#FF0000', width=0,
            tag='Nari'
        )
        self.create_rectangle(
            koma_pos + [int(KOMA_SIZE[0] / 2), 0],
            koma_pos + KOMA_SIZE,
            fill='#000000', width=0,
            tag='Nama'
        )
        self.tag_bind('Nari', '<Button-1>', self.clickNari)
        self.tag_bind('Nama', '<Button-1>', self.clickNama)

    def clickNari(self, event):
        self.Value3 = 'Nari'
        self.teInputbyGui()

    def clickNama(self, event):
        self.Value3 = 'Nama'
        self.teInputbyGui()

    def isKanari(self):
        if(self.Value1 >= 100 or self.Value1 == None):
            return False
        if(self.Value2 >= 100 or self.Value2 == None):
            return False
        if(len(self.piece(self.Value1 // 10, self.Value1 % 10)) == 2):
            return False
        if (self.piece(self.Value1 // 10, self.Value1 % 10) in ['G', 'g', 'K', 'k']):
            return False
        teban = (self.piece(self.Value1 // 10, self.Value1 % 10) ==
                 self.piece(self.Value1 // 10, self.Value1 % 10).lower()
                 )
        if(teban == False):
            return True if (1 <= min(self.Value1 % 10, self.Value2 % 10) <= 3) else False
        else:
            return True if (7 <= max(self.Value1 % 10, self.Value2 % 10) <= 9) else False

    def clickGetValue(self, val):
        print(val)
        if(self.Value1 == None):
            if(val < 100 and (0 if (self.piece(val // 10, val % 10) != self.piece(val // 10, val % 10).lower()) else 1) != self.board.turn):
                pass
            elif(val >= 100 and (val // 100) + (1 - self.board.turn) != 2):
                pass
            else:
                self.Value1 = val
                self.create_selection(val)
        else:
            if(self.Value2 != None):
                pass
            elif(self.Value1 >= 100 and (val < 100 and (self.piece(val // 10, val % 10) != None))):
                pass
            elif(val == self.Value1):
                self.Value1 = None
                self.delete('selection')
            elif(val < 100):
                self.Value2 = val
                if self.isKanari() == True:
                    if not shogi.Move.from_usi(self.te_usi()) in self.board.legal_moves:
                        self.teInputbyGui()
                    else:
                        self.Value3 == 'Machi'
                        self.create_narinama(val)
                else:
                    self.teInputbyGui()

    def te_usi(self):
        list_Mochi = ['P', 'L', 'N', 'S', 'G', 'B', 'R']
        retsu = '-abcdefghi'
        ret = ''
        # 1,2文字目
        if(self.Value1 < 100):
            ret += str(self.Value1 // 10)
            ret += retsu[self.Value1 % 10]
        else:
            ret += list_Mochi[self.Value1 % 100]
            ret += '*'
        # 3,4文字目
        ret += str(self.Value2 // 10)
        ret += retsu[self.Value2 % 10]
        # 5文字目
        if(self.Value3 == 'Nari'):
            ret += '+'
        print(ret)
        return ret

    def teInputbyGui(self):
        te = self.te_usi()
        if(shogi.Move.from_usi(te) in self.board.legal_moves):
            self.board.push_usi(te)
        else:
            print('Illegal Move')
        self.Value1 = None
        self.Value2 = None
        self.Value3 = None
        self.komaDelete()
        self.komaDisplay()
