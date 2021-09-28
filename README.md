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
