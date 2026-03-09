"""
新浪财经 API - 免费实时行情
无需 API Key
"""
import requests
import pandas as pd
from loguru import logger

class SinaAPI:
    """新浪财经股票行情 API"""
    
    BASE_URL = "http://hq.sinajs.cn"
    
    def __init__(self):
        self.session = requests.Session()
        logger.info("✅ 新浪财经 API 初始化完成 (无需 Key)")
    
    def get_realtime_quote(self, symbol):
        """
        获取实时行情
        
        Args:
            symbol: 股票代码 (如 'sh600000' 或 'sz000001')
        
        Returns:
            dict: 行情数据
        """
        try:
            url = f"{self.BASE_URL}/list={symbol}"
            response = self.session.get(url, timeout=5)
            response.encoding = 'gbk'  # 新浪返回 GBK 编码
            
            data = response.text.strip()
            if data:
                # 解析返回数据
                parts = data.split('=')[1].strip('"').split(',')
                return {
                    'symbol': symbol,
                    'name': parts[0],
                    'open': float(parts[1]),
                    'high': float(parts[2]),
                    'low': float(parts[3]),
                    'current': float(parts[4]),
                    'volume': int(parts[5]),
                    'amount': float(parts[6]),
                    'bid': float(parts[7]),
                    'ask': float(parts[8]),
                    'timestamp': f"{parts[30]} {parts[31]}"
                }
        except Exception as e:
            logger.error(f"获取行情失败：{e}")
        return None
    
    def get_kline(self, symbol, period='d', count=100):
        """
        获取 K 线数据
        
        Args:
            symbol: 股票代码
            period: 周期 (d=日，w=周，m=月)
            count: 获取数量
        
        Returns:
            DataFrame: K 线数据
        """
        try:
            url = f"http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData"
            params = {
                'symbol': symbol,
                'scale': period,
                'datalen': count
            }
            response = self.session.get(url, params=params, timeout=10)
            data = response.json()
            
            if data:
                df = pd.DataFrame(data)
                df['day'] = pd.to_datetime(df['day'])
                df = df.rename(columns={
                    'day': 'date',
                    'open': 'open',
                    'high': 'high',
                    'low': 'low',
                    'close': 'close',
                    'volume': 'volume'
                })
                return df
        except Exception as e:
            logger.error(f"获取 K 线失败：{e}")
        return None
    
    def get_stock_list(self, market='sh'):
        """获取股票列表"""
        # 简化版本，实际需要从新浪获取完整列表
        logger.info(f"获取{market}市场股票列表...")
        return []


# 测试
if __name__ == "__main__":
    api = SinaAPI()
    
    # 测试获取实时行情
    quote = api.get_realtime_quote('sh600000')
    if quote:
        print(f"\n📊 {quote['name']} ({quote['symbol']})")
        print(f"   当前价：{quote['current']}")
        print(f"   开盘：{quote['open']}  最高：{quote['high']}  最低：{quote['low']}")
    
    # 测试获取 K 线
    kline = api.get_kline('sh600000', period='d', count=30)
    if kline is not None:
        print(f"\n📈 获取到 {len(kline)} 条 K 线数据")
        print(kline.tail())
