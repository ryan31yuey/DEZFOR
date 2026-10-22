
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle
)

AZUL = colors.HexColor("#1976D2")
CINZA = colors.HexColor("#F3F5F8")
ARQUIVO = Path(__file__).resolve().parent / "relatorio_movimentacoes.pdf"


def gerar_pdf_movimentacoes(movimentacoes):
    ARQUIVO.parent.mkdir(parents=True, exist_ok=True)

    documento = SimpleDocTemplate(
        str(ARQUIVO), pagesize=A4,
        leftMargin=35, rightMargin=35,
        topMargin=45, bottomMargin=45
    )

    estilos = getSampleStyleSheet()
    titulo = estilos["Title"]
    titulo.textColor = AZUL

    conteudo = [
        Paragraph("DEZFOR", titulo),
        Paragraph("Relatório de Movimentações", estilos["Heading2"]),
        Paragraph(
            f"Emitido em {datetime.now():%d/%m/%Y às %H:%M}",
            estilos["Normal"]
        ),
        Spacer(1, 25)
    ]

    colunas = ["Data", "Hora", "Colaborador", "Equipamento", "Tipo", "Qtd"]
    larguras = [65, 55, 125, 125, 90, 50]

    estilo_celula = estilos["BodyText"].clone("CelulaDEZFOR")
    estilo_celula.fontName = "Helvetica"
    estilo_celula.fontSize = 8
    estilo_celula.leading = 11
    estilo_celula.wordWrap = "CJK"

    dados = [colunas] + [
        [
            Paragraph(
                str(valor).replace("&", "&amp;")
                .replace("<", "&lt;").replace(">", "&gt;"),
                estilo_celula
            )
            for valor in registro
        ]
        for registro in movimentacoes
    ]

    tabela = Table(dados, colWidths=larguras, repeatRows=1)
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, CINZA]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LINEBELOW", (0, 0), (-1, 0), 1, AZUL),
    ]))

    conteudo.append(tabela)
    documento.build(conteudo, onFirstPage=rodape, onLaterPages=rodape)

    return str(ARQUIVO)


def rodape(canvas, documento):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawString(35, 25, "DEZFOR | Gestão Inteligente")
    canvas.drawRightString(
        A4[0] - 35, 25, f"Página {documento.page}"
    )
    canvas.restoreState()
