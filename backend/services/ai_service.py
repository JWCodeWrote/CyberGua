"""
AI 服务模块 (AI Service)

负责:
- 组合 Prompt
- 调用 Ollama API
- 生成简单版/详细版分析报告
- 自动检测可用模型
"""

import httpx
from dataclasses import dataclass
from typing import Optional, List
import json
import os


# Ollama 配置 (支持环境变量，方便 Docker 部署)
OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# 优先级排序的模型列表 (从最佳到最快)
PREFERRED_MODELS = [
    "qwen2.5:14b",   # 最佳质量
    "qwen2.5:7b",    # 平衡
    "qwen2.5:1.5b",  # 最快
    "qwen2.5:3b",    # 备选
    "qwen2.5:0.5b",  # 最小
]

DEFAULT_MODEL = "qwen2.5:1.5b"  # 默认回退模型


@dataclass
class AIResponse:
    """AI 回复结果"""
    content: str
    model: str
    success: bool
    error: Optional[str] = None


class AIService:
    """AI 调用服务"""

    def __init__(
        self,
        base_url: str = OLLAMA_BASE_URL,
        model: str = None,  # None 表示自动检测
        timeout: float = 120.0,
    ):
        """
        初始化 AI 服务

        Args:
            base_url: Ollama API 地址
            model: 使用的模型名称 (None 则自动检测)
            timeout: 请求超时时间 (秒)
        """
        self.base_url = base_url
        self._model = model
        self.timeout = timeout
        self._detected_model = None

    @property
    def model(self) -> str:
        """获取当前使用的模型名称"""
        if self._model:
            return self._model
        if self._detected_model:
            return self._detected_model
        return DEFAULT_MODEL

    async def detect_best_model(self) -> Optional[str]:
        """
        自动检测已安装的最佳 Qwen 模型
        
        Returns:
            最佳可用模型名称，如果没有则返回 None
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code != 200:
                    return None
                
                data = response.json()
                installed_models = [m.get("name", "") for m in data.get("models", [])]
                
                # 按优先级查找最佳模型
                for preferred in PREFERRED_MODELS:
                    if preferred in installed_models:
                        self._detected_model = preferred
                        print(f"[AI] 自动检测到模型: {preferred}")
                        return preferred
                
                # 如果没有找到优先模型，查找任何 qwen 模型
                for model in installed_models:
                    if "qwen" in model.lower():
                        self._detected_model = model
                        print(f"[AI] 使用已安装的模型: {model}")
                        return model
                
                return None
        except Exception as e:
            print(f"[AI] 模型检测失败: {e}")
            return None

    async def check_health(self) -> bool:
        """检查 Ollama 服务是否可用，并自动检测模型"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    # 顺便检测最佳模型
                    await self.detect_best_model()
                    return True
                return False
        except Exception:
            return False

    def _build_simple_prompt(
        self,
        hexagram: dict,
        context: str,
        question: str,
    ) -> str:
        """构建简单版 Prompt"""
        system = """你是一位精通梅花易数的命理大师。
用户通过报数起卦，你需要根据卦象分析吉凶。
请用通俗易懂的语言解读，给出具体的建议。
回答需要简洁有力，控制在 200 字以内。"""

        user = f"""用户问题：{question}

起卦结果：
- 本卦：{hexagram.get('original', {}).get('name', '未知')}
  （上卦{hexagram.get('original', {}).get('upper', {}).get('name', '')}，
    下卦{hexagram.get('original', {}).get('lower', {}).get('name', '')}）
- 变卦：{hexagram.get('changed', {}).get('name', '未知')}
- 体卦：{hexagram.get('ti_gua', {}).get('name', '')}（{hexagram.get('ti_gua', {}).get('element', '')}）
- 用卦：{hexagram.get('yong_gua', {}).get('name', '')}（{hexagram.get('yong_gua', {}).get('element', '')}）
- 体用关系：{hexagram.get('ti_yong_relation', '')}
- 初步判断：{hexagram.get('interpretation', '')}

外应参考（网络信息）：
{context}

请根据以上信息，给出你的分析和建议。"""

        return f"<|im_start|>system\n{system}<|im_end|>\n<|im_start|>user\n{user}<|im_end|>\n<|im_start|>assistant\n"

    def _build_detailed_prompt(
        self,
        bazi: dict,
        hexagram: dict,
        fengshui: dict,
        context: str,
        question: str,
    ) -> str:
        """构建详细版 Prompt (命、运、局三段式)"""
        system = """你是一位精通八字命理、梅花易数和风水学的资深命理师。
你需要综合分析用户的命盘、卦象和风水格局，给出全面的战略建议。

请严格按照以下三个部分输出分析报告：

## 一、命 (能否做？)
分析八字格局，判断命主是否有能力承载此事。

## 二、运 (何时做？)
分析卦象吉凶，判断事情的时机和趋势。

## 三、局 (在哪做？)
分析风水方位，给出具体的布局建议。

## 总结
综合以上分析，给出最终建议。

回答需要专业且有条理，总字数控制在 600 字以内。"""

        # 格式化八字
        four_pillars = bazi.get("four_pillars", {})
        bazi_str = (
            f"年柱：{four_pillars.get('year', '')}\n"
            f"月柱：{four_pillars.get('month', '')}\n"
            f"日柱：{four_pillars.get('day', '')}\n"
            f"时柱：{four_pillars.get('hour', '')}\n"
            f"日主：{bazi.get('day_master', '')}（{bazi.get('day_master_wuxing', '')}）\n"
            f"身强弱：{bazi.get('strength', '')}\n"
            f"喜用神：{'、'.join(bazi.get('favorable_elements', []))}"
        )

        # 格式化卦象
        hexagram_str = (
            f"本卦：{hexagram.get('original', {}).get('name', '')}\n"
            f"变卦：{hexagram.get('changed', {}).get('name', '')}\n"
            f"体用关系：{hexagram.get('ti_yong_relation', '')}\n"
            f"初步判断：{hexagram.get('interpretation', '')}"
        )

        # 格式化风水
        ming_gua = fengshui.get("ming_gua", {})
        flying = fengshui.get("flying_stars", {})
        fengshui_str = (
            f"本命卦：{ming_gua.get('gua_name', '')}（{ming_gua.get('life_group', '')}）\n"
            f"个人吉方：{'、'.join(ming_gua.get('favorable_directions', []))}\n"
            f"流年财位：{flying.get('wealth_position', '')}\n"
            f"流年桃花位：{flying.get('romance_position', '')}\n"
            f"流年吉方：{'、'.join(flying.get('auspicious', []))}"
        )

        user = f"""用户问题：{question}

【八字信息】
{bazi_str}

【梅花卦象】
{hexagram_str}

【风水格局】
{fengshui_str}

【外应参考】
{context}

请按照「命、运、局」三段式格式，给出完整分析报告。"""

        return f"<|im_start|>system\n{system}<|im_end|>\n<|im_start|>user\n{user}<|im_end|>\n<|im_start|>assistant\n"

    async def generate(self, prompt: str, stream: bool = False) -> AIResponse:
        """
        调用 Ollama 生成回复

        Args:
            prompt: 完整的提示词
            stream: 是否使用流式输出

        Returns:
            AIResponse: AI 回复结果
        """
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9,
                            "num_predict": 1024,
                        },
                    },
                )

                if response.status_code != 200:
                    return AIResponse(
                        content="",
                        model=self.model,
                        success=False,
                        error=f"Ollama API 返回错误: {response.status_code}",
                    )

                data = response.json()
                return AIResponse(
                    content=data.get("response", ""),
                    model=self.model,
                    success=True,
                )

        except httpx.TimeoutException:
            return AIResponse(
                content="",
                model=self.model,
                success=False,
                error="请求超时，请稍后重试",
            )
        except Exception as e:
            return AIResponse(
                content="",
                model=self.model,
                success=False,
                error=str(e),
            )

    async def analyze_simple(
        self,
        hexagram: dict,
        context: str,
        question: str,
    ) -> AIResponse:
        """
        简单版分析

        Args:
            hexagram: 梅花卦象结果 (字典格式)
            context: 外应搜索摘要
            question: 用户问题

        Returns:
            AIResponse: AI 分析结果
        """
        prompt = self._build_simple_prompt(hexagram, context, question)
        return await self.generate(prompt)

    async def analyze_detailed(
        self,
        bazi: dict,
        hexagram: dict,
        fengshui: dict,
        context: str,
        question: str,
    ) -> AIResponse:
        """
        详细版分析 (命、运、局)

        Args:
            bazi: 八字结果 (字典格式)
            hexagram: 梅花卦象结果 (字典格式)
            fengshui: 风水结果 (字典格式)
            context: 外应搜索摘要
            question: 用户问题

        Returns:
            AIResponse: AI 分析报告
        """
        prompt = self._build_detailed_prompt(bazi, hexagram, fengshui, context, question)
        return await self.generate(prompt)
