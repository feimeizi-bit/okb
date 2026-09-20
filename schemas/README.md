# schemas — 数据契约

> 状态：待 B 复核接口回复后冻结（见 `../docs/interface-response-v0.2.md`）

## 规划文件

| 文件 | 内容 | 负责人 |
|---|---|---|
| `evidence.schema.json` | 证据流水字段基线（对齐接口单 I-1：`id/run_id/seq/ts/task_id/session_id/turn/source/type/actor/payload/raw_ref`） | A |
| `sample.schema.json` | 测试样本结构（六维场景、write/probe 阶段、fixture、标准答案、judge 类型） | B |

## 冻结规则

- 字段与枚举取值以 `docs/CONTRACT.md` 为唯一权威（B 复核 I-9/I-12/I-14 后抄录）
- 冻结后只允许新增字段，不允许改名或删除（变更需在 CONTRACT.md 记录）
