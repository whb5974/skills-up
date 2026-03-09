"""
配置管理模块
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 项目根目录
BASE_DIR = Path(__file__).parent

# API 配置
class APIConfig:
    TUSHARE_TOKEN = os.getenv('TUSHARE_TOKEN', '')
    JOINQUANT_USER = os.getenv('JOINQUANT_USERNAME', '')
    JOINQUANT_PASS = os.getenv('JOINQUANT_PASSWORD', '')
    ALPHA_VANTAGE_KEY = os.getenv('ALPHA_VANTAGE_KEY', '')

# 交易配置
class TradingConfig:
    DEFAULT_CAPITAL = float(os.getenv('DEFAULT_CAPITAL', 100000))
    MAX_POSITION = float(os.getenv('MAX_POSITION', 0.3))
    STOP_LOSS = float(os.getenv('STOP_LOSS', 0.05))
    TAKE_PROFIT = float(os.getenv('TAKE_PROFIT', 0.15))

# 路径配置
class PathConfig:
    DATA_DIR = BASE_DIR / 'data'
    RAW_DATA_DIR = DATA_DIR / 'raw'
    PROCESSED_DATA_DIR = DATA_DIR / 'processed'
    LOGS_DIR = BASE_DIR / 'logs'
    
    @classmethod
    def init_dirs(cls):
        """初始化目录"""
        for dir_path in [cls.DATA_DIR, cls.RAW_DATA_DIR, 
                         cls.PROCESSED_DATA_DIR, cls.LOGS_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)

# 初始化目录
PathConfig.init_dirs()

print("✅ 配置加载完成")
