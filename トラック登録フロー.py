from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics import renderPDF

# 日本語フォント登録
pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))

# 出力PDF
pdf_path_truck_flow = "truck_registration_flow.pdf"
doc = SimpleDocTemplate(pdf_path_truck_flow, pagesize=A4)
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleJP", fontName="HeiseiMin-W3", fontSize=18, leading=22))
styles.add(ParagraphStyle(name="NormalJP", fontName="HeiseiMin-W3", fontSize=12, leading=16))

story = []

# タイトル
story.append(Paragraph("🚛 トラック登録の処理フロー", styles["TitleJP"]))
story.append(Spacer(1, 16))

# 説明文
desc = """
この図は、トラックマスタ (truck_master) への登録処理の流れを示しています。
フォーム入力から MySQL への INSERT まで、UI・サービス層・リポジトリ層に分かれています。
"""
story.append(Paragraph(desc, styles["NormalJP"]))
story.append(Spacer(1, 16))

# 図の作成
d = Drawing(400, 300)

# UI box
d.add(Rect(50, 220, 120, 50, strokeWidth=1, strokeColor="black", fillColor=None))
d.add(String(60, 240, "UI", fontName="HeiseiMin-W3", fontSize=12))
d.add(String(60, 225, "transport_page.py", fontName="HeiseiMin-W3", fontSize=10))

# Service box
d.add(Rect(200, 220, 120, 50, strokeWidth=1, strokeColor="black", fillColor=None))
d.add(String(210, 240, "Service", fontName="HeiseiMin-W3", fontSize=12))
d.add(String(210, 225, "transport_service.py", fontName="HeiseiMin-W3", fontSize=10))

# Repository box
d.add(Rect(50, 120, 120, 50, strokeWidth=1, strokeColor="black", fillColor=None))
d.add(String(60, 140, "Repository", fontName="HeiseiMin-W3", fontSize=12))
d.add(String(60, 125, "transport_repository.py", fontName="HeiseiMin-W3", fontSize=10))

# DB box
d.add(Rect(200, 120, 120, 50, strokeWidth=1, strokeColor="black", fillColor=None))
d.add(String(210, 140, "DB", fontName="HeiseiMin-W3", fontSize=12))
d.add(String(210, 125, "truck_master", fontName="HeiseiMin-W3", fontSize=10))

# 矢印
d.add(Line(170, 245, 200, 245))  # UI → Service
d.add(Line(110, 220, 110, 170))  # Service → Repository
d.add(Line(170, 145, 200, 145))  # Repository → DB

# ラベル
d.add(String(175, 255, "truck_data", fontName="HeiseiMin-W3", fontSize=8))
d.add(String(115, 195, "create_truck()", fontName="HeiseiMin-W3", fontSize=8))
d.add(String(175, 155, "INSERT", fontName="HeiseiMin-W3", fontSize=8))

story.append(d)
story.append(Spacer(1, 20))

# 補足説明
extra = """
【補足】
- UI (transport_page.py): フォーム入力（FormComponents.truck_form）と登録ボタン。
- Service (transport_service.py): create_truck() が呼ばれる。
- Repository (transport_repository.py): save_truck() がSQLを実行。
- DB (truck_master): トラック情報がINSERTされる。
"""
story.append(Paragraph(extra, styles["NormalJP"]))

# PDF生成
doc.build(story)

pdf_path_truck_flow
