from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

# 日本語フォントを登録
pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))

# 出力ファイルパス
pdf_path_full = "ts_app_deepseek_structure_complete.pdf"

# PDF準備
doc = SimpleDocTemplate(pdf_path_full, pagesize=A4)
styles = getSampleStyleSheet()

# 日本語スタイル
styles.add(ParagraphStyle(name="NormalJP", fontName="HeiseiMin-W3", fontSize=13, leading=16))
styles.add(ParagraphStyle(name="TitleJP", fontName="HeiseiMin-W3", fontSize=18, leading=22))
styles.add(ParagraphStyle(name="CodeJP", fontName="HeiseiMin-W3", fontSize=12, leading=14))

story = []

# タイトル
story.append(Paragraph("ts_app_deepseek プロジェクト構成（完全版 日本語訳）", styles["TitleJP"]))
story.append(Spacer(1, 16))

# 構成テキスト（ui/pages を含む完全版）
structure_text = """
ts_app_deepseek/
├── config.py                → 設定ファイル
├── main.py                  → メイン（アプリのエントリーポイント）
├── __init__.py              → パッケージ初期化ファイル
├── domain/                  → ドメイン層（業務ロジックの中心）
│   ├── calculators/         → 計算ロジック
│   │   ├── production_calculator.py → 生産計算モジュール
│   │   └── transport_planner.py     → 輸送計画モジュール
│   ├── models/              → データモデル
│   │   ├── product.py       → 製品モデル
│   │   ├── production.py    → 生産モデル
│   │   └── transport.py     → 輸送モデル
│   └── validators/          → バリデーション（入力検証）
│       └── loading_validator.py     → 積載検証モジュール
├── repository/              → リポジトリ層（データアクセス）
│   ├── database_manager.py  → データベース管理
│   ├── product_repository.py → 製品リポジトリ
│   ├── production_repository.py → 生産リポジトリ
│   └── transport_repository.py  → 輸送リポジトリ
├── services/                → サービス層（業務サービス）
│   ├── production_service.py → 生産サービス
│   └── transport_service.py  → 輸送サービス
└── ui/                      → ユーザーインターフェース
    ├── components/          → UIコンポーネント
    │   ├── charts.py        → グラフ描画
    │   ├── forms.py         → 入力フォーム
    │   └── tables.py        → 表（テーブル）
    ├── layouts/             → レイアウト
    │   └── sidebar.py       → サイドバー
    └── pages/               → ページ画面
        ├── constraints_page.py → 制約条件ページ
        ├── dashboard_page.py   → ダッシュボードページ
        ├── production_page.py  → 生産計画ページ
        └── transport_page.py   → トラック管理・積載計画ページ
"""

story.append(Preformatted(structure_text, styles["CodeJP"]))

# 補足説明
extra_text = """
【補足】
- domain はアプリの業務知識・計算ロジックをまとめた層
- repository はデータベースやストレージとやり取りする層
- services はドメインの処理を組み合わせて提供するサービス層
- ui/components は入力フォームや表などの共通部品
- ui/pages は画面単位のページ（例：dashboard_page, transport_page）
- ui/layouts は画面レイアウト（サイドバーなど）

いわゆる DDD（ドメイン駆動設計）＋フロントエンドのUI構造を合わせたアーキテクチャになっています。
"""

story.append(Spacer(1, 16))
story.append(Paragraph(extra_text, styles["NormalJP"]))

# PDF生成
doc.build(story)

pdf_path_full
