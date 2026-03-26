from customtkinter import *
from PIL import Image
from config import (
    DEFAULT_BUTTON_THEME, ACCENT_BUTTON_THEME,
    DARK_BG, DARK_SURFACE, DARK_SURFACE2, DARK_TEXT, DARK_SUBTEXT, DARK_BORDER,
    LIGHT_BG, LIGHT_SURFACE, LIGHT_SURFACE2, LIGHT_TEXT, LIGHT_SUBTEXT, LIGHT_BORDER,
    ACCENT, ACCENT_LIGHT, WIN_COLOR, DRAW_COLOR, LOSE_COLOR
)
from assest import *
from components import *


RULES = [
    ("3×3 Grid",         "The game is played on a 3×3 board with 9 cells."),
    ("Two Symbols",      "Player 1 plays as X  ·  Player 2 (or AI) plays as O."),
    ("Take Turns",       "Players alternate turns, placing their symbol in any empty cell."),
    ("Win Condition",    "Get 3 of your symbols in a row — horizontally, vertically, or diagonally."),
    ("Draw",             "If all 9 cells are filled and no one has 3 in a row, the game is a draw."),
    ("No Do-Overs",      "A placed symbol cannot be moved or removed."),
    ("New Game",         "Use the 'New Game' button to reset the board while keeping the score."),
]

AI_RULES = [
    ("AI Mode",          "Play Solo pits you against a Machine Learning AI trained on thousands of games."),
    ("AI Logic",         "The AI first checks if it can win immediately, then blocks your winning moves, then uses its ML model to pick the best available cell."),
    ("You Go First",     "In Solo mode you always move first as X. The AI plays as O."),
]


class AboutScreen:
    def __init__(self, parent, switch_back_callback, close_app, btn_manager):
        self.frame = CTkFrame(parent, fg_color=(LIGHT_BG, DARK_BG))
        self.btn_manager = btn_manager
        self.topbar = TopBar(self.frame, DEFAULT_BUTTON_THEME, close_app, self.btn_manager)
        self.return_image = CTkImage(Image.open(LEFT_ARROW_ICON), size=(20, 20))
        self.topbar.f1b2.configure(command=switch_back_callback, image=self.return_image)


        # self._build_topbar(switch_back_callback, close_app)
        self._build_content()

    # def _build_topbar(self, switch_back_callback, close_app):
    #     from PIL import Image as _Image
    #     bar = CTkFrame(self.frame, fg_color="transparent", height=52)
    #     bar.pack(pady=(16, 0), padx=20, fill="x")
    #     bar.pack_propagate(False)

    #     back_img = CTkImage(_Image.open(LEFT_ARROW_ICON), size=(20, 20))
    #     back_btn = CTkButton(
    #         bar,
    #         height=40, width=40,
    #         text="",
    #         image=back_img,
    #         command=switch_back_callback,
    #         **DEFAULT_BUTTON_THEME
    #     )
        # back_btn.pack(side=LEFT)
        # self.btn_manager.add(back_btn)

        # power_img = CTkImage(_Image.open(POWER_ICON), size=(20, 20))
        # power_btn = CTkButton(
        #     bar,
        #     height=40, width=40,
        #     text="",
        #     image=power_img,
        #     command=close_app,
        #     **DEFAULT_BUTTON_THEME
        # )
        # power_btn.pack(side=RIGHT)
        # self.btn_manager.add(power_btn)

    def _build_content(self):
        scroll = CTkScrollableFrame(
            self.frame,
            fg_color="transparent",
            scrollbar_button_color=(LIGHT_BORDER, DARK_BORDER),
            scrollbar_button_hover_color=(LIGHT_SUBTEXT, DARK_SUBTEXT),
        )
        scroll.pack(fill="both", expand=True, padx=20, pady=(12, 16))

        self._section_header(scroll, "About the Game")

        about_card = CTkFrame(
            scroll,
            fg_color=(LIGHT_SURFACE, DARK_SURFACE),
            corner_radius=16,
            border_width=1,
            border_color=(LIGHT_BORDER, DARK_BORDER)
        )
        about_card.pack(fill="x", pady=(0, 20))

        CTkLabel(
            about_card,
            text=(
                "Tic-Tac-Toe is a classic two-player strategy game. "
                "Simple to learn, yet surprisingly deep — the right move "
                "can mean the difference between victory and defeat."
            ),
            font=("Helvetica", 13),
            text_color=(LIGHT_TEXT, DARK_TEXT),
            wraplength=330,
            justify="left",
            anchor="w"
        ).pack(padx=16, pady=14, anchor="w")

        self._section_header(scroll, "Game Rules")
        self._rule_cards(scroll, RULES)

        self._section_header(scroll, "AI Opponent")
        self._rule_cards(scroll, AI_RULES, accent=True)

        self._section_header(scroll, "Win Patterns")
        self._win_patterns(scroll)

    def _section_header(self, parent, text):
        CTkLabel(
            parent,
            text=text,
            font=("Helvetica", 15, "bold"),
            text_color=(LIGHT_TEXT, DARK_TEXT),
            anchor="w"
        ).pack(anchor="w", pady=(6, 8))

    def _rule_cards(self, parent, rules, accent=False):
        container = CTkFrame(
            parent,
            fg_color=(LIGHT_SURFACE, DARK_SURFACE),
            corner_radius=16,
            border_width=1,
            border_color=(LIGHT_BORDER, DARK_BORDER)
        )
        container.pack(fill="x", pady=(0, 20))

        for idx, (title, desc) in enumerate(rules):
            row = CTkFrame(container, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=(12 if idx == 0 else 4, 4))

            num_color = (ACCENT, ACCENT_LIGHT) if not accent else (WIN_COLOR, WIN_COLOR)
            badge = CTkFrame(
                row,
                width=24, height=24,
                corner_radius=12,
                fg_color=num_color
            )
            badge.pack(side=LEFT, anchor="n", pady=(3, 0))
            badge.pack_propagate(False)
            CTkLabel(
                badge,
                text=f"{idx + 1}",
                font=("Helvetica", 11, "bold"),
                text_color="white"
            ).place(relx=0.5, rely=0.5, anchor="center")

            text_col = CTkFrame(row, fg_color="transparent")
            text_col.pack(side=LEFT, fill="x", expand=True, padx=(10, 0))

            CTkLabel(
                text_col,
                text=title,
                font=("Helvetica", 13, "bold"),
                text_color=(LIGHT_TEXT, DARK_TEXT),
                anchor="w"
            ).pack(anchor="w")

            CTkLabel(
                text_col,
                text=desc,
                font=("Helvetica", 12),
                text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT),
                wraplength=310,
                justify="left",
                anchor="w"
            ).pack(anchor="w", pady=(1, 0))

            if idx < len(rules) - 1:
                CTkFrame(
                    container,
                    fg_color=(LIGHT_BORDER, DARK_BORDER),
                    height=1
                ).pack(fill="x", padx=14, pady=(8, 0))

        CTkFrame(container, fg_color="transparent", height=10).pack()

    def _win_patterns(self, parent):
        card = CTkFrame(
            parent,
            fg_color=(LIGHT_SURFACE, DARK_SURFACE),
            corner_radius=16,
            border_width=1,
            border_color=(LIGHT_BORDER, DARK_BORDER)
        )
        card.pack(fill="x", pady=(0, 20))

        patterns = [
            ("Rows",       "━━━  Top, middle, or bottom row"),
            ("Columns",    "┃┃┃  Left, center, or right column"),
            ("Diagonals",  "╲ ╱  Top-left→bottom-right  or  top-right→bottom-left"),
        ]

        for idx, (label, desc) in enumerate(patterns):
            row = CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=(12 if idx == 0 else 4, 4))

            CTkLabel(
                row,
                text=label,
                font=("Helvetica", 13, "bold"),
                width=80,
                text_color=(ACCENT, ACCENT_LIGHT),
                anchor="w"
            ).pack(side=LEFT)

            CTkLabel(
                row,
                text=desc,
                font=("Helvetica", 12),
                text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT),
                anchor="w"
            ).pack(side=LEFT, padx=(4, 0))

            if idx < len(patterns) - 1:
                CTkFrame(
                    card,
                    fg_color=(LIGHT_BORDER, DARK_BORDER),
                    height=1
                ).pack(fill="x", padx=14, pady=(8, 0))

        CTkFrame(card, fg_color="transparent", height=10).pack()
