# engine — 考试流程引擎

> 负责人：A　状态：待开发（接口冻结后开工）

## 职责

驱动一次完整评测的运行（对应模块 A 的任务 2、3）：

```
读题（paper.jsonl）→ 为每个 agent × 每道题：
  准备 workspace（fixture）→ 快照
  写入阶段（write_phase）→ 跨会话（重启/清上下文）
  干扰 + 探测（probe_phase）
  收集证据（对话 / 记忆读写 / 文件变更）
→ 打包 runs/<run_id>/（evidence.jsonl + raw/ + manifest.json）
```

## 规划中的模块

| 文件 | 职责 | 对齐接口 |
|---|---|---|
| `runner.py` | 批量调度（agents × samples）、状态机 | I-9 |
| `adapter.py` | Agent 适配器基类：capabilities/reset/send/probe_memory | I-2/I-3/I-4 |
| `adapters/` | 各 Agent 的具体适配器（openclaw、hermes） | I-7 action_map |
| `collectors.py` | 对话/记忆/文件/工具四路证据采集 | I-1/I-10/I-11 |
| `workspace.py` | 运行空间管理（fixture 布置、快照、清理） | I-10/I-14 |

## 约定

- 证据字段以 `docs/interface-response-v0.2.md` 冻结后的 `CONTRACT.md` 为准
- 批量运行日志追加到 `notes/runlog.md`
- 第三方 Agent 本体不入库，仅通过 `deploy/` 脚本安装
