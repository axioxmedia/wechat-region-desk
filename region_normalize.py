# -*- coding: utf-8 -*-
"""Turn a WeChat 地区 string into one tag: the first geographic unit."""

from __future__ import annotations

import re
from typing import Iterable

NOISE = [
    "朋友资料",
    "添加备注名",
    "更多信息",
    "共同群聊",
    "个性签名",
    "朋友圈",
    "添加时间",
    "发消息",
    "语音聊天",
    "视频聊天",
    "朋友权限",
    "标签",
    "备注",
    "来源",
    "微信号",
]

FIRST_UNITS = [
    "中国香港",
    "中国澳门",
    "中国台湾",
    "中国大陆",
    "马来西亚",
    "新加坡",
    "印度尼西亚",
    "菲律宾",
    "澳大利亚",
    "新西兰",
    "美利坚",
    "内蒙古",
    "黑龙江",
    "香港",
    "澳门",
    "台湾",
    "日本",
    "韩国",
    "美国",
    "英国",
    "加拿大",
    "泰国",
    "越南",
    "德国",
    "法国",
    "意大利",
    "西班牙",
    "俄罗斯",
    "印度",
    "阿联酋",
    "广东",
    "广西",
    "北京",
    "上海",
    "天津",
    "重庆",
    "浙江",
    "江苏",
    "四川",
    "福建",
    "山东",
    "山西",
    "湖北",
    "湖南",
    "河南",
    "河北",
    "安徽",
    "江西",
    "辽宁",
    "吉林",
    "陕西",
    "甘肃",
    "青海",
    "云南",
    "贵州",
    "海南",
    "宁夏",
    "西藏",
    "新疆",
]

TWO_WORD_FIRST = {
    "hong kong": "中国香港",
    "hongkong": "中国香港",
    "macau": "中国澳门",
    "macao": "中国澳门",
    "new zealand": "新西兰",
    "united states": "美国",
    "united kingdom": "英国",
    "saudi arabia": "沙特",
    "south korea": "韩国",
    "north korea": "朝鲜",
}


def clean_region_text(raw: str | None) -> str:
    text = re.sub(r"\s+", "", raw or "")
    for n in NOISE:
        text = text.replace(n, "")
    text = re.sub(r"Wfäe.*$", "", text, flags=re.I)
    return text.strip(" ：:·-|")


def is_hongkong(raw: str | None, extra_keys: Iterable[str] | None = None) -> bool:
    text = clean_region_text(raw).lower()
    if not text:
        return False
    keys = ["中国香港", "香港", "hong kong", "hongkong", "hk"]
    if extra_keys:
        keys.extend(str(k).lower() for k in extra_keys)
    return any(k.lower() in text for k in keys)


def first_region_unit(raw: str | None, empty_tag: str = "未填写地区") -> str:
    """广东深圳 → 广东；马来西亚吉隆坡 → 马来西亚；中国香港中西区 → 中国香港."""
    text = clean_region_text(raw)
    if not text or text in {"-", "无", "未知", "未设置"}:
        return empty_tag
    lowered = text.lower()
    for phrase, tag in TWO_WORD_FIRST.items():
        if lowered.startswith(phrase):
            return tag
    for unit in FIRST_UNITS:
        if text.startswith(unit) or text.find(unit) == 0:
            return unit
    m = re.match(r"([\u4e00-\u9fff]{2,4})", text)
    if m:
        return m.group(1)
    token = re.split(r"[\s,，/|]+", text, maxsplit=1)[0].strip()
    if len(token) == 1:
        return empty_tag
    return token or empty_tag


def normalize_region(raw: str | None, empty_tag: str = "未填写地区", max_len: int = 16) -> str:
    tag = first_region_unit(raw, empty_tag=empty_tag)
    limit = max(4, int(max_len or 16))
    if len(tag) > limit:
        return tag[:limit]
    return tag
