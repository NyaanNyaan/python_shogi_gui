from PIL import Image
import os
import sys


def imgsplit(im, num):
    if(not 0 <= num <= 31):
        raise ValueError
    height = 90
    width = 81
    h1 = num // 8
    w1 = num % 8
    w2 = w1 * width
    h2 = h1 * height
    c = im.crop((w2, h2, width + w2, height + h2))
    return c


def komaimgset():
    im = Image.open('.\\common\\koma.gif')
    komaimg = {}
    komaimg['K'] = imgsplit(im, 8)
    komaimg['R'] = imgsplit(im, 1)
    komaimg['B'] = imgsplit(im, 2)
    komaimg['G'] = imgsplit(im, 3)
    komaimg['S'] = imgsplit(im, 4)
    komaimg['N'] = imgsplit(im, 5)
    komaimg['L'] = imgsplit(im, 6)
    komaimg['P'] = imgsplit(im, 7)
    komaimg['+R'] = imgsplit(im, 9)
    komaimg['+B'] = imgsplit(im, 10)
    komaimg['+S'] = imgsplit(im, 12)
    komaimg['+N'] = imgsplit(im, 13)
    komaimg['+L'] = imgsplit(im, 14)
    komaimg['+P'] = imgsplit(im, 15)
    komaimg['k'] = imgsplit(im, 16)
    komaimg['r'] = imgsplit(im, 17)
    komaimg['b'] = imgsplit(im, 18)
    komaimg['g'] = imgsplit(im, 19)
    komaimg['s'] = imgsplit(im, 20)
    komaimg['n'] = imgsplit(im, 21)
    komaimg['l'] = imgsplit(im, 22)
    komaimg['p'] = imgsplit(im, 23)
    komaimg['+r'] = imgsplit(im, 25)
    komaimg['+b'] = imgsplit(im, 26)
    komaimg['+s'] = imgsplit(im, 28)
    komaimg['+n'] = imgsplit(im, 29)
    komaimg['+l'] = imgsplit(im, 30)
    komaimg['+p'] = imgsplit(im, 31)
    return komaimg
