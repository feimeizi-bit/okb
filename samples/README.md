# samples — 样例数据与样例结果

> 赛题交付物 3.b 要求：提供少量示例任务、示例运行证据和示例评分结果

## 规划内容

```
samples/
├─ paper_sample.jsonl       # 少量示例题目（覆盖 6 个能力维度）
├─ evidence_sample/         # 示例运行证据（evidence.jsonl + raw/ 摘录）
└─ report_sample/           # 示例评分结果（六维分数 + 每题理由）
```

## 约定

- 样例只放**少量、脱敏、可公开**的内容；批量运行产物留在虚拟机 `runs/` 中，不入库
- 样例中的敏感信息使用占位符（对齐接口单 I-12）
- 样例结果需与 `notes/runlog.md` 中的真实 run 记录对应，可追溯
