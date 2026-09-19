# File này để chạy WEB PANEL trên Vercel (chỉ giao diện, không chạy bot nhạc 24/7)
# Vercel không chạy được discord bot voice lâu dài
from flask import Flask, render_template, request, jsonify
import os
import sys
# Thêm thư mục gốc vào path để import template
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def status():
    return jsonify({
        "running": False,
        "msg": "Bạn đang chạy trên Vercel - Vercel chỉ host được giao diện web, không host được bot nhạc 24/7. Hãy host bot.py trên Render/Railway (xem README)"
    })

@app.route('/api/start', methods=['POST'])
def start():
    return jsonify({
        "success": False,
        "msg": "⚠️ Vercel không thể chạy bot Discord 24/7. Vui lòng đọc README.md để host bot.py trên Render.com (free)"
    })

# Vercel sẽ gọi app này
# app = app
