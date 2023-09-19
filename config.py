# Sqlite3 DB Config
from models.database import BaseDB,engine,SessionLocal
from models.db_users import UserTableMode
import hashlib


if __name__ == '__main__':
    BaseDB.metadata.create_all(bind=engine)
    db = SessionLocal()

    new_user = UserTableMode(
        name="刘浪",
        username="liulang",
        password=hashlib.md5("Ljt20021128.".encode('utf-8')).hexdigest(),
        email="liulang@example.com",
        userRole = 1
    )

    # 添加用户记录到数据库
    db.add(new_user)
    db.commit()

    # 关闭会话
    db.close()