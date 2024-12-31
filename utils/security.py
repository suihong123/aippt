from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import secrets

def hash_password(password):
    """使用 Werkzeug 的加密方法"""
    return generate_password_hash(password, method='pbkdf2:sha256:150000')

def verify_password(stored_hash, password):
    """验证密码"""
    return check_password_hash(stored_hash, password)

def generate_token():
    """生成安全的随机令牌"""
    return secrets.token_urlsafe(32)

def hash_file(file_data):
    """计算文件哈希值"""
    return hashlib.sha256(file_data).hexdigest() 