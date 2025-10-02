from repository.product_repository import ProductRepository
from domain.models.product import Product
from repository.transport_repository import TransportRepository

class ProductService:
    def __init__(self, db_manager):
        self.repository = ProductRepository(db_manager)
        self.container_repository = TransportRepository(db_manager)

    def get_products(self):
        return self.repository.get_all_products()

    def create_product(self, product_data: dict) -> bool:
        return self.repository.create_product(product_data)

    def update_product(self, product_id: int, update_data: dict) -> bool:
        return self.repository.update_product(product_id, update_data)

    def delete_product(self, product_id: int) -> bool:
        return self.repository.delete_product(product_id)

    def get_containers(self):
        """製品登録用に利用可能な容器一覧を取得"""
        return self.container_repository.get_containers()
