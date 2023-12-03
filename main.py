from tkinter import *
from tkinter import font
from PIL import Image, ImageTk
import time, copy

def fresize(s, nw, nh):
    img = Image.open(s)
    resized = img.resize((nw, nh))
    new_img = ImageTk.PhotoImage(resized)
    return new_img

def create_piece(i, j, img):
    global chessx1, chessx2, chessy1, chessy2, side
    return w.create_image(chessx1 + side//2 + j*side, chessy1 + side//2 + i*side, image = img)

def update_chess():
    global pawn_img, chess, pchess, knight_img, rect_gameover, txt_gameover, txt_restart, txt_win
    rowstat = 1
    colstat = 0
    fill_color = 'white'
    for i in range(1, 9):
        rowstat = 1-rowstat
        colstat = rowstat
        for j in range(1, 9):
            if colstat == 0: fill_color = 'white'
            else: fill_color = 'gray'
            cchess[i-1][j-1] = w.create_rectangle(chessx1+(j-1)*side, chessy1+(i-1)*side, chessx1+j*side, chessy1+i*side, fill=fill_color, width = 2)
            colstat = 1-colstat
    for i in range(8):
        for j in range(8):
            if chess[i][j] == 1: pchess[i][j] = create_piece(i, j, pawn_img)
            elif chess[i][j] == 2: pchess[i][j] = create_piece(i, j, knight_img)
            else: pchess[i][j] = 0

def update_btn():
    global game_stat
    w.itemconfig(txt_go, text = game_stat)

def update_score():
    global moves
    w.itemconfig(txt_move, text = f'Moves: {moves}')

def knight_check(r1, c1, r2, c2):
    return (abs(r2-r1) == 2 and abs(c2-c1) == 1) or (abs(r2-r1) == 1 and abs(c2-c1) == 2)

def check_res(l):
    global game_stat, moves
    cnt0 = 0
    cnt2 = 0
    for i in range(8):
        for j in range(8):
            if l[i][j] == 0: cnt0+=1
            elif l[i][j] == 2: cnt2+=1
    if cnt0 == 63 and cnt2 == 1 and moves == 16:
        print("Win")
        game_stat = "Pause"
        w.itemconfig(rect_gameover, state = 'normal')
        w.itemconfig(txt_win, state = 'normal')
        w.itemconfig(txt_restart, state = 'normal')
        w.tag_raise(rect_gameover)
        w.tag_raise(txt_win)
        w.tag_raise(txt_restart)
    if moves > 16:
        print("Game Over!")
        game_stat = "Pause"
        w.itemconfig(rect_gameover, state = 'normal')
        w.itemconfig(txt_gameover, state = 'normal')
        w.itemconfig(txt_restart, state = 'normal')
        w.tag_raise(rect_gameover)
        w.tag_raise(txt_gameover)
        w.tag_raise(txt_restart)

def clicked(e):
    global chessx1, chessx2, chessy1, chessy2, side, chess, cchess, pchess, ccolorb, ccolorw, selectedrow, selectedcol, gox1, goy1, gox2, goy2, game_stat, knightcol, knightrow, moves, steps, undox1, undoy1, undox2, undoy2, chess_his
    mx, my = e.x, e.y
    if chessx1 <= mx <= chessx2 and chessy1 <= my <= chessy2 and game_stat != "Pause":
        row = (my - chessy1)//side
        col = (mx - chessx1)//side
        # print(row, col)
        if selectedrow == None and selectedcol == None: pass
        elif selectedrow != None and selectedcol != None and chess[row][col] != 2:
            if (selectedrow + selectedcol) % 2 == 0: w.itemconfig(cchess[selectedrow][selectedcol], fill = 'white')
            else: w.itemconfig(cchess[selectedrow][selectedcol], fill = 'gray')
        
        if chess[row][col] != 2:
            if (row + col) % 2 == 0: w.itemconfig(cchess[row][col], fill = ccolorw)
            else: w.itemconfig(cchess[row][col], fill = ccolorb)
            selectedrow = row
            selectedcol = col
        # print(selectedcol, se)
    elif gox1 <= mx <= gox2 and goy1 <= my <= goy2 and selectedcol != None:
        if game_stat == 'Place' and chess[selectedrow][selectedcol] == 0:
            w.itemconfig(knight, state='hidden')
            chess[selectedrow][selectedcol] = 2
            if (selectedrow + selectedcol) % 2 == 0: w.itemconfig(cchess[selectedrow][selectedcol], fill = 'white')
            else: w.itemconfig(cchess[selectedrow][selectedcol], fill = 'gray')
            game_stat = 'Go'
            update_btn()
            knightrow = selectedrow
            knightcol = selectedcol
            selectedrow = selectedcol = None
            update_chess()
            steps.append(f"Place {knightrow} {knightcol}")
            chess_his.append(copy.deepcopy(chess))
            # for v in chess_his:
            #     print(*v, sep = '\n')
            #     print()
        elif game_stat == 'Go':
            if (not knight_check(knightrow, knightcol, selectedrow, selectedcol)): return
            # print("Go Clicked")
            chess[knightrow][knightcol] = 0
            chess[selectedrow][selectedcol] = 2
            if (selectedrow + selectedcol) % 2 == 0: w.itemconfig(cchess[selectedrow][selectedcol], fill = 'white')
            else: w.itemconfig(cchess[selectedrow][selectedcol], fill = 'gray')
            knightrow = selectedrow
            knightcol = selectedcol
            selectedrow = selectedcol = None
            moves += 1
            update_score()
            update_btn()
            update_chess()
            check_res(chess)
            steps.append(f"Move {knightrow} {knightcol}")
            chess_his.append(copy.deepcopy(chess))
            # print(steps)
            # for v in chess_his:
            #     print(*v, sep = '\n')
            #     print()
    elif undox1 <= mx <= undox2 and undoy1 <= my <= undoy2:
        if selectedcol != None and selectedrow != None:
            if (selectedrow + selectedcol) % 2 == 0: w.itemconfig(cchess[selectedrow][selectedcol], fill = 'white')
            else: w.itemconfig(cchess[selectedrow][selectedcol], fill = 'gray')
            selectedrow = selectedcol = None
        if len(steps) > 1:
            t = steps[-2]
            prevrow, prevcol = [int(s) for s in t[-3:].split()]
            knightrow = prevrow
            knightcol = prevcol
            chess = copy.deepcopy(chess_his[-2])
            # for v in chess_his:
            #     print(*v, sep = '\n')
            #     print()
            moves-=1
            steps.pop(-1)
            chess_his.pop(-1)
            # print(steps)
            update_score()
            update_chess()
            # print(game_stat)
        else:
            # print(0)
            restart("Undo")
    else:
        pass

def restart(e):
    global game_stat, moves, chess, steps
    # print(game_stat)
    if game_stat != "Pause" and e != 'Undo': return
    w.itemconfig(rect_gameover, state = 'hidden')
    w.itemconfig(txt_gameover, state = 'hidden')
    w.itemconfig(txt_win, state = 'hidden')
    w.itemconfig(txt_restart, state = 'hidden')
    moves = 0
    game_stat = "Place"
    chess = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]
    steps = []
    w.itemconfig(knight, state = 'normal')
    update_btn()
    update_chess()
    update_score()

# Init
window = Tk()
window.title("Knight's Move")
swidth, sheight = window.winfo_screenwidth(), window.winfo_screenheight()
window.iconbitmap("resources/knight.ico")
# print(swidth, sheight)
# window.geometry(f"{swidth}x{sheight}")

#Variales
chess = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
cchess = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
pchess = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]
steps = []
chess_his = []
selectedrow = None
selectedcol = None
knightrow = -1
knightcol = -1
game_stat = 'Place'
moves = 0
# print(chess)

#Constants
side = sheight*60//720
chessx1 = swidth//2-side*4
chessy1 = sheight//2-side*4-40
chessx2 = swidth//2+side*4
chessy2 = sheight//2+side*4-40
ccolorw = "#bcdb32"
ccolorb = "#93ab27"

gox1, goy1 = swidth*1000//1280, sheight*480//720
gox2, goy2 = swidth*1150//1280, sheight*530//720

undox1, undoy1 = gox1, goy1+sheight*60//720
undox2, undoy2 = gox2, goy2+sheight*60//720

mvx1, mvy1, mvx2, mvy2 = swidth*100//1280, sheight*100//720, swidth*220//1280, sheight*150//720

#Main Code
#Canvas
w = Canvas(window, width = swidth, height = sheight, bg="#ffffff")
w.pack()

#Draw Chess
rowstat = 1
colstat = 0
fill_color = 'white'
for i in range(1, 9):
    rowstat = 1-rowstat
    colstat = rowstat
    for j in range(1, 9):
        if colstat == 0: fill_color = 'white'
        else: fill_color = 'gray'
        cchess[i-1][j-1] = w.create_rectangle(chessx1+(j-1)*side, chessy1+(i-1)*side, chessx1+j*side, chessy1+i*side, fill=fill_color, width = 2)
        colstat = 1-colstat

#Chess Row-Col Marking
colm = 'ABCDEFGH'
for i in range(1, 9):
    txt = w.create_text(chessx1+side//2+side*(i-1), chessy2+20, text=colm[i-1], font = ("Arial", 18, "bold"))
for i in range(1, 9):
    txt = w.create_text(chessx1-20, chessy1+side//2+side*(i-1), text=str(9-i), font = ("Arial", 18, "bold"))

#Sprites
knight_img = fresize("resources/Knight.png", side, side)
knight = w.create_image(chessx1-(swidth * 120//1280), sheight//2, image = knight_img)

pawn_img = fresize("resources/Pawn.png", side, side)
update_chess()

btn_go = w.create_rectangle(gox1, goy1, gox2, goy2, fill = 'white', width = 2)
txt_go = w.create_text(gox1 + (gox2-gox1)//2, goy1 + (goy2-goy1)//2, text = 'Place', font = 'Arial 18')

btn_undo = w.create_rectangle(undox1, undoy1, undox2, undoy2, fill = 'white', width = 2)
txt_undo = w.create_text(undox1 + (undox2 - undox1)//2, undoy1 + (undoy2 - undoy1)//2, text = 'Undo', font = 'Arial 18')

rect_move = w.create_rectangle(mvx1, mvy1, mvx2, mvy2, fill = 'white', width = 2)
txt_move = w.create_text(mvx1 + (mvx2 - mvx1)//2, mvy1 + (mvy2 - mvy1)//2, text = 'Moves: 0', font = 'Arial 18')

rect_gameover = w.create_rectangle(swidth//2-260, sheight//2-120, swidth//2+260, sheight//2+20, fill='white', width = 2)
txt_win = w.create_text(swidth//2, sheight//2-50, text = "You Win!!!", fill = '#e8b009', font = "Arial 60")
txt_gameover = w.create_text(swidth//2, sheight//2-50, text = "Game Over!!!", fill = 'red', font = "Arial 60")
txt_restart = w.create_text(swidth//2, sheight//2, text = "Press \"Space\" to restart", font = "Arial 14")

w.itemconfig(rect_gameover, state = 'hidden')
w.itemconfig(txt_gameover, state = 'hidden')
w.itemconfig(txt_win, state = 'hidden')
w.itemconfig(txt_restart, state = 'hidden')

# print(*chess, sep='\n')

#Keys
window.bind_all("<Button-1>", clicked)
window.bind_all("<space>", restart)

#Mainloop
window.state('zoomed')
window.mainloop()