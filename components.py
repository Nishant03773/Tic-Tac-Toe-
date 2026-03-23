from customtkinter import *
from PIL import Image
from assest import *
from config import DEFAULT_BUTTON_THEME, DARK_SUBTEXT, LIGHT_SUBTEXT


class TopBar:
    def __init__(self, main_frame, default_button_theme, close_app, btn_manager):
        self.btn_manager = btn_manager

        img_light_raw = Image.open(THEME_ICON_DARK)
        img_dark_raw = Image.open(THEME_ICON_LIGHT)
        img_light_res = img_light_raw.resize((64, 64), resample=Image.LANCZOS)
        img_dark_res = img_dark_raw.resize((64, 64), resample=Image.LANCZOS)

        self.img_theme_toggle = CTkImage(
            light_image=img_light_res,
            dark_image=img_dark_res,
            size=(20, 20)
        )
        self.img_power = CTkImage(Image.open(POWER_ICON), size=(20, 20))

        self.frame1 = CTkFrame(
            main_frame,
            fg_color="transparent",
            width=400,
            height=52
        )
        self.frame1.pack(pady=(16, 0), padx=20, fill="x")
        self.frame1.pack_propagate(False)

        self.f1b2 = CTkButton(
            self.frame1,
            height=40, width=40,
            text="",
            image=self.img_power,
            command=close_app,
            **default_button_theme
        )
        self.f1b2.pack(side=LEFT)

        self.f1b1 = CTkButton(
            master=self.frame1,
            height=40, width=40,
            text="",
            image=self.img_theme_toggle,
            command=self.toggle_theme,
            **default_button_theme
        )
        self.f1b1.pack(side=RIGHT)

        self.btn_list = [self.f1b1, self.f1b2]

    def is_dark(self):
        return get_appearance_mode() == "Dark"

    def toggle_theme(self):
        if self.is_dark():
            set_appearance_mode("light")
        else:
            set_appearance_mode("dark")
        self.btn_manager.update_borders(self.is_dark())


class ButtonManager:
    def __init__(self):
        self.buttons = []

    def add(self, *btns):
        self.buttons.extend(btns)

    def update_borders(self, is_dark):
        border = 0 if is_dark else 1
        for btn in self.buttons:
            try:
                btn.configure(border_width=border)
            except Exception:
                pass
