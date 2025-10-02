# app/ui/layouts/sidebar.py
import streamlit as st

def create_sidebar() -> str:
    """サイドバー作成"""
    st.sidebar.title("🏭 生産計画システム")
    
    page = st.sidebar.radio(
        "メニュー",
        ["ダッシュボード", "制限設定", "生産計画", "配送便計画", "製品管理"],
        key="main_navigation"
    )
    
    # システム情報
    st.sidebar.markdown("---")
    st.sidebar.info(
        "生産計画管理システム v1.0\n\n"
        "機能:\n"
        "• 需要分析\n"
        "• 生産計画\n"
        "• 運送計画\n"
        "• 制約管理"
    )
    
    return page