"""
Mowe Prime Pitch Generator - Corrected & Upgraded
Run: python3 mowe_prime_app.py
Then open: http://localhost:5000

Requirements: pip install flask reportlab
"""

from flask import Flask, request, send_file, render_template_string
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import io

app = Flask(__name__)

W, H = A4
GREEN  = (13/255, 43/255, 30/255)
DKGRN  = (8/255, 28/255, 18/255)
GOLD   = (200/255, 168/255, 75/255)
GOLD2  = (232/255, 201/255, 107/255)
CREAM  = (247/255, 243/255, 236/255)
WHITE  = (1, 1, 1)
DARK   = (0.18, 0.18, 0.18)
MUTED  = (0.42, 0.42, 0.42)
LGRAY  = (0.93, 0.91, 0.87)

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
.btn:active{background:#b8962e;}
.note{font-size:12px;color:#888;font-style:italic;}

/* ---- PREVIEW STYLES ---- */
.preview-box{max-width:820px;margin:0 auto;padding:0 16px 60px;}
.pv-card{background:#fff;border-radius:6px;border:1px solid #e0d9cc;overflow:hidden;}

/* HERO */
.pv-hero{background:#0d2b1e;padding:44px 40px 36px;position:relative;overflow:hidden;}
.pv-hero::before{content:'MOWE PRIME';position:absolute;font-size:100px;font-weight:700;color:rgba(200,168,75,0.05);right:-10px;top:8px;white-space:nowrap;pointer-events:none;letter-spacing:4px;}
.pv-tag{display:inline-block;font-size:8px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#c8a84b;border:1px solid rgba(200,168,75,0.4);padding:4px 12px;border-radius:2px;margin-bottom:18px;}
.pv-hero h2{font-size:clamp(20px,3.2vw,30px);font-weight:700;color:#fff;line-height:1.22;margin-bottom:12px;}
.pv-hero p{font-size:12px;color:rgba(255,255,255,0.58);line-height:1.7;max-width:480px;}

/* STATS */
.stat-row{background:#c8a84b;display:flex;flex-wrap:wrap;}
.stat-cell{flex:1 1 80px;text-align:center;padding:12px 8px;border-right:1px solid rgba(13,43,30,0.18);}
.stat-cell:last-child{border-right:none;}
.stat-v{display:block;font-size:18px;font-weight:700;color:#0d2b1e;line-height:1;}
.stat-l{display:block;font-size:7px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:rgba(13,43,30,0.6);margin-top:3px;}

/* SECTIONS */
.pv-sec{padding:28px 40px;border-bottom:1px solid #e0d9cc;background:#fff;}
.pv-sec.cream{background:#f7f3ec;}
.pv-sec.dark{background:#0d2b1e;}
.pv-sec.gold-bg{background:#c8a84b;}
.slbl{font-size:8px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:#c8a84b;margin-bottom:10px;display:block;}
.pv-sec.dark .slbl{color:#e8c96b;}
.pv-sec h3{font-size:18px;font-weight:700;color:#0d2b1e;margin-bottom:12px;line-height:1.3;}
.pv-sec.dark h3{color:#fff;}
.pv-sec.gold-bg h3{color:#0d2b1e;font-size:22px;}
.pv-sec p{font-size:13px;color:#3a3a3a;line-height:1.8;}
.pv-sec.dark p{color:rgba(255,255,255,0.72);}
.pv-sec.gold-bg p{color:rgba(13,43,30,0.72);}

/* WHY GRID */
.why-g{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px;}
.why-i{flex:1 1 210px;background:#fff;border-left:3px solid #c8a84b;padding:14px 16px;border-radius:0 4px 4px 0;}
.wi-t{font-size:11px;font-weight:700;color:#0d2b1e;margin-bottom:5px;}
.wi-b{font-size:11px;color:#666;line-height:1.6;}

/* TIERS */
.pg{display:flex;flex-wrap:wrap;gap:14px;margin:16px 0;}
.pi{flex:1 1 170px;border:1px solid rgba(200,168,75,0.25);border-radius:5px;padding:18px 16px;background:rgba(255,255,255,0.05);}
.pi.ft{background:rgba(200,168,75,0.14);border-color:#c8a84b;}
.pi-tag{font-size:8px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#c8a84b;margin-bottom:8px;display:block;}
.pi-pr{font-size:28px;font-weight:700;color:#fff;line-height:1;margin-bottom:5px;}
.pi-sz{font-size:11px;color:rgba(255,255,255,0.45);margin-bottom:12px;}
.pi-dc{font-size:11px;color:rgba(255,255,255,0.65);line-height:1.8;}
.pmn{background:rgba(200,168,75,0.1);border:1px solid rgba(200,168,75,0.3);border-radius:3px;padding:12px 16px;font-size:12px;color:rgba(255,255,255,0.72);line-height:1.7;}
.pmn strong{color:#c8a84b;}

/* COMPARISON TABLE */
.ctbl{width:100%;border-collapse:collapse;margin-top:14px;font-size:12px;}
.ctbl th{background:#0d2b1e;color:#c8a84b;font-size:8px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;padding:9px 12px;text-align:left;}
.ctbl td{padding:9px 12px;border-bottom:1px solid #e0d9cc;color:#3a3a3a;}
.ctbl tr.hl td{background:rgba(200,168,75,0.1);font-weight:700;color:#0d2b1e;}
.ctbl tr.ev td{background:#faf8f4;}
.bdg{display:inline-block;font-size:10px;font-weight:700;padding:2px 7px;border-radius:20px;}
.bg{background:#d4edda;color:#155724;}.br{background:#f8d7da;color:#721c24;}.by{background:#fff3cd;color:#856404;}

/* BUNGALOWS */
.bg2{display:flex;flex-wrap:wrap;gap:14px;margin:16px 0;}
.bi{flex:1 1 195px;background:#fff;border:1px solid #e0d9cc;border-top:3px solid #c8a84b;border-radius:0 0 5px 5px;padding:18px 16px;}
.bi-t{font-size:14px;font-weight:700;color:#0d2b1e;margin-bottom:8px;}
.bi-b{font-size:12px;color:#666;line-height:1.7;}
.bn{background:#0d2b1e;border-radius:4px;padding:16px 18px;font-size:12px;color:rgba(255,255,255,0.75);line-height:1.75;}
.bn strong{color:#c8a84b;}

/* CTA */
.ctact{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 4px;}
.ci{background:#0d2b1e;border-radius:3px;padding:10px 16px;display:flex;align-items:center;gap:8px;}
.ci-l{font-size:8px;font-weight:700;letter-spacing:1.8px;text-transform:uppercase;color:#c8a84b;display:block;margin-bottom:2px;}
.ci-v{font-size:12px;color:#fff;font-weight:500;}
.sig{margin-top:16px;font-size:11px;color:rgba(13,43,30,0.55);}

@media(max-width:560px){.pv-hero,.pv-sec{padding:22px 18px;}.field{flex:1 1 100%;}.stat-v{font-size:14px;}}
</style>
</head>
<body>
<div class="hdr">
  <h1>Mowe Prime Pitch Generator</h1>
  <p>Fill in the fields below, preview your personalised pitch, then download a full-colour PDF instantly.</p>
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
          <option value="standard" {% if d.tier=='standard' %}selected{% endif %}>Standard (N8M / 300 sqm)</option>
          <option value="premium" {% if d.tier=='premium' %}selected{% endif %}>Premium (N15M / 500 sqm)</option>
        </select>
      </div>
    </div>
    <div class="divider"></div>
    <div class="sec-hdr">Consultant Information</div>
    <div class="grid">
      <div class="field"><label>Consultant Name</label><input name="agent" value="{{ d.agent }}"/></div>
      <div class="field"><label>Phone Number</label><input name="phone" value="{{ d.phone }}"/></div>
      <div class="field"><label>Email Address</label><input name="email" value="{{ d.email }}"/></div>
      <div class="field"><label>Property URL</label><input name="url" value="{{ d.url }}"/></div>
    </div>
    <div class="divider"></div>
    <div class="btn-row">
      <button class="btn" type="submit" name="action" value="preview">Preview Pitch</button>
      <button class="btn" type="submit" name="action" value="pdf" style="background:#0d2b1e;color:#c8a84b;">Download Coloured PDF</button>
      <span class="note">Preview first, or download directly.</span>
    </div>
  </div>
</form>
</div>

{% if preview %}
<div class="preview-box">
<div class="pv-card">

  <!-- HERO -->
  <div class="pv-hero">
    <div class="pv-tag">Private Investment Brief &nbsp;&middot;&nbsp; Asset by Israel</div>
    <h2>{{ headline }}</h2>
    <p>{{ hero_sub }}</p>
  </div>

  <!-- STATS BAR -->
  <div class="stat-row">
    <div class="stat-cell"><span class="stat-v">29km</span><span class="stat-l">From Lagos</span></div>
    <div class="stat-cell"><span class="stat-v">12-18%</span><span class="stat-l">Annual Appreciation</span></div>
    <div class="stat-cell"><span class="stat-v">200K</span><span class="stat-l">RCCG Residents</span></div>
    <div class="stat-cell"><span class="stat-v">60+</span><span class="stat-l">Multinationals</span></div>
    <div class="stat-cell"><span class="stat-v">C of O</span><span class="stat-l">Bankable Title</span></div>
  </div>

  <!-- STORY SECTION -->
  <div class="pv-sec">
    <span class="slbl">{{ full_name }}, Here Is Something Worth Knowing</span>
    <h3>{{ body_hl }}</h3>
    <p>{{ body_text }}</p>
  </div>

  <!-- WHY IT WORKS -->
  <div class="pv-sec cream">
    <span class="slbl">{{ full_name }}, These Are the Reasons I Am Bringing This to You</span>
    <div class="why-g">
      <div class="why-i"><div class="wi-t">Lagos Is Overflowing, and Mowe Gets the Largest Share</div><div class="wi-b">Lagos is running out of affordable land and what it cannot contain overflows into Mowe via the expressway. That overflow is not a trend, it is the structural reality of two cities growing toward each other, and it does not stop.</div></div>
      <div class="why-i"><div class="wi-t">60+ Multinationals Drive Constant Demand</div><div class="wi-b">Nestle, AB InBev, CWAY, Rite Foods and dozens more are all operational nearby, employing tens of thousands of workers who need housing in the same corridor. Supply of good land is already short, and your plot sits right in the middle of that demand gap.</div></div>
      <div class="why-i"><div class="wi-t">RCCG City Is an Anchor Nothing Can Replicate</div><div class="wi-b">2,500 hectares. 200,000 residents. 197 countries represented in RCCG membership. Millions of visitors every single year. This demand does not fluctuate with the economy. It only compounds.</div></div>
      <div class="why-i"><div class="wi-t">Lagos-Ogun Infrastructure MOU Has Been Signed</div><div class="wi-b">Two state governments are now committed to joint road development, waterworks, rail, and waterways in this corridor. Government money follows where government signs. And property values follow government money.</div></div>
    </div>
  </div>

  <!-- TIERS -->
  <div class="pv-sec dark">
    <span class="slbl">{{ full_name }}, We Have Two Entry Points</span>
    <h3>Pick the One That Works Best for You</h3>
    <div class="pg">
      {% if d.tier == 'standard' %}
      <div class="pi ft"><span class="pi-tag">Recommended for You</span><div class="pi-pr">N8M</div><div class="pi-sz">300 SQM &middot; 50ft x 60ft</div><div class="pi-dc">C of O Backed Title<br/>Deed of Assignment<br/>Registered Survey Plan<br/>Contract of Sale<br/>Allocation Letter + Receipt</div></div>
      {% elif d.tier == 'premium' %}
      <div class="pi ft"><span class="pi-tag">Recommended for You</span><div class="pi-pr">N15M</div><div class="pi-sz">500 SQM &middot; 60ft x 100ft</div><div class="pi-dc">C of O Backed Title<br/>Deed of Assignment<br/>Registered Survey Plan<br/>Contract of Sale<br/>Allocation Letter + Receipt</div></div>
      {% else %}
      <div class="pi"><span class="pi-tag">Standard</span><div class="pi-pr">N8M</div><div class="pi-sz">300 SQM &middot; 50ft x 60ft</div><div class="pi-dc">C of O Backed Title<br/>Deed of Assignment<br/>Registered Survey Plan<br/>Contract of Sale<br/>Allocation Letter + Receipt</div></div>
      <div class="pi ft"><span class="pi-tag">Premium</span><div class="pi-pr">N15M</div><div class="pi-sz">500 SQM &middot; 60ft x 100ft</div><div class="pi-dc">C of O Backed Title<br/>Deed of Assignment<br/>Registered Survey Plan<br/>Contract of Sale<br/>Allocation Letter + Receipt</div></div>
      {% endif %}
    </div>
    <div class="pmn"><strong>Pay Outright</strong> for instant allocation &nbsp;&middot;&nbsp; <strong>6 Months Interest-Free:</strong> deposit from N2M, balance monthly.<br/><span style="opacity:0.5;font-size:11px;">Account: Land Republic Limited &nbsp;&middot;&nbsp; 78 Finance Company or 78 MFB &nbsp;&middot;&nbsp; 0001549819</span></div>
  </div>

  <!-- COMPARISON TABLE -->
  <div class="pv-sec">
    <span class="slbl">{{ full_name }}, Let Us Do a Quick Comparison</span>
    <h3 style="font-size:15px;margin-bottom:4px;">Mowe Prime vs. The Market</h3>
    <p style="font-size:11px;color:#888;margin-bottom:0;">500 to 600 SQM residential plot, comparable axis</p>
    <table class="ctbl">
      <thead><tr><th>Location</th><th>Price Range</th><th>Title</th><th>5-Yr Potential</th></tr></thead>
      <tbody>
        <tr class="hl"><td>Mowe Prime</td><td>N8M to N15M</td><td><span class="bdg bg">C of O</span></td><td><span class="bdg bg">300 to 450%</span></td></tr>
        <tr><td>Magboro</td><td>N18M+</td><td><span class="bdg by">Varies</span></td><td>N/A</td></tr>
        <tr class="ev"><td>Ibadan (Bodija)</td><td>N40M+</td><td><span class="bdg by">Varies</span></td><td>N/A</td></tr>
        <tr><td>Abuja (Gwarinpa)</td><td>N80M+</td><td><span class="bdg by">Varies</span></td><td>N/A</td></tr>
        <tr class="ev"><td>Lagos (VI)</td><td>N180M+</td><td><span class="bdg bg">C of O</span></td><td><span class="bdg br">Saturated</span></td></tr>
      </tbody>
    </table>
  </div>

  <!-- BUNGALOWS -->
  <div class="pv-sec cream" style="border-top:4px solid #c8a84b;">
    <span class="slbl">{{ full_name }}, There Is One More Thing</span>
    <h3>Modern Bungalows Are Also Coming to Mowe Prime</h3>
    <p style="margin-bottom:14px;">We are not just selling land in this estate. We are also building modern 2-bedroom and 3-bedroom bungalows, right here within Mowe Prime, and they are coming in soon. These are clean, contemporary structures built to a high finish standard, on good road networks, in a well laid-out estate with functioning security, an operational school, its own internal transportation system, and over 100 existing homes with residents already living in the community. You are not buying into an open field. You are buying into a place that already works.</p>
    <div class="bg2">
      <div class="bi"><div class="bi-t">2-Bedroom Bungalow</div><div class="bi-b">Compact, modern, and efficient. Ideal for young families, rental income plays, or a personal property with strong resale upside as the corridor matures.</div></div>
      <div class="bi"><div class="bi-t">3-Bedroom Bungalow</div><div class="bi-b">More space, more comfort, more value. Perfect for those who want a ready-made home without the stress of building, or investors targeting higher rental yields.</div></div>
    </div>
    <div class="bn"><strong>Why this matters for your land:</strong> Modern finished homes within the same estate directly push up the value of surrounding land. Your plot benefits whether you build or not. And if a bungalow interests you as well, we can also build one for you. Just mention it and we will walk you through what that looks like.</div>
  </div>

  <!-- CTA -->
  <div class="pv-sec gold-bg" style="border-radius:0 0 6px 6px;">
    <h3>{{ cta_hl }}</h3>
    <p>{{ cta_txt }}</p>
    <div class="ctact">
      <div class="ci"><div><span class="ci-l">Call / WhatsApp</span><span class="ci-v">{{ d.phone }}</span></div></div>
      <div class="ci"><div><span class="ci-l">Email</span><span class="ci-v">{{ d.email }}</span></div></div>
      <div class="ci"><div><span class="ci-l">View Property</span><span class="ci-v">{{ d.url }}</span></div></div>
    </div>
    <p class="sig">Prepared by <strong>{{ d.agent }}</strong> &nbsp;&middot;&nbsp; @asset_by_israel &nbsp;&middot;&nbsp; Your Favorite Real Estate Consultant</p>
  </div>

</div>
</div>
{% endif %}
</body>
</html>
"""


def get_body(goal, name):
    prefix = name + ", " if name else ""
    m = {
        'build wealth': (
            f"Some years ago, Mowe was largely an agricultural zone, a stretch of farmland that most Lagosians drove past without a second thought. "
            f"A few early buyers saw something different and acquired land there quietly, and they were mostly companies, multinationals from India, China, and across West Africa "
            f"that were buying in bulk, holding the land, and beginning to develop. Then the Lagos-Ibadan Expressway rehabilitation came in and it changed everything. "
            f"The corridor opened up, infrastructure followed commerce, and Mowe transformed from a transit point into a destination in its own right. "
            f"The people who bought ten years ago now sit on assets worth multiples of what they paid. And the trajectory has not stalled. "
            f"It has accelerated, because Lagos is now saturated and the only affordable, titled land with direct expressway access to Lagos sits on this exact corridor. "
            f"That is why I am bringing this to you, {name + '.' if name else 'you.'} "
            f"Mowe Prime is a C of O-backed land opportunity positioned 29km from Lagos, inside a functioning estate that already has residents, schools, security, and its own transport system. "
            f"It is not speculative. It is the second great window on a corridor that the first wave of buyers already validated."
        ),
        'secure land': (
            f"Some years ago, Mowe was largely farmland that most people drove past without a second glance. A few quiet buyers saw what was coming and secured land at prices that feel almost impossible today. "
            f"Then the Lagos-Ibadan Expressway came in and opened everything up, multinationals moved in along the corridor, RCCG built an entire city right there, "
            f"and the people who bought early now hold assets worth multiples of what they paid. "
            f"Another window like that is open right now, {name + ',' if name else ''} and it will not stay open much longer. "
            f"Every month, more titled land in this corridor gets absorbed. Mowe Prime still offers C of O-backed plots at a fraction of Lagos prices, "
            f"inside a functioning estate with existing residents, schools, and security already in place. "
            f"The legal title is clean. The corridor is active. And the price is still at a point where future appreciation will be significant."
        ),
        'invest idle funds': (
            f"Idle naira loses real value every single month, and the choice is always the same: park it somewhere it works, or watch inflation quietly erode it. "
            f"Mowe Prime sits on a corridor that has appreciated at 12 to 18 percent annually, documented, and it is backed by C of O title, "
            f"which means the asset is bankable, transferable, and legally airtight. "
            f"Around it, Nestle, AB InBev, CWAY, Rite Foods, and over 60 active multinationals have locked their operations into the same area, "
            f"RCCG has built a 2,500-hectare city with 200,000 residents, and two state governments have signed a joint infrastructure MOU to develop roads, rail, and waterways in the corridor. "
            f"That is not a promotional narrative, {name + ',' if name else ''} that is money, institutions, and government all pointing in the same direction. "
            f"Land here does not crash overnight. It does not disappear. And when you are ready to exit, the demand is already there waiting."
        ),
        'diaspora property': (
            f"Owning property in Nigeria from abroad should not feel like a gamble, and with Mowe Prime it does not have to. "
            f"The title is C of O, the highest land title possible, and everything, documents, deed, survey, is processed and issued in your name. "
            f"Land Republic is registered in both Nigeria and Delaware, so the legal structure holds in both worlds. "
            f"The corridor itself is not a bet on something that might happen. It is a functioning economic zone, "
            f"with 60+ active multinationals, 200,000 RCCG residents, a signed interstate infrastructure MOU, and consistent 12 to 18 percent annual appreciation on record. "
            f"You do not need to be on the ground to own here, {name + ',' if name else ''} and the corridor keeps compounding value whether you are in London, Houston, or Lagos."
        ),
        'diversify': (
            f"Every serious portfolio needs at least one asset that is not correlated to stock markets or currency swings, and C of O-backed land 29km from Lagos is exactly that. "
            f"Mowe Prime sits in one of Nigeria's most structurally supported real estate corridors: over 60 active multinationals nearby, "
            f"RCCG's 2,500-hectare city with 200,000 residents, a signed Lagos-Ogun infrastructure MOU, and documented 12 to 18 percent annual appreciation. "
            f"It is a non-correlated, appreciating hard asset, {name + ',' if name else ''} and it will not move with Dangote shares or drop when crypto corrects. "
            f"That is the kind of weight a strong portfolio needs to stay balanced when everything else is volatile."
        ),
        'build a home': (
            f"Mowe Prime is designed to let you build at your own pace and on your own terms. No deadline. No pressure to start on day one. "
            f"C of O title means bank financing is accessible the moment you are ready to build, and the corridor keeps pushing your land value higher whether you have broken ground or not. "
            f"But here is what makes this different from most land opportunities, {name + ',' if name else ''} you are not buying into an empty field. "
            f"You are entering a functioning estate that already has residents, an operational school, its own internal transportation, and 24-hour security. "
            f"The community is already alive. You are simply adding your home to a place that is already working."
        ),
    }
    return m.get(goal, m['build wealth'])


def get_cta(full, ctype):
    if ctype == 'diaspora':
        txt = (
            f"The land is real, the title is clean, the corridor is active, and everything can be completed remotely. "
            f"Documents are processed and registered in your name from wherever you are. "
            f"It only takes one conversation to get your allocation started and get your own plot secured. Reach out today."
        )
    else:
        txt = (
            f"The land is real, the title is clean, the corridor is active, and the environment around it is growing. "
            f"It only takes one conversation to get your allocation started and get your own plot secured. Reach out today."
        )
    return txt


def rgb(t):
    from reportlab.lib import colors as rlc
    return rlc.Color(t[0], t[1], t[2])


def build_pdf(d):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas as rl_canvas
    from reportlab.lib.utils import simpleSplit

    W2, H2 = A4
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=A4)
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
        if lh is None:
            lh = size * 1.5
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
    if pt and fn:
        full = pt + ' ' + fn
    elif pt:
        full = pt
    elif fn:
        full = fn
    else:
        full = 'You'

    hero_hl = (full + ', This Land Was Built for Someone with Your Eye for Opportunity') if full != 'You' else 'A Land Opportunity Built Around Your Goals'
    hero_sub = (
        d.get('job', '') + 's who want to ' + d.get('goal', 'build wealth') + ' are exactly who Mowe Prime was positioned for.'
    ) if d.get('job') else 'Mowe Prime: C of O titled land, 29km from Lagos, inside an already-functioning estate in Nigeria\'s fastest-appreciating corridor.'

    body_hl = (
        'Your Naira Is Losing Ground Every Month, but This Land Is Gaining It.'
        if d.get('type') == 'diaspora'
        else 'Mowe Has Already Arrived, but Permit Me to Say the Price Has Not Fully Arrived Yet.'
    )
    body_text = get_body(d.get('goal', 'build wealth'), fn or pt or '')
    cta_hl = (full + ', This Is Your Move, Make It') if full != 'You' else 'This Is Your Move, Make It'
    cta_txt = get_cta(full, d.get('type', 'home'))

    # ---- PAGE 1 ----
    hero_h = 148
    fill(0, H2 - hero_h, W2, hero_h, GREEN)

    # Watermark text
    c.saveState()
    c.setFont('Helvetica-Bold', 72)
    c.setFillColor(rgb((200/255, 168/255, 75/255)))
    c.setFillAlpha(0.04)
    c.drawString(W2 * 0.25, H2 - 80, 'MOWE PRIME')
    c.restoreState()

    # Hero badge
    c.setFont('Helvetica-Bold', 7)
    c.setFillColor(rgb(GOLD))
    c.drawString(M, H2 - 14, 'PRIVATE INVESTMENT BRIEF   |   ASSET BY ISRAEL')

    # Hero headline
    c.setFont('Helvetica-Bold', 18)
    c.setFillColor(rgb(WHITE))
    hl_lines = simpleSplit(hero_hl, 'Helvetica-Bold', 18, CW)
    hy = H2 - 34
    for line in hl_lines:
        c.drawString(M, hy, line)
        hy -= 22

    # Hero sub
    c.setFont('Helvetica', 9)
    c.setFillColor(rgb((0.62, 0.62, 0.62)))
    for line in simpleSplit(hero_sub, 'Helvetica', 9, CW):
        c.drawString(M, hy, line)
        hy -= 13

    # Stats bar
    sb_y = H2 - hero_h - 26
    fill(0, sb_y, W2, 26, GOLD)
    stats = [('29km', 'FROM LAGOS'), ('12-18%', 'ANN. APPREC.'), ('200K', 'RCCG RESID.'), ('60+', 'MULTINATLS'), ('C of O', 'TITLE')]
    sw = W2 / len(stats)
    for i, (val, lbl) in enumerate(stats):
        cx = i * sw + sw / 2
        c.setFont('Helvetica-Bold', 11)
        c.setFillColor(rgb(GREEN))
        c.drawCentredString(cx, sb_y + 15, val)
        c.setFont('Helvetica', 5.5)
        c.setFillColor(rgb((0.15, 0.32, 0.22)))
        c.drawCentredString(cx, sb_y + 7, lbl)

    y = sb_y - 10

    # Section: Story
    fill(0, y - 18, W2, 18, LGRAY)
    c.setFont('Helvetica-Bold', 7)
    c.setFillColor(rgb(GOLD))
    c.drawString(M, y - 7, (full.upper() + ', HERE IS SOMETHING WORTH KNOWING').replace('YOU', '').strip() if full != 'You' else 'HERE IS SOMETHING WORTH KNOWING')
    y -= 22

    y = wrap(body_hl, M, y - 6, CW, size=14, bold=True, col=GREEN, lh=18) - 6
    y = wrap(body_text, M, y, CW, size=9, col=DARK, lh=13) - 10

    # Section: Why It Works
    fill(0, y - 16, W2, 16, CREAM)
    c.setFont('Helvetica-Bold', 7)
    c.setFillColor(rgb(GOLD))
    name_lbl = (full.upper() + ', ') if full != 'You' else ''
    c.drawString(M, y - 7, name_lbl + 'THE REASONS I AM BRINGING THIS TO YOU')
    y -= 20

    reasons = [
        ('Lagos Overflow: Structural', 'Lagos is running out of affordable land. Mowe gets the largest share via the Expressway. It does not stop.'),
        ('60+ Multinationals Nearby', 'Nestle, AB InBev, CWAY, Rite Foods and dozens more. Tens of thousands employed. Workers need housing. Your land benefits.'),
        ('RCCG City Anchor', '2,500 hectares. 200,000 residents. 197 countries of RCCG membership. Millions of visitors annually. This demand only grows.'),
        ('Lagos-Ogun MOU Signed', 'Two state governments committed to joint roads, waterworks, rail and waterways. Government money follows. Property values follow.'),
    ]
    col_w = (CW - 8) / 2
    row_h = 38
    for i, (rt, rb) in enumerate(reasons):
        col = i % 2
        row = i // 2
        rx = M + col * (col_w + 8)
        ry = y - (row + 1) * (row_h + 4)
        fill(rx, ry, col_w, row_h, CREAM)
        c.setFillColor(rgb(GOLD))
        c.rect(rx, ry, 2.5, row_h, fill=1, stroke=0)
        c.setFont('Helvetica-Bold', 8)
        c.setFillColor(rgb(GREEN))
        c.drawString(rx + 6, ry + row_h - 10, rt)
        c.setFont('Helvetica', 7)
        c.setFillColor(rgb(MUTED))
        lines = simpleSplit(rb, 'Helvetica', 7, col_w - 12)[:3]
        for bi, bl in enumerate(lines):
            c.drawString(rx + 6, ry + row_h - 19 - bi * 8.5, bl)

    y -= 2 * (row_h + 4) + 14

    # ---- PAGE 2 ----
    c.showPage()
    y = H2 - M

    # Tiers header block
    fill(0, H2 - 108, W2, 108, GREEN)
    c.setFont('Helvetica-Bold', 7)
    c.setFillColor(rgb(GOLD))
    c.drawString(M, y - 4, (full.upper() + ', ') if full != 'You' else '' + 'WE HAVE TWO ENTRY POINTS')
    y -= 16
    c.setFont('Helvetica-Bold', 16)
    c.setFillColor(rgb(WHITE))
    c.drawString(M, y, 'Pick the One That Works Best for You')
    y -= 14

    tier = d.get('tier', 'both')
    if tier == 'standard':
        tiers_data = [('Recommended for You', 'N8M', '300 SQM / 50ft x 60ft')]
    elif tier == 'premium':
        tiers_data = [('Recommended for You', 'N15M', '500 SQM / 60ft x 100ft')]
    else:
        tiers_data = [('Standard', 'N8M', '300 SQM / 50ft x 60ft'), ('Premium', 'N15M', '500 SQM / 60ft x 100ft')]

    tw = CW if len(tiers_data) == 1 else (CW - 12) / 2
    docs_list = ['C of O Backed Title', 'Deed of Assignment', 'Registered Survey Plan', 'Contract of Sale', 'Allocation Letter + Receipt']

    for i, (tlbl, tprice, tsize) in enumerate(tiers_data):
        tx = M + i * (tw + 12)
        ty = y - 56
        c.setFillColor(rgb((0.15, 0.42, 0.26)))
        c.setStrokeColor(rgb(GOLD))
        c.rect(tx, ty, tw, 56, fill=1, stroke=1)
        c.setFont('Helvetica-Bold', 7)
        c.setFillColor(rgb(GOLD))
        c.drawString(tx + 6, ty + 47, tlbl.upper())
        c.setFont('Helvetica-Bold', 22)
        c.setFillColor(rgb(WHITE))
        c.drawString(tx + 6, ty + 32, tprice)
        c.setFont('Helvetica', 8)
        c.setFillColor(rgb((0.62, 0.62, 0.62)))
        c.drawString(tx + 6, ty + 22, tsize)
        c.setFont('Helvetica', 7)
        c.setFillColor(rgb((0.70, 0.70, 0.70)))
        for di, dl in enumerate(docs_list):
            c.drawString(tx + 6, ty + 13 - di * 8, '+ ' + dl)

    y -= 62

    # Payment note
    fill(M, y - 20, CW, 20, (0.08, 0.28, 0.18))
    c.setFont('Helvetica-Bold', 8)
    c.setFillColor(rgb(GOLD))
    c.drawString(M + 5, y - 9, 'Pay Outright')
    c.setFont('Helvetica', 8)
    c.setFillColor(rgb((0.70, 0.70, 0.70)))
    c.drawString(M + 72, y - 9, 'for instant allocation   |   ')
    c.setFont('Helvetica-Bold', 8)
    c.setFillColor(rgb(GOLD))
    c.drawString(M + 164, y - 9, '6 Months Interest-Free:')
    c.setFont('Helvetica', 8)
    c.setFillColor(rgb((0.70, 0.70, 0.70)))
    c.drawString(M + 278, y - 9, 'deposit from N2M, balance monthly.')
    c.setFont('Helvetica', 6.5)
    c.setFillColor(rgb((0.52, 0.52, 0.52)))
    c.drawString(M + 5, y - 17, 'Account: Land Republic Limited   |   78 Finance Co or 78 MFB   |   0001549819')
    y -= 30

    # Comparison
    c.setFont('Helvetica-Bold', 7)
    c.setFillColor(rgb(GOLD))
    c.drawString(M, y - 4, ((full.upper() + ', ') if full != 'You' else '') + 'LET US DO A QUICK COMPARISON')
    y -= 14
    c.setFont('Helvetica-Bold', 13)
    c.setFillColor(rgb(GREEN))
    c.drawString(M, y, 'Mowe Prime vs. The Market')
    y -= 10

    col_ws = [108, 80, 68, 78]
    headers = ['Location', 'Price Range', 'Title', '5-Yr Potential']
    fill(M, y - 14, CW, 14, GREEN)
    cx = M
    for hi, hdr in enumerate(headers):
        c.setFont('Helvetica-Bold', 7)
        c.setFillColor(rgb(GOLD))
        c.drawString(cx + 3, y - 9, hdr.upper())
        cx += col_ws[hi]
    y -= 14

    rows = [
        ('Mowe Prime', 'N8M to N15M', 'C of O', '300 to 450%', True),
        ('Magboro', 'N18M+', 'Varies', 'N/A', False),
        ('Ibadan (Bodija)', 'N40M+', 'Varies', 'N/A', False),
        ('Abuja (Gwarinpa)', 'N80M+', 'Varies', 'N/A', False),
        ('Lagos (VI)', 'N180M+', 'C of O', 'Saturated', False),
    ]
    for ri, (loc, price, title_c, pot, hl) in enumerate(rows):
        bg = (0.96, 0.93, 0.87) if hl else ((0.98, 0.97, 0.95) if ri % 2 == 0 else WHITE)
        fill(M, y - 14, CW, 14, bg)
        cx = M
        for vi, val in enumerate([loc, price, title_c, pot]):
            c.setFont('Helvetica-Bold' if hl else 'Helvetica', 8)
            c.setFillColor(rgb(GREEN if hl else DARK))
            c.drawString(cx + 3, y - 9, val)
            cx += col_ws[vi]
        y -= 14
    y -= 10

    # Gold divider
    c.setFillColor(rgb(GOLD))
    c.rect(M, y - 3, CW, 3, fill=1, stroke=0)
    y -= 10

    # Bungalows
    c.setFont('Helvetica-Bold', 7)
    c.setFillColor(rgb(GOLD))
    c.drawString(M, y - 4, ((full.upper() + ', ') if full != 'You' else '') + 'THERE IS ONE MORE THING')
    y -= 14
    c.setFont('Helvetica-Bold', 12)
    c.setFillColor(rgb(GREEN))
    c.drawString(M, y, 'Modern Bungalows Are Also Coming to Mowe Prime')
    y -= 10

    bung_intro = (
        'We are not just selling land in this estate. We are also building modern 2-bedroom and 3-bedroom bungalows '
        'right here within Mowe Prime, on good roads, with functioning security, an operational school, '
        'over 100 existing homes with residents already in the community, and its own internal transport system. '
        'You are not buying into an open field. You are buying into a place that already works.'
    )
    y = wrap(bung_intro, M, y, CW, size=9, col=DARK, lh=13) - 8

    bung_items = [
        ('2-Bedroom Bungalow', 'Compact, modern, and efficient. Ideal for young families, rental income plays, or a personal property with strong resale upside as the corridor matures.'),
        ('3-Bedroom Bungalow', 'More space, more comfort, more value. Perfect for those wanting a ready-made home without the stress of building, or investors targeting higher rental yields.'),
    ]
    bh = 40
    bw2 = (CW - 8) / 2
    for i, (bt, bb) in enumerate(bung_items):
        bx = M + i * (bw2 + 8)
        by = y - bh
        fill(bx, by, bw2, bh, CREAM)
        c.setFillColor(rgb(GOLD))
        c.rect(bx, by + bh - 2.5, bw2, 2.5, fill=1, stroke=0)
        c.setFont('Helvetica-Bold', 9)
        c.setFillColor(rgb(GREEN))
        c.drawString(bx + 5, by + bh - 12, bt)
        c.setFont('Helvetica', 7)
        c.setFillColor(rgb(MUTED))
        for bi2, bl2 in enumerate(simpleSplit(bb, 'Helvetica', 7, bw2 - 12)[:4]):
            c.drawString(bx + 5, by + bh - 22 - bi2 * 8.5, bl2)
    y -= bh + 8

    fill(M, y - 30, CW, 30, GREEN)
    c.setFont('Helvetica-Bold', 8)
    c.setFillColor(rgb(GOLD))
    c.drawString(M + 5, y - 10, 'Why this matters for your land:')
    c.setFont('Helvetica', 7.5)
    c.setFillColor(rgb((0.75, 0.75, 0.75)))
    note_txt = 'Modern finished homes within the estate push up surrounding land values. Your plot benefits whether you build or not. If a bungalow interests you, we can also build one for you. Just mention it and we will walk you through the details.'
    for ni, nl in enumerate(simpleSplit(note_txt, 'Helvetica', 7.5, CW - 14)[:3]):
        c.drawString(M + 5, y - 19 - ni * 9, nl)
    y -= 38

    # CTA
    cta_h = max(y - M, 90)
    fill(0, M, W2, cta_h, GOLD)
    c.setFont('Helvetica-Bold', 16)
    c.setFillColor(rgb(GREEN))
    hl2_lines = simpleSplit(cta_hl, 'Helvetica-Bold', 16, CW)
    cy = M + cta_h - 16
    for hl2 in hl2_lines:
        c.drawString(M, cy, hl2)
        cy -= 20

    c.setFont('Helvetica', 9)
    c.setFillColor(rgb((0.08, 0.22, 0.13)))
    for cl in simpleSplit(cta_txt, 'Helvetica', 9, CW):
        c.drawString(M, cy, cl)
        cy -= 12
    cy -= 6

    contacts = [
        ('CALL / WHATSAPP', d.get('phone', '+234 903 349 9271')),
        ('EMAIL', d.get('email', 'Israel@landrepublic.co')),
        ('VIEW PROPERTY', d.get('url', 'landrepublic.co/mowe-prime')),
    ]
    bw3 = 150
    for ci2, (clbl, cval) in enumerate(contacts):
        bx2 = M + ci2 * (bw3 + 8)
        fill(bx2, cy - 22, bw3, 22, GREEN)
        c.setFont('Helvetica-Bold', 6)
        c.setFillColor(rgb(GOLD))
        c.drawString(bx2 + 5, cy - 9, clbl)
        c.setFont('Helvetica', 8)
        c.setFillColor(rgb(WHITE))
        c.drawString(bx2 + 5, cy - 18, cval)
    cy -= 30

    c.setFont('Helvetica', 7.5)
    c.setFillColor(rgb((0.1, 0.22, 0.13)))
    c.drawString(M, cy, f"Prepared by {d.get('agent', 'Israel Olaleye')}   |   @asset_by_israel   |   Your Favorite Real Estate Consultant")

    c.save()
    buf.seek(0)
    return buf


DEFAULT = dict(
    title='', fname='', job='', goal='build wealth', type='home', tier='both',
    agent='Israel Toluwalope OLALEYE', phone='+2349033499271',
    email='Israel@landrepublic.co', url='landrepublic.co/mowe-prime'
)


@app.route('/', methods=['GET'])
def index():
    return render_template_string(
        HTML, d=DEFAULT, preview=False,
        headline='', hero_sub='', body_hl='', body_text='',
        cta_hl='', cta_txt='', full_name=''
    )


@app.route('/generate', methods=['POST'])
def generate():
    d = {k: request.form.get(k, DEFAULT[k]) for k in DEFAULT}
    action = request.form.get('action', 'preview')

    pt = d['title'].strip()
    fn = d['fname'].strip()
    if pt and fn:
        full = pt + ' ' + fn
    elif pt:
        full = pt
    elif fn:
        full = fn
    else:
        full = 'You'

    headline = (
        full + ', This Land Was Built for Someone with Your Eye for Opportunity'
        if full != 'You'
        else 'A Land Opportunity Built Around Your Goals'
    )
    hero_sub = (
        d['job'] + 's who want to ' + d['goal'] + ' are exactly who Mowe Prime was positioned for.'
        if d['job']
        else 'Mowe Prime: C of O titled land, 29km from Lagos, inside an already-functioning estate in Nigeria\'s fastest-appreciating corridor.'
    )
    body_hl = (
        'Your Naira Is Losing Ground Every Month, but This Land Is Gaining It.'
        if d['type'] == 'diaspora'
        else 'Mowe Has Already Arrived, but Permit Me to Say the Price Has Not Fully Arrived Yet.'
    )
    body_text = get_body(d['goal'], fn or pt or '')
    cta_hl = (full + ', This Is Your Move, Make It') if full != 'You' else 'This Is Your Move, Make It'
    cta_txt = get_cta(full, d['type'])

    if action == 'pdf':
        buf = build_pdf(d)
        fname_clean = (full.replace(' ', '-') + '-') if full != 'You' else ''
        return send_file(
            buf, mimetype='application/pdf',
            as_attachment=True,
            download_name=f'Mowe-Prime-Pitch-{fname_clean}.pdf'
        )

    return render_template_string(
        HTML, d=d, preview=True,
        headline=headline, hero_sub=hero_sub,
        body_hl=body_hl, body_text=body_text,
        cta_hl=cta_hl, cta_txt=cta_txt,
        full_name=full
    )


if __name__ == '__main__':
    import socket
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = '0.0.0.0'
    print('\n' + '=' * 52)
    print('  MOWE PRIME PITCH GENERATOR')
    print('=' * 52)
    print(f'  Open on THIS device:  http://localhost:5000')
    print(f'  Share on same WiFi:   http://{local_ip}:5000')
    print('=' * 52)
    print('  Press Ctrl+C to stop\n')
    app.run(host='0.0.0.0', port=5000, debug=False)
