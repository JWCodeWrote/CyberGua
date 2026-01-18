# CyberGua 赛博卦 🔮

> 融合东方玄学与现代 AI 的命理预测系统  
> A fortune-telling system combining Eastern metaphysics with modern AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Vue](https://img.shields.io/badge/Vue-3.x-green.svg)](https://vuejs.org/)

---

## 📖 简介 | Introduction

**CyberGua** 是一个本地部署的命理预测应用，整合了八字、梅花易数、九宫飞星三大传统术数系统，并通过 AI 大语言模型（Ollama + Qwen）生成深度解读报告。

**CyberGua** is a locally-deployed fortune-telling application that integrates three traditional Chinese divination systems: BaZi (Eight Characters), Plum Blossom Numerology, and Flying Stars Feng Shui, enhanced with AI-powered analysis using Ollama and Qwen models.

### ✨ 核心特性 | Key Features

- 🎲 **双模式预测 | Dual Prediction Modes**
  - **简单版 Simple Mode**: 梅花易数快速起卦 | Quick divination with Plum Blossom
  - **详细版 Detailed Mode**: 命(八字) + 运(梅花) + 局(风水) 综合分析 | Comprehensive analysis with BaZi + Hexagram + Feng Shui

- 🤖 **AI 赋能 | AI-Powered**
  - 使用 Qwen 大模型生成专业命理解读 | Professional metaphysics interpretation with Qwen LLM
  - 本地运行，隐私安全 | Local deployment, privacy guaranteed

- 🌐 **外应整合 | External Signs Integration**
  - DuckDuckGo 实时搜索融入卦象分析 | Real-time web search integrated into divination

- 🎨 **现代化 UI | Modern Interface**
  - Vue 3 + TailwindCSS 响应式设计 | Responsive design with Vue 3 + TailwindCSS
  - Luxury 黑金主题 | Luxury dark-gold theme
  - 呼吸冥想引导动画 | Meditation guidance with breathing animations

---

## 🏗️ 技术架构 | Architecture

```
┌─────────────────────────────────────────┐
│          Frontend (Vue 3)               │
│   ┌─────────────────────────────────┐   │
│   │  Mode Selection                 │   │
│   │  Meditation View                │   │
│   │  Input Forms (Simple/Detailed)  │   │
│   │  Result Display                 │   │
│   └─────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │ HTTP/JSON
               ▼
┌─────────────────────────────────────────┐
│        Backend (FastAPI)                │
│   ┌──────────┬──────────┬──────────┐    │
│   │  Meihua  │   BaZi   │ FengShui │    │
│   │ 梅花易数  │   八字    │  九宫飞星  │    │
│   └──────────┴──────────┴──────────┘    │
│   ┌─────────────────────────────────┐   │
│   │  AI Service (Ollama + Qwen)     │   │
│   │  外应搜索 (DuckDuckGo)            │   │
│   └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### 技术栈 | Tech Stack

| 层级 Layer              | 技术 Technology                           |
| ----------------------- | ----------------------------------------- |
| 前端 Frontend           | Vue 3 + Vite + TailwindCSS v3 + daisyUI   |
| 后端 Backend            | FastAPI + Python 3.10+                    |
| AI 推理 AI Inference    | Ollama + Qwen 2.5                         |
| 命理算法 Divination     | lunar_python + 自研算法 Custom algorithms |
| 外应搜索 External Signs | DuckDuckGo Search API                     |

---

## 🚀 快速开始 | Quick Start

### 前置要求 | Prerequisites

- Python 3.10+
- Node.js 18+
- Ollama (可选，用于 AI 分析 | Optional, for AI analysis)

### 1. 克隆项目 | Clone Repository

```bash
git clone https://github.com/JWCodeWrote/CyberGua.git
cd CyberGua
```

### 2. 启动后端 | Start Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

后端将运行在: `http://localhost:8000`  
Backend will run at: `http://localhost:8000`

### 3. 启动前端 | Start Frontend

```bash
cd frontend
npm install
npm run dev
```

前端将运行在: `http://localhost:5173`  
Frontend will run at: `http://localhost:5173`

### 4. (可选) 启动 AI 服务 | (Optional) Start AI Service

#### 🍎 macOS 用户

1. **安装 Ollama**

   ```bash
   brew install ollama
   ```

2. **启动服务**

   ```bash
   ollama serve
   ```

3. **下载模型**
   ```bash
   ollama pull qwen2.5:1.5b
   ```

#### 🪟 Windows 用户

1. **安装 Ollama**
   - 访问 [Ollama 官网](https://ollama.com/download/windows) 下载 Windows 安装包
   - 双击运行 `OllamaSetup.exe`
   - 安装完成后，Ollama 通常会自动在后台运行

2. **验证运行**
   - 打开 PowerShell 或 CMD
   - 输入 `ollama` 查看是否有输出

3. **下载模型**
   ```powershell
   ollama pull qwen2.5:1.5b
   ```

#### 🐧 Linux 用户

1. **一键安装**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
2. **启动服务**
   ```bash
   ollama serve
   ```
3. **下载模型**
   ```bash
   ollama pull qwen2.5:1.5b
   ```

---

#### 📦 模型选择建议 | Model Selection

| 模型 Model       | 大小 Size | 速度 Speed | 质量 Quality    | 适用场景 Usecase |
| ---------------- | --------- | ---------- | --------------- | ---------------- |
| **qwen2.5:1.5b** | ~1GB      | ⚡️ 极快    | ⭐ 入门         | 快速测试功能     |
| **qwen2.5:7b**   | ~4.7GB    | 🚀 快      | ⭐⭐⭐ 均衡     | 日常使用推荐     |
| **qwen2.5:14b**  | ~9GB      | 🐢 慢      | ⭐⭐⭐⭐⭐ 最佳 | 深度专业解读     |

````

---

## 📚 使用指南 | User Guide

### 简单版 | Simple Mode

1. **冥想引导** - 闭眼深呼吸，专注当前问题
2. **报数起卦** - 凭直觉输入三个数字 (1-64)
3. **提出问题** - 描述您想占卜的事情
4. **查看结果** - 本卦、变卦、体用关系 + AI 解读

### 详细版 | Detailed Mode

1. **输入八字** - 提供出生年月日时 (阳历) + 性别
2. **梅花起卦** - 输入三个数字
3. **提出问题** - 描述您的人生大事
4. **综合报告** -
   - **命 (能否做?)** - 八字格局分析
   - **运 (何时做?)** - 梅花卦象吉凶
   - **局 (在哪做?)** - 风水方位建议

---

## 🔧 API 接口 | API Endpoints

### 健康检查 | Health Check

```http
GET /api/health
````

### 简单版预测 | Simple Prediction

```http
POST /api/predict/simple
Content-Type: application/json

{
  "nums": [3, 5, 2],
  "question": "明天面试会顺利吗？"
}
```

### 详细版预测 | Detailed Prediction

```http
POST /api/predict/detailed
Content-Type: application/json

{
  "birth_year": 1990,
  "birth_month": 5,
  "birth_day": 20,
  "birth_hour": 14,
  "gender": "male",
  "nums": [3, 5, 2],
  "question": "我适合创业吗？"
}
```

---

## 📁 项目结构 | Project Structure

```
CyberGua/
├── backend/                 # Python 后端 | Python backend
│   ├── main.py             # FastAPI 入口 | FastAPI entry
│   ├── requirements.txt    # Python 依赖 | Python dependencies
│   ├── core/               # 核心算法 | Core algorithms
│   │   ├── meihua.py       # 梅花易数 | Plum Blossom
│   │   ├── bazi.py         # 八字排盘 | BaZi calculator
│   │   ├── fengshui.py     # 九宫飞星 | Flying Stars
│   │   └── crawler.py      # 外应搜索 | External signs
│   └── services/
│       └── ai_service.py   # AI 调用 | AI service
│
├── frontend/               # Vue 3 前端 | Vue 3 frontend
│   ├── src/
│   │   ├── App.vue        # 主应用 | Main app
│   │   ├── components/    # UI 组件 | UI components
│   │   └── api/           # API 服务 | API services
│   └── package.json
│
└── README.md              # 本文件 | This file
```

---

## 🎯 算法说明 | Algorithm Details

### 梅花易数 | Plum Blossom Numerology

- **起卦规则 | Hexagram Rules**:
  - 下卦 = 第一数 % 8 | Lower trigram = num1 % 8
  - 上卦 = 第二数 % 8 | Upper trigram = num2 % 8
  - 变爻 = 第三数 % 6 | Moving line = num3 % 6

- **体用分析 | Ti-Yong Analysis**:
  - 体克用 = 吉 | Ti overcomes Yong = Auspicious
  - 用克体 = 凶 | Yong overcomes Ti = Inauspicious
  - 用生体 = 进益 | Yong generates Ti = Beneficial
  - 体生用 = 泄气 | Ti generates Yong = Draining

### 八字 (BaZi)

使用 `lunar_python` 库进行阳历转农历，排出四柱干支，分析日主强弱和喜用神。

Uses `lunar_python` to convert solar to lunar calendar, derive Four Pillars, and analyze day master strength and favorable elements.

### 风水 (Feng Shui)

- **本命卦计算 | Ming Gua Calculation**: 根据出生年份和性别 | Based on birth year and gender
- **流年飞星 | Flying Stars**: 九宫飞星方位吉凶 | Annual star positions

---

## 🐛 故障排查 | Troubleshooting

### 前端崩溃 | Frontend Crashes

**问题 | Issue**: `panicked at crates/oxide ... Utf8Error`  
**原因 | Cause**: TailwindCSS v4 对中文支持问题 | TailwindCSS v4 UTF-8 bug with Chinese  
**解决 | Solution**: 项目已降级到 v3 | Project downgraded to v3

### AI 无响应 | AI Not Responding

1. 检查 Ollama 服务 | Check Ollama service:

   ```bash
   curl http://localhost:11434/api/tags
   ```

2. 确认模型已下载 | Verify model downloaded:
   ```bash
   ollama list
   ```

---

## 📝 待办事项 | TODO

- [ ] 添加更多卦象解释库 | Add more hexagram interpretations
- [ ] 支持时间起卦模式 | Support time-based hexagram generation
- [ ] 增加用户历史记录 | Add user history tracking
- [ ] Docker 一键部署 | Docker one-click deployment
- [ ] 移动端适配优化 | Mobile UI optimization

---

## 🤝 贡献 | Contributing

欢迎提交 Issue 和 Pull Request！  
Issues and Pull Requests are welcome!

---

## 📄 开源协议 | License

MIT License - 详见 LICENSE 文件  
MIT License - See LICENSE file for details

---

## 🙏 致谢 | Acknowledgments

- [lunar_python](https://github.com/6tail/lunar-python) - 农历/八字库 | Lunar calendar library
- [Ollama](https://ollama.ai/) - 本地 LLM 运行时 | Local LLM runtime
- [Qwen](https://github.com/QwenLM/Qwen) - 阿里通义千问模型 | Alibaba Qwen model
- [daisyUI](https://daisyui.com/) - TailwindCSS 组件库 | TailwindCSS component library

---

**Built with ❤️ by the CyberGua Team**

_命运可算，未来可期 | Destiny can be calculated, future can be anticipated_
