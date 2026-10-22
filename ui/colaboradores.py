
import sqlite3
import customtkinter as ctk
from tkinter import messagebox, ttk

from database.database import Database


class Colaboradores(ctk.CTkFrame):
    CAMPOS = {
        "nome": "Nome do colaborador",
        "registro": "Matrícula / Registro",
        "setor": "Setor"
    }

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.banco = Database()
        self.id_selecionado = None
        self.campos = {}

        ctk.CTkLabel(
            self, text="Colaboradores",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(20, 10))

        formulario = ctk.CTkFrame(self)
        formulario.pack(pady=10, padx=20)

        for nome, placeholder in self.CAMPOS.items():
            campo = ctk.CTkEntry(
                formulario, placeholder_text=placeholder,
                width=400, height=40
            )
            campo.pack(padx=20, pady=8)
            self.campos[nome] = campo

        botoes = ctk.CTkFrame(formulario, fg_color="transparent")
        botoes.pack(pady=15)

        for texto, comando, cor in [
            ("Salvar", self.salvar_colaborador, None),
            ("Atualizar", self.atualizar_colaborador, None),
            ("Excluir", self.excluir_colaborador, "#b71c1c")
        ]:
            opcoes = {"fg_color": cor} if cor else {}
            ctk.CTkButton(
                botoes, text=texto, width=115,
                command=comando, **opcoes
            ).pack(side="left", padx=5)

        self.pesquisa = ctk.CTkEntry(
            self, placeholder_text="Pesquisar colaborador...",
            width=700, height=40
        )
        self.pesquisa.pack(pady=10)
        self.pesquisa.bind("<KeyRelease>", self.atualizar_lista)

        colunas = ("id", "nome", "registro", "setor")
        self.tabela = ttk.Treeview(
            self, columns=colunas, show="headings", height=8
        )

        for coluna, largura in zip(colunas, (60, 260, 150, 200)):
            self.tabela.heading(coluna, text=coluna.capitalize())
            self.tabela.column(
                coluna, width=largura,
                anchor="w" if coluna == "nome" else "center"
            )

        self.tabela.pack(pady=10)
        self.tabela.bind(
            "<<TreeviewSelect>>", self.selecionar_colaborador
        )
        self.atualizar_lista()

    def dados_formulario(self):
        dados = [
            campo.get().strip() for campo in self.campos.values()
        ]
        if not all(dados):
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return None
        return dados

    def salvar_colaborador(self):
        self.persistir()

    def atualizar_colaborador(self):
        if self.id_selecionado is None:
            messagebox.showwarning("Atenção", "Selecione um colaborador.")
            return
        self.persistir(atualizar=True)

    def persistir(self, atualizar=False):
        dados = self.dados_formulario()
        if dados is None:
            return

        try:
            if atualizar:
                self.banco.atualizar_colaborador(
                    self.id_selecionado, *dados
                )
            else:
                self.banco.cadastrar_colaborador(*dados)
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Erro", "Esta matrícula já está cadastrada."
            )
            return

        self.limpar_campos()
        self.atualizar_lista()
        acao = "atualizado" if atualizar else "cadastrado"
        messagebox.showinfo("Sucesso", f"Colaborador {acao} com sucesso!")

    def excluir_colaborador(self):
        if self.id_selecionado is None:
            messagebox.showwarning("Atenção", "Selecione um colaborador.")
            return

        if messagebox.askyesno(
            "Excluir", "Deseja realmente excluir este colaborador?"
        ):
            self.banco.excluir_colaborador(self.id_selecionado)
            self.limpar_campos()
            self.atualizar_lista()
            messagebox.showinfo("Sucesso", "Colaborador excluído.")

    def atualizar_lista(self, evento=None):
        termo = self.pesquisa.get().strip()
        registros = (
            self.banco.pesquisar_colaboradores(termo)
            if termo else self.banco.listar_colaboradores()
        )

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for registro in registros:
            self.tabela.insert("", "end", values=registro)

    def selecionar_colaborador(self, evento=None):
        selecionados = self.tabela.selection()
        if not selecionados:
            return

        id_colaborador, *dados = self.tabela.item(
            selecionados[0], "values"
        )
        self.id_selecionado = int(id_colaborador)

        for campo, valor in zip(self.campos.values(), dados):
            campo.delete(0, "end")
            campo.insert(0, valor)

    def limpar_campos(self):
        self.id_selecionado = None
        self.tabela.selection_remove(*self.tabela.selection())

        for campo in self.campos.values():
            campo.delete(0, "end")

    def destroy(self):
        self.banco.fechar()
        super().destroy()
