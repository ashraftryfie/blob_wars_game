from tkinter import *
from tkinter import messagebox

from Game_Controller import Game_Controller
from Game_Board import Game_Board
from Game_Logic import Game_Logic
from Position import Position
from Player import Player
from Blob import Blob

RED_COLOR = "#EE4035"
BLUE_COLOR = "#0492CF"
Green_color = "#7BC043"
Gray_color = "gray"
White_color = "white"

print('1- Easy\n2- Normal\n3- Hard')
level = int(input())

blobs_list = list()  # to store the initial blobs

# Dimension of Board
size = 6
rows = size
columns = size

blobs_list.append(Blob(Position(0, 0), Player('Human')))
blobs_list.append(Blob(Position(0, columns - 1), Player('Human')))
blobs_list.append(Blob(Position(rows - 1, 0), Player('AI')))
blobs_list.append(Blob(Position(rows - 1, columns - 1), Player('AI')))
blob_game = Game_Board(rows, columns, blobs_list)  # game board
game_ctrl = Game_Controller(blob_game)  # game controller
game_logic = Game_Logic(game_ctrl)  # game logic
blob_game.display_board()
blob_game.get_board()

root = Tk()
root.title("Blob Wars")
my_menu = Menu(root)

root.config(menu=my_menu)


def do_job():
    for i in range(rows):
        for j in range(columns):
            if blob_game.board[i][j] not in ['P', 'B']:
                # blob_game.board[i][j] = 'P'
                buttons[i][j]["text"] = 'P'
                if buttons[i][j]["text"] == 'B':
                    buttons[i][j]["foreground"] = BLUE_COLOR
                elif buttons[i][j]["text"] == 'P':
                    buttons[i][j]["foreground"] = RED_COLOR
                else:
                    buttons[i][j]["foreground"] = White_color

    blob_game.pass_turn()
    blob_game.display_board()
    check_win()


my_menu.add_command(label='pass', command=do_job)
my_score=my_menu.add_command(label=f' Human : {blob_game.get_score()[0]}   VS   AI : {blob_game.get_score()[1]}')
# my_menu.add_command(label='Save', command=do_job)

# my_menu.entryconfigure(1, label="hhh")
# أضف خط فاصل
my_menu.add_separator()

turn = True
from_cell = None
to_cell = Position(-1, -1)
cell_value = 'x'


def human(pos):
    global from_cell, to_cell, cell_value, turn,my_score

    if from_cell is None:
        if can_select(pos[0], pos[1]):
            from_cell = Position(pos[0], pos[1])
            print("From: (", from_cell.x, ', ', from_cell.y, ')')
            cell_value = blob_game.board[pos[0]][pos[1]]
            buttons[from_cell.x][from_cell.y].config(bg=Green_color)
            my_menu.entryconfigure(2, label=f'Human : {blob_game.get_score()[0]}   VS   AI : {blob_game.get_score()[1]}')

        # tev = False
    else:
        to_cell = Position(pos[0], pos[1])
        if to_cell.x == from_cell.x and to_cell.y == from_cell.y:
            buttons[from_cell.x][from_cell.y].config(bg=White_color)
            from_cell, to_cell = None, None
        else:
            if blob_game.board[to_cell.x][to_cell.y] != 'P':
                print("To: (", to_cell.x, ', ', to_cell.y, ')')
                if game_ctrl.make_move_to_blob(from_cell, to_cell, Player('Human')):
                    blob_game.display_board()
                    buttons[pos[0]][pos[1]]["text"] = cell_value
                    buttons[pos[0]][pos[1]]["foreground"] = BLUE_COLOR
                    buttons[from_cell.x][from_cell.y].config(bg=White_color)
                    # buttons[to_cell.x][to_cell.y].config(bg="white")

                    from_cell, to_cell = None, None
                    cell_value = 'x'
                    turn = False
                    my_menu.entryconfigure(2,
                    label=f'Human : {blob_game.get_score()[0]}   VS   AI : {blob_game.get_score()[1]}')

                    if not check_win():

                        ai()


def ai():
    global turn, buttons, blob_game

    game_ctrl.AI_plays(game_logic, level)

    turn = True

    blob_game.display_board()

    for i in range(rows):
        for j in range(columns):
            buttons[i][j]["text"] = blob_game.board[i][j]
            if buttons[i][j]["text"] == 'B':
                buttons[i][j]["foreground"] = BLUE_COLOR
            elif buttons[i][j]["text"] == 'P':

                buttons[i][j]["foreground"] = RED_COLOR
            else:
                buttons[i][j]["foreground"] = White_color
    my_menu.entryconfigure(2, label=f'Human : {blob_game.get_score()[0]}   VS   AI : {blob_game.get_score()[1]}')
    # buttons[x_ai][y_ai]["foreground"] = RED_COLOR
    check_win()


def can_select(x, y):
    return buttons[x][y]["text"] not in ['', 'P', '-']


def get_coord(x, y):
    global turn

    if turn:
        human([x, y])


def destroy_widgets():
    for widget in root.winfo_children():
        widget.destroy()


human_score, ai_score, draw_score = 0, 0, 0

size_of_board = 600
canvas = None


def check_win():
    global human_score, ai_score, draw_score, canvas, size_of_board
    temp = False
    if blob_game.is_final_state():
        score = blob_game.get_score()
        print('score: ', score)
        if score[0] < score[1]:
            print('AI Wins !')
            destroy_widgets()
            text = 'Winner: AI (Red)'
            color = RED_COLOR
            ai_score = score[1]
            human_score = score[0]
        elif score[0] > score[1]:
            print('Human Wins !')
            destroy_widgets()
            color = BLUE_COLOR
            text = 'Winner: Human (Blue)'
            # human_score += 1
            ai_score = score[1]
            human_score = score[0]
        else:
            print('Match Draw !')
            text = 'Match Draw !'
            color = 'gray'
            temp = True

            root.destroy()
        canvas = Canvas(root, width=size_of_board, height=size_of_board)
        canvas.pack()
        canvas.create_text(size_of_board / 2, size_of_board / 3,
                           font="cmr 30 bold",
                           fill=color,
                           text=text)

        score_text = 'Scores \n'
        canvas.create_text(size_of_board / 2, 5 * size_of_board / 8,
                           font="cmr 20 bold",
                           fill='black',
                           text=score_text)

        if temp:
            score_text = 'Draw    : ' + str(draw_score)
        else:
            score_text = 'Human : ' + str(human_score) + '\n\n'
            score_text += 'AI         : ' + str(ai_score) + '\n\n'
        canvas.create_text(size_of_board / 2, 3 * size_of_board / 4,
                           font="cmr 15 bold",
                           fill=Green_color,
                           text=score_text)
        return True
    return False


buttons = [[Button() for j in range(columns)] for i in range(rows)]


# Add buttons to the grid
def initialize_board():
    for i in range(0, rows):
        for j in range(0, columns):
            if blob_game.board[i][j] == 'P':
                blob_color = RED_COLOR
            elif blob_game.board[i][j] == 'B':
                blob_color = BLUE_COLOR
            else:
                blob_color = Gray_color
            if blob_game.board[i][j] == '-':
                vlaue = ''
            else:
                vlaue = blob_game.board[i][j]
            buttons[i][j] = Button(root,
                                   text=("%s" % vlaue),
                                   foreground=blob_color,
                                   font='sans 14 bold',
                                   command=lambda x=i, y=j: get_coord(x, y),
                                   height=2, width=4,
                                   bg=White_color)

            buttons[i][j].grid(row=i, column=j, sticky='news')


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


initialize_board()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()

# while not blob_game.is_final_state():
#     print("Human Turn : Enter your move (blob cell number - cell to move) : ")
#     target_blob = int(input())
#     direction = int(input())
#     pos = game_ctrl.mapping(target_blob)  # where pos will be [x, y]
#     position = Position(pos[0], pos[1])
#     cell = game_ctrl.mapping(direction)
#     cell_to_move = Position(cell[0], cell[1])
#     while (True):
#         if game_ctrl.make_move_to_blob(position, cell_to_move, Player('Human')) != False:
#             break
#         else:  # re-enter inputs
#             print("Re-Enter your move (blob cell number - cell to move) : ")
#             target_blob = int(input())
#             direction = int(input())
#             pos = game_ctrl.mapping(target_blob)  # where pos will be [x, y]
#             position = Position(pos[0], pos[1])
#             cell = game_ctrl.mapping(direction)
#             cell_to_move = Position(cell[0], cell[1])
#     blob_game.display_board()
#
#     game_ctrl.AI_plays(game_logic, 2)
#
#     blob_game.display_board()
#
# score = blob_game.get_score()
# if score[0] == 0:
#     print('AI Wins !')
# else:
#     print('Human Wins !')

# Launch the GUI
