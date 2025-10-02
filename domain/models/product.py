# app/domain/models/product.py
from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Product:
    """製品モデル - 実際のproductsテーブル構造に合わせる"""
    id: int
    data_no: Optional[int] = None
    factory: Optional[str] = None
    client_code: Optional[int] = None
    calculation_date: Optional[date] = None
    production_complete_date: Optional[date] = None
    modified_factory: Optional[str] = None
    product_category: Optional[str] = None
    product_code: Optional[str] = None
    ac_code: Optional[str] = None
    processing_content: Optional[str] = None
    product_name: Optional[str] = None
    delivery_location: Optional[str] = None
    box_type: Optional[str] = None
    capacity: Optional[int] = None
    grouping_category: Optional[str] = None
    form_category: Optional[str] = None
    inspection_category: Optional[str] = None
    ordering_category: Optional[str] = None
    regular_replenishment_category: Optional[str] = None
    lead_time: Optional[int] = None
    fixed_point_days: Optional[int] = None
    shipping_factory: Optional[str] = None
    client_product_code: Optional[str] = None
    purchasing_org: Optional[str] = None
    item_group: Optional[str] = None
    processing_type: Optional[str] = None
    inventory_transfer_category: Optional[str] = None
    container_width: Optional[int] = None
    container_depth: Optional[int] = None
    container_height: Optional[int] = None
    stackable: Optional[bool] = True
    created_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成（余分なキーを無視）"""
        valid_fields = {}
        for field_name, field_type in cls.__annotations__.items():
            if field_name in data and data[field_name] is not None:
                valid_fields[field_name] = data[field_name]
        return cls(**valid_fields)

@dataclass
class ProductConstraint:
    """製品制約モデル - production_constraintsテーブル構造に合わせる"""
    
    product_id: int
    id: Optional[int] = None  # デフォルト値ありの引数を後に
    daily_capacity: int = 1000
    smoothing_level: float = 0.70
    volume_per_unit: float = 1.00
    is_transport_constrained: bool = False
    created_at: Optional[str] = None# app/domain/models/product.py
from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class Product:
    """製品モデル - 実際のproductsテーブル構造に合わせる"""
    id: int
    data_no: Optional[int] = None
    factory: Optional[str] = None
    client_code: Optional[int] = None
    calculation_date: Optional[date] = None
    production_complete_date: Optional[date] = None
    modified_factory: Optional[str] = None
    product_category: Optional[str] = None
    product_code: Optional[str] = None
    ac_code: Optional[str] = None
    processing_content: Optional[str] = None
    product_name: Optional[str] = None
    delivery_location: Optional[str] = None
    box_type: Optional[str] = None
    capacity: Optional[int] = None
    grouping_category: Optional[str] = None
    form_category: Optional[str] = None
    inspection_category: Optional[str] = None
    ordering_category: Optional[str] = None
    regular_replenishment_category: Optional[str] = None
    lead_time: Optional[int] = None
    fixed_point_days: Optional[int] = None
    shipping_factory: Optional[str] = None
    client_product_code: Optional[str] = None
    purchasing_org: Optional[str] = None
    item_group: Optional[str] = None
    processing_type: Optional[str] = None
    inventory_transfer_category: Optional[str] = None
    container_width: Optional[int] = None
    container_depth: Optional[int] = None
    container_height: Optional[int] = None
    stackable: Optional[bool] = True
    created_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成（余分なキーを無視）"""
        valid_fields = {}
        for field_name, field_type in cls.__annotations__.items():
            if field_name in data and data[field_name] is not None:
                valid_fields[field_name] = data[field_name]
        return cls(**valid_fields)

@dataclass
class ProductConstraint:
    """製品制約モデル - production_constraintsテーブル構造に合わせる"""
    product_id: int  # デフォルト値なしの引数を先に
    daily_capacity: int = 1000
    smoothing_level: float = 0.70
    volume_per_unit: float = 1.00
    is_transport_constrained: bool = False
    id: Optional[int] = None  # デフォルト値ありの引数を後に
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    # 結合用フィールド
    product_code: Optional[str] = None
    product_name: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        valid_fields = {}
        for field_name, field_type in cls.__annotations__.items():
            if field_name in data and data[field_name] is not None:
                # tinyint(1)をboolに変換
                if field_name == 'is_transport_constrained' and isinstance(data[field_name], int):
                    valid_fields[field_name] = bool(data[field_name])
                else:
                    valid_fields[field_name] = data[field_name]
        return cls(**valid_fields)
    updated_at: Optional[str] = None
    # 結合用フィールド
    product_code: Optional[str] = None
    product_name: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        """辞書からモデルを作成"""
        valid_fields = {}
        for field_name, field_type in cls.__annotations__.items():
            if field_name in data and data[field_name] is not None:
                # tinyint(1)をboolに変換
                if field_name == 'is_transport_constrained' and isinstance(data[field_name], int):
                    valid_fields[field_name] = bool(data[field_name])
                else:
                    valid_fields[field_name] = data[field_name]
        return cls(**valid_fields)