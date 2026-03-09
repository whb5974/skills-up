"""
投资组合跟踪器
用于记录和分析投资收益与风险

使用方法:
    python portfolio-tracker.py --init     # 初始化组合
    python portfolio-tracker.py --add      # 添加持仓
    python portfolio-tracker.py --update   # 更新价格
    python portfolio-tracker.py --report   # 生成报告
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from loguru import logger
import sys

# 数据文件
DATA_DIR = Path(__file__).parent / 'data'
DATA_DIR.mkdir(exist_ok=True)

PORTFOLIO_FILE = DATA_DIR / 'portfolio.json'
TRANSACTIONS_FILE = DATA_DIR / 'transactions.csv'
REPORTS_DIR = DATA_DIR / 'reports'
REPORTS_DIR.mkdir(exist_ok=True)


class PortfolioTracker:
    """投资组合跟踪器"""
    
    def __init__(self):
        self.portfolio = self.load_portfolio()
        self.transactions = self.load_transactions()
        logger.info("✅ 投资组合跟踪器初始化完成")
    
    def load_portfolio(self):
        """加载持仓数据"""
        if PORTFOLIO_FILE.exists():
            with open(PORTFOLIO_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'cash': 100000,  # 初始资金
            'positions': {},  # 持仓
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'initial_capital': 100000
        }
    
    def save_portfolio(self):
        """保存持仓数据"""
        with open(PORTFOLIO_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.portfolio, f, ensure_ascii=False, indent=2)
        logger.info("💾 持仓数据已保存")
    
    def load_transactions(self):
        """加载交易记录"""
        transactions = []
        if TRANSACTIONS_FILE.exists():
            with open(TRANSACTIONS_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                transactions = list(reader)
        return transactions
    
    def save_transaction(self, transaction):
        """保存交易记录"""
        is_new = not TRANSACTIONS_FILE.exists()
        with open(TRANSACTIONS_FILE, 'a', encoding='utf-8', newline='') as f:
            fieldnames = ['date', 'type', 'symbol', 'name', 'price', 
                         'shares', 'amount', 'fee', 'note']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if is_new:
                writer.writeheader()
            writer.writerow(transaction)
    
    def add_position(self, symbol, name, shares, price, fee=0, note=''):
        """
        添加/增加持仓
        
        Args:
            symbol: 代码
            name: 名称
            shares: 数量
            price: 价格
            fee: 手续费
            note: 备注
        """
        amount = shares * price + fee
        if amount > self.portfolio['cash']:
            logger.error(f"❌ 资金不足！需要{amount:.2f}元，可用{self.portfolio['cash']:.2f}元")
            return False
        
        # 扣减现金
        self.portfolio['cash'] -= amount
        
        # 更新持仓
        if symbol not in self.portfolio['positions']:
            self.portfolio['positions'][symbol] = {
                'name': name,
                'shares': 0,
                'cost_basis': 0,
                'current_price': price
            }
        
        pos = self.portfolio['positions'][symbol]
        old_shares = pos['shares']
        old_cost = pos['shares'] * pos['cost_basis']
        
        new_shares = old_shares + shares
        new_cost = old_cost + (shares * price) + fee
        pos['shares'] = new_shares
        pos['cost_basis'] = new_cost / new_shares if new_shares > 0 else 0
        pos['current_price'] = price
        
        # 保存交易记录
        self.save_transaction({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': 'BUY',
            'symbol': symbol,
            'name': name,
            'price': price,
            'shares': shares,
            'amount': amount,
            'fee': fee,
            'note': note
        })
        
        self.save_portfolio()
        logger.info(f"✅ 买入 {name}({symbol}) {shares}股 @ {price:.2f}元")
        return True
    
    def sell_position(self, symbol, shares, price, fee=0, note=''):
        """
        卖出持仓
        
        Args:
            symbol: 代码
            shares: 数量
            price: 价格
            fee: 手续费
            note: 备注
        """
        if symbol not in self.portfolio['positions']:
            logger.error(f"❌ 未持有 {symbol}")
            return False
        
        pos = self.portfolio['positions'][symbol]
        if pos['shares'] < shares:
            logger.error(f"❌ 持仓不足！持有{pos['shares']}股，欲卖出{shares}股")
            return False
        
        # 计算收益
        amount = shares * price - fee
        cost = shares * pos['cost_basis']
        profit = amount - cost
        
        # 增加现金
        self.portfolio['cash'] += amount
        
        # 更新持仓
        pos['shares'] -= shares
        if pos['shares'] == 0:
            del self.portfolio['positions'][symbol]
        
        # 保存交易记录
        self.save_transaction({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': 'SELL',
            'symbol': symbol,
            'name': pos['name'],
            'price': price,
            'shares': shares,
            'amount': amount,
            'fee': fee,
            'note': f'{note} | 盈亏：{profit:.2f}元'
        })
        
        self.save_portfolio()
        logger.info(f"✅ 卖出 {pos['name']}({symbol}) {shares}股 @ {price:.2f}元 | 盈亏：{profit:.2f}元")
        return True
    
    def update_price(self, symbol, price):
        """更新当前价格"""
        if symbol in self.portfolio['positions']:
            self.portfolio['positions'][symbol]['current_price'] = price
    
    def get_portfolio_value(self):
        """计算组合总价值"""
        positions_value = sum(
            pos['shares'] * pos['current_price']
            for pos in self.portfolio['positions'].values()
        )
        return self.portfolio['cash'] + positions_value
    
    def get_portfolio_summary(self):
        """获取组合概览"""
        total_value = self.get_portfolio_value()
        initial = self.portfolio['initial_capital']
        total_return = total_value - initial
        return_pct = (total_return / initial) * 100
        
        summary = {
            'total_value': total_value,
            'cash': self.portfolio['cash'],
            'positions_value': total_value - self.portfolio['cash'],
            'initial_capital': initial,
            'total_return': total_return,
            'return_pct': return_pct,
            'positions': []
        }
        
        for symbol, pos in self.portfolio['positions'].items():
            market_value = pos['shares'] * pos['current_price']
            cost_value = pos['shares'] * pos['cost_basis']
            profit = market_value - cost_value
            profit_pct = (profit / cost_value) * 100 if cost_value > 0 else 0
            
            summary['positions'].append({
                'symbol': symbol,
                'name': pos['name'],
                'shares': pos['shares'],
                'cost_basis': pos['cost_basis'],
                'current_price': pos['current_price'],
                'market_value': market_value,
                'cost_value': cost_value,
                'profit': profit,
                'profit_pct': profit_pct,
                'weight': (market_value / total_value) * 100 if total_value > 0 else 0
            })
        
        return summary
    
    def generate_report(self):
        """生成投资报告"""
        summary = self.get_portfolio_summary()
        
        report = []
        report.append("=" * 60)
        report.append("📊 投资组合报告")
        report.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 60)
        report.append("")
        report.append("💰 总体情况")
        report.append(f"   总资产：{summary['total_value']:,.2f} 元")
        report.append(f"   现金：{summary['cash']:,.2f} 元")
        report.append(f"   持仓市值：{summary['positions_value']:,.2f} 元")
        report.append("")
        report.append("📈 收益情况")
        report.append(f"   初始资金：{summary['initial_capital']:,.2f} 元")
        report.append(f"   总收益：{summary['total_return']:,.2f} 元")
        report.append(f"   收益率：{summary['return_pct']:.2f}%")
        report.append("")
        
        if summary['positions']:
            report.append("📋 持仓明细")
            report.append("-" * 60)
            report.append(f"{'代码':<8} {'名称':<10} {'数量':>8} {'成本':>10} {'现价':>10} {'盈亏':>10} {'仓位':>8}")
            report.append("-" * 60)
            
            for pos in sorted(summary['positions'], key=lambda x: x['weight'], reverse=True):
                profit_str = f"{pos['profit']:+,.0f}({pos['profit_pct']:+.1f}%)"
                report.append(
                    f"{pos['symbol']:<8} {pos['name']:<10} {pos['shares']:>8} "
                    f"{pos['cost_basis']:>10.2f} {pos['current_price']:>10.2f} "
                    f"{profit_str:>10} {pos['weight']:>7.1f}%"
                )
            
            report.append("-" * 60)
        
        # 保存报告
        report_text = '\n'.join(report)
        report_file = REPORTS_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        logger.info(f"📄 报告已保存至：{report_file}")
        return report_text


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='投资组合跟踪器')
    parser.add_argument('--init', action='store_true', help='初始化组合')
    parser.add_argument('--add', action='store_true', help='添加持仓')
    parser.add_argument('--sell', action='store_true', help='卖出持仓')
    parser.add_argument('--update', action='store_true', help='更新价格')
    parser.add_argument('--report', action='store_true', help='生成报告')
    
    args = parser.parse_args()
    
    tracker = PortfolioTracker()
    
    if args.init:
        initial = float(input("初始资金 (元): ") or 100000)
        tracker.portfolio['initial_capital'] = initial
        tracker.portfolio['cash'] = initial
        tracker.save_portfolio()
        print(f"✅ 组合已初始化，初始资金：{initial:,.2f} 元")
    
    elif args.add:
        symbol = input("股票代码：")
        name = input("股票名称：")
        shares = int(input("数量 (股): ") or 0)
        price = float(input("价格 (元): ") or 0)
        fee = float(input("手续费 (元): ") or 0)
        note = input("备注：")
        tracker.add_position(symbol, name, shares, price, fee, note)
    
    elif args.sell:
        symbol = input("股票代码：")
        shares = int(input("数量 (股): ") or 0)
        price = float(input("价格 (元): ") or 0)
        fee = float(input("手续费 (元): ") or 0)
        note = input("备注：")
        tracker.sell_position(symbol, shares, price, fee, note)
    
    elif args.update:
        symbol = input("股票代码 (留空批量更新): ")
        if symbol:
            price = float(input("当前价格：") or 0)
            tracker.update_price(symbol, price)
            tracker.save_portfolio()
        else:
            for sym, pos in tracker.portfolio['positions'].items():
                price = float(input(f"{pos['name']}({sym}) 当前价格：") or pos['current_price'])
                tracker.update_price(sym, price)
            tracker.save_portfolio()
        print("✅ 价格已更新")
    
    elif args.report:
        report = tracker.generate_report()
        print("\n" + report)
    
    else:
        # 默认显示报告
        report = tracker.generate_report()
        print("\n" + report)


if __name__ == "__main__":
    main()
