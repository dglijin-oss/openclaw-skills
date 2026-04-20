---
name: huashu-nuwa
description: |
  女娲造人：输入人名/主题/模糊需求，自动深度调研→思维框架提炼→生成可运行的人物Skill。
  触发词：「造skill」「蒸馏XX」「女娲」「造人」「XX的思维方式」「做个XX视角」「更新XX的skill」「我想提升决策质量」「有没有一种思维方式能帮我...」「我需要一个思维顾问」。
---

# 女娲 · Skill造人术

> 女娲造的不是人，是一面镜子——用另一个人的眼睛看自己的问题。

## 核心流程

### Phase 0: 入口分流

| 用户输入 | 路径 |
|---------|------|
| 明确的人名/主题 | **直接路径** → Phase 0A |
| 模糊的需求/困惑 | **诊断路径** → Phase 0B |

**Phase 0A（直接路径）**：确认人名 → 聚焦方向 → 用途 → 本地语料？ → 进入 Phase 0.5。用户说「就做XX」无更多信息 → 默认全面画像+思维顾问+无本地语料，直接推进。

**Phase 0B（诊断路径）**：最多2轮追问定位需求维度 → 推荐2-3个候选（人物或主题）→ 用户选择 → 已有Skill直接激活，新蒸馏候选进入Phase 0A。需求维度见 [references/diagnostic-dimensions.md](references/diagnostic-dimensions.md)。

### Phase 0.5: 创建Skill目录

```
skills/[person-name]-perspective/
├── SKILL.md
├── scripts/
└── references/
    ├── research/          # 6个Agent调研结果（必存）
    │   ├── 01-writings.md
    │   ├── 02-conversations.md
    │   ├── 03-expression-dna.md
    │   ├── 04-external-views.md
    │   ├── 05-decisions.md
    │   └── 06-timeline.md
    └── sources/           # 一手素材
```

- 每个subagent必须写入对应md文件，不存文件的调研等于没做
- 所有调研文件必须在skill目录内部（references/research/），skill必须自包含
- 中国人物：信息源切换为B站/小宇宙/权威中文媒体，知乎和微信公众号始终排除

### Phase 1: 多源信息采集（6 Agent并行）

启动6个并行subagent，每个负责不同维度：

| Agent | 搜索目标 | 输出文件 |
|-------|---------|---------|
| 1 著作 | 书、长文、核心论点、自创术语、推荐书单 | 01-writings.md |
| 2 对话 | 播客、长视频、AMA、深度采访 | 02-conversations.md |
| 3 表达 | 社交媒体、碎片表达、争议立场 | 03-expression-dna.md |
| 4 他者 | 他人分析、书评、批评、传记 | 04-external-views.md |
| 5 决策 | 重大决策、转折点、争议行为 | 05-decisions.md |
| 6 时间线 | 完整时间线、关键里程碑、最近12个月动态 | 06-timeline.md |

**采集模式**：
- **纯网络搜索**（默认）：6个Agent全部走网络搜索
- **本地语料优先**：先分析用户提供的素材，识别信息缺口，只对缺失维度启动网络搜索
- **纯本地语料**：只分析本地素材，不做网络搜索

**信息源黑名单**：排除知乎、微信公众号、百度百科。中文只接受36氪、极客公园、晚点LatePost、财新等权威媒体。

**Agent超时**：搜索5分钟无有价值结果→不等待，继续推进。宁可生成诚实标注了局限的60分Skill，不要编造90分Skill。

### Phase 1.5: 调研Review检查点

展示调研质量摘要（来源数量、关键发现、矛盾点、信息不足维度）。用户确认OK→进入Phase 2。

### Phase 2: 框架提炼

读取 [references/extraction-framework.md](references/extraction-framework.md) 获取三重验证方法论。

**2.1 心智模型**（3-7个）：三重验证筛选（跨域复现、生成力、排他性），宁少勿多。
**2.2 决策启发式**（5-10条）：「如果X，则Y」格式，有具体案例支撑。
**2.3 表达DNA**：句式偏好、词汇特征、节奏感、幽默方式、确定性表达、引用习惯。
**2.4 价值观与反模式**：3-5条核心价值排序，此人明确反对的行为。
**2.5 智识谱系**：受谁影响→影响了谁→思想地图位置。
**2.6 诚实边界**：明确写出局限，包括信息截止日期。

### Phase 2.5: 提炼确认检查点

展示提炼摘要（心智模型数量、决策启发式数量、表达DNA特征、核心张力、诚实边界）。用户确认OK→进入Phase 3。

### Phase 3: Skill构建

读取 [references/skill-construction.md](references/skill-construction.md) 获取模板和回答工作流生成指引。

将Phase 2提炼结果按模板结构填入，生成 `skills/[person-name]-perspective/SKILL.md`。
- 身份卡用此人语气写50字自我介绍
- 回答工作流（Agentic Protocol）必须根据心智模型自动推导研究维度
- 必须包含Step 2的研究维度（从心智模型反推，不是通用搜索）

### Phase 4: 质量验证

用独立subagent执行3项测试：
1. **已知测试**：选3个此人公开表态过的问题，对比实际立场
2. **边缘测试**：选1个未公开讨论过的相关问题，推断应含不确定性标注
3. **风格测试**：写100字分析，判断是否有此人表达特征（非通用AI味）

通过标准见 [references/extraction-framework.md](references/extraction-framework.md) 末尾。最多循环2轮迭代。

### Phase 5: 双Agent精炼（标准后置）

并行启动两个Agent（auto-skill-optimizer视角 + skill-creator视角）→ 综合改进 → 展示变更摘要请用户确认。

## 更新已有Skill

读取现有SKILL.md → 只启动Agent 2（最新对话）+ Agent 5（最新决策）+ Agent 6（时间线更新）→ 增量更新，不重写整个Skill。

## 特殊场景

- **主题Skill**（非人名）：去掉角色扮演规则，改为「框架概览」+「流派对比」
- **中国人物**：B站/小宇宙/权威中文媒体优先
- **冷门人物**（<10条来源）：心智模型减至2-3个，加大诚实边界篇幅，提前告知用户
- **蒸馏用户自己**：引导用户提供一手素材（文章/博客/视频/备忘录）
