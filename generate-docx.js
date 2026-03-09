const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, WidthType, HeadingLevel, BorderStyle } = require("docx");
const fs = require("fs");

// 读取 markdown 内容
const mdContent = fs.readFileSync('/home/ghost/.openclaw/workspace/专家委员会工作量分解和计划报告_V2.0.docx.md', 'utf8');

// 简单的 markdown 解析函数
function parseMarkdown(md) {
    const sections = [];
    const lines = md.split('\n');
    let currentSection = [];
    
    for (let line of lines) {
        if (line.startsWith('# ')) {
            if (currentSection.length > 0) {
                sections.push({ type: 'heading1', text: line.replace('# ', '').trim() });
            } else {
                sections.push({ type: 'heading1', text: line.replace('# ', '').trim() });
            }
        } else if (line.startsWith('## ')) {
            sections.push({ type: 'heading2', text: line.replace('## ', '').trim() });
        } else if (line.startsWith('### ')) {
            sections.push({ type: 'heading3', text: line.replace('### ', '').trim() });
        } else if (line.startsWith('|')) {
            // 表格行，跳过简化处理
            continue;
        } else if (line.trim() === '') {
            continue;
        } else if (line.startsWith('**') && line.endsWith('**')) {
            sections.push({ type: 'bold', text: line.replace(/\*\*/g, '').trim() });
        } else if (line.startsWith('*') && line.endsWith('*')) {
            sections.push({ type: 'italic', text: line.replace(/\*/g, '').trim() });
        } else {
            sections.push({ type: 'text', text: line.trim() });
        }
    }
    
    return sections;
}

// 创建文档
const doc = new Document({
    sections: [{
        properties: {},
        children: [
            new Paragraph({
                text: "专家委员会工作量分解和计划报告（完善版 V2.0）",
                heading: HeadingLevel.TITLE,
                spacing: { after: 400 }
            }),
            new Paragraph({
                children: [
                    new TextRun({ text: "版本号：V2.0", bold: true }),
                    new TextRun({ text: "\t" }),
                    new TextRun({ text: "编制日期：2026 年 3 月 4 日" }),
                ],
                spacing: { after: 200 }
            }),
            new Paragraph({
                children: [
                    new TextRun({ text: "评审状态：待专家评审", bold: true }),
                    new TextRun({ text: "\t" }),
                    new TextRun({ text: "评审截止日期：2026 年 3 月 11 日" }),
                ],
                spacing: { after: 200 }
            }),
            new Paragraph({
                text: "编制部门：专家委员会",
                spacing: { after: 400 }
            }),
            
            // 第一章
            new Paragraph({
                text: "一、部门职责与任务分解",
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            }),
            new Paragraph({
                text: "（一）岗位职责",
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 200, after: 200 }
            }),
            new Paragraph({
                text: "根据文档内容，专家委员会的核心岗位职责聚焦于技术标准化、质量管控、团队赋能、重难点项目攻坚及合规支撑。具体明确的岗位职责如下：",
                spacing: { after: 200 }
            }),
            
            // 岗位职责列表
            new Paragraph({
                children: [
                    new TextRun({ text: "1. 体系构建与标准审定", bold: true }),
                ],
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "建立健全技术实施风险控制规范流程体系，负责公司内部技术工作标准的审定、发布及定期更新。",
                spacing: { after: 200 }
            }),
            
            new Paragraph({
                children: [
                    new TextRun({ text: "2. 质量管理与运营", bold: true }),
                ],
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "负责业务实施过程中的技术质量管理，包括报告签批前的审核、等级保护测评报告的月度抽查及非常规项目的综合质量管控。",
                spacing: { after: 200 }
            }),
            
            new Paragraph({
                children: [
                    new TextRun({ text: "3. 团队赋能与能力建设", bold: true }),
                ],
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "牵头技术团队能力提升与评价，组织研讨会与培训，传达行管单位动态，解答技术疑难点，推动新技术与新业务模式的探索。",
                spacing: { after: 200 }
            }),
            
            new Paragraph({
                children: [
                    new TextRun({ text: "4. 项目攻坚与研发", bold: true }),
                ],
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "组织实施公司重难点项目及非常规网络安全服务项目，负责重要业务的标准化研发及现有服务的优化迭代。",
                spacing: { after: 200 }
            }),
            
            new Paragraph({
                children: [
                    new TextRun({ text: "5. 外部支撑与应急响应", bold: true }),
                ],
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "支撑公安、网信等行管单位的项目报备与技术需求，组织并实施客户及行管单位的网络安全应急响应与检查任务。",
                spacing: { after: 400 }
            }),
            
            // 职责分解任务表
            new Paragraph({
                text: "（二）职责分解任务",
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 200, after: 200 }
            }),
            
            // 简化表格 - 使用段落代替
            new Paragraph({
                text: "【表格 1】职责分解任务表",
                heading: HeadingLevel.HEADING_3,
                spacing: { after: 200 }
            }),
            new Paragraph({
                text: "1. 制度与标准建设：制定/修订技术实施风险控制规范流程；审定并发布年度技术标准（每季度更新）；建立质量管理体系文件。完成时限：Q1。责任人：部门负责人。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "2. 质量管控执行：执行所有报告签批前质量审核；每月开展等级保护测评报告抽查；针对非常规项目建立专项质量管控档案。完成时限：持续执行。责任人：技术专家。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "3. 团队培训与赋能：每月组织一次技术研讨会或培训课程；定期发布行管单位动态简报；建立内部技术问答机制。完成时限：持续执行。责任人：技术专家。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "4. 创新与研究：组织新业务体系突破研讨；实施标准化网络安全服务业务的研发与迭代。完成时限：Q2-Q3。责任人：项目组。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "5. 项目实施与支撑：带队实施重难点及非常规项目；协助完成公安、网信等项目报备；组建应急响应小组。完成时限：持续执行。责任人：全体。",
                spacing: { after: 400 }
            }),
            
            // 第二章
            new Paragraph({
                text: "二、工作目标",
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            }),
            new Paragraph({
                text: "【表格 2】工作目标量化表",
                heading: HeadingLevel.HEADING_3,
                spacing: { after: 200 }
            }),
            new Paragraph({
                text: "1. 合规化目标：技术流程与标准更新及时率 100%，全年考核，OA 系统记录。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "2. 质量提升目标：报告一次性通过率≥95%，质量整改率降低 50%，Q2 达成，审核统计表。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "3. 能力成长目标：培训覆盖率 100%，技术难点响应≤24 小时，形成≥5 项新技术研究报告，全年考核。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "4. 交付保障目标：行管单位支撑满意度 100%，应急响应成功率 100%，全年考核。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "5. 标准化研发目标：完成 3-5 个核心服务产品标准化，Q3 完成。",
                spacing: { after: 400 }
            }),
            
            // 第三章
            new Paragraph({
                text: "三、任务交付成果",
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            }),
            new Paragraph({
                text: "（一）交付方式",
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 200, after: 200 }
            }),
            new Paragraph({
                text: "1. 文档交付：制度、标准、报告通过 OA 系统或知识库提交，责任方：执行专员。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "2. 会议交付：汇报、共享、培训通过技术研讨会、项目复盘会、培训会形式，责任方：技术专家。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "3. 系统/工具交付：执行表单、审核流程配置、操作手册，责任方：部门负责人。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "4. 现场交付：现场实施记录、总结报告、客户反馈单，责任方：项目组。",
                spacing: { after: 400 }
            }),
            
            new Paragraph({
                text: "（二）交付成果清单（共 17 项）",
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 200, after: 200 }
            }),
            new Paragraph({
                text: "制度规范类（4 项）：《技术实施风险控制规范流程体系》、《公司技术工作标准汇编》、《质量审核管理制度》、《业务交付过程执行表单集》（15+ 表单）",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "质量记录类（3 项）：《月度等级保护测评报告抽查分析报告》（12 份/年）、《项目报告质量审核记录表》、《非常规项目质量管控台账》",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "赋能培训类（4 项）：《技术研讨会会议纪要》（12 份/年）、《技术培训课件库》、《行管单位动态传达简报》（12 份/年）、《技术难点解答知识库》",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "项目研发类（3 项）：《重难点项目实施总结报告》、《新业务体系探索研究报告》（≥5 份）、《标准化网络安全服务业务迭代版本说明》（3-5 份）",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "支撑应急类（3 项）：《项目报备支撑记录》、《网络安全应急响应处置报告》、《网络安全检查工作总结》",
                spacing: { after: 400 }
            }),
            
            // 第四章
            new Paragraph({
                text: "四、质量与效率",
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            }),
            new Paragraph({
                text: "（一）质量管控措施",
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 200, after: 200 }
            }),
            new Paragraph({
                text: "1. 多级审核机制：项目组自检→专家委员会专审→签批前终审三级流程，每项目执行。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "2. 常态化抽查：每月对等级保护测评报告进行随机抽查。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "3. 标准化作业：强制执行统一的审核标准和执行表单。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "4. 交叉审核：不同专家间交叉复核，每季度执行。",
                spacing: { after: 400 }
            }),
            
            new Paragraph({
                text: "（二）效率提升措施",
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 200, after: 200 }
            }),
            new Paragraph({
                text: "1. 知识复用：建立技术难点解答库和标准化服务模板，预期效果：常规项目处理速度提升 30%。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "2. 集中攻关：专家委员会带领团队集中资源攻坚重难点项目，避免单兵作战导致的延期。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "3. 动态同步：定期传达行管要求，减少政策理解偏差，减少返工率 50%。",
                spacing: { after: 400 }
            }),
            
            // 第五章
            new Paragraph({
                text: "五、考核",
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            }),
            new Paragraph({
                text: "（一）考核指标表（9 项核心指标）",
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 200, after: 200 }
            }),
            new Paragraph({
                text: "1. 制度建设完成率：100%，季度考核，权重 20%",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "2. 报告审核覆盖率：100%，月度考核，权重 25%",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "3. 抽查报告合格率：≥95%，月度考核，权重 25%",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "4. 技术研讨会/培训课程举办次数：≥12 次/年，季度考核，权重 10%",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "5. 培训参与覆盖率：100%，季度考核，权重 10%",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "6. 重难点项目验收通过率：100%，季度考核，权重 15%",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "7. 客户/行管单位满意度：≥95%，半年考核，权重 15%",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "8. 技术难点解答及时率：≥95%（≤24 小时），月度考核，权重 10%",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "9. 应急响应到位时间：≤2 小时，每事件考核，权重 10%",
                spacing: { after: 400 }
            }),
            
            new Paragraph({
                text: "（二）考核分解",
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 200, after: 200 }
            }),
            new Paragraph({
                text: "1. 部门负责人（40%）：整体体系建设、重大质量事故、行管支撑满意度",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "2. 技术专家/骨干（40%）：具体标准审定、报告审核质量、培训授课质量、重难点项目实施",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "3. 执行专员（20%）：文档整理、抽查执行、会议组织、日常答疑响应",
                spacing: { after: 400 }
            }),
            
            new Paragraph({
                text: "（三）考核结果应用",
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 200, after: 200 }
            }),
            new Paragraph({
                text: "1. 绩效挂钩：考核结果直接与季度/年度绩效奖金挂钩",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "2. 评优依据：作为年度优秀员工、技术标兵评选的核心依据",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "3. 改进计划：考核未达标者制定限期改进计划（PIP），专家委员会跟踪辅导",
                spacing: { after: 400 }
            }),
            
            // 第六章
            new Paragraph({
                text: "六、时间计划表",
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            }),
            new Paragraph({
                text: "1. Q1 启动期（1 月 -3 月）：制度体系搭建、标准初稿编制、质量管理体系建立。交付物：流程体系 V1.0、标准汇编、审核制度。里程碑：体系搭建完成。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "2. Q2 执行期（4 月 -6 月）：质量审核全覆盖、首期培训完成、月度抽查启动。交付物：审核记录表、培训课件、抽查报告。里程碑：审核机制运行。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "3. Q3 深化期（7 月 -9 月）：重难点项目攻坚、标准化研发、新业务探索。交付物：项目总结报告、标准化服务 V1.0。里程碑：研发成果落地。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "4. Q4 收官期（10 月 -12 月）：年度复盘、标准迭代、考核评估。交付物：年度白皮书、标准 V2.0、考核报告。里程碑：年度目标达成。",
                spacing: { after: 400 }
            }),
            
            // 第七章
            new Paragraph({
                text: "七、人员配置与分工",
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            }),
            new Paragraph({
                text: "1. 部门负责人（1 人）：体系建设、重大决策、行管对接、最终签批。能力要求：8 年以上经验，熟悉行业标准。考核权重：40%。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "2. 技术专家（3-5 人）：标准审定、报告审核、培训授课、技术攻关。能力要求：5 年以上经验，专业技术过硬。考核权重：40%。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "3. 执行专员（2-3 人）：文档管理、抽查执行、会议组织、日常答疑。能力要求：2 年以上经验，细致认真。考核权重：20%。",
                spacing: { after: 200 }
            }),
            new Paragraph({
                text: "AB 角机制：每个关键岗位设置 AB 角，确保人员流动时工作连续性。",
                spacing: { after: 400 }
            }),
            
            // 第八章
            new Paragraph({
                text: "八、资源需求",
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            }),
            new Paragraph({
                text: "1. 系统工具：质量审核管理系统 1 套，预算待评估，用途：审核流程数字化，优先级：高",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "2. 会议资源：技术研讨会场地每月 1 次，内部会议室，用途：团队赋能，优先级：中",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "3. 文档模板：标准化执行表单 15+，内部制作，用途：统一作业标准，优先级：高",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "4. 培训预算：外部专家邀请费 4 次/年，预算待评估，用途：能力提升，优先级：中",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "5. 培训预算：内部培训材料制作持续，预算待评估，用途：知识库建设，优先级：中",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "6. 应急资源：应急响应专项预算待评估，用途：应急事件处理，优先级：高",
                spacing: { after: 400 }
            }),
            
            // 第九章
            new Paragraph({
                text: "九、风险评估与应对",
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            }),
            new Paragraph({
                text: "1. 人员风险（中概率/高影响）：核心专家离职。应对措施：建立 AB 角机制、知识文档化、关键知识双人掌握。责任人：部门负责人。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "2. 政策风险（高概率/中影响）：行管标准变更。应对措施：建立政策监测机制、月度更新、订阅官方通知。责任人：执行专员。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "3. 项目风险（中概率/高影响）：重难点项目延期。应对措施：提前识别、资源预留 20% 缓冲、周进度跟踪。责任人：项目负责人。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "4. 质量风险（低概率/高影响）：审核流于形式。应对措施：交叉审核、抽查复核、审核质量纳入考核。责任人：技术专家。",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "5. 资源风险（中概率/中影响）：预算不足影响工作。应对措施：提前申报、优先级排序、分阶段投入。责任人：部门负责人。",
                spacing: { after: 400 }
            }),
            
            // 第十章
            new Paragraph({
                text: "十、专家评审安排",
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            }),
            new Paragraph({
                text: "（一）评审专家名单（待邀请）",
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 200, after: 200 }
            }),
            new Paragraph({
                text: "1. 技术标准化专家：待邀请，评审重点：制度与标准建设部分",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "2. 质量管理专家：待邀请，评审重点：质量管控与考核部分",
                spacing: { after: 100 }
            }),
            new Paragraph({
                text: "3. 项目管理专家：待邀请，评审重点：时间计划与资源配置部分",
                spacing: { after: 400 }
            }),
            
            new Paragraph({
                text: "（二）评审流程",
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 200, after: 200 }
            }),
            new Paragraph({
                text: "1. 3 月 4 日：发送评审邀请及文档",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "2. 3 月 4 日 -3 月 9 日：专家独立评审",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "3. 3 月 10 日：意见汇总整理",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "4. 3 月 11 日：评审会议（线上/线下）",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "5. 3 月 12 日 -3 月 15 日：报告修订完善",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "6. 3 月 16 日：正式发布",
                spacing: { after: 400 }
            }),
            
            // 附录
            new Paragraph({
                text: "附录：执行表单模板清单",
                heading: HeadingLevel.HEADING_1,
                spacing: { before: 400, after: 200 }
            }),
            new Paragraph({
                text: "1. 《项目报告质量审核记录表》",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "2. 《月度等级保护测评报告抽查表》",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "3. 《非常规项目质量管控台账》",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "4. 《技术研讨会会议纪要模板》",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "5. 《技术培训课件模板》",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "6. 《行管单位动态简报模板》",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "7. 《技术难点解答记录表》",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "8. 《重难点项目实施计划表》",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "9. 《应急响应处置记录表》",
                spacing: { after: 50 }
            }),
            new Paragraph({
                text: "10. 《项目报备支撑记录表》",
                spacing: { after: 400 }
            }),
            
            // 签署信息
            new Paragraph({
                children: [
                    new TextRun({ text: "编制人：", bold: true }),
                    new TextRun({ text: "专家委员会" }),
                ],
                spacing: { after: 100 }
            }),
            new Paragraph({
                children: [
                    new TextRun({ text: "审核人：", bold: true }),
                    new TextRun({ text: "待评审" }),
                ],
                spacing: { after: 100 }
            }),
            new Paragraph({
                children: [
                    new TextRun({ text: "批准人：", bold: true }),
                    new TextRun({ text: "待评审" }),
                ],
                spacing: { after: 100 }
            }),
            new Paragraph({
                children: [
                    new TextRun({ text: "发布日期：", bold: true }),
                    new TextRun({ text: "待定" }),
                ],
                spacing: { after: 400 }
            }),
            
            new Paragraph({
                text: "*本报告版本 V2.0，编制于 2026 年 3 月 4 日*",
                italics: true,
                spacing: { before: 200 }
            }),
        ],
    }],
});

// 生成并保存文档
Packer.toBuffer(doc).then((buffer) => {
    fs.writeFileSync("/home/ghost/.openclaw/workspace/专家委员会工作量分解和计划报告_V2.0.docx", buffer);
    console.log("Document created successfully: 专家委员会工作量分解和计划报告_V2.0.docx");
}).catch((error) => {
    console.error("Error creating document:", error);
    process.exit(1);
});
