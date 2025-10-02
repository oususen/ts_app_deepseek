from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from typing import Optional, List, Dict, Any

from .database_manager import DatabaseManager
from domain.models.product import Product
from domain.models.production import ProductionConstraint


class ProductRepository:
    """製品関連データアクセス"""

    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def get_all_products(self) -> pd.DataFrame:
        """全製品取得"""
        session = self.db.get_session()
        try:
            products = session.query(Product).order_by(Product.product_code).all()
            return pd.DataFrame([{
                "id": p.id,
                "data_no": p.data_no,
                "factory": p.factory,
                "product_code": p.product_code,
                "product_name": p.product_name,
                "inspection_category": p.inspection_category or "",
                "container_width": float(p.container_width or 0.0),
                "container_depth": float(p.container_depth or 0.0),
                "container_height": float(p.container_height or 0.0),
                "stackable": bool(p.stackable) if p.stackable is not None else False
            } for p in products if p is not None])
        except SQLAlchemyError as e:
            print(f"製品取得エラー: {e}")
            return pd.DataFrame()
        finally:
            session.close()

    def get_product_constraints(self) -> pd.DataFrame:
        """製品制約取得"""
        session = self.db.get_session()
        try:
            constraints = (
                session.query(ProductionConstraint, Product)
                .join(Product, ProductionConstraint.product_id == Product.id, isouter=True)
                .order_by(Product.product_code)
                .all()
            )
            return pd.DataFrame([{
                "id": c.id,
                "product_id": c.product_id,
                "daily_capacity": int(c.daily_capacity or 0),
                "smoothing_level": float(c.smoothing_level or 0.0),
                "volume_per_unit": float(c.volume_per_unit or 0.0),
                "is_transport_constrained": bool(c.is_transport_constrained),
                "product_code": p.product_code if p else "",
                "product_name": p.product_name if p else "",
                "inspection_category": p.inspection_category if p else ""
            } for c, p in constraints if c is not None])
        except SQLAlchemyError as e:
            print(f"製品制約取得エラー: {e}")
            return pd.DataFrame()
        finally:
            session.close()

    def save_product_constraints(self, constraints_df: pd.DataFrame) -> bool:
        """製品制約保存（全削除 → 一括挿入）"""
        session = self.db.get_session()
        try:
            session.query(ProductionConstraint).delete()
            for _, row in constraints_df.iterrows():
                constraint = ProductionConstraint(
                    product_id=int(row.get("product_id", 0)),
                    daily_capacity=int(row.get("daily_capacity", 0)),
                    smoothing_level=float(row.get("smoothing_level", 0.0)),
                    volume_per_unit=float(row.get("volume_per_unit", 0.0)),
                    is_transport_constrained=bool(row.get("is_transport_constrained", False))
                )
                session.add(constraint)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"製品制約保存エラー: {e}")
            return False
        finally:
            session.close()

    def create_product(self, product_data: dict) -> bool:
        """製品を新規登録"""
        session = self.db.get_session()
        try:
            product = Product(
                data_no=product_data.get("data_no"),
                factory=product_data.get("factory"),
                product_code=product_data.get("product_code"),
                product_name=product_data.get("product_name"),
                inspection_category=product_data.get("inspection_category", "A"),
                container_width=float(product_data.get("container_width") or 0.0),
                container_depth=float(product_data.get("container_depth") or 0.0),
                container_height=float(product_data.get("container_height") or 0.0),
                stackable=bool(product_data.get("stackable", False))
            )
            session.add(product)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"製品登録エラー: {e}")
            return False
        finally:
            session.close()
