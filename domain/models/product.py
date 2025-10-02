from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from sqlalchemy.orm import declarative_base
from domain.models.transport import Container

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_code = Column(String(20), nullable=False)
    product_name = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=True)  # 入り数

    # 容器へのFK (専用/汎用どちらを使うか)
    used_container_id = Column(Integer, ForeignKey("container_capacity.id"), nullable=True)

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    # リレーション: Container 側に backref
    used_container = relationship("Container", backref="products")

    def __repr__(self):
        return (
            f"<Product(id={self.id}, code={self.product_code}, "
            f"name={self.product_name}, capacity={self.capacity}, "
            f"used_container_id={self.used_container_id})>"
        )


class ProductConstraint(Base):
    __tablename__ = "production_constraints"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    daily_capacity = Column(Integer, default=1000)
    smoothing_level = Column(Integer, default=70)  # %で持たせるかfloatで0.7持つか設計次第
    volume_per_unit = Column(Integer, default=1)
    is_transport_constrained = Column(Boolean, default=False)

    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    # リレーション
    product = relationship("Product", backref="constraints")

    def __repr__(self):
        return (
            f"<ProductConstraint(id={self.id}, product_id={self.product_id}, "
            f"daily_capacity={self.daily_capacity}, smoothing_level={self.smoothing_level}, "
            f"volume_per_unit={self.volume_per_unit}, is_transport_constrained={self.is_transport_constrained})>"
        )
