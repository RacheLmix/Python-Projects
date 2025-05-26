import numpy as np
from scipy import stats, optimize
import os

# 1. Tạo và lưu dữ liệu hiệu suất vào file .npy
def generate_performance_data(filename='performance.npy'):
    np.random.seed(0)  # Để tái lập kết quả
    data = []

    # Giả sử có 5 thành viên và 4 tuần
    for _ in range(4):  # 4 tuần
        week_data = []
        for _ in range(5):  # 5 thành viên
            hours = round(np.random.uniform(35, 45), 1)  # Giờ làm việc
            tasks = np.random.randint(3, 8)  # Số nhiệm vụ
            week_data.append([hours, tasks])
        data.append(week_data)

    performance_array = np.array(data)
    np.save(filename, performance_array)
    print(f"Dữ liệu đã được lưu vào {filename}\n")

# 2. Phân tích thống kê cơ bản
def basic_analysis(filename='performance.npy'):
    if not os.path.exists(filename):
        print("Tệp dữ liệu không tồn tại!")
        return

    data = np.load(filename)
    num_weeks = data.shape[0]

    for week in range(num_weeks):
        week_data = data[week]
        hours = week_data[:, 0]
        tasks = week_data[:, 1]

        avg_hours = np.mean(hours)
        std_hours = np.std(hours)
        total_tasks = int(np.sum(tasks))
        best_member_index = int(np.argmax(tasks))
        best_tasks = int(tasks[best_member_index])

        print(f"Phân tích tuần {week + 1}:")
        print(f"- Trung bình giờ làm: {avg_hours:.2f}")
        print(f"- Độ lệch chuẩn giờ: {std_hours:.2f}")
        print(f"- Tổng nhiệm vụ: {total_tasks}")
        print(f"- Thành viên xuất sắc: Thành viên {best_member_index + 1} ({best_tasks} nhiệm vụ)\n")

# 3. Phân tích nâng cao với SciPy
def advanced_analysis(filename='performance.npy'):
    if not os.path.exists(filename):
        print("Tệp dữ liệu không tồn tại!")
        return

    data = np.load(filename)
    hours_all = data[:, :, 0].flatten()
    tasks_all = data[:, :, 1].flatten()

    # Hồi quy tuyến tính
    slope, intercept, r_value, p_value, std_err = stats.linregress(hours_all, tasks_all)

    # Tính hệ số tương quan Pearson
    correlation, _ = stats.pearsonr(hours_all, tasks_all)

    # Tìm outliers trong giờ làm việc
    mean_hours = np.mean(hours_all)
    std_hours = np.std(hours_all)
    outliers = hours_all[(hours_all < mean_hours - 2 * std_hours) | (hours_all > mean_hours + 2 * std_hours)]

    print("Hồi quy tuyến tính:")
    print(f"- Độ dốc: {slope:.4f}")
    print(f"- Hệ số tương quan: {correlation:.4f}")
    print(f"- Giá trị ngoại lai (giờ làm): {outliers.tolist()}\n")

    return slope, intercept  # Trả về để dùng cho tối ưu

# 4. Tối ưu phân bổ công việc
def optimize_workload(slope, intercept, num_members=5, total_hours=200, min_hours=30):
    def objective(x):
        # Hàm mục tiêu: tổng nhiệm vụ hoàn thành (- để maximize)
        predicted_tasks = slope * np.array(x) + intercept
        return -np.sum(predicted_tasks)

    constraints = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - total_hours}  # Tổng giờ = 200
    ]

    bounds = [(min_hours, total_hours) for _ in range(num_members)]

    # Phân phối ban đầu đều nhau
    x0 = [total_hours / num_members] * num_members

    result = optimize.minimize(objective, x0, bounds=bounds, constraints=constraints)

    print("Phân bổ giờ làm tuần tới:")
    if result.success:
        for i, hours in enumerate(result.x):
            print(f"- Thành viên {i + 1}: {hours:.2f} giờ")
    else:
        print("Không thể tìm được phương án tối ưu.")

# 5. Hàm main tích hợp tất cả
def main():
    try:
        # Bước 1: Tạo và lưu dữ liệu
        generate_performance_data()

        # Bước 2: Phân tích thống kê cơ bản
        basic_analysis()

        # Bước 3: Phân tích nâng cao và nhận hệ số hồi quy
        slope, intercept = advanced_analysis()

        # Bước 4: Tối ưu phân bổ giờ làm việc tuần tới
        optimize_workload(slope, intercept)

    except Exception as e:
        print(f"Lỗi xảy ra: {e}")

if __name__ == "__main__":
    main()
