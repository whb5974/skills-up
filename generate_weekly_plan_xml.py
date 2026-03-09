#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络安全公司周计划报表生成器 - 纯 Python 版（无需外部库）
基于 2025-2026 年工作量分析与战略规划报告
生成 Excel 兼容的 SpreadsheetML XML 格式
"""

from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

# ============================================================
# Excel SpreadsheetML 命名空间
# ============================================================
NS = {
    'ss': 'urn:schemas-microsoft-com:office:spreadsheet',
    'o': 'urn:schemas-microsoft-com:office:office',
    'x': 'urn:schemas-microsoft-com:office:excel',
    'html': 'http://www.w3.org/TR/REC-html40'
}

# ============================================================
# 样式定义
# ============================================================
STYLES = '''
    <ss:Styles>
        <ss:Style ss:ID="Default" ss:Name="Normal">
            <ss:Alignment ss:Vertical="Center"/>
            <ss:Borders/>
            <ss:Font ss:FontName="微软雅黑" ss:Size="10"/>
            <ss:Interior/>
            <ss:NumberFormat/>
            <ss:Protection/>
        </ss:Style>
        <ss:Style ss:ID="sTitle">
            <ss:Alignment ss:Horizontal="Center" ss:Vertical="Center" ss:WrapText="1"/>
            <ss:Font ss:FontName="微软雅黑" ss:Size="16" ss:Bold="1" ss:Color="#FFFFFF"/>
            <ss:Interior ss:Color="#1F4E79" ss:Pattern="Solid"/>
        </ss:Style>
        <ss:Style ss:ID="sHeader">
            <ss:Alignment ss:Horizontal="Center" ss:Vertical="Center" ss:WrapText="1"/>
            <ss:Font ss:FontName="微软雅黑" ss:Size="11" ss:Bold="1" ss:Color="#FFFFFF"/>
            <ss:Interior ss:Color="#2E75B6" ss:Pattern="Solid"/>
        </ss:Style>
        <ss:Style ss:ID="sNormal">
            <ss:Alignment ss:Horizontal="Center" ss:Vertical="Center" ss:WrapText="1"/>
            <ss:Font ss:FontName="微软雅黑" ss:Size="10"/>
            <ss:Borders>
                <ss:Left ss:Weight="1"/>
                <ss:Right ss:Weight="1"/>
                <ss:Top ss:Weight="1"/>
                <ss:Bottom ss:Weight="1"/>
            </ss:Borders>
        </ss:Style>
        <ss:Style ss:ID="sLeft">
            <ss:Alignment ss:Horizontal="Left" ss:Vertical="Center" ss:WrapText="1"/>
            <ss:Font ss:FontName="微软雅黑" ss:Size="10"/>
            <ss:Borders>
                <ss:Left ss:Weight="1"/>
                <ss:Right ss:Weight="1"/>
                <ss:Top ss:Weight="1"/>
                <ss:Bottom ss:Weight="1"/>
            </ss:Borders>
        </ss:Style>
        <ss:Style ss:ID="sDanger">
            <ss:Alignment ss:Horizontal="Center" ss:Vertical="Center" ss:WrapText="1"/>
            <ss:Font ss:FontName="微软雅黑" ss:Size="10"/>
            <ss:Borders>
                <ss:Left ss:Weight="1"/>
                <ss:Right ss:Weight="1"/>
                <ss:Top ss:Weight="1"/>
                <ss:Bottom ss:Weight="1"/>
            </ss:Borders>
            <ss:Interior ss:Color="#FFC7CE" ss:Pattern="Solid"/>
        </ss:Style>
        <ss:Style ss:ID="sWarning">
            <ss:Alignment ss:Horizontal="Center" ss:Vertical="Center" ss:WrapText="1"/>
            <ss:Font ss:FontName="微软雅黑" ss:Size="10"/>
            <ss:Borders>
                <ss:Left ss:Weight="1"/>
                <ss:Right ss:Weight="1"/>
                <ss:Top ss:Weight="1"/>
                <ss:Bottom ss:Weight="1"/>
            </ss:Borders>
            <ss:Interior ss:Color="#FFEB9C" ss:Pattern="Solid"/>
        </ss:Style>
        <ss:Style ss:ID="sSuccess">
            <ss:Alignment ss:Horizontal="Center" ss:Vertical="Center" ss:WrapText="1"/>
            <ss:Font ss:FontName="微软雅黑" ss:Size="10"/>
            <ss:Borders>
                <ss:Left ss:Weight="1"/>
                <ss:Right ss:Weight="1"/>
                <ss:Top ss:Weight="1"/>
                <ss:Bottom ss:Weight="1"/>
            </ss:Borders>
            <ss:Interior ss:Color="#C6EFCE" ss:Pattern="Solid"/>
        </ss:Style>
        <ss:Style ss:ID="sInfo">
            <ss:Alignment ss:Horizontal="Center" ss:Vertical="Center" ss:WrapText="1"/>
            <ss:Font ss:FontName="微软雅黑" ss:Size="10"/>
            <ss:Borders>
                <ss:Left ss:Weight="1"/>
                <ss:Right ss:Weight="1"/>
                <ss:Top ss:Weight="1"/>
                <ss:Bottom ss:Weight="1"/>
            </ss:Borders>
            <ss:Interior ss:Color="#D6EAF8" ss:Pattern="Solid"/>
        </ss:Style>
        <ss:Style ss:ID="sBold">
            <ss:Font ss:FontName="微软雅黑" ss:Size="11" ss:Bold="1"/>
        </ss:Style>
    </ss:Styles>
'''

def create_cell(value, style="sNormal"):
    """创建单元格"""
    if value is None:
        value = ""
    return f'<ss:Cell ss:StyleID="{style}"><ss:Data ss:Type="String">{value}</ss:Data></ss:Cell>'

def create_row(cells, style=None):
    """创建行"""
    return f'<ss:Row ss:AutoFitHeight="0">{"".join(cells)}</ss:Row>'

def create_worksheet(name, headers, data, col_widths=None):
    """创建工作表"""
    # 表头
    header_cells = [create_cell(h, "sHeader") for h in headers]
    header_row = create_row(header_cells)
    
    # 数据行
    data_rows = []
    for row_data in data:
        cells = []
        for i, value in enumerate(row_data):
            # 根据内容选择样式
            style = "sNormal"
            if str(value) == "🔴" or str(value) == "P0" or str(value) == "高":
                style = "sDanger"
            elif str(value) == "🟡" or str(value) == "P1" or str(value) == "中":
                style = "sWarning"
            elif str(value) == "🟢":
                style = "sSuccess"
            elif str(value) == "⚪" or str(value) == "低":
                style = "sInfo"
            
            # 长文本使用左对齐
            if len(str(value)) > 30:
                style = "sLeft"
            
            cells.append(create_cell(value, style))
        data_rows.append(create_row(cells))
    
    # 列宽
    width_xml = ""
    if col_widths:
        for i, w in enumerate(col_widths, 1):
            width_xml += f'<ss:Column ss:Index="{i}" ss:Width="{w}"/>'
    
    worksheet = f'''<ss:Worksheet ss:Name="{name}">
    <ss:Table>
        {width_xml}
        {header_row}
        {"".join(data_rows)}
    </ss:Table>
</ss:Worksheet>'''
    return worksheet

# ============================================================
# 数据定义
# ============================================================

# 核心指标看板数据
KPI_DATA = [
    ["安服部", "人均工时 (小时/周)", "18.4", "15.0", "", "", "🔴"],
    ["安服部", "项目交付数 (个/周)", "7.5", "9.0", "", "", "🟡"],
    ["安服部", "客户应急任务 (个/周)", "0.56", "0.5", "", "", "🟡"],
    ["安服部", "售前支持转化率 (%)", "待统计", "≥30%", "", "", "⚪"],
    ["合规部", "报告产出 (份/周)", "27.8", "31.5", "", "", "🟡"],
    ["合规部", "项目完成率 (%)", "90.46%", "≥95%", "", "", "🔴"],
    ["合规部", "未完成项目清理 (个)", "69", "0", "", "", "🔴"],
    ["合规部", "密评报告 (份/周)", "0", "2", "", "", "⚪"],
    ["质量部", "审核文档 (份/周)", "87.3", "100", "", "", "🟡"],
    ["质量部", "审核及时率 (%)", "待统计", "≥98%", "", "", "⚪"],
    ["质量部", "数据准确性核实", "待完成", "已完成", "", "", "🔴"],
    ["研发部", "软著申请 (项/年)", "6", "15", "", "", "🔴"],
    ["研发部", "技术复用率 (%)", "待统计", "≥40%", "", "", "⚪"],
    ["研发部", "资质维护 (个)", "18", "18", "", "", "🟢"],
    ["综合技术部", "非常规任务 (项/周)", "2.7", "2.0", "", "", "🔴"],
    ["综合技术部", "任务产品化率 (%)", "待统计", "≥50%", "", "", "⚪"],
    ["太原中心", "人均任务负荷 (人天/周)", "7.0", "5.0", "", "", "🔴"],
    ["太原中心", "任务完成率 (%)", "85.7%", "≥95%", "", "", "🔴"],
    ["整体", "人员增编进度 (人)", "0", "12-19", "", "", "🔴"],
    ["整体", "回款率提升 (%)", "基准", "+10%", "", "", "🟡"],
    ["整体", "NPS 客户满意度", "待调研", "≥50", "", "", "⚪"],
]

# 第 1-4 周计划数据
WEEK1_4_DATA = [
    ["第 1 周", "HR+ 安服部", "安服部人员负荷调研启动", "加班工时统计覆盖率", "100%", "", "进行中", "需协调打卡数据接入", "优先获取近 3 个月数据", "P0"],
    ["第 1 周", "质量部", "2025/2026 数据核实", "数据差异报告", "完成核实", "", "进行中", "2026 预估数据存在矛盾", "与财务/运营对表", "P0"],
    ["第 1 周", "合规部", "69 个未完成项目梳理", "项目状态清单", "100% 梳理", "", "进行中", "部分项目客户原因延期", "分类制定清理策略", "P0"],
    ["第 1 周", "财务部", "客户应急收费政策起草", "政策文件初稿", "完成起草", "", "未开始", "需明确收费标准和审批流程", "参考行业标准", "P0"],
    ["第 1 周", "HR", "Top20 核心人员访谈计划", "访谈名单确认", "完成名单", "", "进行中", "需部门总监配合", "制定访谈提纲", "P0"],
    ["第 1 周", "运营部", "周度数据统计模板设计", "模板定稿", "完成设计", "", "进行中", "各部门统计口径不一致", "统一指标定义", "P1"],
    ["第 2 周", "HR+ 安服部", "人员负荷调研数据分析", "加班分析报告", "完成报告", "", "未开始", "待第 1 周数据收集", "识别过劳高风险人员", "P0"],
    ["第 2 周", "质量部", "数据核实报告提交", "核实报告", "提交管理层", "", "未开始", "待核实完成", "提出数据治理建议", "P0"],
    ["第 2 周", "合规部", "未完成项目清理行动 (1/4)", "清理目标 17 个", "17 个", "", "未开始", "客户配合度可能不足", "建立客户沟通机制", "P0"],
    ["第 2 周", "财务部", "应急收费政策评审", "政策定稿", "通过评审", "", "未开始", "需管理层审批", "准备汇报材料", "P0"],
    ["第 2 周", "HR", "核心人员访谈 (1/4)", "完成 5 人访谈", "5 人", "", "未开始", "需协调时间", "记录关键反馈", "P0"],
    ["第 2 周", "HR", "安服部招聘需求发布", "JD 发布", "完成发布", "", "未开始", "需确定薪资范围", "同步启动猎头合作", "P0"],
    ["第 2 周", "运营部", "数据统计模板培训", "培训覆盖率", "100%", "", "未开始", "需协调各部门时间", "录制培训视频", "P1"],
    ["第 3 周", "安服部", "加班缓解措施实施", "人均工时下降", "10%", "", "未开始", "业务高峰期难以调整", "优先调休 + 招聘", "P0"],
    ["第 3 周", "合规部", "未完成项目清理行动 (2/4)", "清理目标 17 个", "累计 34 个", "", "未开始", "部分项目存在纠纷", "法务介入评估", "P0"],
    ["第 3 周", "财务部", "应急收费政策发布", "正式文件", "发布", "", "未开始", "需全员宣贯", "组织政策解读会", "P0"],
    ["第 3 周", "HR", "核心人员访谈 (2/4)", "完成 10 人访谈", "10 人", "", "未开始", "部分人员可能有顾虑", "确保保密性", "P0"],
    ["第 3 周", "HR", "安服部简历筛选", "有效简历数", "≥20 份", "", "未开始", "市场人才竞争激烈", "扩大招聘渠道", "P0"],
    ["第 3 周", "研发部", "知识资产盘点启动", "知识地图框架", "完成框架", "", "未开始", "5780+ 文件分类困难", "优先核心文档", "P1"],
    ["第 3 周", "运营部", "第 1 月数据统计报告", "月度报告", "完成", "", "未开始", "数据收集可能延迟", "建立数据催报机制", "P1"],
    ["第 4 周", "安服部", "加班缓解措施评估", "人均工时下降", "15%", "", "未开始", "需持续监控", "调整措施力度", "P0"],
    ["第 4 周", "合规部", "未完成项目清理行动 (3/4)", "清理目标 18 个", "累计 52 个", "", "未开始", "剩余项目难度加大", "升级处理", "P0"],
    ["第 4 周", "HR", "核心人员访谈 (3/4)", "完成 15 人访谈", "15 人", "", "未开始", "整理共性问题", "形成保留建议", "P0"],
    ["第 4 周", "HR", "安服部面试 (1 批)", "面试人数", "≥10 人", "", "未开始", "协调面试官时间", "准备面试题库", "P0"],
    ["第 4 周", "质量部", "审核流程优化方案", "优化方案", "完成初稿", "", "未开始", "需平衡效率与质量", "试点验证", "P1"],
    ["第 4 周", "研发部", "知识资产盘点 (1/3)", "完成 30% 分类", "30%", "", "未开始", "工作量较大", "考虑外包辅助", "P1"],
    ["第 4 周", "运营部", "月度经营分析会准备", "会议材料", "完成", "", "未开始", "需各部门配合", "提前 3 天发材料", "P1"],
]

# 第 5-8 周计划数据
WEEK5_8_DATA = [
    ["第 5 周", "HR", "核心人员访谈完成", "完成 20 人访谈", "20 人", "", "未开始", "形成分析报告", "提出保留方案", "P0"],
    ["第 5 周", "HR", "安服部面试 (2 批)", "面试人数", "≥10 人", "", "未开始", "推进 offer 发放", "准备薪酬方案", "P0"],
    ["第 5 周", "合规部", "未完成项目清理 (4/4)", "清理目标 17 个", "累计 69 个", "", "未开始", "攻坚剩余难点", "升级管理层协调", "P0"],
    ["第 5 周", "运营部", "标准工时体系设计启动", "框架设计", "完成框架", "", "未开始", "需各部门配合提供数据", "优先核心业务", "P1"],
    ["第 5 周", "市场部", "NPS 调研方案设计", "调研方案", "完成设计", "", "未开始", "确定调研渠道", "准备调研工具", "P1"],
    ["第 5 周", "财务部", "应收账款账龄分析", "分析报告", "完成", "", "未开始", "需历史数据", "识别逾期风险", "P1"],
    ["第 6 周", "HR", "安服部 offer 发放", "发放 offer", "5 个", "", "未开始", "候选人可能犹豫", "加快流程", "P0"],
    ["第 6 周", "HR", "人员保留方案制定", "保留方案", "完成初稿", "", "未开始", "需预算支持", "测算成本", "P0"],
    ["第 6 周", "运营部", "标准工时体系设计 (1/3)", "覆盖 30% 业务", "30%", "", "未开始", "业务类型复杂", "分类处理", "P1"],
    ["第 6 周", "市场部", "NPS 调研启动", "样本量", "≥50 客户", "", "未开始", "客户配合度", "设计激励", "P1"],
    ["第 6 周", "财务部", "应收账款清理启动", "回款目标", "10%", "", "未开始", "客户付款周期长", "制定催收策略", "P1"],
    ["第 6 周", "研发部", "知识资产盘点 (2/3)", "完成 60% 分类", "60%", "", "未开始", "持续推进", "考虑工具辅助", "P1"],
    ["第 7 周", "HR", "安服部新人入职 (1 批)", "入职人数", "3 人", "", "未开始", "办理入职手续", "安排导师", "P0"],
    ["第 7 周", "HR", "人员保留方案评审", "方案通过", "管理层审批", "", "未开始", "可能需要调整", "准备多套方案", "P0"],
    ["第 7 周", "运营部", "标准工时体系设计 (2/3)", "覆盖 60% 业务", "60%", "", "未开始", "收集更多数据", "验证准确性", "P1"],
    ["第 7 周", "市场部", "NPS 调研持续", "样本量", "≥100 客户", "", "未开始", "提高响应率", "电话跟进", "P1"],
    ["第 7 周", "财务部", "应收账款清理持续", "回款目标", "累计 15%", "", "未开始", "重点攻坚大额", "法务支持", "P1"],
    ["第 7 周", "综合技术部", "非常规任务分析", "分析报告", "完成", "", "未开始", "识别可标准化任务", "制定产品化计划", "P1"],
    ["第 8 周", "HR", "安服部新人入职 (2 批)", "入职人数", "累计 5 人", "", "未开始", "完成入职培训", "安排上岗", "P0"],
    ["第 8 周", "HR", "人员保留方案实施", "方案落地", "开始执行", "", "未开始", "跟踪效果", "定期沟通", "P0"],
    ["第 8 周", "运营部", "标准工时体系设计 (3/3)", "覆盖 80% 业务", "80%", "", "未开始", "完成主体设计", "组织评审", "P1"],
    ["第 8 周", "市场部", "NPS 调研完成", "样本量", "≥150 客户", "", "未开始", "数据分析", "形成报告", "P1"],
    ["第 8 周", "财务部", "应收账款清理完成", "回款目标", "累计 20%", "", "未开始", "总结催收经验", "建立长效机制", "P1"],
    ["第 8 周", "研发部", "知识资产盘点完成", "知识地图", "完成", "", "未开始", "建立更新机制", "考虑系统化管理", "P1"],
]

# 第 9-12 周计划数据
WEEK9_12_DATA = [
    ["第 9 周", "IT+ 运营", "BI 系统需求调研", "需求文档", "完成调研", "", "未开始", "需各部门配合", "明确核心指标", "P1"],
    ["第 9 周", "综合技术部", "非常规任务产品化 (1/4)", "标准化 12%", "12%", "", "未开始", "识别共性需求", "优先高频任务", "P1"],
    ["第 9 周", "研发部", "软著申请材料准备", "申请材料", "5 项", "", "未开始", "技术交底书撰写", "外部代理协助", "P1"],
    ["第 9 周", "区域总监", "太原中心人力评估", "评估报告", "完成", "", "未开始", "分析业务需求", "增编 vs 外包", "P1"],
    ["第 9 周", "HR", "2027 年人力规划启动", "规划框架", "完成框架", "", "未开始", "收集业务预测", "对标行业", "P1"],
    ["第 10 周", "IT+ 运营", "BI 系统方案设计", "设计方案", "完成", "", "未开始", "技术选型", "考虑扩展性", "P1"],
    ["第 10 周", "综合技术部", "非常规任务产品化 (2/4)", "标准化 25%", "25%", "", "未开始", "编写标准文档", "培训推广", "P1"],
    ["第 10 周", "研发部", "软著申请提交", "提交数量", "5 项", "", "未开始", "跟进审批进度", "准备后续申请", "P1"],
    ["第 10 周", "区域总监", "太原中心人力优化方案", "优化方案", "完成", "", "未开始", "需预算支持", "多方案比较", "P1"],
    ["第 10 周", "HR", "2027 年人力规划 (1/3)", "完成 30%", "30%", "", "未开始", "部门访谈", "收集需求", "P1"],
    ["第 11 周", "IT+ 运营", "BI 系统开发启动", "开发计划", "启动", "", "未开始", "资源协调", "分阶段交付", "P1"],
    ["第 11 周", "综合技术部", "非常规任务产品化 (3/4)", "标准化 37%", "37%", "", "未开始", "持续优化", "收集反馈", "P1"],
    ["第 11 周", "研发部", "软著申请持续", "累计提交", "10 项", "", "未开始", "挖掘更多成果", "专利评估", "P1"],
    ["第 11 周", "区域总监", "太原中心人力优化实施", "方案落地", "开始执行", "", "未开始", "招聘或签约外包", "平稳过渡", "P1"],
    ["第 11 周", "HR", "2027 年人力规划 (2/3)", "完成 60%", "60%", "", "未开始", "预算测算", "多轮评审", "P1"],
    ["第 12 周", "IT+ 运营", "BI 系统一期交付", "核心模块", "交付", "", "未开始", "用户测试", "迭代优化", "P1"],
    ["第 12 周", "综合技术部", "非常规任务产品化 (4/4)", "标准化 50%", "50%", "", "未开始", "验收评估", "建立维护机制", "P1"],
    ["第 12 周", "研发部", "软著申请完成", "累计提交", "15 项", "", "未开始", "年度目标达成", "规划明年", "P1"],
    ["第 12 周", "区域总监", "太原中心人力优化完成", "增编/外包", "完成", "", "未开始", "效果评估", "持续监控", "P1"],
    ["第 12 周", "HR", "2027 年人力规划完成", "规划定稿", "提交审批", "", "未开始", "管理层评审", "预算批复", "P1"],
    ["第 12 周", "运营部", "12 周总结报告", "总结报告", "完成", "", "未开始", "汇总成果", "规划下阶段", "P0"],
]

# 风险清单数据
RISK_DATA = [
    ["R001", "人员风险", "安服部人均 957 小时/年，严重过劳", "高", "HR+ 安服部", "2026-03-02", "2026-04-30", "进行中", "招聘 5-8 人 + 调休制度", "P0"],
    ["R002", "人员风险", "太原中心 365 人天/人，无休息日", "高", "区域总监", "2026-03-02", "2026-05-31", "未开始", "增编 1-2 人或外包", "P0"],
    ["R003", "现金流风险", "合规部 69 个项目未完成，影响回款", "中", "合规部 + 财务", "2026-03-02", "2026-04-30", "进行中", "专项清理行动", "P0"],
    ["R004", "现金流风险", "客户应急任务可能未收费", "中", "财务部", "2026-03-02", "2026-03-31", "进行中", "制定收费政策", "P0"],
    ["R005", "数据风险", "质量部 2026 预估数据矛盾", "中", "质量部", "2026-03-02", "2026-03-15", "进行中", "数据核实", "P0"],
    ["R006", "质量风险", "高负荷可能导致交付质量下降", "中", "质量部", "2026-03-02", "2026-05-31", "未开始", "质量抽检机制", "P1"],
    ["R007", "知识风险", "研发部软著仅 6 项，转化率低", "中", "研发部", "2026-03-02", "2026-05-31", "未开始", "激励政策 + 目标 15 项", "P1"],
    ["R008", "组织风险", "核心人员流失风险", "高", "HR", "2026-03-02", "2026-04-30", "进行中", "Top20 访谈 + 保留方案", "P0"],
    ["R009", "效率风险", "综合技术部非常规任务 141 项，碎片化", "中", "综合技术部", "2026-03-02", "2026-05-31", "未开始", "任务产品化 50%", "P1"],
    ["R010", "管理风险", "各部门统计口径不一致", "低", "运营部", "2026-03-02", "2026-04-30", "进行中", "统一数据规范", "P1"],
]

# ============================================================
# 生成 XML
# ============================================================

def generate_excel_xml():
    """生成完整的 Excel XML 文档"""
    
    worksheets = []
    
    # 工作表 1: 封面
    cover_data = [
        ["编制日期:", datetime.now().strftime("%Y年%m月%d日")],
        ["报告周期:", "2026 年 3 月第 1 周 - 2026 年 5 月第 4 周（12 周）"],
        ["编制部门:", "战略运营部"],
        ["审批状态:", "待审批"],
        ["版本号:", "V1.0"],
        ["", ""],
        ["核心目标", ""],
        ["📊", "建立周度工作量统计与监控体系"],
        ["⚠️", "识别并缓解安服部过劳风险（人均 957 小时/年）"],
        ["💰", "清理 69 个未完成项目，提升回款率"],
        ["📈", "启动人员增编计划（12-19 人）"],
        ["🔧", "建立标准工时体系框架"],
    ]
    
    cover_xml = '''<ss:Worksheet ss:Name="封面">
    <ss:Table>
        <ss:Column ss:Index="1" ss:Width="30"/>
        <ss:Column ss:Index="2" ss:Width="60"/>
        <ss:Row ss:Height="60">
            <ss:Cell ss:MergeAcross="1" ss:StyleID="sTitle"><ss:Data ss:Type="String">网络安全公司周计划报表</ss:Data></ss:Cell>
        </ss:Row>
        <ss:Row ss:Height="30">
            <ss:Cell ss:MergeAcross="1" ss:StyleID="sNormal"><ss:Data ss:Type="String">基于 2025-2026 年工作量分析与战略规划报告</ss:Data></ss:Cell>
        </ss:Row>
'''
    for row_data in cover_data:
        if row_data[0] == "核心目标":
            cover_xml += f'''        <ss:Row ss:Height="30">
            <ss:Cell ss:MergeAcross="1" ss:StyleID="sBold"><ss:Data ss:Type="String">{row_data[0]}</ss:Data></ss:Cell>
        </ss:Row>\n'''
        else:
            style = "sNormal"
            if row_data[0] in ["📊", "⚠️", "💰", "📈", "🔧"]:
                style = "sInfo"
            cover_xml += f'''        <ss:Row>
            <ss:Cell ss:StyleID="{style}"><ss:Data ss:Type="String">{row_data[0]}</ss:Data></ss:Cell>
            <ss:Cell ss:StyleID="{style}"><ss:Data ss:Type="String">{row_data[1]}</ss:Data></ss:Cell>
        </ss:Row>\n'''
    
    cover_xml += '''    </ss:Table>
</ss:Worksheet>'''
    worksheets.append(cover_xml)
    
    # 工作表 2: 核心指标看板
    worksheets.append(create_worksheet(
        "核心指标看板",
        ["指标类别", "指标名称", "2025 基准值", "2026 目标值", "本周实际值", "完成率", "状态"],
        KPI_DATA,
        [12, 25, 15, 15, 15, 12, 8]
    ))
    
    # 工作表 3: 第 1-4 周计划
    worksheets.append(create_worksheet(
        "第 1-4 周计划",
        ["周次", "责任部门", "行动项", "关键指标", "目标值", "实际值", "完成状态", "问题分析", "下一步建议", "优先级"],
        WEEK1_4_DATA,
        [8, 12, 25, 18, 12, 12, 10, 25, 25, 8]
    ))
    
    # 工作表 4: 第 5-8 周计划
    worksheets.append(create_worksheet(
        "第 5-8 周计划",
        ["周次", "责任部门", "行动项", "关键指标", "目标值", "实际值", "完成状态", "问题分析", "下一步建议", "优先级"],
        WEEK5_8_DATA,
        [8, 12, 25, 18, 12, 12, 10, 25, 25, 8]
    ))
    
    # 工作表 5: 第 9-12 周计划
    worksheets.append(create_worksheet(
        "第 9-12 周计划",
        ["周次", "责任部门", "行动项", "关键指标", "目标值", "实际值", "完成状态", "问题分析", "下一步建议", "优先级"],
        WEEK9_12_DATA,
        [8, 12, 25, 18, 12, 12, 10, 25, 25, 8]
    ))
    
    # 工作表 6: 问题与风险
    worksheets.append(create_worksheet(
        "问题与风险",
        ["编号", "类别", "问题/风险描述", "严重程度", "责任部门", "发现日期", "计划解决日期", "当前状态", "解决措施", "备注"],
        RISK_DATA,
        [8, 12, 35, 10, 15, 12, 15, 12, 30, 20]
    ))
    
    # 工作表 7: 周度总结模板
    summary_template = [
        ["周次", "第 X 周（YYYY-MM-DD 至 YYYY-MM-DD）"],
        ["编制人", ""],
        ["编制日期", ""],
        ["", ""],
        ["一、本周核心指标完成情况", ""],
        ["安服部人均工时", "目标：15.0 小时/周 | 实际：___ | 完成率：___%"],
        ["合规部报告产出", "目标：31.5 份/周 | 实际：___ | 完成率：___%"],
        ["质量部审核文档", "目标：100 份/周 | 实际：___ | 完成率：___%"],
        ["未完成项目清理", "目标：___个 | 实际：___ | 累计：___/69"],
        ["人员增编进度", "目标：___人入职 | 实际：___ | 累计：___/5"],
        ["", ""],
        ["二、本周重点工作完成情况", ""],
        ["重点工作 1", "状态：□完成 □进行中 □未开始 | 说明："],
        ["重点工作 2", "状态：□完成 □进行中 □未开始 | 说明："],
        ["重点工作 3", "状态：□完成 □进行中 □未开始 | 说明："],
        ["", ""],
        ["三、问题分析", ""],
        ["问题 1", "描述：\\n影响：\\n原因："],
        ["问题 2", "描述：\\n影响：\\n原因："],
        ["", ""],
        ["四、风险预警", ""],
        ["风险 1", "描述：\\n严重程度：□高 □中 □低\\n建议措施："],
        ["风险 2", "描述：\\n严重程度：□高 □中 □低\\n建议措施："],
        ["", ""],
        ["五、下周工作计划", ""],
        ["计划 1", "责任人：___ | 完成标准：___"],
        ["计划 2", "责任人：___ | 完成标准：___"],
        ["计划 3", "责任人：___ | 完成标准：___"],
        ["", ""],
        ["六、需要协调支持事项", ""],
        ["事项 1", "需要___部门支持，具体需求："],
        ["事项 2", "需要___部门支持，具体需求："],
    ]
    
    summary_rows = []
    for row_data in summary_template:
        if "一、" in row_data[0] or "二、" in row_data[0] or "三、" in row_data[0] or "四、" in row_data[0] or "五、" in row_data[0] or "六、" in row_data[0]:
            summary_rows.append(f'<ss:Row><ss:Cell ss:MergeAcross="1" ss:StyleID="sInfo"><ss:Data ss:Type="String">{row_data[0]}</ss:Data></ss:Cell></ss:Row>')
        else:
            style = "sLeft" if len(row_data[1]) > 30 else "sNormal"
            summary_rows.append(f'<ss:Row><ss:Cell ss:StyleID="{style}"><ss:Data ss:Type="String">{row_data[0]}</ss:Data></ss:Cell><ss:Cell ss:StyleID="{style}"><ss:Data ss:Type="String">{row_data[1]}</ss:Data></ss:Cell></ss:Row>')
    
    worksheets.append(f'''<ss:Worksheet ss:Name="周度总结模板">
    <ss:Table>
        <ss:Column ss:Index="1" ss:Width="25"/>
        <ss:Column ss:Index="2" ss:Width="60"/>
        {"".join(summary_rows)}
    </ss:Table>
</ss:Worksheet>''')
    
    # 组装完整 XML
    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<?mso-application progid="Excel.Sheet"?>
<ss:Workbook xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"
    xmlns:o="urn:schemas-microsoft-com:office:office"
    xmlns:x="urn:schemas-microsoft-com:office:excel"
    xmlns:html="http://www.w3.org/TR/REC-html40">
    <ss:DocumentProperties xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">
        <ss:Title>网络安全公司周计划报表</ss:Title>
        <ss:Author>战略运营部</ss:Author>
        <ss:Created>{datetime.now().isoformat()}</ss:Created>
    </ss:DocumentProperties>
    {STYLES}
    {"".join(worksheets)}
</ss:Workbook>'''
    
    return xml_content

# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    print("🚀 开始生成周计划报表...")
    
    xml_content = generate_excel_xml()
    
    output_path = "/home/ghost/.openclaw/workspace/网络安全公司周计划报表_20260302.xml"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
    
    print(f"✅ 周计划报表已生成：{output_path}")
    print(f"📊 包含工作表：封面、核心指标看板、第 1-4 周计划、第 5-8 周计划、第 9-12 周计划、问题与风险、周度总结模板")
    print(f"📈 总计行动项：{len(WEEK1_4_DATA) + len(WEEK5_8_DATA) + len(WEEK9_12_DATA)} 项")
    print(f"⚠️ 风险清单：{len(RISK_DATA)} 项")
    print(f"📁 文件格式：Excel 兼容 XML（可直接用 Excel 打开）")
