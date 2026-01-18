# CyberGua 赛博卦 🔮

> 融合东方玄学与现代 AI 的命理预测系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Vue](https://img.shields.io/badge/Vue-3.x-green.svg)](https://vuejs.org/)

**简体中文** | [English](./README_EN.md)

---

## 📖 项目简介

**CyberGua 赛博卦** 是一个本地部署的命理预测应用，整合了三大传统术数系统：

- **八字** - 命运分析
- **梅花易数** - 事件预测
- **九宫飞星** - 空间优化

通过本地 AI 大语言模型（Ollama + Qwen）生成深度玄学解读报告。

### ✨ 核心特性

- 🎲 **双模式预测**
  - **简单版**：梅花易数快速起卦
  - **详细版**：命(八字) + 运(梅花) + 局(风水) 综合分析

- 🤖 **AI 赋能**
  - 使用 Qwen 大模型生成专业命理解读
  - 本地运行，隐私安全

- 🌐 **外应整合**
  - DuckDuckGo 实时搜索融入卦象分析

- 🎨 **现代化 UI**
  - Vue 3 + TailwindCSS 响应式设计
  - Luxury 黑金主题
  - 呼吸冥想引导动画

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────┐
│          前端 (Vue 3)                   │
│   ┌─────────────────────────────────┐   │
│   │  模式选择                        │   │
│   │  冥想引导                        │   │
│   │  输入表单（简单版/详细版）        │   │
│   │  结果展示                        │   │
│   └─────────────────────────────────┘   │
└──────────────┬──────────────────────────┘
               │ HTTP/JSON
               ▼
┌─────────────────────────────────────────┐
│        后端 (FastAPI)                   │
│   ┌──────────┬──────────┬──────────┐    │
│   │  梅花易数 │   八字    │  九宫飞星 │    │
│   └──────────┴──────────┴──────────┘    │
│   ┌─────────────────────────────────┐   │
│   │  AI 服务 (Ollama + Qwen)        │   │
│   │  外应搜索 (DuckDuckGo)          │   │
│   └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### 技术栈

| 层级     | 技术                                    |
| -------- | --------------------------------------- |
| 前端     | Vue 3 + Vite + TailwindCSS v3 + daisyUI |
| 后端     | FastAPI + Python 3.10+                  |
| AI 推理  | Ollama + Qwen 2.5                       |
| 命理算法 | lunar_python + 自研算法                 |
| 外应搜索 | DuckDuckGo Search API                   |

---

## 🚀 快速开始

### 前置要求

- Python 3.10+
- Node.js 18+
- Ollama（可选，用于 AI 分析）
- Docker & Docker Compose（可选，一键部署）

### 🐳 方式一：Docker 一键部署（推荐）

最简单的部署方式，一条命令启动所有服务：

```bash
# 克隆项目
git clone https://github.com/JWCodeWrote/CyberGua.git
cd CyberGua

# 一键启动（首次启动会自动下载 AI 模型，需要几分钟）
docker compose up -d

# 查看日志
docker compose logs -f

# 停止服务
docker compose down
```

启动后访问：

- 🌐 **前端**: http://localhost
- 🔧 **后端 API**: http://localhost:8000
- 🤖 **Ollama**: http://localhost:11434

> 💡 首次启动会自动下载 `qwen2.5:1.5b` 模型（约 1GB）。  
> 如需更高质量的 AI 分析，可修改 `docker-compose.yml` 中的模型为 `qwen2.5:7b` 或 `qwen2.5:14b`。

---

### 方式二：手动部署

如果不使用 Docker，可以手动部署各个服务。

#### 1. 克隆项目

```bash
git clone https://github.com/JWCodeWrote/CyberGua.git
cd CyberGua
```

#### 2. 启动后端

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境（必须执行！）
source venv/bin/activate    # Windows 用户请运行: venv\Scripts\activate

# 安装依赖
pip3 install -r requirements.txt

# 启动后端服务
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

后端将运行在：`http://localhost:8000`

#### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端将运行在：`http://localhost:5173`

#### 4. (可选) 启动 AI 服务

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

#### 📦 模型选择建议

| 模型             | 大小   | 速度    | 质量            | 适用场景     |
| ---------------- | ------ | ------- | --------------- | ------------ |
| **qwen2.5:1.5b** | ~1GB   | ⚡️ 极快 | ⭐ 入门         | 快速测试功能 |
| **qwen2.5:7b**   | ~4.7GB | 🚀 快   | ⭐⭐⭐ 均衡     | 日常使用推荐 |
| **qwen2.5:14b**  | ~9GB   | 🐢 慢   | ⭐⭐⭐⭐⭐ 最佳 | 深度专业解读 |

---

## 📚 使用指南

### 简单版

1. **冥想引导** - 闭眼深呼吸，专注当前问题
2. **报数起卦** - 凭直觉输入三个数字（1-64）
3. **提出问题** - 描述您想占卜的事情
4. **查看结果** - 本卦、变卦、体用关系 + AI 解读

### 详细版

1. **输入八字** - 提供出生年月日时（阳历）+ 性别
2. **梅花起卦** - 输入三个数字
3. **提出问题** - 描述您的人生大事
4. **综合报告**：
   - **命 (能否做?)** - 八字格局分析
   - **运 (何时做?)** - 梅花卦象吉凶
   - **局 (在哪做?)** - 风水方位建议

---

## 🔧 API 接口

### 健康检查

```http
GET /api/health
```

### 简单版预测

```http
POST /api/predict/simple
Content-Type: application/json

{
  "nums": [3, 5, 2],
  "question": "明天面试会顺利吗？"
}
```

### 详细版预测

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

## 📁 项目结构

```
CyberGua/
├── backend/                 # Python 后端
│   ├── main.py             # FastAPI 入口
│   ├── requirements.txt    # Python 依赖
│   ├── core/               # 核心算法
│   │   ├── meihua.py       # 梅花易数
│   │   ├── bazi.py         # 八字排盘
│   │   ├── fengshui.py     # 九宫飞星
│   │   └── crawler.py      # 外应搜索
│   └── services/
│       └── ai_service.py   # AI 调用
│
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── App.vue        # 主应用
│   │   ├── components/    # UI 组件
│   │   └── api/           # API 服务
│   └── package.json
│
└── README.md              # 本文件
```

---

## 🎯 算法说明

### 梅花易数

- **起卦规则**：
  - 下卦 = 第一数 % 8
  - 上卦 = 第二数 % 8
  - 变爻 = 第三数 % 6

- **体用分析**：
  - 体克用 = 吉
  - 用克体 = 凶
  - 用生体 = 进益
  - 体生用 = 泄气

### 八字

使用 `lunar_python` 库进行阳历转农历，排出四柱干支，分析日主强弱和喜用神。

### 风水

- **本命卦计算**：根据出生年份和性别
- **流年飞星**：九宫飞星方位吉凶

---

## 🐛 故障排查

### 前端崩溃

**问题**：`panicked at crates/oxide ... Utf8Error`  
**原因**：TailwindCSS v4 对中文支持问题  
**解决**：项目已降级到 v3

### AI 无响应

1. 检查 Ollama 服务：

   ```bash
   curl http://localhost:11434/api/tags
   ```

2. 确认模型已下载：
   ```bash
   ollama list
   ```

---

## 📝 待办事项

- [ ] 添加更多卦象解释库
- [ ] 支持时间起卦模式
- [ ] 增加用户历史记录
- [ ] Docker 一键部署
- [ ] 移动端适配优化

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 开源协议

MIT License - 详见 LICENSE 文件

---

## 🙏 致谢

- [lunar_python](https://github.com/6tail/lunar-python) - 农历/八字库
- [Ollama](https://ollama.ai/) - 本地 LLM 运行时
- [Qwen](https://github.com/QwenLM/Qwen) - 阿里通义千问模型
- [daisyUI](https://daisyui.com/) - TailwindCSS 组件库

---

**Built with ❤️ by the CyberGua Team**

_命运可算，未来可期_
