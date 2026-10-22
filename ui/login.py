
import customtkinter as ctk
from tkinter import messagebox

from assets.theme.theme import (
    BACKGROUND, CARD, PRIMARY, TEXT_SECONDARY,
    FONT_TITLE, FONT_SUBTITLE, FONT_TEXT, FONT_SMALL
)
from ui.components import BotaoPrimario


class Login(ctk.CTkFrame):
    def __init__(self, master, abrir_sistema):
        super().__init__(master, fg_color=BACKGROUND)
        self.abrir_sistema = abrir_sistema
        self.pack(fill="both", expand=True)

        caixa = ctk.CTkFrame(
            self, width=460, height=520,
            corner_radius=18, fg_color=CARD
        )
        caixa.place(relx=0.5, rely=0.5, anchor="center")
        caixa.pack_propagate(False)

        def texto(conteudo, fonte, cor=TEXT_SECONDARY, pady=0):
            label = ctk.CTkLabel(
                caixa, text=conteudo, font=fonte, text_color=cor
            )
            label.pack(pady=pady)
            return label

        texto("◆", ("Segoe UI", 55), PRIMARY, (25, 5))
        texto("DEZFOR", FONT_TITLE, PRIMARY)
        texto("Gestão inteligente de ativos", FONT_SUBTITLE, pady=(0, 35))

        for atributo, placeholder, ocultar in (
            ("campo_usuario", "Usuário", False),
            ("campo_senha", "Senha", True)
        ):
            campo = ctk.CTkEntry(
                caixa, placeholder_text=placeholder,
                width=330, height=45, corner_radius=10,
                show="*" if ocultar else ""
            )
            campo.pack(pady=10)
            setattr(self, atributo, campo)

        ctk.CTkCheckBox(
            caixa, text="Lembrar usuário", font=FONT_TEXT
        ).pack(anchor="w", padx=65, pady=(5, 20))

        BotaoPrimario(
            caixa, text="ENTRAR", command=self.validar_login
        ).pack()

        texto("Versão 1.0", FONT_SMALL, pady=(40, 0))
        texto("Desenvolvido por Ryan Yuey", FONT_SMALL)

    def validar_login(self):
        usuario = self.campo_usuario.get().strip()
        senha = self.campo_senha.get()

        if usuario == "admin" and senha == "123456":
            self.after_idle(self.abrir_sistema)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")
