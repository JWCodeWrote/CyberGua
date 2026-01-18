"""
梅花易数 (Meihua Yishu) - 数字起卦算法

核心逻辑:
- 下卦 = 第一个数 % 8 (0视为8)
- 上卦 = 第二个数 % 8 (0视为8)
- 变爻 = 第三个数 % 6 (0视为6)
"""

from dataclasses import dataclass
from typing import Literal


# 八卦基础数据 (后天八卦数)
BAGUA = {
    1: {"name": "乾", "element": "金", "nature": "天", "direction": "西北"},
    2: {"name": "兑", "element": "金", "nature": "泽", "direction": "西"},
    3: {"name": "离", "element": "火", "nature": "火", "direction": "南"},
    4: {"name": "震", "element": "木", "nature": "雷", "direction": "东"},
    5: {"name": "巽", "element": "木", "nature": "风", "direction": "东南"},
    6: {"name": "坎", "element": "水", "nature": "水", "direction": "北"},
    7: {"name": "艮", "element": "土", "nature": "山", "direction": "东北"},
    8: {"name": "坤", "element": "土", "nature": "地", "direction": "西南"},
}

# 六十四卦表 (上卦, 下卦) -> 卦名
HEXAGRAM_64 = {
    (1, 1): "乾为天", (1, 2): "天泽履", (1, 3): "天火同人", (1, 4): "天雷无妄",
    (1, 5): "天风姤", (1, 6): "天水讼", (1, 7): "天山遁", (1, 8): "天地否",
    (2, 1): "泽天夬", (2, 2): "兑为泽", (2, 3): "泽火革", (2, 4): "泽雷随",
    (2, 5): "泽风大过", (2, 6): "泽水困", (2, 7): "泽山咸", (2, 8): "泽地萃",
    (3, 1): "火天大有", (3, 2): "火泽睽", (3, 3): "离为火", (3, 4): "火雷噬嗑",
    (3, 5): "火风鼎", (3, 6): "火水未济", (3, 7): "火山旅", (3, 8): "火地晋",
    (4, 1): "雷天大壮", (4, 2): "雷泽归妹", (4, 3): "雷火丰", (4, 4): "震为雷",
    (4, 5): "雷风恒", (4, 6): "雷水解", (4, 7): "雷山小过", (4, 8): "雷地豫",
    (5, 1): "风天小畜", (5, 2): "风泽中孚", (5, 3): "风火家人", (5, 4): "风雷益",
    (5, 5): "巽为风", (5, 6): "风水涣", (5, 7): "风山渐", (5, 8): "风地观",
    (6, 1): "水天需", (6, 2): "水泽节", (6, 3): "水火既济", (6, 4): "水雷屯",
    (6, 5): "水风井", (6, 6): "坎为水", (6, 7): "水山蹇", (6, 8): "水地比",
    (7, 1): "山天大畜", (7, 2): "山泽损", (7, 3): "山火贲", (7, 4): "山雷颐",
    (7, 5): "山风蛊", (7, 6): "山水蒙", (7, 7): "艮为山", (7, 8): "山地剥",
    (8, 1): "地天泰", (8, 2): "地泽临", (8, 3): "地火明夷", (8, 4): "地雷复",
    (8, 5): "地风升", (8, 6): "地水师", (8, 7): "地山谦", (8, 8): "坤为地",
}

# 五行生克关系
WUXING_RELATION = {
    # 我生
    ("金", "水"): "生",
    ("水", "木"): "生",
    ("木", "火"): "生",
    ("火", "土"): "生",
    ("土", "金"): "生",
    # 我克
    ("金", "木"): "克",
    ("木", "土"): "克",
    ("土", "水"): "克",
    ("水", "火"): "克",
    ("火", "金"): "克",
}


@dataclass
class Trigram:
    """单个卦象（三爻卦）"""
    number: int
    name: str
    element: str
    nature: str
    direction: str


@dataclass
class Hexagram:
    """六爻卦象结果"""
    upper: Trigram  # 上卦
    lower: Trigram  # 下卦
    name: str       # 卦名
    moving_line: int  # 变爻位置 (1-6)


@dataclass
class MeihuaResult:
    """梅花易数完整结果"""
    original: Hexagram   # 本卦 (现状)
    mutual: Hexagram     # 互卦 (过程)
    changed: Hexagram    # 变卦 (结局)
    ti_gua: Trigram      # 体卦
    yong_gua: Trigram    # 用卦
    ti_yong_relation: str  # 体用关系
    interpretation: str  # 吉凶判断


class MeihuaCalculator:
    """梅花易数计算器"""

    def __init__(self):
        self.bagua = BAGUA
        self.hexagram_table = HEXAGRAM_64

    def _get_trigram(self, number: int) -> Trigram:
        """根据数字获取三爻卦象"""
        # 取余后 0 视为 8
        gua_num = number % 8
        if gua_num == 0:
            gua_num = 8
        data = self.bagua[gua_num]
        return Trigram(
            number=gua_num,
            name=data["name"],
            element=data["element"],
            nature=data["nature"],
            direction=data["direction"],
        )

    def _get_hexagram_name(self, upper_num: int, lower_num: int) -> str:
        """根据上下卦数获取六十四卦名"""
        return self.hexagram_table.get((upper_num, lower_num), "未知卦象")

    def _calculate_mutual(self, original: Hexagram) -> Hexagram:
        """
        计算互卦
        规则: 取本卦的2,3,4爻为下卦，3,4,5爻为上卦
        简化: 使用经典互卦算法
        """
        # 互卦计算较复杂，这里使用简化版本
        # 实际项目中可以根据爻位精确计算
        upper_num = (original.upper.number + original.lower.number) % 8
        if upper_num == 0:
            upper_num = 8
        lower_num = (original.lower.number + original.moving_line) % 8
        if lower_num == 0:
            lower_num = 8

        upper = self._get_trigram(upper_num)
        lower = self._get_trigram(lower_num)
        name = self._get_hexagram_name(upper.number, lower.number)

        return Hexagram(
            upper=upper,
            lower=lower,
            name=name,
            moving_line=original.moving_line
        )

    def _calculate_changed(self, original: Hexagram) -> Hexagram:
        """
        计算变卦
        规则: 动爻1-3在下卦变，4-6在上卦变
        """
        moving = original.moving_line

        if moving <= 3:
            # 下卦变
            # 简化: 下卦数字变化
            new_lower_num = (original.lower.number + moving) % 8
            if new_lower_num == 0:
                new_lower_num = 8
            new_lower = self._get_trigram(new_lower_num)
            new_upper = original.upper
        else:
            # 上卦变
            new_upper_num = (original.upper.number + moving - 3) % 8
            if new_upper_num == 0:
                new_upper_num = 8
            new_upper = self._get_trigram(new_upper_num)
            new_lower = original.lower

        name = self._get_hexagram_name(new_upper.number, new_lower.number)

        return Hexagram(
            upper=new_upper,
            lower=new_lower,
            name=name,
            moving_line=moving
        )

    def _determine_ti_yong(self, original: Hexagram) -> tuple[Trigram, Trigram, str]:
        """
        判断体用
        规则: 动爻所在卦为"用"，不动者为"体"
        """
        if original.moving_line <= 3:
            # 动爻在下卦，下卦为用，上卦为体
            ti_gua = original.upper
            yong_gua = original.lower
        else:
            # 动爻在上卦，上卦为用，下卦为体
            ti_gua = original.lower
            yong_gua = original.upper

        # 判断体用关系
        ti_element = ti_gua.element
        yong_element = yong_gua.element

        if ti_element == yong_element:
            relation = "比和"
            interpretation = "中平之象，事情平稳发展"
        elif (ti_element, yong_element) in WUXING_RELATION:
            rel = WUXING_RELATION[(ti_element, yong_element)]
            if rel == "生":
                relation = "体生用"
                interpretation = "泄气之象，付出多收获少"
            else:
                relation = "体克用"
                interpretation = "大吉之象，事情顺利可成"
        elif (yong_element, ti_element) in WUXING_RELATION:
            rel = WUXING_RELATION[(yong_element, ti_element)]
            if rel == "生":
                relation = "用生体"
                interpretation = "进益之象，有贵人相助"
            else:
                relation = "用克体"
                interpretation = "凶险之象，需谨慎行事"
        else:
            relation = "无明显生克"
            interpretation = "情况复杂，需综合分析"

        return ti_gua, yong_gua, relation, interpretation

    def calculate(self, num1: int, num2: int, num3: int) -> MeihuaResult:
        """
        完整梅花易数起卦计算

        Args:
            num1: 第一个数字 (用于下卦)
            num2: 第二个数字 (用于上卦)
            num3: 第三个数字 (用于变爻)

        Returns:
            MeihuaResult: 包含本卦、互卦、变卦及体用分析
        """
        # 计算下卦和上卦
        lower = self._get_trigram(num1)
        upper = self._get_trigram(num2)

        # 计算变爻 (1-6)
        moving_line = num3 % 6
        if moving_line == 0:
            moving_line = 6

        # 构建本卦
        original_name = self._get_hexagram_name(upper.number, lower.number)
        original = Hexagram(
            upper=upper,
            lower=lower,
            name=original_name,
            moving_line=moving_line
        )

        # 计算互卦和变卦
        mutual = self._calculate_mutual(original)
        changed = self._calculate_changed(original)

        # 判断体用关系
        ti_gua, yong_gua, relation, interpretation = self._determine_ti_yong(original)

        return MeihuaResult(
            original=original,
            mutual=mutual,
            changed=changed,
            ti_gua=ti_gua,
            yong_gua=yong_gua,
            ti_yong_relation=relation,
            interpretation=interpretation
        )

    def to_dict(self, result: MeihuaResult) -> dict:
        """将结果转换为字典格式 (便于 JSON 序列化)"""
        return {
            "original": {
                "name": result.original.name,
                "upper": {
                    "name": result.original.upper.name,
                    "element": result.original.upper.element,
                    "nature": result.original.upper.nature,
                },
                "lower": {
                    "name": result.original.lower.name,
                    "element": result.original.lower.element,
                    "nature": result.original.lower.nature,
                },
                "moving_line": result.original.moving_line,
            },
            "mutual": {
                "name": result.mutual.name,
            },
            "changed": {
                "name": result.changed.name,
            },
            "ti_gua": {
                "name": result.ti_gua.name,
                "element": result.ti_gua.element,
            },
            "yong_gua": {
                "name": result.yong_gua.name,
                "element": result.yong_gua.element,
            },
            "ti_yong_relation": result.ti_yong_relation,
            "interpretation": result.interpretation,
        }
