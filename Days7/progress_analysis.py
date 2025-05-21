import pandas as pd
import matplotlib.pyplot as plt

# Tạo dữ liệu mẫu
def create_sample_data():
    data = {
        'Tên': ['An', 'Bình', 'Chi', 'Dũng', 'Hà'] * 3,
        'Tuần': [1]*5 + [2]*5 + [3]*5,
        'Bài tập': [5, 4, 3, 6, 5, 6, 5, 4, 7, 6, 7, 6, 5, 8, 7],
        'Điểm': [8.5, 7.0, 6.5, 9.0, 8.0, 9.0, 8.5, 7.5, 9.5, 9.0, 9.5, 9.0, 8.5, 10.0, 9.5]
    }
    df = pd.DataFrame(data)
    df.to_csv('progress.csv', index=False)
    return df

# Phân tích tiến độ tuần
def analyze_weekly_progress(week):
    try:
        df = pd.read_csv('progress.csv')
        weekly_data = df[df['Tuần'] == week]
        
        avg_exercises = weekly_data['Bài tập'].mean()
        avg_score = weekly_data['Điểm'].mean()
        top_student = weekly_data.loc[weekly_data['Điểm'].idxmax()]
        
        print(f"\nPhân tích tuần {week}:")
        print(f"- Bài tập trung bình: {avg_exercises:.1f}")
        print(f"- Điểm trung bình: {avg_score:.1f}")
        print(f"- Học viên xuất sắc: {top_student['Tên']} ({top_student['Điểm']})")
        
        # Hiển thị học viên hoàn thành trên 4 bài tập
        active_students = weekly_data[weekly_data['Bài tập'] > 4]
        print("\nHọc viên tích cực (hoàn thành >4 bài tập):")
        print(active_students[['Tên', 'Bài tập', 'Điểm']])
        
        return weekly_data
    except FileNotFoundError:
        print("Không tìm thấy file dữ liệu. Vui lòng tạo dữ liệu mẫu trước.")
        return None

# Trực quan hóa dữ liệu
def visualize_progress():
    try:
        df = pd.read_csv('progress.csv')
        
        # Biểu đồ đường: Xu hướng điểm trung bình
        plt.figure(figsize=(10, 5))
        for name in df['Tên'].unique():
            student_data = df[df['Tên'] == name]
            plt.plot(student_data['Tuần'], student_data['Điểm'], marker='o', label=name)
        
        plt.title('Xu hướng điểm trung bình qua các tuần')
        plt.xlabel('Tuần')
        plt.ylabel('Điểm')
        plt.legend()
        plt.grid(True)
        plt.savefig('trend.png')
        plt.close()
        
        # Biểu đồ cột: Bài tập hoàn thành trung bình
        avg_exercises = df.groupby('Tuần')['Bài tập'].mean()
        plt.figure(figsize=(8, 5))
        avg_exercises.plot(kind='bar', color='skyblue')
        plt.title('Số bài tập hoàn thành trung bình theo tuần')
        plt.xlabel('Tuần')
        plt.ylabel('Số bài tập')
        plt.xticks(rotation=0)
        plt.savefig('comparison.png')
        plt.close()
        
        print("Đã tạo và lưu các biểu đồ: trend.png và comparison.png")
    except FileNotFoundError:
        print("Không tìm thấy file dữ liệu. Vui lòng tạo dữ liệu mẫu trước.")

# Tạo báo cáo tổng kết
def generate_weekly_report():
    try:
        df = pd.read_csv('progress.csv')
        
        # Tính tổng bài tập và điểm trung bình
        summary = df.groupby('Tên').agg({
            'Bài tập': 'sum',
            'Điểm': 'mean'
        }).reset_index()
        
        # Tìm học viên tiến bộ nhất
        progress = []
        for name in df['Tên'].unique():
            student_data = df[df['Tên'] == name]
            progress.append({
                'Tên': name,
                'Tiến bộ': student_data.iloc[-1]['Điểm'] - student_data.iloc[0]['Điểm']
            })
        
        top_progress = max(progress, key=lambda x: x['Tiến bộ'])
        
        # Lưu báo cáo
        with open('report.txt', 'w', encoding='utf-8') as f:
            f.write("Báo cáo tổng kết:\n\n")
            for _, row in summary.iterrows():
                f.write(f"- Tổng bài tập của {row['Tên']}: {row['Bài tập']}\n")
                f.write(f"- Điểm trung bình của {row['Tên']}: {row['Điểm']:.1f}\n\n")
            f.write(f"Học viên tiến bộ nhất: {top_progress['Tên']} (tăng {top_progress['Tiến bộ']:.1f} điểm)")
        
        # Biểu đồ tròn: Đóng góp bài tập
        plt.figure(figsize=(8, 8))
        plt.pie(summary['Bài tập'], labels=summary['Tên'], autopct='%1.1f%%')
        plt.title('Tỷ lệ đóng góp bài tập của từng học viên')
        plt.savefig('contribution.png')
        plt.close()
        
        print("Đã tạo báo cáo: report.txt và biểu đồ contribution.png")
    except FileNotFoundError:
        print("Không tìm thấy file dữ liệu. Vui lòng tạo dữ liệu mẫu trước.")

# Hàm chính
def main():
    print("=== CÔNG CỤ PHÂN TÍCH TIẾN ĐỘ HỌC TẬP ===\n")
    
    # Tạo dữ liệu mẫu nếu chưa có
    try:
        pd.read_csv('progress.csv')
    except FileNotFoundError:
        print("Tạo dữ liệu mẫu...")
        create_sample_data()
    
    # Phân tích tuần 1
    analyze_weekly_progress(1)
    
    # Tạo biểu đồ
    visualize_progress()
    
    # Tạo báo cáo
    generate_weekly_report()
    
    print("\nHoàn thành phân tích tiến độ học tập!")

if __name__ == "__main__":
    main()