
import customtkinter as ctk

from assets.theme.theme import (
    RADIUS, PRIMARY, PRIMARY_HOVER, TEXT, FONT_TEXT,
    CARD_DARK, BORDER, DANGER, DANGER_HOVER,
    FONT_TITLE, FONT_SUBTITLE, TEXT_SECONDARY, CARD
)


class BotaoBase(ctk.CTkButton):
    def __init__(self, master, text, command, width, cor, hover, altura=42):
        super().__init__(
            master, text=text, command=command,
            width=width, height=altura,
            corner_radius=RADIUS, fg_color=cor,
            hover_color=hover, text_color=TEXT, font=FONT_TEXT
        )


class BotaoPrimario(BotaoBase):
    def __init__(self, master, text, command=None, width=330):
        super().__init__(
            master, text, command, width,
            PRIMARY, PRIMARY_HOVER, altura=48
        )


class BotaoSecundario(BotaoBase):
    def __init__(self, master, text, command=None, width=140):
        super().__init__(
            master, text, command, width, CARD_DARK, BORDER
        )


class BotaoPerigo(BotaoBase):
    def __init__(self, master, text, command=None, width=140):
        super().__init__(
            master, text, command, width, DANGER, DANGER_HOVER
        )


class TituloPagina(ctk.CTkFrame):
    def __init__(self, master, titulo, subtitulo=None):
        super().__init__(master, fg_color="transparent")
        self.pack(fill="x", pady=(20, 10))

        ctk.CTkLabel(
            self, text=titulo, font=FONT_TITLE, text_color=TEXT
        ).pack()

        if subtitulo:
            ctk.CTkLabel(
                self, text=subtitulo,
                font=FONT_SUBTITLE, text_color=TEXT_SECONDARY
            ).pack(pady=(5, 0))


class CardDashboard(ctk.CTkFrame):
    def __init__(self, master, icone, titulo, valor):
        super().__init__(
            master, width=210, height=115,
            corner_radius=14, fg_color=CARD
        )
        self.grid_propagate(False)

        topo = ctk.CTkFrame(self, fg_color="transparent")
        topo.pack(fill="x", padx=14, pady=(10, 0))

        ctk.CTkLabel(
            topo, text=icone,
            font=("Segoe UI Symbol", 22),
            text_color=PRIMARY
        ).pack(side="left")

        ctk.CTkLabel(
            topo, text=titulo,
            font=("Segoe UI", 13, "bold"),
            text_color=TEXT
        ).pack(side="left", padx=8)

        ctk.CTkFrame(
            self, height=2, fg_color=BORDER
        ).pack(fill="x", padx=14, pady=5)

        ctk.CTkLabel(
            self, text=str(valor),
            font=("Segoe UI", 28, "bold"),
            text_color=PRIMARY
        ).pack(expand=True)
