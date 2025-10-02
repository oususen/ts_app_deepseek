# app/services/transport_service.py
from typing import List, Dict, Any
from repository.transport_repository import TransportRepository
from domain.calculators.transport_planner import TransportPlanner
from domain.validators.loading_validator import LoadingValidator
from domain.models.transport import Container, Truck, LoadingItem

class TransportService:
    """運送関連ビジネスロジック"""
    
    def __init__(self, db_manager):
        self.repository = TransportRepository(db_manager)
        self.planner = TransportPlanner()
        self.validator = LoadingValidator()
    
    def get_containers(self) -> List[Container]:
        """容器一覧取得"""
        df = self.repository.get_containers()
        return [Container(**row) for row in df.to_dict('records')]
    
    def get_trucks(self):
        """トラック一覧取得"""
        return self.repository.get_trucks()

    def delete_truck(self, truck_id: int) -> bool:
        """トラック削除"""
        return self.repository.delete_truck(truck_id) 
    def create_container(self, container_data: dict) -> bool:
        """容器作成"""
        return self.repository.save_container(container_data)
    
    def create_truck(self, truck_data: dict) -> bool:
        """トラック作成"""
        return self.repository.save_truck(truck_data)
    
    def calculate_delivery_plan(self, delivery_items: List[dict]) -> Dict[str, Any]:
        """配送計画計算"""
        containers = self.get_containers()
        trucks = self.get_trucks()
        
        # モデル変換
        items = [LoadingItem(**item) for item in delivery_items]
        
        # 計画計算
        return self.planner.calculate_loading_plan(items, containers, trucks)
    
    def validate_loading(self, items: List[dict], truck_id: int) -> tuple:
        """積載バリデーション"""
        containers = self.get_containers()
        trucks = self.get_trucks()
        
        truck = next((t for t in trucks if t.id == truck_id), None)
        if not truck:
            return False, ["トラックが見つかりません"]
        
        loading_items = [LoadingItem(**item) for item in items]
        return self.validator.validate_loading(loading_items, containers, truck)