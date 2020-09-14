from fastapi import HTTPException, status
from config import Config
from base64 import standard_b64encode
from datetime import timedelta, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication 
import aiosmtplib
import urllib.parse
import requests
import hmac
import jwt
import time

# 通过扫码登录获取用户的nick,openid,unionid等信息，其中unionid用于获取用户所在部门
def getUserinfo(code: str):
    # 获取APP_ID
    accessKey = Config.APP_ID
    # 获取时间戳（单位毫秒）
    timestamp = str(round(time.time()*1000))
    # 获取签名信息
    signature = GenUrlSignature(Config.APP_SECRET, timestamp)
    # 请求API并将返回的json转化为字典形式
    try:
        res_dic = requests.post(
            url = "https://oapi.dingtalk.com/sns/getuserinfo_bycode?accessKey={}&timestamp={}&signature={}".format(accessKey, timestamp, signature), 
            json = {"tmp_auth_code": code}
            ).json()
    except:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
            detail = '请求用户信息失败')
    # 当用户试图第二次使用授权码获取token时直接返回未授权
    if res_dic['errcode'] != 0:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = '授权码无效，请尝试重新扫码')
    return res_dic

# 签名算法，注意签名需要进行url编码
def GenUrlSignature(
    app_secret: str, 
    timestamp: str
):
    digest = hmac.HMAC(key = app_secret.encode('utf-8'),
                        msg = timestamp.encode('utf-8'),
                        digestmod = hmac._hashlib.sha256).digest()
    signature = standard_b64encode(digest).decode('utf-8')
    signature_encode = urllib.parse.quote(signature)
    return signature_encode

# 生成token
def create_token(
    openid: str, 
    department: str = '', 
    nick: str = ''
):
    dic = {
        'openid': openid,
        'department': department, 
        'nick': nick,
        'exp': datetime.utcnow() + timedelta(days = Config.EXPIRED_TIME)}
    token_encode = jwt.encode(dic, Config.SECRET_KEY, algorithm = Config.ALGORITHM)
    return token_encode

# 获取用户所在部门
def getDepartment(unionid: str):
    exception = HTTPException(
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
        detail = '请求接口失败或用户所属部门不合法'
        )
    try:
        # 获取调用钉钉接口所需的access_token
        access_token = requests.get(
            'https://oapi.dingtalk.com/gettoken?appkey={}&appsecret={}'.format(Config.ACCESS_APPKEY,Config.ACCESS_APPSECRET)
            ).json()['access_token']
        # 通过access_token和unionid获取用户的userid
        userid = requests.get(
            url = "https://oapi.dingtalk.com/user/getUseridByUnionid?access_token={}&unionid={}".format(access_token, unionid)
            ).json()['userid']
        # 通过access_token和userid获取用户所属部门id列表
        deptIDs = requests.get(
            url = "https://oapi.dingtalk.com/user/get?access_token={}&userid={}".format(access_token, userid)
            ).json()['department']
        # 通过access_token和部门id获取用户所属部门名列表
        depts = []
        for deptID in deptIDs:
            dept = requests.get(
                url = 'https://oapi.dingtalk.com/department/get?access_token={}&id={}'.format(access_token, deptID)
            ).json()['name']
            depts.append(dept)
    except:
        raise exception
    for dept in depts:
        if dept in Config.DEPARTMENT_MAP:
            return dept
        else:
            for group in Config.DEPARTMENT_MAP.values():
                if dept in group:
                    return list(Config.DEPARTMENT_MAP.keys())[list(Config.DEPARTMENT_MAP.values()).index(group)]
    raise exception

# 异步发送邮件
async def send_email(
    recipients: list, 
    subject: str,
    text: str, 
    files: list = []
):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'Token团队'
    msg.attach(MIMEText(text))

    for _file in files:
        attachment = MIMEApplication(await _file.read(), _file.content_type)
        attachment.add_header('Content-Disposition', 'attachment', filename = _file.filename)
        msg.attach(attachment)

    await aiosmtplib.send(
        msg,
        sender = Config.USERNAME_MAIL,
        username = Config.USERNAME_MAIL,
        password = Config.PASSWORD_MAIL,
        hostname = "smtp.qq.com",
        port = 465,
        use_tls = True,
        recipients = recipients
    )