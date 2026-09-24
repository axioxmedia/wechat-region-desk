# -*- coding: utf-8 -*-
"""Find the Contact Manager panel in a desktop shot and snap click targets."""

from __future__ import annotations

from pathlib import Path


def _cv2():
    import cv2

    return cv2


def _np():
    import numpy as np

    return np


def image_to_screen(info: dict, ix: float, iy: float) -> tuple[int, int]:
    """Map a pixel in the DISPLAYED image (cropped panel) to the screen."""
    iw = max(1, int(info.get("image_width") or info.get("width") or 1))
    ih = max(1, int(info.get("image_height") or info.get("height") or 1))
    left = int(info["left"])
    top = int(info["top"])
    box_w = max(1, int(info["right"]) - left)
    box_h = max(1, int(info["bottom"]) - top)
    sx = left + ix * box_w / iw
    sy = top + iy * box_h / ih
    return int(round(sx)), int(round(sy))


def load_bgr(path: str | Path):
    cv2 = _cv2()
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError("无法读取截图")
    return img


def _center(x, y, w, h) -> tuple[int, int, int, int]:
    return int(x + w / 2), int(y + h / 2), int(w), int(h)


def find_manager_roi(img) -> tuple[int, int, int, int]:
    """Return (x, y, w, h) of the white 通讯录管理 card inside a desktop shot."""
    cv2 = _cv2()
    np = _np()
    h, w = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # WeChat green used by 「全部」.
    green = cv2.inRange(hsv, (35, 90, 70), (85, 255, 255))
    green = cv2.medianBlur(green, 5)
    g_contours, _ = cv2.findContours(green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    candidates: list[tuple[int, int, int, int, float]] = []
    for c in g_contours:
        gx, gy, gw, gh = cv2.boundingRect(c)
        # Taskbar WeChat icon is square; 「全部」is a wide green pill.
        if gh > 56 or gw < 72 or gw > 260 or gh < 20 or gh > gw * 0.65:
            continue
        if gy < 40 and gh < 50:
            continue
        x0 = max(0, gx - 24)
        y0 = max(0, gy - 56)
        x1 = min(w, gx + max(520, int(gw * 6)))
        y1 = min(h, gy + max(420, int(gh * 16)))
        roi = img[y0:y1, x0:x1]
        if roi.size == 0:
            continue
        if float(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY).mean()) < 140:
            continue
        score = _panel_score(roi)
        candidates.append((x0, y0, x1 - x0, y1 - y0, score + gw * 0.05))

    if not candidates:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        pale = cv2.inRange(gray, 230, 255)
        pale = cv2.morphologyEx(pale, cv2.MORPH_CLOSE, np.ones((17, 17), np.uint8))
        contours, _ = cv2.findContours(pale, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            x, y, ww, hh = cv2.boundingRect(c)
            if ww < 420 or hh < 360:
                continue
            score = _panel_score(img[y : y + hh, x : x + ww])
            candidates.append((x, y, ww, hh, score))

    if not candidates:
        return 0, 0, w, h
    candidates.sort(key=lambda t: t[4], reverse=True)
    x, y, ww, hh, _ = candidates[0]
    # Tighten by pale content.
    cut = _tight_white(img[y : y + hh, x : x + ww])
    if cut:
        x += cut[0]
        y += cut[1]
        ww, hh = cut[2], cut[3]
    pad = 8
    x = max(0, x - pad)
    y = max(0, y - pad)
    ww = min(w - x, ww + pad * 2)
    hh = min(h - y, hh + pad * 2)
    return int(x), int(y), int(ww), int(hh)


def _tight_white(roi) -> tuple[int, int, int, int] | None:
    cv2 = _cv2()
    np = _np()
    if roi.size == 0:
        return None
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    pale = cv2.inRange(gray, 220, 255)
    ys, xs = np.where(pale > 0)
    if len(xs) < 400:
        return None
    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())
    return x0, y0, max(20, x1 - x0 + 1), max(20, y1 - y0 + 1)


def _panel_score(roi) -> float:
    cv2 = _cv2()
    if roi is None or roi.size == 0:
        return -1
    h, w = roi.shape[:2]
    if h < 80 or w < 80:
        return -1
    found = _detect_in_bgr(roi)
    avatars = found["avatar"]
    checks = found["check"]
    score = len(avatars) * 4 + len(checks) * 2 + len(found["search"])
    if len(avatars) >= 3:
        xs = [p["x"] for p in avatars]
        span = max(xs) - min(xs) if xs else 99
        if span <= 24:
            score += 12
    # Penalize very dark ROIs (the desk app).
    mean = float(cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY).mean())
    if mean < 60:
        score -= 20
    return score


def _detect_in_bgr(img) -> dict:
    cv2 = _cv2()
    np = _np()
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    searches: list[dict] = []
    checks: list[dict] = []
    avatars: list[dict] = []

    top_band = gray[0 : max(48, h // 7), :]
    blur = cv2.GaussianBlur(top_band, (5, 5), 0)
    _, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        x, y, ww, hh = cv2.boundingRect(c)
        if ww >= 80 and 16 <= hh <= 44 and x > w * 0.16:
            cx, cy, ww, hh = _center(x, y, ww, hh)
            searches.append({"x": cx, "y": cy, "w": ww, "h": hh})
    searches.sort(key=lambda p: (p["y"], -p["w"]))
    searches = searches[:2]

    header = max(96, int(h * 0.13))
    # Checkbox rings: Hough circles in the list, below the 昵称 header.
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    circles = cv2.HoughCircles(
        blur,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=28,
        param1=90,
        param2=16,
        minRadius=7,
        maxRadius=16,
    )
    if circles is not None:
        for cx, cy, cr in np.round(circles[0]).astype(int):
            if cy <= header or cx < int(w * 0.18) or cx > int(w * 0.40):
                continue
            checks.append({"x": int(cx), "y": int(cy), "w": int(cr * 2), "h": int(cr * 2)})

    white = cv2.inRange(img, (226, 226, 226), (255, 255, 255))
    ink = cv2.bitwise_not(white)
    ink = cv2.medianBlur(ink, 3)
    contours, _ = cv2.findContours(ink, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        x, y, ww, hh = cv2.boundingRect(c)
        if ww < 8 or hh < 8 or y <= header:
            continue
        ratio = ww / float(hh)
        cx, cy, ww, hh = _center(x, y, ww, hh)
        item = {"x": cx, "y": cy, "w": ww, "h": hh}
        if 9 <= ww <= 26 and 9 <= hh <= 26 and 0.72 <= ratio <= 1.35:
            if not any(abs(p["x"] - cx) < 8 and abs(p["y"] - cy) < 8 for p in checks):
                checks.append(item)
        elif 28 <= ww <= 72 and 28 <= hh <= 72 and 0.78 <= ratio <= 1.28:
            patch = img[max(0, y) : y + hh, max(0, x) : x + ww]
            if patch.size and float(patch.std()) > 12:
                avatars.append(item)

    def column(items, tol):
        if len(items) < 2:
            return items
        xs = np.array([p["x"] for p in items])
        col = int(np.median(xs))
        kept = [p for p in items if abs(p["x"] - col) <= tol]
        kept.sort(key=lambda p: p["y"])
        return kept

    checks = column(checks, 14)
    avatars = column(avatars, 20)
    return {"search": searches, "check": checks, "avatar": avatars, "image_width": w, "image_height": h}


def detect_targets(path: str | Path) -> dict:
    img = load_bgr(path)
    return _detect_in_bgr(img)


def auto_marks(path: str | Path) -> dict:
    found = detect_targets(path)
    marks = {}
    if found["search"]:
        s = found["search"][0]
        marks["search"] = s
    if found["check"]:
        marks["check"] = found["check"][0]
    if found["avatar"]:
        marks["avatar"] = found["avatar"][0]
        if len(found["avatar"]) >= 2:
            marks["row2"] = found["avatar"][1]
    return {"marks": marks, "candidates": found}


def nearest(items: list[dict], ix: int, iy: int, max_dist: int = 48) -> dict | None:
    best = None
    best_d = max_dist
    for it in items:
        d = ((it["x"] - ix) ** 2 + (it["y"] - iy) ** 2) ** 0.5
        if d <= best_d:
            best = it
            best_d = d
    return best


def snap_point(path: str | Path, mode: str, ix: int, iy: int) -> dict:
    found = detect_targets(path)
    key = "avatar" if mode == "row2" else mode
    hit = nearest(found.get(key) or [], ix, iy, max_dist=70 if key == "search" else 42)
    if hit:
        return {
            "snapped": True,
            "img_x": hit["x"],
            "img_y": hit["y"],
            "w": hit["w"],
            "h": hit["h"],
            "mode": mode,
            "candidates": found,
        }
    return {
        "snapped": False,
        "img_x": int(ix),
        "img_y": int(iy),
        "w": 0,
        "h": 0,
        "mode": mode,
        "candidates": found,
    }


def crop_manager_panel(full_path: str | Path, crop_path: str | Path, virt: dict) -> dict:
    """Keep the full desktop shot. Detect the white manager card only for marks."""
    cv2 = _cv2()
    full = load_bgr(full_path)
    fh, fw = full.shape[:2]
    x, y, ww, hh = find_manager_roi(full)
    # Display the original full screenshot — do not crop it away.
    cv2.imwrite(str(crop_path), full)
    marks = {}
    candidates = {"search": [], "check": [], "avatar": []}
    if ww >= 300 and hh >= 240:
        local = _detect_in_bgr(full[y : y + hh, x : x + ww])
        for kind in ("search", "check", "avatar"):
            for it in local.get(kind) or []:
                candidates[kind].append({
                    "x": it["x"] + x,
                    "y": it["y"] + y,
                    "w": it["w"],
                    "h": it["h"],
                })
        if candidates["search"]:
            marks["search"] = candidates["search"][0]
        if candidates["check"]:
            marks["check"] = candidates["check"][0]
        if candidates["avatar"]:
            marks["avatar"] = candidates["avatar"][0]
            if len(candidates["avatar"]) >= 2:
                marks["row2"] = candidates["avatar"][1]
    return {
        "path": str(crop_path),
        "left": int(virt["left"]),
        "top": int(virt["top"]),
        "right": int(virt["right"]),
        "bottom": int(virt["bottom"]),
        "width": int(virt["right"]) - int(virt["left"]),
        "height": int(virt["bottom"]) - int(virt["top"]),
        "image_width": fw,
        "image_height": fh,
        "panel": {"x": x, "y": y, "w": ww, "h": hh},
        "mode": "virtual-screen",
        "auto_marks": marks,
        "candidates": candidates,
    }
