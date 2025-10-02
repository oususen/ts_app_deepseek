# app/domain/calculators/transport_planner.py
from typing import List, Dict, Any
from ..models.transport import Container, Truck, LoadingItem, TransportPlan

class TransportPlanner:
    """運送計画計算機"""
    
    def calculate_loading_plan(self, 
                             items: List[LoadingItem],
                             containers: List[Container],
                             trucks: List[Truck]) -> Dict[str, Any]:
        """積載計画計算"""
        
        plans = []
        remaining_items = items.copy()
        
        # トラックごとに計画作成（デフォルト便を優先）
        sorted_trucks = sorted(trucks, key=lambda x: (not x.default_use, x.departure_time or '23:59:59'))
        
        for truck in sorted_trucks:
            # 各トラックに対して1便のみ計画（max_daily_tripsの代わり）
            truck_plan = self._plan_truck_loading(remaining_items, containers, truck)
            if truck_plan.loaded_items:
                plans.append(truck_plan)
                # 積載済みアイテムを除去
                remaining_items = self._remove_loaded_items(remaining_items, truck_plan.loaded_items)
            
            if not remaining_items:
                break
        
        return {
            "plans": plans,
            "remaining_items": remaining_items,
            "total_trips": len(plans),
            "efficiency": self._calculate_efficiency(plans)
        }
    
    def _plan_truck_loading(self, 
                          items: List[LoadingItem],
                          containers: List[Container],
                          truck: Truck) -> TransportPlan:
        """個別トラックの積載計画"""
        
        loaded_items = []
        current_volume = 0
        current_weight = 0
        truck_volume = (truck.width * truck.depth * truck.height) / 1000000000  # mm³ → m³
        
        for item in items:
            container = next((c for c in containers if c.id == item.container_id), None)
            if not container:
                continue
            
            # 容器の体積計算 (mm³ → m³)
            container_volume = (container.width * container.depth * container.height) / 1000000000
            item_volume = container_volume * item.quantity
            item_weight = item.weight_per_unit * item.quantity
            
            # 積載可否チェック
            if (current_volume + item_volume <= truck_volume and 
                current_weight + item_weight <= truck.max_weight):
                
                loaded_items.append(item)
                current_volume += item_volume
                current_weight += item_weight
        
        return TransportPlan(
            truck=truck,
            loaded_items=loaded_items,
            total_volume=current_volume,
            total_weight=current_weight,
            volume_utilization=current_volume / truck_volume if truck_volume > 0 else 0,
            weight_utilization=current_weight / truck.max_weight if truck.max_weight > 0 else 0
        )
    
    def _remove_loaded_items(self, items: List[LoadingItem], loaded_items: List[LoadingItem]) -> List[LoadingItem]:
        """積載済みアイテムを除去"""
        loaded_ids = {(item.product_id, item.container_id) for item in loaded_items}
        return [item for item in items if (item.product_id, item.container_id) not in loaded_ids]
    
    def _calculate_efficiency(self, plans: List[TransportPlan]) -> float:
        """積載効率計算"""
        if not plans:
            return 0.0
        
        total_volume_utilization = sum(plan.volume_utilization for plan in plans)
        total_weight_utilization = sum(plan.weight_utilization for plan in plans)
        
        return (total_volume_utilization + total_weight_utilization) / (2 * len(plans))