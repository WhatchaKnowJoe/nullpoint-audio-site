import base64, json, os
D = '/mnt/user-data/outputs/NP/design'
OUT = '/mnt/user-data/outputs/NP/site/index.html'
os.makedirs(os.path.dirname(OUT), exist_ok=True)

def svg_uri(theme, name):
    s = open(f'{D}/{theme}/{name}.svg', 'rb').read()
    return 'data:image/svg+xml;base64,' + base64.b64encode(s).decode()

# order = the vocal signal chain
PLUGINS = [
  dict(id='np-zero',  name='NP-Zero',  kind='Noise & room reduction', h=480,
       lead='Cleans the recording before anything else touches it.',
       body='NP-Zero learns the noise profile of a room or a mic chain in a second of silence, then subtracts it from the take without the warble or hollowness of ordinary gates and expanders. Auto mode keeps re-learning as the environment changes.',
       specs=[('Learn / Auto noise profile','one click, or continuous'),('Reduction','0–100 %, spectral'),('Listen','hear only what is removed'),('Latency','zero')]),
  dict(id='np-gate',  name='NP-Gate',  kind='Noise gate', h=540,
       lead='Silence between phrases, without clipped consonants.',
       body='A look-ahead gate with hysteresis, so it opens before the word starts and never chatters on a held note. The sidechain high-pass and low-pass filters stop rumble and bleed from triggering it; Listen lets you tune the detector by ear.',
       specs=[('Threshold / Range','−80 to 0 dB, up to 80 dB attenuation'),('Attack · Hold · Release','0.1 ms – 2 s'),('Look-ahead','up to 10 ms'),('Sidechain filter','HPF + LPF, with Listen')]),
  dict(id='np-deess', name='NP-DeEss', kind='De-esser', h=520,
       lead='Takes the sting out of S and T without dulling the top end.',
       body='NP-DeEss splits the signal with a Linkwitz-Riley 4 crossover, so only the sibilant band is compressed and the rest of the vocal passes untouched. The spectrum display shows where the sibilance actually is; drag the marker to it.',
       specs=[('Frequency','2 – 16 kHz, drag on the display'),('Modes','Split band / Wideband'),('Detection','bandwidth 0.3 – 3 oct, ratio up to 20:1'),('Listen','monitor the detector band')]),
  dict(id='np-eq',    name='NP-EQ',    kind='Parametric equalizer', h=640,
       lead='Eight bands that sound right up to 20 kHz.',
       body='Most digital EQs cramp near Nyquist; NP-EQ uses analog-matched bell filters, so a high shelf at 12 kHz behaves like the hardware it was modelled on. A pre/post analyzer sits behind the curve and every band is drawn, grabbed and scrolled directly on the display.',
       specs=[('Bands','8: bell, low/high shelf, low/high cut 6–48 dB/oct, notch'),('Analyzer','pre, post, or both'),('Range','±6 / ±12 / ±24 dB views'),('Filter design','Vicanek matched, 0.6 dB error at 20 kHz')]),
  dict(id='np-comp',  name='NP-Comp',  kind='Vocal compressor', h=560,
       lead='Level a vocal and keep it alive.',
       body='A feed-forward compressor built for voice: program-dependent auto-release, a sidechain high-pass so plosives don\'t pump the mix, look-ahead for transparent peak control and a mix knob for parallel compression inside the plugin. The transfer curve shows exactly what is happening to the signal.',
       specs=[('Ratio','1:1 – 20:1, soft or hard knee'),('Attack / Release','0.1 – 100 ms / 10 ms – 2 s, Auto'),('Detection','Peak or RMS, sidechain HPF'),('Mix / Makeup','0–100 %, ±24 dB, click-free')]),
  dict(id='np-verb',  name='NP-Verb',  kind='Algorithmic reverb', h=600,
       lead='A reverb you can automate while it plays.',
       body='NP-Verb is a modulated feedback-delay-network with its own early-reflection stage. Changing size, pre-delay or decay during playback cross-fades between settings instead of bending the pitch, so it is safe to automate on a live vocal. Freeze holds the tail forever.',
       specs=[('Modes · Colors','Room, Plate, Hall, Chamber · Vintage, Modern, Dark'),('Decay','0.1 – 30 s, Freeze'),('Damping','high-frequency + bass multiplier'),('Modulation / Diffusion','rate, depth, early & late density')]),
  dict(id='np-limit', name='NP-Limit', kind='True-peak limiter', h=480,
       lead='Loud, and never over the ceiling.',
       body='The last plugin on the chain. NP-Limit looks ahead, finds the minimum gain the signal needs and smooths it so there is no overshoot — mathematically, not approximately — with true-peak metering for streaming delivery.',
       specs=[('Ceiling','−20 to 0 dBTP'),('Look-ahead','0.5 – 10 ms'),('Release','1 ms – 1 s, program dependent'),('Metering','true-peak output, gain reduction history')]),
]

def esc(s): return s.replace('&','&amp;').replace('<','&lt;')

cards = []
for i,p in enumerate(PLUGINS):
    dark, light = svg_uri('dark', p['name']), svg_uri('light-purple', p['name'])
    specs = ''.join(f'<div class="spec"><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k,v in p['specs'])
    flip = ' flip' if i % 2 else ''
    cards.append(f'''
<section class="plugin{flip}" id="{p['id']}">
  <div class="shot"><img src="{dark}" data-dark="{dark}" data-light="{light}" alt="{p['name']} user interface" width="1100" height="{p['h']}"></div>
  <div class="text">
    <div class="step">{i+1} of 7 in the chain</div>
    <h2>{p['name']}<span>{esc(p['kind'])}</span></h2>
    <p class="lead">{esc(p['lead'])}</p>
    <p>{esc(p['body'])}</p>
    <dl class="specs">{specs}</dl>
  </div>
</section>''')

hero_dark, hero_light = svg_uri('dark','NP-Comp'), svg_uri('light-purple','NP-Comp')
chain = ''.join(f'<a href="#{p["id"]}"><b>{p["name"]}</b><i>{esc(p["kind"])}</i></a>' for p in PLUGINS)

html = f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Null Point Audio — NP Vocal Suite</title>
<meta name="description" content="Seven vocal-chain plugins from Null Point Audio: NP-Zero, NP-Gate, NP-DeEss, NP-EQ, NP-Comp, NP-Verb and NP-Limit. VST3 for Windows, one installer.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{
  --bg:#121417; --panel:#1a1d22; --screen:#0e1013; --edge:#272b32; --edge2:#363b44;
  --t1:#eeeeee; --t2:#b3b8c2; --t3:#7d838d;
  --acc:#ff4d4d; --acc-dark:#b02a2a; --acc-soft:rgba(255,77,77,.14);
  --shadow:0 30px 70px rgba(0,0,0,.6);
  --knob:linear-gradient(#2b2f36,#15181c);
}}
[data-theme=light]{{
  --bg:#e6e8ed; --panel:#eef0f4; --screen:#f6f7f9; --edge:#d8dce3; --edge2:#c9ced8;
  --t1:#262b34; --t2:#5a606c; --t3:#8f96a2;
  --acc:#8b5cf6; --acc-dark:#5b36c4; --acc-soft:rgba(139,92,246,.14);
  --shadow:0 30px 70px rgba(70,80,110,.35);
  --knob:linear-gradient(#ffffff,#e3e6ec);
}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
@media (prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}} *{{transition:none!important;animation:none!important}}}}
body{{margin:0;background:var(--bg);color:var(--t1);font-family:Inter,"Segoe UI",Helvetica,Arial,sans-serif;font-size:17px;line-height:1.55;-webkit-font-smoothing:antialiased;transition:background .35s,color .35s}}
a{{color:inherit}}
img{{display:block;max-width:100%;height:auto}}
:focus-visible{{outline:2px solid var(--acc);outline-offset:3px}}
.wrap{{width:min(1180px,calc(100% - 48px));margin:0 auto}}

/* nav */
nav{{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--bg) 86%,transparent);backdrop-filter:blur(14px);border-bottom:1px solid var(--edge)}}
nav .wrap{{display:flex;align-items:center;gap:28px;height:64px}}
.logo{{display:flex;align-items:center;gap:12px;text-decoration:none;font-weight:800;letter-spacing:.18em;font-size:13px;white-space:nowrap}}
@media(max-width:420px){{.logo{{font-size:11px;letter-spacing:.12em}}}}
.mark{{width:26px;height:26px;border-radius:50%;background:radial-gradient(circle at 50% 50%,var(--bg) 0 30%,var(--acc) 31% 58%,var(--acc-soft) 59%);box-shadow:0 0 0 1px var(--edge)}}
nav ul{{display:flex;gap:22px;list-style:none;margin:0 0 0 auto;padding:0;font-size:14px;color:var(--t2)}}
nav ul a{{text-decoration:none}} nav ul a:hover{{color:var(--t1)}}
@media(max-width:760px){{nav ul{{display:none}}}}
.toggle{{margin-left:auto;display:inline-flex;align-items:center;gap:8px;height:34px;padding:0 10px 0 6px;border-radius:17px;border:1px solid var(--edge2);background:var(--panel);color:var(--t2);font:600 12px Inter,sans-serif;letter-spacing:.08em;cursor:pointer}}
nav ul + .toggle{{margin-left:0}}
.toggle .dot{{width:22px;height:22px;border-radius:50%;background:var(--knob);box-shadow:inset 0 0 0 1px var(--edge2);display:grid;place-items:center}}
.toggle svg{{width:13px;height:13px;fill:none;stroke:var(--acc);stroke-width:2;stroke-linecap:round}}
.btn{{display:inline-flex;align-items:center;gap:10px;height:46px;padding:0 22px;border-radius:12px;background:var(--acc);color:#fff;text-decoration:none;font-weight:700;font-size:15px;border:0;cursor:pointer;box-shadow:0 10px 28px var(--acc-soft);transition:transform .15s,box-shadow .15s}}
.btn:hover{{transform:translateY(-1px)}}
.btn.small{{height:36px;padding:0 16px;font-size:14px;border-radius:10px}}
.btn.ghost{{background:var(--panel);color:var(--t1);box-shadow:inset 0 0 0 1px var(--edge2)}}
.btn svg{{width:16px;height:16px;fill:none;stroke:currentColor;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}}

/* hero */
.hero{{padding:72px 0 40px}}
.hero h1{{font-size:clamp(40px,6.4vw,78px);line-height:1.02;letter-spacing:-.03em;font-weight:800;margin:0 0 22px;max-width:14ch}}
.hero p{{font-size:20px;color:var(--t2);max-width:52ch;margin:0 0 30px}}
.cta{{display:flex;flex-wrap:wrap;align-items:center;gap:16px 22px}}
.meta{{color:var(--t3);font-size:14px}}
.meta b{{color:var(--t2);font-weight:600}}
.stage{{margin:56px 0 0;padding:clamp(18px,4vw,56px);border-radius:24px;background:radial-gradient(ellipse at 50% 0%,color-mix(in srgb,var(--panel) 60%,var(--screen)) 0%,var(--screen) 80%);border:1px solid var(--edge);position:relative;overflow:hidden}}
.stage img{{border-radius:12px;box-shadow:var(--shadow);margin:0 auto}}
.stage .hint{{position:absolute;right:20px;top:14px;font-size:12px;color:var(--t3);letter-spacing:.06em}}
@media(max-width:700px){{.stage .hint{{display:none}}}}

/* chain */
.chain{{padding:60px 0 20px}}
.chain h2,.dl h2,.faq h2{{font-size:30px;letter-spacing:-.02em;margin:0 0 8px}}
.chain p.sub{{color:var(--t2);margin:0 0 28px;max-width:60ch}}
.rail{{display:grid;grid-template-columns:repeat(7,1fr);gap:0;border:1px solid var(--edge);border-radius:16px;background:var(--panel);overflow:hidden}}
.rail a{{padding:18px 14px 16px;text-decoration:none;border-right:1px solid var(--edge);position:relative;min-width:0}}
.rail a:last-child{{border-right:0}}
.rail a:hover{{background:var(--acc-soft)}}
.rail b{{display:block;font-size:15px;letter-spacing:.04em}}
.rail i{{display:block;font-style:normal;color:var(--t3);font-size:12.5px;margin-top:4px;line-height:1.3}}
.rail a::after{{content:"";position:absolute;right:-5px;top:50%;width:8px;height:8px;border-top:1.5px solid var(--t3);border-right:1.5px solid var(--t3);transform:translateY(-50%) rotate(45deg);z-index:1}}
.rail a:last-child::after{{display:none}}
@media(max-width:900px){{.rail{{grid-template-columns:repeat(4,1fr)}} .rail a:nth-child(4){{border-right:0}} .rail a:nth-child(-n+4){{border-bottom:1px solid var(--edge)}} .rail a::after{{display:none}}}}
@media(max-width:520px){{.rail{{grid-template-columns:repeat(2,1fr)}} .rail a{{border-right:1px solid var(--edge)!important;border-bottom:1px solid var(--edge)}} .rail a:nth-child(2n){{border-right:0!important}}}}

/* plugin sections */
.plugin{{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(28px,5vw,72px);align-items:center;padding:72px 0;border-top:1px solid var(--edge)}}
.plugin:first-of-type{{border-top:0}}
.plugin.flip .shot{{order:2}}
.shot img{{border-radius:12px;box-shadow:var(--shadow);border:1px solid var(--edge)}}
.step{{font-size:13px;color:var(--acc);font-weight:600;margin-bottom:14px}}
.plugin h2{{font-size:36px;letter-spacing:-.02em;margin:0 0 14px;line-height:1.1}}
.plugin h2 span{{display:block;font-size:15px;font-weight:500;color:var(--t3);letter-spacing:.04em;margin-top:6px}}
.plugin .lead{{font-size:21px;font-weight:600;line-height:1.35;margin:0 0 14px}}
.plugin p{{color:var(--t2);margin:0 0 22px;max-width:52ch}}
.specs{{margin:0;display:grid;grid-template-columns:1fr 1fr;gap:12px 18px}}
.spec{{padding:12px 14px;border-radius:10px;background:var(--panel);box-shadow:inset 0 0 0 1px var(--edge)}}
.spec dt{{font-size:12px;color:var(--t3);font-weight:600;margin:0 0 3px}}
.spec dd{{margin:0;font-size:14px;color:var(--t1);line-height:1.35}}
@media(max-width:860px){{.plugin{{grid-template-columns:1fr;padding:48px 0}} .plugin.flip .shot{{order:0}} .plugin h2{{font-size:30px}}}}
@media(max-width:480px){{.specs{{grid-template-columns:1fr}}}}

/* download */
.dl{{margin-top:40px;padding:64px 0;border-top:1px solid var(--edge)}}
.dl .grid{{display:grid;grid-template-columns:1.1fr .9fr;gap:48px;align-items:start}}
@media(max-width:860px){{.dl .grid{{grid-template-columns:1fr}}}}
.dlbox{{padding:28px;border-radius:18px;background:var(--panel);box-shadow:inset 0 0 0 1px var(--edge)}}
.dlbox h3{{margin:0 0 6px;font-size:22px;letter-spacing:-.01em}}
.dlbox .ver{{color:var(--t3);font-size:14px;margin-bottom:22px}}
.req{{list-style:none;padding:0;margin:22px 0 0;display:grid;gap:8px;color:var(--t2);font-size:15px}}
.req li{{display:flex;gap:10px}} .req li::before{{content:"";width:6px;height:6px;border-radius:50%;background:var(--acc);margin-top:9px;flex:none}}
.steps{{margin:0;padding:0;list-style:none;counter-reset:s}}
.steps li{{counter-increment:s;display:grid;grid-template-columns:36px 1fr;gap:14px;padding:16px 0;border-bottom:1px solid var(--edge);color:var(--t2)}}
.steps li::before{{content:counter(s);width:32px;height:32px;border-radius:50%;background:var(--acc-soft);color:var(--acc);font-weight:700;font-size:14px;display:grid;place-items:center}}
.steps b{{color:var(--t1);display:block;margin-bottom:2px;font-weight:600}}

/* faq */
.faq{{padding:40px 0 70px}}
.faq details{{border-top:1px solid var(--edge);padding:16px 0}}
.faq details:last-child{{border-bottom:1px solid var(--edge)}}
.faq summary{{cursor:pointer;font-weight:600;font-size:17px;list-style:none;display:flex;justify-content:space-between;gap:20px}}
.faq summary::after{{content:"+";color:var(--acc);font-size:22px;line-height:1}}
.faq details[open] summary::after{{content:"–"}}
.faq details p{{color:var(--t2);margin:10px 0 0;max-width:70ch}}

footer{{border-top:1px solid var(--edge);padding:28px 0 40px;color:var(--t3);font-size:13px;display:flex;flex-wrap:wrap;gap:12px 28px;align-items:center}}
footer .wrap{{display:flex;flex-wrap:wrap;gap:12px 28px;align-items:center}}
footer a{{text-decoration:none;color:var(--t2)}}
</style>
</head>
<body>
<nav><div class="wrap">
  <a class="logo" href="#top"><span class="mark"></span>NULL POINT AUDIO</a>
  <ul><li><a href="#chain">The chain</a></li><li><a href="#np-eq">Plugins</a></li><li><a href="#download">Download</a></li><li><a href="#faq">FAQ</a></li></ul>
  <button class="toggle" id="toggle" aria-label="Switch between dark and light theme"><span class="dot">
    <svg id="ico" viewBox="0 0 24 24"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></span><span id="tlabel">LIGHT</span></button>
  <a class="btn small" href="#download">Download</a>
</div></nav>

<main id="top">
<header class="hero wrap">
  <h1>Seven plugins. One vocal chain.</h1>
  <p>NP Vocal Suite takes a raw vocal from noisy take to finished level: clean it, gate it, tame the sibilance, shape it, compress it, give it a space and cap the peaks. Every plugin shares the same interface, the same preset system and the same dark or light skin.</p>
  <div class="cta">
    <a class="btn" href="DOWNLOAD_URL_PLACEHOLDER" id="dl-top"><svg viewBox="0 0 24 24"><path d="M12 3v12m0 0 5-5m-5 5-5-5M4 19h16"/></svg>Download for Windows</a>
    <span class="meta"><b>Free</b> · v1.0.0 · 25 MB · VST3 + standalone · Windows 10/11 64-bit</span>
  </div>
  <div class="stage">
    <span class="hint">Same look inside every DAW, dark or light</span>
    <img id="hero-shot" src="{hero_dark}" data-dark="{hero_dark}" data-light="{hero_light}" alt="NP-Comp compressor interface" width="1100" height="560">
  </div>
</header>

<section class="chain wrap" id="chain">
  <h2>In the order you would use them</h2>
  <p class="sub">The suite is built as a signal path. Put them on a vocal track in this order and each plugin hands a cleaner signal to the next; use any one on its own and it still works like a standard VST3 effect.</p>
  <div class="rail">{chain}</div>
</section>

<div class="wrap">
{''.join(cards)}
</div>

<section class="dl wrap" id="download">
  <h2>Download</h2>
  <div class="grid">
    <div class="dlbox">
      <h3>NP Vocal Suite installer</h3>
      <div class="ver">NullPointAudio_Bundle_Setup_v1.0.0.exe · 25 MB · released November 2026</div>
      <a class="btn" href="DOWNLOAD_URL_PLACEHOLDER" id="dl-main"><svg viewBox="0 0 24 24"><path d="M12 3v12m0 0 5-5m-5 5-5-5M4 19h16"/></svg>Download for Windows</a>
      <ul class="req">
        <li>Windows 10 or 11, 64-bit</li>
        <li>Any VST3 host: FL Studio, Ableton Live, Cubase, Studio One, Reaper, Bitwig, Pro Tools 2024 and later</li>
        <li>Installs all seven plugins; pick individual ones in the installer if you prefer</li>
        <li>Standalone apps are optional and run without a DAW</li>
        <li>No runtime or extra downloads needed</li>
      </ul>
    </div>
    <ol class="steps">
      <li><span><b>Run the installer</b>Close your DAW first. Accept the license and choose the plugins you want.</span></li>
      <li><span><b>Let it install to the system VST3 folder</b>C:\\Program Files\\Common Files\\VST3 — every VST3 host scans it automatically.</span></li>
      <li><span><b>Rescan plugins in your DAW</b>Open the plugin manager and run a scan. The plugins appear under Null Point Audio.</span></li>
      <li><span><b>Pick a skin</b>Click the sun / moon button in any plugin. The choice applies to all seven, in every project.</span></li>
    </ol>
  </div>
</section>

<section class="faq wrap" id="faq">
  <h2>Questions</h2>
  <details><summary>Does the suite add latency?</summary><p>NP-Zero, NP-EQ and NP-Verb are zero-latency. NP-Gate, NP-DeEss, NP-Comp and NP-Limit use look-ahead and report it to the host, so your DAW compensates automatically when tracking or mixing.</p></details>
  <details><summary>Where are presets stored?</summary><p>Factory presets are built in, organised by genre and task. Your own presets are saved as files in <code>%APPDATA%\\NullPointAudio\\&lt;plugin&gt;\\Presets</code>, so they survive reinstalls and can be copied between machines.</p></details>
  <details><summary>Can I use them one at a time?</summary><p>Yes. The chain order is a recommendation. Each plugin is an ordinary VST3 effect and can go anywhere on any track, vocal or not.</p></details>
  <details><summary>How do I uninstall?</summary><p>Windows Settings → Apps → Null Point Audio NP Vocal Suite → Uninstall. Your presets and skin setting are kept unless you delete the NullPointAudio folder yourself.</p></details>
  <details><summary>macOS?</summary><p>Not yet. The suite is Windows-only for version 1.0.</p></details>
</section>
</main>

<footer><div class="wrap">
  <span>© 2026 Null Point Audio</span>
  <a href="https://www.nullpointaudio.com">nullpointaudio.com</a>
  <a href="#download">Download</a>
  <span>VST is a trademark of Steinberg Media Technologies GmbH.</span>
</div></footer>

<script>
(function(){{
  // ---- download link: set this to where the installer is hosted ----
  var DOWNLOAD_URL = "https://www.nullpointaudio.com/downloads/NullPointAudio_Bundle_Setup_v1.0.0.exe";
  document.querySelectorAll('a[href="DOWNLOAD_URL_PLACEHOLDER"]').forEach(function(a){{ a.href = DOWNLOAD_URL; }});

  var root = document.documentElement, btn = document.getElementById('toggle'), lbl = document.getElementById('tlabel'), ico = document.getElementById('ico');
  var SUN = '<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>';
  var MOON = '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>';
  function apply(t){{
    root.setAttribute('data-theme', t);
    lbl.textContent = t === 'dark' ? 'LIGHT' : 'DARK';
    ico.innerHTML = t === 'dark' ? MOON : SUN;
    document.querySelectorAll('img[data-dark]').forEach(function(im){{ im.src = im.getAttribute('data-' + t); }});
    try {{ localStorage.setItem('np-theme', t); }} catch(e) {{}}
  }}
  var saved = null; try {{ saved = localStorage.getItem('np-theme'); }} catch(e) {{}}
  apply(saved === 'light' ? 'light' : 'dark');
  btn.addEventListener('click', function(){{ apply(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'); }});
}})();
</script>
</body>
</html>'''
open(OUT,'w').write(html)
print(len(html)//1024, 'KB')
