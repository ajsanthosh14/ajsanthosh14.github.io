#!/usr/bin/env python3
from pathlib import Path

INDEX = Path('index.html')
START = '<span class="life-subhead rv">Training log</span>'
END = '<p class="lead rv">Colorado turned out to be the other half of the job.'
SCRIPT = '<script src="assets/js/whoop-dashboard.js"></script>'

WHOOP_BLOCK = '''<span class="life-subhead rv">Training log</span><style>
#whoop-week{margin:16px 0 34px;border-radius:24px;overflow:hidden;background:linear-gradient(180deg,#1b232b,#182027);color:#f4f7fa;box-shadow:0 18px 45px rgba(26,31,38,.16);border:1px solid rgba(255,255,255,.04)}
.whoop-main{min-height:230px;display:grid;grid-template-columns:220px 1fr 170px 170px;gap:28px;align-items:center;padding:28px 32px 24px}.whoop-brand{align-self:stretch;display:flex;flex-direction:column;justify-content:center}.whoop-badge{display:inline-flex;align-items:center;gap:9px;width:max-content;color:#82cfff;font-family:var(--mono);font-size:9px;letter-spacing:.16em;text-transform:uppercase;margin-bottom:14px}.whoop-badge:before{content:"";width:8px;height:8px;border-radius:50%;background:#00a6ff;box-shadow:0 0 14px rgba(0,166,255,.6)}.whoop-title{font-family:var(--display);font-size:24px;font-weight:700;line-height:1.06;margin:0 0 8px}.whoop-copy{margin:0;color:#9cabb7;font-size:13px;line-height:1.45}.whoop-gauge-wrap{display:flex;justify-content:center;align-items:center}.whoop-gauge{width:176px;height:176px;position:relative}.whoop-gauge svg{width:100%;height:100%;transform:rotate(-90deg);display:block}.whoop-track{fill:none;stroke:#29343d;stroke-width:10}.whoop-ring{fill:none;stroke:url(#whoopBlueGradient);stroke-width:10;stroke-linecap:butt;stroke-dasharray:452.39;stroke-dashoffset:452.39;transition:stroke-dashoffset .7s ease}.whoop-center{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}.whoop-center-value{font-size:48px;line-height:1;font-weight:500;letter-spacing:-.03em}.whoop-center-label{margin-top:14px;color:#c6c9cc;font-size:15px;font-weight:600}.whoop-metric{min-height:132px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;border-left:1px solid rgba(255,255,255,.06)}.whoop-metric-value{font-size:34px;line-height:1;font-weight:600;letter-spacing:-.03em}.whoop-metric-value small{font-size:13px;margin-left:3px;color:#8fa3b1;font-weight:600}.whoop-metric-label{margin-top:13px;color:#a5adb4;font-size:13px;line-height:1.25}.whoop-bottom{border-top:1px solid rgba(255,255,255,.1);padding:16px 30px 18px;display:flex;justify-content:space-between;align-items:center;gap:20px}.whoop-activities{display:flex;flex-wrap:wrap;gap:9px}.whoop-live-chip{display:inline-flex;gap:7px;align-items:center;padding:7px 10px;border-radius:999px;background:#202a33;border:1px solid rgba(255,255,255,.06);color:#ced6dc;font-size:12px}.whoop-updated{color:#7f909d;font-family:var(--mono);font-size:9px;letter-spacing:.12em;text-transform:uppercase;white-space:nowrap}@media(max-width:900px){.whoop-main{grid-template-columns:1fr 1fr}.whoop-brand{grid-column:1/-1}.whoop-metric{border-left:0;border-top:1px solid rgba(255,255,255,.06);min-height:105px}.whoop-bottom{flex-direction:column;align-items:flex-start}}@media(max-width:560px){.whoop-main{grid-template-columns:1fr;padding:24px 20px}.whoop-brand{grid-column:auto}.whoop-metric{padding-top:20px}.whoop-bottom{padding:16px 20px 20px}}
</style><div id="whoop-week" class="rv"><div class="whoop-main"><div class="whoop-brand"><div class="whoop-badge">WHOOP · this week</div><h3 class="whoop-title">Training snapshot</h3><p class="whoop-copy">A minimal weekly view from WHOOP — focused on strain, training time, and heart rate.</p></div><div class="whoop-gauge-wrap"><div class="whoop-gauge" aria-label="Weekly average strain"><svg viewBox="0 0 176 176" aria-hidden="true"><defs><linearGradient id="whoopBlueGradient" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#00b6ff"/><stop offset="100%" stop-color="#0876d7"/></linearGradient></defs><circle class="whoop-track" cx="88" cy="88" r="72"/><circle id="whoop-strain-ring" class="whoop-ring" cx="88" cy="88" r="72"/></svg><div class="whoop-center"><div id="whoop-strain" class="whoop-center-value">—</div><div class="whoop-center-label">Strain</div></div></div></div><div class="whoop-metric"><div id="whoop-time" class="whoop-metric-value">—</div><div class="whoop-metric-label">Training<br>time</div></div><div class="whoop-metric"><div class="whoop-metric-value"><span id="whoop-peak">—</span><small>bpm</small></div><div class="whoop-metric-label">Peak<br>heart rate</div></div></div><div class="whoop-bottom"><div id="whoop-activities" class="whoop-activities">loading training…</div><div id="whoop-updated" class="whoop-updated">loading WHOOP…</div></div></div>'''


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
