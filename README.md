# OpenClaw Skills

个人定制的 OpenClaw 技能集合，用于自动化抖音内容分析和账号拆解。

## 📦 技能列表

### 1. Account Analyzer - 对标账号拆解 🔍

自动化拆解抖音对标账号，提取爆款因子、分析起号路径、识别变现模式。

**功能：**
- 自动抓取博主主页所有视频数据（标题、点赞、评论）
- 数据统计分析（平均/中位/最高点赞，破百赞/千赞数量）
- 起号路径分析（最高赞、破百赞、破千赞视频识别）
- 热门话题标签提取
- 爆款因子分析（疑问式/感叹式/数字型标题检测）
- 视频文案转写（可选，基于 Whisper）
- 一键生成 Markdown 分析报告

**用法：**
```bash
python3 skills/account-analyzer/scripts/analyze.py \
  --profile-url "https://www.douyin.com/user/XXXXX" \
  --mode basic \
  --transcribe-top 5
```

### 2. Douyin Video Transcriber - 抖音视频转写 🎙️

批量下载抖音视频并转写为文字文案。

**功能：**
- 支持单个视频或博主主页批量转写
- 基于本地 Whisper 模型（无需 API 密钥）
- 按点赞排序取 Top N 条
- 自动生成 Markdown 报告

**用法：**
```bash
# 单条视频
python3 skills/douyin-video-transcriber/scripts/run.py \
  --url "https://www.douyin.com/video/XXXXX"

# 博主主页批量
python3 skills/douyin-video-transcriber/scripts/batch_transcribe.py \
  --profile-url "https://www.douyin.com/user/XXXXX" \
  --top 20
```

### 3. Nuwa - 女娲造人 👤

输入人名/主题/模糊需求，自动深度调研→思维框架提炼→生成可运行的人物 Skill。

### 4. Self-Evolve - 自我进化 🧬

自动识别弱点、修复问题、编写新技能，持续改进 Agent 能力。

## 🛠️ 前置条件

- Python 3.10+
- ffmpeg
- OpenAI Whisper (`pip install openai-whisper`)
- Playwright (`pip install playwright`)
- yt-dlp (`pip install yt-dlp`)

## 📝 License

MIT
