"""
Hệ thống quản lý đơn hàng cửa hàng trực tuyến với MongoDB
Mô tả: Hệ thống quản lý sản phẩm và đơn hàng với đầy đủ chức năng CRUD
"""

from pymongo import MongoClient
from datetime import datetime
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class OnlineStoreManager:
    def __init__(self, connection_string="mongodb://localhost:27017/"):
        """
        Khởi tạo kết nối MongoDB
        Args:
            connection_string: Chuỗi kết nối MongoDB
        """
        try:
            self.client = MongoClient(connection_string)
            self.db = self.client.online_store
            logger.info("Kết nối MongoDB thành công")
        except Exception as e:
            logger.error(f"Lỗi kết nối MongoDB: {e}")
            raise

    def setup_database(self):
        """
        Tạo cơ sở dữ liệu và collection
        - Tạo database online_store
        - Tạo collection products và orders
        """
        try:
            # Kiểm tra và tạo collection products
            if "products" not in self.db.list_collection_names():
                self.db.create_collection("products")
                logger.info("Tạo collection 'products' thành công")
            else:
                logger.info("Collection 'products' đã tồn tại")

            # Kiểm tra và tạo collection orders
            if "orders" not in self.db.list_collection_names():
                self.db.create_collection("orders")
                logger.info("Tạo collection 'orders' thành công")
            else:
                logger.info("Collection 'orders' đã tồn tại")

            # Tạo index để tối ưu truy vấn
            self.db.products.create_index("product_id", unique=True)
            self.db.orders.create_index("order_id", unique=True)
            self.db.orders.create_index("customer_name")

            logger.info("Thiết lập database hoàn tất")

        except Exception as e:
            logger.error(f"Lỗi thiết lập database: {e}")
            raise

    def add_data(self):
        """
        Thêm dữ liệu mẫu vào database
        - Thêm 5 sản phẩm vào collection products
        - Thêm 10 đơn hàng vào collection orders
        """
        try:
            # Dữ liệu sản phẩm mẫu (Insert nhiều sản phẩm)
            products_data = [
                {"product_id": "SP001", "name": "Áo thun nam", "price": 150000.0, "stock": 50},
                {"product_id": "SP002", "name": "Quần jean nữ", "price": 450000.0, "stock": 30},
                {"product_id": "SP003", "name": "Giày thể thao", "price": 800000.0, "stock": 25},
                {"product_id": "SP004", "name": "Túi xách da", "price": 1200000.0, "stock": 15},
                {"product_id": "SP005", "name": "Mũ lưỡi trai", "price": 80000.0, "stock": 100}
            ]

            # Kiểm tra và thêm sản phẩm (tránh trùng lặp)
            for product in products_data:
                existing = self.db.products.find_one({"product_id": product["product_id"]})
                if not existing:
                    self.db.products.insert_one(product)
                    logger.info(f"Thêm sản phẩm {product['product_id']}: {product['name']}")

            # Dữ liệu đơn hàng mẫu (Insert nhiều đơn hàng)
            orders_data = [
                {"order_id": "DH001", "customer_name": "Nguyễn Văn An", "product_id": "SP001", "quantity": 2,
                 "total_price": 300000.0, "order_date": "2025-04-10"},
                {"order_id": "DH002", "customer_name": "Trần Thị Bình", "product_id": "SP002", "quantity": 1,
                 "total_price": 450000.0, "order_date": "2025-04-11"},
                {"order_id": "DH003", "customer_name": "Lê Văn Cường", "product_id": "SP003", "quantity": 1,
                 "total_price": 800000.0, "order_date": "2025-04-12"},
                {"order_id": "DH004", "customer_name": "Nguyễn Văn An", "product_id": "SP004", "quantity": 1,
                 "total_price": 1200000.0, "order_date": "2025-04-13"},
                {"order_id": "DH005", "customer_name": "Phạm Thị Dung", "product_id": "SP005", "quantity": 3,
                 "total_price": 240000.0, "order_date": "2025-04-14"},
                {"order_id": "DH006", "customer_name": "Trần Thị Bình", "product_id": "SP001", "quantity": 5,
                 "total_price": 750000.0, "order_date": "2025-04-15"},
                {"order_id": "DH007", "customer_name": "Lê Văn Cường", "product_id": "SP002", "quantity": 2,
                 "total_price": 900000.0, "order_date": "2025-04-16"},
                {"order_id": "DH008", "customer_name": "Nguyễn Văn An", "product_id": "SP005", "quantity": 1,
                 "total_price": 80000.0, "order_date": "2025-04-17"},
                {"order_id": "DH009", "customer_name": "Phạm Thị Dung", "product_id": "SP003", "quantity": 1,
                 "total_price": 800000.0, "order_date": "2025-04-18"},
                {"order_id": "DH010", "customer_name": "Trần Thị Bình", "product_id": "SP004", "quantity": 1,
                 "total_price": 1200000.0, "order_date": "2025-04-19"}
            ]

            # Kiểm tra và thêm đơn hàng (tránh trùng lặp)
            for order in orders_data:
                existing = self.db.orders.find_one({"order_id": order["order_id"]})
                if not existing and order["quantity"] > 0 and order["total_price"] > 0:
                    self.db.orders.insert_one(order)
                    logger.info(f"Thêm đơn hàng {order['order_id']} cho khách hàng {order['customer_name']}")

            logger.info("Thêm dữ liệu mẫu hoàn tất")

        except Exception as e:
            logger.error(f"Lỗi thêm dữ liệu: {e}")
            raise

    def query_orders(self, customer_name=None, min_price=500000):
        """
        Truy vấn đơn hàng với các điều kiện
        Args:
            customer_name: Tên khách hàng cần truy vấn
            min_price: Giá trị đơn hàng tối thiểu
        """
        try:
            print("\n" + "=" * 50)
            print("TRUY VẤN ĐỚN HÀNG")
            print("=" * 50)

            # 1. Truy vấn đơn hàng của khách hàng cụ thể (Query với $eq)
            if customer_name:
                print(f"\n1. Đơn hàng của khách hàng '{customer_name}':")
                customer_orders = self.db.orders.find({"customer_name": {"$eq": customer_name}})

                for order in customer_orders:
                    print(
                        f"- Mã đơn: {order['order_id']}, Sản phẩm: {order['product_id']}, Tổng: {order['total_price']:,.0f} VNĐ")

            # 2. Tìm đơn hàng có giá trị trên min_price (Query với $gt, Sort, Limit)
            print(f"\n2. Đơn hàng có giá trị trên {min_price:,.0f} VNĐ (sắp xếp giảm dần, tối đa 5 đơn):")

            high_value_orders = self.db.orders.find(
                {"total_price": {"$gt": min_price}}  # Query với $gt
            ).sort("total_price", -1).limit(5)  # Sort giảm dần và Limit 5 kết quả

            count = 0
            for order in high_value_orders:
                count += 1
                print(f"- Mã đơn: {order['order_id']}, Khách hàng: {order['customer_name']}, "
                      f"Sản phẩm: {order['product_id']}, Tổng: {order['total_price']:,.0f} VNĐ")

            if count == 0:
                print("- Không có đơn hàng nào thỏa mãn điều kiện")

        except Exception as e:
            logger.error(f"Lỗi truy vấn đơn hàng: {e}")
            raise

    def update_order(self, order_id, new_quantity):
        """
        Cập nhật đơn hàng (Update với $set)
        Args:
            order_id: Mã đơn hàng cần cập nhật
            new_quantity: Số lượng mới
        """
        try:
            # Tìm đơn hàng và sản phẩm để tính lại giá
            order = self.db.orders.find_one({"order_id": order_id})
            if not order:
                logger.warning(f"Không tìm thấy đơn hàng {order_id}")
                return

            product = self.db.products.find_one({"product_id": order["product_id"]})
            if not product:
                logger.warning(f"Không tìm thấy sản phẩm {order['product_id']}")
                return

            # Tính giá mới
            new_total_price = product["price"] * new_quantity

            # Cập nhật đơn hàng (Update với $set)
            result = self.db.orders.update_one(
                {"order_id": order_id},
                {"$set": {
                    "quantity": new_quantity,
                    "total_price": new_total_price
                }}
            )

            if result.modified_count > 0:
                print(f"\n✅ Cập nhật đơn hàng {order_id}:")
                print(f"- Số lượng mới: {new_quantity}")
                print(f"- Tổng giá mới: {new_total_price:,.0f} VNĐ")
                logger.info(f"Cập nhật đơn hàng {order_id} thành công")
            else:
                logger.warning(f"Không có thay đổi nào cho đơn hàng {order_id}")

        except Exception as e:
            logger.error(f"Lỗi cập nhật đơn hàng: {e}")
            raise

    def delete_order(self, max_price=100000):
        """
        Xóa các đơn hàng có giá trị thấp (Delete với $lt)
        Args:
            max_price: Giá trị tối đa của đơn hàng sẽ bị xóa
        """
        try:
            # Đếm số đơn hàng sẽ bị xóa
            count_before = self.db.orders.count_documents({"total_price": {"$lt": max_price}})

            if count_before == 0:
                print(f"\n⚠️  Không có đơn hàng nào có giá trị dưới {max_price:,.0f} VNĐ")
                return

            # Xóa đơn hàng (Delete với $lt)
            result = self.db.orders.delete_many({"total_price": {"$lt": max_price}})

            print(f"\n🗑️  Đã xóa {result.deleted_count} đơn hàng có giá trị dưới {max_price:,.0f} VNĐ")
            logger.info(f"Xóa {result.deleted_count} đơn hàng thành công")

        except Exception as e:
            logger.error(f"Lỗi xóa đơn hàng: {e}")
            raise

    def generate_report(self):
        """
        Tạo báo cáo doanh thu và thống kê sản phẩm
        Sử dụng aggregation pipeline để tính toán
        """
        try:
            print("\n" + "=" * 50)
            print("BÁO CÁO CỬA HÀNG")
            print("=" * 50)

            # 1. Tính doanh thu theo từng sản phẩm (sử dụng aggregation)
            print("\n📊 Doanh thu theo sản phẩm:")

            pipeline = [
                {"$group": {
                    "_id": "$product_id",
                    "total_revenue": {"$sum": "$total_price"},
                    "total_quantity": {"$sum": "$quantity"}
                }},
                {"$sort": {"total_revenue": -1}}
            ]

            revenue_data = list(self.db.orders.aggregate(pipeline))

            for item in revenue_data:
                product_info = self.db.products.find_one({"product_id": item["_id"]})
                product_name = product_info["name"] if product_info else "Không xác định"
                print(f"- Sản phẩm {item['_id']} ({product_name}): "
                      f"Doanh thu {item['total_revenue']:,.0f} VNĐ "
                      f"(Đã bán {item['total_quantity']} sản phẩm)")

            # 2. Thống kê sản phẩm tồn kho thấp (Query với $lt)
            print(f"\n📦 Sản phẩm tồn kho thấp (dưới 10 sản phẩm):")
            low_stock_products = list(self.db.products.find({"stock": {"$lt": 10}}))

            if low_stock_products:
                for product in low_stock_products:
                    print(f"- {product['product_id']} ({product['name']}): "
                          f"Còn {product['stock']} sản phẩm")
                print(f"\n⚠️  Tổng cộng: {len(low_stock_products)} sản phẩm cần nhập thêm")
            else:
                print("✅ Tất cả sản phẩm đều có tồn kho đủ")

            # 3. Thống kê tổng quan
            total_orders = self.db.orders.count_documents({})
            total_revenue = sum(item["total_revenue"] for item in revenue_data)
            total_products = self.db.products.count_documents({})

            print(f"\n📈 Tổng quan:")
            print(f"- Tổng số đơn hàng: {total_orders}")
            print(f"- Tổng doanh thu: {total_revenue:,.0f} VNĐ")
            print(f"- Tổng số sản phẩm: {total_products}")

        except Exception as e:
            logger.error(f"Lỗi tạo báo cáo: {e}")
            raise

    def cleanup_database(self, confirm=False):
        """
        Dọn dẹp database (Drop Collection)
        Args:
            confirm: Xác nhận xóa dữ liệu
        """
        try:
            if not confirm:
                response = input("\n❓ Bạn có chắc chắn muốn xóa collection 'orders'? (y/N): ")
                if response.lower() != 'y':
                    print("⏹️  Hủy thao tác dọn dẹp")
                    return

            # Kiểm tra collection có tồn tại không
            if "orders" in self.db.list_collection_names():
                self.db.orders.drop()  # Drop Collection
                print("🧹 Đã xóa collection 'orders'")
                logger.info("Xóa collection 'orders' thành công")
            else:
                print("⚠️  Collection 'orders' không tồn tại")

        except Exception as e:
            logger.error(f"Lỗi dọn dẹp database: {e}")
            raise

    def close_connection(self):
        """Đóng kết nối MongoDB"""
        try:
            self.client.close()
            logger.info("Đã đóng kết nối MongoDB")
        except Exception as e:
            logger.error(f"Lỗi đóng kết nối: {e}")


def main():
    """
    Hàm main tích hợp toàn bộ chương trình
    Thực hiện các chức năng theo thứ tự yêu cầu
    """
    print("🏪 KHỞI ĐỘNG HỆ THỐNG QUẢN LÝ CỬA HÀNG TRỰC TUYẾN")
    print("=" * 60)

    store_manager = None

    try:
        # 1. Khởi tạo kết nối và thiết lập database
        print("\n1️⃣  Thiết lập kết nối và database...")
        store_manager = OnlineStoreManager()
        store_manager.setup_database()

        # 2. Thêm dữ liệu mẫu
        print("\n2️⃣  Thêm dữ liệu mẫu...")
        store_manager.add_data()

        # 3. Truy vấn đơn hàng
        print("\n3️⃣  Truy vấn đơn hàng...")
        store_manager.query_orders(customer_name="Nguyễn Văn An", min_price=500000)

        # 4. Cập nhật đơn hàng
        print("\n4️⃣  Cập nhật đơn hàng...")
        store_manager.update_order("DH001", 3)  # Cập nhật đơn DH001 thành 3 sản phẩm

        # 5. Xóa đơn hàng giá trị thấp
        print("\n5️⃣  Xóa đơn hàng giá trị thấp...")
        store_manager.delete_order(100000)  # Xóa đơn hàng dưới 100,000 VNĐ

        # 6. Tạo báo cáo
        print("\n6️⃣  Tạo báo cáo doanh thu...")
        store_manager.generate_report()

        # 7. Tùy chọn dọn dẹp database
        print("\n7️⃣  Dọn dẹp database (tùy chọn)...")
        store_manager.cleanup_database()

        print("\n✅ HOÀN THÀNH TOÀN BỘ CÁC CHỨC NĂNG!")
        print("=" * 60)

    except Exception as e:
        logger.error(f"Lỗi trong quá trình thực thi: {e}")
        print(f"❌ Lỗi: {e}")

    finally:
        # Đảm bảo đóng kết nối
        if store_manager:
            store_manager.close_connection()


if __name__ == "__main__":
    main()