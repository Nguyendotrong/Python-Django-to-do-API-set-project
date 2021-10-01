# Python-Django-to-do-API-set-project
Project xây dựng các API quản lý các công việc cần làm, viết bằng công nghệ Django Rest API.
(Đã băm mật khẩu trước khi lưu xuống Database) 

# I. Cách deploy source code:
  - Cài đặt môi trường venv cho project
  - Cài đặt các thư viện được liệt kê trong tập tin requipment.txt (sữ dụng lệnh pip install -r requirement.txt)

# II. Kết nối database.
  - Trong mysql tạo database tên todoprojectdb
  - Cần trỏ đường dẫn terminal vào trong thư mục todoproject để chạy server thông qua tập tin manage.py
  - chỉ định lại user và password để đăng nhập vào database của Mysql cho project thông qua biến DATABASES trong tập tin setting.py
  - Trong màn hình terminal của IDE, thực thi lệnh sau để migrate database: python manage.py migrate
   -> Bây giờ ta có thể chạy project

# III.  Danh các tiếp đầu ngữ url tương ứng cho các Api
  **Lưu ý 1**: Ngoại trừ API đăng ký user, các API còn lại phải chứng thực user khi thực thi (truyền Bearer token và chuỗi access token cho đối số Authorization) như sau:
      Bearer "chuỗi access token"
      ![image](https://user-images.githubusercontent.com/52287665/135322157-ecb75f4c-8df8-455f-8145-a39a3f2a3caa.png)
      
   **Lưu ý 2**: cần migrate trước khi chạy server để cập nhật database phòng trường hợp database thay đổi (dùng lệnh python manage.py migrate).
   
  ## 1.  /accounts/    (method="GET") 
      - Lấy tất cả user.
  ## 2.  /accounts/sign-up/ (method="POST") 
      - Đăng ký user.
      - body: 
        + username: str (đối số bắt buộc)
        + password: str (đối số bắt buộc)
        + first_name: str
        + last_name:str
        + email: str
  
  ## 3.  accounts/sign-in/        (method="POST")                 
      - Đăng nhập (Trả về chuổi access và refresh)
      - Body:
       + username: str (đối số bắt buộc)
       + password: str (đối số bắt buộc)
    
  ## 4.  /tasks/     (method="GET")        
     - Lấy danh sách tất cả to-do.
    
  ## 5.  /tasks/     (method="POST")       
     - Tạo một to-do.
     - Body: 
       + name: str                 (đối số bắt buộc)
       + description: str          (đối số bắt buộc)
       + user: int                  (đối số bắt buộc)
       + date_of_completion: datetime, format(yyyy-MM-DD hh:mm:ss), Lưu ý: date_of_completion phải lớn hơn ngày tạo task(mặc định là ngày hiện tại)  (đối số bắt buộc)
        
  ##  6.  /tasks/{id}  (method="GET")  
      - Xem chi tiết một to-do.
      
  ## 7.  /tasks/{id}   (method="PATCH")    
      - Cập nhật một to-do.
      - Body: 
       + name: str                 
       + description: str          
       + user: int        (id của user cần phân task)                
       + date_of_completion: datetime, format(yyyy-MM-DD hh:mm:ss), Lưu ý: date_of_completion phải lớn hơn ngày tạo task(mặc định là ngày hiện tại)
       + status: int, ( truyền 0 hoặc 1. 0 tương ứng là new, 1 tương ứng complete.)
       
  ## 8.  /tasks/{id}   (method="DELETE")   
     - Xóa một to-do.
     
  ## 9.  /tasks/{id}/assign-to-to/         (method="POST") 
     - Phân lại một to-do cho user khác. 
     - Body:
      + user: int (id của user cần phân task)
