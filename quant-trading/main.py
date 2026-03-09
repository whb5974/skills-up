"""
量化交易分析系统 - 主程序入口

功能:
1. 获取股票行情数据
2. 技术指标分析
3. 风险评估
4. 选股策略
5. 生成投资建议
"""
import sys
from pathlib import Path
from loguru import logger

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from config import TradingConfig
from src.api.sina_api import SinaAPI
from src.api.tushare_api import TushareAPI
from src.analysis.technical import TechnicalAnalysis
from src.analysis.risk import RiskAnalysis

# 配置日志
logger.add("logs/quant_{time}.log", rotation="1 day", retention="7 days")
logger.info("🚀 量化交易分析系统启动")

def analyze_stock(symbol, name):
    """分析单只股票"""
    print(f"\n{'='*60}")
    print(f"📊 分析：{name} ({symbol})")
    print('='*60)
    
    # 获取数据
    api = SinaAPI()
    df = api.get_kline(symbol, period='d', count=60)
    
    if df is None or len(df) < 30:
        print(f"⚠️ 数据不足，跳过")
        return None
    
    # 计算技术指标
    df = TechnicalAnalysis.calculate_all(df)
    
    # 风险分析
    risk_analysis = RiskAnalysis.analyze_stock(df, name)
    risk_rating = RiskAnalysis.risk_rating(risk_analysis)
    
    # 生成信号
    df = TechnicalAnalysis.generate_signal(df)
    latest_signal = df.iloc[-1]['signal']
    
    # 输出结果
    print(f"\n📈 当前价格：{df.iloc[-1]['close']:.2f}")
    print(f"📉 5 日均线：{df.iloc[-1]['ma5']:.2f}")
    print(f"📉 20 日均线：{df.iloc[-1]['ma20']:.2f}")
    print(f"📊 RSI: {df.iloc[-1]['rsi']:.2f}")
    print(f"📊 MACD: {df.iloc[-1]['macd']:.4f}")
    
    print(f"\n🎯 风险评级：{risk_rating}")
    print(f"📊 波动率：{risk_analysis['volatility']:.2%}")
    print(f"📉 最大回撤：{risk_analysis['max_drawdown']:.2%}")
    print(f"📈 夏普比率：{risk_analysis['sharpe_ratio']:.2f}")
    print(f"💹 总收益：{risk_analysis['total_return']:.2%}")
    
    signal_text = {1: '买入', -1: '卖出', 0: '持有'}
    print(f"\n📌 交易信号：{signal_text.get(latest_signal, '持有')}")
    
    return {
        'symbol': symbol,
        'name': name,
        'price': df.iloc[-1]['close'],
        'signal': latest_signal,
        'risk_rating': risk_rating,
        'analysis': risk_analysis
    }


def select_stocks(capital=100000):
    """
    选股策略 - 筛选值得投资的股票
    
    筛选条件:
    1. 技术面：MA5>MA20 (上升趋势)
    2. 动量：RSI 在 40-70 之间 (不过热)
    3. 风险：波动率<50%，最大回撤>-30%
    4. 收益：夏普比率>0
    """
    print("\n" + "="*60)
    print("🔍 开始选股分析...")
    print("="*60)
    
    # 候选股票池 (示例)
    candidates = [
        ('sh600000', '浦发银行'),
        ('sh600036', '招商银行'),
        ('sh601318', '中国平安'),
        ('sh600519', '贵州茅台'),
        ('sz000858', '五粮液'),
        ('sz000333', '美的集团'),
        ('sz002415', '海康威视'),
        ('sh600030', '中信证券'),
        ('sh601166', '兴业银行'),
        ('sz000001', '平安银行'),
    ]
    
    results = []
    for symbol, name in candidates:
        result = analyze_stock(symbol, name)
        if result:
            results.append(result)
    
    # 筛选符合条件的股票
    print("\n" + "="*60)
    print("🎯 筛选结果")
    print("="*60)
    
    filtered = []
    for r in results:
        score = 0
        reasons = []
        
        # 趋势条件
        if r['signal'] == 1:
            score += 2
            reasons.append("技术面买入信号")
        
        # 风险条件
        if r['risk_rating'] in ['低风险', '中风险']:
            score += 1
            reasons.append(f"风险评级:{r['risk_rating']}")
        
        # 收益条件
        if r['analysis']['sharpe_ratio'] > 0.5:
            score += 2
            reasons.append(f"夏普比率:{r['analysis']['sharpe_ratio']:.2f}")
        
        if r['analysis']['total_return'] > 0.1:
            score += 1
            reasons.append(f"总收益:{r['analysis']['total_return']:.2%}")
        
        # 波动率条件
        if r['analysis']['volatility'] < 0.4:
            score += 1
            reasons.append(f"波动率:{r['analysis']['volatility']:.2%}")
        
        r['score'] = score
        r['reasons'] = reasons
        
        if score >= 3:
            filtered.append(r)
    
    # 按分数排序
    filtered.sort(key=lambda x: x['score'], reverse=True)
    
    # 输出 Top 3
    print(f"\n✅ 筛选出 {len(filtered)} 只符合条件的股票")
    print(f"\n🏆 推荐 Top 3:\n")
    
    for i, stock in enumerate(filtered[:3], 1):
        print(f"{i}. {stock['name']} ({stock['symbol']})")
        print(f"   当前价：{stock['price']:.2f} 元")
        print(f"   评分：{'⭐'*stock['score']} ({stock['score']}分)")
        print(f"   理由:")
        for reason in stock['reasons']:
            print(f"      • {reason}")
        
        # 投资建议
        position = RiskAnalysis.position_sizing(capital/3)
        print(f"   💰 建议仓位：{position:.0f} 元 (约{position/stock['price']:.0f}股)")
        print(f"   🛑 止损价：{stock['price']*0.95:.2f} 元 (-5%)")
        print(f"   🎯 目标价：{stock['price']*1.15:.2f} 元 (+15%)")
        print()
    
    return filtered[:3]


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 量化交易分析系统")
    print("="*60)
    print(f"💰 默认资金：{TradingConfig.DEFAULT_CAPITAL:,.0f} 元")
    print(f"📊 单只最大仓位：{TradingConfig.MAX_POSITION:.0%}")
    print(f"🛑 止损比例：{TradingConfig.STOP_LOSS:.0%}")
    print(f"🎯 止盈比例：{TradingConfig.TAKE_PROFIT:.0%}")
    
    # 执行选股
    top_stocks = select_stocks(TradingConfig.DEFAULT_CAPITAL)
    
    if len(top_stocks) >= 3:
        print("\n" + "="*60)
        print("📋 投资总结")
        print("="*60)
        print(f"推荐 3 只股票，总建议投入：{TradingConfig.DEFAULT_CAPITAL:,.0f} 元")
        print("⚠️ 以上分析仅供参考，不构成投资建议")
        print("⚠️ 股市有风险，投资需谨慎")
        print("="*60 + "\n")
    else:
        print("\n⚠️ 未找到足够符合条件的股票，建议观望")
