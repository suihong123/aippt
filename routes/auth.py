from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, Response
from datetime import datetime, timedelta
from config import SECURITY_CONFIG
from io import BytesIO
import random
from PIL import Image, ImageDraw, ImageFont

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login_page():
    if 'user_id' in session:
        return redirect(url_for('main.index'))
    return render_template('login.html')

@auth_bp.route('/register')
def register_page():
    return render_template('register.html')

@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.form
    captcha = data.get('captcha', '').upper()
    
    # 验证码检查
    if captcha != session.get('captcha'):
        return jsonify({
            'success': False,
            'message': '验证码错误'
        })
    
    # 清除验证码
    session.pop('captcha', None)
    
    username = data.get('username')
    password = data.get('password')
    
    # 验证用户
    user = redis_client.hgetall(f"user:{username}")
    if not user or user['password'] != password:  # 实际应使用加密密码
        return jsonify({
            'success': False,
            'message': '用户名或密码错误'
        })
    
    session['user_id'] = username
    return jsonify({
        'success': True,
        'message': '登录成功'
    })

@auth_bp.route('/api/activate', methods=['POST'])
def activate():
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': '请先登录'
        })
    
    code = request.json.get('code')
    if not code:
        return jsonify({
            'success': False,
            'message': '请输入激活码'
        })
    
    # 验证激活码
    code_data = redis_client.hgetall(f"code:{code}")
    if not code_data or code_data.get('used') == '1':
        return jsonify({
            'success': False,
            'message': '无效的激活码'
        })
    
    # 激活用户
    user_id = session['user_id']
    days = int(code_data.get('days', 30))
    uses = int(code_data.get('uses', 100))
    
    user_key = f"user:{user_id}"
    current_expire = redis_client.hget(user_key, 'expire_time')
    current_uses = int(redis_client.hget(user_key, 'remaining_uses') or 0)
    
    # 更新到期时间
    if current_expire and float(current_expire) > datetime.now().timestamp():
        new_expire = datetime.fromtimestamp(float(current_expire)) + timedelta(days=days)
    else:
        new_expire = datetime.now() + timedelta(days=days)
    
    # 更新用户信息
    redis_client.hmset(user_key, {
        'expire_time': new_expire.timestamp(),
        'remaining_uses': current_uses + uses
    })
    
    # 标记激活码已使用
    redis_client.hmset(f"code:{code}", {
        'used': '1',
        'used_by': user_id,
        'used_time': datetime.now().timestamp()
    })
    
    return jsonify({
        'success': True,
        'data': {
            'expire_time': new_expire.strftime('%Y-%m-%d %H:%M:%S'),
            'remaining_uses': current_uses + uses
        }
    }) 

@auth_bp.route('/api/captcha')
def get_captcha():
    # 生成随机验证码
    chars = ''.join(random.choices('23456789ABCDEFGHJKLMNPQRSTUVWXYZ', k=4))
    
    # 创建图片
    width = 120
    height = 38
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # 添加干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill='#ddd')
    
    # 添加文字
    font = ImageFont.truetype('arial.ttf', 28)
    for i, char in enumerate(chars):
        x = 15 + i * 23
        y = random.randint(2, 8)
        draw.text((x, y), char, font=font, fill='#333')
    
    # 保存验证码到session
    session['captcha'] = chars
    
    # 返回图片
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return Response(buffer.getvalue(), mimetype='image/png') 