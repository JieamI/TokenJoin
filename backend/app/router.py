from fastapi import Depends, File, Form, HTTPException, status, Body, UploadFile
from typing import Optional, List, Dict
from config import Config 
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import models, engine
from . import schemas
from . import app
from depends import *
import utils
import datetime

import random
import uuid

# 数据库测试
@app.get('/test')
def test(db: Session = Depends(get_db)):
    return 'dwadwa'

@app.get('/recv')
def recv(db: Session = Depends(get_db)):
    # models.CVinfo.__table__.drop(engine)
    # models.CVinfo.__table__.create(engine)
    # department_lis = ['技术部', '设计部', '产品部', '产品运营', '新媒体运营', '人力资源部', '杂志部']
    # nick_lis = ['Jie', 'Jane', 'Lucy', 'John', 'Mike', 'Lihua', 'Sarah', 'Amy']
    # for i in range(0,10):
    #     a = models.CVinfo(
    #         department = random.choice(department_lis), 
    #         sno = str(uuid.uuid4()), 
    #         name = random.choice(nick_lis),
    #         sex = random.choice(['男', '女']),
    #         birthday = '2000年8月4日',
    #         hometown = '广东东莞',
    #         nation = '汉族',
    #         college = '信息学院',
    #         grade = '2020',
    #         proclass = '电信2008',
    #         mail = '1732615826@qq.com')
    #     db.add(a)
    # db.commit()
    days = [i for i in range(0, 31)]
    months = [8, 9, 10, 11, 12]
    hours = [i for i in range(0, 24)]
    minutes = [i for i in range(0, 60)]
    seconds = [i for i in range(0, 60)]
    cv_lis = db.query(models.CVinfo).all()
    for cv in cv_lis:
        time = datetime.datetime(2020, random.choice(months), random.choice(days), random.choice(hours), random.choice(minutes), random.choice(seconds))
        cv.time = time.strftime('%Y-%m-%d %H:%M:%S')
    db.commit()
    return

# 重置数据库
@app.get('/refresh')
async def refreshDb(db: Session = Depends(get_db)):
    # 重置部门表
    models.Department.__table__.drop(engine)
    models.Department.__table__.create(engine)
    department_lis = ['技术部', '设计部', '产品部', '产品运营', '新媒体运营', '人力资源部', '杂志部']
    for each in department_lis:
        depart = models.Department(Name = each)
        db.add(depart)
    # 重置用户表
    models.User.__table__.drop(engine)
    models.User.__table__.create(engine)
    nick_lis = ['Jie', 'Jane', 'Lucy', 'John', 'Mike', 'Lihua', 'Sarah', 'Amy']
    auth_lis = [True, False]
    for i in range(0, 10):
        user = models.User(
            Nick = random.choice(nick_lis), 
            Openid = str(uuid.uuid4()), 
            Department_name = random.choice(department_lis),
            Authorized = random.choice(auth_lis))
        db.add(user)
    # 重置记录表
    models.Record.__table__.drop(engine)
    models.Record.__table__.create(engine)
    # for i in range(0, 10):
    #     record = models.Record(Owner = random.choice(department_lis), Operator = random.choice(nick_lis), Operation = 'undefined')
    #     db.add(record)
    db.commit()
    return

# -------------------------登录/申请处理路由------------------------------------

# 处理登录
@app.post("/login")
def handleLogin(
    code: schemas.Authcode, 
    db: Session = Depends(get_db)
    ):
    # 获取用户信息
    res_dic = utils.getUserinfo(code.dict()['code'])
    # 数据库中查询用户身份，如果是管理员则授权码为1并生成有效token，否则为0，token为空
    user = db.query(models.User).filter(res_dic['user_info']['openid'] == models.User.Openid).first()
    if user: 
        if user.Authorized:
            authcode = 1
        else:
            authcode = 0
        token = utils.create_token(res_dic['user_info']['openid'])
    else:
        # 如果用户不在数据库内，则在其token内加入department属性
        authcode = 0
        department = utils.getDepartment(res_dic['user_info']['unionid'])
        token = utils.create_token(res_dic['user_info']['openid'], department, res_dic['user_info']['nick'])
    return {
        'access_token': token, 
        'token_type': 'bearer', 
        'nick': res_dic['user_info']['nick'],
        'authcode': authcode}

# 处理管理员申请
@app.post('/apply')
def handleApply(
    code: schemas.Authcode, 
    db: Session = Depends(get_db)
    ):
    # 获取用户信息
    res_dic = utils.getUserinfo(code.code)
    # 判断申请用户是否在数据库内
    user = db.query(models.User).filter(res_dic['user_info']['openid'] == models.User.Openid).first()
    if user:
        if user.Authorized:
            raise HTTPException(
                status_code = status.HTTP_503_SERVICE_UNAVAILABLE, 
                detail = '您已是管理员')
        raise HTTPException(
                status_code = status.HTTP_503_SERVICE_UNAVAILABLE, 
                detail = '您已向管理员申请，请勿重复申请')
    
    department = utils.getDepartment(res_dic['user_info']['unionid'])
    try:
        user = models.User(
            Nick = res_dic['user_info']['nick'], 
            Openid = res_dic['user_info']['openid'], 
            Department_name = department)
        db.add(user)
        db.commit()
    except:
        raise HTTPException(
                status_code = status.HTTP_503_SERVICE_UNAVAILABLE, 
                detail = '录入信息异常')
    return {'code': 0}

# --------------------------部门状态获取及更新路由-------------------------------

# 获取部门状态，包括部门信息模板，操作记录和展示状态
@app.get('/deptstate', response_model = schemas.DeptState)
def getDeptState(
    current_user: models.User = Depends(validate_auth)
    ):
    dept_state = current_user.Department
    # 将字符类型的信息模板列表化
    dept_state.Message = eval(dept_state.Message)
    return dept_state

# 更新部门展示状态
@app.post('/updateshow')
def handleUpdateShow(
    current_user: models.User = Depends(validate_auth), 
    Show: bool = Body(..., embed = True), 
    db: Session = Depends(get_db)
    ):
    try:
        current_user.Department.Show = Show
        # 更新记录
        record = models.Record(
            Owner = current_user.Department_name,
            Operator = current_user.Nick, 
            Operation = '打开了部门展示' if Show else '关闭了部门展示')
        db.add(record)
        db.commit()
        return {'code': 0}
    except:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = '展示状态切换失败')

# 更新部门信息模板
@app.post('/updatemsg')
def handleUpdateMsg(
    current_user: models.User = Depends(validate_auth), 
    Message: List[str] = Body(..., embed = True), 
    db: Session = Depends(get_db)
    ):
    try:
        current_user.Department.Message = str(Message)
        # 添加记录
        record = models.Record(
            Owner = current_user.Department_name,
            Operator = current_user.Nick, 
            Operation = '更新了信息模板')
        db.add(record)
        db.commit()
        return {'code': 0}
    except:
        raise HTTPException(
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
        detail = '信息模板更新失败')

# -------------------------后台权限设定相关理由-----------------------------------

# 获取当前用户所属部门的权限设定数据，包括管理员数据和申请管理员数据
@app.get('/setting/tabledata', response_model = Dict[str, List[schemas.Table_data]])
def getTableData(
    current_user: models.User = Depends(validate_auth), 
    db: Session = Depends(get_db)
    ):
    admin_lis = db.query(models.User).filter(
        and_(models.User.Department_name == current_user.Department_name, models.User.Authorized == True)).all()
    apply_lis = db.query(models.User).filter(
        and_(models.User.Department_name == current_user.Department_name, models.User.Authorized == False)).all()
    return {'admin_lis': admin_lis, 'apply_lis': apply_lis}

# 移除管理员
@app.post('/setting/remove')
def handleRemove(
    remove_lis: List[schemas.Setting_param], 
    current_user: models.User = Depends(validate_auth),
    db: Session = Depends(get_db)
    ):
    try:
        for remove_user in remove_lis:
            user = db.query(models.User).filter(models.User.Openid == remove_user.Openid).first()
            # 添加记录
            record = models.Record(
                Owner = current_user.Department_name,
                Operator = current_user.Nick, 
                Operation = '移除了管理员' + user.Nick)
            if user:
                db.delete(user)
                db.add(record)
        db.commit()
    except:
        raise HTTPException( 
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = '移除失败')
    return {'code': 0}

# 同意普通成员的管理员申请
@app.post('/setting/accept')
def handleAccept(
    accept_lis: List[schemas.Setting_param], 
    current_user: models.User = Depends(validate_auth),
    db: Session = Depends(get_db)
    ):
    try:
        for accept_user in accept_lis:
            user = db.query(models.User).filter(models.User.Openid == accept_user.Openid).first()
            record = models.Record(
                Owner = current_user.Department_name,
                Operator = current_user.Nick, 
                Operation = '同意了' + user.Nick + '的管理员申请')
            if user:
                user.Authorized = True
                db.add(record)
        db.commit()
    except:
        raise HTTPException( 
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = '同意申请失败')
    return {'code': 0}

# 拒绝普通成员的管理员申请
@app.post('/setting/refuse')
def handleRefuse(
    refuse_lis: List[schemas.Setting_param],
    current_user: models.User = Depends(validate_auth),
    db: Session = Depends(get_db)
    ):
    try:
        for refuse_user in refuse_lis:
            user = db.query(models.User).filter(models.User.Openid == refuse_user.Openid).first()
            if user:
                record = models.Record(
                    Owner = current_user.Department_name,
                    Operator = current_user.Nick, 
                    Operation = '拒绝了' + user.Nick + '的管理员申请')
                db.delete(user)
                db.add(record)
        db.commit()
    except:
        raise HTTPException( 
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = '拒绝申请失败')
    return {'code': 0}


# -------------------------后台首页统计数据获取-----------------------------------
# 获取各部门简历投递的统计数据
@app.get('/index/data')
def getStatistics(
    current_user: models.User = Depends(validate_auth),
    db: Session = Depends(get_db)
    ):
    try:
        cvinfo_list = db.query(models.CVinfo).all()
        # 将每个简历对应的投递部门名加入列表
        depts = [cv.department for cv in cvinfo_list]
        pie_data = [{'name': dept, 'value': depts.count(dept)} for dept in depts]
        # 滤除重复的字典
        pie_data = [dict(t) for t in {tuple(d.items()) for d in pie_data}]
        
        # 将每个简历的投递时间都加入列表，且只取年月日
        dates = [cv.time.split(' ')[0] for cv in cvinfo_list]
        line_data = [[date, dates.count(date)] for date in dates]
        # 滤除重复的列表
        line_data = [list(t) for t in {tuple(l) for l in line_data}]
        return {'pie_data': pie_data, 'line_data': line_data}
    except:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = '统计数据获取异常')

# 返回招新宣传首页各部门的展示状态
@app.get('/getshow')
def getDeptShowState(db: Session = Depends(get_db)):
    dept_lis = db.query(models.Department).all()
    res = []
    for dept in dept_lis:
        if dept.Show:
            res.append(dept.Name)
    return {'showingList': res}

# -------------------------简历投递/管理相关路由-----------------------------------

# 简历投递
@app.post('/join/cv')
def handleJoin(
    cv: schemas.CVinfo, 
    db: Session = Depends(get_db)
    ):
    candidate = db.query(models.CVinfo).filter(models.CVinfo.sno == cv.sno).first()
    # 如果投递者信息已在库，则判断两次投递时间间隔是否超过24小时，若未超过则不允许投递
    if candidate:
        date = datetime.datetime.strptime(candidate.time, '%Y-%m-%d %H:%M:%S')
        delta = datetime.datetime.now() - date
        if delta.days < 1:
            raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = '您已投递简历，若需更改请在24小时后操作')
        else:
            cv_dic = cv.dict()
            cv_dic['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            db.query(models.CVinfo).filter(models.CVinfo.sno == cv.sno).update(cv_dic)
            db.commit()
            return {'code': 0}
    try:
        obj = models.CVinfo(**cv.dict())
        db.add(obj)
        db.commit()
        return {'code': 0}
    except:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = '简历投递失败')

# 返回简历信息
@app.get('/join/cvinfo')
def handleCvinfo(
    current_user: models.User = Depends(get_user),
    db: Session = Depends(get_db)
    ):
    cvinfo_lis = db.query(models.CVinfo).filter(current_user.Department_name == models.CVinfo.department).all()
    for cv in cvinfo_lis:
        cv.comment = eval(cv.comment)
    return {'cvinfo_lis': cvinfo_lis}


# 简历状态/标记更新
@app.post('/join/updatecv')
def handleCvupdate(
    data: schemas.CVupdate,
    current_user: models.User = Depends(validate_auth),
    db: Session = Depends(get_db)
    ):
    cv = db.query(models.CVinfo).filter(models.CVinfo.sno == data.sno).first()
    if not cv:
        raise HTTPException(
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
        detail = '简历信息不存在')
    try:
        if data.state:
            cv.state = data.state
            # 添加记录
            record = models.Record(
                Owner = current_user.Department_name,
                Operator = current_user.Nick, 
                Operation = '将' + cv.name + '的简历状态设置为' + data.state)
            db.add(record)
            db.commit()
        else:
            cv.sign = data.sign
            record = models.Record(
                Owner = current_user.Department_name,
                Operator = current_user.Nick, 
                Operation = '标记了' + cv.name if data.sign else '取消了对' + cv.name + '的标记')
            db.add(record)
            db.commit()
        return {'code': 0}
    except:
        raise HTTPException(
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
        detail = '数据库异常')

@app.post('/join/setcomment')
def setCVComment(
    data: schemas.CVcomment,
    current_user: models.User = Depends(get_user),
    db: Session = Depends(get_db)
    ):
    cv = db.query(models.CVinfo).filter(models.CVinfo.sno == data.sno).first()
    if not cv:
        raise HTTPException(
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
        detail = '简历信息不存在')
    try:
        comment_dic = eval(cv.comment) 
        comment_dic[current_user.Nick] = data.comment
        cv.comment = str(comment_dic)
        # 添加记录
        record = models.Record(
            Owner = current_user.Department_name,
            Operator = current_user.Nick, 
            Operation = '对' + cv.name + '进行了面试评价')
        db.add(record)
        db.commit()
        return {'code': 0}
    except:
        raise HTTPException(
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
        detail = '数据库异常')

# 邮件发送
@app.post('/join/sendemail')
async def sendEmail(
    token: str = Form(None),
    files: List[UploadFile] = File(None), 
    recipients:str = Form(...),
    text: str = Form(...),
    subject: str = Form(...),
    db: Session = Depends(get_db)
    ):
    if not token:
        raise HTTPException(
                status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
                detail = '你没有发送邮件的权限')
    if recipients:
        try:
            # 字符串转化为列表
            recipients = recipients.split(',')
            if files:
                await utils.send_email(recipients, subject, text, files)
            else:
                await utils.send_email(recipients, subject, text)
            # 添加记录
            token_decode = jwt.decode(token, Config.SECRET_KEY, algorithms = Config.ALGORITHM)
            openid = token_decode['openid']
            current_user = db.query(models.User).filter(models.User.Openid == openid).first()
            record = models.Record(
                Owner = current_user.Department_name,
                Operator = current_user.Nick, 
                Operation = '发送了邮件')
            db.add(record)
            db.commit()
            return {'code': 0}
        except:
            raise HTTPException(
                status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
                detail = '邮件发送失败')
    raise HTTPException(
                status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
                detail = '没有简历被选中')

# 超级管理员用户获取所有用户
@app.post('/super/getalltabledata', response_model = Dict[str, List[schemas.Table_data]])
def getTableData(
    usr: str = Body(...),
    pwd: str = Body(...), 
    db: Session = Depends(get_db)
    ):
    if usr == Config.superUsr and pwd == Config.superpwd:
        admin_lis = db.query(models.User).filter(models.User.Authorized == True).all()
        apply_lis = db.query(models.User).filter(models.User.Authorized == False).all()
        return {'admin_lis': admin_lis, 'apply_lis': apply_lis}
    else:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = '账号密码错误'
        )

@app.post('/super/authorsetting')
def setAuthor(
    accept_lis: List[schemas.Setting_param] = Body(None),
    refuse_lis: List[schemas.Setting_param] = Body(None),
    remove_lis: List[schemas.Setting_param] = Body(None),
    usr: str = Body(...),
    pwd: str = Body(...),
    db: Session = Depends(get_db)
    ):
    if usr != Config.superUsr or pwd != Config.superpwd:
        raise HTTPException( 
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = '权限不足')
    try:    
        if accept_lis:
            for accept_user in accept_lis:
                user = db.query(models.User).filter(models.User.Openid == accept_user.Openid).first()
                if user:
                    user.Authorized = True
        if refuse_lis:
            for refuse_user in refuse_lis:
                user = db.query(models.User).filter(models.User.Openid == refuse_user.Openid).first()
                if user:
                    db.delete(user)
        if remove_lis:
            for remove_user in remove_lis:
                user = db.query(models.User).filter(models.User.Openid == remove_user.Openid).first()
                if user:
                    db.delete(user)
        db.commit()
        return {'code': 0}
    except:
        raise HTTPException( 
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = '操作异常')