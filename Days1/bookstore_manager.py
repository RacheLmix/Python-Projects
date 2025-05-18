# Hệ thống quản lý cửa hàng sách

# Khởi tạo dữ liệu sách
books = [
    {"name": "Python Programming", "price": 120000.0, "stock": 15, "sold": 25},
    {"name": "Clean Code", "price": 150000.0, "stock": 8, "sold": 12},
    {"name": "Data Structures", "price": 90000.0, "stock": 5, "sold": 8},
    {"name": "Algorithms", "price": 110000.0, "stock": 0, "sold": 30},
    {"name": "Introduction to AI", "price": 80000.0, "stock": 10, "sold": 5}
]

# Thông tin khách hàng
customer_name = "Nguyen Van A"
customer_type = "VIP"

def calculate_bill(book_name, quantity, customer_type):
    """
    Tính tổng hóa đơn cho sách đã mua với giảm giá cho khách VIP
    
    Tham số:
        book_name (str): Tên sách
        quantity (int): Số lượng mua
        customer_type (str): "VIP" hoặc "thường"
        
    Trả về:
        tuple: (tổng_tiền (float), trạng_thái_kho (str))
    """
    # Find the book
    book = next((b for b in books if b["name"] == book_name), None)
    
    if not book:
        return (0.0, "Không tìm thấy sách")
        
    if quantity <= 0:
        return (0.0, "Số lượng không hợp lệ")
    
    # Calculate total
    total = book["price"] * quantity
    
    # Apply VIP discount
    if customer_type == "VIP":
        total *= 0.9  # 10% discount
    
    # Check stock
    if book["stock"] == 0:
        return (total, "Hết hàng")
    elif book["stock"] < quantity:
        return (total, "Hết hàng hoặc không đủ")
    else:
        return (total, "Còn hàng")

# Function to check stock status
def check_stock(book_name, quantity):
    """
    Kiểm tra trạng thái kho và phân loại sách theo giá
    
    Tham số:
        book_name (str): Tên sách
        quantity (int): Số lượng kiểm tra
        
    Trả về:
        tuple: (còn_hàng (bool), thông_báo (str), phân_loại_giá (str))
    """
    book = next((b for b in books if b["name"] == book_name), None)
    
    if not book:
        return (False, "Không tìm thấy sách", "")
    
    # Check stock
    if book["stock"] == 0:
        return (False, "Hết hàng", "")
    elif book["stock"] < quantity:
        return (False, "Hết hàng hoặc không đủ", "")
    else:
        # Classify by price
        price = book["price"]
        if price < 50000:
            category = "Sách giá rẻ"
        elif 50000 <= price <= 100000:
            category = "Sách trung bình"
        else:
            category = "Sách cao cấp"
            
        return (True, "Còn hàng", category)

# Lambda function to generate discount code
generate_discount_code = lambda name, c_type: name.upper() + "_VIP" if c_type == "VIP" else name.upper() + "_REG"

# Function to find popular books
def find_popular_books():
    """In sách bán chạy (số lượng bán > 10) và tìm sách bán chạy nhất"""
    print("Sách bán chạy (số lượng bán > 10):")
    
    # Using for loop to find popular books
    for book in books:
        if book["sold"] > 10:
            print(f"- {book['name']}: {book['sold']} cuốn")
    
    # Using while loop to find the bestseller
    if books:
        max_sold = 0
        bestseller = None
        i = 0
        
        while i < len(books):
            if books[i]["sold"] > max_sold:
                max_sold = books[i]["sold"]
                bestseller = books[i]
            i += 1
            
        if bestseller:
            print(f"\nSách bán chạy nhất: {bestseller['name']} ({bestseller['sold']} cuốn)")

# Main function
def main():
    """Thực thi chương trình chính"""
    # Example usage
    book_name = "Python Programming"
    quantity = 2
    
    # Calculate bill example
    total, status = calculate_bill(book_name, quantity, customer_type)
    print(f"\nHóa đơn cho {book_name}:")
    print(f"- Số lượng: {quantity}")
    print(f"- Tổng tiền: {total:,.0f} VNĐ")
    print(f"- Trạng thái: {status}")
    
    book_to_check = "Algorithms"
    check_qty = 1
    has_stock, message, category = check_stock(book_to_check, check_qty)
    print(f"\nKiểm tra kho cho {book_to_check}:")
    print(f"- Trạng thái: {message}")
    if category:
        print(f"- Phân loại: {category}")
    
    discount_code = generate_discount_code(customer_name, customer_type)
    print(f"\nMã giảm giá: {discount_code}")
    
    find_popular_books()

if __name__ == "__main__":
    main()