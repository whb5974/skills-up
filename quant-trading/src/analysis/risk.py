"""
风险分析模块
包含风险评估和资金管理
"""
import pandas as pd
import numpy as np
from loguru import logger

class RiskAnalysis:
    """风险分析工具类"""
    
    @staticmethod
    def calculate_returns(prices):
        """计算收益率序列"""
        return prices.pct_change().dropna()
    
    @staticmethod
    def calculate_volatility(returns, annualize=True):
        """
        计算波动率
        
        Args:
            returns: 收益率序列
            annualize: 是否年化 (A 股约 242 交易日)
        """
        vol = returns.std()
        if annualize:
            vol = vol * np.sqrt(242)
        return vol
    
    @staticmethod
    def calculate_max_drawdown(prices):
        """
        计算最大回撤
        
        Returns:
            float: 最大回撤比例
        """
        cum_max = prices.cummax()
        drawdown = (prices - cum_max) / cum_max
        return drawdown.min()
    
    @staticmethod
    def calculate_sharpe_ratio(returns, risk_free_rate=0.03):
        """
        计算夏普比率
        
        Args:
            returns: 收益率序列
            risk_free_rate: 无风险利率 (默认 3%)
        
        Returns:
            float: 夏普比率
        """
        excess_return = returns.mean() * 242 - risk_free_rate
        volatility = returns.std() * np.sqrt(242)
        if volatility == 0:
            return 0
        return excess_return / volatility
    
    @staticmethod
    def calculate_var(returns, confidence=0.95):
        """
        计算 VaR (Value at Risk)
        
        Args:
            returns: 收益率序列
            confidence: 置信水平 (默认 95%)
        
        Returns:
            float: VaR 值
        """
        return returns.quantile(1 - confidence)
    
    @staticmethod
    def calculate_beta(stock_returns, market_returns):
        """
        计算 Beta 系数
        
        Args:
            stock_returns: 股票收益率
            market_returns: 市场收益率
        
        Returns:
            float: Beta 系数
        """
        covariance = np.cov(stock_returns, market_returns)[0][1]
        market_variance = np.var(market_returns)
        if market_variance == 0:
            return 0
        return covariance / market_variance
    
    @staticmethod
    def analyze_stock(df, stock_name=''):
        """
        全面分析一只股票的风险指标
        
        Args:
            df: 包含 close 列的 DataFrame
            stock_name: 股票名称
        
        Returns:
            dict: 风险指标
        """
        returns = RiskAnalysis.calculate_returns(df['close'])
        
        analysis = {
            'stock': stock_name,
            'volatility': RiskAnalysis.calculate_volatility(returns),
            'max_drawdown': RiskAnalysis.calculate_max_drawdown(df['close']),
            'sharpe_ratio': RiskAnalysis.calculate_sharpe_ratio(returns),
            'var_95': RiskAnalysis.calculate_var(returns, 0.95),
            'avg_return': returns.mean() * 242,  # 年化
            'total_return': (df['close'].iloc[-1] / df['close'].iloc[0]) - 1
        }
        
        return analysis
    
    @staticmethod
    def risk_rating(analysis):
        """
        根据指标给出风险评级
        
        Returns:
            str: 风险等级 (低/中/高)
        """
        score = 0
        
        # 波动率评分
        if analysis['volatility'] < 0.3:
            score += 1
        elif analysis['volatility'] > 0.6:
            score -= 1
        
        # 最大回撤评分
        if analysis['max_drawdown'] > -0.2:
            score += 1
        elif analysis['max_drawdown'] < -0.4:
            score -= 1
        
        # 夏普比率评分
        if analysis['sharpe_ratio'] > 1.5:
            score += 1
        elif analysis['sharpe_ratio'] < 0:
            score -= 1
        
        if score >= 2:
            return '低风险'
        elif score <= -1:
            return '高风险'
        else:
            return '中风险'
    
    @staticmethod
    def position_sizing(capital, risk_per_trade=0.02, stop_loss=0.05):
        """
        计算仓位大小 (基于风险)
        
        Args:
            capital: 总资金
            risk_per_trade: 每笔交易风险 (默认 2%)
            stop_loss: 止损比例 (默认 5%)
        
        Returns:
            float: 建议仓位金额
        """
        risk_amount = capital * risk_per_trade
        position = risk_amount / stop_loss
        return min(position, capital * 0.3)  # 单只不超过 30%


# 测试
if __name__ == "__main__":
    # 创建测试数据
    np.random.seed(42)
    prices = pd.Series(100 + np.cumsum(np.random.randn(252)))
    
    analysis = RiskAnalysis.analyze_stock(pd.DataFrame({'close': prices}), '测试股票')
    
    print("\n📊 风险分析结果:")
    for key, value in analysis.items():
        if isinstance(value, float):
            print(f"   {key}: {value:.4f}")
        else:
            print(f"   {key}: {value}")
    
    rating = RiskAnalysis.risk_rating(analysis)
    print(f"\n🎯 风险评级：{rating}")
    
    position = RiskAnalysis.position_sizing(100000)
    print(f"\n💰 建议仓位：{position:.2f} 元")
