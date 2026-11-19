"""퇴근 카운트다운 CLI.

사용법:
    python leave.py                       # 기본 09:00 ~ 18:00
    python leave.py --start 08:30 --end 17:30
    python leave.py --lunch 12:00-13:00   # 점심시간 표시(진행률 계산에는 포함)
종료: Ctrl+C
"""
from __future__ import annotations

import argparse
import time
from datetime import datetime, timedelta

from rich.align import Align
from rich.console import Group
from rich.live import Live
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from rich.table import Table
from rich.text import Text

WEEKDAYS = "월화수목금토일"


def parse_hm(s: str) -> tuple[int, int]:
    h, m = s.split(":")
    return int(h), int(m)


def at(now: datetime, hm: tuple[int, int]) -> datetime:
    return now.replace(hour=hm[0], minute=hm[1], second=0, microsecond=0)


def fmt_delta(td: timedelta) -> str:
    total = max(int(td.total_seconds()), 0)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def mood(remaining: timedelta, working: bool) -> tuple[str, str]:
    """(색, 한마디)"""
    if not working:
        return "cyan", "근무 시간이 아닙니다 🎉"
    mins = remaining.total_seconds() / 60
    if mins <= 10:
        return "bold green", "가방 챙기세요 🎒"
    if mins <= 60:
        return "green", "거의 다 왔다, 마지막 한 시간 🔥"
    if mins <= 180:
        return "yellow", "조금만 더 버텨요 ☕"
    return "red", "아직 멀었다... 😇"


def days_to_weekend(now: datetime) -> int:
    """이번 주 마지막 근무일(금)까지 남은 일수. 토/일이면 0."""
    wd = now.weekday()
    return max(4 - wd, 0) if wd < 5 else 0


def render(now: datetime, start, end, lunch) -> Panel:
    s, e = at(now, start), at(now, end)
    is_workday = now.weekday() < 5
    working = is_workday and s <= now < e

    if working:
        total = (e - s).total_seconds()
        done = (now - s).total_seconds()
        pct = done / total
        remaining = e - now
    elif is_workday and now < s:
        pct, remaining = 0.0, s - now
    else:
        pct, remaining = 1.0, timedelta(0)

    color, msg = mood(remaining, working)

    title = Text(f"{now:%Y-%m-%d} ({WEEKDAYS[now.weekday()]}) {now:%H:%M:%S}", style="dim")
    if working:
        big = Text(fmt_delta(remaining), style=f"bold {color}", justify="center")
        caption = Text("퇴근까지", style="dim", justify="center")
    elif is_workday and now < s:
        big = Text(fmt_delta(remaining), style="bold cyan", justify="center")
        caption = Text("출근까지", style="dim", justify="center")
    elif not is_workday:
        big = Text("주말입니다", style="bold cyan", justify="center")
        caption = Text("", justify="center")
    else:
        big = Text("퇴근 완료", style="bold cyan", justify="center")
        caption = Text("", justify="center")

    bar = ProgressBar(total=100, completed=round(pct * 100), width=40,
                      complete_style=color.replace("bold ", ""), finished_style="cyan")

    info = Table.grid(padding=(0, 2))
    info.add_column(justify="right", style="dim")
    info.add_column()
    info.add_row("진행률", f"{pct * 100:5.1f}%")
    info.add_row("근무시간", f"{start[0]:02d}:{start[1]:02d} ~ {end[0]:02d}:{end[1]:02d}")
    if lunch:
        ls, le = at(now, lunch[0]), at(now, lunch[1])
        if now < ls and working:
            info.add_row("점심까지", fmt_delta(ls - now))
        elif ls <= now < le and working:
            info.add_row("점심", "지금 먹는 중 🍚")
        else:
            info.add_row("점심", "끝남" if now >= le else "-")
    d = days_to_weekend(now)
    info.add_row("주말까지", "오늘이 금요일! 🎊" if (is_workday and d == 0) else (f"{d}일" if is_workday else "주말 🛋️"))

    body = Group(
        Align.center(title), Text(),
        Align.center(caption), Align.center(big), Text(),
        Align.center(bar), Text(),
        Align.center(info), Text(),
        Align.center(Text(msg, style=color)),
    )
    return Panel(body, title="퇴근 카운트다운", border_style=color.replace("bold ", ""), padding=(1, 4))


def main() -> None:
    ap = argparse.ArgumentParser(description="퇴근 카운트다운")
    ap.add_argument("--start", default="09:00", help="출근 시각 HH:MM")
    ap.add_argument("--end", default="18:00", help="퇴근 시각 HH:MM")
    ap.add_argument("--lunch", default="12:00-13:00", help="점심시간 HH:MM-HH:MM, 끄려면 none")
    a = ap.parse_args()

    start, end = parse_hm(a.start), parse_hm(a.end)
    lunch = None
    if a.lunch.lower() != "none":
        l1, l2 = a.lunch.split("-")
        lunch = (parse_hm(l1), parse_hm(l2))

    try:
        with Live(render(datetime.now(), start, end, lunch), refresh_per_second=4, screen=True) as live:
            while True:
                live.update(render(datetime.now(), start, end, lunch))
                time.sleep(0.25)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
