# -*- coding: utf-8 -*-
"""Layout locked to the user-supplied 通讯录管理 screenshot (1307 x 849)."""

REF_W = 1307
REF_H = 849

# Pixel centers measured on that screenshot.
REF = {
    "search": (448, 42),
    "check": (366, 151),
    "avatar": (446, 152),
    "row2": (446, 222),
    "row_h": 70,
}


def marks_for_image(image_width: int, image_height: int) -> dict:
    sx = image_width / float(REF_W)
    sy = image_height / float(REF_H)
    out = {}
    for key, val in REF.items():
        if key == "row_h":
            out["row_h"] = max(36, int(round(val * sy)))
            continue
        x, y = val
        out[key] = {
            "x": int(round(x * sx)),
            "y": int(round(y * sy)),
            "w": 28 if key != "search" else 160,
            "h": 28 if key != "search" else 28,
        }
    return out
