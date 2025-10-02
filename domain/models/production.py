# app/domain/models/production.py
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, List
from domain.models.transport import Truck, Container, TruckContainerRule, TransportConstraint, LoadingItem, TransportPlan
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from repository.database_manager import DatabaseManager
from repository.production_repository import ProductionRepository
from repository.transport_repository import TransportRepository
import streamlit as st
from domain.models.product import Product
@dataclass
class ProductionInstruction:
    """生産指示モデル - production_instructions_detailテーブル構造に合わせる"""
    id: int
    product_id: Optional[int] = None
    record_type: Optional[str] = None
    start_month: Optional[str] = None
    total_first_month: Optional[int] = None
    total_next_month: Optional[int] = None
    total_next_next_month: Optional[int] = None
    instruction_date: Optional[date] = None
    instruction_quantity: Optional[int] = None
    inspection_category: Optional[str] = None
    month_type: Optional[str] = None
    day_number: Optional[int] = None
    created_at: Optional[str] = None
    # 結合用フィールド
    product_code: Optional[str] = None
    product_name: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        valid_fields = {}
        for field_name, field_type in cls.__annotations__.items():
            if field_name in data and data[field_name] is not None:
                valid_fields[field_name] = data[field_name]
        return cls(**valid_fields)

@dataclass
class ProductionPlan:
    """生産計画モデル"""
    date: date
    product_id: int
    product_code: str
    product_name: str
    demand_quantity: float
    planned_quantity: float
    inspection_category: str
    is_constrained: bool
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        valid_fields = {}
        for field_name, field_type in cls.__annotations__.items():
            if field_name in data and data[field_name] is not None:
                valid_fields[field_name] = data[field_name]
        return cls(**valid_fields)
@dataclass
class ProductConstraint:    
    """製品制約モデル - products_constraintsテーブル構造に合わせる"""
    id: int
    product_id: Optional[int] = None
    min_lot_size: Optional[int] = None
    max_lot_size: Optional[int] = None
    lead_time_days: Optional[int] = None
    created_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        valid_fields = {}
        for field_name, field_type in cls.__annotations__.items():
            if field_name in data and data[field_name] is not None:
                valid_fields[field_name] = data[field_name]
        return cls(**valid_fields)
@dataclass
class ProductionConstraint:
    """生産制約モデル - production_constraintsテーブル構造に合わせる"""
    id: int
    product_id: Optional[int] = None
    daily_capacity: Optional[int] = None
    smoothing_level: Optional[float] = None
    volume_per_unit: Optional[float] = None
    is_transport_constrained: Optional[bool] = None
    created_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        valid_fields = {}
        for field_name, field_type in cls.__annotations__.items():
            if field_name in data and data[field_name] is not None:
                valid_fields[field_name] = data[field_name]
        return cls(**valid_fields)
    def __eq__(self, other):
        if not isinstance(other, ProductionConstraint):
            return False
        return (self.product_id == other.product_id and
                self.daily_capacity == other.daily_capacity and
                self.smoothing_level == other.smoothing_level and
                self.volume_per_unit == other.volume_per_unit and
                self.is_transport_constrained == other.is_transport_constrained)
    def __hash__(self):
        return hash((self.product_id, self.daily_capacity, self.smoothing_level,
                     self.volume_per_unit, self.is_transport_constrained))
@dataclass
class TransportConstraint:
    """輸送制約モデル - transport_constraintsテーブル構造に合わせる"""
    id: int
    product_id: Optional[int] = None
    container_id: Optional[int] = None
    max_quantity: Optional[int] = None
    created_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        valid_fields = {}
        for field_name, field_type in cls.__annotations__.items():
            if field_name in data and data[field_name] is not None:
                valid_fields[field_name] = data[field_name]
        return cls(**valid_fields)
    def __eq__(self, other):
        if not isinstance(other, TransportConstraint):
            return False
        return (self.product_id == other.product_id and
                self.container_id == other.container_id and
                self.max_quantity == other.max_quantity)    
    def __hash__(self):
        return hash((self.product_id, self.container_id, self.max_quantity))
@dataclass
class Container:
    """容器モデル - containersテーブル構造に合わせる"""
    id: int
    container_code: Optional[str] = None
    container_name: Optional[str] = None
    width: Optional[float] = None
    depth: Optional[float] = None
    height: Optional[float] = None
    max_stack: Optional[int] = None
    created_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        valid_fields = {}
        for field_name, field_type in cls.__annotations__.items():
            if field_name in data and data[field_name] is not None:
                valid_fields[field_name] = data[field_name]
        return cls(**valid_fields)
    def __eq__(self, other):
        if not isinstance(other, Container):
            return False
        return (self.container_code == other.container_code and
                self.container_name == other.container_name and
                self.width == other.width and
                self.depth == other.depth and
                self.height == other.height and
                self.max_stack == other.max_stack)
    def __hash__(self):
        return hash((self.container_code, self.container_name, self.width,
                     self.depth, self.height, self.max_stack))
@dataclass
class Truck:
    """トラックモデル - trucksテーブル構造に合わせる"""
    id: int
    truck_code: Optional[str] = None
    truck_name: Optional[str] = None
    max_load_volume: Optional[float] = None
    max_load_weight: Optional[float] = None
    created_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        valid_fields = {}
        for field_name, field_type in cls.__annotations__.items():
            if field_name in data and data[field_name] is not None:
                valid_fields[field_name] = data[field_name]
        return cls(**valid_fields)
    def __eq__(self, other):
        if not isinstance(other, Truck):
            return False
        return (self.truck_code == other.truck_code and
                self.truck_name == other.truck_name and
                self.max_load_volume == other.max_load_volume and
                self.max_load_weight == other.max_load_weight)
    def __hash__(self):
        return hash((self.truck_code, self.truck_name,
                     self.max_load_volume, self.max_load_weight))
@dataclass
class TruckContainerRule:
    """トラックと容器の紐付けルールモデル - truck_container_rulesテーブル構造に合わせる"""
    id: int
    truck_id: Optional[int] = None
    container_id: Optional[int] = None
    max_quantity: Optional[int] = None
    priority: Optional[int] = None
    created_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        valid_fields = {}
        for field_name, field_type in cls.__annotations__.items():
            if field_name in data and data[field_name] is not None:
                valid_fields[field_name] = data[field_name]
        return cls(**valid_fields)
    def __eq__(self, other):
        if not isinstance(other, TruckContainerRule):
            return False
        return (self.truck_id == other.truck_id and
                self.container_id == other.container_id and
                self.max_quantity == other.max_quantity and
                self.priority == other.priority)
    def __hash__(self):
        return hash((self.truck_id, self.container_id, self.max_quantity, self.priority))
@dataclass
class TransportConstraint:
    """輸送制約モデル - transport_constraintsテーブル構造に合わせる"""
    id: int
    product_id: Optional[int] = None
    container_id: Optional[int] = None
    max_quantity: Optional[int] = None
    created_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        valid_fields = {}
        for field_name, field_type in cls.__annotations__.items():
            if field_name in data and data[field_name] is not None:
                valid_fields[field_name] = data[field_name]
        return cls(**valid_fields)
    def __eq__(self, other):
        if not isinstance(other, TransportConstraint):
            return False
        return (self.product_id == other.product_id and
                self.container_id == other.container_id and
                self.max_quantity == other.max_quantity)    
    def __hash__(self):
        return hash((self.product_id, self.container_id, self.max_quantity))
@dataclass
class LoadingPlan:
    """積載計画モデル"""
    truck_id: int
    container_id: int
    product_id: int
    quantity: int
    total_volume: float
    total_weight: float
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        valid_fields = {}
        for field_name, field_type in cls.__annotations__.items():
            if field_name in data and data[field_name] is not None:
                valid_fields[field_name] = data[field_name]
        return cls(**valid_fields)
@dataclass
class LoadingResult:
    """積載結果モデル"""
    truck_id: int
    container_id: int
    product_id: int
    quantity: int
    total_volume: float
    total_weight: float
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        valid_fields = {}
        for field_name, field_type in cls.__annotations__.items():
            if field_name in data and data[field_name] is not None:
                valid_fields[field_name] = data[field_name]
        return cls(**valid_fields)
@dataclass
class LoadingSummary:
    """積載集計モデル"""
    truck_id: int
    total_volume: float
    total_weight: float
    volume_utilization: float
    weight_utilization: float
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        valid_fields = {}
        for field_name, field_type in cls.__annotations__.items():
            if field_name in data and data[field_name] is not None:
                valid_fields[field_name] = data[field_name]
        return cls(**valid_fields)
@dataclass
class TruckLoadingPlan:
    """トラック積載計画モデル"""
    truck: Truck
    loading_plans: list[LoadingPlan]
    total_volume: float
    total_weight: float
    volume_utilization: float
    weight_utilization: float
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        valid_fields = {}
        for field_name, field_type in cls.__annotations__.items():
            if field_name in data and data[field_name] is not None:
                valid_fields[field_name] = data[field_name]
        return cls(**valid_fields)



