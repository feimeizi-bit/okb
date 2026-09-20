# 接口需求单 v0.2 · A 侧回复

> 回复方：A（评测框架线）　接收方：B（数据与评分线）
> 回复日：2026-09-20　期望复核日：2026-09-22（回复日 + 2 天）
> 状态：待 B 复核 I-9 / I-12 / I-14

## 0. 总览

- 13 条需求：**确认 11 条**（其中 4 条附补充说明），**改成这样 2 条**（I-9、I-12）
- 另提 **1 条新增建议**（I-14，样本 fixture）
- 需 B 复核：**I-9、I-12、I-14**；复核通过后抄入 `docs/CONTRACT.md` 并冻结

## 1. 逐条回复

| 编号 | A 的回复 | A 的补充说明 |
|---|---|---|
| I-1 | 确认 | 需共同冻结枚举，见 2.1 |
| I-2 | 确认 | 建议签名见 2.2；缺能力项标 skip，不整批报错 |
| I-3 | 确认（有条件） | 仅 `capabilities().memory = true` 的 Agent 提供；无记忆后端时该维度记 N/A |
| I-4 | 确认 | 跨会话分两类实现，见 2.3 |
| I-5 | 确认 | 字段照单全收，建议补 `schema_version` / openKylin 版本 / host / agent 启动 argv |
| I-6 | 确认 | 顶层五件套不动；`raw/` 内部按 `raw/<task_id>/` 组织，内部文件名 A 侧自定 |
| I-7 | 确认（最好有） | 映射表 `action_map/<agent>.yaml`；未映射动作不静默跳过，报告打 warning |
| I-8 | 确认 | dialogue 必须支持；memory_api / file_drop 按 capabilities 条件支持，缺则 skip |
| I-9 | **改成这样** | status 增加 `skip`，与 invalid 区分，见 2.4；**待 B 复核** |
| I-10 | 确认 | 每 run 独立记忆路径 + 工作目录；建议先串行跑批（本地模型资源有限），天然互不干扰 |
| I-11 | 确认（加约束） | 大文件只存 sha256 + 前 64KB + truncated 标记；raw 允许 gzip，见 2.5 |
| I-12 | **改成这样** | 用确定性占位符替代掩码/哈希，见 2.6；**待 B 复核** |
| I-13 | 确认（最好有） | replay 模式 + judge cache，缓存键细化见 2.7 |
| I-14 | 新增建议 | 样本声明 fixture 清单，A 负责布置与恢复，见 2.8；**待 B 复核** |

## 2. 逐条细节

### 2.1 I-1 枚举冻结（需共同确认）

- `source ∈ {dialogue, memory, file, tool, system}`
- `type` 建议值：`message / memory_read / memory_write / file_read / file_write / tool_call / tool_result / error`
- `actor ∈ {user, agent, env}`
- `id` 规则：`ev_<run短号>_<6位序号>`，`seq` 在 run 内单调递增、不按 task 重置

### 2.2 I-2 接口签名（建议）

```
capabilities() -> {
  "dialogue": bool, "memory": bool, "file": bool, "tool": bool,
  "notes": str   # 能力限制说明，如"记忆仅存进程内存，不支持跨会话"
}
```

### 2.3 I-4 跨会话的两类实现

- 类 1（Agent 有会话参数）：切换 session 时重置对话上下文，持久记忆目录不变
- 类 2（无会话概念）：重启 Agent 进程实现同等语义
- 限制：记忆仅存进程内存的 Agent 无法测跨会话，manifest 标注 limitation，对应维度记 N/A

### 2.4 I-9 任务状态（改成这样，待复核）

```
status ∈ {ok, timeout, agent_error, env_error, skip}
```

- invalid（剔除能力统计）= `timeout / agent_error / env_error`
- `skip` = 能力缺失或样本条件不满足（如无记忆后端跑记忆样本），**单独统计，不与 invalid 混列**
- 报告分列 5 类数量；理由：环境抽风与能力缺失是两种性质，混在一起会污染"稳定性"证据

### 2.5 I-11 存储约束

- 全量保留：LLM 请求/响应、工具调用参数、文件写入前后内容（文本）
- 单文件 > 1MB：只存 `sha256` + 前 64KB + `truncated: true`
- `raw/` 允许 `.jsonl.gz`；`evidence.jsonl` 的 `raw_ref` 必须能定位到文件 + 行号

### 2.6 I-12 脱敏方案（改成这样，待复核）

- 敏感值在样本中即以占位符定义，如 `<PII_PHONE_1>`
- 落盘证据中真实值 → 占位符全局替换；映射表只存内存，不落盘
- 判官看到占位符仍可判"是否泄露 / 是否持久化 / 是否拒绝"
- Agent 若原样吐出真实值：证据中保留占位符版本，另加 `pii_leak_detected: true`
- 理由：纯掩码会丢失"是否引用敏感信息"的判据；纯哈希可判但可读性差，占位符两者兼得

### 2.7 I-13 离线复现

- `bench replay --run <run_id>`：不重跑 Agent，只重跑评分
- judge cache 键 = `sha256(证据行 + 判官版本 + prompt 模板版本)`，存 `runs/<run_id>/raw/judge_cache.jsonl`
- 判官调用失败自动重试；仍失败标 `judge_error`，不污染分数

### 2.8 I-14 样本 fixture（新增，待复核）

- 文件类样本需声明初始工作区，否则不可复现
- 建议 sample schema 增加：

```json
"fixture": [{"path": "订单.yaml", "content": "...", "encoding": "utf-8"}]
```

- A 在 task 开始前按 fixture 重建 workspace，结束后清理

## 3. A 侧实施承诺

1. 适配器架构：CLI 只认 `agent.yaml` + `capabilities()`，接入第二款 Agent 只改配置（支撑 claims C-1，将以 git diff 统计改动行数）
2. `okb` 仓库尽快 `git init`，保证 C-1 / C-4 的 diff 与重跑证据可产出
3. 收到 B 对 I-9 / I-12 / I-14 的复核后，24 小时内抄入 `docs/CONTRACT.md`

## 4. 变更记录

| 版本 | 日期 | 改了什么 | 谁改的 |
|---|---|---|---|
| v0.2-r1 | 2026-09-20 | A 首次逐条回复：11 确认 + 2 改成这样 + 1 新增 | A |
