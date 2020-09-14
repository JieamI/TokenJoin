from pydantic import BaseSettings

class Config(BaseSettings):
    # 钉钉扫码登录配置
    APP_ID: str = 'dingoalrnidom4p3khixr0'
    APP_SECRET: str = 'QNDiNQbWbJfiLLuTkR523G8VDRT79Geo-2VplHBEZVJqOKQ62mE8v03lySvPRpoT'
    # APP_ID: str = 'dingoapm6ohzqxmd1kzesi'
    # APP_SECRET: str = 'ccBS_06R4SFXSevbHCKrQco2aQzLVGavH3AkAjeUWuQwt3KK-RxmI5Nw_PK9HLe6'
    # 获取接口调用权限access_token
    ACCESS_APPKEY: str = 'dingit4vuspgz8jk7pce'
    ACCESS_APPSECRET: str = 'xhgolkRUphy07oM6f9se79ebyn18RYU0DHHWWToxWy7PRIfo0Sw13on90DxN2G-C'
    # ACCESS_APPKEY: str = 'ding5apkzoo1aiwmiztt'
    # ACCESS_APPSECRET: str = 'wmE3AJMzPLnFU1VM7WqB22FiNSdCfG5SX1jIYuyOdnjyovCUOG_BCtvRzrQdX7m6'
    # Token相关配置（SECRET_KEY：token生成密钥配置；ALGORITHM：token生成算法配置；EXPIRED_TIME：token有效时间配置，单位天）
    SECRET_KEY: str = "d8ce842b4861102c3719d0f7f1d96047"
    ALGORITHM: str = "HS256"
    EXPIRED_TIME: int = 7
    # 邮箱发送服务配置
    USERNAME_MAIL = "2577438164@qq.com"
    PASSWORD_MAIL = "gifixtxgcwadeajb"
    # 超级管理员账号密码    
    superUsr = 'token123'
    superpwd = 'token123'
    # 部门名映射
    DEPARTMENT_MAP: dict = {
        '技术部': ['前端组', '服务端组', '移动客户端组', '基础架构组'], 
        '设计部': ['交互视觉设计组', '用户研究组'],
        '产品部': [],
        '产品运营': [],
        '新媒体运营': [],
        '人力资源部': [],
        '杂志部': [],
        }

Config = Config()