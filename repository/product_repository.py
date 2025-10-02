from sqlalchemy.exc import SQLAlchemyError
import pandas as pd

from .database_manager import DatabaseManager
from domain.models.product import Product, ProductConstraint


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
                "product_code": p.product_code,
                "product_name": p.product_name,
                "capacity": p.capacity,
                "used_container_id": p.used_container_id,
                "container_name": p.used_container.name if p.used_container else None,
                "created_at": p.created_at
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
                session.query(ProductConstraint, Product)
                .join(Product, ProductConstraint.product_id == Product.id, isouter=True)
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
                "product_name": p.product_name if p else ""
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
            session.query(ProductConstraint).delete()
            for _, row in constraints_df.iterrows():
                constraint = ProductConstraint(
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
                product_code=product_data.get("product_code"),
                product_name=product_data.get("product_name"),
                capacity=product_data.get("capacity"),
                used_container_id=product_data.get("used_container_id"),
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

    def update_product(self, product_id: int, update_data: dict) -> bool:
        """製品を更新"""
        session = self.db.get_session()
        try:
            product = session.query(Product).get(product_id)
            if not product:
                return False
            for key, value in update_data.items():
                setattr(product, key, value)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"製品更新エラー: {e}")
            return False
        finally:
            session.close()

    def delete_product(self, product_id: int) -> bool:
        """製品を削除"""
        session = self.db.get_session()
        try:
            product = session.query(Product).get(product_id)
            if not product:
                return False
            session.delete(product)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"製品削除エラー: {e}")
            return False
        finally:
            session.close()
