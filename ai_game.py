from customtkinter import *
from PIL import Image
import pandas as pd
import pickle
from components import TopBar
from config import (
    DEFAULT_BUTTON_THEME, ACCENT_BUTTON_THEME,
    DARK_BG, DARK_SURFACE, DARK_SURFACE2, DARK_TEXT, DARK_SUBTEXT, DARK_BORDER,
    LIGHT_BG, LIGHT_SURFACE, LIGHT_SURFACE2, LIGHT_TEXT, LIGHT_SUBTEXT, LIGHT_BORDER,
    ACCENT, ACCENT_LIGHT, WIN_COLOR, LOSE_COLOR, DRAW_COLOR
)
from assest import *


class Game:
    def __init__(self, parent, switch_back_callback, close_app, btn_manager):
        self.frame = CTkFrame(parent, fg_color=(LIGHT_BG, DARK_BG))
        self.btn_manager = btn_manager

        self.board = [""] * 9
        self.player_score = 0
        self.ai_score = 0
        self.draws = 0
        self.buttons = []
        self.player_name = "You"

        self.img_X = CTkImage(Image.open(CROSS_ICON), size=(38, 38))
        self.img_O = CTkImage(Image.open(CIRCLE_ICON), size=(38, 38))

        self._model_import()

        self.topbar = TopBar(self.frame, DEFAULT_BUTTON_THEME, close_app, self.btn_manager)
        self.return_image = CTkImage(Image.open(LEFT_ARROW_ICON), size=(20, 20))
        self.topbar.f1b2.configure(command=switch_back_callback, image=self.return_image)
        self.btn_manager.add(*self.topbar.btn_list)
        self.btn_manager.update_borders(get_appearance_mode() == "Dark")

        self._build_header()
        self._build_scoreboard()
        self._build_status_bar()
        self._build_board()
        self._build_controls()

    def set_player_name(self, name):
        self.player_name = name or "You"
        self.score_player_label.configure(text=self.player_name)

    def _build_header(self):
        header = CTkFrame(self.frame, fg_color="transparent")
        header.pack(pady=(8, 0))

        CTkLabel(
            header,
            text="TIC  TAC  TOE",
            font=("Helvetica", 22, "bold"),
            text_color=(LIGHT_TEXT, DARK_TEXT)
        ).pack()

        CTkLabel(
            header,
            text="You vs AI",
            font=("Helvetica", 12),
            text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT)
        ).pack(pady=(2, 0))

    def _build_scoreboard(self):
        outer = CTkFrame(self.frame, fg_color="transparent")
        outer.pack(pady=(12, 0), padx=24, fill="x")

        player_card = CTkFrame(
            outer,
            fg_color=(LIGHT_SURFACE, DARK_SURFACE),
            corner_radius=16,
            border_width=1,
            border_color=(LIGHT_BORDER, DARK_BORDER)
        )
        player_card.pack(side=LEFT, expand=True, fill="both", padx=(0, 6))

        CTkLabel(
            player_card,
            image=CTkImage(Image.open(CIRCLE_ICON), size=(20, 20)),
            text=""
        ).pack(pady=(10, 2))

        self.score_player_label = CTkLabel(
            player_card,
            text=self.player_name,
            font=("Helvetica", 11),
            text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT)
        )
        self.score_player_label.pack()

        self.score_player = CTkLabel(
            player_card,
            text="0",
            font=("Helvetica", 24, "bold"),
            text_color=(ACCENT, ACCENT_LIGHT)
        )
        self.score_player.pack(pady=(2, 10))

        draws_card = CTkFrame(
            outer,
            fg_color=(LIGHT_SURFACE, DARK_SURFACE),
            corner_radius=16,
            border_width=1,
            border_color=(LIGHT_BORDER, DARK_BORDER)
        )
        draws_card.pack(side=LEFT, expand=True, fill="both", padx=3)

        CTkLabel(
            draws_card,
            text="—",
            font=("Helvetica", 18, "bold"),
            text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT)
        ).pack(pady=(10, 2))

        CTkLabel(
            draws_card,
            text="Draws",
            font=("Helvetica", 11),
            text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT)
        ).pack()

        self.score_draws = CTkLabel(
            draws_card,
            text="0",
            font=("Helvetica", 24, "bold"),
            text_color=(LIGHT_TEXT, DARK_TEXT)
        )
        self.score_draws.pack(pady=(2, 10))

        ai_card = CTkFrame(
            outer,
            fg_color=(LIGHT_SURFACE, DARK_SURFACE),
            corner_radius=16,
            border_width=1,
            border_color=(LIGHT_BORDER, DARK_BORDER)
        )
        ai_card.pack(side=LEFT, expand=True, fill="both", padx=(6, 0))

        CTkLabel(
            ai_card,
            image=CTkImage(Image.open(CROSS_ICON), size=(20, 20)),
            text=""
        ).pack(pady=(10, 2))

        CTkLabel(
            ai_card,
            text="AI",
            font=("Helvetica", 11),
            text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT)
        ).pack()

        self.score_ai = CTkLabel(
            ai_card,
            text="0",
            font=("Helvetica", 24, "bold"),
            text_color=(LOSE_COLOR, LOSE_COLOR)
        )
        self.score_ai.pack(pady=(2, 10))

    def _build_status_bar(self):
        self.status_frame = CTkFrame(
            self.frame,
            fg_color=(LIGHT_SURFACE2, DARK_SURFACE2),
            corner_radius=12,
            height=44
        )
        self.status_frame.pack(pady=(12, 0), padx=24, fill="x")
        self.status_frame.pack_propagate(False)

        self.result_label = CTkLabel(
            self.status_frame,
            text="Your turn — make a move",
            font=("Helvetica", 13, "bold"),
            text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT)
        )
        self.result_label.pack(expand=True)

    def _build_board(self):
        board_outer = CTkFrame(
            self.frame,
            fg_color=(LIGHT_SURFACE, DARK_SURFACE),
            corner_radius=20,
            border_width=1,
            border_color=(LIGHT_BORDER, DARK_BORDER)
        )
        board_outer.pack(pady=(12, 0), padx=24)

        board_inner = CTkFrame(board_outer, fg_color="transparent")
        board_inner.pack(padx=12, pady=12)

        for i in range(9):
            row, col = i // 3, i % 3

            cell_bg = (LIGHT_SURFACE2, DARK_SURFACE2)

            btn = CTkButton(
                board_inner,
                text="",
                width=88,
                height=88,
                corner_radius=14,
                fg_color=cell_bg,
                hover_color=(LIGHT_BORDER, DARK_BORDER),
                border_width=0,
                command=lambda i=i: self.click(i)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.buttons.append(btn)

    def _build_controls(self):
        ctrl = CTkFrame(self.frame, fg_color="transparent")
        ctrl.pack(pady=(12, 16), padx=24, fill="x")

        reset_img = CTkImage(Image.open(RESET_ICON), size=(20, 20))

        self.reset_btn = CTkButton(
            ctrl,
            text="  New Game",
            image=reset_img,
            compound="left",
            command=self.reset_board,
            height=50,
            font=("Helvetica", 14, "bold"),
            **ACCENT_BUTTON_THEME
        )
        self.reset_btn.pack(fill="x")

    def _model_import(self):
        try:
            self.model, self.feature_names = pickle.load(open("model.pkl", "rb"))
        except Exception:
            self.model = None
            self.feature_names = None

    def convert_board(self, board):
        mapping = {"X": 1, "O": -1, "": 0}
        return [mapping[x] for x in board]

    def check_winner_sim(self, temp_board, player):
        win_conditions = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for a, b, c in win_conditions:
            if temp_board[a] == temp_board[b] == temp_board[c] == player:
                return True
        return False

    def ai_move(self):
        for i in range(9):
            if self.board[i] == "":
                temp = self.board.copy()
                temp[i] = "O"
                if self.check_winner_sim(temp, "O"):
                    return i

        for i in range(9):
            if self.board[i] == "":
                temp = self.board.copy()
                temp[i] = "X"
                if self.check_winner_sim(temp, "X"):
                    return i

        if self.model is None:
            for i in range(9):
                if self.board[i] == "":
                    return i
            return None

        numeric_board = self.convert_board(self.board)
        best_move = None
        best_score = -1

        for i in range(9):
            if self.board[i] == "":
                temp = numeric_board.copy()
                temp[i] = -1
                temp_df = pd.DataFrame([temp], columns=self.feature_names)
                prob = self.model.predict_proba(temp_df)[0][1]
                if prob > best_score:
                    best_score = prob
                    best_move = i

        return best_move

    def click(self, i):
        if self.board[i] != "":
            return

        self.board[i] = "X"
        self.buttons[i].configure(image=self.img_X, text="", fg_color=(LIGHT_SURFACE2, DARK_SURFACE2))

        if self.check_winner() or self.check_draw():
            return

        self.result_label.configure(text="AI is thinking...", text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT))
        self.frame.after(300, self._do_ai_move)

    def _do_ai_move(self):
        move = self.ai_move()
        if move is not None:
            self.board[move] = "O"
            self.buttons[move].configure(image=self.img_O, text="", fg_color=(LIGHT_SURFACE2, DARK_SURFACE2))
            if not self.check_winner() and not self.check_draw():
                self.result_label.configure(
                    text="Your turn — make a move",
                    text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT)
                )

    def check_winner(self):
        win_conditions = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for a, b, c in win_conditions:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != "":
                if self.board[a] == "X":
                    self.player_score += 1
                    self.score_player.configure(text=str(self.player_score))
                    self.result_label.configure(
                        text="You Win!",
                        text_color=(WIN_COLOR, WIN_COLOR)
                    )
                else:
                    self.ai_score += 1
                    self.score_ai.configure(text=str(self.ai_score))
                    self.result_label.configure(
                        text="AI Wins!",
                        text_color=(LOSE_COLOR, LOSE_COLOR)
                    )
                self._disable_buttons()
                return True
        return False

    def check_draw(self):
        if "" not in self.board:
            self.draws += 1
            self.score_draws.configure(text=str(self.draws))
            self.result_label.configure(
                text="It's a Draw!",
                text_color=(DRAW_COLOR, DRAW_COLOR)
            )
            self._disable_buttons()
            return True
        return False

    def _disable_buttons(self):
        for btn in self.buttons:
            btn.configure(state=DISABLED)

    def reset_board(self):
        self.board = [""] * 9
        for btn in self.buttons:
            btn.configure(image=None, text="", state=NORMAL, fg_color=(LIGHT_SURFACE2, DARK_SURFACE2))
        self.result_label.configure(
            text="Your turn — make a move",
            text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT)
        )
