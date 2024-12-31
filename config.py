# 应用配置
APP_CONFIG = {
    'DEBUG': False,
    'SECRET_KEY': 'your-secret-key',
    'BASE_URL': '/aippt/',  # GitHub Pages 项目路径
    'SESSION_TYPE': 'redis'
}

# Redis配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'password': None,
    'decode_responses': True
}

# 安全配置
SECURITY_CONFIG = {
    'PASSWORD_MIN_LENGTH': 8,
    'MAX_LOGIN_ATTEMPTS': 5,
    'LOGIN_TIMEOUT': 300,  # 5分钟
    'ALLOWED_ORIGINS': ['http://localhost:5000', 'https://yourdomain.com']
}

# API配置
API_CONFIG = {
    'base_url': 'https://api.docmee.cn',  # 使用外部API
    'endpoints': {
        'login': '/api/login',
        'register': '/api/register'
    }
}

# 邮件配置
MAIL_CONFIG = {
    'MAIL_SERVER': 'smtp.example.com',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USERNAME': 'your-email@example.com',
    'MAIL_PASSWORD': 'your-password'
}

# 文件路径配置
PATH_CONFIG = {
    'templates': 'templates',
    'static': 'static',
    'uploads': 'uploads'
}

# 用户相关路由
@app.route('/')
def index():
    if 'phone' in session:
        return redirect(url_for('main'))
    return render_template('login.html')

@app.route('/main')
def main():
    if 'phone' not in session:
        return redirect(url_for('index'))
    return render_template('main.html')

@app.route('/admin')
def admin():
    # 这里应该添加管理员验证
    return render_template('admin.html')

# API路由
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    phone = data.get('phone')
    nickname = data.get('nickname')
    
    if not phone or not nickname:
        return jsonify({
            'success': False,
            'message': '请输入手机号和昵称'
        })
    
    # 存储用户信息
    user_key = f"user:{phone}"
    user_data = {
        'phone': phone,
        'nickname': nickname,
        'create_time': datetime.now().timestamp()
    }
    
    redis_client.hmset(user_key, user_data)
    session['phone'] = phone
    
    return jsonify({
        'success': True,
        'message': '登录成功'
    })

@app.route('/api/activate', methods=['POST'])
def activate():
    if 'phone' not in session:
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
    code_key = f"code:{code}"
    code_data = redis_client.hgetall(code_key)
    
    if not code_data or code_data.get('used') == '1':
        return jsonify({
            'success': False,
            'message': '无效的激活码'
        })
    
    # 激活会员
    phone = session['phone']
    days = int(code_data.get('days', 30))
    user_key = f"user:{phone}"
    
    current_expire = redis_client.hget(user_key, 'vip_expire')
    if current_expire and float(current_expire) > datetime.now().timestamp():
        new_expire = datetime.fromtimestamp(float(current_expire)) + timedelta(days=days)
    else:
        new_expire = datetime.now() + timedelta(days=days)
    
    # 更新用户会员时间
    redis_client.hset(user_key, 'vip_expire', new_expire.timestamp())
    
    # 标记激活码已使用
    redis_client.hmset(code_key, {
        'used': '1',
        'used_by': phone,
        'used_time': datetime.now().timestamp()
    })
    
    return jsonify({
        'success': True,
        'data': {
            'expire_time': new_expire.strftime('%Y-%m-%d %H:%M:%S'),
            'days': days
        }
    })

@app.route('/api/user/status')
def user_status():
    if 'phone' not in session:
        return jsonify({
            'success': False,
            'message': '未登录'
        })
    
    phone = session['phone']
    user_key = f"user:{phone}"
    user_data = redis_client.hgetall(user_key)
    
    if not user_data:
        return jsonify({
            'success': False,
            'message': '用户不存在'
        })
    
    vip_expire = user_data.get('vip_expire')
    is_vip = False
    remaining_days = 0
    expire_time = None
    
    if vip_expire:
        expire_time = datetime.fromtimestamp(float(vip_expire))
        is_vip = expire_time > datetime.now()
        remaining_days = (expire_time - datetime.now()).days if is_vip else 0
    
    return jsonify({
        'success': True,
        'data': {
            'nickname': user_data['nickname'],
            'phone': user_data['phone'],
            'is_vip': is_vip,
            'remaining_days': remaining_days,
            'expire_time': expire_time.strftime('%Y-%m-%d %H:%M:%S') if expire_time else None
        }
    })

# 管理员接口
@app.route('/api/admin/generate-code', methods=['POST'])
def generate_code():
    # 这里应该添加管理员验证
    days = request.json.get('days', 30)
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    code_key = f"code:{code}"
    redis_client.hmset(code_key, {
        'code': code,
        'days': days,
        'used': '0',
        'create_time': datetime.now().timestamp()
    })
    
    return jsonify({
        'success': True,
        'data': {
            'code': code,
            'days': days
        }
    })

if __name__ == '__main__':
    app.run(debug=True)