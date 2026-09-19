# HƯỚNG DẪN UP LÊN VERCEL

## File này để làm gì?
- vercel.json: File cấu hình bắt buộc để Vercel hiểu đây là Python project
- api/index.py: File chính để Vercel chạy (Vercel chỉ chạy file trong thư mục api/)
- templates/index.html: Giao diện web

## Cách up lên Vercel (chỉ được giao diện web):

1. Tạo tài khoản vercel.com
2. Up code này lên GitHub (tạo repo mới, upload hết file)
3. Vào Vercel -> Add New Project -> Import repo vừa tạo
4. Vercel sẽ tự phát hiện Python, bấm Deploy
5. Xong! Bạn sẽ có link web https://ten-ban.vercel.app

## NHƯNG QUAN TRỌNG:
Vercel KHÔNG chạy được bot.py (bot nhạc) vì:
- Vercel tắt function sau 10 giây
- Không có ffmpeg
- Không giữ kết nối voice Discord

=> Web trên Vercel chỉ là giao diện demo.

## Để BOT NHẠC CHẠY 24/7 THẬT (FREE):

### Cách 1: Render.com (khuyên dùng nhất, free)
1. Vào render.com -> New + -> Background Worker
2. Connect GitHub repo này
3. 
   Name: discord-music-bot
   Language: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python bot.py
4. Vào Environment -> Add: DISCORD_TOKEN = token bot của bạn
5. Create Worker -> Bot sẽ online 24/7

### Cách 2: Railway.app (free $5/tháng)
Tương tự Render, chọn Start Command: python bot.py

### Cách 3: Chạy trên máy bạn (24/7 cần treo máy)
pip install -r requirements.txt
python bot.py

## Lệnh bot:
!join - vào kênh thoại
!play <link youtube hoặc tên bài>
!stop - thoát
