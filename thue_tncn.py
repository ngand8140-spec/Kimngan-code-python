import os

DATA_FILE = "D:/Python/tax_data.txt"

# Biểu thuế lũy tiến từng phần
TAX_BRACKETS = [
    (5_000_000, 0.05),
    (10_000_000, 0.10),
    (18_000_000, 0.15),
    (32_000_000, 0.20),
    (52_000_000, 0.25),
    (80_000_000, 0.30),
    (float('inf'), 0.35)
]

DEDUCTION_SELF = 11_000_000       # Giảm trừ bản thân: 11 triệu/tháng
DEDUCTION_DEPENDENT = 4_400_000  # Giảm trừ người phụ thuộc: 4.4 triệu/người/tháng


def calculate_tax_details(income: float, dependents: int):
    """Tính toán các khoản giảm trừ, thu nhập tính thuế và thuế phải nộp."""
    total_deduction = DEDUCTION_SELF + (dependents * DEDUCTION_DEPENDENT)
    taxable_income = income - total_deduction
    
    if taxable_income <= 0:
        taxable_income = 0.0
        tax = 0.0
    else:
        tax = 0.0
        prev_limit = 0
        for limit, rate in TAX_BRACKETS:
            if taxable_income > limit:
                tax += (limit - prev_limit) * rate
                prev_limit = limit
            else:
                tax += (taxable_income - prev_limit) * rate
                break
                
    return total_deduction, taxable_income, tax


def validate_input_number(prompt: str, is_int: bool = False):
    """Kiểm tra dữ liệu đầu vào không âm và đúng kiểu."""
    while True:
        try:
            val_str = input(prompt).strip()
            if not val_str:
                print(">> Lỗi: Thông tin bắt buộc không được bỏ trống!")
                continue
            val = int(val_str) if is_int else float(val_str)
            if val < 0:
                print(">> Lỗi: Giá trị không được là số âm!")
                continue
            return val
        except ValueError:
            print(">> Lỗi: Nhập sai kiểu dữ liệu số! Vui lòng nhập lại.")


# 1. Quản lý dữ liệu
def add_record(records: list):
    print("\n--- 1. THÊM BẢN GHI MỚI ---")
    while True:
        emp_id = input("Nhập mã người lao động: ").strip()
        if not emp_id:
            print(">> Lỗi: Mã người lao động không được bỏ trống!")
            continue
        if any(r['id'] == emp_id for r in records):
            print(">> Lỗi: Mã người lao động đã bị trùng!")
            continue
        break
        
    while True:
        name = input("Nhập họ tên: ").strip()
        if name:
            break
        print(">> Lỗi: Họ tên không được bỏ trống!")
        
    income = validate_input_number("Nhập thu nhập (VNĐ): ")
    dependents = validate_input_number("Nhập số người phụ thuộc: ", is_int=True)
    
    deduction, taxable_income, tax = calculate_tax_details(income, dependents)
    
    record = {
        'id': emp_id,
        'name': name,
        'income': income,
        'dependents': dependents,
        'deduction': deduction,
        'taxable_income': taxable_income,
        'tax': tax
    }
    records.append(record)
    print(">> Thêm bản ghi mới thành công!")


def show_records(records: list):
    print("\n--- 2. HIỂN THỊ DANH SÁCH TÍNH THUẾ ---")
    if not records:
        print(">> Danh sách hiện đang trống.")
        return
    
    print(f"{'Mã NLĐ':<10} | {'Họ tên':<20} | {'Thu nhập':<15} | {'NPT':<5} | {'Giảm trừ':<15} | {'TN Tính thuế':<15} | {'Thuế phải nộp':<15}")
    print("-" * 105)
    for r in records:
        print(f"{r['id']:<10} | {r['name']:<20} | {r['income']:>15,.0f} | {r['dependents']:<5} | {r['deduction']:>15,.0f} | {r['taxable_income']:>15,.0f} | {r['tax']:>15,.0f}")


def update_record(records: list):
    print("\n--- 3. CẬP NHẬT THÔNG TIN ---")
    emp_id = input("Nhập mã người lao động cần cập nhật: ").strip()
    for r in records:
        if r['id'] == emp_id:
            print(f"Đang sửa thông tin người lao động: {r['name']}")
            new_name = input(f"Họ tên mới ({r['name']}): ").strip()
            if new_name:
                r['name'] = new_name
                
            inc_str = input(f"Thu nhập mới ({r['income']:,.0f}): ").strip()
            if inc_str:
                try:
                    inc = float(inc_str)
                    if inc >= 0:
                        r['income'] = inc
                    else:
                        print(">> Giá trị âm không hợp lệ, giữ nguyên thu nhập cũ.")
                except ValueError:
                    print(">> Định dạng sai, giữ nguyên thu nhập cũ.")
                    
            dep_str = input(f"Số người phụ thuộc mới ({r['dependents']}): ").strip()
            if dep_str:
                try:
                    dep = int(dep_str)
                    if dep >= 0:
                        r['dependents'] = dep
                    else:
                        print(">> Giá trị âm không hợp lệ, giữ nguyên NPT cũ.")
                except ValueError:
                    print(">> Định dạng sai, giữ nguyên NPT cũ.")
                    
            r['deduction'], r['taxable_income'], r['tax'] = calculate_tax_details(r['income'], r['dependents'])
            print(">> Cập nhật thông tin thành công!")
            return
    print(">> Không tìm thấy người lao động với mã đã nhập.")


def delete_record(records: list):
    print("\n--- 4. XÓA BẢN GHI ---")
    emp_id = input("Nhập mã người lao động cần xóa: ").strip()
    for i, r in enumerate(records):
        if r['id'] == emp_id:
            confirm = input(f"Bạn có chắc chắn muốn xóa bản ghi của '{r['name']}'? (y/n): ").strip().lower()
            if confirm == 'y':
                records.pop(i)
                print(">> Đã xóa bản ghi thành công.")
            else:
                print(">> Hủy thao tác xóa.")
            return
    print(">> Không tìm thấy người lao động với mã đã nhập.")


# 2. Tìm kiếm
def search_records(records: list):
    print("\n--- 5. TÌM KIẾM BẢN GHI ---")
    print("1. Tìm kiếm theo Mã người lao động")
    print("2. Tìm kiếm theo Họ tên")
    print("3. Tìm kiếm theo Mức thu nhập (>= Mức nhập vào)")
    choice = input("Chọn tiêu chí tìm kiếm (1-3): ").strip()
    
    results = []
    if choice == '1':
        kw = input("Nhập mã NLĐ cần tìm: ").strip().lower()
        results = [r for r in records if kw in r['id'].lower()]
    elif choice == '2':
        kw = input("Nhập tên cần tìm: ").strip().lower()
        results = [r for r in records if kw in r['name'].lower()]
    elif choice == '3':
        min_inc = validate_input_number("Nhập mức thu nhập tối thiểu: ")
        results = [r for r in records if r['income'] >= min_inc]
    else:
        print(">> Lựa chọn không hợp lệ.")
        return
        
    if results:
        print(f"\n[KẾT QUẢ TÌM KIẾM - Tìm thấy {len(results)} bản ghi]")
        show_records(results)
    else:
        print(">> Không tìm thấy bản ghi nào phù hợp với yêu cầu.")


# 3. Sắp xếp
def sort_records(records: list):
    print("\n--- 6. SẮP XẾP DANH SÁCH ---")
    print("1. Sắp xếp theo Thu nhập")
    print("2. Sắp xếp theo Thuế phải nộp")
    opt = input("Chọn tiêu chí (1-2): ").strip()
    
    print("a. Tăng dần")
    print("b. Giảm dần")
    order = input("Chọn thứ tự (a/b): ").strip().lower()
    
    is_reverse = True if order == 'b' else False
    
    if opt == '1':
        records.sort(key=lambda x: x['income'], reverse=is_reverse)
        print(">> Đã sắp xếp theo Thu nhập!")
    elif opt == '2':
        records.sort(key=lambda x: x['tax'], reverse=is_reverse)
        print(">> Đã sắp xếp theo Thuế phải nộp!")
    else:
        print(">> Lựa chọn không hợp lệ.")
        return
    show_records(records)


# 4. Tính toán và Thống kê
def statistics(records: list):
    print("\n--- 7. TÍNH TOÁN VÀ THỐNG KÊ ---")
    if not records:
        print(">> Không có dữ liệu để thống kê.")
        return
        
    total_income = sum(r['income'] for r in records)
    total_tax = sum(r['tax'] for r in records)
    
    max_income_person = max(records, key=lambda x: x['income'])
    max_tax_person = max(records, key=lambda x: x['tax'])
    
    no_tax_count = sum(1 for r in records if r['tax'] == 0)
    
    # Thống kê theo nhóm thu nhập
    group_under_11 = sum(1 for r in records if r['income'] <= 11_000_000)
    group_11_to_30 = sum(1 for r in records if 11_000_000 < r['income'] <= 30_000_000)
    group_over_30  = sum(1 for r in records if r['income'] > 30_000_000)
    
    print(f"- Tổng số người lao động  : {len(records)}")
    print(f"- Tổng thu nhập           : {total_income:,.0f} VNĐ")
    print(f"- Tổng thuế thu được      : {total_tax:,.0f} VNĐ")
    print(f"- Người có Thu nhập cao nhất: {max_income_person['name']} ({max_income_person['income']:,.0f} VNĐ)")
    print(f"- Người nộp Thuế cao nhất  : {max_tax_person['name']} ({max_tax_person['tax']:,.0f} VNĐ)")
    print(f"- Số người không phát sinh thuế: {no_tax_count} người")
    print("\n* Thống kê theo nhóm thu nhập:")
    print(f"  + Dưới hoặc bằng 11 triệu  : {group_under_11} người")
    print(f"  + Từ 11 đến 30 triệu       : {group_11_to_30} người")
    print(f"  + Trên 30 triệu            : {group_over_30} người")


# 5. Lưu và Đọc dữ liệu File TXT
def save_file(records: list):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            for r in records:
                line = f"{r['id']}|{r['name']}|{r['income']}|{r['dependents']}|{r['deduction']}|{r['taxable_income']}|{r['tax']}\n"
                f.write(line)
        print(">> Đã lưu danh sách xuống file TXT thành công!")
    except Exception as e:
        print(f">> Lỗi khi lưu file: {e}")


def load_file() -> list:
    records = []
    if not os.path.exists(DATA_FILE):
        return records
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 7:
                    record = {
                        'id': parts[0],
                        'name': parts[1],
                        'income': float(parts[2]),
                        'dependents': int(parts[3]),
                        'deduction': float(parts[4]),
                        'taxable_income': float(parts[5]),
                        'tax': float(parts[6])
                    }
                    records.append(record)
        print(">> Đã đọc dữ liệu từ file TXT thành công!")
    except Exception as e:
        print(f">> Lỗi khi đọc file TXT: {e}")
    return records


# Menu điều khiển Console
def main():
    records = load_file()
    while True:
        print("\n=========================================")
        print("  CHƯƠNG TRÌNH TÍNH THUẾ THU NHẬP CÁ NHÂN")
        print("=========================================")
        print("1. Thêm bản ghi mới")
        print("2. Hiển thị toàn bộ danh sách")
        print("3. Cập nhật thông tin")
        print("4. Xóa bản ghi")
        print("5. Tìm kiếm")
        print("6. Sắp xếp")
        print("7. Tính toán / Thống kê")
        print("8. Lưu dữ liệu ra file TXT")
        print("9. Đọc dữ liệu từ file TXT")
        print("0. Thoát")
        print("=========================================")
        choice = input("Lựa chọn chức năng (0-9): ").strip()
        
        if choice == '1':
            add_record(records)
        elif choice == '2':
            show_records(records)
        elif choice == '3':
            update_record(records)
        elif choice == '4':
            delete_record(records)
        elif choice == '5':
            search_records(records)
        elif choice == '6':
            sort_records(records)
        elif choice == '7':
            statistics(records)
        elif choice == '8':
            save_file(records)
        elif choice == '9':
            records = load_file()
        elif choice == '0':
            save_file(records)
            print(">> Đã lưu dữ liệu. Tạm biệt!")
            break
        else:
            print(">> Lựa chọn không hợp lệ, vui lòng chọn lại.")

if __name__ == "__main__":
    main()
