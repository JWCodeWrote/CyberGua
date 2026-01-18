"""
八字排盘 (Bazi) - 四柱命理计算

使用 lunar_python 库进行:
- 阳历转农历
- 计算四柱 (年柱、月柱、日柱、时柱)
- 分析日主强弱
- 判断喜用神
"""

from dataclasses import dataclass
from typing import Literal, Optional

try:
    from lunar_python import Lunar, Solar
except ImportError:
    raise ImportError("请安装 lunar_python: pip install lunar_python")


# 天干
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 地支
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 天干五行
TIANGAN_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}

# 地支五行
DIZHI_WUXING = {
    "子": "水", "丑": "土",
    "寅": "木", "卯": "木",
    "辰": "土", "巳": "火",
    "午": "火", "未": "土",
    "申": "金", "酉": "金",
    "戌": "土", "亥": "水",
}

# 地支藏干 (主气、中气、余气)
DIZHI_CANGGAN = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"],
}

# 五行相生相克
WUXING_SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
WUXING_KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}


@dataclass
class Pillar:
    """一柱 (年/月/日/时)"""
    tiangan: str      # 天干
    dizhi: str        # 地支
    tiangan_wuxing: str  # 天干五行
    dizhi_wuxing: str    # 地支五行
    canggan: list[str]   # 地支藏干


@dataclass
class BaziResult:
    """八字完整结果"""
    year_pillar: Pillar    # 年柱
    month_pillar: Pillar   # 月柱
    day_pillar: Pillar     # 日柱
    hour_pillar: Pillar    # 时柱
    day_master: str        # 日主 (日干)
    day_master_wuxing: str # 日主五行
    strength: str          # 身强/身弱
    favorable_elements: list[str]  # 喜用神 (五行)
    unfavorable_elements: list[str]  # 忌神 (五行)
    analysis: str          # 分析文字


class BaziCalculator:
    """八字计算器"""

    def __init__(self):
        pass

    def _create_pillar(self, ganzhi: str) -> Pillar:
        """从干支字符串创建 Pillar 对象"""
        if len(ganzhi) != 2:
            raise ValueError(f"干支格式错误: {ganzhi}")

        tiangan = ganzhi[0]
        dizhi = ganzhi[1]

        return Pillar(
            tiangan=tiangan,
            dizhi=dizhi,
            tiangan_wuxing=TIANGAN_WUXING.get(tiangan, ""),
            dizhi_wuxing=DIZHI_WUXING.get(dizhi, ""),
            canggan=DIZHI_CANGGAN.get(dizhi, []),
        )

    def _count_wuxing(self, pillars: list[Pillar]) -> dict[str, int]:
        """统计四柱中各五行的数量"""
        count = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}

        for p in pillars:
            # 天干算1点
            if p.tiangan_wuxing:
                count[p.tiangan_wuxing] += 1
            # 地支主气算1点
            if p.canggan:
                main_canggan = p.canggan[0]
                cg_wuxing = TIANGAN_WUXING.get(main_canggan, "")
                if cg_wuxing:
                    count[cg_wuxing] += 1

        return count

    def _analyze_strength(
        self, day_master_wuxing: str, wuxing_count: dict[str, int]
    ) -> tuple[str, list[str], list[str]]:
        """
        分析日主强弱与喜用神

        规则 (简化版):
        - 同我者 (比劫) + 生我者 (印绶) 的五行数量多 = 身强
        - 身强喜: 克泄耗 (官杀、食伤、财星)
        - 身弱喜: 生扶 (印绶、比劫)
        """
        dm = day_master_wuxing

        # 找出同我、生我、克我、我克、我生
        sheng_wo = [k for k, v in WUXING_SHENG.items() if v == dm][0]  # 生我者
        wo_sheng = WUXING_SHENG[dm]  # 我生者
        ke_wo = [k for k, v in WUXING_KE.items() if v == dm][0]  # 克我者
        wo_ke = WUXING_KE[dm]  # 我克者

        # 计算身强身弱
        support_score = wuxing_count[dm] + wuxing_count[sheng_wo]  # 比劫 + 印绶
        drain_score = wuxing_count[wo_sheng] + wuxing_count[wo_ke] + wuxing_count[ke_wo]

        if support_score >= drain_score:
            strength = "身强"
            favorable = [ke_wo, wo_sheng, wo_ke]  # 官杀、食伤、财星
            unfavorable = [dm, sheng_wo]  # 比劫、印绶
        else:
            strength = "身弱"
            favorable = [sheng_wo, dm]  # 印绶、比劫
            unfavorable = [ke_wo, wo_sheng, wo_ke]  # 官杀、食伤、财星

        return strength, favorable, unfavorable

    def _generate_analysis(
        self,
        day_master: str,
        day_master_wuxing: str,
        strength: str,
        favorable: list[str],
        unfavorable: list[str],
    ) -> str:
        """生成分析文字"""
        lines = []
        lines.append(f"日主为「{day_master}」，五行属「{day_master_wuxing}」。")
        lines.append(f"综合分析八字格局，命主「{strength}」。")

        if strength == "身强":
            lines.append(f"身强者宜泄耗，喜用神为「{'、'.join(favorable)}」。")
            lines.append("适合财运、事业发展，能承担压力。")
        else:
            lines.append(f"身弱者宜生扶，喜用神为「{'、'.join(favorable)}」。")
            lines.append("宜稳健行事，借助贵人助力，不宜冒进。")

        return "\n".join(lines)

    def calculate(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
    ) -> BaziResult:
        """
        计算八字

        Args:
            year: 出生年 (阳历)
            month: 出生月 (阳历)
            day: 出生日 (阳历)
            hour: 出生时辰 (0-23 小时)

        Returns:
            BaziResult: 完整八字分析结果
        """
        # 使用 lunar_python 获取八字
        solar = Solar.fromYmdHms(year, month, day, hour, 0, 0)
        lunar = solar.getLunar()
        bazi = lunar.getEightChar()

        # 获取四柱
        year_gz = bazi.getYear()
        month_gz = bazi.getMonth()
        day_gz = bazi.getDay()
        hour_gz = bazi.getTime()

        # 创建 Pillar 对象
        year_pillar = self._create_pillar(year_gz)
        month_pillar = self._create_pillar(month_gz)
        day_pillar = self._create_pillar(day_gz)
        hour_pillar = self._create_pillar(hour_gz)

        pillars = [year_pillar, month_pillar, day_pillar, hour_pillar]

        # 日主
        day_master = day_pillar.tiangan
        day_master_wuxing = day_pillar.tiangan_wuxing

        # 统计五行
        wuxing_count = self._count_wuxing(pillars)

        # 分析强弱与喜用神
        strength, favorable, unfavorable = self._analyze_strength(
            day_master_wuxing, wuxing_count
        )

        # 生成分析
        analysis = self._generate_analysis(
            day_master, day_master_wuxing, strength, favorable, unfavorable
        )

        return BaziResult(
            year_pillar=year_pillar,
            month_pillar=month_pillar,
            day_pillar=day_pillar,
            hour_pillar=hour_pillar,
            day_master=day_master,
            day_master_wuxing=day_master_wuxing,
            strength=strength,
            favorable_elements=favorable,
            unfavorable_elements=unfavorable,
            analysis=analysis,
        )

    def to_dict(self, result: BaziResult) -> dict:
        """将结果转换为字典格式"""
        return {
            "four_pillars": {
                "year": f"{result.year_pillar.tiangan}{result.year_pillar.dizhi}",
                "month": f"{result.month_pillar.tiangan}{result.month_pillar.dizhi}",
                "day": f"{result.day_pillar.tiangan}{result.day_pillar.dizhi}",
                "hour": f"{result.hour_pillar.tiangan}{result.hour_pillar.dizhi}",
            },
            "day_master": result.day_master,
            "day_master_wuxing": result.day_master_wuxing,
            "strength": result.strength,
            "favorable_elements": result.favorable_elements,
            "unfavorable_elements": result.unfavorable_elements,
            "analysis": result.analysis,
        }
