import io
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.pdfbase.pdfmetrics import stringWidth


def printLedger(account):
    records = account.records
    bal_state = account.bal_state
    owner = account.owner

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)

    text = f"{owner} Company"
    text_width = stringWidth(text, "Helvetica-Bold", 10) * 0.0352778 * cm
    textob = c.beginText()
    textob.setTextOrigin((21.6 * cm - text_width) / 2.0, cm * 26)
    textob.setFont("Helvetica-Bold", 14)
    textob.textLine(text)
    c.drawText(textob)

    tables = []
    for key, data in records.items():
        data = [['Description', 'Credit', 'Description', 'Debit']] + data

        t = Table(data, rowHeights=cm * 0.5, colWidths=5 * cm)
        t.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
        ]))

        tables.append([key.capitalize() + ' Account:'])
        tables.append([t])
        tables.append([''])

    tables.append([''])
    tables.append(['Balance Statement:'])
    data = [['Description', 'Credit', 'Debit']]
    data += bal_state

    t = Table(data, rowHeights=cm * 0.5, colWidths=6.5 * cm)
    t.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
    ]))
    tables.append([t])
    tables.append([''])

    t_master = Table(tables)
    t_master.wrapOn(c, 0, 0)
    t_master.drawOn(c, cm, cm)

    c.showPage()
    c.save()
    buf.seek(0)

    return buf


def printSample():
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(cm, cm)
    textob.setFont("Helvetica", 14)

    lines = [
        "This is line 1",
        "This is line 2",
        "This is line 3",
    ]

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return buf
