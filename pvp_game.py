from customtkinter import *
from PIL import Image
from components import TopBar
from config import (
    DEFAULT_BUTTON_THEME, ACCENT_BUTTON_THEME,
    DARK_BG, DARK_SURFACE, DARK_SURFACE2, DARK_TEXT, DARK_SUBTEXT, DARK_BORDER,
    LIGHT_BG, LIGHT_SURFACE, LIGHT_SURFACE2, LIGHT_TEXT, LIGHT_SUBTEXT, LIGHT_BORDER,
    ACCENT, ACCENT_LIGHT, WIN_COLOR, LOSE_COLOR, DRAW_COLOR
)
from assest import *


class PvPGame:
    def __init__(self, parent, switch_back_callback, close_app, btn_manager):
        self.frame = CTkFrame(parent, fg_color=(LIGHT_BG, DARK_BG))
        self.btn_manager = btn_manager

        self.board = [""] * 9
        self.player1_score = 0
        self.player2_score = 0
        self.draws = 0
        self.buttons = []
        self.player1_name = "Player 1"
        self.player2_name = "Player 2"
        self.current_turn = 1

        self.img_X = CTkImage(Image.open(CROSS_ICON), size=(38, 38))
        self.img_O = CTkImage(Image.open(CIRCLE_ICON), size=(38, 38))

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

    def set_player_names(self, name1, name2):
        self.player1_name = name1 or "Player 1"
        self.player2_name = name2 or "Player 2"
        self.score_p1_label.configure(text=self.player1_name)
        self.score_p2_label.configure(text=self.player2_name)
        self._update_status()

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
            text="Player vs Player",
            font=("Helvetica", 12),
            text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT)
        ).pack(pady=(2, 0))

    def _build_scoreboard(self):
        outer = CTkFrame(self.frame, fg_color="transparent")
        outer.pack(pady=(12, 0), padx=24, fill="x")

        p1_card = CTkFrame(
            outer,
            fg_color=(LIGHT_SURFACE, DARK_SURFACE),
            corner_radius=16,
            border_width=1,
            border_color=(LIGHT_BORDER, DARK_BORDER)
        )
        p1_card.pack(side=LEFT, expand=True, fill="both", padx=(0, 6))

        CTkLabel(
            p1_card,
            image=CTkImage(Image.open(CROSS_ICON), size=(20, 20)),
            text=""
        ).pack(pady=(10, 2))

        self.score_p1_label = CTkLabel(
            p1_card,
            text=self.player1_name,
            font=("Helvetica", 11),
            text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT)
        )
        self.score_p1_label.pack()

        self.score_p1 = CTkLabel(
            p1_card,
            text="0",
            font=("Helvetica", 24, "bold"),
            text_color=(ACCENT, ACCENT_LIGHT)
        )
        self.score_p1.pack(pady=(2, 10))

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

        p2_card = CTkFrame(
            outer,
            fg_color=(LIGHT_SURFACE, DARK_SURFACE),
            corner_radius=16,
            border_width=1,
            border_color=(LIGHT_BORDER, DARK_BORDER)
        )
        p2_card.pack(side=LEFT, expand=True, fill="both", padx=(6, 0))

        CTkLabel(
            p2_card,
            image=CTkImage(Image.open(CIRCLE_ICON), size=(20, 20)),
            text=""
        ).pack(pady=(10, 2))

        self.score_p2_label = CTkLabel(
            p2_card,
            text=self.player2_name,
            font=("Helvetica", 11),
            text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT)
        )
        self.score_p2_label.pack()

        self.score_p2 = CTkLabel(
            p2_card,
            text="0",
            font=("Helvetica", 24, "bold"),
            text_color=(LOSE_COLOR, LOSE_COLOR)
        )
        self.score_p2.pack(pady=(2, 10))

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
            text="",
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
            btn = CTkButton(
                board_inner,
                text="",
                width=88,
                height=88,
                corner_radius=14,
                fg_color=(LIGHT_SURFACE2, DARK_SURFACE2),
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

    def _update_status(self):
        if self.current_turn == 1:
            name = self.player1_name
            symbol = "X"
        else:
            name = self.player2_name
            symbol = "O"
        self.result_label.configure(
            text=f"{name}'s turn  ({symbol})",
            text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT)
        )

    def click(self, i):
        if self.board[i] != "":
            return

        symbol = "X" if self.current_turn == 1 else "O"
        img = self.img_X if self.current_turn == 1 else self.img_O

        self.board[i] = symbol
        self.buttons[i].configure(image=img, text="", fg_color=(LIGHT_SURFACE2, DARK_SURFACE2))

        if self.check_winner():
            return
        if self.check_draw():
            return

        self.current_turn = 2 if self.current_turn == 1 else 1
        self._update_status()

    def check_winner_sim(self, board, player):
        win_conditions = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for a, b, c in win_conditions:
            if board[a] == board[b] == board[c] == player:
                return True
        return False

    def check_winner(self):
        win_conditions = [
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
        ]
        for a, b, c in win_conditions:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != "":
                if self.board[a] == "X":
                    self.player1_score += 1
                    self.score_p1.configure(text=str(self.player1_score))
                    self.result_label.configure(
                        text=f"{self.player1_name} Wins!",
                        text_color=(WIN_COLOR, WIN_COLOR)
                    )
                else:
                    self.player2_score += 1
                    self.score_p2.configure(text=str(self.player2_score))
                    self.result_label.configure(
                        text=f"{self.player2_name} Wins!",
                        text_color=(WIN_COLOR, WIN_COLOR)
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
        self.current_turn = 1
        for btn in self.buttons:
            btn.configure(image=None, text="", state=NORMAL, fg_color=(LIGHT_SURFACE2, DARK_SURFACE2))
        self._update_status()
