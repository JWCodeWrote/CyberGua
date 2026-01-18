"""
赛博玄学 API 服务入口

提供以下接口:
- GET  /api/health          健康检查
- POST /api/predict/simple  简单版预测 (梅花易数)
- POST /api/predict/detailed 详细版预测 (命+运+局)
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime

from core import MeihuaCalculator, BaziCalculator, FengshuiCalculator, ContextCrawler
from services import AIService

# 创建 FastAPI 应用
app = FastAPI(
    title="赛博玄学 API",
    description="整合八字、梅花易数、九宫飞星的命理预测系统",
    version="1.0.0",
)

# CORS 配置 (允许前端跨域请求)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化计算器
meihua = MeihuaCalculator()
bazi = BaziCalculator()
fengshui = FengshuiCalculator()
crawler = ContextCrawler()
ai = AIService()


# ==================== 请求/响应模型 ====================

class SimpleRequest(BaseModel):
    """简单版请求"""
    nums: list[int] = Field(..., min_length=3, max_length=3, description="三个数字 (1-64)")
    question: str = Field(..., min_length=1, max_length=500, description="问题")


class DetailedRequest(BaseModel):
    """详细版请求"""
    birth_year: int = Field(..., ge=1900, le=2100, description="出生年份")
    birth_month: int = Field(..., ge=1, le=12, description="出生月份")
    birth_day: int = Field(..., ge=1, le=31, description="出生日期")
    birth_hour: int = Field(..., ge=0, le=23, description="出生时辰 (0-23)")
    gender: Literal["male", "female"] = Field(..., description="性别")
    nums: list[int] = Field(..., min_length=3, max_length=3, description="三个数字 (1-64)")
    question: str = Field(..., min_length=1, max_length=500, description="问题")


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    ollama: bool
    timestamp: str


class SimpleResponse(BaseModel):
    """简单版响应"""
    hexagram: dict
    context: dict
    ai_analysis: str
    success: bool
    error: Optional[str] = None


class DetailedResponse(BaseModel):
    """详细版响应"""
    bazi: dict
    hexagram: dict
    fengshui: dict
    context: dict
    ai_report: str
    success: bool
    error: Optional[str] = None


# ==================== API 路由 ====================

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """
    健康检查

    检查后端服务和 Ollama 是否正常运行
    """
    ollama_ok = await ai.check_health()

    return HealthResponse(
        status="ok",
        ollama=ollama_ok,
        timestamp=datetime.now().isoformat(),
    )


@app.post("/api/predict/simple", response_model=SimpleResponse)
async def predict_simple(request: SimpleRequest):
    """
    简单版预测

    使用梅花易数快速起卦，适合日常决策
    """
    try:
        # 1. 起卦
        result = meihua.calculate(
            request.nums[0],
            request.nums[1],
            request.nums[2],
        )
        hexagram_dict = meihua.to_dict(result)

        # 2. 搜索外应
        context_result = crawler.search(request.question)
        context_dict = crawler.to_dict(context_result)

        # 3. AI 分析
        ai_response = await ai.analyze_simple(
            hexagram=hexagram_dict,
            context=context_result.summary,
            question=request.question,
        )

        if not ai_response.success:
            return SimpleResponse(
                hexagram=hexagram_dict,
                context=context_dict,
                ai_analysis=f"AI 分析暂时不可用: {ai_response.error}",
                success=False,
                error=ai_response.error,
            )

        return SimpleResponse(
            hexagram=hexagram_dict,
            context=context_dict,
            ai_analysis=ai_response.content,
            success=True,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/predict/detailed", response_model=DetailedResponse)
async def predict_detailed(request: DetailedRequest):
    """
    详细版预测

    综合八字、梅花易数、九宫飞星，生成完整战略报告
    """
    try:
        # 1. 八字排盘
        bazi_result = bazi.calculate(
            year=request.birth_year,
            month=request.birth_month,
            day=request.birth_day,
            hour=request.birth_hour,
        )
        bazi_dict = bazi.to_dict(bazi_result)

        # 2. 梅花起卦
        meihua_result = meihua.calculate(
            request.nums[0],
            request.nums[1],
            request.nums[2],
        )
        hexagram_dict = meihua.to_dict(meihua_result)

        # 3. 风水分析
        fengshui_result = fengshui.calculate(
            birth_year=request.birth_year,
            gender=request.gender,
        )
        fengshui_dict = fengshui.to_dict(fengshui_result)

        # 4. 搜索外应
        context_result = crawler.search(request.question)
        context_dict = crawler.to_dict(context_result)

        # 5. AI 综合分析
        ai_response = await ai.analyze_detailed(
            bazi=bazi_dict,
            hexagram=hexagram_dict,
            fengshui=fengshui_dict,
            context=context_result.summary,
            question=request.question,
        )

        if not ai_response.success:
            return DetailedResponse(
                bazi=bazi_dict,
                hexagram=hexagram_dict,
                fengshui=fengshui_dict,
                context=context_dict,
                ai_report=f"AI 分析暂时不可用: {ai_response.error}",
                success=False,
                error=ai_response.error,
            )

        return DetailedResponse(
            bazi=bazi_dict,
            hexagram=hexagram_dict,
            fengshui=fengshui_dict,
            context=context_dict,
            ai_report=ai_response.content,
            success=True,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 启动入口 ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
