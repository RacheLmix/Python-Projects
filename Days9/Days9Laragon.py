import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': ''
}


def connect_to_mysql():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print("Lỗi kết nối MySQL:", e)
        return None


def setup_database():
    conn = connect_to_mysql()
    cursor = conn.cursor()

    # Tạo cơ sở dữ liệu nếu chưa tồn tại
    cursor.execute("CREATE DATABASE IF NOT EXISTS Days9")
    cursor.execute("USE Days9")

    # Tạo bảng members
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS members
                   (
                       member_id
                       INT
                       AUTO_INCREMENT
                       PRIMARY
                       KEY,
                       name
                       VARCHAR
                   (
                       100
                   ),
                       role VARCHAR
                   (
                       50
                   )
                       )
                   """)

    # Tạo bảng weekly_progress
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS weekly_progress
                   (
                       progress_id
                       INT
                       AUTO_INCREMENT
                       PRIMARY
                       KEY,
                       member_id
                       INT,
                       week_number
                       INT,
                       hours_worked
                       FLOAT
                       CHECK
                   (
                       hours_worked
                       >=
                       0
                   ),
                       tasks_completed INT,
                       notes TEXT,
                       FOREIGN KEY
                   (
                       member_id
                   ) REFERENCES members
                   (
                       member_id
                   )
                       )
                   """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Đã thiết lập cơ sở dữ liệu và bảng.")


def add_data():
    conn = connect_to_mysql()
    cursor = conn.cursor()
    cursor.execute("USE Days9")

    # Thêm thành viên
    members = [
        ("An", "Developer"),
        ("Bình", "Tester"),
        ("Cường", "Project Manager"),
        ("Dương", "Developer"),
        ("Evy", "Designer")
    ]
    cursor.executemany("INSERT INTO members (name, role) VALUES (%s, %s)", members)

    # Lấy member_id để thêm bản ghi tiến độ
    cursor.execute("SELECT member_id FROM members")
    member_ids = [row[0] for row in cursor.fetchall()]

    progress_data = [
        (member_ids[0], 1, 40.0, 5, "Làm backend API"),
        (member_ids[1], 1, 38.5, 4, "Kiểm thử module đăng nhập"),
        (member_ids[2], 1, 30.0, 3, "Quản lý team"),
        (member_ids[3], 1, 42.0, 6, "Xử lý giao diện người dùng"),
        (member_ids[4], 1, 36.0, 4, "Thiết kế UI trang chủ"),
        (member_ids[0], 2, 39.0, 6, "Tối ưu API"),
        (member_ids[1], 2, 37.0, 5, "Viết test case"),
        (member_ids[2], 2, 32.0, 3, "Họp khách hàng"),
        (member_ids[3], 2, 44.0, 7, "Cập nhật giao diện"),
        (member_ids[4], 2, 35.0, 4, "Thiết kế giao diện dashboard")
    ]

    cursor.executemany("""
                       INSERT INTO weekly_progress (member_id, week_number, hours_worked, tasks_completed, notes)
                       VALUES (%s, %s, %s, %s, %s)
                       """, progress_data)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Đã thêm dữ liệu thành viên và tiến độ.")


def query_progress(week_number):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    cursor.execute("USE Days9")

    query = """
            SELECT m.name, wp.hours_worked, wp.tasks_completed, wp.notes
            FROM weekly_progress wp
                     JOIN members m ON wp.member_id = m.member_id
            WHERE wp.week_number = %s
            ORDER BY wp.tasks_completed DESC LIMIT 5 \
            """
    cursor.execute(query, (week_number,))
    results = cursor.fetchall()

    print(f"\n📅 Tuần {week_number}:")
    for name, hours, tasks, note in results:
        print(f"- {name}: {hours} giờ, {tasks} nhiệm vụ, Ghi chú: {note}")

    cursor.close()
    conn.close()


def update_progress(progress_id, new_hours, new_notes):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    cursor.execute("USE Days9")

    cursor.execute("""
                   UPDATE weekly_progress
                   SET hours_worked = %s,
                       notes        = %s
                   WHERE progress_id = %s
                   """, (new_hours, new_notes, progress_id))

    conn.commit()
    print(f"✅ Đã cập nhật tiến độ ID {progress_id}.")
    cursor.close()
    conn.close()


def delete_progress(week_number):
    conn = connect_to_mysql()
    cursor = conn.cursor()
    cursor.execute("USE Days9")

    cursor.execute("SELECT COUNT(*) FROM weekly_progress WHERE week_number = %s", (week_number,))
    count = cursor.fetchone()[0]
    if count == 0:
        print(f"⚠️ Không có bản ghi nào cho tuần {week_number}.")
    else:
        cursor.execute("DELETE FROM weekly_progress WHERE week_number = %s", (week_number,))
        conn.commit()
        print(f"🗑️ Đã xóa {count} bản ghi tiến độ tuần {week_number}.")

    cursor.close()
    conn.close()


def generate_summary():
    conn = connect_to_mysql()
    cursor = conn.cursor()
    cursor.execute("USE Days9")

    cursor.execute("""
                   SELECT m.name, SUM(wp.hours_worked), SUM(wp.tasks_completed)
                   FROM weekly_progress wp
                            JOIN members m ON wp.member_id = m.member_id
                   GROUP BY m.name
                   """)

    results = cursor.fetchall()
    print("\n📊 Báo cáo tổng kết:")
    for name, total_hours, total_tasks in results:
        print(f"- {name}: Tổng {total_hours} giờ, {total_tasks} nhiệm vụ")

    cursor.close()
    conn.close()


def cleanup_database():
    conn = connect_to_mysql()
    cursor = conn.cursor()
    cursor.execute("USE Days9")

    cursor.execute("SHOW TABLES LIKE 'weekly_progress'")
    if cursor.fetchone():
        cursor.execute("DROP TABLE weekly_progress")
        conn.commit()
        print("🧹 Đã xóa bảng weekly_progress.")
    else:
        print("⚠️ Bảng weekly_progress không tồn tại.")

    cursor.close()
    conn.close()


def main():
    setup_database()
    add_data()
    query_progress(1)
    update_progress(1, 45.0, "Hoàn thành sớm")
    delete_progress(2)
    generate_summary()
    cleanup_database()


if __name__ == "__main__":
    main()
