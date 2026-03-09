"""
Alpha Vantage API - 全球金融市场数据
免费 Key 限制：每分钟 5 次，每天 500 次
官网：https://www.alphavantage.co
"""
import requests
import pandas as pd
from loguru import logger
from config import APIConfig

class AlphaVantageAPI:
    """Alpha Vantage 数据接口"""
    
    BASE_URL = "https://www.alphavantage.co/query"
    
    def __init__(self):
        self.api_key = APIConfig.ALPHA_VANTAGE_KEY
        self.session = requests.Session()
        
        if not self.api_key or self.api_key == 'your_alpha_vantage_key':
            logger.warning("⚠️ ALPHA_VANTAGE_KEY 未配置，请在.env 文件中设置")
        else:
            logger.info("✅ Alpha Vantage API 初始化完成")
    
    def get_global_quote(self, symbol):
        """
        获取全球股票报价
        
        Args:
            symbol: 股票代码 (如 'IBM', 'AAPL')
        
        Returns:
            dict: 报价数据
        """
        if not self.api_key:
            return None
        
        try:
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': symbol,
                'apikey': self.api_key
            }
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            data = response.json()
            
            if 'Global Quote' in data:
                quote = data['Global Quote']
                return {
                    'symbol': quote.get('01. symbol', ''),
                    'open': float(quote.get('02. open', 0)),
                    'high': float(quote.get('03. high', 0)),
                    'low': float(quote.get('04. low', 0)),
                    'price': float(quote.get('05. price', 0)),
                    'volume': int(quote.get('06. volume', 0)),
                    'change': float(quote.get('09. change', 0)),
                    'change_percent': quote.get('10. change percent', ''),
                }
        except Exception as e:
            logger.error(f"获取报价失败：{e}")
        return None
    
    def get_time_series(self, symbol, outputsize='compact'):
        """
        获取日线时间序列
        
        Args:
            symbol: 股票代码
            outputsize: compact(100 条) 或 full(20 年数据)
        
        Returns:
            DataFrame: 日线数据
        """
        if not self.api_key:
            return None
        
        try:
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'outputsize': outputsize,
                'apikey': self.api_key
            }
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            data = response.json()
            
            if 'Time Series (Daily)' in data:
                df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
                df.index = pd.to_datetime(df.index)
                df = df.astype(float)
                df = df.rename(columns={
                    '1. open': 'open',
                    '2. high': 'high',
                    '3. low': 'low',
                    '4. close': 'close',
                    '5. volume': 'volume'
                })
                return df.sort_index()
        except Exception as e:
            logger.error(f"获取时间序列失败：{e}")
        return None
    
    def get_technical_indicator(self, symbol, indicator, **kwargs):
        """
        获取技术指标
        
        Args:
            symbol: 股票代码
            indicator: 指标名称 (SMA, EMA, RSI, MACD, BBANDS 等)
            **kwargs: 其他参数 (period, series_type 等)
        
        Returns:
            DataFrame: 指标数据
        """
        if not self.api_key:
            return None
        
        try:
            params = {
                'function': indicator,
                'symbol': symbol,
                'apikey': self.api_key,
                **kwargs
            }
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            data = response.json()
            
            # 查找数据 key
            for key in data:
                if key != 'Meta Data':
                    df = pd.DataFrame.from_dict(data[key], orient='index')
                    df.index = pd.to_datetime(df.index)
                    df = df.astype(float)
                    return df.sort_index()
        except Exception as e:
            logger.error(f"获取技术指标失败：{e}")
        return None
    
    def get_sector_performance(self):
        """
        获取行业板块表现
        
        Returns:
            dict: 各行业表现
        """
        if not self.api_key:
            return None
        
        try:
            params = {
                'function': 'SECTOR',
                'apikey': self.api_key
            }
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            data = response.json()
            return data
        except Exception as e:
            logger.error(f"获取行业表现失败：{e}")
        return None


# 测试
if __name__ == "__main__":
    api = AlphaVantageAPI()
    
    if api.api_key:
        # 测试获取报价
        quote = api.get_global_quote('IBM')
        if quote:
            print(f"\n📊 {quote['symbol']}")
            print(f"   当前价：{quote['price']}")
            print(f"   涨跌：{quote['change']} ({quote['change_percent']})")
        
        # 测试时间序列
        ts = api.get_time_series('IBM', outputsize='compact')
        if ts is not None:
            print(f"\n📈 获取到 {len(ts)} 条数据")
            print(ts[['close', 'volume']].tail())
    else:
        print("\n⚠️ 请先配置 ALPHA_VANTAGE_KEY")
