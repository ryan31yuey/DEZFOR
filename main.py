
import customtkinter as ctk

from database.database import Database
from database.auth import criar_tabela
from ui.login import Login
from ui.main_window import DezforApp


def main():
    banco = Database()
    banco.fechar()
    criar_tabela()

    janela = ctk.CTk()
    janela.title("DEZFOR")
    janela.geometry("500x550")
    janela.resizable(False, False)

    def abrir_sistema():
        for widget in janela.winfo_children():
            widget.destroy()

        DezforApp(janela)

    Login(master=janela, abrir_sistema=abrir_sistema)

    janela.mainloop()


if __name__ == "__main__":
    main()
