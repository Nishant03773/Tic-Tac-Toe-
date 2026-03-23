from customtkinter import *
from PIL import Image
from ai_game import Game
from pvp_game import PvPGame
from about_screen import AboutScreen
from components import TopBar, ButtonManager
from config import (
    DEFAULT_BUTTON_THEME, ACCENT_BUTTON_THEME,
    DARK_BG, DARK_SURFACE, DARK_SURFACE2, DARK_TEXT, DARK_SUBTEXT, DARK_BORDER,
    LIGHT_BG, LIGHT_SURFACE, LIGHT_SURFACE2, LIGHT_TEXT, LIGHT_SUBTEXT, LIGHT_BORDER,
    ACCENT
)
from assest import *


class App:
    def __init__(self):
        self.app = CTk()
        self.app.geometry("420x720")
        self.app.resizable(False, False)
        self.app.title("Tic Tac Toe")

        set_appearance_mode("system")

        self.home_frame = CTkFrame(self.app, fg_color=(LIGHT_BG, DARK_BG))
        self.home_frame.pack(fill="both", expand=True)

        self.img_logo = CTkImage(Image.open(GAME_LOGO), size=(90, 90))

        self.btn_manager = ButtonManager()

        self.topbar = TopBar(
            self.home_frame,
            DEFAULT_BUTTON_THEME,
            self.close_app,
            self.btn_manager
        )
        self.btn_manager.add(*self.topbar.btn_list)

        self._build_hero()
        self._build_name_entries()
        self._build_action_buttons()

        self.btn_manager.add(self.btn_solo, self.btn_1v1, self.btn_about)
        self.btn_manager.update_borders(self.is_dark())

        self.solo_screen = Game(
            self.app,
            self.show_home,
            self.close_app,
            self.btn_manager
        )

        self.pvp_screen = PvPGame(
            self.app,
            self.show_home,
            self.close_app,
            self.btn_manager
        )

        self.about_screen = AboutScreen(
            self.app,
            self.show_home,
            self.close_app,
            self.btn_manager
        )

        self.app.mainloop()

    def close_app(self):
        self.app.destroy()

    def show_home(self):
        self.solo_screen.frame.pack_forget()
        self.pvp_screen.frame.pack_forget()
        self.about_screen.frame.pack_forget()
        self.app.geometry("420x740")
        self.home_frame.pack(fill="both", expand=True)

    def show_about(self):
        self.home_frame.pack_forget()
        self.app.geometry("420x740")
        self.about_screen.frame.pack(fill="both", expand=True)

    def show_solo(self):
        name = self.name1_entry.get().strip() or "You"
        self.solo_screen.set_player_name(name)
        self.home_frame.pack_forget()
        self.app.geometry("420x740")
        self.solo_screen.frame.pack(fill="both", expand=True)

    def show_pvp(self):
        name1 = self.name1_entry.get().strip() or "Player 1"
        name2 = self.name2_entry.get().strip() or "Player 2"
        self.pvp_screen.set_player_names(name1, name2)
        self.home_frame.pack_forget()
        self.app.geometry("420x740")
        self.pvp_screen.frame.pack(fill="both", expand=True)

    def is_dark(self):
        return get_appearance_mode() == "Dark"

    def _build_hero(self):
        hero = CTkFrame(self.home_frame, fg_color="transparent")
        hero.pack(pady=(24, 0))

        CTkLabel(hero, image=self.img_logo, text="").pack()

        CTkLabel(
            hero,
            text="Tic-Tac-Toe",
            font=("Helvetica", 28, "bold"),
            text_color=(LIGHT_TEXT, DARK_TEXT)
        ).pack(pady=(12, 4))

        CTkLabel(
            hero,
            text="Play with AI or a friend",
            font=("Helvetica", 13),
            text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT)
        ).pack()

    def _build_name_entries(self):
        wrapper = CTkFrame(self.home_frame, fg_color="transparent")
        wrapper.pack(pady=(28, 0), padx=28, fill="x")

        CTkLabel(
            wrapper,
            text="Player 1 Name",
            font=("Helvetica", 12, "bold"),
            text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT),
            anchor="w"
        ).pack(anchor="w", pady=(0, 6))

        self.name1_entry = CTkEntry(
            wrapper,
            placeholder_text="Enter Player 1 name...",
            height=46,
            font=("Helvetica", 14),
            fg_color=(LIGHT_SURFACE, DARK_SURFACE),
            border_color=(LIGHT_BORDER, DARK_BORDER),
            border_width=1,
            corner_radius=12,
            text_color=(LIGHT_TEXT, DARK_TEXT),
            placeholder_text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT)
        )
        self.name1_entry.pack(fill="x")

        divider = CTkFrame(
            wrapper,
            fg_color=(LIGHT_BORDER, DARK_BORDER),
            height=1
        )
        divider.pack(fill="x", pady=14)

        CTkLabel(
            wrapper,
            text="Player 2 Name",
            font=("Helvetica", 12, "bold"),
            text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT),
            anchor="w"
        ).pack(anchor="w", pady=(0, 6))

        self.name2_entry = CTkEntry(
            wrapper,
            placeholder_text="Enter Player 2 name...",
            height=46,
            font=("Helvetica", 14),
            fg_color=(LIGHT_SURFACE, DARK_SURFACE),
            border_color=(LIGHT_BORDER, DARK_BORDER),
            border_width=1,
            corner_radius=12,
            text_color=(LIGHT_TEXT, DARK_TEXT),
            placeholder_text_color=(LIGHT_SUBTEXT, DARK_SUBTEXT)
        )
        self.name2_entry.pack(fill="x")

    def _build_action_buttons(self):
        wrapper = CTkFrame(self.home_frame, fg_color="transparent")
        wrapper.pack(pady=(20, 0), padx=28, fill="x")

        self.btn_solo = CTkButton(
            wrapper,
            text="Play vs AI",
            height=50,
            font=("Helvetica", 15, "bold"),
            command=self.show_solo,
            **ACCENT_BUTTON_THEME
        )
        self.btn_solo.pack(fill="x", pady=(0, 10))

        self.btn_1v1 = CTkButton(
            wrapper,
            text="Play 1v1",
            height=50,
            font=("Helvetica", 15, "bold"),
            command=self.show_pvp,
            **DEFAULT_BUTTON_THEME
        )
        self.btn_1v1.pack(fill="x", pady=(0, 10))

        self.btn_about = CTkButton(
            wrapper,
            text="About",
            height=50,
            font=("Helvetica", 15, "bold"),
            command=self.show_about,
            **DEFAULT_BUTTON_THEME
        )
        self.btn_about.pack(fill="x")



if __name__ == "__main__":
    App()
