"""课堂倒计时页面的生成。"""

from __future__ import annotations

import html
import json
import re
from typing import List, Sequence, Tuple

SEPARATOR = re.compile(r"[,，、;；\s]+")
MAX_PRESETS = 9
MAX_MINUTES = 180

PAGE_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(circle at 50% 0%, #1f3a5f 0%, #0d1b2a 55%, #070d14 100%);
    color: #f1f5f9;
    font-family: "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
    transition: background 0.3s;
  }
  body.done { background: radial-gradient(circle at 50% 0%, #7f1d1d 0%, #450a0a 60%, #1a0505 100%); }
  main { width: min(92vw, 880px); text-align: center; padding: 24px 16px; }
  h1 { font-size: clamp(18px, 3vw, 26px); font-weight: 600; margin: 0 0 6px; letter-spacing: 1px; }
  .hint { color: #94a3b8; font-size: 14px; margin: 0 0 18px; }
  .display {
    font-family: "SF Mono", "Menlo", "Consolas", monospace;
    font-size: clamp(88px, 20vw, 200px);
    font-weight: 700;
    line-height: 1;
    letter-spacing: 4px;
    font-variant-numeric: tabular-nums;
    margin: 8px 0 10px;
    text-shadow: 0 0 40px rgba(56, 189, 248, 0.25);
  }
  body.done .display { color: #fca5a5; animation: pulse 0.8s infinite alternate; }
  @keyframes pulse { from { opacity: 1; } to { opacity: 0.55; } }
  .status { min-height: 24px; color: #7dd3fc; font-size: 16px; margin-bottom: 18px; }
  body.done .status { color: #fca5a5; font-weight: 600; }
  .presets { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-bottom: 18px; }
  .presets button {
    background: rgba(148, 163, 184, 0.14);
    color: #e2e8f0;
    border: 1px solid rgba(148, 163, 184, 0.35);
    border-radius: 10px;
    padding: 10px 16px;
    font-size: 15px;
    cursor: pointer;
  }
  .presets button:hover { background: rgba(56, 189, 248, 0.2); border-color: #38bdf8; }
  .presets button.active { background: #0284c7; border-color: #38bdf8; color: #fff; }
  .controls { display: flex; gap: 12px; justify-content: center; }
  .controls button {
    min-width: 130px;
    padding: 14px 22px;
    border-radius: 12px;
    border: none;
    font-size: 17px;
    font-weight: 600;
    cursor: pointer;
  }
  #toggle { background: #0ea5e9; color: #fff; }
  #toggle:hover { background: #38bdf8; }
  #reset { background: rgba(148, 163, 184, 0.18); color: #e2e8f0; border: 1px solid rgba(148, 163, 184, 0.35); }
  #reset:hover { background: rgba(148, 163, 184, 0.3); }
  @media (max-width: 480px) {
    .controls button { min-width: 0; flex: 1; padding: 12px; }
  }
</style>
</head>
<body>
<main>
  <h1>__TITLE__</h1>
  <p class="hint">点击预设时间，按空格开始或暂停，按 R 重置</p>
  <div class="display" id="display">05:00</div>
  <div class="status" id="status">准备开始</div>
  <div class="presets" id="presets">__PRESET_BUTTONS__</div>
  <div class="controls">
    <button id="toggle" type="button">开始</button>
    <button id="reset" type="button">重置</button>
  </div>
</main>
<script>
(function () {
  "use strict";
  var PRESETS = __PRESETS_JSON__;
  var display = document.getElementById("display");
  var status = document.getElementById("status");
  var toggle = document.getElementById("toggle");
  var resetButton = document.getElementById("reset");
  var presetBox = document.getElementById("presets");
  var buttons = Array.prototype.slice.call(presetBox.querySelectorAll("button"));
  var totalMs = PRESETS[0] * 1000;
  var remainingMs = totalMs;
  var endTime = 0;
  var running = false;
  var timerId = null;

  function pad(value) {
    return value < 10 ? "0" + value : String(value);
  }

  function render() {
    var seconds = Math.ceil(remainingMs / 1000);
    var minutes = Math.floor(seconds / 60);
    var rest = seconds % 60;
    display.textContent = pad(minutes) + ":" + pad(rest);
  }

  function markActive(seconds) {
    buttons.forEach(function (button) {
      button.classList.toggle(
        "active", Number(button.getAttribute("data-seconds")) === seconds
      );
    });
  }

  function stopTicker() {
    if (timerId !== null) {
      clearInterval(timerId);
      timerId = null;
    }
  }

  function setPreset(seconds) {
    stopTicker();
    document.body.classList.remove("done");
    running = false;
    totalMs = seconds * 1000;
    remainingMs = totalMs;
    toggle.textContent = "开始";
    status.textContent = "准备开始";
    markActive(seconds);
    render();
  }

  function beep() {
    try {
      var Context = window.AudioContext || window.webkitAudioContext;
      if (!Context) { return; }
      var context = new Context();
      [0, 0.35, 0.7].forEach(function (offset) {
        var oscillator = context.createOscillator();
        var gain = context.createGain();
        oscillator.type = "sine";
        oscillator.frequency.value = 880;
        gain.gain.value = 0.22;
        oscillator.connect(gain);
        gain.connect(context.destination);
        oscillator.start(context.currentTime + offset);
        oscillator.stop(context.currentTime + offset + 0.18);
      });
    } catch (error) {
      /* 音频不可用时静默处理，不影响计时 */
    }
  }

  function finish() {
    stopTicker();
    running = false;
    remainingMs = 0;
    render();
    document.body.classList.add("done");
    status.textContent = "时间到";
    toggle.textContent = "开始";
    beep();
  }

  function tick() {
    remainingMs = Math.max(0, endTime - Date.now());
    render();
    if (remainingMs <= 0) {
      finish();
    }
  }

  function start() {
    if (running) { return; }
    if (remainingMs <= 0) {
      remainingMs = totalMs;
    }
    document.body.classList.remove("done");
    running = true;
    endTime = Date.now() + remainingMs;
    toggle.textContent = "暂停";
    status.textContent = "计时中";
    timerId = setInterval(tick, 200);
    tick();
  }

  function pause() {
    if (!running) { return; }
    remainingMs = Math.max(0, endTime - Date.now());
    stopTicker();
    running = false;
    toggle.textContent = "继续";
    status.textContent = "已暂停";
    render();
  }

  function toggleTimer() {
    if (running) { pause(); } else { start(); }
  }

  function reset() {
    stopTicker();
    running = false;
    document.body.classList.remove("done");
    remainingMs = totalMs;
    toggle.textContent = "开始";
    status.textContent = "已重置";
    render();
  }

  buttons.forEach(function (button) {
    button.addEventListener("click", function () {
      setPreset(Number(button.getAttribute("data-seconds")));
    });
  });
  toggle.addEventListener("click", toggleTimer);
  resetButton.addEventListener("click", reset);

  document.addEventListener("keydown", function (event) {
    if (event.code === "Space") {
      event.preventDefault();
      toggleTimer();
    } else if (event.key === "r" || event.key === "R") {
      reset();
    } else if (/^[1-9]$/.test(event.key)) {
      var index = Number(event.key) - 1;
      if (index < PRESETS.length) {
        setPreset(PRESETS[index]);
      }
    }
  });

  markActive(PRESETS[0]);
  render();
})();
</script>
</body>
</html>
"""


class TimerError(ValueError):
    """预设时间不合法。"""


def parse_presets(text: str) -> Tuple[int, ...]:
    """把「1,3,5,10」解析成分钟列表。"""
    values: List[int] = []
    seen = set()
    for part in SEPARATOR.split(text.strip()):
        if not part:
            continue
        try:
            minutes = int(part)
        except ValueError:
            raise TimerError("预设时间不是整数: %s" % part) from None
        if minutes <= 0:
            raise TimerError("预设时间必须大于 0 分钟")
        if minutes > MAX_MINUTES:
            raise TimerError("单个预设不能超过 %d 分钟" % MAX_MINUTES)
        if minutes not in seen:
            seen.add(minutes)
            values.append(minutes)
    if not values:
        raise TimerError("至少需要一个预设时间")
    if len(values) > MAX_PRESETS:
        raise TimerError("最多支持 %d 个预设" % MAX_PRESETS)
    return tuple(values)


def render_page(title: str = "课堂计时", presets: Sequence[int] = (1, 3, 5, 10)) -> str:
    """生成单文件倒计时页面。"""
    if not title.strip():
        raise TimerError("页面标题不能为空")
    values = [int(item) for item in presets]
    if not values or any(item <= 0 for item in values):
        raise TimerError("预设时间必须是正整数")
    buttons = "".join(
        '<button type="button" data-seconds="%d">%d 分钟</button>'
        % (minutes * 60, minutes)
        for minutes in values
    )
    return (
        PAGE_TEMPLATE.replace("__TITLE__", html.escape(title))
        .replace("__PRESET_BUTTONS__", buttons)
        .replace("__PRESETS_JSON__", json.dumps([item * 60 for item in values]))
    )


__all__ = ["MAX_PRESETS", "TimerError", "parse_presets", "render_page"]
