"""应用配置模块

集中管理应用级配置，避免硬编码分散在各处。
生产环境可通过环境变量覆盖默认值。
支持从 .env 文件加载配置（需安装 python-dotenv）。
"""

import os


# 尝试从 .env 文件加载环境变量
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
except ImportError:
    # python-dotenv 未安装，跳过
    pass


class Config:
    """应用配置"""

    # Flask 服务配置
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', '5000'))

    # API 请求超时配置（秒）
    API_TIMEOUT_SHORT = int(os.getenv('API_TIMEOUT_SHORT', '90'))    # 场景分析
    API_TIMEOUT_MEDIUM = int(os.getenv('API_TIMEOUT_MEDIUM', '120')) # Chat API
    API_TIMEOUT_LONG = int(os.getenv('API_TIMEOUT_LONG', '180'))     # Image API

    # 场景分析配置
    SCENE_ANALYSIS_TEMPERATURE = float(os.getenv('SCENE_ANALYSIS_TEMP', '0.3'))
    SCENE_ANALYSIS_MAX_TOKENS = int(os.getenv('SCENE_ANALYSIS_TOKENS', '1500'))

    # 文件上传配置
    UPLOAD_MAX_AGE_HOURS = int(os.getenv('UPLOAD_MAX_AGE_HOURS', '24'))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

    # CORS 配置
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')  # 生产环境应设置具体域名

    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')


# 导出配置实例
config = Config()
