from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, models
from config import Config
import jwt

# 建立并获取和数据库间的会话，在返回响应后关闭会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 将获取token的地址作为参数传入bearer类并实例化
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
# 权限验证，未授权将无法调用使用了该依赖的API
def validate_auth(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "令牌失效，请重新登录")
    try:
        token_decode = jwt.decode(token, Config.SECRET_KEY, algorithms = Config.ALGORITHM)
        openid = token_decode['openid']
    except:
        raise exception
    current_user =  db.query(models.User).filter(models.User.Openid == openid).first()
    if not current_user or not current_user.Authorized:
        raise exception
    return current_user

# 获取当前用户，此依赖用于不需要权限但需要当前用户信息的理由
def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    exception = HTTPException(
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
        detail = '当前用户信息获取异常')
    try:
        token_decode = jwt.decode(token, Config.SECRET_KEY, algorithms = Config.ALGORITHM)
        openid = token_decode['openid']
    except:
        raise exception
    current_user =  db.query(models.User).filter(models.User.Openid == openid).first()
    # 如果当前用户不在数据库内，则生成一个当前用户对象
    if not current_user:
        department = token_decode['department']
        nick = token_decode['nick']
        current_user = models.User(Openid = openid, Department_name = department, Nick = nick)
    return current_user