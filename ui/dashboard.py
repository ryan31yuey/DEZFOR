
import customtkinter as ctk

from database.database import Database
from assets.theme.theme import (
    BACKGROUND, CARD, PRIMARY, SUCCESS, TEXT,
    TEXT_SECONDARY, FONT_TITLE, FONT_SUBTITLE,
    FONT_TEXT, FONT_SMALL
)
from ui.components import CardDashboard


class Dashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BACKGROUND)
        self.pack(fill="both", expand=True)

        banco = Database()
        try:
            indicadores = [
                ("♙", "Colaboradores", banco.total_colaboradores()),
                ("⚙", "Equipamentos", banco.total_equipamentos()),
                ("▣", "Estoque Total", banco.total_estoque()),
                ("↗", "Retiradas", banco.total_retiradas()),
                ("↙", "Devoluções", banco.total_devolucoes()),
            ]
            movimentacoes = banco.ultimas_movimentacoes()
        finally:
            banco.fechar()

        ctk.CTkLabel(
            self, text="◆ DEZFOR",
            font=FONT_TITLE, text_color=PRIMARY
        ).pack(pady=(15, 3))

        ctk.CTkLabel(
            self, text="Gestão Inteligente",
            font=FONT_SUBTITLE, text_color=TEXT_SECONDARY
        ).pack(pady=(0, 10))

        painel = ctk.CTkFrame(self, fg_color="transparent")
        painel.pack(pady=5)

        for i, (icone, titulo, valor) in enumerate(indicadores):
            CardDashboard(
                painel, icone=icone, titulo=titulo, valor=valor
            ).grid(row=i // 3, column=i % 3, padx=10, pady=10)

        self.criar_movimentacoes(movimentacoes)

    def criar_movimentacoes(self, movimentacoes):
        painel = ctk.CTkFrame(
            self, width=680, height=220,
            corner_radius=14, fg_color=CARD
        )
        painel.pack(pady=(10, 15))
        painel.pack_propagate(False)

        ctk.CTkLabel(
            painel, text="◷ Últimas Movimentações",
            font=("Segoe UI", 17, "bold"),
            text_color=TEXT
        ).pack(anchor="w", padx=20, pady=(10, 5))

        if not movimentacoes:
            ctk.CTkLabel(
                painel, text="Nenhuma movimentação registrada.",
                font=FONT_TEXT, text_color=TEXT_SECONDARY
            ).pack(pady=20)
            return

        for data, hora, colaborador, equipamento, tipo, quantidade in movimentacoes:
            retirada = tipo == "Retirada"
            acao = "retirou" if retirada else "devolveu"
            icone = "↗" if retirada else "↙"

            ctk.CTkLabel(
                painel,
                text=f"{icone} {data} • {hora} | {colaborador} {acao} "
                     f"{quantidade}x {equipamento}",
                font=FONT_SMALL,
                text_color=PRIMARY if retirada else SUCCESS
            ).pack(anchor="w", padx=20, pady=2)
