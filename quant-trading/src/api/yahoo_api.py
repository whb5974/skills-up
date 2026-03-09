"""
Yahoo Finance API - 国际金融市场数据
通过 yfinance 库访问，无需 API Key
"""
import pandas as pd
from loguru import logger

try:
    import yfinance as yf
    HAS_YF = True
except ImportError:
    HAS_YF = False
    logger.warning("yfinance 未安装，请运行：pip install yfinance")

class YahooFinanceAPI:
    """Yahoo Finance 数据接口"""
    
    def __init__(self):
        if HAS_YF:
            logger.info("✅ Yahoo Finance API 初始化完成 (无需 Key)")
        else:
            logger.error("❌ yfinance 库未安装")
    
    def get_ticker(self, symbol):
        """
        获取股票对象
        
        Args:
            symbol: 股票代码 (如 'AAPL', '600000.SS' 上证指数)
        
        Returns:
            Ticker 对象
        """
        if not HAS_YF:
            return None
        try:
            ticker = yf.Ticker(symbol)
            return ticker
        except Exception as e:
            logger.error(f"获取股票对象失败：{e}")
            return None
    
    def get_history(self, symbol, period='1mo', interval='1d'):
        """
        获取历史行情
        
        Args:
            symbol: 股票代码
            period: 时间范围 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: 时间间隔 (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
        
        Returns:
            DataFrame: 历史数据
        """
        if not HAS_YF:
            return None
        
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            return df
        except Exception as e:
            logger.error(f"获取历史数据失败：{e}")
            return None
    
    def get_info(self, symbol):
        """
        获取股票基本信息
        
        Returns:
            dict: 股票信息
        """
        if not HAS_YF:
            return None
        
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                'name': info.get('shortName', ''),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'marketCap': info.get('marketCap', 0),
                'peRatio': info.get('trailingPE', 0),
                'dividendYield': info.get('dividendYield', 0),
                '52WeekHigh': info.get('fiftyTwoWeekHigh', 0),
                '52WeekLow': info.get('fiftyTwoWeekLow', 0),
            }
        except Exception as e:
            logger.error(f"获取股票信息失败：{e}")
            return None
    
    def get_recommendations(self, symbol):
        """
        获取分析师评级
        
        Returns:
            DataFrame: 评级历史
        """
        if not HAS_YF:
            return None
        
        try:
            ticker = yf.Ticker(symbol)
            rec = ticker.recommendations
            return rec
        except Exception as e:
            logger.error(f"获取评级失败：{e}")
            return None


# 测试
if __name__ == "__main__":
    if HAS_YF:
        api = YahooFinanceAPI()
        
        # 测试美股
        print("\n📊 测试 AAPL (苹果公司):")
        info = api.get_info('AAPL')
        if info:
            for k, v in info.items():
                print(f"   {k}: {v}")
        
        # 测试历史数据
        hist = api.get_history('AAPL', period='1mo')
        if hist is not None:
            print(f"\n📈 获取到 {len(hist)} 条数据")
            print(hist[['Close', 'Volume']].tail())
    else:
        print("\n⚠️ 请先安装 yfinance: pip install yfinance")
