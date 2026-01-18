"""
外应搜索模块 (Context Crawler)

使用 DuckDuckGo 搜索引擎获取实时信息作为"外应"
- 提取问题关键词
- 搜索相关新闻/信息
- 返回摘要作为外应参考
"""

import re
from dataclasses import dataclass
from typing import Optional

try:
    from duckduckgo_search import DDGS
except ImportError:
    DDGS = None


@dataclass
class SearchResult:
    """单条搜索结果"""
    title: str
    snippet: str
    url: str


@dataclass
class ContextResult:
    """外应搜索完整结果"""
    query: str
    results: list[SearchResult]
    summary: str
    success: bool
    error: Optional[str] = None


class ContextCrawler:
    """外应爬虫"""

    def __init__(self, max_results: int = 3, timeout: int = 10):
        """
        初始化爬虫

        Args:
            max_results: 最大搜索结果数
            timeout: 请求超时时间 (秒)
        """
        self.max_results = max_results
        self.timeout = timeout

    def _extract_keywords(self, question: str) -> str:
        """
        从问题中提取关键词用于搜索

        策略:
        - 移除停用词
        - 添加运势相关词汇
        """
        # 停用词
        stop_words = [
            "吗", "呢", "啊", "呀", "吧", "了", "的", "是", "会",
            "能", "可以", "应该", "怎么", "什么", "如何", "为什么",
            "我", "你", "他", "她", "它", "我们", "他们",
            "请问", "想问", "问一下", "帮我", "帮忙",
        ]

        # 清理问题
        query = question
        for word in stop_words:
            query = query.replace(word, " ")

        # 移除多余空格
        query = re.sub(r"\s+", " ", query).strip()

        # 如果结果太短，使用原问题
        if len(query) < 4:
            query = question[:20]

        # 添加运势关键词 (可选)
        # query += " 运势 分析"

        return query

    def search(self, question: str) -> ContextResult:
        """
        执行搜索获取外应

        Args:
            question: 用户的问题

        Returns:
            ContextResult: 搜索结果与摘要
        """
        if DDGS is None:
            return ContextResult(
                query=question,
                results=[],
                summary="外应模块未启用 (duckduckgo_search 未安装)",
                success=False,
                error="duckduckgo_search library not installed",
            )

        # 提取搜索关键词
        query = self._extract_keywords(question)

        try:
            # 执行搜索
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    query,
                    max_results=self.max_results,
                    region="cn-zh",  # 中国区域，中文结果
                ))

            if not results:
                return ContextResult(
                    query=query,
                    results=[],
                    summary="未找到相关外应信息",
                    success=True,
                )

            # 解析结果
            search_results = []
            summaries = []

            for r in results:
                sr = SearchResult(
                    title=r.get("title", ""),
                    snippet=r.get("body", ""),
                    url=r.get("href", ""),
                )
                search_results.append(sr)
                if sr.snippet:
                    summaries.append(sr.snippet[:100])

            # 生成综合摘要
            summary = "；".join(summaries[:3]) if summaries else "无相关外应"

            return ContextResult(
                query=query,
                results=search_results,
                summary=summary,
                success=True,
            )

        except Exception as e:
            return ContextResult(
                query=query,
                results=[],
                summary=f"外应搜索失败: {str(e)}",
                success=False,
                error=str(e),
            )

    def to_dict(self, result: ContextResult) -> dict:
        """将结果转换为字典格式"""
        return {
            "query": result.query,
            "results": [
                {
                    "title": r.title,
                    "snippet": r.snippet,
                    "url": r.url,
                }
                for r in result.results
            ],
            "summary": result.summary,
            "success": result.success,
            "error": result.error,
        }
