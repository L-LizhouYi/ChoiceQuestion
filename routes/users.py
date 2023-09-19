from fastapi import APIRouter
from models.db_users import UserDateMode,UserTableMode

user_router = APIRouter()

# 检查用户名可用
@user_router.get("/users/checkName/{user_name}")
def check_user_name(user_name: str):
    return user_name

# 检查邮箱是否可用
@user_router.get("/users/checkEmail/{user_email}")
def check_user_email(user_email: str):
    return user_email

# 提交注册
@user_router.post("/users/register")
def register_user(user: UserDateMode):
    print(user.dict())
    from models.db_users import UserFunction
    return UserFunction().add_db_user(user.dict())



# 注册 登陆 注销 续签JWT