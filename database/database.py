
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "nr35.db"


class Database:
    def __init__(self):
        self.conexao = sqlite3.connect(DB_PATH)
        self.criar_tabelas()

    def criar_tabelas(self):
        tabelas = [
            """
            CREATE TABLE IF NOT EXISTS colaboradores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                registro TEXT NOT NULL UNIQUE,
                setor TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS equipamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                ca TEXT NOT NULL,
                quantidade INTEGER NOT NULL DEFAULT 0,
                fabricante TEXT NOT NULL,
                validade TEXT NOT NULL,
                observacoes TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                colaborador TEXT NOT NULL,
                equipamento TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                data TEXT NOT NULL,
                hora TEXT NOT NULL
            )
            """
        ]

        with self.conexao:
            for sql in tabelas:
                self.conexao.execute(sql)

    def executar(self, sql, parametros=()):
        with self.conexao:
            return self.conexao.execute(sql, parametros)

    def consultar(self, sql, parametros=()):
        return self.conexao.execute(sql, parametros).fetchall()

    def consultar_um(self, sql, parametros=()):
        return self.conexao.execute(sql, parametros).fetchone()

    # Colaboradores

    def cadastrar_colaborador(self, nome, registro, setor):
        self.executar(
            "INSERT INTO colaboradores (nome, registro, setor) VALUES (?, ?, ?)",
            (nome.strip(), registro.strip(), setor.strip())
        )

    def listar_colaboradores(self):
        return self.consultar(
            "SELECT id, nome, registro, setor FROM colaboradores ORDER BY nome"
        )

    def pesquisar_colaboradores(self, termo):
        busca = f"%{termo.strip()}%"
        return self.consultar("""
            SELECT id, nome, registro, setor FROM colaboradores
            WHERE nome LIKE ? OR registro LIKE ? OR setor LIKE ?
            ORDER BY nome
        """, (busca,) * 3)

    def atualizar_colaborador(self, id_colaborador, nome, registro, setor):
        self.executar("""
            UPDATE colaboradores SET nome = ?, registro = ?, setor = ?
            WHERE id = ?
        """, (nome.strip(), registro.strip(), setor.strip(), id_colaborador))

    def excluir_colaborador(self, id_colaborador):
        self.executar(
            "DELETE FROM colaboradores WHERE id = ?", (id_colaborador,)
        )

    def nomes_colaboradores(self):
        return [
            linha[0] for linha in self.consultar(
                "SELECT nome FROM colaboradores ORDER BY nome"
            )
        ]

    # Equipamentos

    def cadastrar_equipamento(
        self, nome, ca, quantidade, fabricante, validade, observacoes=""
    ):
        self.executar("""
            INSERT INTO equipamentos
            (nome, ca, quantidade, fabricante, validade, observacoes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            nome.strip(), ca.strip(), int(quantidade),
            fabricante.strip(), validade.strip(), observacoes.strip()
        ))

    def listar_equipamentos(self):
        return self.consultar("""
            SELECT id, nome, ca, quantidade, fabricante, validade
            FROM equipamentos ORDER BY nome
        """)

    def pesquisar_equipamentos(self, termo):
        busca = f"%{termo.strip()}%"
        return self.consultar("""
            SELECT id, nome, ca, quantidade, fabricante, validade
            FROM equipamentos
            WHERE nome LIKE ? OR ca LIKE ?
               OR fabricante LIKE ? OR validade LIKE ?
            ORDER BY nome
        """, (busca,) * 4)

    def buscar_equipamento_por_id(self, id_equipamento):
        return self.consultar_um(
            "SELECT * FROM equipamentos WHERE id = ?", (id_equipamento,)
        )

    def atualizar_equipamento(
        self, id_equipamento, nome, ca, quantidade,
        fabricante, validade, observacoes=""
    ):
        self.executar("""
            UPDATE equipamentos
            SET nome = ?, ca = ?, quantidade = ?,
                fabricante = ?, validade = ?, observacoes = ?
            WHERE id = ?
        """, (
            nome.strip(), ca.strip(), int(quantidade),
            fabricante.strip(), validade.strip(),
            observacoes.strip(), id_equipamento
        ))

    def excluir_equipamento(self, id_equipamento):
        self.executar(
            "DELETE FROM equipamentos WHERE id = ?", (id_equipamento,)
        )

    def nomes_equipamentos(self):
        return [
            linha[0] for linha in self.consultar(
                "SELECT nome FROM equipamentos ORDER BY nome"
            )
        ]

    def buscar_quantidade_equipamento(self, nome):
        resultado = self.consultar_um(
            "SELECT quantidade FROM equipamentos WHERE nome = ?", (nome,)
        )
        return resultado[0] if resultado else None

    def alterar_quantidade(self, nome, quantidade):
        self.executar(
            "UPDATE equipamentos SET quantidade = ? WHERE nome = ?",
            (int(quantidade), nome)
        )

    # Movimentações

    def registrar_movimentacao(
        self, colaborador, equipamento, quantidade, tipo, data, hora
    ):
        self.executar("""
            INSERT INTO movimentacoes
            (colaborador, equipamento, quantidade, tipo, data, hora)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (colaborador, equipamento, int(quantidade), tipo, data, hora))

    def movimentar_estoque(self, colaborador, equipamento, quantidade, tipo):
        colaborador, equipamento = colaborador.strip(), equipamento.strip()

        if tipo not in ("Retirada", "Devolução"):
            raise ValueError("Tipo de movimentação inválido.")
        if type(quantidade) is not int or quantidade <= 0:
            raise ValueError("Informe uma quantidade inteira positiva.")

        diferenca = -quantidade if tipo == "Retirada" else quantidade
        agora = datetime.now()

        with self.conexao:
            existe = self.conexao.execute(
                "SELECT 1 FROM colaboradores WHERE nome = ?", (colaborador,)
            ).fetchone()

            if not existe:
                raise ValueError("Colaborador não cadastrado.")

            equipamentos = self.conexao.execute(
                "SELECT id FROM equipamentos WHERE nome = ?", (equipamento,)
            ).fetchall()

            if len(equipamentos) != 1:
                raise ValueError("Equipamento não encontrado ou nome duplicado.")

            id_equipamento = equipamentos[0][0]

            cursor = self.conexao.execute("""
                UPDATE equipamentos SET quantidade = quantidade + ?
                WHERE id = ? AND quantidade + ? >= 0
            """, (diferenca, id_equipamento, diferenca))

            if cursor.rowcount != 1:
                raise ValueError("Estoque insuficiente.")

            self.conexao.execute("""
                INSERT INTO movimentacoes
                (colaborador, equipamento, quantidade, tipo, data, hora)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                colaborador, equipamento, quantidade, tipo,
                agora.strftime("%d/%m/%Y"),
                agora.strftime("%H:%M:%S")
            ))

            resultado = self.conexao.execute(
                "SELECT quantidade FROM equipamentos WHERE id = ?",
                (id_equipamento,)
            ).fetchone()

        return resultado[0]

    def listar_movimentacoes(self):
        return self.consultar("""
            SELECT data, hora, colaborador, equipamento, tipo, quantidade
            FROM movimentacoes ORDER BY id DESC
        """)

    def ultimas_movimentacoes(self, limite=5):
        return self.consultar("""
            SELECT data, hora, colaborador, equipamento, tipo, quantidade
            FROM movimentacoes ORDER BY id DESC LIMIT ?
        """, (limite,))

    def pesquisar_movimentacoes(self, termo):
        busca = f"%{termo.strip()}%"
        return self.consultar("""
            SELECT data, hora, colaborador, equipamento, tipo, quantidade
            FROM movimentacoes
            WHERE colaborador LIKE ? OR equipamento LIKE ?
               OR tipo LIKE ? OR data LIKE ?
            ORDER BY id DESC
        """, (busca,) * 4)

    def limpar_movimentacoes(self):
        self.executar("DELETE FROM movimentacoes")

    # Dashboard

    def contar(self, tabela, condicao=""):
        if tabela not in ("colaboradores", "equipamentos", "movimentacoes"):
            raise ValueError("Tabela inválida.")
        if condicao and (
            tabela != "movimentacoes"
            or condicao not in ("Retirada", "Devolução")
        ):
            raise ValueError("Condição inválida.")

        sql = f"SELECT COUNT(*) FROM {tabela}"
        parametros = ()

        if condicao:
            sql += " WHERE tipo = ?"
            parametros = (condicao,)

        return self.consultar_um(sql, parametros)[0]

    def total_colaboradores(self):
        return self.contar("colaboradores")

    def total_equipamentos(self):
        return self.contar("equipamentos")

    def total_estoque(self):
        return self.consultar_um(
            "SELECT COALESCE(SUM(quantidade), 0) FROM equipamentos"
        )[0]

    def total_retiradas(self):
        return self.contar("movimentacoes", "Retirada")

    def total_devolucoes(self):
        return self.contar("movimentacoes", "Devolução")

    def fechar(self):
        self.conexao.close()
