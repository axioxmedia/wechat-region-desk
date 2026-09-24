# -*- coding: utf-8 -*-
"""WeChat 4.1 contact-manager helpers.

4.x paints the list inside MMUIRenderSubWindowHW, so UIA has almost no
children. Scanning clicks fixed offsets inside that surface, then reads
the floating profile card (UIA names if present, otherwise clipboard /
nearby window text).
"""

from __future__ import annotations

import re
import sys
import time
from collections import Counter, defaultdict
from typing import Callable

from region_normalize import clean_region_text, is_hongkong, normalize_region

LogFn = Callable[[str], None]


def is_windows() -> bool:
    return sys.platform == "win32"


def _auto():
    if not is_windows():
        raise RuntimeError("WeChat UI automation requires Windows.")
    try:
        import uiautomation as auto
    except ImportError as exc:
        raise RuntimeError("uiautomation is not installed.") from exc
    return auto


def find_manager_window(name: str = "通讯录管理"):
    auto = _auto()
    exact = []
    loose = []
    root = auto.GetRootControl()
    for win in root.GetChildren():
        title = win.Name or ""
        cls = win.ClassName or ""
        if title == name or (name in title and "打标" not in title and "Region" not in title):
            exact.append(win)
        elif name in title:
            loose.append(win)
        elif cls.startswith("Qt") and "微信" in title:
            loose.append(win)
    if exact:
        return exact[0]
    if loose:
        return loose[0]
    win = auto.WindowControl(searchDepth=1, SubName=name)
    if win.Exists(0, 0):
        return win
    return None


def window_status(name: str = "通讯录管理") -> dict:
    if not is_windows():
        return {
            "ok": False,
            "platform": sys.platform,
            "found": False,
            "title": "",
            "class_name": "",
            "message": "not-windows",
        }
    try:
        win = find_manager_window(name)
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "platform": sys.platform,
            "found": False,
            "title": "",
            "class_name": "",
            "message": str(exc),
        }
    if not win:
        return {
            "ok": False,
            "platform": "win32",
            "found": False,
            "title": "",
            "class_name": "",
            "message": "window-missing",
        }
    return {
        "ok": True,
        "platform": "win32",
        "found": True,
        "title": win.Name or "",
        "class_name": win.ClassName or "",
        "message": "ready-qt-surface",
    }


def dump_tree(name: str = "通讯录管理", max_depth: int = 6) -> str:
    win = find_manager_window(name)
    if not win:
        return "WINDOW_NOT_FOUND"
    rect = win.BoundingRectangle
    lines: list[str] = [
        f"Name={win.Name!r}",
        f"ClassName={win.ClassName!r}",
        f"ControlType={win.ControlTypeName!r}",
        "",
    ]

    def walk(ctrl, depth: int = 0) -> None:
        if depth > max_depth:
            return
        try:
            r = ctrl.BoundingRectangle
            lines.append(
                f"{'  ' * depth}{ctrl.ControlTypeName} name={ctrl.Name!r} "
                f"class={ctrl.ClassName!r} rect=({r.left},{r.top},{r.right},{r.bottom})"
            )
            for child in ctrl.GetChildren():
                walk(child, depth + 1)
        except Exception as exc:  # noqa: BLE001
            lines.append(f"{'  ' * depth}<error {exc}>")

    walk(win)
    painted = any("MMUIRenderSubWindowHW" in (ln or "") for ln in lines)
    lines.append("")
    if painted:
        lines.append("DIAGNOSIS: WeChat 4.x Qt paint surface (MMUIRenderSubWindowHW).")
        lines.append("UIA will not list nicknames. This is expected, not a hang.")
        lines.append("Scan uses click offsets inside this window.")
    layout = _layout(rect)
    lines.append(
        f"LAYOUT sidebar={layout['sidebar']} row_h={layout['row_h']} "
        f"avatar=({layout['avatar_x']},{layout['first_y']})"
    )
    return "\n".join(lines)


def _dpi_aware() -> None:
    if not is_windows():
        return
    try:
        import ctypes

        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass


def virtual_screen() -> tuple[int, int, int, int]:
    _dpi_aware()
    if not is_windows():
        return (0, 0, 1920, 1080)
    import ctypes

    user32 = ctypes.windll.user32
    vx = int(user32.GetSystemMetrics(76))
    vy = int(user32.GetSystemMetrics(77))
    vw = int(user32.GetSystemMetrics(78))
    vh = int(user32.GetSystemMetrics(79))
    if vw <= 0 or vh <= 0:
        vw = int(user32.GetSystemMetrics(0))
        vh = int(user32.GetSystemMetrics(1))
        vx, vy = 0, 0
    return vx, vy, vx + vw, vy + vh


def click_screen(x: int, y: int) -> None:
    """Physical-pixel click. Do not use UIA Click — it drifts under DPI."""
    _dpi_aware()
    if not is_windows():
        return
    import ctypes

    x, y = int(x), int(y)
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.05)
    ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
    time.sleep(0.03)
    ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)


def manager_screen_rect(name: str = "通讯录管理"):
    """Physical window box via win32, not UIA."""
    if not is_windows():
        return None
    try:
        import win32gui
    except Exception:
        return None
    found = []

    def cb(hwnd, _ctx):
        if not win32gui.IsWindowVisible(hwnd):
            return True
        title = win32gui.GetWindowText(hwnd) or ""
        if title == name or (name in title and "打标" not in title and "Region" not in title):
            found.append(hwnd)
        return True

    win32gui.EnumWindows(cb, None)
    if not found:
        return None
    return win32gui.GetWindowRect(found[0])


def resize_manager_to_reference(name: str = "通讯录管理") -> None:
    from reference_layout import REF_H, REF_W

    if not is_windows():
        return
    import win32con
    import win32gui

    found = []

    def cb(hwnd, _ctx):
        if not win32gui.IsWindowVisible(hwnd):
            return True
        title = win32gui.GetWindowText(hwnd) or ""
        if title == name or (name in title and "打标" not in title and "Region" not in title):
            found.append(hwnd)
        return True

    win32gui.EnumWindows(cb, None)
    if not found:
        raise RuntimeError("通讯录管理窗口未找到")
    hwnd = found[0]
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, 80, 80, int(REF_W), int(REF_H), win32con.SWP_SHOWWINDOW)
    time.sleep(0.35)


def snapshot_manager(dest, name: str = "通讯录管理") -> dict:
    """Resize to 1307x849, then capture that window."""
    from reference_layout import marks_for_image

    _dpi_aware()
    resize_manager_to_reference(name)
    box = manager_screen_rect(name)
    if not box:
        raise RuntimeError("通讯录管理窗口未找到")
    left, top, right, bottom = [int(v) for v in box]
    if right - left < 80 or bottom - top < 80:
        raise RuntimeError("窗口矩形过小")
    try:
        from PIL import ImageGrab
    except ImportError as exc:
        raise RuntimeError("缺少 Pillow，无法截图") from exc
    dest.parent.mkdir(parents=True, exist_ok=True)
    img = ImageGrab.grab(bbox=(left, top, right, bottom))
    img.save(dest)
    iw, ih = img.size
    marks = marks_for_image(iw, ih)
    try:
        from calibrate import auto_marks

        live = (auto_marks(dest) or {}).get("marks") or {}
        for key in ("search", "check", "avatar", "row2"):
            if live.get(key):
                marks[key] = live[key]
        if live.get("avatar") and live.get("row2"):
            marks["row_h"] = max(36, int(live["row2"]["y"] - live["avatar"]["y"]))
    except Exception:
        pass
    return {
        "path": str(dest),
        "left": left,
        "top": top,
        "right": right,
        "bottom": bottom,
        "width": right - left,
        "height": bottom - top,
        "image_width": iw,
        "image_height": ih,
        "mode": "window",
        "auto_marks": marks,
        "candidates": {},
        "reference": {"w": iw, "h": ih},
    }


def test_click(x: int, y: int) -> None:
    click_screen(x, y)


def layout_from_calibrate(rect, cal: dict | None) -> dict:
    """Use the same absolute screen pixels as 试点击. Rebase if the window moved."""
    base = _layout(rect)
    if not cal or cal.get("avatar_x") is None:
        return base
    old_l = int(cal.get("origin_left") or 0)
    old_t = int(cal.get("origin_top") or 0)
    dx = dy = 0
    cur = manager_screen_rect()
    if cur:
        dx = int(cur[0]) - old_l
        dy = int(cur[1]) - old_t

    def abs_pt(xk, yk, fx, fy):
        if cal.get(xk) is None or cal.get(yk) is None:
            return fx, fy
        return int(cal[xk]) + dx, int(cal[yk]) + dy

    sx, sy = abs_pt("search_x", "search_y", base["search_x"], base["search_y"])
    cx, cy = abs_pt("check_x", "check_y", base["check_x"], base["first_y"])
    ax, ay = abs_pt("avatar_x", "avatar_y", base["avatar_x"], base["first_y"])
    r2x, r2y = abs_pt("row2_x", "row2_y", ax, ay + 58)
    row_h = abs(r2y - ay) or 58
    base.update(
        {
            "search_x": sx,
            "search_y": sy,
            "check_x": cx,
            "avatar_x": ax,
            "first_y": ay,
            "row_h": max(36, row_h),
            "list_mid_x": ax + 80,
            "calibrated": True,
        }
    )
    return base


def _layout(rect) -> dict:
    width = max(1, rect.right - rect.left)
    # If UIA reports a very wide window, the manager itself is still the
    # left stack: sidebar ~188px, list after that.
    sidebar = 188
    if width < 700:
        sidebar = max(140, int(width * 0.22))
    return {
        "left": rect.left,
        "top": rect.top,
        "right": rect.right,
        "bottom": rect.bottom,
        "sidebar": sidebar,
        "search_x": rect.left + sidebar + 80,
        "search_y": rect.top + 28,
        "avatar_x": rect.left + sidebar + 52,
        "check_x": rect.left + sidebar + 16,
        "first_y": rect.top + 108,
        "row_h": 58,
        "list_mid_x": rect.left + sidebar + 220,
    }


def collect_texts(ctrl, acc: list | None = None, depth: int = 0, max_depth: int = 8) -> list[str]:
    acc = acc if acc is not None else []
    try:
        name = (ctrl.Name or "").strip()
        if name:
            acc.append(name)
        if depth < max_depth:
            for child in ctrl.GetChildren():
                collect_texts(child, acc, depth + 1, max_depth)
    except Exception:
        pass
    return acc


PLACE_WORDS = (
    "中国香港", "中国澳门", "中国台湾", "香港", "澳门", "台湾",
    "新加坡", "马来西亚", "日本", "韩国", "美国", "英国", "加拿大",
    "澳大利亚", "泰国", "越南", "菲律宾", "印度尼西亚", "印尼",
    "德国", "法国", "意大利", "西班牙", "俄罗斯", "印度", "阿联酋",
    "广东", "北京", "上海", "深圳", "浙江", "江苏", "四川", "福建",
    "山东", "湖北", "湖南", "河南", "河北", "安徽", "重庆", "天津",
)


def parse_region(texts: list[str]) -> str:
    blob = "\n".join(texts)
    m = re.search(r"地\s*区\s*[:：]?\s*([^\n]{1,24})", blob)
    if m:
        val = m.group(1).strip(" ：:·-|")
        if val and val not in {"朋友资料", "备注", "添加备注名"} and not re.search(r"Wfäe|微信号|Nothing|tgx:", val, re.I):
            return val
    for i, t in enumerate(texts):
        if re.search(r"微.?号|Wfäe|WeChat\s*ID", t, re.I):
            if i + 1 < len(texts):
                nxt = texts[i + 1].strip()
                if nxt and not re.search(r"朋友|备注|更多|来源|标签|签名", nxt):
                    if len(nxt) <= 24:
                        return nxt
    for t in texts:
        for place in PLACE_WORDS:
            if place in t and "微信号" not in t:
                extra = re.sub(r"地\s*区\s*[:：]?", "", t).strip()
                return extra or place
    for i, t in enumerate(texts):
        if t in {"地区", "地区：", "Region", "Region:"}:
            if i + 1 < len(texts):
                nxt = texts[i + 1].strip()
                if nxt and nxt not in {"朋友资料", "备注", "添加备注名", "朋友圈", "更多信息"}:
                    return nxt
        if t.startswith("地区：") and len(t) > 3:
            return t.split("：", 1)[1].strip()
        if t.startswith("地区:") and len(t) > 3:
            return t.split(":", 1)[1].strip()
    return ""


def parse_nickname(texts: list[str], fallback: str = "") -> str:
    skip = {
        "朋友资料",
        "备注",
        "添加备注名",
        "朋友圈",
        "更多信息",
        "共同群聊",
        "个性签名",
        "来源",
        "添加时间",
        "发消息",
        "语音聊天",
        "视频聊天",
        "地区",
        "微信号",
        "标签",
        "朋友权限",
        "通讯录管理",
        "微信地区打标台",
        "WeChat Region Desk",
        "任务栏",
        "Taskbar",
        "搜索",
        "通知",
        "Windows 输入体验",
        "Program Manager",
    }
    for t in texts:
        if not t or t in skip or t.endswith("：") or t.startswith("微信号"):
            continue
        if t.startswith("地区") or t.startswith("微信"):
            continue
        if len(t) > 40:
            continue
        return t
    return fallback


def _window_score(texts: list[str]) -> int:
    blob = "\n".join(texts)
    score = 0
    if "微信号" in blob:
        score += 4
    if "地区" in blob:
        score += 4
    if "朋友资料" in blob:
        score += 2
    if "个性签名" in blob:
        score += 1
    if "任务栏" in blob:
        score -= 5
    return score


def read_open_profile(auto) -> tuple[str, str]:
    root = auto.GetRootControl()
    best_texts: list[str] = []
    best_score = 0
    for win in root.GetChildren():
        title = win.Name or ""
        if "打标台" in title or "Region Desk" in title or title in {"任务栏", "Taskbar"}:
            continue
        texts = collect_texts(win, max_depth=8)
        score = _window_score(texts)
        if title == "通讯录管理":
            score += 1
        if score > best_score:
            best_score = score
            best_texts = texts
    if best_score <= 0:
        return "", ""
    return parse_nickname(best_texts), parse_region(best_texts)


def list_row_controls(win):
    found = []

    def walk(node, depth=0):
        if depth > 12:
            return
        try:
            if (node.ControlTypeName or "") in {"ListItemControl", "DataItemControl"}:
                found.append(node)
            for ch in node.GetChildren():
                walk(ch, depth + 1)
        except Exception:
            return

    walk(win)
    return found


def manager_alive(name: str = "通讯录管理") -> bool:
    try:
        win = find_manager_window(name)
        return bool(win and (win.Name or "").find(name) >= 0)
    except Exception:
        return False


_OCR = None


def _ocr_engine():
    global _OCR
    if _OCR is False:
        return None
    if _OCR is not None:
        return _OCR
    try:
        from rapidocr_onnxruntime import RapidOCR

        _OCR = RapidOCR()
        return _OCR
    except Exception:
        _OCR = False
        return None


def ocr_windows(pil_img) -> list[str]:
    """Use the OCR engine shipped with Windows 10+ (same family as Live Text)."""
    try:
        import winocr

        out = None
        for lang in ("zh-Hans", "zh-CN", "en"):
            try:
                out = winocr.recognize_pil_sync(pil_img, lang=lang)
            except TypeError:
                out = winocr.recognize_pil_sync(pil_img)
            except Exception:
                out = None
            if out:
                break
    except Exception:
        return []
    text = ""
    if isinstance(out, str):
        text = out
    elif isinstance(out, dict):
        text = str(out.get("text") or out.get("plain_text") or "")
        if not text and out.get("lines"):
            text = "\n".join(str(x) for x in out["lines"])
    elif hasattr(out, "text"):
        text = str(out.text)
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def ocr_lines(pil_img) -> list[str]:
    engine = _ocr_engine()
    rapid: list[str] = []
    if engine is not None:
        import numpy as np

        arr = np.array(pil_img.convert("RGB"))[:, :, ::-1]
        try:
            result, _elapse = engine(arr)
            for item in result or []:
                if len(item) >= 2 and item[1]:
                    rapid.append(str(item[1]).strip())
        except Exception:
            rapid = []
    if rapid:
        return rapid
    return ocr_windows(pil_img)


def parse_ocr_profile(lines: list[str]) -> tuple[str, str]:
    region = parse_region(lines)
    nick = ""
    skip = {"朋友资料", "备注", "微信号", "地区", "标签", "更多信息", "Weixin", "微信", "添加备注名", "朋友圈"}
    for raw in lines:
        t = raw.strip()
        if re.search(r"地\s*区", t):
            part = re.split(r"[:：]", t, 1)
            if len(part) > 1 and part[1].strip():
                region = region or part[1].strip()
            continue
        if re.search(r"微.?号|Wfäe", t):
            if not nick:
                left = re.split(r"微.?号|Wfäe", t, 1)[0].strip(" ：:")
                if left and left not in skip:
                    nick = left
            continue
        if t in skip or len(t) > 36:
            continue
        if not nick:
            nick = re.split(r"微.?号|Wfäe", t, 1)[0].strip()
    nick = re.split(r"微.?号|Wfäe", nick or "", 1)[0].strip(" ：:")
    return nick, region


def read_profile_by_ocr(x: int, y: int, log: LogFn | None = None) -> tuple[str, str]:
    try:
        from PIL import ImageGrab
    except Exception:
        return "", ""
    boxes = [
        (x + 8, y - 90, x + 560, y + 520),
        (x - 80, y - 90, x + 480, y + 480),
        (x + 80, y - 40, x + 620, y + 560),
    ]
    all_lines: list[str] = []
    for box in boxes:
        img = ImageGrab.grab(bbox=box)
        all_lines.extend(ocr_lines(img))
    nick, region = parse_ocr_profile(all_lines)
    if log:
        if all_lines:
            log("OCR " + " | ".join(all_lines[:10]))
        else:
            log("OCR 空白。请在本机执行 pip install winocr rapidocr-onnxruntime")
    return nick, region


def wheel_delta(x: int, y: int, delta: int) -> None:
    import ctypes

    ctypes.windll.user32.SetCursorPos(int(x), int(y))
    time.sleep(0.04)
    # MOUSEEVENTF_WHEEL = 0x0800, delta 120 = one notch
    ctypes.windll.user32.mouse_event(0x0800, 0, 0, delta & 0xFFFFFFFF, 0)


def is_avatar_chip(img) -> bool:
    try:
        import numpy as np
    except Exception:
        return True
    a = np.asarray(img.convert("RGB"))
    sat = a.max(axis=2) - a.min(axis=2)
    return float(sat.mean()) > 18 and float(a.std()) > 14


def chip_changed(a, b, threshold: float = 10.0) -> bool:
    try:
        import numpy as np
    except Exception:
        return True
    aa = np.asarray(a).astype("float32")
    bb = np.asarray(b).astype("float32")
    if aa.shape != bb.shape:
        return True
    return float(np.mean(np.abs(aa - bb))) > threshold


def dismiss_profile(auto, layout: dict) -> None:
    """Close the card by clicking the search box, not a checkbox."""
    click_screen(layout["search_x"], layout["search_y"])
    time.sleep(0.12)


def scan_contacts(
    cfg: dict,
    log: LogFn,
    should_stop: Callable[[], bool],
    on_row: Callable[[dict], None],
) -> list[dict]:
    auto = _auto()
    name = cfg.get("manager_window_name") or "通讯录管理"
    win = find_manager_window(name)
    if not win:
        raise RuntimeError("通讯录管理窗口未找到")
    try:
        win.SetActive()
    except Exception:
        pass
    time.sleep(0.8)
    if not manager_alive(name):
        raise RuntimeError("通讯录管理在激活后消失，请重新打开该窗口后再扫")
    layout = layout_from_calibrate(win.BoundingRectangle, cfg.get("calibrate"))
    if not layout.get("calibrated"):
        raise RuntimeError("尚未完成校点。请先在截图上点出搜索框、勾选圈和两行头像。")
    if layout["avatar_x"] <= layout.get("check_x", layout["avatar_x"] - 40) + 28:
        layout["avatar_x"] = layout["check_x"] + 42
        log("头像坐标过于靠近圆圈，已右移，避免勾选好友")
    log("不会发送 Esc。微信 4.1 里 Esc 会直接关掉通讯录管理。")
    log(
        f"使用校点 row={layout['row_h']} "
        f"avatar=({layout['avatar_x']},{layout['first_y']})"
    )
    limit = int(cfg.get("limit") or 0)
    log(f"本次扫描上限：{'不限制' if limit <= 0 else str(limit) + ' 人'}")
    pause = float(cfg.get("scan_pause_seconds") or 0.45)
    empty_tag = cfg.get("empty_region_tag") or "未填写地区"
    max_len = int(cfg.get("max_tag_name_length") or 16)
    rows: list[dict] = []
    seen: set[str] = set()
    stagnant = 0
    last_nick = ""
    visible = max(6, int((layout["bottom"] - layout["first_y"] - 20) / layout["row_h"]))

    def grab_avatar_centers() -> list[tuple[int, int]]:
        try:
            from PIL import ImageGrab
            from calibrate import detect_targets, image_to_screen
        except Exception:
            return []
        left, top, right, bottom = virtual_screen()
        info = {"left": left, "top": top, "right": right, "bottom": bottom}
        tmp = dest_shot()
        img = ImageGrab.grab(bbox=(left, top, right, bottom), all_screens=True)
        img.save(tmp)
        info["image_width"], info["image_height"] = img.size
        found = detect_targets(tmp)
        out = []
        for it in found.get("avatar") or []:
            sx, sy = image_to_screen(info, it["x"], it["y"])
            if abs(sx - layout["avatar_x"]) <= 28:
                out.append((sx, sy))
        out.sort(key=lambda p: p[1])
        return out

    def dest_shot():
        from pathlib import Path

        p = Path(__file__).resolve().parent / "output" / "scan_live.png"
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    def one_click(x: int, y: int) -> dict | None:
        if not manager_alive(name):
            raise RuntimeError("通讯录管理已关闭，扫描已停止")
        click_screen(int(x), int(y))
        time.sleep(max(0.95, pause + 0.25))
        nick, region = read_open_profile(auto)
        if not region or nick in {"Weixin", "微信", "任务栏", "通讯录管理"}:
            o_nick, o_region = read_profile_by_ocr(int(x), int(y), log=log)
            if o_region:
                region = o_region
            if o_nick and o_nick not in {"Weixin", "微信"}:
                nick = o_nick
        dismiss_profile(auto, layout)
        if nick in {"任务栏", "Taskbar", "搜索", "通知", "通讯录管理", "Weixin", "微信"}:
            nick = ""
        if not nick and not region:
            return None
        region = clean_region_text(region) or region
        tag = normalize_region(region, empty_tag=empty_tag, max_len=max_len)
        return {
            "nickname": nick,
            "region_raw": region,
            "tag_name": tag,
            "is_hongkong": bool(is_hongkong(region)),
            "status": "scanned",
            "note": "",
        }

    # Prefer native list items when a rare build exposes them.
    items = []
    if False and len(items) >= 3:
        log("检测到可见列表项，改走控件点击")
        for item in items:
            if should_stop() or (limit and len(rows) >= limit):
                break
            rect = item.BoundingRectangle
            rec = one_click((rect.left + rect.right) // 2, (rect.top + rect.bottom) // 2)
            if not rec:
                continue
            sig = rec["nickname"] + "|" + rec["region_raw"]
            if sig in seen:
                continue
            seen.add(sig)
            rows.append(rec)
            on_row(rec)
            log(f"[{len(rows)}] {rec['nickname']} | {rec['region_raw'] or '（空）'} → {rec['tag_name']}")
        return rows

    log("只点击您标定的头像坐标，每读一人后滚动一行")
    while not should_stop():
        if not manager_alive(name):
            log("通讯录管理已关闭，停止移动鼠标")
            break
        centers = [(layout["avatar_x"], layout["first_y"])]
        progressed = False
        for _sx, sy in centers:
            if should_stop():
                break
            if limit and len(rows) >= limit:
                log("已达到扫描上限")
                return rows
            try:
                rec = one_click(_sx, sy)
            except RuntimeError as exc:
                log(str(exc))
                return rows
            if not rec:
                stagnant += 1
                continue
            sig = rec["nickname"] + "|" + rec["region_raw"]
            if sig in seen:
                continue
            seen.add(sig)
            rows.append(rec)
            on_row(rec)
            progressed = True
            stagnant = 0
            log(f"[{len(rows)}] {rec['nickname']} | {rec['region_raw'] or '（空）'} → {rec['tag_name']}")
            if rec["nickname"] == last_nick:
                stagnant += 1
            last_nick = rec["nickname"]
        if not progressed:
            stagnant += 1
        if not manager_alive(name):
            log("通讯录管理已关闭，停止移动鼠标")
            break
        try:
            from PIL import ImageGrab

            r = 20
            ax, ay = layout["avatar_x"], layout["first_y"]
            before = ImageGrab.grab((ax - r, ay - r, ax + r, ay + r))
            moved = False
            for _ in range(16):
                wheel_delta(layout["list_mid_x"], ay, -40)
                time.sleep(0.12)
                after = ImageGrab.grab((ax - r, ay - r, ax + r, ay + r))
                if chip_changed(before, after) and is_avatar_chip(after):
                    moved = True
                    break
            if not moved:
                wheel_delta(layout["list_mid_x"], ay, -120)
                time.sleep(0.16)
        except Exception:
            auto.MoveTo(layout["list_mid_x"], layout["first_y"])
            auto.WheelDown(wheelTimes=1, waitTime=0.08)
            time.sleep(0.2)
        if stagnant >= 10:
            log("连续重复或空白，结束扫描")
            break
    log(f"扫描结束，共 {len(rows)} 人")
    return rows


def plan_from_rows(rows: list[dict]) -> list[dict]:
    groups: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        groups[str(row.get("tag_name") or "未填写地区")].append(str(row.get("nickname") or ""))
    plan = []
    for tag, names in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        plan.append({"tag_name": tag, "count": len(names), "sample": "、".join(names[:8])})
    return plan


def counts_from_rows(rows: list[dict]) -> dict:
    tags = Counter(str(r.get("tag_name") or "") for r in rows)
    return {
        "total": len(rows),
        "hongkong": sum(1 for r in rows if r.get("is_hongkong")),
        "tags": len(tags),
        "top": [{"tag": k, "count": v} for k, v in tags.most_common(20)],
    }


def try_click_named(root, names: list[str]) -> bool:
    targets = []

    def walk(node, depth=0):
        if depth > 12:
            return
        try:
            if (node.Name or "") in names:
                targets.append(node)
            for ch in node.GetChildren():
                walk(ch, depth + 1)
        except Exception:
            return

    walk(root)
    if not targets:
        return False
    targets[0].Click()
    return True


def search_and_select(win, nickname: str, cfg: dict, auto) -> bool:
    layout = layout_from_calibrate(win.BoundingRectangle, cfg.get("calibrate"))
    click_screen(layout["search_x"], layout["search_y"])
    time.sleep(0.12)
    auto.SendKeys("{Ctrl}a")
    auto.SendKeys("{Delete}")
    time.sleep(0.08)
    auto.SendKeys(nickname, waitTime=0.02)
    time.sleep(0.4)
    click_screen(layout["check_x"], layout["first_y"])
    time.sleep(float(cfg.get("click_pause_seconds") or 0.25))
    return True


def apply_tag_to_selection(tag: str, auto) -> None:
    root = auto.GetRootControl()
    opened = try_click_named(root, ["添加标签", "设置标签", "标签", "打标签"])
    if not opened:
        auto.SendKeys("{Apps}")
        time.sleep(0.2)
        try_click_named(root, ["添加标签", "设置标签", "标签"])
    time.sleep(0.3)
    auto.SendKeys(tag, waitTime=0.03)
    time.sleep(0.2)
    auto.SendKeys("{Enter}")
    time.sleep(0.3)
    try_click_named(root, ["确定", "完成", "保存", "OK"])
    time.sleep(0.2)


def apply_tags(
    rows: list[dict],
    cfg: dict,
    log: LogFn,
    should_stop: Callable[[], bool],
) -> dict:
    auto = _auto()
    win = find_manager_window(cfg.get("manager_window_name") or "通讯录管理")
    if not win:
        raise RuntimeError("通讯录管理窗口未找到")
    win.SetActive()
    time.sleep(0.35)
    only_hk = bool(cfg.get("only_hk"))
    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        tag = str(row.get("tag_name") or "").strip()
        if not tag:
            continue
        if only_hk and not row.get("is_hongkong"):
            continue
        groups[tag].append(row)
    ok = 0
    miss = 0
    log(f"开始打标，共 {len(groups)} 个标签")
    for tag, members in groups.items():
        if should_stop():
            break
        log(f"标签「{tag}」{len(members)} 人")
        selected = 0
        for member in members:
            if should_stop():
                break
            nick = str(member.get("nickname") or "")
            if not nick:
                miss += 1
                continue
            search_and_select(win, nick, cfg, auto)
            ok += 1
            selected += 1
            log(f"OK  {tag}  {nick}")
        if selected:
            apply_tag_to_selection(tag, auto)
        auto.SendKeys("{Ctrl}a")
        auto.SendKeys("{Delete}")
        time.sleep(0.15)
    log(f"打标结束 OK={ok} MISS={miss}")
    return {"ok": ok, "miss": miss, "tags": len(groups)}
