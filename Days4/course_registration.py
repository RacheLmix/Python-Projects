import re
import json
from datetime import datetime
import pendulum  # Thư viện xử lý ngày giờ nâng cao
# Cài đặt: pip install pendulum

class CourseRegistration:
    def __init__(self):
        self.courses = {
            "KH001": 1000000,
            "KH002": 1500000,
            "KH003": 2000000
        }
        self.discounts = {
            "SUMMER25": 0.25,
            "EARLYBIRD": 0.15
        }

    def validate_input(self, name: str, email: str, course_code: str) -> bool:
        """Kiểm tra dữ liệu đầu vào"""
        if len(name) < 3:
            raise ValueError("Tên phải có ít nhất 3 ký tự")
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Email không hợp lệ")
            
        if not re.match(r'^KH\d{3}$', course_code):
            raise ValueError("Mã khóa học phải có dạng KHxxx (x là số)")
            
        return True

    def calculate_cost(self, course_code: str, quantity: int, promo_code: str = None) -> float:
        """Tính toán chi phí khóa học"""
        if course_code not in self.courses:
            raise ValueError("Mã khóa học không tồn tại")
            
        base_price = self.courses[course_code]
        total = base_price * quantity
        
        if promo_code in self.discounts:
            total *= (1 - self.discounts[promo_code])
            
        return round(total, 2)

    def save_registration(self, filename: str, data: dict) -> None:
        """Lưu thông tin đăng ký vào file JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            raise IOError(f"Lỗi khi lưu file: {str(e)}")

    def load_registrations(self, filename: str) -> list:
        """Đọc thông tin đăng ký từ file JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except Exception as e:
            raise IOError(f"Lỗi khi đọc file: {str(e)}")

def main():
    registration = CourseRegistration()
    
    try:
        # Nhập thông tin
        name = input("Nhập họ tên: ")
        email = input("Nhập email: ")
        course_code = input("Nhập mã khóa học (KHxxx): ").upper()
        
        # Kiểm tra dữ liệu
        registration.validate_input(name, email, course_code)
        
        # Nhập số lượng và mã ưu đãi
        quantity = int(input("Nhập số lượng: "))
        promo_code = input("Nhập mã ưu đãi (nếu có): ").upper() or None
        
        # Tính toán chi phí
        cost = registration.calculate_cost(course_code, quantity, promo_code)
        print(f"\nTổng chi phí cho {quantity} khóa học là: {cost:,.2f} VNĐ")
        
        # Lưu thông tin đăng ký
        reg_date = pendulum.now().to_datetime_string()
        data = {
            "name": name,
            "email": email,
            "course_code": course_code,
            "date": reg_date,
            "cost": cost
        }
        
        registration.save_registration("registrations.json", data)
        print(f"\nChúc mừng {name} đã đăng ký khóa học {course_code} vào ngày {reg_date}!")
        
        # Hiển thị danh sách đăng ký
        print("\nDanh sách đăng ký:")
        registrations = registration.load_registrations("registrations.json")
        for reg in registrations:
            print(f"Đăng ký của {reg['name']}: Khóa học {reg['course_code']}, Ngày {reg['date']}, Chi phí {reg['cost']:,.2f} VNĐ")
            
    except Exception as e:
        print(f"\nLỗi: {str(e)}")

if __name__ == "__main__":
    main()