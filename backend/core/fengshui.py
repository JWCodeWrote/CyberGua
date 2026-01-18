"""
九宫飞星与本命卦计算 (Feng Shui)

功能:
- 计算本命卦 (根据出生年份和性别)
- 计算流年飞星 (当年吉凶方位)
- 提供风水布局建议
"""

from dataclasses import dataclass
from typing import Literal
from datetime import datetime


# 九星信息
NINE_STARS = {
    1: {"name": "一白贪狼星", "element": "水", "nature": "吉", "effect": "桃花、人缘"},
    2: {"name": "二黑巨门星", "element": "土", "nature": "凶", "effect": "病符、疾病"},
    3: {"name": "三碧禄存星", "element": "木", "nature": "凶", "effect": "是非、官非"},
    4: {"name": "四绿文曲星", "element": "木", "nature": "吉", "effect": "文昌、学业"},
    5: {"name": "五黄廉贞星", "element": "土", "nature": "大凶", "effect": "灾祸、破财"},
    6: {"name": "六白武曲星", "element": "金", "nature": "吉", "effect": "偏财、贵人"},
    7: {"name": "七赤破军星", "element": "金", "nature": "凶", "effect": "破败、口舌"},
    8: {"name": "八白左辅星", "element": "土", "nature": "大吉", "effect": "财运、置业"},
    9: {"name": "九紫右弼星", "element": "火", "nature": "大吉", "effect": "喜庆、桃花"},
}

# 后天八卦方位
DIRECTIONS = {
    1: "北", 2: "西南", 3: "东", 4: "东南",
    5: "中宫", 6: "西北", 7: "西", 8: "东北", 9: "南",
}

# 本命卦对应
MING_GUA_MAP = {
    1: {"name": "坎卦", "direction": "北", "element": "水"},
    2: {"name": "坤卦", "direction": "西南", "element": "土"},
    3: {"name": "震卦", "direction": "东", "element": "木"},
    4: {"name": "巽卦", "direction": "东南", "element": "木"},
    # 5 特殊: 男归坤(2)，女归艮(8)
    6: {"name": "乾卦", "direction": "西北", "element": "金"},
    7: {"name": "兑卦", "direction": "西", "element": "金"},
    8: {"name": "艮卦", "direction": "东北", "element": "土"},
    9: {"name": "离卦", "direction": "南", "element": "火"},
}

# 东四命/西四命
EAST_LIFE = [1, 3, 4, 9]
WEST_LIFE = [2, 6, 7, 8]


@dataclass
class MingGuaResult:
    """本命卦结果"""
    gua_number: int
    gua_name: str
    element: str
    best_direction: str
    life_group: str  # 东四命/西四命
    favorable_directions: list[str]
    unfavorable_directions: list[str]


@dataclass
class FlyingStarResult:
    """流年飞星结果"""
    year: int
    center_star: int
    positions: dict[str, dict]  # 方位 -> 星信息
    auspicious: list[str]  # 吉方
    inauspicious: list[str]  # 凶方
    wealth_position: str  # 财位
    romance_position: str  # 桃花位


@dataclass
class FengshuiResult:
    """完整风水分析结果"""
    ming_gua: MingGuaResult
    flying_stars: FlyingStarResult
    recommendations: list[str]


class FengshuiCalculator:
    """风水计算器"""

    def __init__(self):
        pass

    def _reduce_to_single(self, num: int) -> int:
        """将数字迭代相加至个位数"""
        while num > 9:
            num = sum(int(d) for d in str(num))
        return num

    def calculate_ming_gua(
        self, birth_year: int, gender: Literal["male", "female"]
    ) -> MingGuaResult:
        """
        计算本命卦

        规则:
        - 男: 11 - (年份后两位数字之和迭代至个位)
        - 女: (年份后两位数字之和迭代至个位) + 4

        注意: 2000年后规则有调整，此处使用传统算法
        """
        # 取年份后两位
        last_two = birth_year % 100

        # 迭代相加至个位
        year_sum = self._reduce_to_single(last_two)

        if gender == "male":
            # 男命公式 (1900-1999 年)
            if birth_year < 2000:
                gua_num = 11 - year_sum
            else:
                # 2000年后
                gua_num = 10 - year_sum
            if gua_num > 9:
                gua_num = self._reduce_to_single(gua_num)
        else:
            # 女命公式
            if birth_year < 2000:
                gua_num = year_sum + 4
            else:
                gua_num = year_sum + 6
            if gua_num > 9:
                gua_num = self._reduce_to_single(gua_num)

        # 处理 5 的特殊情况
        if gua_num == 5:
            gua_num = 2 if gender == "male" else 8

        # 获取卦信息
        gua_info = MING_GUA_MAP[gua_num]

        # 判断东四命/西四命
        if gua_num in EAST_LIFE:
            life_group = "东四命"
            favorable_dirs = ["北", "南", "东", "东南"]
            unfavorable_dirs = ["西", "西北", "西南", "东北"]
        else:
            life_group = "西四命"
            favorable_dirs = ["西", "西北", "西南", "东北"]
            unfavorable_dirs = ["北", "南", "东", "东南"]

        return MingGuaResult(
            gua_number=gua_num,
            gua_name=gua_info["name"],
            element=gua_info["element"],
            best_direction=gua_info["direction"],
            life_group=life_group,
            favorable_directions=favorable_dirs,
            unfavorable_directions=unfavorable_dirs,
        )

    def calculate_flying_stars(self, year: int) -> FlyingStarResult:
        """
        计算流年飞星

        规则: 使用三元九运，计算某年的九宫飞星分布
        """
        # 计算中宫星 (简化公式)
        # 标准公式较复杂，此处使用近似算法
        base_year = 2024  # 已知2024年五黄入中
        base_center = 5

        diff = year - base_year
        center_star = ((base_center - diff - 1) % 9) + 1

        # 按洛书顺序飞星
        # 洛书顺序: 中->西北->西->东北->南->北->西南->东->东南
        luo_shu_order = [5, 6, 7, 8, 9, 1, 2, 3, 4]
        direction_order = ["中宫", "西北", "西", "东北", "南", "北", "西南", "东", "东南"]

        positions = {}
        for i, direction in enumerate(direction_order):
            # 计算该方位的星
            star_num = ((center_star + luo_shu_order[i] - 5 - 1) % 9) + 1
            star_info = NINE_STARS[star_num]
            positions[direction] = {
                "star_number": star_num,
                "star_name": star_info["name"],
                "element": star_info["element"],
                "nature": star_info["nature"],
                "effect": star_info["effect"],
            }

        # 找出吉凶方位
        auspicious = []
        inauspicious = []
        wealth_pos = ""
        romance_pos = ""

        for direction, info in positions.items():
            if direction == "中宫":
                continue
            if info["nature"] in ["吉", "大吉"]:
                auspicious.append(f"{direction}({info['star_name'][:2]})")
                if info["star_number"] == 8:  # 八白财星
                    wealth_pos = direction
                if info["star_number"] in [1, 9]:  # 桃花星
                    romance_pos = direction
            else:
                inauspicious.append(f"{direction}({info['star_name'][:2]})")

        if not wealth_pos:
            wealth_pos = auspicious[0].split("(")[0] if auspicious else "东北"
        if not romance_pos:
            romance_pos = "南" if "南" not in [d.split("(")[0] for d in inauspicious] else "北"

        return FlyingStarResult(
            year=year,
            center_star=center_star,
            positions=positions,
            auspicious=auspicious,
            inauspicious=inauspicious,
            wealth_position=wealth_pos,
            romance_position=romance_pos,
        )

    def generate_recommendations(
        self, ming_gua: MingGuaResult, flying_stars: FlyingStarResult
    ) -> list[str]:
        """生成风水布局建议"""
        recs = []

        # 基于本命卦
        recs.append(
            f"命主属「{ming_gua.life_group}」，本命卦为「{ming_gua.gua_name}」。"
        )
        recs.append(
            f"个人吉方为：{'、'.join(ming_gua.favorable_directions)}；"
            f"不利方位：{'、'.join(ming_gua.unfavorable_directions)}。"
        )

        # 基于流年飞星
        recs.append(
            f"{flying_stars.year}年流年财位在「{flying_stars.wealth_position}」，"
            f"可摆放绿植或流水摆件催财。"
        )
        recs.append(
            f"桃花位在「{flying_stars.romance_position}」，单身者可在此方位放置鲜花。"
        )

        if flying_stars.inauspicious:
            recs.append(
                f"流年凶方：{'、'.join(flying_stars.inauspicious[:3])}，"
                f"宜悬挂铜铃或放置金属物品化解。"
            )

        return recs

    def calculate(
        self,
        birth_year: int,
        gender: Literal["male", "female"],
        current_year: int = None,
    ) -> FengshuiResult:
        """
        完整风水分析

        Args:
            birth_year: 出生年份
            gender: 性别 ("male" 或 "female")
            current_year: 流年年份 (默认当前年)

        Returns:
            FengshuiResult: 完整风水分析结果
        """
        if current_year is None:
            current_year = datetime.now().year

        ming_gua = self.calculate_ming_gua(birth_year, gender)
        flying_stars = self.calculate_flying_stars(current_year)
        recommendations = self.generate_recommendations(ming_gua, flying_stars)

        return FengshuiResult(
            ming_gua=ming_gua,
            flying_stars=flying_stars,
            recommendations=recommendations,
        )

    def to_dict(self, result: FengshuiResult) -> dict:
        """将结果转换为字典格式"""
        return {
            "ming_gua": {
                "gua_number": result.ming_gua.gua_number,
                "gua_name": result.ming_gua.gua_name,
                "element": result.ming_gua.element,
                "life_group": result.ming_gua.life_group,
                "best_direction": result.ming_gua.best_direction,
                "favorable_directions": result.ming_gua.favorable_directions,
                "unfavorable_directions": result.ming_gua.unfavorable_directions,
            },
            "flying_stars": {
                "year": result.flying_stars.year,
                "center_star": result.flying_stars.center_star,
                "wealth_position": result.flying_stars.wealth_position,
                "romance_position": result.flying_stars.romance_position,
                "auspicious": result.flying_stars.auspicious,
                "inauspicious": result.flying_stars.inauspicious,
            },
            "recommendations": result.recommendations,
        }
