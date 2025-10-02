# app/domain/models/transport.py
from typing import List, Optional
import pandas as pd
from datetime import time
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Time, Float 
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()


from sqlalchemy import Column, Integer, String, Float, Boolean, TIMESTAMP, Computed

class Container(Base):
    __tablename__ = "container_capacity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    width = Column(Integer, nullable=False)   # mm
    depth = Column(Integer, nullable=False)   # mm
    height = Column(Integer, nullable=False)  # mm
    max_weight = Column(Integer, nullable=False, default=0)
    max_volume = Column(Float, Computed("((width * depth * height) / 1000000000.0)", persisted=True))
    can_mix = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, nullable=True, server_default="CURRENT_TIMESTAMP")

    def __repr__(self):
        return f"<Container(id={self.id}, name='{self.name}', size={self.width}x{self.depth}x{self.height}, max_weight={self.max_weight}, max_volume={self.max_volume}, can_mix={self.can_mix})>"


class Truck(Base):
    """トラックモデル - SQLAlchemy ORM"""
    __tablename__ = "truck_master"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    width = Column(Integer, nullable=False)
    depth = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    max_weight = Column(Integer, default=10000)
    departure_time = Column(Time, nullable=False)
    arrival_time = Column(Time, nullable=False)
    default_use = Column(Boolean, default=False)
    arrival_day_offset = Column(Integer, default=0)

    def __repr__(self):
        return f"<Truck(id={self.id}, name='{self.name}', departure={self.departure_time}, arrival={self.arrival_time}, offset={self.arrival_day_offset})>"

class TruckContainerRule:
    """トラックと容器の紐付けルール"""
    
    def __init__(self, id: int, truck_id: int, container_id: int, 
                 max_quantity: Optional[int] = None, priority: int = 0,
                 truck_name: Optional[str] = None, container_name: Optional[str] = None):
        self.id = id
        self.truck_id = truck_id
        self.container_id = container_id
        self.max_quantity = max_quantity
        self.priority = priority
        self.truck_name = truck_name
        self.container_name = container_name
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        return cls(
            id=data.get('id'),
            truck_id=data.get('truck_id'),
            container_id=data.get('container_id'),
            max_quantity=data.get('max_quantity'),
            priority=data.get('priority', 0),
            truck_name=data.get('truck_name'),
            container_name=data.get('container_name')
        )

# 他のクラスは変更なし
class LoadingItem:
    """積載アイテム"""
    
    def __init__(self, product_id: int, container_id: int, quantity: int, weight_per_unit: float):
        self.product_id = product_id
        self.container_id = container_id
        self.quantity = quantity
        self.weight_per_unit = weight_per_unit
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        return cls(
            product_id=data.get('product_id'),
            container_id=data.get('container_id'),
            quantity=data.get('quantity'),
            weight_per_unit=data.get('weight_per_unit')
        )

class TransportPlan:
    """運送計画モデル"""
    
    def __init__(self, truck: Truck, loaded_items: List[LoadingItem], total_volume: float,
                 total_weight: float, volume_utilization: float, weight_utilization: float):
        self.truck = truck
        self.loaded_items = loaded_items
        self.total_volume = total_volume
        self.total_weight = total_weight
        self.volume_utilization = volume_utilization
        self.weight_utilization = weight_utilization
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        return cls(
            truck=data.get('truck'),
            loaded_items=data.get('loaded_items', []),
            total_volume=data.get('total_volume'),
            total_weight=data.get('total_weight'),
            volume_utilization=data.get('volume_utilization'),
            weight_utilization=data.get('weight_utilization')
        )
class TransportConstraint:
    """運送制約モデル"""
    def __init__(self, id: int, product_id: int, container_id: int, max_quantity: Optional[int] = None):
        self.id = id  
        self.product_id = product_id
        self.container_id = container_id  
        self.max_quantity = max_quantity
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        return cls(
            id=data.get('id'),
            product_id=data.get('product_id'),
            container_id=data.get('container_id'),
            max_quantity=data.get('max_quantity')
        )
    def __repr__(self):
        return f"<TransportConstraint(id={self.id}, product_id={self.product_id}, container_id={self.container_id}, max_quantity={self.max_quantity})>"
    def to_dict(self):
        """辞書に変換"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "container_id": self.container_id,
            "max_quantity": self.max_quantity
        }
    @staticmethod
    def to_dataframe(constraints: List['TransportConstraint']) -> pd.DataFrame:
        """TransportConstraintのリストをDataFrameに変換"""
        data = [constraint.to_dict() for constraint in constraints]
        return pd.DataFrame(data)
    @staticmethod
    def from_dataframe(df: pd.DataFrame) -> List['TransportConstraint']:
        """DataFrameからTransportConstraintのリストを作成"""
        constraints = []
        for _, row in df.iterrows():
            constraint = TransportConstraint.from_dict(row.to_dict())
            constraints.append(constraint)
        return constraints
    def __eq__(self, other):
        if not isinstance(other, TransportConstraint):
            return False
        return (self.product_id == other.product_id and
                self.container_id == other.container_id and
                self.max_quantity == other.max_quantity)
    def __hash__(self):
        return hash((self.product_id, self.container_id, self.max_quantity))
# 他のクラスは変更なし
class ProductConstraint:
    """製品制約モデル"""
    
    def __init__(self, id: int, product_id: int, min_lot_size: Optional[int] = None, 
                 max_lot_size: Optional[int] = None, lead_time_days: Optional[int] = None):
        self.id = id
        self.product_id = product_id
        self.min_lot_size = min_lot_size
        self.max_lot_size = max_lot_size
        self.lead_time_days = lead_time_days
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        return cls(
            id=data.get('id'),
            product_id=data.get('product_id'),
            min_lot_size=data.get('min_lot_size'),
            max_lot_size=data.get('max_lot_size'),
            lead_time_days=data.get('lead_time_days')
        )
class ProductionInstruction:
    """生産指示モデル"""
    
    def __init__(self, id: int, product_id: int, scheduled_date: str, quantity: int, 
                 inspection_category: str, product_name: Optional[str] = None):
        self.id = id
        self.product_id = product_id
        self.scheduled_date = scheduled_date
        self.quantity = quantity
        self.inspection_category = inspection_category
        self.product_name = product_name
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        return cls(
            id=data.get('id'),
            product_id=data.get('product_id'),
            scheduled_date=data.get('scheduled_date'),
            quantity=data.get('quantity'),
            inspection_category=data.get('inspection_category'),
            product_name=data.get('product_name')
        )
class ProductionPlan:
    """生産計画モデル"""
    
    def __init__(self, product_id: int, scheduled_date: str, quantity: int, 
                 inspection_category: str, is_constrained: bool = False, product_name: Optional[str] = None):
        self.product_id = product_id
        self.scheduled_date = scheduled_date
        self.quantity = quantity
        self.inspection_category = inspection_category
        self.is_constrained = is_constrained
        self.product_name = product_name
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        return cls(
            product_id=data.get('product_id'),
            scheduled_date=data.get('scheduled_date'),
            quantity=data.get('quantity'),
            inspection_category=data.get('inspection_category'),
            is_constrained=bool(data.get('is_constrained', False)),
            product_name=data.get('product_name')
        )
# 他のクラスは変更なし

