#!/usr/bin/env python3
from pathlib import Path

INDEX = Path('index.html')
START = '<span class="life-subhead rv">Training log</span>'
END = '<p class="lead rv">Colorado turned out to be the other half of the job.'
SCRIPT = '<script src="assets/js/whoop-dashboard.js"></script>'

WHOOP_BLOCK = '''<span class="life-subhead rv">Training log</span><div id="whoop-week" class="rv" style="margin:16px 0 34px;padding:18px 20px;border-radius:24px;background:var(--card);border:1px solid var(--line);box-shadow:0 8px 24px rgba(36,29,46,.04)"><div style="display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap"><div style="min-width:160px"><span style="font-family:var(--mono);font-size:9px;letter-spacing:.1em;text-transform:uppercase;color:var(--dim)">WHOOP · this week</span><div style="display:flex;align-items:baseline;gap:7px;margin-top:4px"><span id="whoop-strain" style="font-family:var(--display);font-size:32px;font-weight:700;line-height:1">—</span><span style="font-family:var(--mono);font-size:9px;text-transform:uppercase;color:var(--dim)">avg strain</span></div></div><div style="flex:1;min-width:220px"><div style="height:12px;border-radius:999px;background:rgba(36,29,46,.08);overflow:hidden"><div id="whoop-strain-fill" style="height:100%;width:0;border-radius:999px;background:linear-gradient(90deg,var(--mint),var(--yellow),var(--peach));transition:width .6s ease"></div></div><div style="display:flex;justify-content:space-between;margin-top:6px;font-family:var(--mono);font-size:8px;color:rgba(36,29,46,.45)"><span>0</span><span>strain · 21</span></div></div><div style="display:flex;align-items:center;gap:22px;flex-wrap:wrap"><div><div id="whoop-time" style="font-family:var(--display);font-size:22px;font-weight:700;line-height:1">—</div><div style="font-family:var(--mono);font-size:8.5px;text-transform:uppercase;color:var(--dim);margin-top:5px">training time</div></div><div><div style="display:flex;align-items:baseline;gap:3px"><span id="whoop-peak" style="font-family:var(--display);font-size:22px;font-weight:700;line-height:1">—</span><span style="font-family:var(--mono);font-size:8px;color:var(--dim)">bpm</span></div><div style="font-family:var(--mono);font-size:8.5px;text-transform:uppercase;color:var(--dim);margin-top:5px">peak HR</div></div></div></div><div style="display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;margin-top:13px;padding-top:12px;border-top:1px solid var(--line)"><span id="whoop-activities" style="font-size:12.5px;color:var(--dim)">loading training…</span><span id="whoop-updated" style="font-family:var(--mono);font-size:8.5px;text-transform:uppercase;color:rgba(36,29,46,.45)">loading WHOOP…</span></div></div>'''


def main():
    text = INDEX.read_text(encoding='utf-8')
    start = text.find(START)
    end = text.find(END, start)
    if start < 0 or end < 0:
        raise SystemExit('Could not find the Training log block safely.')

    current = text[start:end]
    changed = False
    if current != WHOOP_BLOCK:
        text = text[:start] + WHOOP_BLOCK + text[end:]
        changed = True

    if SCRIPT not in text:
        text = text.replace('</body>', SCRIPT + '\n</body>')
        changed = True

    if changed:
        INDEX.write_text(text, encoding='utf-8')
        print('Updated WHOOP dashboard markup on homepage.')
    else:
        print('WHOOP dashboard already current.')


if __name__ == '__main__':
    main()
