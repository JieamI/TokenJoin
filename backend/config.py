from pydantic import BaseSettings

class Config(BaseSettings):
    # 钉钉扫码登录配置
    APP_ID: str = 'xxxxxxxxxxxxxxxxx'
    APP_SECRET: str = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    # 获取接口调用权限access_token
    ACCESS_APPKEY: str = 'xxxxxxxxxxxxxxxxxxxxxxxx'
    ACCESS_APPSECRET: str = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
      # Token相关配置（SECRET_KEY：token生成密钥配置；ALGORITHM：token生成算法配置；EXPIRED_TIME：token有效时间配置，单位天）
    SECRET_KEY: str = "xxxxxxxxxxxxxxxxxxxxxxxxx"
    ALGORITHM: str = "HS256"
    EXPIRED_TIME: int = 7
    # 邮箱发送服务配置
    USERNAME_MAIL = "xxxxxxxx@qq.com"
    PASSWORD_MAIL = "xxxxxxxxxxxxxxx"
    # 超级管理员账号密码    
    superUsr = 'xxxxx'
    superpwd = 'xxxxx'
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
