"""
投资风险分析计算器

功能:
- 计算投资组合的风险指标
- 夏普比率、最大回撤、VaR 等
- 风险评估与建议
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from loguru import logger


class RiskCalculator:
    """投资风险分析器"""
    
    def __init__(self):
        logger.info("✅ 风险分析器初始化完成")
    
    def calculate_returns(self, prices):
        """计算收益率序列"""
        if isinstance(prices, list):
            prices = pd.Series(prices)
        return prices.pct_change().dropna()
    
    def calculate_volatility(self, returns, annualize=True):
        """
        计算波动率
        
        Args:
            returns: 收益率序列
            annualize: 是否年化 (A 股 242 交易日)
        """
        vol = returns.std()
        if annualize:
            vol = vol * np.sqrt(242)
        return vol
    
    def calculate_max_drawdown(self, prices):
        """
        计算最大回撤
        
        Returns:
            float: 最大回撤比例 (负值)
        """
        if isinstance(prices, list):
            prices = pd.Series(prices)
        
        cum_max = prices.cummax()
        drawdown = (prices - cum_max) / cum_max
        return drawdown.min()
    
    def calculate_sharpe_ratio(self, returns, risk_free_rate=0.03):
        """
        计算夏普比率
        
        Args:
            returns: 收益率序列
            risk_free_rate: 无风险利率 (默认 3%)
        
        Returns:
            float: 夏普比率
        """
        if len(returns) < 2:
            return 0
        
        excess_return = returns.mean() * 242 - risk_free_rate
        volatility = returns.std() * np.sqrt(242)
        
        if volatility == 0:
            return 0
        
        return excess_return / volatility
    
    def calculate_var(self, returns, confidence=0.95):
        """
        计算 VaR (Value at Risk)
        
        Args:
            returns: 收益率序列
            confidence: 置信水平 (默认 95%)
        
        Returns:
            float: VaR 值 (负值表示损失)
        """
        return returns.quantile(1 - confidence)
    
    def calculate_beta(self, stock_returns, market_returns):
        """
        计算 Beta 系数
        
        Args:
            stock_returns: 股票收益率
            market_returns: 市场收益率
        
        Returns:
            float: Beta 系数
        """
        if len(stock_returns) < 2 or len(market_returns) < 2:
            return 1
        
        # 对齐数据
        min_len = min(len(stock_returns), len(market_returns))
        stock_returns = stock_returns.iloc[:min_len]
        market_returns = market_returns.iloc[:min_len]
        
        covariance = np.cov(stock_returns, market_returns)[0][1]
        market_variance = np.var(market_returns)
        
        if market_variance == 0:
            return 1
        
        return covariance / market_variance
    
    def calculate_sortino_ratio(self, returns, risk_free_rate=0.03):
        """
        计算索提诺比率 (只考虑下行波动)
        
        Returns:
            float: 索提诺比率
        """
        if len(returns) < 2:
            return 0
        
        excess_return = returns.mean() * 242 - risk_free_rate
        
        # 下行标准差
        downside_returns = returns[returns < 0]
        if len(downside_returns) == 0:
            return float('inf')
        
        downside_std = downside_returns.std() * np.sqrt(242)
        
        if downside_std == 0:
            return float('inf')
        
        return excess_return / downside_std
    
    def analyze_portfolio(self, positions, market_returns=None):
        """
        全面分析投资组合
        
        Args:
            positions: dict, 持仓数据
                {
                    'symbol': {
                        'name': str,
                        'shares': int,
                        'cost_basis': float,
                        'current_price': float,
                        'history': list  # 历史价格 (可选)
                    }
                }
            market_returns: 市场收益率序列 (用于计算 Beta)
        
        Returns:
            dict: 风险分析结果
        """
        results = {
            'positions': [],
            'portfolio': {},
            'risk_rating': '',
            'suggestions': []
        }
        
        total_value = 0
        total_cost = 0
        
        # 分析每个持仓
        for symbol, pos in positions.items():
            market_value = pos['shares'] * pos['current_price']
            cost_value = pos['shares'] * pos['cost_basis']
            profit = market_value - cost_value
            profit_pct = (profit / cost_value) * 100 if cost_value > 0 else 0
            
            position_analysis = {
                'symbol': symbol,
                'name': pos['name'],
                'market_value': market_value,
                'cost_value': cost_value,
                'profit': profit,
                'profit_pct': profit_pct,
                'weight': 0,
                'volatility': 0,
                'risk_rating': '中'
            }
            
            # 如果有历史数据，计算风险指标
            if 'history' in pos and len(pos['history']) > 20:
                history = pd.Series(pos['history'])
                returns = self.calculate_returns(history)
                position_analysis['volatility'] = self.calculate_volatility(returns)
                
                # 风险评级
                vol = position_analysis['volatility']
                if vol < 0.3:
                    position_analysis['risk_rating'] = '低'
                elif vol > 0.6:
                    position_analysis['risk_rating'] = '高'
            
            results['positions'].append(position_analysis)
            total_value += market_value
            total_cost += cost_value
        
        # 组合整体分析
        total_profit = total_value - total_cost
        total_profit_pct = (total_profit / total_cost) * 100 if total_cost > 0 else 0
        
        results['portfolio'] = {
            'total_value': total_value,
            'total_cost': total_cost,
            'total_profit': total_profit,
            'total_profit_pct': total_profit_pct,
        }
        
        # 计算权重
        for pos in results['positions']:
            pos['weight'] = (pos['market_value'] / total_value) * 100 if total_value > 0 else 0
        
        # 整体风险评估
        avg_volatility = np.average(
            [p['volatility'] for p in results['positions']],
            weights=[p['weight'] for p in results['positions']]
        ) if results['positions'] else 0
        
        results['portfolio']['avg_volatility'] = avg_volatility
        
        # 风险评级
        if avg_volatility < 0.35:
            results['risk_rating'] = '低风险'
        elif avg_volatility > 0.55:
            results['risk_rating'] = '高风险'
        else:
            results['risk_rating'] = '中风险'
        
        # 生成建议
        results['suggestions'] = self.generate_suggestions(results)
        
        return results
    
    def generate_suggestions(self, analysis):
        """根据分析结果生成投资建议"""
        suggestions = []
        
        portfolio = analysis['portfolio']
        positions = analysis['positions']
        
        # 集中度风险
        max_weight = max([p['weight'] for p in positions]) if positions else 0
        if max_weight > 30:
            suggestions.append(f"⚠️ 集中度过高：单只股票占比{max_weight:.1f}%，建议分散至 20% 以下")
        
        # 高风险资产比例
        high_risk = [p for p in positions if p['risk_rating'] == '高']
        high_risk_weight = sum([p['weight'] for p in high_risk])
        if high_risk_weight > 40:
            suggestions.append(f"⚠️ 高风险资产占比{high_risk_weight:.1f}%，建议降低至 30% 以下")
        
        # 整体收益
        if portfolio['total_profit_pct'] > 30:
            suggestions.append("✅ 收益良好，考虑止盈部分仓位锁定利润")
        elif portfolio['total_profit_pct'] < -15:
            suggestions.append("⚠️ 亏损较大，检查是否触及止损线")
        
        # 波动率
        if portfolio.get('avg_volatility', 0) > 0.5:
            suggestions.append("⚠️ 组合波动率较高，建议增加债券或货币基金配置")
        
        if not suggestions:
            suggestions.append("✅ 组合风险可控，继续保持")
        
        return suggestions
    
    def print_report(self, analysis):
        """打印风险分析报告"""
        print("\n" + "=" * 60)
        print("📊 投资风险分析报告")
        print("=" * 60)
        
        print(f"\n🎯 整体风险评级：{analysis['risk_rating']}")
        
        print(f"\n💰 组合概况")
        p = analysis['portfolio']
        print(f"   总资产：{p['total_value']:,.2f} 元")
        print(f"   总成本：{p['total_cost']:,.2f} 元")
        print(f"   总盈亏：{p['total_profit']:+,.2f} 元 ({p['total_profit_pct']:+.2f}%)")
        print(f"   平均波动率：{p.get('avg_volatility', 0):.2%}")
        
        print(f"\n📋 持仓风险明细")
        print("-" * 60)
        print(f"{'代码':<8} {'名称':<10} {'仓位':>8} {'盈亏':>12} {'风险':>8} {'波动率':>10}")
        print("-" * 60)
        
        for pos in sorted(analysis['positions'], key=lambda x: x['weight'], reverse=True):
            profit_str = f"{pos['profit']:+,.0f}({pos['profit_pct']:+.1f}%)"
            vol_str = f"{pos['volatility']:.2%}" if pos['volatility'] > 0 else 'N/A'
            print(
                f"{pos['symbol']:<8} {pos['name']:<10} {pos['weight']:>7.1f}% "
                f"{profit_str:>12} {pos['risk_rating']:>8} {vol_str:>10}"
            )
        
        print("-" * 60)
        
        print(f"\n💡 投资建议")
        for i, sug in enumerate(analysis['suggestions'], 1):
            print(f"   {i}. {sug}")
        
        print("\n" + "=" * 60)


# 测试
if __name__ == "__main__":
    calculator = RiskCalculator()
    
    # 模拟持仓
    positions = {
        '600000': {
            'name': '浦发银行',
            'shares': 1000,
            'cost_basis': 8.5,
            'current_price': 9.2,
            'history': [8.0 + np.cumsum(np.random.randn(60))]
        },
        '600519': {
            'name': '贵州茅台',
            'shares': 50,
            'cost_basis': 1800,
            'current_price': 1950,
            'history': [1700 + np.cumsum(np.random.randn(60))]
        },
        '000858': {
            'name': '五粮液',
            'shares': 200,
            'cost_basis': 150,
            'current_price': 145,
            'history': [140 + np.cumsum(np.random.randn(60))]
        }
    }
    
    analysis = calculator.analyze_portfolio(positions)
    calculator.print_report(analysis)
