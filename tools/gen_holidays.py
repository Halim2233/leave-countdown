"""한국 공휴일(대체공휴일 포함) 목록을 docs/holidays.json 으로 생성한다.

사용법: python tools/gen_holidays.py [시작연도] [끝연도]
의존성: pip install holidays  (실행 시에만 필요, 앱 자체는 JSON만 읽음)
주의: 임시공휴일·선거일은 라이브러리에 없을 수 있으니 발표되면 JSON에 직접 추가할 것.
"""
import json
import sys
from pathlib import Path

import holidays

y0 = int(sys.argv[1]) if len(sys.argv) > 1 else 2025
y1 = int(sys.argv[2]) if len(sys.argv) > 2 else 2030

out = {}
for y in range(y0, y1 + 1):
    for d, name in sorted(holidays.country_holidays("KR", years=y, language="ko").items()):
        out[d.isoformat()] = name

path = Path(__file__).resolve().parent.parent / "docs" / "holidays.json"
path.write_text(json.dumps(out, ensure_ascii=False, indent=0), encoding="utf-8")
print(f"{len(out)}개 -> {path}")
