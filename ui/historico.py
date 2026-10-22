
import customtkinter as ctk
from tkinter import messagebox, ttk

from assets.theme.theme import BACKGROUND
from database.auth import autenticar
from database.database import Database
from ui.components import BotaoPerigo, TituloPagina


class Historico(ctk.CTkFrame):
    COLUNAS = {
        "data": ("Data", 110, "center"),
        "hora": ("Hora", 100, "center"),
        "colaborador": ("Colaborador", 230, "w"),
        "equipamento": ("Equipamento", 230, "w"),
        "tipo": ("Tipo", 120, "center"),
        "quantidade": ("Qtd", 80, "center"),
    }

    def __init__(self, master):
        super().__init__(master, fg_color=BACKGROUND)
        self.pack(fill="both", expand=True)

        TituloPagina(
            self,
            "Histórico de Movimentações",
            "Consulte retiradas e devoluções registradas no sistema."
        )

        barra = ctk.CTkFrame(self, fg_color="transparent")
        barra.pack(pady=(10, 5))

        self.pesquisa = ctk.CTkEntry(
            barra,
            width=680,
            height=40,
            placeholder_text="Pesquisar movimentações..."
        )
        self.pesquisa.pack(side="left", padx=(0, 10))
        self.pesquisa.bind("<KeyRelease>", self.atualizar_lista)

        BotaoPerigo(
            barra,
            text="Limpar Histórico",
            width=170,
            command=self.limpar_historico
        ).pack(side="left")

        self.tabela = ttk.Treeview(
            self,
            columns=list(self.COLUNAS),
            show="headings",
            height=18
        )

        for coluna, (titulo, largura, alinhamento) in self.COLUNAS.items():
            self.tabela.heading(coluna, text=titulo)
            self.tabela.column(
                coluna,
                width=largura,
                anchor=alinhamento
            )

        self.tabela.pack(pady=20)
        self.atualizar_lista()

    def atualizar_lista(self, evento=None):
        termo = self.pesquisa.get().strip()
        banco = Database()

        try:
            registros = banco.pesquisar_movimentacoes(termo)
        finally:
            banco.fechar()

        self.tabela.delete(*self.tabela.get_children())

        for registro in registros:
            self.tabela.insert("", "end", values=registro)

    def limpar_historico(self):
        banco = Database()

        try:
            registros = banco.listar_movimentacoes()
        finally:
            banco.fechar()

        if not registros:
            messagebox.showinfo(
                "Histórico vazio",
                "Não existem movimentações para excluir."
            )
            return

        janela = ctk.CTkToplevel(self)
        janela.title("Autorização administrativa")
        janela.geometry("380x260")
        janela.resizable(False, False)
        janela.transient(self.winfo_toplevel())
        janela.grab_set()

        ctk.CTkLabel(
            janela,
            text="Confirmar identidade",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            janela,
            text="Informe a senha do administrador."
        ).pack(pady=(0, 15))

        campo_senha = ctk.CTkEntry(
            janela,
            placeholder_text="Senha",
            show="*",
            width=280,
            height=40
        )
        campo_senha.pack(pady=5)
        campo_senha.focus_set()

        def confirmar_exclusao():
            if not autenticar("admin", campo_senha.get()):
                messagebox.showerror(
                    "Acesso negado",
                    "Senha administrativa incorreta.",
                    parent=janela
                )
                campo_senha.delete(0, "end")
                return

            confirmar = messagebox.askyesno(
                "Confirmar exclusão",
                "Deseja apagar permanentemente TODO o histórico?\n\n"
                "Esta operação não poderá ser desfeita.",
                parent=janela
            )

            if not confirmar:
                return

            banco = Database()

            try:
                banco.limpar_movimentacoes()
            except Exception as erro:
                messagebox.showerror(
                    "Erro",
                    f"Não foi possível limpar o histórico:\n{erro}",
                    parent=janela
                )
                return
            finally:
                banco.fechar()

            janela.destroy()
            self.atualizar_lista()

            messagebox.showinfo(
                "Histórico limpo",
                "Todas as movimentações foram excluídas."
            )

        ctk.CTkButton(
            janela,
            text="Confirmar exclusão",
            fg_color="#C62828",
            hover_color="#B71C1C",
            width=280,
            height=40,
            command=confirmar_exclusao
        ).pack(pady=20)

        campo_senha.bind(
            "<Return>",
            lambda evento: confirmar_exclusao()
        )
