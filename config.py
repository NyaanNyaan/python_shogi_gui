# ソフトのパス
soft_name = "./YaneuraOu-by-gcc"
# ソフトの置かれているディレクトリ
soft_dir = "./"
# オプション
setoption = [
    "setoption name EvalDir value eval",
    "setoption name BookFile value no_book",
    "setoption name Threads value 2",
    "setoption name Hash value 1024",
    "setoption name ConsiderationMode value true"
]

from common.vec2d import Vec
CHANGE_SCALE = 0.6
# for gui
GUI_SIZE = Vec([1400,1300]) * CHANGE_SCALE
BOARD_POS = Vec([150, 0]) * CHANGE_SCALE
MATTA_POS = Vec([300, 900]) * CHANGE_SCALE
EXEC_POS = Vec([500, 900]) * CHANGE_SCALE
KILL_POS = Vec([750, 900]) * CHANGE_SCALE
INFO_POS = Vec([60, 960]) * CHANGE_SCALE
INFO_SIZE = Vec([1260, 300]) * CHANGE_SCALE
# for ShogiBoard
IMG_SIZE = Vec([81, 90])
CANVAS_SIZE = Vec([1080, 960]) * CHANGE_SCALE
KOMA_SIZE = IMG_SIZE * CHANGE_SCALE
BANMEN_POS = Vec([160, 60]) * CHANGE_SCALE
SENTEMOCHI_POS = Vec([918, 280]) * CHANGE_SCALE
GOTEMOCHI_POS = Vec([10, 20]) * CHANGE_SCALE
MOCHI_LABEL_X = int(30 * CHANGE_SCALE)
MOCHI_TEXT_SIZE = int(20 * CHANGE_SCALE)

# koma image
image_filename = './common/koma.gif'