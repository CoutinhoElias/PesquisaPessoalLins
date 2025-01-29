# from reportlab.lib.pagesizes import letter, landscape, A4
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
# from reportlab.lib import colors

# doc = SimpleDocTemplate("tabela.pdf", pagesize=landscape(A4))

# data = [
#     ['Nome', 'Idade', 'Cidade'],
#     ['Alice', '30', 'Fortaleza'],
#     ['Bruno', '25', 'Caucaia'],
#     ['Carol', '22', 'Sobral'],
# ]

# table = Table(data)

# style = TableStyle([
#     ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#     ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#     ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
# ])

# table.setStyle(style)

# elements = [table]
# doc.build(elements)




from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

doc = SimpleDocTemplate("tabela.pdf", pagesize=landscape(letter))

data = [
    ['Nome', 'Idade', 'Cidade'],
    ['Alice', '30', 'Fortaleza'],
    ['Bruno', '25', 'Caucaia'],
    ['Carol', '22', 'Sobral'],
]

table = Table(data)

style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
])

table.setStyle(style)

elements = [table]
doc.build(elements)





# import flet as ft


# def main(page: ft.Page):
#     page.title = "AlertDialog examples"
#     page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

#     dlg = ft.AlertDialog(
#         title=ft.Text("Hi, this is a non-modal dialog!"),
#         on_dismiss=lambda e: page.add(ft.Text("Non-modal dialog dismissed")),
#     )

#     def handle_close(e):
#         page.close(dlg_modal)
#         page.add(ft.Text(f"Modal dialog closed with action: {e.control.text}"))

#     dlg_modal = ft.AlertDialog(
#         modal=True,
#         title=ft.Text("Please confirm"),
#         content=ft.Text("Do you really want to delete all those files?"),
#         actions=[
#             ft.TextButton("Yes", on_click=handle_close),
#             ft.TextButton("No", on_click=handle_close),
#         ],
#         actions_alignment=ft.MainAxisAlignment.END,
#         on_dismiss=lambda e: page.add(
#             ft.Text("Modal dialog dismissed"),
#         ),
#     )

#     page.add(
#         ft.ElevatedButton("Open dialog", on_click=lambda e: page.open(dlg)),
#         ft.ElevatedButton("Open modal dialog", on_click=lambda e: page.open(dlg_modal)),
#     )


# ft.app(main)