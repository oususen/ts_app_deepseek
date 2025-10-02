# app/ui/pages/transport_page.py
import streamlit as st
import pandas as pd
from ui.components.forms import FormComponents
from ui.components.tables import TableComponents

class TransportPage:
    """配送便計画ページ - トラック積載計画の作成画面"""
    
    def __init__(self, transport_service):
        self.service = transport_service
        self.tables = TableComponents()
    
    def show(self):
        """ページ表示"""
        st.title("🚚 配送便計画")
        st.write("トラックの積載計画と容器・車両管理を行います。")
        
        tab1, tab2, tab3 = st.tabs(["📦 積載計画", "🧰 容器管理", "🚛 トラック管理"])
        
        with tab1:
            self._show_loading_planning()
        with tab2:
            self._show_container_management()
        with tab3:
            self._show_truck_management()
    
    def _show_loading_planning(self):
        """積載計画表示"""
        st.header("📦 積載計画作成")
        st.write("製品と容器を選択してトラック積載計画を作成します。")
        
        try:
            containers = self.service.get_containers()
            trucks = self.service.get_trucks()
            
            if not containers or not trucks:
                st.warning("容器またはトラックデータがありません。まず管理画面で登録してください。")
                return
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("積載アイテム設定")
                
                # サンプルアイテム（実際は製品から選択）
                st.write("**積載アイテム**（サンプルデータ）")
                
                sample_items = [
                    {'product_id': 1, 'container_id': 1, 'quantity': 10, 'weight_per_unit': 5.0},
                    {'product_id': 2, 'container_id': 2, 'quantity': 5, 'weight_per_unit': 8.0},
                    {'product_id': 3, 'container_id': 1, 'quantity': 8, 'weight_per_unit': 6.0},
                ]
                
                items_df = pd.DataFrame(sample_items)
                st.dataframe(items_df, use_container_width=True)
                
                # トラック選択
                st.subheader("トラック選択")
                truck_options = {f"{truck.name} ({truck.width}x{truck.depth}x{truck.height}cm)": truck.id for truck in trucks}
                selected_truck_name = st.selectbox("トラックを選択", options=list(truck_options.keys()))
                selected_truck_id = truck_options[selected_truck_name]
            
            with col2:
                st.subheader("積載計画")
                
                if st.button("🔄 積載計画計算", type="primary"):
                    with st.spinner("積載計画を計算中..."):
                        plan_result = self.service.calculate_delivery_plan(sample_items)
                        self.tables.display_loading_plan(plan_result)
                
                # 積載バリデーション
                st.subheader("積載チェック")
                if st.button("✅ 積載可否チェック"):
                    is_valid, errors = self.service.validate_loading(sample_items, selected_truck_id)
                    if is_valid:
                        st.success("✅ 積載可能です")
                    else:
                        st.error("❌ 積載不可:")
                        for error in errors:
                            st.write(f"• {error}")
        
        except Exception as e:
            st.error(f"積載計画エラー: {e}")
    def _show_container_management(self):
        """容器管理表示"""
        st.header("🧰 容器管理")
        st.write("積載に使用する容器の登録と管理を行います。")

        try:
            # 新規容器登録
            st.subheader("新規容器登録")
            container_data = FormComponents.container_form()

            if container_data:
                success = self.service.create_container(container_data)
                if success:
                    st.success(f"容器 '{container_data['name']}' を登録しました")
                    st.rerun()
                else:
                    st.error("容器登録に失敗しました")

            # 容器一覧表示
            st.subheader("登録済み容器一覧")
            containers = self.service.get_containers()

            if containers:
                for container in containers:
                    with st.expander(f"📦 {container.name} (ID: {container.id})"):
                        st.write(f"寸法: {container.width} × {container.depth} × {container.height} cm")
                        st.write(f"体積: {(container.width * container.depth * container.height) / 1000000:.3f} m³")
                        st.write(f"最大重量: {container.max_weight} kg")

                        # --- 更新フォーム ---
                        with st.form(f"edit_container_form_{container.id}"):
                            st.write("✏️ 容器情報を編集")

                            new_name = st.text_input("容器名", value=container.name)
                            new_width = st.number_input("幅 (cm)", min_value=1, value=container.width)
                            new_depth = st.number_input("奥行 (cm)", min_value=1, value=container.depth)
                            new_height = st.number_input("高さ (cm)", min_value=1, value=container.height)
                            new_weight = st.number_input("最大重量 (kg)", min_value=1, value=container.max_weight)

                            submitted = st.form_submit_button("更新")
                            if submitted:
                                update_data = {
                                    "name": new_name,
                                    "width": new_width,
                                    "depth": new_depth,
                                    "height": new_height,
                                    "max_weight": new_weight,
                                }
                                success = self.service.update_container(container.id, update_data)
                                if success:
                                    st.success(f"✅ 容器 '{container.name}' を更新しました")
                                    st.rerun()
                                else:
                                    st.error("❌ 容器更新に失敗しました")

                        # --- 削除ボタン ---
                        if st.button("🗑️ 削除", key=f"delete_container_{container.id}"):
                            success = self.service.delete_container(container.id)
                            if success:
                                st.success(f"容器 '{container.name}' を削除しました")
                                st.rerun()
                            else:
                                st.error("容器削除に失敗しました")

                # 統計
                st.subheader("容器統計")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("登録容器数", len(containers))
                with col2:
                    avg_volume = sum((c.width * c.depth * c.height) for c in containers) / len(containers) / 1000000
                    st.metric("平均体積", f"{avg_volume:.2f} m³")
                with col3:
                    avg_weight = sum(c.max_weight for c in containers) / len(containers)
                    st.metric("平均最大重量", f"{avg_weight:.1f} kg")

            else:
                st.info("登録されている容器がありません")

        except Exception as e:
            st.error(f"容器管理エラー: {e}")
    
     

    def _show_truck_management(self):
        """トラック管理表示"""
        st.header("🚛 トラック管理")
        st.write("積載に使用するトラックの登録と管理を行います。")

        try:
            # 新規トラック登録
            st.subheader("新規トラック登録")
            truck_data = FormComponents.truck_form()

            if truck_data:
                success = self.service.create_truck(truck_data)
                if success:
                    st.success(f"トラック '{truck_data['name']}' を登録しました")
                    st.rerun()
                else:
                    st.error("トラック登録に失敗しました")

            # トラック一覧表示
            st.subheader("登録済みトラック一覧")
            trucks_df = self.service.get_trucks()

            if not trucks_df.empty:
                for _, truck in trucks_df.iterrows():
                    with st.expander(f"🛻 {truck['name']} (ID: {truck['id']})"):
                        st.write(f"荷台寸法: {truck['width']} × {truck['depth']} × {truck['height']} mm")
                        st.write(f"最大積載重量: {truck['max_weight']} kg")
                        st.write(f"出発時刻: {truck['departure_time']}")
                        st.write(f"到着時刻: {truck['arrival_time']} (+{truck['arrival_day_offset']}日)")
                        st.write(f"デフォルト便: {'✅' if truck['default_use'] else '❌'}")

                        # --- 更新フォーム ---
                        with st.form(f"edit_truck_form_{truck['id']}"):
                            st.write("✏️ トラック情報を編集")

                            new_name = st.text_input("トラック名", value=truck['name'])
                            new_width = st.number_input("荷台幅 (mm)", min_value=1, value=int(truck['width']))
                            new_depth = st.number_input("荷台奥行 (mm)", min_value=1, value=int(truck['depth']))
                            new_height = st.number_input("荷台高さ (mm)", min_value=1, value=int(truck['height']))
                            new_weight = st.number_input("最大積載重量 (kg)", min_value=1, value=int(truck['max_weight']))
                            new_dep = st.time_input("出発時刻", value=truck['departure_time'])
                            new_arr = st.time_input("到着時刻", value=truck['arrival_time'])
                            new_offset = st.number_input("到着日オフセット（日）", min_value=0, max_value=7, value=int(truck['arrival_day_offset']))
                            new_default = st.checkbox("デフォルト便", value=bool(truck['default_use']))

                            submitted = st.form_submit_button("更新")
                            if submitted:
                                update_data = {
                                    "name": new_name,
                                    "width": new_width,
                                    "depth": new_depth,
                                    "height": new_height,
                                    "max_weight": new_weight,
                                    "departure_time": new_dep,
                                    "arrival_time": new_arr,
                                    "arrival_day_offset": new_offset,
                                    "default_use": new_default,
                                }
                                success = self.service.update_truck(truck['id'], update_data)
                                if success:
                                    st.success(f"✅ トラック '{truck['name']}' を更新しました")
                                    st.rerun()
                                else:
                                    st.error("❌ トラック更新に失敗しました")

                        # --- 削除ボタン ---
                        if st.button("🗑️ 削除", key=f"delete_truck_{truck['id']}"):
                            success = self.service.delete_truck(truck['id'])
                            if success:
                                st.success(f"トラック '{truck['name']}' を削除しました")
                                st.rerun()
                            else:
                                st.error("トラック削除に失敗しました")

            else:
                st.info("登録されているトラックがありません")

        except Exception as e:
            st.error(f"トラック管理エラー: {e}")

          
