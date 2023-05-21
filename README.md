# fb-crawler
Simple facebook crawler tool
# Setting

## cài wsl
- Mở window terminal
- wsl --install -d ubuntu-22.04
- restart lại máy (nếu cài wsl lần đầu)
- tìm kiếm và mở ubuntu 22.04 LTS lên
- Khởi tạo username và password

## cài môi trường
- sudo apt update && sudo apt upgrade
- sudo apt install python3-pip
- git clone https://github.com/l0ngnguyen/fb-crawler.git
- pip install -r fb-crawler/requirements.txt


# Cách chạy và lấy dữ liệu
## chạy
- cd ~/fb-crawler
- python3 main.py
- Login facebook bằng cách nhập username và password (chỉ cần nhập lần đầu, lần sau không cần nhập)
## Nhập các thông số cài đặt
- Input search text: <từ khóa tìm kiếm>
- Input search location: <khu vực tìm kiếm>
- Input download delay: <delay giữa các thao tác, thường để 3 hoặc 4>
- Input Number of threads: <số nhân cpu thực hiện (càng nhiều càng nhanh)>
- Input output file path: <đường dẫn đến file đầu ra>