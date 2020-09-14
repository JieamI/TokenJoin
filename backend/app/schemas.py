from pydantic import BaseModel
from typing import List, Optional


# 规范钉钉登录授权码数据类型
class Authcode(BaseModel):
    code: str

# 声明前端权限设定中的用户信息规范
class Setting_param(BaseModel):
    Nick: str
    Openid: str
    Department_name: str
    
# 声明返回给前端的管理员列表数据和申请列表数据规范
class Table_data(BaseModel):
    Nick: str
    Openid: str
    Department_name: str
    class Config:
        orm_mode = True

# 声明部门的操作记录数据规范
class Record(BaseModel):
    Operator: str
    Operation: str
    Time: str
    class Config:
        orm_mode = True

# 声明返回给前端的部门状态数据规范
class DeptState(BaseModel):
    Show: bool
    Message: List[str]
    Record: List[Record] 
    class Config:
        orm_mode = True

# 声明投递的简历信息规范
class CVinfo(BaseModel):
    sno: str
    department: str
    name: str
    sex: str
    birthday: str
    hometown: str
    nation: str
    college: str
    grade: str
    proclass: str
    dormitory: str
    phone: str
    qq: str
    mail: str
    experience: str
    introduce: str
    reason: str

# 声明更新简历状态，标记简历的数据规范
class CVupdate(BaseModel):
    sno: str
    state: Optional[str] = None
    sign: Optional[bool] = None

class CVcomment(BaseModel):
    sno: str
    comment: str