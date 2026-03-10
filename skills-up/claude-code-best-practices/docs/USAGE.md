# 使用示例

> 💡 Claude Code 最佳实践技能包使用示例

---

## 📚 Skills 使用示例

### 1. project-status

**查看项目状态**

```bash
/skill project-status
```

**输出示例:**
```
=== Git 状态 ===
 M src/main.js
 M package.json
?? new-feature.js

=== 最近提交 ===
a1b2c3d 添加用户认证功能
e4f5g6h 修复登录页面 bug
h7i8j9k 优化数据库查询

=== 工作区文件 ===
./README.md
./src/main.js
./src/utils.js
./package.json
./tests/auth.test.js
```

**使用场景:**
- 开始新任务前了解项目状态
- 提交代码前检查变更
- 长时间工作后回顾进度

---

### 2. code-review

**审查单个文件**

```bash
/skill code-review src/auth.js
```

**审查多个文件**

```bash
/skill code-review src/auth.js src/utils.js
```

**输出示例:**
```markdown
## 审查结果：src/auth.js

### ✅ 优点
- 函数职责清晰
- 错误处理完整
- 注释充分

### ⚠️ 需要注意
- 密码验证逻辑可以优化
- 缺少输入长度限制

### ❌ 问题
- [严重] 第 45 行：硬编码的密钥
  ```javascript
  const SECRET = "my-secret-key";  // ❌
  ```
  建议：使用环境变量
  ```javascript
  const SECRET = process.env.AUTH_SECRET;  // ✅
  ```

- [一般] 第 78 行：未处理空值
  ```javascript
  function getUser(id) {
    return users.find(u => u.id === id);  // 可能返回 undefined
  }
  ```
  建议：添加空值检查
  ```javascript
  function getUser(id) {
    const user = users.find(u => u.id === id);
    if (!user) throw new Error('User not found');
    return user;
  }
  ```

### 建议修改
1. 将密钥移至环境变量
2. 添加输入验证
3. 增加单元测试覆盖
```

**使用场景:**
- 提交代码前自查
- 学习代码审查最佳实践
- 发现潜在 bug 和安全问题

---

### 3. test-gen

**为函数生成测试**

```bash
/skill test-gen src/utils.js
```

**为模块生成测试**

```bash
/skill test-gen src/auth.js
```

**输出示例:**
```javascript
// 测试文件：src/utils.test.js

const { formatDate, validateEmail, calculateTotal } = require('./utils');

describe('formatDate', () => {
  it('应该正确格式化日期', () => {
    const date = new Date('2026-03-10');
    expect(formatDate(date)).toBe('2026-03-10');
  });

  it('应该处理无效日期', () => {
    expect(() => formatDate(null)).toThrow('Invalid date');
  });

  it('应该处理边界情况（闰年）', () => {
    const date = new Date('2024-02-29');
    expect(formatDate(date)).toBe('2024-02-29');
  });
});

describe('validateEmail', () => {
  it('应该接受有效邮箱', () => {
    expect(validateEmail('test@example.com')).toBe(true);
  });

  it('应该拒绝无效邮箱', () => {
    expect(validateEmail('invalid')).toBe(false);
    expect(validateEmail('test@')).toBe(false);
  });

  it('应该处理空值', () => {
    expect(validateEmail('')).toBe(false);
    expect(validateEmail(null)).toBe(false);
  });
});

describe('calculateTotal', () => {
  it('应该计算正确总额', () => {
    const items = [
      { price: 10, quantity: 2 },
      { price: 5, quantity: 3 }
    ];
    expect(calculateTotal(items)).toBe(35);
  });

  it('应该处理空数组', () => {
    expect(calculateTotal([])).toBe(0);
  });

  it('应该处理负数（退货情况）', () => {
    const items = [
      { price: -10, quantity: 1 },
      { price: 50, quantity: 1 }
    ];
    expect(calculateTotal(items)).toBe(40);
  });
});
```

**使用场景:**
- 新功能开发时快速生成测试
- 为遗留代码补充测试
- 学习测试用例设计

---

## 🔧 Hooks 使用示例

### on-file-edit.sh

**自动触发场景:**

当你编辑文件后，Hook 会自动运行：

```bash
# 编辑 JavaScript 文件
# 输出:
📝 文件已修改：src/main.js
🔍 检查语法...
✅ 语法检查通过
---

# 编辑 Python 文件
# 输出:
📝 文件已修改：script.py
🔍 检查 Python 语法...
✅ 语法检查通过
---

# 编辑 Markdown 文件
# 输出:
📝 文件已修改：README.md
✅ Markdown 文件已更新
---
```

**手动测试:**

```bash
# 测试 Hook
./.claude/hooks/on-file-edit.sh src/test.js
```

---

### on-task-complete.sh

**自动触发场景:**

完成任务后，Hook 会自动显示变更摘要：

```bash
# 输出:
✅ 任务完成
📅 完成时间：2026-03-10 12:45:30

📊 Git 变更摘要:
 M src/main.js
 M src/utils.js
?? src/test.js

📝 未暂存的变更:
 src/main.js  | 15 +++++++++++----
 src/utils.js |  8 ++++++++
 2 files changed, 19 insertions(+), 4 deletions(-)

---
```

**手动测试:**

```bash
# 测试 Hook
./.claude/hooks/on-task-complete.sh
```

---

## 🎯 完整工作流示例

### 场景 1: 开发新功能

```bash
# 1. 查看当前状态
/skill project-status

# 2. 开始开发...
# (编写代码)

# 3. 文件编辑后自动语法检查
# (Hook 自动触发)

# 4. 生成测试
/skill test-gen src/new-feature.js

# 5. 代码审查
/skill code-review src/new-feature.js

# 6. 根据审查建议修改

# 7. 完成任务
# (Hook 自动显示变更摘要)

# 8. 提交代码
git add .
git commit -m "添加新功能"
```

---

### 场景 2: 修复 Bug

```bash
# 1. 查看项目状态
/skill project-status

# 2. 审查相关代码
/skill code-review src/buggy-code.js

# 3. 修复 Bug
# (编写修复代码)

# 4. 自动生成测试
/skill test-gen src/buggy-code.js

# 5. 运行测试
npm test

# 6. 再次审查
/skill code-review src/buggy-code.js

# 7. 提交修复
git add .
git commit -m "修复 XXX bug"
```

---

### 场景 3: 代码重构

```bash
# 1. 审查要重构的代码
/skill code-review src/old-code.js

# 2. 开始重构
# (编写新代码)

# 3. 为新代码生成测试
/skill test-gen src/refactored-code.js

# 4. 对比测试覆盖
# (确保测试通过)

# 5. 审查新代码
/skill code-review src/refactored-code.js

# 6. 提交重构
git add .
git commit -m "重构 XXX 模块"
```

---

## 📊 实战案例

### 坦克大战游戏开发

**项目:** 创建经典坦克大战 HTML5 游戏

**使用的技能:**

1. **项目初始化**
   ```bash
   /skill project-status
   # 确认工作区状态
   ```

2. **代码审查**
   ```bash
   /skill code-review src/game.js
   # 检查游戏逻辑
   ```

3. **测试生成**
   ```bash
   /skill test-gen src/game.js
   # 生成 22 个单元测试
   ```

4. **测试结果**
   ```
   📊 测试结果：22 通过，0 失败
   🎉 所有测试通过！
   ```

**最终成果:**
- 1242 行游戏代码
- 362 行测试代码
- 完整文档

---

## 💡 最佳实践提示

1. **开始工作前:** 先用 `/skill project-status` 了解状态
2. **提交代码前:** 先用 `/skill code-review` 自查
3. **新功能开发:** 先用 `/skill test-gen` 生成测试框架
4. **遇到问题:** 检查 Hooks 输出，可能有线索
5. **定期回顾:** 使用 Hooks 的输出了解工作进度

---

**更多示例:** 查看 [examples/](../examples/) 目录

**最后更新:** 2026-03-10
