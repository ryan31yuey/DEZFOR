
import customtkinter as ctk

from assets.theme.theme import (
    BACKGROUND, CARD, CARD_DARK, PRIMARY,
    PRIMARY_HOVER, TEXT, TEXT_SECONDARY,
    FONT_TEXT, FONT_SMALL
)
from ui.dashboard import Dashboard
from ui.colaboradores import Colaboradores
from ui.equipamentos import Equipamentos
from ui.estoque import Estoque
from ui.historico import Historico
from ui.relatorios import Relatorios


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class DezforApp:
    TELAS = {
        "Dashboard": ("⌂", Dashboard),
        "Colaboradores": ("♙", Colaboradores),
        "Equipamentos": ("▣", Equipamentos),
        "Estoque": ("▤", Estoque),
        "Histórico": ("◷", Historico),
        "Relatórios": ("▤", Relatorios),
    }

    def __init__(self, janela):
        self.janela = janela
        self.janela.title("DEZFOR")
        self.janela.geometry("1200x700")
        self.janela.resizable(False, False)
        self.botoes_menu = {}
        self.criar_layout()

    def criar_layout(self):
        topo = ctk.CTkFrame(
            self.janela, height=70, corner_radius=0,
            fg_color=CARD_DARK
        )
        topo.pack(fill="x")

        ctk.CTkLabel(
            topo, text="◆ DEZFOR",
            font=("Segoe UI", 24, "bold"),
            text_color=PRIMARY
        ).pack(side="left", padx=25)

        ctk.CTkLabel(
            topo, text="Painel de gerenciamento",
            font=FONT_TEXT, text_color=TEXT_SECONDARY
        ).pack(side="right", padx=25)

        corpo = ctk.CTkFrame(
            self.janela, fg_color=BACKGROUND, corner_radius=0
        )
        corpo.pack(fill="both", expand=True)

        menu = ctk.CTkFrame(
            corpo, width=240, fg_color=CARD,
            corner_radius=0
        )
        menu.pack(side="left", fill="y")
        menu.pack_propagate(False)

        self.area_principal = ctk.CTkFrame(
            corpo, fg_color=BACKGROUND,
            corner_radius=0
        )
        self.area_principal.pack(
            side="right", fill="both", expand=True
        )

        ctk.CTkLabel(
            menu, text="◆",
            font=("Segoe UI", 42),
            text_color=PRIMARY
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            menu, text="DEZFOR",
            font=("Segoe UI", 22, "bold"),
            text_color=PRIMARY
        ).pack()

        ctk.CTkLabel(
            menu, text="Gestão Inteligente",
            font=("Segoe UI", 11),
            text_color=TEXT_SECONDARY
        ).pack(pady=(0, 25))

        for nome, (icone, tela) in self.TELAS.items():
            botao = ctk.CTkButton(
                menu,
                text=f"{icone}  {nome}",
                width=200,
                height=42,
                corner_radius=12,
                anchor="w",
                font=FONT_TEXT,
                fg_color="transparent",
                hover_color=PRIMARY_HOVER,
                text_color=TEXT,
                command=lambda t=tela, n=nome: self.trocar_tela(t, n)
            )
            botao.pack(pady=6, padx=20)
            self.botoes_menu[nome] = botao

        ctk.CTkLabel(
            menu, text="Versão 1.0",
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY
        ).pack(side="bottom", pady=20)

        self.trocar_tela(Dashboard, "Dashboard")

    def trocar_tela(self, tela, nome):
        for widget in self.area_principal.winfo_children():
            widget.destroy()

        for titulo, botao in self.botoes_menu.items():
            botao.configure(
                fg_color=PRIMARY if titulo == nome else "transparent"
            )

        tela(self.area_principal)
