# 퇴근 카운트다운

퇴근까지 남은 시간을 실시간으로 보여주는 미니 프로젝트입니다. 터미널(CLI) 버전과 웹 버전이 있습니다.

**웹 버전**: https://halim2233.github.io/leave-countdown/

## 기능
- 퇴근까지(출근 전이면 출근까지) 남은 시간 `HH:MM:SS`
- 근무 진행률 바
- 점심까지 남은 시간, 이번 주 금요일까지 남은 일수
- 남은 시간에 따라 색과 멘트가 바뀜
- 한국 공휴일(대체공휴일 포함) 반영, 다음 공휴일 D-day
- 월급날 D-day (기본 매월 25일, 주말·공휴일이면 직전 근무일로 당김)

## CLI 버전 (Python)
```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt   # macOS/Linux: .venv/bin/pip
.venv/Scripts/python leave.py                    # 기본 09:00 ~ 18:00
.venv/Scripts/python leave.py --start 08:30 --end 17:30 --lunch 11:30-12:30 --payday 10
```
종료는 `Ctrl+C`. 점심 표시를 끄려면 `--lunch none`.

## 웹 버전
`docs/index.html` 한 파일로 동작하며 GitHub Pages로 배포됩니다. 시간 설정은 브라우저에 저장됩니다.

## 공휴일 데이터
`docs/holidays.json`(2025~2030)을 CLI와 웹이 함께 씁니다. 갱신하려면:
```bash
pip install holidays
python tools/gen_holidays.py 2025 2032
```
임시공휴일·선거일은 라이브러리에 없을 수 있으니 발표되면 JSON에 `"YYYY-MM-DD": "이름"`으로 직접 추가하세요.
