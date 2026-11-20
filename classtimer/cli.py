"""命令行入口：生成课堂倒计时页面。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from .timer import TimerError, parse_presets, render_page


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="classtimer",
        description="课堂倒计时：生成可全屏使用、带预设时间的单文件页面",
    )
    parser.add_argument("--version", action="version", version="classtimer 0.1.0")
    parser.add_argument(
        "-o", "--output", default="timer.html", help="输出 HTML 路径"
    )
    parser.add_argument("--title", default="课堂计时", help="页面标题")
    parser.add_argument(
        "--presets",
        default="1,3,5,10",
        help="预设分钟数，逗号分隔，例如 1,3,5,10",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        presets = parse_presets(args.presets)
        page = render_page(args.title, presets)
    except TimerError as exc:
        print("错误: %s" % exc, file=sys.stderr)
        return 2

    try:
        Path(args.output).write_text(page, encoding="utf-8")
    except OSError as exc:
        print("错误: 写入文件失败: %s" % exc, file=sys.stderr)
        return 1

    print(
        "已生成 %s：预设 %s 分钟"
        % (args.output, "、".join(str(item) for item in presets))
    )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
