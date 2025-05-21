import os

def create_weekly_log():
    """Tạo nhật ký tuần mới"""
    try:
        week = int(input("Nhập số tuần: "))
        hours = float(input("Nhập số giờ làm việc: "))
        tasks = int(input("Nhập số nhiệm vụ hoàn thành: "))
        notes = input("Nhập ghi chú: ")
        
        filename = f"week_{week}.txt"
        with open(filename, 'w') as f:
            f.write(f"Tuần: {week}\n")
            f.write(f"Số giờ làm việc: {hours}\n")
            f.write(f"Nhiệm vụ hoàn thành: {tasks}\n")
            f.write(f"Ghi chú: {notes}\n")
            
        print(f"Đã tạo nhật ký tuần {week}")
    except ValueError:
        print("Lỗi: Dữ liệu nhập không hợp lệ")

def read_weekly_log():
    """Đọc nhật ký tuần"""
    try:
        week = int(input("Nhập số tuần cần đọc: "))
        filename = f"week_{week}.txt"
        
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                print(f"\n=== NHẬT KÝ TUẦN {week} ===")
                print(f.read())
        else:
            print(f"Nhật ký tuần {week} không tồn tại.")
    except ValueError:
        print("Lỗi: Số tuần phải là số nguyên")

def update_weekly_log():
    """Cập nhật nhật ký tuần"""
    try:
        week = int(input("Nhập số tuần cần cập nhật: "))
        filename = f"week_{week}.txt"
        
        if os.path.exists(filename):
            print(f"\nNhập thông tin mới cho tuần {week}:")
            hours = float(input("Số giờ làm việc: "))
            tasks = int(input("Số nhiệm vụ hoàn thành: "))
            notes = input("Ghi chú: ")
            
            with open(filename, 'w') as f:
                f.write(f"Tuần: {week}\n")
                f.write(f"Số giờ làm việc: {hours}\n")
                f.write(f"Nhiệm vụ hoàn thành: {tasks}\n")
                f.write(f"Ghi chú: {notes}\n")
                
            print(f"Đã cập nhật nhật ký tuần {week}")
        else:
            print(f"Nhật ký tuần {week} không tồn tại. Tạo mới?")
            create_weekly_log()
    except ValueError:
        print("Lỗi: Dữ liệu nhập không hợp lệ")

def delete_weekly_log():
    """Xóa nhật ký tuần"""
    try:
        week = int(input("Nhập số tuần cần xóa: "))
        filename = f"week_{week}.txt"
        
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Đã xóa nhật ký tuần {week}")
        else:
            print(f"Không tìm thấy nhật ký tuần {week}")
    except ValueError:
        print("Lỗi: Số tuần phải là số nguyên")

def generate_summary():
    """Tạo báo cáo tổng kết"""
    total_weeks = 0
    total_hours = 0.0
    total_tasks = 0
    
    for filename in os.listdir():
        if filename.startswith("week_") and filename.endswith(".txt"):
            try:
                with open(filename, 'r') as f:
                    lines = f.readlines()
                    total_weeks += 1
                    total_hours += float(lines[1].split(": ")[1])
                    total_tasks += int(lines[2].split(": ")[1])
            except (IndexError, ValueError):
                continue
    
    print("\n=== BÁO CÁO TỔNG KẾT ===")
    print(f"Tổng số tuần: {total_weeks}")
    print(f"Tổng số giờ làm việc: {total_hours}")
    print(f"Tổng nhiệm vụ hoàn thành: {total_tasks}")

def main():
    """Hàm chính"""
    while True:
        print("\n=== QUẢN LÝ NHẬT KÝ TUẦN ===")
        print("1. Tạo nhật ký tuần mới")
        print("2. Đọc nhật ký tuần")
        print("3. Cập nhật nhật ký tuần")
        print("4. Xóa nhật ký tuần")
        print("5. Tạo báo cáo tổng kết")
        print("6. Thoát")
        
        choice = input("Chọn chức năng (1-6): ")
        
        if choice == "1":
            create_weekly_log()
        elif choice == "2":
            read_weekly_log()
        elif choice == "3":
            update_weekly_log()
        elif choice == "4":
            delete_weekly_log()
        elif choice == "5":
            generate_summary()
        elif choice == "6":
            print("Cảm ơn đã sử dụng chương trình!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn từ 1 đến 6.")

if __name__ == "__main__":
    main()