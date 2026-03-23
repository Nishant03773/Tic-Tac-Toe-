from customtkinter import *
from PIL import Image
import pandas as pd
import pickle


app = CTk()
app.title("Tic Tac Toe Game")       
app.geometry("400x620")
app.resizable(FALSE,FALSE)
app.configure(fg_color="#232c46",padx=12)
app._set_appearance_mode('system')
label1 = CTkLabel(master=app,text="TIC TAC TOE",font=("Cascadia Code SemiBold", 22, "bold"))
label1.pack(pady = 12)



frame1 = CTkFrame(app,width=400,height=70,fg_color="transparent")
frame1.pack()
frame1.pack_propagate(False)

frame1_1 = CTkFrame(master=frame1,width=120,height=69,fg_color="#3e4f69",border_width=2,border_color="#6c7793")
frame1_1.pack(side=LEFT)
frame1_1.pack_propagate(False)

img_f1_1 = CTkImage(Image.open("./logos/circle.png"), size=(22,22))
l1f1 = CTkLabel(frame1_1,image=img_f1_1,text="")
l1f1.pack(anchor="nw",pady=5,padx=10)

frame1_1_1 = CTkFrame(master=frame1_1,width=120,height=30,corner_radius=0,fg_color="transparent")
frame1_1_1.pack(fill="x",padx=10)
frame1_1_1.pack_propagate(False)

l2f1 = CTkLabel(frame1_1_1,text="You: ",font=("Helvetica", 16))
l2f1.pack(side=LEFT)

l2f1 = CTkLabel(frame1_1_1,text="0",font=("Helvetica", 16))
l2f1.pack(side=RIGHT,padx=20)



frame1_2 = CTkFrame(master=frame1,width=120,height=69,fg_color="#3e4f69",border_width=2,border_color="#6c7793")
frame1_2.pack(side=RIGHT)
frame1_2.pack_propagate(False)

img_f1_2 = CTkImage(Image.open("./logos/cross.png"), size=(22,22))
l1f2 = CTkLabel(frame1_2,image=img_f1_2,text="")
l1f2.pack(anchor="nw",pady=5,padx=10)

frame1_2_1 = CTkFrame(master=frame1_2,width=120,height=30,corner_radius=0,fg_color="transparent")
frame1_2_1.pack(fill="x",padx=10)
frame1_2_1.pack_propagate(False)

l2f2 = CTkLabel(frame1_2_1,text="AI: ",font=("Helvetica", 16))
l2f2.pack(side=LEFT)

l2f2 = CTkLabel(frame1_2_1,text="0",font=("Helvetica", 16))
l2f2.pack(side=RIGHT,padx=20)


label2 = CTkLabel(master=app,text="You vs AI",font=("Segoe UI", 22, "bold"))
label2.pack(pady = 12)


frame2 = CTkFrame(master=app,fg_color="#404d6b")
frame2.pack(padx=20)
frame2.pack_propagate(False)

result_label = CTkLabel(app, text="", font=("Segoe UI", 20, "bold"))
result_label.pack(pady=10)

buttons = []
for i in range(9):
    btn = CTkButton(
    master=frame2,
    text="",
    corner_radius=12,
    width=90,
    height=90,
    command=lambda i=i: click(i),
    fg_color="#232c46",   
    hover_color="#2a3555",
)
    btn.grid(row=i//3, column=i%3, sticky="nsew", padx=8, pady=8)

    buttons.append(btn)

for i in range(3):
    frame2.grid_rowconfigure(i, weight=1)
    frame2.grid_columnconfigure(i, weight=1)




model, feature_names = pickle.load(open("model.pkl", "rb"))

board = [""] * 9 #equals to ['','','','','','','','','']

player_score = 0
ai_score = 0


def convert_board(board):
    mapping = {"X":1, "O":-1, "":0}
    
    new_board = []
    
    for x in board:
        new_board.append(mapping[x])
    
    return new_board

# def ai_move():
#     numeric_board = convert_board(board) #convert board into numeric values

#     best_move = None
#     best_score = -1 #range of probability(0 to 1)

#     for i in range(9):
#         if board[i] == "":
#             temp = numeric_board.copy()
#             temp[i] = -1   # AI = O

#             temp_df = pd.DataFrame([temp], columns=feature_names)
#             prob = model.predict_proba(temp_df)[0][1]

#             if prob > best_score:
#                 best_score = prob
#                 best_move = i

#     return best_move

def ai_move():
    numeric_board = convert_board(board)

    # 1. Check if AI can win
    for i in range(9):
        if board[i] == "":
            temp = board.copy()
            temp[i] = "O"
            if check_winner_sim(temp, "O"):
                return i

    # 2. Block player win
    for i in range(9):
        if board[i] == "":
            temp = board.copy()
            temp[i] = "X"
            if check_winner_sim(temp, "X"):
                return i

    # 3. Use ML
    best_move = None
    best_score = -1

    for i in range(9):
        if board[i] == "":
            temp = numeric_board.copy()
            temp[i] = -1

            temp_df = pd.DataFrame([temp], columns=feature_names)
            prob = model.predict_proba(temp_df)[0][0]

            if prob > best_score:
                best_score = prob
                best_move = i

    return best_move


def check_winner():
    global player_score, ai_score

    win_conditions = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]

    for a,b,c in win_conditions:
        if board[a] == board[b] == board[c] and board[a] != "":
            
            if board[a] == "X":
                player_score += 1
                l2f1.configure(text=str(player_score))
                result_label.configure(text="You Win!")
            else:
                ai_score += 1
                l2f2.configure(text=str(ai_score))
                result_label.configure(text="AI Wins!")

            disable_buttons()
            return True

    return False

def check_winner_sim(temp_board, player):
    win_conditions = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]

    for a,b,c in win_conditions:
        if temp_board[a] == temp_board[b] == temp_board[c] == player:
            return True

    return False



def check_draw():
    if "" not in board:
        result_label.configure(text="It's a Draw!")
        disable_buttons()
        return True
    return False

def disable_buttons():
    for btn in buttons:
        btn.configure(state=DISABLED) #Change of configuration of the button state to disabled 

img_X = CTkImage(Image.open("./logos/cross.png"), size=(40,40))
img_O = CTkImage(Image.open("./logos/circle.png"), size=(40,40))

def click(i):
    if board[i] == "":
        # PLAYER MOVE
        board[i] = "X"
        buttons[i].configure(image=img_X,text="")#Place image instead of text
        buttons[i].image = img_X

        if check_winner() or check_draw():
            return

        # AI MOVE
        move = ai_move()
        if move is not None:
            board[move] = "O"
            buttons[move].configure(image=img_O,text="")#Place image instead of text
            buttons[move].image = img_O

            check_winner() or check_draw()

def reset_board():
    global board
    board = [""] * 9

    for btn in buttons:
        btn.configure(image=None, text="", state=NORMAL)

    result_label.configure(text="")

img_reset = CTkImage(Image.open("./logos/reset.png"), size=(30,30))

reset_btn = CTkButton(
    app,
    text="    Restart",
    image=img_reset,
    compound="left", 
    command=reset_board,
    fg_color="#FFFFFF",
    hover_color="#c4c4c4",
    width=400,height=50,
    font=("Arial",20),
    text_color="Black"
)
reset_btn.pack(pady=10)

app.mainloop()