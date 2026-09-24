const LAST = 6;
const SLUG = "wechat-region-desk";
const AXIOXMEDIA_BRAND = "Axiox Media";
const AIO_WATERMARK = "axioxmedia";

const I18N = {
  zh: {
    "app.title": "微信地区打标台",
    "app.subtitle": "读取电脑微信「地区」，按地域写入标签",
    "next": "下一步",
    "back": "上一步",
    "stop": "停止",
    "mem": "记住本次选择",
    "s0.h": "打开通讯录管理",
    "s0.lead": "本工具只驱动已经打开的微信窗口。请先登录电脑微信 4.1，并打开「通讯录 → 通讯录管理」。",
    "s0.plat": "系统",
    "s0.win": "窗口",
    "s0.cls": "类名",
    "s0.ver": "微信版本（备忘）",
    "s0.refresh": "重新检测",
    "s0.needwin": "尚未找到「通讯录管理」。请打开该窗口后再继续。",
    "s0.linux": "当前不是 Windows。可预览界面，实际扫描必须在已登录微信的 Windows 电脑上运行。",
    "s0.ok": "已找到通讯录管理窗口，可以继续。",
    "s1.h": "标签取地区第一段",
    "s1.lead": "不必手填城市词。读到「地区」后，取空格前的第一段作为标签：广东 深圳 → 广东；马来西亚 吉隆坡 → 马来西亚；中国香港 → 中国香港。",
    "s1.hk": "香港匹配词（逗号分隔）",
    "s1.empty": "空地区标签",
    "s1.prefix": "标签前缀（可选）",
    "s1.pause": "扫描间隔（秒）",
    "s1.len": "标签最大字数",
    "s1.onlyhk": "打标阶段只处理香港好友",
    "s2.h": "探测窗口控件",
    "s2.lead": "微信 4.x 把名单画在自绘层上，控件树通常只有三行，这是正常结果，不是卡住。探测完成后请点右下角「下一步」。",
    "s2.empty": "尚未探测",
    "s2.run": "探测",
    "s3.h": "扫描好友地区",
    "s3.lead": "程序会逐个点开头像读取「地区」。请先试扫 15 人，确认无误再全量。",
    "s3.all": "扫描全部好友",
    "s3.limit": "试扫人数",
    "s3.warn": "扫描时请不要操作鼠标键盘，也不要按 Esc。Esc 会关掉通讯录管理。",
    "s3.run": "开始扫描",
    "s4.h": "核对打标计划",
    "s4.lead": "香港行以绿色标出。可直接改 tag_name，合并过细的城市后再写入。",
    "s4.save": "保存修改",
    "s4.xlsx": "下载 Excel",
    "s5.h": "写入微信标签",
    "s5.lead": "按计划搜索昵称、勾选并添加标签。完成后请在「标签」栏抽查。",
    "s5.run": "开始打标",
    "sc.h": "在截图上标定点击位置",
    "sc.lead": "拍摄前会把通讯录管理改成 1307×849，再截图并按参考图标出点击位。不对再用方向键微调。",
    "sc.align": "自动对齐（默认关，不建议开）",
    "sc.search": "1 搜索框",
    "sc.check": "2 第一行圆圈",
    "sc.avatar": "3 第一行头像",
    "sc.row2": "4 第二行头像",
    "sc.snap": "拍摄窗口",
    "sc.test": "试点击当前点",
    "sc.clear1": "清除当前点",
    "sc.clearall": "清除全部",
    "rail.0": "窗口",
    "rail.1": "规则",
    "rail.2": "探测",
    "rail.3": "校点",
    "rail.4": "扫描",
    "rail.5": "核对",
    "rail.6": "打标",
  },
  en: {
    "app.title": "WeChat Region Desk",
    "app.subtitle": "Read the Region field and write WeChat tags",
    "next": "Next",
    "back": "Back",
    "stop": "Stop",
    "mem": "Remember these choices",
    "s0.h": "Open Contact Manager",
    "s0.lead": "This app only drives the already-open WeChat window. Sign in to WeChat 4.1 PC and open Contacts → Contact Manager.",
    "s0.plat": "OS",
    "s0.win": "Window",
    "s0.cls": "Class",
    "s0.ver": "WeChat version (note)",
    "s0.refresh": "Recheck",
    "s0.needwin": "Contact Manager was not found. Open that window first.",
    "s0.linux": "Not Windows. You can preview the UI; scanning requires a logged-in WeChat PC client.",
    "s0.ok": "Contact Manager is visible. Continue.",
    "s1.h": "Tag is the first region token",
    "s1.lead": "No city keyword list. 广东 深圳 → 广东; 马来西亚 吉隆坡 → 马来西亚; 中国香港 → 中国香港.",
    "s1.hk": "Hong Kong keywords (comma separated)",
    "s1.empty": "Empty-region tag",
    "s1.prefix": "Tag prefix (optional)",
    "s1.pause": "Scan pause (sec)",
    "s1.len": "Max tag length",
    "s1.onlyhk": "Apply tags to Hong Kong contacts only",
    "s2.h": "Probe UI tree",
    "s2.lead": "WeChat 4.x paints the list itself. A three-line tree is normal, not a hang. Click Next after the probe.",
    "s2.empty": "Not probed yet",
    "s2.run": "Probe",
    "s3.h": "Scan regions",
    "s3.lead": "The app clicks each avatar and reads Region. Trial-scan 15 people before a full pass.",
    "s3.all": "Scan every contact",
    "s3.limit": "Trial count",
    "s3.warn": "Do not touch the mouse or press Esc. Esc closes Contact Manager on WeChat 4.1.",
    "s3.run": "Start scan",
    "s4.h": "Review the plan",
    "s4.lead": "Hong Kong rows are green. Edit tag_name to merge fine-grained cities before writing.",
    "s4.save": "Save edits",
    "s4.xlsx": "Download Excel",
    "s5.h": "Write WeChat tags",
    "s5.lead": "Search each nickname, tick the row, and add the planned tag. Spot-check Tags afterwards.",
    "s5.run": "Start tagging",
    "sc.h": "Mark click points on a screenshot",
    "sc.lead": "The shot is cropped to Contact Manager and pre-marked. Nudge if a crosshair is off.",
    "sc.align": "Auto-align (on by default)",
    "sc.search": "1 Search box",
    "sc.check": "2 First checkbox",
    "sc.avatar": "3 First avatar",
    "sc.row2": "4 Second avatar",
    "sc.snap": "Capture window",
    "sc.test": "Test-click current point",
    "sc.clear1": "Clear this point",
    "sc.clearall": "Clear all",
    "rail.0": "Window",
    "rail.1": "Rules",
    "rail.2": "Probe",
    "rail.3": "Calibrate",
    "rail.4": "Scan",
    "rail.5": "Review",
    "rail.6": "Apply",
  },
};

let lang = "zh";
let currentStep = 0;
const calState = {
  mode: "search",
  snap: null,
  data: {},
};
let defaults = {};
let windowReady = false;
let packShown = 0;
let packTarget = 0;
let packTimer = null;

function detectUiLang() {
  const saved = localStorage.getItem("aio.uiLang");
  if (saved === "zh" || saved === "en") return saved;
  const nav = (navigator.language || "zh").toLowerCase();
  return nav.startsWith("zh") ? "zh" : "en";
}

function t(key) {
  return (I18N[lang] && I18N[lang][key]) || I18N.zh[key] || key;
}

function applyI18n() {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    el.textContent = t(el.getAttribute("data-i18n"));
  });
  document.getElementById("langZh").classList.toggle("on", lang === "zh");
  document.getElementById("langEn").classList.toggle("on", lang === "en");
  renderStepNav();
}

function hideAllStages() {
  for (let i = 0; i <= LAST; i++) document.getElementById("stage" + i)?.classList.remove("on");
}

function goStep(n) {
  currentStep = n;
  hideAllStages();
  document.getElementById("stage" + n)?.classList.add("on");
  renderStepNav();
  applyI18n();
}

function renderStepNav() {
  const nav = document.getElementById("stepNav");
  nav.innerHTML = "";
  for (let i = 0; i <= LAST; i++) {
    const pill = document.createElement("button");
    pill.type = "button";
    pill.className = "step-pill" + (i === currentStep ? " on" : i < currentStep ? " done" : "");
    pill.textContent = `${String(i + 1).padStart(2, "0")} ${t("rail." + i)}`;
    pill.addEventListener("click", () => {
      if (i <= currentStep) goStep(i);
    });
    nav.appendChild(pill);
  }
}

function prefsFromForm() {
  return {
    remember: document.getElementById("remember").checked,
    wechat_version: document.getElementById("wechatVersion").value.trim(),
    match_hongkong_keywords: document.getElementById("hkKeys").value.split(/[,，]/).map((s) => s.trim()).filter(Boolean),
    empty_region_tag: document.getElementById("emptyTag").value.trim() || "未填写地区",
    tag_prefix: document.getElementById("tagPrefix").value.trim(),
    scan_pause_seconds: Number(document.getElementById("scanPause").value || 0.35),
    max_tag_name_length: Number(document.getElementById("maxLen").value || 16),
    only_hk: document.getElementById("onlyHk").checked,
    scan_all: document.getElementById("scanAll").checked,
    scan_limit: Number(document.getElementById("scanLimit").value || 15),
    manager_window_name: "通讯录管理",
    click_pause_seconds: 0.25,
    calibrate: calState.data || {},
  };
}

function fillForm(p) {
  document.getElementById("remember").checked = p.remember !== false;
  document.getElementById("wechatVersion").value = p.wechat_version || "4.1.13.65";
  document.getElementById("hkKeys").value = (p.match_hongkong_keywords || []).join("，");
  document.getElementById("emptyTag").value = p.empty_region_tag || "未填写地区";
  document.getElementById("tagPrefix").value = p.tag_prefix || "";
  document.getElementById("scanPause").value = p.scan_pause_seconds ?? 0.35;
  document.getElementById("maxLen").value = p.max_tag_name_length ?? 16;
  document.getElementById("onlyHk").checked = !!p.only_hk;
  document.getElementById("scanAll").checked = !!p.scan_all;
  document.getElementById("scanLimit").value = p.scan_limit ?? 15;
  if (p.calibrate) {
    calState.data = p.calibrate;
    paintCalMarks();
  }
}

async function persistPrefs() {
  const body = prefsFromForm();
  if (body.remember) {
    localStorage.setItem(SLUG + ".prefs", JSON.stringify(body));
    await fetch("/api/prefs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  }
}

function paintStatus(st) {
  document.getElementById("stPlat").textContent = st.platform || "—";
  document.getElementById("stWin").textContent = st.found ? (st.title || "OK") : "—";
  document.getElementById("stCls").textContent = st.class_name || "—";
  windowReady = !!st.found;
  const chip = document.getElementById("winChip");
  chip.textContent = st.found ? (lang === "zh" ? "窗口已连接" : "Window ready") : (lang === "zh" ? "未找到窗口" : "No window");
  const hint = document.getElementById("s0hint");
  if (st.platform && st.platform !== "win32") hint.textContent = t("s0.linux");
  else if (!st.found) hint.textContent = t("s0.needwin");
  else hint.textContent = t("s0.ok");
}

function renderReview(data) {
  const counts = data.counts || {};
  document.getElementById("countRow").innerHTML = `
    <div class="stat"><span>Total</span><strong>${counts.total || 0}</strong></div>
    <div class="stat"><span>Hong Kong</span><strong>${counts.hongkong || 0}</strong></div>
    <div class="stat"><span>Tags</span><strong>${counts.tags || 0}</strong></div>`;
  const pb = document.querySelector("#planTable tbody");
  pb.innerHTML = "";
  (data.plan || []).forEach((p) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${escapeHtml(p.tag_name)}</td><td>${p.count}</td><td>${escapeHtml(p.sample || "")}</td>`;
    pb.appendChild(tr);
  });
  const rb = document.querySelector("#rowTable tbody");
  rb.innerHTML = "";
  (data.rows || data.rows_preview || []).forEach((r, i) => {
    const tr = document.createElement("tr");
    if (r.is_hongkong) tr.className = "hk";
    tr.innerHTML = `<td>${escapeHtml(r.nickname || "")}</td>
      <td>${escapeHtml(r.region_raw || "")}</td>
      <td><input data-i="${i}" class="tagEdit" value="${escapeHtml(r.tag_name || "")}" /></td>
      <td>${r.is_hongkong ? "Y" : ""}</td>`;
    rb.appendChild(tr);
  });
  window.__rows = data.rows || data.rows_preview || [];
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function setPackTarget(n) {
  packTarget = n;
}

function startPackTicker() {
  if (packTimer) return;
  packTimer = setInterval(() => {
    const gap = packTarget - packShown;
    if (gap <= 0.05) {
      packShown = packTarget;
    } else {
      packShown += Math.max(0.15, gap / 18);
    }
    document.getElementById("packBar").style.width = packShown + "%";
    document.getElementById("packPct").textContent = Math.round(packShown) + "%";
  }, 80);
}

function openOverlay(title) {
  document.getElementById("loading").hidden = false;
  document.getElementById("packTitle").textContent = title;
  document.getElementById("packStage").textContent = "…";
  document.getElementById("packLog").textContent = "";
  packShown = 0;
  packTarget = 8;
  startPackTicker();
}

function closeOverlay() {
  setPackTarget(100);
  setTimeout(() => {
    document.getElementById("loading").hidden = true;
    packShown = 0;
    packTarget = 0;
  }, 500);
}

function appendLog(line) {
  const box = document.getElementById("packLog");
  box.textContent += line + "\n";
  box.scrollTop = box.scrollHeight;
}

function listenJob(onDone) {
  const es = new EventSource("/api/job/events");
  const handle = (ev) => {
    let data = {};
    try { data = JSON.parse(ev.data || "{}"); } catch {}
    if (data.message) {
      document.getElementById("packStage").textContent = data.message;
      appendLog(data.message);
    }
    if (ev.type === "log") setPackTarget(Math.min(82, packTarget + 2));
    if (ev.type === "row") setPackTarget(Math.min(82, packTarget + 1));
    if (ev.type === "done") {
      setPackTarget(100);
      es.close();
      onDone && onDone(data);
      closeOverlay();
    }
    if (ev.type === "error") {
      appendLog("ERROR " + (data.message || ""));
      es.close();
      closeOverlay();
    }
  };
  ["log", "row", "done", "error"].forEach((name) => es.addEventListener(name, handle));
}

async function boot() {
  lang = detectUiLang();
  applyI18n();
  const res = await fetch("/api/defaults");
  defaults = await res.json();
  document.querySelector(".app-version").textContent = "v" + (defaults.version || "1.0.0");
  const local = localStorage.getItem(SLUG + ".prefs");
  fillForm(local ? { ...defaults.prefs, ...JSON.parse(local) } : defaults.prefs);
  paintStatus(defaults.status || {});
  if (defaults.rows_total) {
    const c = await fetch("/api/contacts").then((r) => r.json());
    renderReview(c);
  }
}

document.getElementById("langZh").onclick = () => {
  lang = "zh";
  localStorage.setItem("aio.uiLang", "zh");
  applyI18n();
};
document.getElementById("langEn").onclick = () => {
  lang = "en";
  localStorage.setItem("aio.uiLang", "en");
  applyI18n();
};

document.getElementById("btnRefresh").onclick = async () => {
  const st = await fetch("/api/status").then((r) => r.json());
  paintStatus(st);
};

document.getElementById("btnNext0").onclick = async () => {
  const st = await fetch("/api/status").then((r) => r.json());
  paintStatus(st);
  if (!st.found && st.platform === "win32") return;
  persistPrefs();
  goStep(1);
};

document.getElementById("btnNext1").onclick = () => {
  persistPrefs();
  goStep(2);
};

document.getElementById("btnInspect").onclick = async () => {
  const box = document.getElementById("treeBox");
  box.textContent = "…";
  const res = await fetch("/api/inspect", { method: "POST" });
  if (!res.ok) {
    box.textContent = await res.text();
    return;
  }
  const data = await res.json();
  box.textContent = data.tree || "";
  const hint = document.getElementById("probeHint");
  if (hint) {
    hint.textContent = (data.tree || "").includes("DIAGNOSIS")
      ? (lang === "zh" ? "探测完成：自绘层属正常，请点右下角下一步。" : "Probe complete. The paint surface is expected. Click Next.")
      : (lang === "zh" ? "探测完成，请点下一步。" : "Probe complete. Click Next.");
  }
};

document.getElementById("btnNext2").onclick = () => goStep(3);

document.getElementById("btnScan").onclick = async () => {
  await persistPrefs();
  const limit = Number(document.getElementById("scanLimit").value || 15);
  const scanAll = document.getElementById("scanAll").checked;
  openOverlay(lang === "zh" ? "正在扫描" : "Scanning");
  setPackTarget(16);
  const res = await fetch("/api/scan/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      scan_limit: limit,
      scan_all: scanAll,
      calibrate: calState.data || {},
    }),
  });
  if (!res.ok) {
    appendLog(await res.text());
    closeOverlay();
    return;
  }
  listenJob(async () => {
    const c = await fetch("/api/contacts").then((r) => r.json());
    renderReview(c);
    goStep(5);
  });
};

document.getElementById("btnSaveRows").onclick = async () => {
  const rows = (window.__rows || []).map((r, i) => {
    const inp = document.querySelector(`.tagEdit[data-i="${i}"]`);
    return { ...r, tag_name: inp ? inp.value.trim() : r.tag_name };
  });
  const res = await fetch("/api/contacts/save", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ rows }),
  });
  const data = await res.json();
  const c = await fetch("/api/contacts").then((r) => r.json());
  renderReview(c);
  document.getElementById("applyHint").textContent = JSON.stringify(data.counts || {});
};

document.getElementById("btnNext4").onclick = () => {
  const counts = (defaults.counts) || {};
  document.getElementById("applyHint").textContent =
    lang === "zh"
      ? "写入前请确认 Excel / 表格中的 tag_name。"
      : "Confirm tag_name values before writing.";
  goStep(6);
};

document.getElementById("btnApply").onclick = async () => {
  await persistPrefs();
  openOverlay(lang === "zh" ? "正在打标" : "Tagging");
  setPackTarget(24);
  const res = await fetch("/api/apply/start", { method: "POST" });
  if (!res.ok) {
    appendLog(await res.text());
    closeOverlay();
    return;
  }
  listenJob((data) => {
    const box = document.getElementById("applyResult");
    box.hidden = false;
    box.textContent = `OK=${data.ok ?? ""}  MISS=${data.miss ?? ""}`;
  });
};

document.getElementById("btnStop").onclick = () => fetch("/api/job/stop", { method: "POST" });

document.querySelectorAll("[data-back]").forEach((btn) => {
  btn.addEventListener("click", () => goStep(Number(btn.getAttribute("data-back"))));
});

const CAL_KEYS = {
  search: ["search_ix", "search_iy", "search_x", "search_y", "S"],
  check: ["check_ix", "check_iy", "check_x", "check_y", "C"],
  avatar: ["avatar_ix", "avatar_iy", "avatar_x", "avatar_y", "A"],
  row2: ["row2_ix", "row2_iy", "row2_x", "row2_y", "2"],
};

function imgScale() {
  const img = document.getElementById("calImg");
  const iw = img.naturalWidth || calState.snap.image_width || calState.snap.width;
  const ih = img.naturalHeight || calState.snap.image_height || calState.snap.height;
  return {
    wr: img.clientWidth / Math.max(1, iw),
    hr: img.clientHeight / Math.max(1, ih),
    iw, ih,
  };
}

function paintCalMarks() {
  const box = document.getElementById("calMarks");
  const img = document.getElementById("calImg");
  if (!box || !img || !calState.snap) {
    if (box) box.innerHTML = "";
    return;
  }
  box.innerHTML = "";
  const { wr, hr } = imgScale();
  const cand = {};
  Object.entries(CAL_KEYS).forEach(([, [ixk, iyk, , , label]]) => {
    const ix = calState.data[ixk];
    const iy = calState.data[iyk];
    if (ix == null || iy == null) return;
    const mark = document.createElement("div");
    mark.className = "cal-mark";
    mark.textContent = label;
    mark.style.left = ix * wr + "px";
    mark.style.top = iy * hr + "px";
    box.appendChild(mark);
  });
}

function setCalHint(extra) {
  const hint = document.getElementById("calHint");
  if (!hint) return;
  const d = calState.data;
  const have = ["search_ix", "check_ix", "avatar_ix", "row2_iy"].filter((k) => d[k] != null).length;
  const base = lang === "zh"
    ? `已标 ${have}/4。试点击与扫描使用同一组屏幕坐标。当前：${t("sc." + (calState.mode === "row2" ? "row2" : calState.mode))}`
    : `Marked ${have}/4. Test and scan use the same screen pixels. Mode: ${calState.mode}`;
  hint.textContent = extra ? extra + " " + base : base;
}

function clearMode(mode) {
  const keys = CAL_KEYS[mode];
  keys.slice(0, 4).forEach((k) => { delete calState.data[k]; });
}

document.querySelectorAll("#calModes [data-mode]").forEach((btn) => {
  btn.addEventListener("click", () => {
    calState.mode = btn.getAttribute("data-mode");
    document.querySelectorAll("#calModes [data-mode]").forEach((b) => b.classList.toggle("on", b === btn));
    setCalHint();
  });
});

document.getElementById("btnSnap").onclick = async () => {
  const hint = document.getElementById("calHint");
  hint.textContent = lang === "zh" ? "正在截图…" : "Capturing…";
  const res = await fetch("/api/calibrate/snapshot", { method: "POST" });
  if (!res.ok) {
    hint.textContent = await res.text();
    return;
  }
  const info = await res.json();
  calState.snap = info;
  calState.candidates = info.candidates || {};
  calState.data.origin_left = info.left;
  calState.data.origin_top = info.top;
  calState.data.origin_right = info.right;
  calState.data.origin_bottom = info.bottom;
  calState.data.image_width = info.image_width;
  calState.data.image_height = info.image_height;
  calState.data.mode = info.mode || "window";
  const had = calState.data.avatar_ix != null && calState.data.search_ix != null;
  if (had) {
    ["search", "check", "avatar", "row2"].forEach((mode) => {
      const [ixk, iyk, sxk, syk] = CAL_KEYS[mode];
      if (calState.data[ixk] == null) return;
      const ratioX = (info.right - info.left) / Math.max(1, info.image_width);
      const ratioY = (info.bottom - info.top) / Math.max(1, info.image_height);
      calState.data[sxk] = Math.round(info.left + calState.data[ixk] * ratioX);
      calState.data[syk] = Math.round(info.top + calState.data[iyk] * ratioY);
    });
  } else {
    applyAutoMarks(info.auto_marks || {});
  }
  persistPrefs();
  const img = document.getElementById("calImg");
  img.onload = () => paintCalMarks();
  img.src = info.url;
  setCalHint(had
    ? (lang === "zh" ? "已加载您保存的校点，未覆盖自动检测。" : "Restored saved marks.")
    : (lang === "zh" ? "无存档，已放入自动检测点，请改到正中后保存。" : "No archive, auto marks applied."));
};

function applyAutoMarks(marks) {
  const map = { search: "search", check: "check", avatar: "avatar", row2: "row2" };
  Object.entries(map).forEach(([mode, key]) => {
    const hit = marks[key];
    if (!hit) return;
    const [ixk, iyk, sxk, syk] = CAL_KEYS[mode];
    calState.data[ixk] = hit.x;
    calState.data[iyk] = hit.y;
    if (calState.snap) {
      const ratioX = (calState.snap.right - calState.snap.left) / Math.max(1, calState.snap.image_width);
      const ratioY = (calState.snap.bottom - calState.snap.top) / Math.max(1, calState.snap.image_height);
      calState.data[sxk] = Math.round(calState.snap.left + hit.x * ratioX);
      calState.data[syk] = Math.round(calState.snap.top + hit.y * ratioY);
    }
  });
  persistPrefs();
}

function nudge(dx, dy) {
  const [ixk, iyk, sxk, syk] = CAL_KEYS[calState.mode];
  if (calState.data[ixk] == null) return;
  calState.data[ixk] += dx;
  calState.data[iyk] += dy;
  if (calState.data[sxk] != null) {
    calState.data[sxk] += dx;
    calState.data[syk] += dy;
  }
  paintCalMarks();
  persistPrefs();
}

document.getElementById("calImg").onclick = async (ev) => {
  if (!calState.snap) {
    document.getElementById("calHint").textContent = lang === "zh" ? "请先拍摄窗口" : "Capture the window first";
    return;
  }
  const img = ev.currentTarget;
  const r = img.getBoundingClientRect();
  const { iw, ih } = imgScale();
  const ix = Math.round((ev.clientX - r.left) / Math.max(1, r.width) * iw);
  const iy = Math.round((ev.clientY - r.top) / Math.max(1, r.height) * ih);
  const [ixk, iyk, sxk, syk] = CAL_KEYS[calState.mode];
  const autoOn = document.getElementById("autoAlign") ? document.getElementById("autoAlign").checked : false;
  if (!autoOn) {
    calState.data[ixk] = ix;
    calState.data[iyk] = iy;
    const ratioX = (calState.snap.right - calState.snap.left) / Math.max(1, calState.snap.image_width);
    const ratioY = (calState.snap.bottom - calState.snap.top) / Math.max(1, calState.snap.image_height);
    calState.data[sxk] = Math.round(calState.snap.left + ix * ratioX);
    calState.data[syk] = Math.round(calState.snap.top + iy * ratioY);
    paintCalMarks();
    setCalHint(lang === "zh" ? "已使用手动位置。" : "Manual point set.");
    persistPrefs();
    return;
  }
  const res = await fetch("/api/calibrate/snap-point", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ mode: calState.mode, img_x: ix, img_y: iy }),
  });
  if (res.ok) {
    const hit = await res.json();
    calState.candidates = hit.candidates || calState.candidates;
    calState.data[ixk] = hit.img_x;
    calState.data[iyk] = hit.img_y;
    calState.data[sxk] = hit.screen_x;
    calState.data[syk] = hit.screen_y;
    setCalHint(hit.snapped
      ? (lang === "zh" ? "已吸附到元素中心。" : "Snapped to element center.")
      : (lang === "zh" ? "附近没有识别框，使用点击位置。" : "No box nearby, raw click used."));
  } else {
    calState.data[ixk] = ix;
    calState.data[iyk] = iy;
    setCalHint();
  }
  paintCalMarks();
  persistPrefs();
};

document.getElementById("btnUseAuto").onclick = () => {
  if (!calState.snap) return;
  ["search", "check", "avatar", "row2"].forEach(clearMode);
  applyAutoMarks(calState.snap.auto_marks || {});
  paintCalMarks();
  persistPrefs();
  setCalHint(lang === "zh" ? "已套用自动检测点。" : "Auto marks applied.");
};
document.getElementById("btnSaveCal").onclick = () => {
  persistPrefs();
  setCalHint(lang === "zh" ? "校点已写入本地存档，下次拍摄会沿用。" : "Marks saved.");
};

document.getElementById("btnClearOne").onclick = () => {
  clearMode(calState.mode);
  paintCalMarks();
  setCalHint(lang === "zh" ? "已清除当前点。" : "Cleared.");
  persistPrefs();
};

document.getElementById("btnClearAll").onclick = () => {
  Object.keys(CAL_KEYS).forEach(clearMode);
  paintCalMarks();
  setCalHint(lang === "zh" ? "已清除全部标记。" : "All marks cleared.");
  persistPrefs();
};

["btnNudgeL", "btnNudgeR", "btnNudgeU", "btnNudgeD"].forEach((id) => {
  const el = document.getElementById(id);
  if (!el) return;
  el.onclick = () => {
    if (id.endsWith("L")) nudge(-1, 0);
    if (id.endsWith("R")) nudge(1, 0);
    if (id.endsWith("U")) nudge(0, -1);
    if (id.endsWith("D")) nudge(0, 1);
  };
});

document.getElementById("btnTestClick").onclick = async () => {
  const [, , sxk, syk] = CAL_KEYS[calState.mode];
  const x = calState.data[sxk];
  const y = calState.data[syk];
  if (x == null) {
    document.getElementById("calHint").textContent = lang === "zh" ? "请先在图上点这个位置" : "Mark this point first";
    return;
  }
  await fetch("/api/calibrate/test-click", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ x, y }),
  });
};

document.getElementById("btnNextCal").onclick = () => {
  const d = calState.data;
  if (d.avatar_ix == null || d.check_ix == null || d.search_ix == null || d.row2_iy == null) {
    document.getElementById("calHint").textContent = lang === "zh"
      ? "四个点都点完才能进入扫描。"
      : "Mark all four points before scanning.";
    return;
  }
  persistPrefs();
  goStep(4);
};

boot();
void AXIOXMEDIA_BRAND;
void AIO_WATERMARK;
