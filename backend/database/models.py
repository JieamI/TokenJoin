from sqlalchemy import Column, Boolean, String, Integer, Enum, ForeignKey, DateTime, Text, event
from sqlalchemy.orm import relationship
import datetime
from . import Base

def set_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key = True)
    Nick = Column(String(160))
    Openid = Column(String(160), unique = True, nullable = False, index = True)
    Department_name = Column(Enum(
        '技术部', '设计部', '产品部', '产品运营', '新媒体运营', '人力资源部', '杂志部'
        ), 
        ForeignKey('department.Name'), 
        nullable = False)
    Authorized = Column(Boolean, default = False)
    Department = relationship('Department')

# 存储部门状态信息，包含部门是否处于展示状态以及部门内管理员的操作记录，其中操作记录反向引用于Record表
class Department(Base):
    __tablename__ = 'department'

    Name = Column(Enum(
        '技术部', '设计部', '产品部', '产品运营', '新媒体运营', '人力资源部', '杂志部'
        ), 
        nullable = False, 
        unique = True, 
        primary_key = True)
    Show = Column(Boolean, default = True)
    Message = Column(String(160), server_default = '[]')

# 管理员操作记录，用于记录管理员同意拒绝申请，更改面试状态，及发送邮件等操作
class Record(Base):
    __tablename__ = 'record'

    id = Column(Integer, primary_key = True)
    Owner = Column(Enum(
        '技术部', '设计部', '产品部', '产品运营', '新媒体运营', '人力资源部', '杂志部'
        ), 
        ForeignKey('department.Name'), 
        nullable = False, index = True)
    Operator = Column(String(160))
    Operation = Column(String(160))
    Time = Column(String(160), default = set_time)

    # 通过类属性规定查询对象以时间降序
    __mapper_args__ = {
        "order_by": Time.desc()
    }
    # 作为Department表的反向引用
    Department = relationship('Department', backref = 'Record')

# 简历投递信息
class CVinfo(Base):
    __tablename__ = 'cvinfo'

    sno = Column(
        String(64), 
        unique = True, 
        primary_key = True, 
        index = True, 
        nullable = False)
    department = Column(Enum(
        '技术部', '设计部', '产品部', '产品运营', '新媒体运营', '人力资源部', '杂志部'
        ), 
        ForeignKey('department.Name'),
        primary_key = True, 
        nullable = False)
    sign = Column(Boolean, default = False)
    state = Column(Enum('未审核', '简历通过', '笔试完成', '面试完成', '已录取', '未录取'), default = '未审核')
    name = Column(String(160))
    sex = Column(Enum('男', '女'))
    birthday = Column(String(160))
    hometown = Column(String(160))
    nation = Column(String(160))
    college = Column(String(160))
    grade = Column(String(160))
    proclass = Column(String(160))
    dormitory = Column(String(160))
    phone = Column(String(160))
    qq = Column(String(160))
    mail = Column(String(160))
    experience = Column(Text)
    introduce = Column(Text)
    reason = Column(Text)
    comment = Column(Text)
    time = Column(String(160), default = set_time)
       
    # 通过类属性规定查询对象以时间降序
    __mapper_args__ = {
        "order_by": time.desc()
    }
    # 作为Department表的反向引用
    Department = relationship('Department', backref = 'CVinfo')

# 创建数据库后初始化Department数据    
def init_data(target, connection, **kw):
    depts = ['技术部', '设计部', '产品部', '产品运营', '新媒体运营', '人力资源部', '杂志部']
    for dept in depts:
        connection.execute(target.insert(), {'Name': dept})

event.listen(Department.__table__, 'after_create', init_data)   