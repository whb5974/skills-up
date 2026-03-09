"""
Tushare API - 国内金融数据接口
需要 Token: https://tushare.pro
"""
import tushare as ts
import pandas as pd
from loguru import logger
from config import APIConfig

class TushareAPI:
    """Tushare 数据接口"""
    
    def __init__(self):
        token = APIConfig.TUSHARE_TOKEN
        if not token or token == 'your_tushare_token_here':
            logger.warning("⚠️ TUSHARE_TOKEN 未配置，请在.env 文件中设置")
            self.pro = None
        else:
            ts.set_token(token)
            self.pro = ts.pro_api()
            logger.info("✅ Tushare API 初始化完成")
    
    def get_daily(self, ts_code, start_date, end_date):
        """
        获取日线行情
        
        Args:
            ts_code: 股票代码 (如 '600000.SH')
            start_date: 开始日期 (YYYYMMDD)
            end_date: 结束日期 (YYYYMMDD)
        
        Returns:
            DataFrame: 日线数据
        """
        if not self.pro:
            logger.error("Tushare 未配置")
            return None
        
        try:
            df = self.pro.daily(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date
            )
            return df
        except Exception as e:
            logger.error(f"获取日线失败：{e}")
            return None
    
    def get_stock_basic(self, exchange=''):
        """
        获取股票基本信息
        
        Args:
            exchange: 交易所 (SSE/ SZSE/ BSE)
        
        Returns:
            DataFrame: 股票列表
        """
        if not self.pro:
            return None
        
        try:
            df = self.pro.stock_basic(exchange=exchange)
            return df
        except Exception as e:
            logger.error(f"获取股票列表失败：{e}")
            return None
    
    def get_fina_indicator(self, ts_code, start_date, end_date):
        """
        获取财务指标
        
        Args:
            ts_code: 股票代码
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            DataFrame: 财务指标
        """
        if not self.pro:
            return None
        
        try:
            df = self.pro.fina_indicator(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date
            )
            return df
        except Exception as e:
            logger.error(f"获取财务指标失败：{e}")
            return None
    
    def get_index_daily(self, ts_code, start_date, end_date):
        """
        获取大盘指数行情
        
        Args:
            ts_code: 指数代码 (如 '000001.SH' 上证指数)
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            DataFrame: 指数数据
        """
        if not self.pro:
            return None
        
        try:
            df = self.pro.index_daily(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date
            )
            return df
        except Exception as e:
            logger.error(f"获取指数数据失败：{e}")
            return None


# 测试
if __name__ == "__main__":
    api = TushareAPI()
    
    if api.pro:
        # 测试获取股票列表
        stocks = api.get_stock_basic()
        if stocks is not None:
            print(f"\n📋 获取到 {len(stocks)} 只股票")
            print(stocks[['ts_code', 'name', 'industry']].head())
        
        # 测试获取日线
        daily = api.get_daily('600000.SH', '20260101', '20260226')
        if daily is not None:
            print(f"\n📈 获取到 {len(daily)} 条日线数据")
            print(daily.head())
    else:
        print("\n⚠️ 请先配置 TUSHARE_TOKEN")
