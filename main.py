# app/main.py


import streamlit as st
from repository.database_manager import DatabaseManager
from services.production_service import ProductionService
from services.transport_service import TransportService
from ui.layouts.sidebar import create_sidebar
from ui.pages.dashboard_page import DashboardPage
from ui.pages.constraints_page import ConstraintsPage
from ui.pages.production_page import ProductionPage
from ui.pages.transport_page import TransportPage
from ui.pages.product_page import ProductPage
from config import APP_CONFIG
from services.product_service import ProductService
class ProductionPlanningApp:
    """生産計画アプリケーション - メイン制御クラス"""
    
    def __init__(self):
        # データベース接続
        self.db = DatabaseManager()
        
        # サービス層初期化
        self.production_service = ProductionService(self.db)
        self.transport_service = TransportService(self.db)
        self.product_service = ProductService(self.db)
        
        # ページ初期化
        self.pages = {
            "ダッシュボード": DashboardPage(self.production_service),
            "制限設定": ConstraintsPage(self.production_service),
            "生産計画": ProductionPage(self.production_service),
            "配送便計画": TransportPage(self.transport_service),
            "製品管理": ProductPage(self.product_service)
        }
    
    def run(self):
        """アプリケーション実行"""
        # ページ設定
        st.set_page_config(
            page_title=APP_CONFIG.page_title,
            page_icon=APP_CONFIG.page_icon,
            layout=APP_CONFIG.layout
        )
        
        # サイドバー表示
        selected_page = create_sidebar()
        
        # 選択されたページを表示
        if selected_page in self.pages:
            try:
                self.pages[selected_page].show()
            except Exception as e:
                st.error(f"ページ表示エラー: {e}")
                st.info("データベース接続を確認してください")
        else:
            st.error("選択されたページが見つかりません")
    
    def __del__(self):
        """リソース解放"""
        if hasattr(self, 'db'):
            self.db.close()

def main():
    """メイン関数"""
    try:
        app = ProductionPlanningApp()
        app.run()
    except Exception as e:
        st.error(f"アプリケーション起動エラー: {e}")
        st.info("設定ファイルとデータベース接続を確認してください")

if __name__ == "__main__":
    main()