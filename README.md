# 퇴근 카운트다운

퇴근까지 남은 시간을 실시간으로 보여주는 미니 프로젝트입니다. 터미널(CLI) 버전과 웹 버전이 있습니다.

**웹 버전**: https://halim2233.github.io/leave-countdown/

## 기능
- 퇴근까지(출근 전이면 출근까지) 남은 시간 `HH:MM:SS`
- 근무 진행률 바
- 점심까지 남은 시간, 이번 주 금요일까지 남은 일수
- 남은 시간에 따라 색과 멘트가 바뀜
- 평일/주말 구분 (공휴일은 반영하지 않음)

## CLI 버전 (Python)
```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt   # macOS/Linux: .venv/bin/pip
.venv/Scripts/python leave.py                    # 기본 09:00 ~ 18:00
.venv/Scripts/python leave.py --start 08:30 --end 17:30 --lunch 11:30-12:30
```
종료는 `Ctrl+C`. 점심 표시를 끄려면 `--lunch none`.

## 웹 버전
`docs/index.html` 한 파일로 동작하며 GitHub Pages로 배포됩니다. 시간 설정은 브라우저에 저장됩니다.
