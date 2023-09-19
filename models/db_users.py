import hashlib
import re
import secrets
import string

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from pydantic import BaseModel, constr, validator
from models.database import BaseDB


# 创建用户表模型
class UserTableMode(BaseDB):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True, index=True, default=lambda: UserFunction().generate_random_uid())
    name = Column(String)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    userRole = Column(Integer, default=0)  # 用户权限 0默认为普通用户，1为管理员
    accountStatus = Column(Integer, default=1)  # 用户状态,0 代表禁用，1为启用
    registrationDate = Column(DateTime, default=datetime.utcnow)  # 注册日期


# 用户数据模型
class UserDateMode(BaseModel):
    name: constr(max_length=8, min_length=3)
    username: constr(max_length=12, min_length=6)
    password: constr(max_length=32, min_length=8) = None
    md5password: str = None
    email: constr(max_length=32)

    @validator('password')
    def check_password(cls, value):
        # 验证密码复杂性
        if not re.search(r'[A-Z]', value):  # 包含大写字母
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):  # 包含小写字母
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'\d', value):  # 包含数字
            raise ValueError("Password must contain at least one digit")
        return value

    @validator('email')
    # 验证邮箱格式
    def check_email(cls, value):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise ValueError("Email must error")
        return value

    @validator('md5password', pre=True, always=True)
    def create_md5_password(cls, value, values):
        password = values.get('password')
        if password:
            md5_password = hashlib.md5(password.encode('utf-8')).hexdigest()
            return md5_password
        if not value:
            raise ValueError("密码不能为空")
        return value

class UserFunction():

    def __init__(self):
        from models.database import SessionLocal
        self.db = SessionLocal()

    def __del__(self):
        self.db.close()

    # 生成随机 6 位数的 UID
    def generate_random_uid(self):
        characters = string.digits  # 使用数字字符
        while True:
            random_uid = ''.join(secrets.choice(characters) for i in range(6))
            if not self.db.query(UserTableMode).filter(UserTableMode.uid == random_uid).first():
                return random_uid

    def cheak_db_username(self, new_username):
        if self.db.query(UserTableMode).filter(UserTableMode.username == new_username).first():
            return False
        return True

    def cheak_db_email(self, new_email):
        if self.db.query(UserTableMode).filter(UserTableMode.email == new_email).first():
            return False
        return True

    # 用户注册
    def add_db_user(self, data):
        try:
            new_data = UserTableMode(
                name=data['name'],
                username=data['username'],
                password=data['md5password'],
                email=data['email']
            )
            if not self.cheak_db_username(data['username']):
                return {"message": "User add Info", "code": 401, "info": "用户名已存在"}
            if not self.cheak_db_email(data['email']):
                return {"message": "User add Info", "code": 402, "info": "邮箱已存在"}
            self.db.add(new_data)
            self.db.commit()
            return {"message": "User add Info", "code": 200, "info": "注册成功"}
        except Exception as e:
            self.db.rollback()
            return {"message": "User add Info", "code": 400, "info": "注册失败"}
        finally:
            self.db.close()

    # 登陆

    # 删除用户

    # 修改用户

    # 查询用户