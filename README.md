# Python-Django-to-do-API-set-project
Project xây dựng các API quản lý các công việc cần làm, viết bằng công nghệ Django Rest API.

I. Cách deploy source code:
- Cài đặt môi trường venv cho project
- Cài đặt các thư viện được liệt kê trong tập tin requipment.txt (sữ dụng lệnh pip install -r requirement.txt)

II. Kết nối database.
- Trong mysql tạo database tên todoprojectdb
- Cần trỏ đường dẫn terminal vào trong thư mục todoproject để chạy server thông qua tập tin manage.py
- chỉ định lại user và password để đăng nhập vào database của Mysql cho project thông qua biến DATABASES trong tập tin setting.py
- Trong màn hình terminal của IDE, thực thi lệnh sau để migrate database: python manage.py migrate
  -> Bây giờ ta có thể chạy project

III.  Danh các tiếp đầu ngữ url tương ứng cho các Api
  1.  /accounts/                        - Lấy tất cả user.
  2.  /acounts/sign-up/ (method="POST") - Đăng ký user.
  3.  /sign-in/                         - Đăng nhập (Trả về chuổi access và refresh)
  4.  /tasks/     (method="GET")        - Lấy danh sách tất cả to-do.
  5.  /tasks/     (method="POST")       - Tạo một to-do.
  6.  /tasks/{id}  (method="GET")       - Xem chi tiết một to-do.
  7.  /tasks/{id}   (method="PATCH")    - Cập nhật một to-do.
  8.  /tasks/{id}   (method="DELETE")   - Xóa một to-do.
  9.  /tasks/{id}/assign-to-to/         - Phân lại một to-do cho user khác. 
