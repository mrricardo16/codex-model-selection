# Codex 模型选择与子代理路由

[English README](README.md) · [MIT License](LICENSE)

这是一个面向 Codex 的模型/子代理路由 Skill。核心原则是：**选择能够可靠完成并验证任务的最低成本路线**，而不是把所有复杂任务默认交给最强模型。

## 路由层级

| 路由 | 适用场景 | 默认执行者 |
| --- | --- | --- |
| A — 直接处理 | 需求明确、风险低、符合既有模式、容易验证 | 主对话，不启动子代理 |
| B — 常规工程 | 需要业务判断或相关组件协调，但不需要深度技术调查 | `terra_builder` |
| C — 复杂工程 | 根因不明确、跨模块、技术不确定性较高，但影响范围可控且能验证 | `sol_engineer` |
| D — 高风险审查 | 错误可能导致重大数据损失、安全暴露、生产故障、不可逆变更，或存在明确的能力缺口 | `astra_critical`，默认只做审查 |

## 设计原则

- 可靠性优先于成本；只有多个路线都能可靠完成时，才选择成本更低的路线。
- 不按文件数量、提示词长度、工具数量或技术关键词单独路由。
- 数据库、安全、迁移等关键词本身不意味着必须使用 Astra。
- 普通构建、测试、工具或环境失败，不应自动触发模型升级。
- 同一任务默认一次只运行一个子代理；Astra 与 Sol 不并行执行同一任务。
- Astra 默认审查方案、风险或代码差异，不因被调用就接管实现。
- 高影响任务可以先由 Astra 审查计划，再释放 Astra、交给 Sol 实施。
- 调用高风险代理不等于获得生产写入、破坏性 SQL 或不可逆操作的授权。

## 快速开始

1. 阅读 [SKILL.md](SKILL.md) 和 [路由策略](references/routing-policy.md)。
2. 将 Skill 放到当前 Codex 版本支持的 Skill 目录。
3. 将 [templates/AGENTS.md](templates/AGENTS.md) 合并进用户级或项目级指令，不要直接覆盖已有规则。
4. 将 `agents/` 下的 TOML 放到当前运行环境支持的自定义代理目录。
5. 修改模型 ID 和推理强度，使其匹配你的运行环境。
6. 运行 `python scripts/validate_package.py`，然后使用 [回归提示词](references/test-cases.md) 验证路由行为。

配置路径和模型 ID 会随 Codex 版本及部署方式变化。仓库中的代理文件是示例，不保证可在所有环境中原样使用。

## 验证

需要 Python 3.11+，无第三方依赖：

```bash
python scripts/validate_package.py
```

## 许可证

MIT，详见 [LICENSE](LICENSE)。
