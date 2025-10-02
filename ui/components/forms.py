# app/ui/components/forms.py
import streamlit as st
from typing import Callable, Any, List,Dict
import streamlit as st

class FormComponents:
    """フォームコンポーネント"""
    
    @staticmethod
    def product_constraints_form(products, existing_constraints=None):
        """製品制約フォーム"""
        constraints_data = []
        
        for product in products:
            st.write(f"**{product.product_name}** ({product.product_code})")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                daily_capacity = st.number_input(
                    "日次生産能力",
                    min_value=0,
                    value=existing_constraints.get(product.id, {}).get('daily_capacity', 1000),
                    key=f"capacity_{product.id}"
                )
            
            with col2:
                smoothing_level = st.number_input(
                    "平均化レベル",
                    min_value=0.0,
                    max_value=1.0,
                    value=existing_constraints.get(product.id, {}).get('smoothing_level', 0.7),
                    key=f"smoothing_{product.id}"
                )
            
            with col3:
                volume_per_unit = st.number_input(
                    "単位体積(m³)",
                    min_value=0.0,
                    value=existing_constraints.get(product.id, {}).get('volume_per_unit', 1.0),
                    key=f"volume_{product.id}"
                )
            
            is_transport_constrained = st.checkbox(
                "運送制限対象",
                value=existing_constraints.get(product.id, {}).get('is_transport_constrained', False),
                key=f"transport_{product.id}"
            )
            
            constraints_data.append({
                'product_id': product.id,
                'daily_capacity': daily_capacity,
                'smoothing_level': smoothing_level,
                'volume_per_unit': volume_per_unit,
                'is_transport_constrained': is_transport_constrained
            })
            
            st.divider()
        
        return constraints_data
    # app/ui/components/forms.py の一部修正

    @staticmethod
    def container_form() -> Dict[str, Any]:
        """容器登録フォーム - mm単位に変更"""
        with st.form("container_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("容器名", value="小箱")
                width = st.number_input("幅 (mm)", min_value=1, value=800)
                depth = st.number_input("奥行 (mm)", min_value=1, value=600)
            
            with col2:
                height = st.number_input("高さ (mm)", min_value=1, value=600)
                max_weight = st.number_input("最大重量 (kg)", min_value=1, value=100)
                can_mix = st.checkbox("混載可能", value=True)
            
            submitted = st.form_submit_button("容器登録")
            
            if submitted:
                return {
                    'name': name,
                    'width': width,
                    'depth': depth,
                    'height': height,
                    'max_weight': max_weight,
                    'can_mix': can_mix
                }
        
        return None
   
    @staticmethod
    def truck_form() -> Dict[str, Any]:
        """トラック登録フォーム - mm単位に変更"""
        with st.form("truck_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("トラック名", value="1便")
                width = st.number_input("荷台幅 (mm)", min_value=1, value=2100)
                depth = st.number_input("荷台奥行 (mm)", min_value=1, value=3200)
                height = st.number_input("荷台高さ (mm)", min_value=1, value=2100)
            
            with col2:
                max_weight = st.number_input("最大積載重量 (kg)", min_value=1, value=2000)
                departure_time = st.time_input("出発時刻", value=None)
                
                arrival_time = st.time_input("到着時刻", value=None)
                arrival_day_offset = st.selectbox("到着日", options=[0, 1], format_func=lambda x: "当日" if x == 0 else "翌日")
                arr_time_str = arrival_time.strftime('%H:%M:%S') if arrival_time else "12:00:00"
                default_use = st.checkbox("デフォルト便", value=False)
            
            submitted = st.form_submit_button("トラック登録")
            
            if submitted:
                # 時刻のデフォルト値処理
                dep_time = departure_time if departure_time else "08:00:00"
                arr_time = arrival_time if arrival_time else "12:00:00"
                
                return {
                    'name': name,
                    'width': width,
                    'depth': depth,
                    'height': height,
                    'max_weight': max_weight,
                    'departure_time': dep_time.strftime('%H:%M:%S') if hasattr(dep_time, 'strftime') else dep_time,
                    'arrival_time': arr_time.strftime('%H:%M:%S') if hasattr(arr_time, 'strftime') else arr_time,
                    'default_use': default_use
                }
        
        return None    
class FormComponents:
    ...
    @staticmethod
    def product_form(containers) -> Dict[str, Any]:
        """製品登録フォーム"""
        with st.form("product_form"):
            col1, col2 = st.columns(2)

            with col1:
                product_code = st.text_input("製品コード")
                product_name = st.text_input("製品名")

            with col2:
                capacity = st.number_input("入り数", min_value=1, value=1, step=1)

                container_options = {c.id: c.name for c in containers}
                used_container_id = st.selectbox(
                    "使用容器",
                    options=container_options.keys(),
                    format_func=lambda x: container_options[x] if x in container_options else "未選択"
                )

            submitted = st.form_submit_button("製品登録")

            if submitted:
                return {
                    "product_code": product_code,
                    "product_name": product_name,
                    "capacity": capacity,
                    "used_container_id": used_container_id,
                }

        return None

           