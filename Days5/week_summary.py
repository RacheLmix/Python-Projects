import re
import json
from datetime import datetime
import pendulum
from tabulate import tabulate
from google.colab import drive

class WeekSummary:
    def __init__(self):
        self.students = []

    def validate_input(self, name: str, email: str, exercises: int, score: float) -> bool:
        if not re.match(r'^[a-zA-Z\sÀ-ỹ]+$', name):
            raise ValueError("Tên chỉ được chứa chữ cái và khoảng trắng")

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Email không hợp lệ")

        if exercises < 0:
            raise ValueError("Số bài tập không thể âm")

        if not 0 <= score <= 10:
            raise ValueError("Điểm phải từ 0 đến 10")

        return True

    def calculate_stats(self) -> dict:
        if not self.students:
            raise ValueError("Chưa có dữ liệu học viên")

        avg_score = round(sum(s['score'] for s in self.students) / len(self.students), 2)
        max_student = max(self.students, key=lambda x: x['score'])
        min_student = min(self.students, key=lambda x: x['score'])
        completion_rate = round(sum(s['exercises'] for s in self.students) / (5 * len(self.students)) * 100, 2)

        return {
            'avg_score': avg_score,
            'top_student': max_student['name'],
            'top_score': max_student['score'],
            'low_student': min_student['name'],
            'low_score': min_student['score'],
            'completion_rate': completion_rate
        }

    def save_to_drive(self, week_num: int) -> None:
        summary = {
            'week': week_num,
            'date': pendulum.now("Asia/Ho_Chi_Minh").format("dddd, DD/MM/YYYY"),
            'students': self.students,
            'stats': self.calculate_stats()
        }

        filename = f"/content/drive/MyDrive/week_{week_num}.json"
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=4)

        print(f"✅ Đã lưu tổng kết tuần {week_num} vào Google Drive.")

    def load_from_drive(self, week_num: int) -> dict:
        filename = f"/content/drive/MyDrive/week_{week_num}.json"
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise ValueError(f"Không tìm thấy file tổng kết tuần {week_num} trên Google Drive.")

def display_stats(stats):
    print("\n=== THỐNG KÊ TUẦN ===")
    print(f"Điểm trung bình: {stats['avg_score']}")
    print(f"Học viên xuất sắc: {stats['top_student']} ({stats['top_score']})")
    print(f"Học viên điểm thấp nhất: {stats['low_student']} ({stats['low_score']})")
    print(f"Tỷ lệ hoàn thành: {stats['completion_rate']}%")

def main():
    print("=== CÔNG CỤ TỔNG KẾT TUẦN HỌC TẬP ===\n")

    # Kết nối Google Drive
    drive.mount('/content/drive')

    summary = WeekSummary()

    try:
        week_num = int(input("Nhập số tuần học: "))

        n = int(input("Nhập số lượng học viên (tối thiểu 3): "))
        if n < 3:
            raise ValueError("Cần ít nhất 3 học viên")

        for i in range(n):
            print(f"\nNhập thông tin học viên thứ {i+1}:")
            while True:
                try:
                    name = input("Họ tên: ")
                    email = input("Email: ")
                    exercises = int(input("Số bài tập hoàn thành: "))
                    score = float(input("Điểm trung bình: "))

                    summary.validate_input(name, email, exercises, score)
                    summary.students.append({
                        'name': name,
                        'email': email,
                        'exercises': exercises,
                        'score': score
                    })
                    break
                except Exception as e:
                    print(f"❌ Lỗi: {e} - Vui lòng nhập lại.")

        stats = summary.calculate_stats()
        display_stats(stats)

        print("\n=== DANH SÁCH HỌC VIÊN ===")
        print(tabulate(
            [[s['name'], s['email'], s['exercises'], s['score']] for s in summary.students],
            headers=["Họ tên", "Email", "Bài tập", "Điểm"],
            tablefmt="grid"
        ))

        summary.save_to_drive(week_num)

        loaded_data = summary.load_from_drive(week_num)
        print(f"\n✅ Đã đọc lại dữ liệu tuần {loaded_data['week']}: {loaded_data['date']}")
        print(tabulate(
            [[s['name'], s['email'], s['exercises'], s['score']] for s in loaded_data['students']],
            headers=["Họ tên", "Email", "Bài tập", "Điểm"],
            tablefmt="grid"
        ))

    except Exception as e:
        print(f"❌ Lỗi chương trình: {e}")

if __name__ == "__main__":
    main()
