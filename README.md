# okb — openKylin 长期记忆评测 benchmark

工作目录说明。当前只放了**规划与协作类文档**，代码和 schema 还没开始写。

## 目录

```
okb/
├─ README.md                          ← 本文件
├─ docs/
│  └─ interface-request-v0.2.md       ← 接口需求单（B 提给 A，待 A 逐条回复）
└─ notes/
   ├─ claims.md                       ← 说法 vs 证据对照表（每周五花 10 分钟更新）
   └─ runlog.md                       ← 跑批日志（每次跑批追加一条）
```

## 当前状态

| 事项 | 状态 | 负责人 |
|---|---|---|
| 接口需求单 v0.2 | A 已逐条回复（见 `docs/interface-response-v0.2.md`），**待 B 复核 I-9 / I-12 / I-14** | A/B |
| `docs/CONTRACT.md`（人话版接口说明 + 变更规则） | 未开始，等 B 复核后抄录冻结 | A/B |
| `schemas/evidence.schema.json` | 未开始，字段基线见需求单 I-1 | A（B 提要求） |
| `schemas/sample.schema.json` | 未开始 | B |
| 合成考生（三档 mock agent） | 未开始 | B |
| openKylin 虚拟机 + 两款 Agent | ✅ **已完成**（openKylin 3.0 + OpenClaw + Hermes，见 `docs/SETUP_VM_AGENTS.md`） | A |

## 下一步三件事

1. B 复核 `docs/interface-response-v0.2.md` 的 I-9 / I-12 / I-14，通过后抄入 `docs/CONTRACT.md`
2. A 开始设计证据采集（对话 / 记忆读写 / 文件变更），对齐 I-1 证据流水格式
3. B 开始合成考生（三档 mock agent），A 完成 schema 基线后即可联调

## 术语约定

| 词 | 含义 |
|---|---|
| A / B | A = 评测框架线，B = 数据与评分线 |
| run / run_id | 一次完整的批量评测运行 / 它的编号 |
| evidence | 运行证据：对话、记忆读写、工具调用、文件变更 |
| verdict | 单条样本的判定结论：记住 / 遗漏 / 混淆 / 错误持久化 / 错误复用 |
| 判官（judge） | 用大模型做语义评分的那个模型 |
| κ（Cohen's Kappa） | 自动评分与人工评分的一致性系数，用于证明评分可信 |
| 合成考生（mock agent） | 不走真实模型的假 Agent，用来当"标尺"检验样本区分度 |
