from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 连接MYSQL
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:@:3306/smart_elderly_care_db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=True)

# 创建基本的映射类
Base = declarative_base(name='Base')


