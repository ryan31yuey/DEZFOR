
import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime

from database.database import Database


class Equipamentos(ctk.CTkFrame):
    CAMPOS = {
        "nome": "Nome do equipamento",
        "ca": "Número do CA",
        "quantidade": "Quantidade",
        "fabricante": "Fabricante",
        "validade": "Validade (DD/MM/AAAA)",
        "observacoes": "Observações (opcional)"
    }

    COLUNAS = {
        "id": ("ID", 50),
        "nome": ("Equipamento", 220),
        "ca": ("CA", 110),
        "quantidade": ("Qtd", 80),
        "fabricante": ("Fabricante", 160),
        "validade": ("Validade", 140)
    }

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.banco = Database()
        self.id_selecionado = None
        self.campos = {}

        ctk.CTkLabel(
            self, text="Equipamentos",
            font=("Segoe UI", 28, "bold")
        ).pack(pady=(15, 10))

        formulario = ctk.CTkFrame(self)
        formulario.pack(pady=5)

        for nome, placeholder in self.CAMPOS.items():
            campo = ctk.CTkEntry(
                formulario, placeholder_text=placeholder,
                width=560, height=36
            )
            campo.pack(padx=20, pady=5)
            self.campos[nome] = campo

        botoes = ctk.CTkFrame(formulario, fg_color="transparent")
        botoes.pack(pady=12)

        for texto, comando, cor in [
            ("Salvar", self.salvar_equipamento, None),
            ("Atualizar", self.atualizar_equipamento, None),
            ("Excluir", self.excluir_equipamento, "#b71c1c")
        ]:
            opcoes = {"fg_color": cor} if cor else {}
            ctk.CTkButton(
                botoes, text=texto, width=150,
                height=40, command=comando, **opcoes
            ).pack(side="left", padx=5)

        self.pesquisa = ctk.CTkEntry(
            self, placeholder_text="Pesquisar equipamento...",
            width=760, height=38
        )
        self.pesquisa.pack(pady=10)
        self.pesquisa.bind("<KeyRelease>", self.atualizar_lista)

        self.tabela = ttk.Treeview(
            self, columns=list(self.COLUNAS),
            show="headings", height=7
        )

        for coluna, (titulo, largura) in self.COLUNAS.items():
            self.tabela.heading(coluna, text=titulo)
            self.tabela.column(
                coluna, width=largura,
                anchor="w" if coluna in ("nome", "fabricante") else "center"
            )

        self.tabela.pack(pady=10)
        self.tabela.bind(
            "<<TreeviewSelect>>", self.selecionar_equipamento
        )
        self.atualizar_lista()

    def dados_formulario(self):
        dados = {
            nome: campo.get().strip()
            for nome, campo in self.campos.items()
        }

        if not all(
            valor for nome, valor in dados.items()
            if nome != "observacoes"
        ):
            messagebox.showwarning(
                "Atenção", "Preencha os campos obrigatórios."
            )
            return None

        if not dados["quantidade"].isdigit():
            messagebox.showwarning(
                "Atenção", "Informe uma quantidade inteira não negativa."
            )
            return None

        try:
            datetime.strptime(dados["validade"], "%d/%m/%Y")
        except ValueError:
            messagebox.showwarning(
                "Atenção", "Use uma data válida no formato DD/MM/AAAA."
            )
            return None

        dados["quantidade"] = int(dados["quantidade"])
        return list(dados.values())

    def salvar_equipamento(self):
        self.persistir()

    def atualizar_equipamento(self):
        if self.id_selecionado is None:
            messagebox.showwarning(
                "Atenção", "Selecione um equipamento."
            )
            return
        self.persistir(atualizar=True)

    def persistir(self, atualizar=False):
        dados = self.dados_formulario()
        if dados is None:
            return

        try:
            if atualizar:
                self.banco.atualizar_equipamento(
                    self.id_selecionado, *dados
                )
            else:
                self.banco.cadastrar_equipamento(*dados)
        except (ValueError, TypeError) as erro:
            messagebox.showerror("Erro", str(erro))
            return

        self.limpar_campos()
        self.atualizar_lista()

        acao = "atualizado" if atualizar else "cadastrado"
        messagebox.showinfo(
            "Sucesso", f"Equipamento {acao} com sucesso!"
        )

    def excluir_equipamento(self):
        if self.id_selecionado is None:
            messagebox.showwarning(
                "Atenção", "Selecione um equipamento."
            )
            return

        if messagebox.askyesno(
            "Excluir", "Deseja realmente excluir este equipamento?"
        ):
            self.banco.excluir_equipamento(self.id_selecionado)
            self.limpar_campos()
            self.atualizar_lista()
            messagebox.showinfo(
                "Sucesso", "Equipamento excluído com sucesso!"
            )

    def atualizar_lista(self, evento=None):
        termo = self.pesquisa.get().strip()
        registros = (
            self.banco.pesquisar_equipamentos(termo)
            if termo else self.banco.listar_equipamentos()
        )

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        for registro in registros:
            self.tabela.insert("", "end", values=registro)

    def selecionar_equipamento(self, evento=None):
        selecionados = self.tabela.selection()
        if not selecionados:
            return

        dados = self.tabela.item(selecionados[0], "values")
        self.id_selecionado = int(dados[0])

        equipamento = self.banco.buscar_equipamento_por_id(
            self.id_selecionado
        )
        if equipamento is None:
            return

        for campo, valor in zip(
            self.campos.values(), equipamento[1:]
        ):
            campo.delete(0, "end")
            campo.insert(0, "" if valor is None else str(valor))

    def limpar_campos(self):
        self.id_selecionado = None
        self.tabela.selection_remove(*self.tabela.selection())

        for campo in self.campos.values():
            campo.delete(0, "end")

    def destroy(self):
        self.banco.fechar()
        super().destroy()
