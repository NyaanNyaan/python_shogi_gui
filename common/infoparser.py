import shogi

piece_to_char = {
    "p": "歩", "l": "香", "n": "桂", "s": "銀", "g": "金", "b": "角", "r": "飛", "k": "玉", "+p": "と", "+l": "成香", "+n": "成桂", "+s": "成銀", "+b": "馬", "+r": "竜"
}
alphabet_to_num = {
    "a": "1", "b": "2", "c": "3", "d": "4", "e": "5", "f": "6", "g": "7", "h": "8", "i": "9"
}


def usi_to_csa(te, board):
    s = "▲" if board.turn == 0 else "△"
    if(te == 'resign'):
        s += "投了"
    elif(te == 'rep_draw'):
        s += "千日手"
    elif(te[0:3] == "rep"):
        s += te
    else:
        if(te[1] == "*"):
            s += te[2] + alphabet_to_num[te[3]]
            s += piece_to_char[te[0].lower()]
        else:
            s += te[2] + alphabet_to_num[te[3]]
            koma = board.piece_at(
                9 - int(te[0]) + (int(alphabet_to_num[te[1]]) - 1) * 9)
            if(koma != None):
                s += piece_to_char[koma.symbol().lower()]
        if(len(te) == 5 and te[4] == "+"):
            s += "成"
        if(te[1] == '*'):
            s += "打"
        else:
            s += "(" + te[0] + alphabet_to_num[te[1]] + ")"
    return s


def info_parser(line, sfen=None):
    args = line.split()
    if(args[0] != 'info'):
        return None
    arg_itr = iter(args)
    depth = 'None'
    seldepth = 'None'
    score = 'None'
    nodes = 'None'
    nps = 'None'
    time = 'None'
    kifu = []
    board = shogi.Board(sfen)
    for arg in arg_itr:
        if(arg == 'depth'):
            depth = next(arg_itr)
        elif(arg == 'seldepth'):
            seldepth = next(arg_itr)
        elif(arg == 'score'):
            score = next(arg_itr)
            if(score == 'mate'):
                score = str(30000 - int(next(arg_itr)))
            elif(score == 'cp'):
                score = next(arg_itr)
            if(board.turn == 1):
                score = str(int(score) * -1)
        elif(arg == 'nodes'):
            nodes = next(arg_itr)
        elif(arg == 'nps'):
            nps = next(arg_itr)
        elif(arg == 'time'):
            time = int(next(arg_itr))
        elif(arg == 'pv'):
            try:
                while True:
                    arg = next(arg_itr)
                    kifu.append(usi_to_csa(arg, board))
                    try:
                        board.push_usi(arg)
                    except ValueError:
                        pass
            except StopIteration:
                pass

    msg = '{:0=2}:{:0=2}:{:0=2}s'.format(
        time // 3600000, (time % 60000) // 1000, (time % 1000) // 10)
    msg += ' 評価値: ' + score
    if(-300 < int(score) < 300):
        msg += "(互角)"
    elif (300 <= int(score) <= 699):
        msg += "(先手有利)"
    elif (700 <= int(score) <= 1499):
        msg += "(先手優勢)"
    elif (1500 <= int(score)):
        msg += "(先手勝勢)"
    elif (-300 >= int(score) >= -699):
        msg += "(後手有利)"
    elif (-700 >= int(score) >= -1499):
        msg += "(後手優勢)"
    elif (-1500 >= int(score)):
        msg += "(後手勝勢)"
    msg += " 局面数: " + nodes + ' NPS: ' + nps
    
    for i in range(len(kifu)):
        if(i % 6 == 0):
            msg += '\n'
        msg += kifu[i]
    return msg


if __name__ == '__main__':
    infoStr = 'info depth 19 seldepth 23 score cp 22 nodes 3520619 nps 1623901 hashfull 36 time 2168 pv 7g7f 3c3d 1g1f 8b4b 6g6f 4c4d 7i7h 4d4e 7h6g 4e4f 4g4f 4b4f 6g5f 4f4b 2h6h 5a6b 3i3h 6b7b 8h7g 7b8b 3h4g'
    InfoParser(infoStr)
