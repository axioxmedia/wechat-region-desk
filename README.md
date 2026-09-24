<div align="center">

# WeChat Region Desk

**Packed via Axiox Media**

A local Windows wizard that reads the Region field in PC WeChat 4.1 Contact Manager and writes region tags.

<p>
  <a href="docs/README-zh.md"><img src="https://img.shields.io/badge/中文说明-README--zh-e7c07a?style=for-the-badge" alt="Chinese README" /></a>
</p>

<p>
  <a href="#install">Install</a> ·
  <a href="#features">Features</a> ·
  <a href="#requirements">Requirements</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#documentation">FAQ</a>
</p>

<p>
  <img src="https://img.shields.io/badge/platform-Windows_10%2F11-0b0d12?style=flat-square" alt="Windows" />
  <img src="https://img.shields.io/badge/python-3.11%2B-e7c07a?style=flat-square" alt="Python" />
  <img src="https://img.shields.io/badge/ui-zh%20%2F%20en-7ee0c6?style=flat-square" alt="i18n" />
  <img src="https://img.shields.io/badge/wechat-4.1.13-c9a227?style=flat-square" alt="wechat" />
</p>

</div>

<p align="center">
  <img src="docs/APPCap.png" width="100%" alt="WeChat Region Desk preview" />
</p>

> [!NOTE]
> The packed EXE is unsigned. Windows SmartScreen may warn on first launch. The app only drives the WeChat window already open on this PC.

---

## At a glance

| Item | Value |
| --- | --- |
| Product | WeChat Region Desk / 微信地区打标台 |
| Version | 1.0.0 |
| Target client | WeChat PC 4.1.13.65 |
| UI | zh / en wizard |
| Output | `output/contacts_region.xlsx` plus WeChat tags |

<a id="install"></a>

## Install

### 1. GitHub Deploy Desk (recommended)

Install with [GitHub Deploy Desk](https://github.com/axioxmedia/github-deployer). Paste this repository URL, choose source, and launch.

### 2. Build from source

| Step | Action |
| --- | --- |
| 1 | Install Python 3.11+ and tick “Add python.exe to PATH” |
| 2 | Unzip the project |
| 3 | Double-click `build_exe.bat` |
| 4 | Open `dist\WeChatRegionDesk.exe` |

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

<a id="features"></a>

## Features

| Step | Action |
| --- | --- |
| 01 Window | Detect the already-open 通讯录管理 window |
| 02 Rules | Hong Kong keywords, empty-region tag, optional prefix |
| 03 Probe | Dump the Qt / UIA control tree |
| 04 Scan | Click avatars, read 地区, write Excel |
| 05 Review | Edit `tag_name`, merge cities, download xlsx |
| 06 Apply | Search, tick, and write WeChat tags |

Hong Kong matching treats `中国香港`, `香港`, `Hong Kong`, and `HK` as tag `香港`.

<a id="requirements"></a>

## Requirements

| | Minimum | Recommended |
| --- | --- | --- |
| OS | Windows 10 | Windows 11 |
| Python | 3.11 | 3.12 |
| WeChat | 4.1.6+ | 4.1.13.65 |
| Display | Contact Manager visible | Contact Manager in front |

<a id="architecture"></a>

## Architecture

```
pywebview window
    -> FastAPI 127.0.0.1
        -> static wizard (zh / en)
        -> wechat_ops (UI Automation)
        -> output/*.xlsx
PyInstaller onefile EXE
```

<a id="documentation"></a>

## FAQ

<details>
<summary>Does the search box in Contact Manager already filter by region?</summary>
Some older WeChat builds did. If typing 香港 already filters the list, you do not need this app for Hong Kong only. Use it when you want every contact tagged by region.
</details>

<details>
<summary>Will this upload my contacts?</summary>
No. All files stay next to the EXE. Tags are written only into your local WeChat client.
</details>

<details>
<summary>Why trial-scan 15 people first?</summary>
WeChat 4.x is a Qt UI. A minor client update can move the avatar hit-box. Confirm Region values in Excel before a 782-person run.
</details>

Packed via Axiox Media · [axiox.media](https://axiox.media)
