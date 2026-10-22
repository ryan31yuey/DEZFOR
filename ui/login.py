
import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path

from assets.theme.theme import (
    BACKGROUND, CARD, PRIMARY, TEXT_SECONDARY,
    FONT_TITLE, FONT_SUBTITLE, FONT_TEXT, FONT_SMALL
)
from database.auth import autenticar
from ui.components import BotaoPrimario


ARQUIVO_USUARIO = (
    Path(__file__).resolve().parent.parent / ".usuario_local"
)


class Login(ctk.CTkFrame):
    def __init__(self, master, abrir_sistema):
        super().__init__(master, fg_color=BACKGROUND)

        self.abrir_sistema = abrir_sistema
        self.pack(fill="both", expand=True)

        self.criar_interface()
        self.carregar_usuario()

    def criar_interface(self):
        caixa = ctk.CTkFrame(
            self,
            width=460,
            height=520,
            corner_radius=18,
            fg_color=CARD
        )
        caixa.place(relx=0.5, rely=0.5, anchor="center")
        caixa.pack_propagate(False)

        def texto(conteudo, fonte, cor=TEXT_SECONDARY, pady=0):
            label = ctk.CTkLabel(
                caixa,
                text=conteudo,
                font=fonte,
                text_color=cor
            )
            label.pack(pady=pady)
            return label

        texto("◆", ("Segoe UI", 55), PRIMARY, (25, 5))
        texto("DEZFOR", FONT_TITLE, PRIMARY)
        texto(
            "Gestão Inteligente",
            FONT_SUBTITLE,
            pady=(0, 35)
        )

        self.campo_usuario = ctk.CTkEntry(
            caixa,
            placeholder_text="Usuário",
            width=330,
            height=45,
            corner_radius=10
        )
        self.campo_usuario.pack(pady=10)

        self.campo_senha = ctk.CTkEntry(
            caixa,
            placeholder_text="Senha",
            width=330,
            height=45,
            corner_radius=10,
            show="*"
        )
        self.campo_senha.pack(pady=10)

        self.lembrar = ctk.CTkCheckBox(
            caixa,
            text="Lembrar usuário",
            font=FONT_TEXT
        )
        self.lembrar.pack(
            anchor="w",
            padx=65,
            pady=(5, 20)
        )

        BotaoPrimario(
            caixa,
            text="ENTRAR",
            command=self.validar_login
        ).pack()

        texto(
            "Versão 1.0",
            FONT_SMALL,
            pady=(40, 0)
        )
        texto(
            "Desenvolvido por Ryan Yuey",
            FONT_SMALL
        )

        self.campo_senha.bind(
            "<Return>",
            lambda evento: self.validar_login()
        )

    def carregar_usuario(self):
        if ARQUIVO_USUARIO.exists():
            usuario = ARQUIVO_USUARIO.read_text(
                encoding="utf-8"
            ).strip()

            if usuario:
                self.campo_usuario.insert(0, usuario)
                self.lembrar.select()

    def salvar_preferencia(self, usuario):
        if self.lembrar.get():
            ARQUIVO_USUARIO.write_text(
                usuario,
                encoding="utf-8"
            )
        else:
            ARQUIVO_USUARIO.unlink(missing_ok=True)

    def validar_login(self):
        usuario = self.campo_usuario.get().strip()
        senha = self.campo_senha.get()

        if not usuario or not senha:
            messagebox.showwarning(
                "Atenção",
                "Informe o usuário e a senha."
            )
            return

        if autenticar(usuario, senha):
            self.salvar_preferencia(usuario)
            self.after_idle(self.abrir_sistema)
        else:
            messagebox.showerror(
                "Acesso negado",
                "Usuário ou senha inválidos."
            )
            self.campo_senha.delete(0, "end")
