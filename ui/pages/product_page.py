# app/ui/pages/product_page.py
import streamlit as st
from ui.components.forms import FormComponents

class ProductPage:
    """製品管理ページ"""

    def __init__(self, product_service):
        self.service = product_service

    def show(self):
        st.title("📦 製品管理")
        st.write("製品の登録・更新・削除を行います。")

        # 新規登録
        st.subheader("新規製品登録")
        product_data = FormComponents.product_form()
        if product_data:
            if self.service.create_product(product_data):
                st.success(f"製品 '{product_data['name']}' を登録しました")
                st.rerun()
            else:
                st.error("製品登録に失敗しました")

        # 一覧
        st.subheader("登録済み製品一覧")
        products = self.service.get_products()
        if not products:
            st.info("製品が登録されていません")
            return

        for product in products:
            with st.expander(f"📦 {product.name} (ID: {product.id})"):
                st.write(f"製品コード: {product.code}, 重量: {product.weight} kg")

                # 更新フォーム
                with st.form(f"edit_product_{product.id}"):
                    new_name = st.text_input("製品名", value=product.name)
                    new_code = st.text_input("製品コード", value=product.code)
                    new_weight = st.number_input("重量 (kg)", min_value=0, value=product.weight)
                    submitted = st.form_submit_button("更新")
                    if submitted:
                        update_data = {
                            "name": new_name,
                            "code": new_code,
                            "weight": new_weight,
                        }
                        if self.service.update_product(product.id, update_data):
                            st.success("製品を更新しました")
                            st.rerun()
                        else:
                            st.error("製品更新に失敗しました")

                # 削除
                if st.button("🗑️ 削除", key=f"delete_product_{product.id}"):
                    if self.service.delete_product(product.id):
                        st.success("製品を削除しました")
                        st.rerun()
                    else:
                        st.error("削除に失敗しました")
