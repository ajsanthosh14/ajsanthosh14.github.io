#!/usr/bin/env python3
from pathlib import Path

INDEX = Path('index.html')
START = '<span class="life-subhead rv">Training log</span>'
END = '<p class="lead rv">Colorado turned out to be the other half of the job.'
SCRIPT = '<script src="assets/js/whoop-dashboard.js"></script>'

WHOOP_BLOCK = '''<span class="life-subhead rv">Training log</span><div id="whoop-week" class="rv" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;align-items:stretch;margin:18px 0 34px;padding:24px;border-radius:28px;background:var(--card);border:1px solid var(--line);box-shadow:0 10px 30px rgba(36,29,46,.04)"><div style="display:flex;flex-direction:column;justify-content:center"><span style="display:inline-flex;align-items:center;gap:8px;width:max-content;font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:#241d2e;background:var(--mint);border-radius:99px;padding:6px 10px">WHOOP · live training</span><h3 style="font-family:var(--display);font-size:clamp(28px,4vw,42px);line-height:1;margin:11px 0 10px">Whatever I’m training this week.</h3><p style="color:var(--dim);margin:0;max-width:50ch;font-size:15px">Gym sessions, Muay Thai, conditioning, hiking — automatically summarized from my WHOOP workouts.</p><div style="display:flex;flex-wrap:wrap;gap:7px;margin-top:17px"><span style="font-family:var(--mono);font-size:9.5px;text-transform:uppercase;letter-spacing:.06em;background:var(--bg);border:1px solid var(--line);border-radius:99px;padding:6px 10px;color:var(--dim)">🥊 Muay Thai</span><span style="font-family:var(--mono);font-size:9.5px;text-transform:uppercase;letter-spacing:.06em;background:var(--bg);border:1px solid var(--line);border-radius:99px;padding:6px 10px;color:var(--dim)">🏋️ Gym</span><span style="font-family:var(--mono);font-size:9.5px;text-transform:uppercase;letter-spacing:.06em;background:var(--bg);border:1px solid var(--line);border-radius:99px;padding:6px 10px;color:var(--dim)">⛰️ Hiking</span><span style="font-family:var(--mono);font-size:9.5px;text-transform:uppercase;letter-spacing:.06em;background:var(--bg);border:1px solid var(--line);border-radius:99px;padding:6px 10px;color:var(--dim)">⚡ Conditioning</span></div></div><div style="border-radius:22px;padding:20px;background:linear-gradient(145deg,var(--mint),#fff);border:1px solid rgba(36,29,46,.08);display:flex;flex-direction:column;justify-content:center"><div style="display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:14px;font-family:var(--mono);font-size:9.5px;text-transform:uppercase;color:rgba(36,29,46,.6)"><span>this week</span><span id="whoop-updated">loading WHOOP…</span></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:10px"><div style="background:rgba(255,255,255,.7);border-radius:18px;padding:14px"><div id="whoop-workouts" style="font-family:var(--display);font-size:30px;font-weight:700;line-height:1">—</div><div style="font-family:var(--mono);font-size:9px;text-transform:uppercase;color:var(--dim);margin-top:6px">workouts</div></div><div style="background:rgba(255,255,255,.7);border-radius:18px;padding:14px"><div id="whoop-time" style="font-family:var(--display);font-size:30px;font-weight:700;line-height:1">—</div><div style="font-family:var(--mono);font-size:9px;text-transform:uppercase;color:var(--dim);margin-top:6px">training time</div></div><div style="background:rgba(255,255,255,.7);border-radius:18px;padding:14px"><div id="whoop-strain" style="font-family:var(--display);font-size:30px;font-weight:700;line-height:1">—</div><div style="font-family:var(--mono);font-size:9px;text-transform:uppercase;color:var(--dim);margin-top:6px">avg strain</div></div><div style="background:rgba(255,255,255,.7);border-radius:18px;padding:14px"><div style="display:flex;align-items:baseline;gap:4px"><div id="whoop-peak" style="font-family:var(--display);font-size:30px;font-weight:700;line-height:1">—</div><span style="font-family:var(--mono);font-size:9px;color:var(--dim)">bpm</span></div><div style="font-family:var(--mono);font-size:9px;text-transform:uppercase;color:var(--dim);margin-top:6px">peak HR</div></div></div><div id="whoop-activities" style="margin-top:14px"></div><div style="font-family:var(--mono);font-size:9px;text-transform:uppercase;color:rgba(36,29,46,.5);margin-top:12px">updated automatically from WHOOP</div></div></div>'''


def main():
    text = INDEX.read_text(encoding='utf-8')
    changed = False

    if 'id="whoop-week"' not in text:
        start = text.find(START)
        end = text.find(END, start)
        if start < 0 or end < 0:
            raise SystemExit('Could not find the existing Training log block safely.')
        text = text[:start] + WHOOP_BLOCK + text[end:]
        changed = True

    if SCRIPT not in text:
        text = text.replace('</body>', SCRIPT + '\n</body>')
        changed = True

    if changed:
        INDEX.write_text(text, encoding='utf-8')
        print('Installed WHOOP dashboard on homepage.')
    else:
        print('WHOOP dashboard already installed.')


if __name__ == '__main__':
    main()
