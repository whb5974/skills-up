# Skill: test-gen

## 描述
为指定函数或模块生成测试用例。

## 测试生成规则
1. **覆盖场景**:
   - 正常输入
   - 边界条件
   - 错误输入
   - 空值/null 处理

2. **测试框架**:
   - JavaScript/TypeScript: Jest 或 Vitest
   - Python: pytest 或 unittest
   - 优先使用项目现有测试框架

3. **测试命名**: 清晰描述测试场景

## 输出格式
```javascript
// 测试文件：xxx.test.js
describe('函数名', () => {
  it('应该处理正常情况', () => {
    // ...
  });
  
  it('应该处理边界条件', () => {
    // ...
  });
  
  it('应该处理错误输入', () => {
    // ...
  });
});
```

## 使用方式
在 Claude Code 中输入：`/skill test-gen <文件路径或函数名>`
