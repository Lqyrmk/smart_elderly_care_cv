from sqlalchemy import Column, String, Integer
from utils.mysql_utils.database import Base


class Elderly(Base):
    # 表名
    __tablename__ = 'elderly'
    # 表结构
    elderly_id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='老人id')
    elderly_name = Column(String(45), nullable=False, comment='老人姓名')
    gender = Column(String(45), comment='性别')
    phone = Column(String(45), comment='电话')
    id_card = Column(String(45), comment='身份证号')
    birthday = Column(String(45), comment='出生日期')
    checkin_date = Column(String(45), comment='入养老院日期')
    checkout_date = Column(String(45), comment='离开养老院日期')
    imgset_dir = Column(String(45), comment='图像目录')
    profile_photo = Column(String(45), comment='头像路径')
    room_number = Column(String(45), comment='房间号')
    first_guardian_name = Column(String(45), comment='第一监护人姓名')
    first_guardian_relationship = Column(String(45), comment='与第一监护人关系')
    first_guardian_phone = Column(String(45), comment='第一监护人电话')
    first_guardian_wechat = Column(String(45), comment='第一监护人微信')
    second_guardian_name = Column(String(45), comment='第二监护人姓名')
    second_guardian_relationship = Column(String(45), comment='与第二监护人关系')
    second_guardian_phone = Column(String(45), comment='第二监护人电话')
    second_guardian_wechat = Column(String(45), comment='第二监护人微信')
    health_state = Column(String(45), comment='健康状况')

class Employee(Base):
    # 表名
    __tablename__ = 'employee'
    # 表结构
    employee_id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='工作人员id')
    employee_name = Column(String(45), nullable=False, comment='工作人员姓名')
    gender = Column(String(45), comment='性别')
    phone = Column(String(45), comment='电话')
    id_card = Column(String(45), comment='身份证号')
    birthday = Column(String(45), comment='出生日期')
    checkin_date = Column(String(45), comment='访问日期')
    checkout_date = Column(String(45), comment='离开日期')
    imgset_dir = Column(String(45), comment='图像目录')
    profile_photo = Column(String(45), comment='头像路径')

class Volunteer(Base):
    # 表名
    __tablename__ = 'volunteer'
    # 表结构
    volunteer_id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='义工id')
    volunteer_name = Column(String(45), nullable=False, comment='义工姓名')
    gender = Column(String(45), comment='性别')
    phone = Column(String(45), comment='电话')
    id_card = Column(String(45), comment='身份证号')
    birthday = Column(String(45), comment='出生日期')
    checkin_date = Column(String(45), comment='访问日期')
    checkout_date = Column(String(45), comment='离开日期')
    imgset_dir = Column(String(45), comment='图像目录')
    profile_photo = Column(String(45), comment='头像路径')

class Event(Base):
    # 表名
    __tablename__ = 'event'
    # 表结构
    event_id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='事件id')
    event_type = Column(Integer, comment='事件类型')
    event_date = Column(String(45), comment='事件发生的时间')
    event_location = Column(String(45), comment='事件发生的地点')
    event_desc = Column(String(45), comment='事件描述')
    elderly_id = Column(Integer, comment='老人id：和老人信息表的id关联')

    def __init__(self, event_type, event_date, event_location, event_desc, elderly_id):
        self.event_type = event_type
        self.event_date = event_date
        self.event_location = event_location
        self.event_desc = event_desc
        self.elderly_id = elderly_id

class Algorithm(Base):
    # 表名
    __tablename__ = 'algorithm'
    # 表结构
    algorithm_id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='算法id')
    algorithm_name = Column(String(32), comment='算法类型')

class Camera(Base):
    # 表名
    __tablename__ = 'camera'
    # 表结构
    camera_id = Column(Integer, primary_key=True, index=True, autoincrement=True, comment='摄像头id')
    camera_name = Column(String(32), comment='摄像头名')
    stream_address = Column(String(32), comment='流地址')
