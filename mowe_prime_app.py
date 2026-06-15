"""
Mowe Prime Pitch Generator
Run: python3 mowe_prime_app.py
Then open: http://localhost:5000

Requirements: pip install flask reportlab gunicorn
"""

from flask import Flask, request, send_file, render_template_string
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import io
import os

app = Flask(__name__)

W, H = A4
GREEN = (13/255, 43/255, 30/255)
GOLD = (200/255, 168/255, 75/255)
GOLD2 = (232/255, 201/255, 107/255)
CREAM = (247/255, 243/255, 236/255)
WHITE = (1, 1, 1)
DARK = (0.27, 0.27, 0.27)
MUTED = (0.42, 0.42, 0.42)

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>Mowe Prime Pitch Generator</title>
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif;background:#f0ece3;color:#1a1a1a;min-height:100vh;}
.hdr{background:#0d2b1e;padding:22px 28px 18px;border-bottom:4px solid #c8a84b;}
.hdr h1{color:#c8a84b;font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;margin-bottom:4px;}
.hdr p{color:rgba(255,255,255,0.42);font-size:11px;}
.wrap{max-width:820px;margin:28px auto;padding:0 16px 60px;}
.card{background:#fff;border-radius:6px;border:1px solid #e0d9cc;overflow:hidden;}
.sec-hdr{background:#0d2b1e;color:#c8a84b;font-size:9px;font-weight:700;letter-spacing:3px;text-transform:uppercase;padding:10px 20px;}
.grid{display:flex;flex-wrap:wrap;gap:14px;padding:20px;}
.field{flex:1 1 190px;min-width:150px;}
.field label{display:block;font-size:9px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#888;margin-bottom:5px;}
.field input,.field select{width:100%;border:1px solid #ddd;border-radius:3px;padding:9px 11px;font-family:inherit;font-size:13px;color:#1a1a1a;background:#fafafa;outline:none;-webkit-appearance:none;appearance:none;}
.field input:focus,.field select:focus{border-color:#c8a84b;background:#fff;}
.divider{height:1px;background:#e0d9cc;margin:0 20px;}
.btn-row{padding:20px;display:flex;gap:12px;flex-wrap:wrap;align-items:center;}
.btn{background:#c8a84b;color:#0d2b1e;border:none;padding:13px 28px;font-family:inherit;font-size:12px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border-radius:3px;cursor:pointer;-webkit-appearance:none;}
.btn:hover{background:#d4b45a;}
.note{font-size:12px;color:#888;font-style:italic;}
.preview-box{max-width:820px;margin:0 auto;padding:0 16px 60px;}
.pv-card{background:#fff;border-radius:6px;border:1px solid #e0d9cc;overflow:hidden;}
.pv-hero{background:#0d2b1e;padding:40px 36px 32px;position:relative;overflow:hidden;}
.pv-tag{display:inline-block;font-size:8px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#c8a84b;border:1px solid rgba(200,168,75,0.4);padding:4px 10px;border-radius:2px;margin-bottom:14px;}
.pv-hero h2{font-size:clamp(18px,3vw,28px);font-weight:700;color:#fff;line-height:1.22;margin-bottom:10px;}
.pv-hero p{font-size:12px;color:rgba(255,255,255,0.6);line-height:1.6;max-width:450px;}
.stat-row{background:#c8a84b;display:flex;flex-wrap:wrap;}
.stat-cell{flex:1 1 80px;text-align:center;padding:11px 8px;border-right:1px solid rgba(13,43,30,0.18);}
.stat-cell:last-child{border-right:none;}
.stat-v{display:block;font-size:17px;font-weight:700;color:#0d2b1e;line-height:1;}
.stat-l{display:block;font-size:7px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:rgba(13,43,30,0.6);margin-top:3px;}
.pv-sec{padding:26px 36px;border-bottom:1px solid #e0d9cc;background:#fff;}
.pv-sec.cream{background:#f7f3ec;}
.pv-sec.dark{background:#0d2b1e;}
.pv-sec.gold{background:#c8a84b;}
.slbl{font-size:8px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#c8a84b;margin-bottom:10px;display:block;}
.pv-sec.dark .slbl{color:#e8c96b;}
.pv-sec h3{font-size:17px;font-weight:700;color:#0d2b1e;margin-bottom:10px;line-height:1.28;}
.pv-sec.dark h3{color:#fff;}
.pv-sec.gold h3{color:#0d2b1e;font-size:22px;}
.pv-sec p{font-size:13px;color:#444;line-height:1.75;}
.pv-sec.dark p{color:rgba(255,255,255,0.7);}
.pv-sec.gold p{color:rgba(13,43,30,0.72);}
.why-g{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px;}
.why-i{flex:1 1 210px;background:#fff;border-left:3px solid #c8a84b;padding:12px 14px;border-radius:0 3px 3px 0;}
.wi-t{font-size:11px;font-weight:700;color:#0d2b1e;margin-bottom:4px;}
.wi-b{font-size:11px;color:#6b6b6b;line-height:1.5;}
.pg{display:flex;flex-wrap:wrap;gap:12px;margin:14px 0;}
.pi{flex:1 1 170px;border:1px solid rgba(200,168,75,0.25);border-radius:4px;padding:16px 14px;background:rgba(255,255,255,0.06);}
.pi.ft{background:rgba(200,168,75,0.12);border-color:#c8a84b;}
.pi-tag{font-size:8px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#c8a84b;margin-bottom:6px;display:block;}
.pi-pr{font-size:26px;font-weight:700;color:#fff;line-height:1;margin-bottom:4px;}
.pi-sz{font-size:11px;color:rgba(255,255,255,0.45);margin-bottom:10px;}
.pi-dc{font-size:11px;color:rgba(255,255,255,0.65);line-height:1.7;}
.pmn{background:rgba(200,168,75,0.1);border:1px solid rgba(200,168,75,0.3);border-radius:3px;padding:10px 14px;font-size:12px;color:rgba(255,255,255,0.7);line-height:1.6;}
.pmn strong{color:#c8a84b;}
.ctbl{width:100%;border-collapse:collapse;margin-top:14px;font-size:12px;}
.ctbl th{background:#0d2b1e;color:#c8a84b;font-size:8px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;padding:8px 12px;text-align:left;}
.ctbl td{padding:8px 12px;border-bottom:1px solid #e0d9cc;color:#444;}
.ctbl tr.hl td{background:rgba(200,168,75,0.1);font-weight:700;color:#0d2b1e;}
.ctbl tr.ev td{background:#faf8f4;}
.bdg{display:inline-block;font-size:10px;font-weight:700;padding:2px 7px;border-radius:20px;}
.bg{background:#d4edda;color:#155724;}.br{background:#f8d7da;color:#721c24;}.by{background:#fff3cd;color:#856404;}
.bg2{display:flex;flex-wrap:wrap;gap:12px;margin:14px 0;}
.bi{flex:1 1 195px;background:#fff;border:1px solid #e0d9cc;border-top:3px solid #c8a84b;border-radius:0 0 4px 4px;padding:16px 14px;}
.bi-t{font-size:14px;font-weight:700;color:#0d2b1e;margin-bottom:6px;}
.bi-b{font-size:12px;color:#6b6b6b;line-height:1.6;}
.bn{background:#0d2b1e;border-radius:3px;padding:14px 16px;font-size:12px;color:rgba(255,255,255,0.75);line-height:1.7;}
.bn strong{color:#c8a84b;}
.ctact{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0;}
.ci{background:#0d2b1e;border-radius:3px;padding:10px 14px;display:flex;align-items:center;gap:8px;}
.ci-l{font-size:8px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;color:#c8a84b;display:block;margin-bottom:1px;}
.ci-v{font-size:12px;color:#fff;font-weight:500;}
.sig{margin-top:14px;font-size:11px;color:rgba(13,43,30,0.58);}
@media(max-width:560px){.pv-hero,.pv-sec{padding:22px 18px;}.field{flex:1 1 100%;}.stat-v{font-size:14px;}}
</style>
</head>
<body>
<div class="hdr">
<h1>Mowe Prime Pitch Generator</h1>
<p>Fill in the fields, preview your pitch, then download a fully coloured PDF instantly.</p>
</div>
<div class="wrap">
<form method="POST" action="/generate">
<div class="card">
<div class="sec-hdr">Prospect Details</div>
<div class="grid">
<div class="field"><label>Prospect Title</label><input name="title" placeholder="Dr. / Engr. / Chief / Mr." value="{{ d.title }}"/></div>
<div class="field"><label>First Name</label><input name="fname" placeholder="e.g. Tunde" value="{{ d.fname }}"/></div>
<div class="field"><label>What They Do</label><input name="job" placeholder="e.g. Banker / Engineer" value="{{ d.job }}"/></div>
<div class="field"><label>Their Primary Goal</label>
<select name="goal">
<option value="build wealth" {% if d.goal=='build wealth' %}selected{% endif %}>Build Long-Term Wealth</option>
<option value="secure land" {% if d.goal=='secure land' %}selected{% endif %}>Secure Land for the Future</option>
<option value="invest idle funds" {% if d.goal=='invest idle funds' %}selected{% endif %}>Invest Idle Funds</option>
<option value="diaspora property" {% if d.goal=='diaspora property' %}selected{% endif %}>Own Property from Abroad</option>
<option value="diversify" {% if d.goal=='diversify' %}selected{% endif %}>Diversify Their Portfolio</option>
<option value="build a home" {% if d.goal=='build a home' %}selected{% endif %}>Build a Home</option>
</select>
</div>
<div class="field"><label>Profile Type</label>
<select name="type">
<option value="home" {% if d.type=='home' %}selected{% endif %}>Nigeria-Based</option>
<option value="diaspora" {% if d.type=='diaspora' %}selected{% endif %}>Diaspora (Abroad)</option>
</select>
</div>
<div class="field"><label>Tier to Recommend</label>
<select name="tier">
<option value="both" {% if d.tier=='both' %}selected{% endif %}>Both Options</option>
<option value="standard" {% if d.tier=='standard' %}selected{% endif %}>Standard (N8M)</option>
<option value="premium" {% if d.tier=='premium' %}selected{% endif %}>Premium (N15M)</option>
</select>
</div>
</div>
<div class="divider"></div>
<div class="sec-hdr">Your Contact Details</div>
<div class="grid">
<div class="field"><label>Your Name</label><input name="agent" value="{{ d.agent }}"/></div>
<div class="field"><label>Your Phone</label><input name="phone" value="{{ d.phone }}"/></div>
<div class="field"><label>Your Email</label><input name="email" value="{{ d.email }}"/></div>
<div class="field"><label>Property URL</label><input name="url" value="{{ d.url }}"/></div>
</div>
<div class="divider"></div>
<div class="btn-row">
<button class="btn" type="submit" name="action" value="preview">Preview Pitch</button>
<button class="btn" type="submit" name="action" value="pdf" style="background:#0d2b1e;color:#c8a84b;">Download Coloured PDF</button>
<span class="note">Preview first or download directly.</span>
</div>
</div>
</form>
</div>
{% if preview %}
<div class="preview-box">
<div class="pv-card">
<div class="pv-hero">
<div class="pv-tag">Private Investment Brief &nbsp;·&nbsp; Land Republic</div>
<h2>{{ headline }}</h2>
<p>{{ hero_sub }}</p>
</div>
<div class="stat-row">
<div class="stat-cell"><span class="stat-v">29km</span><span class="stat-l">From Lagos</span></div>
<div class="stat-cell"><span class="stat-v">12-18%</span><span class="stat-l">Annual Appreciation</span></div>
<div class="stat-cell"><span class="stat-v">200K</span><span class="stat-l">RCCG Residents</span></div>
<div class="stat-cell"><span class="stat-v">60+</span><span class="stat-l">Multinationals</span></div>
<div class="stat-cell"><span class="stat-v">C of O</span><span class="stat-l">Bankable Title</span></div>
</div>
<div class="pv-sec"><span class="slbl">Why This Matters to You</span><h3>{{ body_hl }}</h3><p>{{ body_text }}</p></div>
<div class="pv-sec cream"><span class="slbl">The 4 Reasons This Works</span>
<div class="why-g">
<div class="why-i"><div class="wi-t">Lagos Overflow: Structural, Not a Trend</div><div class="wi-b">Lagos is running out of affordable land. Mowe gets the largest share of that overflow because of Expressway access. This does not stop.</div></div>
<div class="why-i"><div class="wi-t">60+ Multinationals: Constant Rental Demand</div><div class="wi-b">Nestle, AB InBev, CWAY, Rite Foods and dozens more employ tens of thousands nearby. Supply is short. Your land wins.</div></div>
<div class="why-i"><div class="wi-t">RCCG City: The Anchor No One Replicates</div><div class="wi-b">2,500 hectares. 200,000 residents. 197 countries of RCCG membership. Millions of annual visitors. Demand only grows.</div></div>
<div class="why-i"><div class="wi-t">Lagos-Ogun Infrastructure MOU (Signed)</div><div class="wi-b">Two state governments committed to joint roads, waterworks, rail, and waterways. Property values follow government money.</div></div>
</div></div>
<div class="pv-sec dark"><span class="slbl">Allocation Tiers</span><h3>Pick Your Entry Point</h3>
<div class="pg">
{% if d.tier == 'standard' %}<div class="pi ft"><span class="pi-tag">Recommended For You</span><div class="pi-pr">N8M</div><div class="pi-sz">300 SQM · 50ft x 60ft</div><div class="pi-dc">C of O Backed Title<br/>Deed of Assignment<br/>Registered Survey Plan<br/>Contract of Sale<br/>Allocation Letter + Receipt</div></div>
{% elif d.tier == 'premium' %}<div class="pi ft"><span class="pi-tag">Recommended For You</span><div class="pi-pr">N15M</div><div class="pi-sz">500 SQM · 60ft x 100ft</div><div class="pi-dc">C of O Backed Title<br/>Deed of Assignment<br/>Registered Survey Plan<br/>Contract of Sale<br/>Allocation Letter + Receipt</div></div>
{% else %}<div class="pi"><span class="pi-tag">Standard</span><div class="pi-pr">N8M</div><div class="pi-sz">300 SQM · 50ft x 60ft</div><div class="pi-dc">C of O Backed Title<br/>Deed of Assignment<br/>Registered Survey Plan<br/>Contract of Sale<br/>Allocation Letter + Receipt</div></div>
<div class="pi ft"><span class="pi-tag">Premium</span><div class="pi-pr">N15M</div><div class="pi-sz">500 SQM · 60ft x 100ft</div><div class="pi-dc">C of O Backed Title<br/>Deed of Assignment<br/>Registered Survey Plan<br/>Contract of Sale<br/>Allocation Letter + Receipt</div></div>
{% endif %}
</div>
<div class="pmn"><strong>Pay Outright</strong> for instant allocation &nbsp;·&nbsp; <strong>6 Months Interest-Free:</strong> deposit from N2M, balance monthly.<br/><span style="opacity:0.55;font-size:11px;">Account: Land Republic Limited · 78 Finance Company or 78 MFB · 0001549819</span></div>
</div>
<div class="pv-sec"><span class="slbl">How It Compares</span><h3 style="font-size:15px;margin-bottom:4px;">Mowe Prime vs. The Market</h3>
<table class="ctbl"><thead><tr><th>Location</th><th>Price Range</th><th>Title</th><th>5-Yr Potential</th></tr></thead>
<tbody>
<tr class="hl"><td>Mowe Prime</td><td>N8M to N15M</td><td><span class="bdg bg">C of O</span></td><td><span class="bdg bg">300 to 450%</span></td></tr>
<tr><td>Magboro</td><td>N18M+</td><td><span class="bdg by">Varies</span></td><td>N/A</td></tr>
<tr class="ev"><td>Ibadan (Bodija)</td><td>N40M+</td><td><span class="bdg by">Varies</span></td><td>N/A</td></tr>
<tr><td>Abuja (Gwarinpa)</td><td>N80M+</td><td><span class="bdg by">Varies</span></td><td>N/A</td></tr>
<tr class="ev"><td>Lagos (VI)</td><td>N180M+</td><td><span class="bdg bg">C of O</span></td><td><span class="bdg br">Saturated</span></td></tr>
</tbody></table></div>
<div class="pv-sec cream" style="border-top:4px solid #c8a84b;"><span class="slbl">Also Coming to Mowe Prime</span>
<h3>Modern Bungalows. Move-In Ready. On the Same Land.</h3>
<p style="margin-bottom:14px;">Beyond the land plots, we are developing modern 2-bedroom and 3-bedroom bungalows right here within Mowe Prime.</p>
<div class="bg2">
<div class="bi"><div class="bi-t">2-Bedroom Bungalow</div><div class="bi-b">Compact, modern, efficient. Ideal for young families, rental income plays, or a personal property with strong resale upside as the corridor matures.</div></div>
<div class="bi"><div class="bi-t">3-Bedroom Bungalow</div><div class="bi-b">More space, more comfort, more value. Perfect for those wanting a ready-made home without the stress of building, or investors targeting higher rental yields.</div></div>
</div>
<div class="bn"><strong>Why this lifts your investment:</strong> Modern finished homes within the estate directly raise the value of surrounding land. Your plot benefits whether you build or not.</div>
</div>
<div class="pv-sec gold" style="border-radius:0 0 6px 6px;">
<h3>{{ cta_hl }}</h3><p>{{ cta_txt }}</p>
<div class="ctact">
<div class="ci"><div><span class="ci-l">Call / WhatsApp</span><span class="ci-v">{{ d.phone }}</span></div></div>
<div class="ci"><div><span class="ci-l">Email</span><span class="ci-v">{{ d.email }}</span></div></div>
<div class="ci"><div><span class="ci-l">View Property</span><span class="ci-v">{{ d.url }}</span></div></div>
</div>
<p class="sig">Prepared by <strong>{{ d.agent }}</strong> &nbsp;·&nbsp; @asset_by_israel &nbsp;·&nbsp; Your Favorite Real Estate Consultant</p>
</div>
</div>
</div>
{% endif %}
</body>
</html>
"""


def get_body(goal, name):
    m = {
        'build wealth': (name + ', ' if name else '') + "land in the Mowe corridor has returned 12 to 18% annually, documented. That is not a promise, it is a market record. With Nestle, AB InBev, RCCG City, and a signed state infrastructure MOU all active, appreciation here is riding what is already in motion.",
        'secure land': "The best time to secure land near Lagos was 5 years ago. The second best time is now. Mowe Prime still offers C of O-backed plots at a fraction of Lagos prices. Every month more titled land gets absorbed. Securing a plot today means a legally clean appreciating asset while others are still thinking about it.",
        'invest idle funds': "Idle Naira loses ground every month. Land appreciating at 12 to 18% annually, backed by C of O title and surrounded by operating multinationals, is one of the most reliable stores of value in Nigeria right now. It does not crash overnight. It does not vanish. And when you are ready to exit, the demand is already there.",
        'diaspora property': "If you are in the diaspora, this is the cleanest Nigerian land deal available. C of O title: the highest land title possible. All documents in your name. A developer registered in both Nigeria and Delaware. Corridor gains absorb a significant portion of any FX gap.",
        'diversify': "Every serious portfolio needs a hard asset. C of O titled land 29km from Lagos, surrounded by 60+ active multinationals and three independent demand drivers: a non-correlated appreciating asset that will not move with stock markets or crypto.",
        'build a home': "Mowe Prime is a buy-and-build estate. Build at your own pace. No deadline, no pressure. C of O title means bank financing is accessible when you are ready. And the corridor keeps pushing your asset value higher whether you have broken ground or not.",
    }
    return m.get(goal, m['build wealth'])

def rgb(t):
    from reportlab.lib import colors as rlc
    return rlc.Color(t[0], t[1], t[2])

def build_pdf(d):
    W2, H2 = A4
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    M = 36
    CW = W2 - M * 2

    def fill(x, yt, w, h, col):
        c.setFillColor(rgb(col))
        c.rect(x, yt, w, h, fill=1, stroke=0)

    def txt(s, x, yt, size=10, bold=False, col=DARK):
        c.setFont('Helvetica-Bold' if bold else 'Helvetica', size)
        c.setFillColor(rgb(col))
        c.drawString(x, yt, str(s))

    def wrap(s, x, yt, mw, size=10, bold=False, col=DARK, lh=None):
        if lh is None: lh = size * 1.45
        font = 'Helvetica-Bold' if bold else 'Helvetica'
        c.setFont(font, size)
        c.setFillColor(rgb(col))
        lines = simpleSplit(str(s), font, size, mw)
        for line in lines:
            c.drawString(x, yt, line)
            yt -= lh
        return yt

    pt = d.get('title', '').strip()
    fn = d.get('fname', '').strip()
    if pt and fn: full = pt + ' ' + fn
    elif pt: full = pt
    elif fn: full = fn
    else: full = 'You'

    hero_hl = (full + ', This Land Was Made for People Like You') if full != 'You' else 'A Land Investment Built Around Your Goals'
    hero_sub = (d.get('job', '') + 's who want to ' + d.get('goal', '') + ' are exactly who Mowe Prime was built for.') if d.get('job') else "Mowe Prime - C of O titled land, 29km from Lagos, inside Nigeria's fastest-appreciating real estate corridor."
    body_hl = 'Your Naira Is Losing Ground. This Land Is Gaining It.' if d.get('type') == 'diaspora' else 'Mowe Has Already Arrived. The Price Has Not.'
    body_text = get_body(d.get('goal', 'build wealth'), fn or pt or '')
    cta_hl = (full + ', This Is Your Move. Make It.') if full != 'You' else 'This Is Your Move. Make It.'
    cta_txt = 'Everything can be completed remotely. Documents are processed and issued in your name. One call or message is all it takes. Do not leave this for later.' if d.get('type') == 'diaspora' else 'The land is real. The title is clean. The corridor is active. One conversation is all it takes to get your allocation started. Reach out today.'

    # PAGE 1
    fill(0, H2 - 160, W2, 160, GREEN)
    c.setFont('Helvetica-Bold', 7)
    c.setFillColor(rgb(GOLD))
    c.drawString(M, H2 - 14, 'PRIVATE INVESTMENT BRIEF | LAND REPUBLIC')

    c.setFont('Helvetica-Bold', 19)
    c.setFillColor(rgb(WHITE))
    hl_lines = simpleSplit(hero_hl, 'Helvetica-Bold', 19, CW)
    hy = H2 - 36
    for line in hl_lines:
        c.drawString(M, hy, line)
        hy -= 24

    c.setFont('Helvetica', 9)
    c.setFillColor(rgb((0.65, 0.65, 0.65)))
    for line in simpleSplit(hero_sub, 'Helvetica', 9, CW):
        c.drawString(M, hy, line)
        hy -= 13

    sb_y = H2 - 160 - 28
    fill(0, sb_y, W2, 28, GOLD)
    stats = [('29km','FROM LAGOS'),('12-18%','ANN. APPREC.'),('200K','RCCG RESID.'),('60+','MULTINATLS'),('C of O','TITLE')]
    sw = W2 / len(stats)
    for i, (val, lbl) in enumerate(stats):
        cx = i * sw + sw / 2
        c.setFont('Helvetica-Bold', 12)
        c.setFillColor(rgb(GREEN))
        c.drawCentredString(cx, sb_y + 16, val)
        c.setFont('Helvetica', 6)
        c.setFillColor(rgb((0.2, 0.35, 0.25)))
        c.drawCentredString(cx, sb_y + 7, lbl)

    y = sb_y - 8
    fill(0, y - 20, W2, 20, (0.97, 0.97, 0.97))
    c.setFont('Helvetica-Bold', 7)
    c.setFillColor(rgb(GOLD))
    c.drawString(M, y - 7, 'WHY THIS MATTERS TO YOU')
    y -= 20
    y = wrap(body_hl, M, y - 12, CW, size=14, bold=True, col=GREEN, lh=18) - 5
    y = wrap(body_text, M, y, CW, size=9, col=(0.27,0.27,0.27), lh=13) - 10

    fill(0, y - 15, W2, 15, CREAM)
    c.setFont('Helvetica-Bold', 7)
    c.setFillColor(rgb(GOLD))
    c.drawString(M, y - 6, 'THE 4 REASONS THIS WORKS')
    y -= 18

    reasons = [
        ('Lagos Overflow: Structural', 'Lagos is running out of affordable land. Mowe gets the largest share of overflow via the Expressway. This does not stop.'),
        ('60+ Multinationals Nearby', 'Nestle, AB InBev, CWAY, Rite Foods employ tens of thousands nearby. Workers need housing. Supply is short. Your land wins.'),
        ('RCCG City Anchor', '2,500 hectares. 200,000 residents. 197 countries of RCCG membership. Millions of annual visitors. Demand only grows.'),
        ('Lagos-Ogun MOU Signed', 'Two state governments committed to joint roads, waterworks, rail and waterways. Government money follows. Property values follow.'),
    ]
    col_w = (CW - 8) / 2
    row_h = 34
    for i, (rt, rb) in enumerate(reasons):
        col = i % 2
        row = i // 2
        rx = M + col * (col_w + 8)
        ry = y - (row + 1) * (row_h + 4)
        fill(rx, ry, col_w, row_h, CREAM)
        c.setFillColor(rgb(GOLD))
        c.rect(rx, ry, 2, row_h, fill=1, stroke=0)
        c.setFont('Helvetica-Bold', 8)
        c.setFillColor(rgb(GREEN))
        c.drawString(rx+5, ry+row_h-9, rt)
        c.setFont('Helvetica', 7)
        c.setFillColor(rgb(MUTED))
        for bi, bl in enumerate(simpleSplit(rb, 'Helvetica', 7, col_w-10)[:3]):
            c.drawString(rx+5, ry+row_h-17-bi*8, bl)

    y -= 2 * (row_h + 4) + 12

    # PAGE 2
    c.showPage()
    y = H2 - M

    fill(0, H2 - 105, W2, 105, GREEN)
    c.setFont('Helvetica-Bold', 7)
    c.setFillColor(rgb(GOLD))
    c.drawString(M, y - 4, 'ALLOCATION TIERS')
    y -= 14
    c.setFont('Helvetica-Bold', 15)
    c.setFillColor(rgb(WHITE))
    c.drawString(M, y, 'Pick Your Entry Point')
    y -= 12

    tier = d.get('tier', 'both')
    if tier == 'standard':
        tiers_data = [('Recommended For You', 'N8M', '300 SQM - 50ft x 60ft')]
    elif tier == 'premium':
        tiers_data = [('Recommended For You', 'N15M', '500 SQM - 60ft x 100ft')]
    else:
        tiers_data = [('Standard', 'N8M', '300 SQM - 50ft x 60ft'), ('Premium', 'N15M', '500 SQM - 60ft x 100ft')]

    tw = CW if len(tiers_data) == 1 else (CW - 10) / 2
    docs_list = ['C of O Backed Title','Deed of Assignment','Registered Survey Plan','Contract of Sale','Allocation Letter + Receipt']

    for i, (tlbl, tprice, tsize) in enumerate(tiers_data):
        tx = M + i * (tw + 10)
        ty = y - 52
        c.setFillColor(rgb((0.18, 0.44, 0.27)))
        c.setStrokeColor(rgb(GOLD))
        c.rect(tx, ty, tw, 52, fill=1, stroke=1)
        c.setFont('Helvetica-Bold', 7)
        c.setFillColor(rgb(GOLD))
        c.drawString(tx+6, ty+44, tlbl.upper())
        c.setFont('Helvetica-Bold', 20)
        c.setFillColor(rgb(WHITE))
        c.drawString(tx+6, ty+30, tprice)
        c.setFont('Helvetica', 8)
        c.setFillColor(rgb((0.65,0.65,0.65)))
        c.drawString(tx+6, ty+20, tsize)
        c.setFont('Helvetica', 7)
        c.setFillColor(rgb((0.72,0.72,0.72)))
        for di, dl in enumerate(docs_list):
            c.drawString(tx+6, ty+12-di*8, '- '+dl)

    y -= 58
    fill(M, y-18, CW, 18, (0.1, 0.3, 0.2))
    c.setFont('Helvetica-Bold', 8)
    c.setFillColor(rgb(GOLD))
    c.drawString(M+4, y-8, 'Pay Outright')
    c.setFont('Helvetica', 8)
    c.setFillColor(rgb((0.72,0.72,0.72)))
    c.drawString(M+58, y-8, 'for instant allocation | ')
    c.setFont('Helvetica-Bold', 8)
    c.setFillColor(rgb(GOLD))
    c.drawString(M+148, y-8, '6 Months Interest-Free:')
    c.setFont('Helvetica', 8)
    c.setFillColor(rgb((0.72,0.72,0.72)))
    c.drawString(M+262, y-8, ' deposit from N2M, balance monthly.')
    c.setFont('Helvetica', 6.5)
    c.setFillColor(rgb((0.55,0.55,0.55)))
    c.drawString(M+4, y-15, 'Account: Land Republic Limited | 78 Finance Co or 78 MFB | 0001549819')
    y -= 28

    c.setFont('Helvetica-Bold', 7)
    c.setFillColor(rgb(GOLD))
    c.drawString(M, y-4, 'HOW IT COMPARES')
    y -= 14
    c.setFont('Helvetica-Bold', 12)
    c.setFillColor(rgb(GREEN))
    c.drawString(M, y, 'Mowe Prime vs. The Market')
    y -= 10

    col_ws = [100,80,70,75]
    headers = ['Location','Price Range','Title','5-Yr Potential']
    fill(M, y-14, CW, 14, GREEN)
    cx = M
    for hi, hdr in enumerate(headers):
        c.setFont('Helvetica-Bold', 7)
        c.setFillColor(rgb(GOLD))
        c.drawString(cx+3, y-9, hdr.upper())
        cx += col_ws[hi]
    y -= 14

    rows = [
        ('Mowe Prime','N8M to N15M','C of O','300 to 450%',True),
        ('Magboro','N18M+','Varies','N/A',False),
        ('Ibadan (Bodija)','N40M+','Varies','N/A',False),
        ('Abuja (Gwarinpa)','N80M+','Varies','N/A',False),
        ('Lagos (VI)','N180M+','C of O','Saturated',False)
    ]
    for ri, (loc, price, title_c, pot, hl) in enumerate(rows):
        bg = (0.96,0.93,0.87) if hl else ((0.98,0.97,0.95) if ri%2==0 else WHITE)
        fill(M, y-14, CW, 14, bg)
        cx = M
        for vi, val in enumerate([loc,price,title_c,pot]):
            c.setFont('Helvetica-Bold' if hl else 'Helvetica', 8)
            c.setFillColor(rgb(GREEN if hl else (0.27,0.27,0.27)))
            c.drawString(cx+3, y-9, val)
            cx += col_ws[vi]
        y -= 14
    y -= 10

    c.setFillColor(rgb(GOLD))
    c.rect(M, y-4, CW, 4, fill=1, stroke=0)
    y -= 10
    c.setFont('Helvetica-Bold', 7)
    c.setFillColor(rgb(GOLD))
    c.drawString(M, y-4, 'ALSO COMING TO MOWE PRIME')
    y -= 14
    c.setFont('Helvetica-Bold', 12)
    c.setFillColor(rgb(GREEN))
    c.drawString(M, y, 'Modern Bungalows. Move-In Ready. On the Same Land.')
    y -= 10
    bung_intro = 'Beyond the land plots, we are developing modern 2-bedroom and 3-bedroom bungalows right here within Mowe Prime. Clean, contemporary structures built to a high finish standard, designed for the quality of life that this corridor now commands.'
    y = wrap(bung_intro, M, y, CW, size=9, col=(0.27,0.27,0.27), lh=13) - 8

    bung_items = [
        ('2-Bedroom Bungalow','Compact, modern, and efficient. Ideal for young families, rental income plays, or a personal property with strong resale upside as the corridor matures.'),
        ('3-Bedroom Bungalow','More space, more comfort, more value. Perfect for those wanting a ready-made home without the stress of building, or investors targeting higher rental yields.')
    ]
    bh = 36
    bw2 = (CW-8)/2
    for i,(bt,bb) in enumerate(bung_items):
        bx = M+i*(bw2+8)
        by = y-bh
        fill(bx, by, bw2, bh, CREAM)
        c.setFillColor(rgb(GOLD))
        c.rect(bx, by+bh-2, bw2, 2, fill=1, stroke=0)
        c.setFont('Helvetica-Bold',9)
        c.setFillColor(rgb(GREEN))
        c.drawString(bx+5, by+bh-11, bt)
        c.setFont('Helvetica',7)
        c.setFillColor(rgb(MUTED))
        for bi2,bl2 in enumerate(simpleSplit(bb,'Helvetica',7,bw2-10)[:4]):
            c.drawString(bx+5, by+bh-20-bi2*8, bl2)
    y -= bh+6

    fill(M, y-30, CW, 30, GREEN)
    c.setFont('Helvetica-Bold',8)
    c.setFillColor(rgb(GOLD))
    c.drawString(M+4, y-10, 'Why this lifts your investment:')
    c.setFont('Helvetica',7.5)
    c.setFillColor(rgb((0.78,0.78,0.78)))
    note_txt = 'Modern finished homes within the estate directly raise the value of surrounding land. Your plot benefits whether you build or not. If a bungalow interests you, reach out and we will walk you through the details.'
    for ni,nl in enumerate(simpleSplit(note_txt,'Helvetica',7.5,CW-12)[:3]):
        c.drawString(M+4, y-18-ni*9, nl)
    y -= 38

    cta_h = max(y - M, 85)
    fill(0, M, W2, cta_h, GOLD)
    c.setFont('Helvetica-Bold',17)
    c.setFillColor(rgb(GREEN))
    hl2_lines = simpleSplit(cta_hl,'Helvetica-Bold',17,CW)
    cy = M + cta_h - 16
    for hl2 in hl2_lines:
        c.drawString(M, cy, hl2)
        cy -= 21

    c.setFont('Helvetica',9)
    c.setFillColor(rgb((0.1,0.25,0.15)))
    for cl in simpleSplit(cta_txt,'Helvetica',9,CW):
        c.drawString(M, cy, cl)
        cy -= 12
    cy -= 6

    contacts = [
        ('CALL / WHATSAPP', d.get('phone','+234 903 349 9271')),
        ('EMAIL', d.get('email','Israel@landrepublic.co')),
        ('VIEW PROPERTY', d.get('url','landrepublic.co/mowe-prime'))
    ]
    bw3 = 150
    for ci2,(clbl,cval) in enumerate(contacts):
        bx2 = M + ci2*(bw3+8)
        fill(bx2, cy-20, bw3, 20, GREEN)
        c.setFont('Helvetica-Bold',6)
        c.setFillColor(rgb(GOLD))
        c.drawString(bx2+5, cy-9, clbl)
        c.setFont('Helvetica',8)
        c.setFillColor(rgb(WHITE))
        c.drawString(bx2+5, cy-17, cval)
    cy -= 28
    c.setFont('Helvetica',7.5)
    c.setFillColor(rgb((0.1,0.22,0.13)))
    c.drawString(M, cy, "Prepared by " + d.get('agent','Israel Olaleye') + " | @asset_by_israel | Your Favorite Real Estate Consultant")

    c.save()
    buf.seek(0)
    return buf


DEFAULT = dict(title='', fname='', job='', goal='build wealth', type='home', tier='both',
               agent='Israel Olaleye', phone='+234 903 349 9271',
               email='Israel@landrepublic.co', url='landrepublic.co/mowe-prime')

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML, d=DEFAULT, preview=False,
                                  headline='', hero_sub='', body_hl='', body_text='',
                                  cta_hl='', cta_txt='')

@app.route('/generate', methods=['POST'])
def generate():
    d = {k: request.form.get(k, DEFAULT[k]) for k in DEFAULT}
    action = request.form.get('action', 'preview')
    pt = d['title'].strip()
    fn = d['fname'].strip()
    if pt and fn: full = pt + ' ' + fn
    elif pt: full = pt
    elif fn: full = fn
    else: full = 'You'
    headline = (full + ', This Land Was Made for People Like You') if full != 'You' else 'A Land Investment Built Around Your Goals'
    hero_sub = (d['job'] + 's who want to ' + d['goal'] + ' are exactly who Mowe Prime was built for.') if d['job'] else "Mowe Prime - C of O titled land, 29km from Lagos, inside Nigeria's fastest-appreciating real estate corridor."
    body_hl = 'Your Naira Is Losing Ground. This Land Is Gaining It.' if d['type'] == 'diaspora' else 'Mowe Has Already Arrived. The Price Has Not.'
    body_text = get_body(d['goal'], fn or pt or '')
    cta_hl = (full + ', This Is Your Move. Make It.') if full != 'You' else 'This Is Your Move. Make It.'
    cta_txt = 'Everything can be completed remotely. Documents are processed and issued in your name. One call or message is all it takes. Do not leave this for later.' if d['type'] == 'diaspora' else 'The land is real. The title is clean. The corridor is active. One conversation is all it takes to get your allocation started. Reach out today.'
    if action == 'pdf':
        buf = build_pdf(d)
        fname_clean = (full.replace(' ', '-') + '-') if full != 'You' else ''
        return send_file(buf, mimetype='application/pdf', as_attachment=True,
                         download_name='Mowe-Prime-Pitch-' + fname_clean + '.pdf')
    return render_template_string(HTML, d=d, preview=True, headline=headline, hero_sub=hero_sub,
                                  body_hl=body_hl, body_text=body_text, cta_hl=cta_hl, cta_txt=cta_txt)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
