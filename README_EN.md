# CyberGua 🔮

> A fortune-telling system combining Eastern metaphysics with modern AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Vue](https://img.shields.io/badge/Vue-3.x-green.svg)](https://vuejs.org/)

[中文文档](./README.md) | **English**

---

## Introduction

**CyberGua** is a locally-deployed fortune-telling application that integrates three traditional Chinese divination systems:

- **BaZi (Eight Characters)** - Destiny analysis
- **Plum Blossom Numerology** - Event prediction
- **Flying Stars Feng Shui** - Spatial optimization

Enhanced with AI-powered analysis using Ollama and Qwen models for deep metaphysical interpretation.

### Key Features

- 🎲 **Dual Prediction Modes**
  - **Simple Mode**: Quick hexagram divination with Plum Blossom
  - **Detailed Mode**: Comprehensive analysis with BaZi + Hexagram + Feng Shui

- 🤖 **AI-Powered Interpretation**
  - Professional metaphysics analysis with Qwen LLM
  - Local deployment ensures privacy protection

- 🌐 **External Signs Integration**
  - Real-time web search via DuckDuckGo integrated into divination context

- 🎨 **Modern Interface**
  - Responsive design with Vue 3 + TailwindCSS
  - Luxury dark-gold cyberpunk theme
  - Meditation guidance with breathing animations

---

## Architecture

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
│   │ Plum Blo │  Eight   │  Flying  │    │
│   │   wer    │   Char   │  Stars   │    │
│   └──────────┴──────────┴──────────┘    │
│   ┌─────────────────────────────────┐   │
│   │  AI Service (Ollama + Qwen)     │   │
│   │  External Signs (DuckDuckGo)    │   │
│   └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Tech Stack

| Layer          | Technology                              |
| -------------- | --------------------------------------- |
| Frontend       | Vue 3 + Vite + TailwindCSS v3 + daisyUI |
| Backend        | FastAPI + Python 3.10+                  |
| AI Inference   | Ollama + Qwen 2.5                       |
| Divination     | lunar_python + Custom algorithms        |
| External Signs | DuckDuckGo Search API                   |

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Ollama (Optional, for AI analysis)

### 1. Clone Repository

```bash
git clone https://github.com/JWCodeWrote/CyberGua.git
cd CyberGua
```

### 2. Start Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Backend will run at: `http://localhost:8000`

### 3. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at: `http://localhost:5173`

### 4. (Optional) Start AI Service

#### 🍎 macOS Users

1. **Install Ollama**

   ```bash
   brew install ollama
   ```

2. **Start Service**

   ```bash
   ollama serve
   ```

3. **Download Model**
   ```bash
   ollama pull qwen2.5:1.5b
   ```

#### 🪟 Windows Users

1. **Install Ollama**
   - Visit [Ollama Official Site](https://ollama.com/download/windows) to download installer
   - Run `OllamaSetup.exe`
   - Ollama will auto-start after installation

2. **Verify Installation**
   - Open PowerShell or CMD
   - Type `ollama` to check output

3. **Download Model**
   ```powershell
   ollama pull qwen2.5:1.5b
   ```

#### 🐧 Linux Users

1. **One-Click Install**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
2. **Start Service**
   ```bash
   ollama serve
   ```
3. **Download Model**
   ```bash
   ollama pull qwen2.5:1.5b
   ```

---

#### 📦 Model Selection Guide

| Model            | Size   | Speed        | Quality         | Use Case                |
| ---------------- | ------ | ------------ | --------------- | ----------------------- |
| **qwen2.5:1.5b** | ~1GB   | ⚡️ Very Fast | ⭐ Basic        | Quick testing           |
| **qwen2.5:7b**   | ~4.7GB | 🚀 Fast      | ⭐⭐⭐ Balanced | Daily use (Recommended) |
| **qwen2.5:14b**  | ~9GB   | 🐢 Slow      | ⭐⭐⭐⭐⭐ Best | Professional analysis   |

---

## User Guide

### Simple Mode

1. **Meditation** - Close eyes, deep breathe, focus on your question
2. **Number Selection** - Input three numbers (1-64) intuitively
3. **Ask Question** - Describe what you want to divine
4. **View Result** - Original hexagram, changed hexagram, Ti-Yong analysis + AI interpretation

### Detailed Mode

1. **Input BaZi** - Provide birth date/time (Solar calendar) + Gender
2. **Hexagram** - Input three numbers
3. **Ask Question** - Describe your life matter
4. **Comprehensive Report**:
   - **Destiny (Can I do it?)** - BaZi analysis
   - **Timing (When to do it?)** - Hexagram fortune
   - **Location (Where to do it?)** - Feng Shui direction

---

## API Endpoints

### Health Check

```http
GET /api/health
```

### Simple Prediction

```http
POST /api/predict/simple
Content-Type: application/json

{
  "nums": [3, 5, 2],
  "question": "Will tomorrow's interview go well?"
}
```

### Detailed Prediction

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
  "question": "Am I suitable for entrepreneurship?"
}
```

---

## Project Structure

```
CyberGua/
├── backend/                 # Python backend
│   ├── main.py             # FastAPI entry
│   ├── requirements.txt    # Python dependencies
│   ├── core/               # Core algorithms
│   │   ├── meihua.py       # Plum Blossom divination
│   │   ├── bazi.py         # BaZi calculator
│   │   ├── fengshui.py     # Flying Stars
│   │   └── crawler.py      # External signs
│   └── services/
│       └── ai_service.py   # AI service
│
├── frontend/               # Vue 3 frontend
│   ├── src/
│   │   ├── App.vue        # Main app
│   │   ├── components/    # UI components
│   │   └── api/           # API services
│   └── package.json
│
└── README.md              # This file
```

---

## Algorithm Details

### Plum Blossom Numerology

- **Hexagram Rules**:
  - Lower trigram = num1 % 8
  - Upper trigram = num2 % 8
  - Moving line = num3 % 6

- **Ti-Yong Analysis**:
  - Ti overcomes Yong = Auspicious
  - Yong overcomes Ti = Inauspicious
  - Yong generates Ti = Beneficial
  - Ti generates Yong = Draining

### BaZi (Eight Characters)

Uses `lunar_python` library to convert solar to lunar calendar, derive Four Pillars, and analyze day master strength and favorable elements.

### Feng Shui (Flying Stars)

- **Ming Gua Calculation**: Based on birth year and gender
- **Flying Stars**: Annual star positions for fortune analysis

---

## Troubleshooting

### Frontend Crashes

**Issue**: `panicked at crates/oxide ... Utf8Error`  
**Cause**: TailwindCSS v4 UTF-8 bug with Chinese characters  
**Solution**: Project uses TailwindCSS v3 (stable version)

### AI Not Responding

1. Check Ollama service:

   ```bash
   curl http://localhost:11434/api/tags
   ```

2. Verify model downloaded:
   ```bash
   ollama list
   ```

---

## TODO

- [ ] Add more hexagram interpretation library
- [ ] Support time-based hexagram generation
- [ ] Add user history tracking
- [ ] Docker one-click deployment
- [ ] Mobile UI optimization

---

## Contributing

Issues and Pull Requests are welcome!

---

## License

MIT License - See LICENSE file for details

---

## Acknowledgments

- [lunar_python](https://github.com/6tail/lunar-python) - Lunar calendar library
- [Ollama](https://ollama.ai/) - Local LLM runtime
- [Qwen](https://github.com/QwenLM/Qwen) - Alibaba Qwen model
- [daisyUI](https://daisyui.com/) - TailwindCSS component library

---

**Built with ❤️ by the CyberGua Team**

_Destiny can be calculated, future can be anticipated_
