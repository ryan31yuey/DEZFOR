
import customtkinter as ctk
from tkinter import messagebox, ttk

from assets.theme.theme import BACKGROUND
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
            self, "Histórico de Movimentações",
            "Consulte retiradas e devoluções registradas no sistema."
        )

        barra = ctk.CTkFrame(self, fg_color="transparent")
        barra.pack(pady=(10, 5))

        self.pesquisa = ctk.CTkEntry(
            barra, width=680, height=40,
            placeholder_text="Pesquisar movimentações..."
        )
        self.pesquisa.pack(side="left", padx=(0, 10))
        self.pesquisa.bind("<KeyRelease>", self.atualizar_lista)

        BotaoPerigo(
            barra, text="Limpar Histórico", width=170,
            command=self.limpar_historico
        ).pack(side="left")

        self.tabela = ttk.Treeview(
            self, columns=list(self.COLUNAS),
            show="headings", height=18
        )

        for coluna, (titulo, largura, alinhamento) in self.COLUNAS.items():
            self.tabela.heading(coluna, text=titulo)
            self.tabela.column(coluna, width=largura, anchor=alinhamento)

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
        if not self.tabela.get_children():
            messagebox.showinfo(
                "Histórico vazio",
                "Nenhuma movimentação encontrada na tabela."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Deseja apagar permanentemente todo o histórico?\n"
            "Esta operação não poderá ser desfeita."
        )

        if not confirmar:
            return

        messagebox.showinfo(
            "Operação protegida",
            "A exclusão permanente está desabilitada até "
            "configurarmos a autenticação administrativa."
        )
