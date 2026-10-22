
import customtkinter as ctk
from tkinter import messagebox

from assets.theme.theme import BACKGROUND, CARD, FONT_TEXT, TEXT_SECONDARY
from database.database import Database
from ui.components import BotaoSecundario, TituloPagina


class Estoque(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=BACKGROUND)
        self.pack(fill="both", expand=True)
        self.banco = Database()

        TituloPagina(
            self, "Controle de Estoque",
            "Registre retiradas e devoluções de equipamentos."
        )

        formulario = ctk.CTkFrame(
            self, width=620, height=380,
            corner_radius=18, fg_color=CARD
        )
        formulario.pack(pady=20)
        formulario.pack_propagate(False)

        self.colaborador = self.criar_combo(
            formulario, self.banco.nomes_colaboradores(),
            "Selecione o colaborador"
        )
        self.equipamento = self.criar_combo(
            formulario, self.banco.nomes_equipamentos(),
            "Selecione o equipamento",
            command=lambda _: self.atualizar_estoque()
        )

        self.label_estoque = ctk.CTkLabel(
            formulario, text="Estoque atual: -",
            font=FONT_TEXT, text_color=TEXT_SECONDARY
        )
        self.label_estoque.pack(pady=8)

        self.quantidade = ctk.CTkEntry(
            formulario, placeholder_text="Quantidade",
            width=450, height=40
        )
        self.quantidade.pack(pady=12)

        botoes = ctk.CTkFrame(formulario, fg_color="transparent")
        botoes.pack(pady=18)

        for tipo in ("Retirada", "Devolução"):
            BotaoSecundario(
                botoes, text=tipo, width=180,
                command=lambda t=tipo: self.movimentar(t)
            ).pack(side="left", padx=10)

    def criar_combo(self, master, valores, placeholder, command=None):
        combo = ctk.CTkComboBox(
            master, values=valores or [placeholder],
            width=450, height=40,
            state="readonly", command=command
        )
        combo.pack(pady=12)
        combo.set(placeholder)
        return combo

    def atualizar_estoque(self):
        equipamento = self.equipamento.get()
        quantidade = self.banco.buscar_quantidade_equipamento(equipamento)
        texto = "-" if quantidade is None else quantidade
        self.label_estoque.configure(text=f"Estoque atual: {texto}")

    def validar(self):
        colaborador = self.colaborador.get().strip()
        equipamento = self.equipamento.get().strip()
        quantidade = self.quantidade.get().strip()

        if colaborador not in self.banco.nomes_colaboradores():
            mensagem = "Selecione um colaborador válido."
        elif equipamento not in self.banco.nomes_equipamentos():
            mensagem = "Selecione um equipamento válido."
        elif not quantidade.isascii() or not quantidade.isdecimal() or int(quantidade) <= 0:
            mensagem = "Informe uma quantidade inteira maior que zero."
        else:
            return colaborador, equipamento, int(quantidade)

        messagebox.showwarning("Atenção", mensagem)
        return None

    def movimentar(self, tipo):
        dados = self.validar()
        if dados is None:
            return

        try:
            novo_estoque = self.banco.movimentar_estoque(*dados, tipo)
        except ValueError as erro:
            messagebox.showwarning("Atenção", str(erro))
            return
        except Exception:
            messagebox.showerror(
                "Erro", "Não foi possível registrar a movimentação."
            )
            return

        self.quantidade.delete(0, "end")
        self.atualizar_estoque()

        messagebox.showinfo(
            "Sucesso",
            f"{tipo} registrada com sucesso!\n"
            f"Novo estoque: {novo_estoque}"
        )

    def destroy(self):
        self.banco.fechar()
        super().destroy()
