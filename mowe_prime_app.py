"""
Mowe Prime Pitch Generator - v2 (OMM Architecture)
Run: python3 mowe_prime_v2.py
Then open: http://localhost:5000

Requirements: pip install flask reportlab
"""

from flask import Flask, request, send_file, render_template_string
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import io

app = Flask(__name__)

# Brand Colors - Mowe Prime (Deep Green / Gold)
DKGREEN  = colors.HexColor("#0D2B1E")
MDGREEN  = colors.HexColor("#1A4A32")
LTGREEN  = colors.HexColor("#2A6B48")
GOLD     = colors.HexColor("#C8A84B")
GOLD2    = colors.HexColor("#E8C96B")
CREAM    = colors.HexColor("#F7F3EC")
WHITE    = colors.Color(1, 1, 1)
DARK     = colors.HexColor("#2C2C2C")
MUTED    = colors.HexColor("#6B6B6B")
LTCREAM  = colors.HexColor("#EEE9DF")

W, H = A4


# ---- GOAL PARAGRAPHS ----
GOAL_PARAGRAPHS = {
    "build wealth": (
        "Some years ago, Mowe was largely an agricultural zone, a stretch of farmland that most Lagosians drove past without a second thought. "
        "A few early buyers saw something different and acquired land there quietly, and they were mostly companies, multinationals from India, China, and across West Africa "
        "that were buying in bulk, holding the land, and beginning to develop. Then the Lagos-Ibadan Expressway rehabilitation came in and it changed everything. "
        "The corridor opened up, infrastructure followed commerce, and Mowe transformed from a transit point into a destination in its own right. "
        "The people who bought ten years ago now sit on assets worth multiples of what they paid, and the trajectory has not stalled. "
        "It has accelerated, because Lagos is now saturated and the only affordable, titled land with direct expressway access to Lagos sits on this exact corridor. "
        "That is why I am bringing this to you. "
        "Mowe Prime is a C of O-backed land opportunity positioned 29km from Lagos, inside a functioning estate that already has residents, schools, security, and its own transport system. "
        "It is not speculative. It is the second great window on a corridor that the first wave of buyers already validated."
    ),
    "secure land": (
        "Some years ago, Mowe was largely farmland that most people drove past without a second glance. A few quiet buyers saw what was coming and secured land at prices that feel almost impossible today. "
        "Then the Lagos-Ibadan Expressway came in and opened everything up, multinationals moved in along the corridor, RCCG built an entire city right there, "
        "and the people who bought early now hold assets worth multiples of what they paid. "
        "Another window like that is open right now, and it will not stay open much longer. "
        "Every month, more titled land in this corridor gets absorbed. Mowe Prime still offers C of O-backed plots at a fraction of Lagos prices, "
        "inside a functioning estate with existing residents, schools, and security already in place. "
        "The legal title is clean. The corridor is active. And the price is still at a point where future appreciation will be significant."
    ),
    "invest idle funds": (
        "Idle naira loses real value every single month, and the choice is always the same: park it somewhere it works, or watch inflation quietly erode it. "
        "Mowe Prime sits on a corridor that has appreciated at 12 to 18 percent annually, documented, and it is backed by C of O title, "
        "which means the asset is bankable, transferable, and legally airtight. "
        "Around it, Nestle, AB InBev, CWAY, Rite Foods, and over 60 active multinationals have locked their operations into the same area, "
        "RCCG has built a 2,500-hectare city with 200,000 residents, and two state governments have signed a joint infrastructure MOU to develop roads, rail, and waterways in the corridor. "
        "That is not a promotional narrative. That is money, institutions, and government all pointing in the same direction. "
        "Land here does not crash overnight. It does not disappear. And when you are ready to exit, the demand is already there waiting."
    ),
    "diaspora property": (
        "Owning property in Nigeria from abroad should not feel like a gamble, and with Mowe Prime it does not have to. "
        "The title is C of O, the highest land title possible, and everything, documents, deed, survey, is processed and issued in your name. "
        "Land Republic is registered in both Nigeria and Delaware, so the legal structure holds in both worlds. "
        "The corridor itself is not a bet on something that might happen. It is a functioning economic zone, "
        "with 60+ active multinationals, 200,000 RCCG residents, a signed interstate infrastructure MOU, and consistent 12 to 18 percent annual appreciation on record. "
        "You do not need to be on the ground to own here, and the corridor keeps compounding value whether you are in London, Houston, or Lagos."
    ),
    "diversify": (
        "Every serious portfolio needs at least one asset that is not correlated to stock markets or currency swings, and C of O-backed land 29km from Lagos is exactly that. "
        "Mowe Prime sits in one of Nigeria's most structurally supported real estate corridors: over 60 active multinationals nearby, "
        "RCCG's 2,500-hectare city with 200,000 residents, a signed Lagos-Ogun infrastructure MOU, and documented 12 to 18 percent annual appreciation. "
        "It is a non-correlated, appreciating hard asset that will not move with Dangote shares or drop when crypto corrects. "
        "That is the kind of weight a strong portfolio needs to stay balanced when everything else is volatile."
    ),
    "build a home": (
        "Mowe Prime is designed to let you build at your own pace and on your own terms. No deadline. No pressure to start on day one. "
        "C of O title means bank financing is accessible the moment you are ready to build, and the corridor keeps pushing your land value higher whether you have broken ground or not. "
        "But here is what makes this different from most land opportunities. "
        "You are not buying into an empty field. "
        "You are entering a functioning estate that already has residents, an operational school, its own internal transportation, and 24-hour security. "
        "The community is already alive. You are simply adding your home to a place that is already working."
    ),
}

GOAL_LABELS = {
    "build wealth":    "Build Long-Term Wealth",
    "secure land":     "Secure Land for the Future",
    "invest idle funds": "Invest Idle Funds",
    "diaspora property": "Own Property from Abroad",
    "diversify":       "Diversify Their Portfolio",
    "build a home":    "Build a Home",
}

TIER_DATA = {
    "standard": {
        "name": "Standard", "price": "N8,000,000", "deposit": "N2,000,000",
        "size": "300 SQM (50ft x 60ft)", "lease": "C of O Backed",
    },
    "premium": {
        "name": "Premium", "price": "N15,000,000", "deposit": "N2,000,000",
        "size": "500 SQM (60ft x 100ft)", "lease": "C of O Backed",
    },
}

DOCS_LIST = [
    "C of O Backed Title",
    "Deed of Assignment",
    "Registered Survey Plan",
    "Contract of Sale",
    "Allocation Letter + Receipt",
]


# ---- HTML ----
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mowe Prime Pitch Generator</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', Arial, sans-serif; background: #0D2B1E; color: #F7F3EC; min-height: 100vh; }

  /* HERO */
  .hero { background: linear-gradient(135deg, #0D2B1E 0%, #1A4A32 60%, #0D2B1E 100%); padding: 48px 32px 36px; text-align: center; border-bottom: 3px solid #C8A84B; }
  .hero-badge { display: inline-block; background: #C8A84B; color: #0D2B1E; font-size: 11px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; padding: 6px 18px; border-radius: 2px; margin-bottom: 18px; }
  .hero h1 { font-family: Georgia, serif; font-size: 2.6rem; font-weight: 700; color: #F7F3EC; line-height: 1.15; margin-bottom: 10px; }
  .hero h1 span { color: #C8A84B; }
  .hero p { font-size: 1rem; color: #A8C8A8; max-width: 560px; margin: 0 auto; line-height: 1.6; }

  /* STATS */
  .stats-bar { display: flex; justify-content: center; background: #C8A84B; }
  .stat { flex: 1; text-align: center; padding: 14px 10px; border-right: 1px solid rgba(13,43,30,0.25); color: #0D2B1E; }
  .stat:last-child { border-right: none; }
  .stat-num { font-size: 1.4rem; font-weight: 800; display: block; }
  .stat-label { font-size: 0.7rem; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; opacity: 0.75; }

  /* FORM */
  .form-wrap { max-width: 720px; margin: 40px auto; background: #112B1E; border-radius: 8px; padding: 40px 44px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); border: 1px solid rgba(200,168,75,0.2); }
  .form-wrap h2 { font-family: Georgia, serif; font-size: 1.5rem; color: #C8A84B; margin-bottom: 8px; }
  .form-wrap > p { color: #7AAA8A; font-size: 0.9rem; margin-bottom: 28px; line-height: 1.5; }
  .field-group { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .field-group.single { grid-template-columns: 1fr; }
  .field { display: flex; flex-direction: column; margin-bottom: 18px; }
  .field label { font-size: 0.78rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #7AAA8A; margin-bottom: 7px; }
  .field input, .field select { background: #0D2B1E; border: 1px solid rgba(200,168,75,0.3); border-radius: 4px; color: #F7F3EC; font-size: 0.95rem; padding: 11px 14px; outline: none; transition: border 0.2s; }
  .field input:focus, .field select:focus { border-color: #C8A84B; }
  .field select option { background: #0D2B1E; }
  .divider { border: none; border-top: 1px solid rgba(200,168,75,0.15); margin: 28px 0 20px; }
  .section-label { font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase; color: #C8A84B; font-weight: 700; margin-bottom: 16px; }

  /* BUTTONS */
  .btn-row { display: flex; gap: 14px; flex-wrap: wrap; margin-top: 28px; }
  .submit-btn { flex: 1; background: #C8A84B; color: #0D2B1E; font-size: 0.95rem; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; padding: 16px; border: none; border-radius: 4px; cursor: pointer; transition: background 0.2s; }
  .submit-btn:hover { background: #b8962e; }
  .submit-btn.secondary { background: #1A4A32; color: #C8A84B; border: 1px solid #C8A84B; }
  .submit-btn.secondary:hover { background: #0D2B1E; }

  /* PREVIEW CARD */
  .preview-wrap { max-width: 820px; margin: 0 auto 60px; padding: 0 16px; }
  .pv-card { background: #fff; border-radius: 8px; overflow: hidden; border: 1px solid #ddd; }
  .pv-hero { background: #0D2B1E; padding: 44px 40px 36px; border-bottom: 3px solid #C8A84B; }
  .pv-badge { display: inline-block; background: #C8A84B; color: #0D2B1E; font-size: 9px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; padding: 5px 14px; border-radius: 2px; margin-bottom: 16px; }
  .pv-hero h2 { font-family: Georgia, serif; font-size: clamp(20px, 3vw, 28px); color: #fff; line-height: 1.25; margin-bottom: 10px; }
  .pv-hero p { font-size: 12px; color: #A8C8A8; line-height: 1.7; max-width: 480px; }
  .pv-stats { display: flex; background: #C8A84B; }
  .pv-stat { flex: 1; text-align: center; padding: 12px 8px; border-right: 1px solid rgba(13,43,30,0.2); }
  .pv-stat:last-child { border-right: none; }
  .pv-stat-n { display: block; font-size: 16px; font-weight: 800; color: #0D2B1E; }
  .pv-stat-l { display: block; font-size: 7px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: rgba(13,43,30,0.65); margin-top: 2px; }
  .pv-sec { padding: 28px 40px; border-bottom: 1px solid #e8e8e8; background: #fff; }
  .pv-sec.cream { background: #F7F3EC; }
  .pv-sec.dark { background: #0D2B1E; }
  .pv-sec.gold-bg { background: #C8A84B; }
  .pv-slbl { font-size: 8px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase; color: #C8A84B; display: block; margin-bottom: 10px; }
  .pv-sec.dark .pv-slbl { color: #E8C96B; }
  .pv-sec.gold-bg .pv-slbl { color: rgba(13,43,30,0.6); }
  .pv-sec h3 { font-family: Georgia, serif; font-size: 18px; color: #0D2B1E; margin-bottom: 12px; line-height: 1.3; }
  .pv-sec.dark h3 { color: #fff; }
  .pv-sec.gold-bg h3 { color: #0D2B1E; font-size: 22px; }
  .pv-sec p { font-size: 13px; color: #333; line-height: 1.8; }
  .pv-sec.dark p { color: rgba(255,255,255,0.75); }
  .pv-sec.gold-bg p { color: rgba(13,43,30,0.72); }

  /* CORRIDOR TABLE */
  .loc-tbl { width: 100%; border-collapse: collapse; margin-top: 14px; }
  .loc-tbl td { padding: 9px 12px; font-size: 12px; border-bottom: 1px solid #d8e8d8; vertical-align: middle; }
  .loc-tbl td:first-child { font-weight: 700; color: #1A4A32; background: #E4F0E8; width: 38%; }
  .loc-tbl td:last-child { color: #222; }
  .loc-tbl tr:nth-child(even) td:last-child { background: #F7F3EC; }

  /* TIER TABLE */
  .tier-tbl { width: 100%; border-collapse: collapse; margin-top: 14px; }
  .tier-tbl th { background: #0D2B1E; color: #C8A84B; font-size: 8.5px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; padding: 10px 8px; text-align: center; }
  .tier-tbl td { padding: 10px 8px; text-align: center; font-size: 12px; border-bottom: 1px solid rgba(13,43,30,0.2); }
  .tier-tbl tr:nth-child(odd) td { background: #1A4A32; color: #F7F3EC; }
  .tier-tbl tr:nth-child(even) td { background: #2A6B48; color: #F7F3EC; }
  .tier-tbl td.cat { font-weight: 700; color: #fff; }
  .tier-tbl td.amt { font-weight: 700; color: #C8A84B; font-size: 16px; }

  /* PAYMENT NOTE */
  .pay-note { margin-top: 12px; background: #0A2018; border: 1px solid #1A4A32; border-radius: 4px; }
  .pay-note-row { display: flex; border-bottom: 1px solid rgba(200,168,75,0.2); }
  .pay-note-row:last-child { border-bottom: none; }
  .pay-cell { flex: 1; padding: 10px 14px; border-right: 1px solid rgba(26,74,50,0.5); }
  .pay-cell:last-child { border-right: none; }
  .pay-lbl { font-size: 8px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #C8A84B; display: block; margin-bottom: 4px; }
  .pay-val { font-size: 12px; color: #F7F3EC; line-height: 1.5; }

  /* WHY ITEMS */
  .why-items { margin-top: 14px; }
  .why-item { display: flex; gap: 14px; margin-bottom: 10px; background: #F7F3EC; border-bottom: 1px solid #dde8d8; padding: 14px; }
  .why-num { font-family: Georgia, serif; font-size: 28px; font-weight: 700; color: #C8A84B; min-width: 40px; line-height: 1; }
  .why-content h4 { font-size: 13px; font-weight: 700; color: #0D2B1E; margin-bottom: 6px; }
  .why-content p { font-size: 12px; color: #444; line-height: 1.6; }

  /* BUNGALOWS */
  .bung-grid { display: flex; gap: 14px; margin-top: 16px; flex-wrap: wrap; }
  .bung-card { flex: 1; min-width: 200px; background: #fff; border: 1px solid #d8e8d8; border-top: 3px solid #C8A84B; border-radius: 0 0 5px 5px; padding: 18px 16px; }
  .bung-card h4 { font-size: 14px; font-weight: 700; color: #0D2B1E; margin-bottom: 8px; }
  .bung-card p { font-size: 12px; color: #555; line-height: 1.7; }
  .bung-note { margin-top: 14px; background: #0D2B1E; border-radius: 4px; padding: 14px 16px; font-size: 12px; color: rgba(255,255,255,0.75); line-height: 1.75; }
  .bung-note strong { color: #C8A84B; }

  /* COMPARISON */
  .comp-tbl { width: 100%; border-collapse: collapse; margin-top: 14px; }
  .comp-tbl th { background: #0D2B1E; color: #C8A84B; font-size: 8.5px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; padding: 9px 10px; text-align: left; }
  .comp-tbl td { padding: 9px 10px; font-size: 12px; border-bottom: 1px solid #d8e8d8; color: #333; }
  .comp-tbl td:first-child { font-weight: 700; color: #0D2B1E; }
  .comp-tbl td.mp { color: #1A4A32; font-weight: 600; background: #EBF4EE; }
  .comp-tbl tr:nth-child(even) td { background: #F7F3EC; }
  .comp-tbl tr:nth-child(even) td.mp { background: #EBF4EE; }

  /* CTA */
  .cta-block { background: #1A4A32; border-top: 3px solid #C8A84B; padding: 32px 40px; }
  .cta-block .pv-slbl { color: #E8C96B; }
  .cta-block h3 { font-family: Georgia, serif; font-size: 22px; color: #C8A84B; margin-bottom: 10px; line-height: 1.3; }
  .cta-block p { font-size: 13px; color: rgba(255,255,255,0.78); line-height: 1.8; margin-bottom: 18px; }
  .cta-contacts { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 16px; }
  .cta-ci { background: #0D2B1E; border-radius: 3px; padding: 10px 16px; }
  .cta-ci-l { font-size: 8px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #C8A84B; display: block; margin-bottom: 3px; }
  .cta-ci-v { font-size: 12px; color: #fff; font-weight: 500; }
  .cta-sig { font-size: 11px; color: rgba(255,255,255,0.45); margin-top: 10px; }

  .footer { text-align: center; padding: 28px; color: #2A5A3A; font-size: 0.8rem; }

  @media (max-width: 580px) {
    .field-group { grid-template-columns: 1fr; }
    .form-wrap { padding: 28px 18px; }
    .hero h1 { font-size: 1.8rem; }
    .stats-bar, .pv-stats { flex-wrap: wrap; }
    .stat, .pv-stat { min-width: 50%; }
    .pv-sec, .pv-hero, .cta-block { padding: 22px 18px; }
    .btn-row { flex-direction: column; }
  }
</style>
</head>
<body>

<div class="hero">
  <span class="hero-badge">Asset by Israel x Land Republic</span>
  <h1>Mowe Prime Estate<br><span>Pitch Generator</span></h1>
  <p>Generate a fully personalised, print-ready investment pitch PDF for any prospect, tailored to their profile, goals, and recommended land tier.</p>
</div>
<div class="stats-bar">
  <div class="stat"><span class="stat-num">29km</span><span class="stat-label">From Lagos</span></div>
  <div class="stat"><span class="stat-num">12-18%</span><span class="stat-label">Ann. Appreciation</span></div>
  <div class="stat"><span class="stat-num">200K</span><span class="stat-label">RCCG Residents</span></div>
  <div class="stat"><span class="stat-num">60+</span><span class="stat-label">Multinationals</span></div>
  <div class="stat"><span class="stat-num">C of O</span><span class="stat-label">Bankable Title</span></div>
</div>

<form class="form-wrap" method="POST" action="/generate">
  <h2>Prospect Information</h2>
  <p>Fill in the prospect's details and goals. The generator builds a personalised pitch document around them.</p>

  <p class="section-label">Prospect Details</p>
  <div class="field-group">
    <div class="field">
      <label>Title</label>
      <select name="title">
        <option>Mr.</option><option>Mrs.</option><option>Miss</option>
        <option>Dr.</option><option>Prof.</option><option>Engr.</option>
        <option>Chief</option><option>Alhaji</option><option>Alhaja</option>
        <option>Barrister</option>
      </select>
    </div>
    <div class="field">
      <label>First Name</label>
      <input type="text" name="first_name" placeholder="e.g. Tunde" required>
    </div>
  </div>
  <div class="field-group">
    <div class="field">
      <label>What They Do</label>
      <input type="text" name="occupation" placeholder="e.g. Engineer, Business Owner" required>
    </div>
    <div class="field">
      <label>Profile Type</label>
      <select name="profile">
        <option value="home">Nigeria-Based</option>
        <option value="diaspora">Diaspora (Abroad)</option>
      </select>
    </div>
  </div>
  <div class="field-group single">
    <div class="field">
      <label>Their Primary Goal</label>
      <select name="goal">
        <option value="build wealth">Build Long-Term Wealth</option>
        <option value="secure land">Secure Land for the Future</option>
        <option value="invest idle funds">Invest Idle Funds</option>
        <option value="diaspora property">Own Property from Abroad</option>
        <option value="diversify">Diversify Their Portfolio</option>
        <option value="build a home">Build a Home</option>
      </select>
    </div>
  </div>
  <div class="field-group single">
    <div class="field">
      <label>Tier to Recommend</label>
      <select name="tier">
        <option value="both">Both Options (Standard + Premium)</option>
        <option value="standard">Standard Only (N8M / 300 sqm)</option>
        <option value="premium">Premium Only (N15M / 500 sqm)</option>
      </select>
    </div>
  </div>

  <hr class="divider">
  <p class="section-label">Consultant Information</p>
  <div class="field-group">
    <div class="field">
      <label>Consultant Name</label>
      <input type="text" name="agent_name" placeholder="Your full name" required>
    </div>
    <div class="field">
      <label>Phone Number</label>
      <input type="text" name="agent_phone" placeholder="+234 xxx xxx xxxx" required>
    </div>
  </div>
  <div class="field-group">
    <div class="field">
      <label>Email Address</label>
      <input type="email" name="agent_email" placeholder="you@example.com">
    </div>
    <div class="field">
      <label>Property URL (optional)</label>
      <input type="text" name="property_url" placeholder="landrepublic.co/mowe-prime">
    </div>
  </div>
  <div class="field-group">
    <div class="field">
      <label>Social Media Handle (optional)</label>
      <input type="text" name="agent_social" placeholder="e.g. @asset_by_israel">
    </div>
    <div class="field">
      <label>Tagline (optional)</label>
      <input type="text" name="agent_tagline" placeholder="e.g. Your Favorite Real Estate Consultant">
    </div>
  </div>

  <div class="btn-row">
    <button type="submit" name="action" value="preview" class="submit-btn secondary">Preview Pitch</button>
    <button type="submit" name="action" value="pdf" class="submit-btn">Download PDF</button>
  </div>
</form>

{% if preview %}
<div class="preview-wrap">
<div class="pv-card">

  <!-- HERO -->
  <div class="pv-hero">
    <span class="pv-badge">Private Investment Brief &middot; Asset by Israel</span>
    <h2>Prepared Exclusively for You, {{ full_title }}</h2>
    <p>{{ hero_sub }}</p>
  </div>

  <!-- STATS -->
  <div class="pv-stats">
    <div class="pv-stat"><span class="pv-stat-n">29km</span><span class="pv-stat-l">From Lagos</span></div>
    <div class="pv-stat"><span class="pv-stat-n">12-18%</span><span class="pv-stat-l">Ann. Appreciation</span></div>
    <div class="pv-stat"><span class="pv-stat-n">200K</span><span class="pv-stat-l">RCCG Residents</span></div>
    <div class="pv-stat"><span class="pv-stat-n">60+</span><span class="pv-stat-l">Multinationals</span></div>
    <div class="pv-stat"><span class="pv-stat-n">C of O</span><span class="pv-stat-l">Bankable Title</span></div>
  </div>

  <!-- INVESTMENT BRIEF -->
  <div class="pv-sec">
    <span class="pv-slbl">{{ full_title }}, This Is the Investment Brief</span>
    <h3>Mowe Prime Is for Someone Like You</h3>
    <p>{{ goal_para }}</p>
  </div>

  <!-- CORRIDOR STORY -->
  <div class="pv-sec cream">
    <span class="pv-slbl">{{ full_title }}, Let Us Talk About the Corridor</span>
    <h3>Mowe Has Already Arrived, but Permit Me to Say the Price Has Not Fully Arrived Yet</h3>
    <p>Mowe is not a new name in the real estate conversation. It is the corridor that Lagos outgrew into, the expressway junction that multinationals have been quietly building around for years, and the closest affordable titled land to a city that has already run out of it. What is new is that most retail buyers are still catching up to what institutional money already understood a decade ago. Nestle, AB InBev, CWAY, and Rite Foods did not build there by accident. RCCG did not build a 2,500-hectare city with 200,000 residents there by accident. And two state governments did not sign a joint infrastructure MOU for roads, rail, and waterways there by accident. The price of land in Mowe will eventually catch up to the fundamentals around it. That gap between the current price and the underlying value is exactly where the opportunity sits right now.</p>
    <table class="loc-tbl">
      <tr><td>Distance from Lagos</td><td>29km via Lagos-Ibadan Expressway</td></tr>
      <tr><td>Minutes from Berger</td><td>Approximately 20 to 30 minutes by road</td></tr>
      <tr><td>Multinationals Nearby</td><td>60+ including Nestle, AB InBev, CWAY, Rite Foods</td></tr>
      <tr><td>RCCG City</td><td>2,500 hectares, 200,000 residents, 197 countries of membership</td></tr>
      <tr><td>Infrastructure MOU</td><td>Lagos-Ogun joint roads, rail, waterways (signed)</td></tr>
      <tr><td>Annual Appreciation</td><td>12 to 18 percent documented over the past 5 years</td></tr>
    </table>
  </div>

  <!-- LAND CASE -->
  <div class="pv-sec">
    <span class="pv-slbl">{{ full_title }}, Here Is the Land Investment Case</span>
    <h3>A Functioning Estate, Not an Open Field</h3>
    <p>Mowe Prime is not a raw land deal in an empty expanse. The estate already has over 100 homes with residents living in them, an operational school, its own internal transportation system, and functioning 24-hour security. When you buy here, you are buying into a community that already works, and that changes the investment risk profile entirely. The infrastructure is not a promise. It is already there. What is still growing is the price, and that window does not stay open forever.</p>
    <p style="margin-top:12px;">Between Lagos getting saturated on one side and Ibadan growing on the other, Mowe sits at the exact midpoint of two of Nigeria's largest and fastest-growing cities. Access to both, priced like neither. That is the structural argument for this corridor in a single sentence.</p>
  </div>

  <!-- TIERS -->
  <div class="pv-sec dark">
    <span class="pv-slbl">{{ full_title }}, We Have {{ tier_label }}</span>
    <h3>Pick the One That Works Best for You</h3>
    <table class="tier-tbl">
      <thead>
        <tr><th>Tier</th><th>Price</th><th>Size</th><th>Deposit</th><th>Title</th></tr>
      </thead>
      <tbody>
        {% if show_standard %}
        <tr><td class="cat">Standard</td><td class="amt">N8,000,000</td><td>300 SQM (50ft x 60ft)</td><td>N2,000,000</td><td>C of O</td></tr>
        {% endif %}
        {% if show_premium %}
        <tr><td class="cat">Premium</td><td class="amt">N15,000,000</td><td>500 SQM (60ft x 100ft)</td><td>N2,000,000</td><td>C of O</td></tr>
        {% endif %}
      </tbody>
    </table>
    <p style="margin-top:14px;font-size:12px;color:rgba(255,255,255,0.6);">Each plot comes with: C of O Backed Title &middot; Deed of Assignment &middot; Registered Survey Plan &middot; Contract of Sale &middot; Allocation Letter + Receipt</p>
    <div class="pay-note">
      <div class="pay-note-row">
        <div class="pay-cell"><span class="pay-lbl">Pay Outright</span><span class="pay-val">Instant allocation on payment</span></div>
        <div class="pay-cell"><span class="pay-lbl">6 Months Interest-Free</span><span class="pay-val">Deposit from N2M, balance monthly</span></div>
      </div>
      <div class="pay-note-row">
        <div class="pay-cell" style="flex:3;"><span class="pay-lbl">Bank Account</span><span class="pay-val">LAND REPUBLIC LIMITED &nbsp;&middot;&nbsp; 78 Finance Company or 78 MFB &nbsp;&middot;&nbsp; 0001549819</span></div>
      </div>
    </div>
  </div>

  <!-- WHY IT WORKS -->
  <div class="pv-sec cream">
    <span class="pv-slbl">{{ full_title }}, at a Quick Glance, Here Is Why This Generally Works</span>
    <h3>Four Reasons This Investment Makes Sense</h3>
    <div class="why-items">
      <div class="why-item"><div class="why-num">01</div><div class="why-content"><h4>Lagos Overflow Is Structural, Not a Trend</h4><p>Lagos is running out of affordable, titled land and what it cannot contain flows into Mowe via the expressway. That is not marketing. That is the documented consequence of two cities growing toward each other, and it does not stop.</p></div></div>
      <div class="why-item"><div class="why-num">02</div><div class="why-content"><h4>60+ Multinationals Drive Constant Housing Demand</h4><p>Nestle, AB InBev, CWAY, Rite Foods, and dozens more employ tens of thousands of workers in this corridor. Those workers need housing nearby. Supply of titled, well-located land is already short and your plot sits in the middle of that demand gap.</p></div></div>
      <div class="why-item"><div class="why-num">03</div><div class="why-content"><h4>RCCG City Is an Anchor Nothing Can Replicate</h4><p>2,500 hectares. 200,000 residents. 197 countries of RCCG membership. Millions of annual visitors. This demand does not fluctuate with the economy. It only compounds over time.</p></div></div>
      <div class="why-item"><div class="why-num">04</div><div class="why-content"><h4>Lagos-Ogun Infrastructure MOU Has Been Signed</h4><p>Two state governments committed to joint road development, waterworks, rail, and waterways in this corridor. Government money follows where government signs, and property values follow government money. These are not future promises. The agreement is already done.</p></div></div>
    </div>
  </div>

  <!-- BUNGALOWS -->
  <div class="pv-sec">
    <span class="pv-slbl">{{ full_title }}, There Is One More Thing</span>
    <h3>Modern Bungalows Are Also Coming to Mowe Prime</h3>
    <p>We are not just selling land in this estate. We are also building modern 2-bedroom and 3-bedroom bungalows right here within Mowe Prime, on good roads, within a well laid-out estate with existing residents and functioning infrastructure already in place. Construction is starting soon and if a bungalow interests you alongside or instead of a land plot, we can also build for you as a company. Just mention it and we will walk you through what that looks like.</p>
    <div class="bung-grid">
      <div class="bung-card"><h4>2-Bedroom Bungalow</h4><p>Compact, modern, and efficient. Ideal for young families, rental income plays, or a personal property with strong resale upside as the corridor matures.</p></div>
      <div class="bung-card"><h4>3-Bedroom Bungalow</h4><p>More space, more comfort, more value. Perfect for those who want a ready-made home without the stress of building, or investors targeting higher rental yields in a growing corridor.</p></div>
    </div>
    <div class="bung-note"><strong>Why this matters for your land:</strong> Modern finished homes within the same estate directly push up the value of surrounding plots. Your land benefits whether you build on it or not.</div>
  </div>

  <!-- COMPARISON -->
  <div class="pv-sec cream">
    <span class="pv-slbl">{{ full_title }}, Let Us Also Do a Quick Market Comparison</span>
    <h3>How Mowe Prime Compares to the Market</h3>
    <table class="comp-tbl">
      <thead><tr><th>Location</th><th>Mowe Prime</th><th>Magboro</th><th>Ibadan Bodija</th><th>Lagos VI</th></tr></thead>
      <tbody>
        <tr><td>Price Range</td><td class="mp">N8M to N15M</td><td>N18M+</td><td>N40M+</td><td>N180M+</td></tr>
        <tr><td>Title</td><td class="mp">C of O</td><td>Varies</td><td>Varies</td><td>C of O</td></tr>
        <tr><td>5-Yr Potential</td><td class="mp">300 to 450%</td><td>N/A</td><td>N/A</td><td>Saturated</td></tr>
        <tr><td>Lagos Access</td><td class="mp">29km / Expressway</td><td>Closer but pricier</td><td>Ibadan-based</td><td>Already inside</td></tr>
        <tr><td>Market Status</td><td class="mp">Growing corridor</td><td>Expensive entry</td><td>Different market</td><td>No room to grow</td></tr>
      </tbody>
    </table>
  </div>

  <!-- CTA -->
  <div class="cta-block">
    <span class="pv-slbl">Next Step</span>
    <h3>{{ full_title }}, Your Plot at Mowe Prime Is Waiting</h3>
    <p>The land is real, the title is clean, the corridor is active, and the environment around it is growing. It only takes one conversation to get your allocation started and secure your own plot. Let us have a consultation call so we can talk about your preferred tier, payment structure, and any questions you might have. We can also arrange a site inspection so you see the estate for yourself.</p>
    <div class="cta-contacts">
      <div class="cta-ci"><span class="cta-ci-l">Call / WhatsApp</span><span class="cta-ci-v">{{ agent_phone }}</span></div>
      <div class="cta-ci"><span class="cta-ci-l">Email</span><span class="cta-ci-v">{{ agent_email }}</span></div>
      {% if property_url %}
      <div class="cta-ci"><span class="cta-ci-l">View Property</span><span class="cta-ci-v">{{ property_url }}</span></div>
      {% endif %}
    </div>
    <div class="cta-ci" style="display:inline-block;margin-bottom:14px;"><span class="cta-ci-l">Bank Account</span><span class="cta-ci-v">LAND REPUBLIC LIMITED &nbsp;&middot;&nbsp; 78 Finance Company or 78 MFB &nbsp;&middot;&nbsp; 0001549819</span></div>
    <p class="cta-sig">Prepared by <strong>{{ agent_name }}</strong>{% if agent_social %} &nbsp;&middot;&nbsp; {{ agent_social }}{% endif %}{% if agent_tagline %} &nbsp;&middot;&nbsp; {{ agent_tagline }}{% endif %}</p>
  </div>

</div>
</div>
{% endif %}

<div class="footer">Mowe Prime Estate &mdash; C of O Titled Land, 29km from Lagos, Ogun State &mdash; Presented by Land Republic</div>
</body>
</html>
"""


# ---- PDF STYLES ----
def build_styles():
    return {
        "hero_badge": ParagraphStyle("hero_badge", fontName="Helvetica-Bold",
            fontSize=8, textColor=DKGREEN, leading=12, alignment=TA_CENTER, spaceAfter=10),
        "hero_title": ParagraphStyle("hero_title", fontName="Times-Bold",
            fontSize=24, textColor=WHITE, leading=30, alignment=TA_CENTER, spaceAfter=6),
        "hero_sub": ParagraphStyle("hero_sub", fontName="Times-Italic",
            fontSize=11, textColor=colors.HexColor("#A8C8A8"), leading=16,
            alignment=TA_CENTER, spaceAfter=4),
        "section_label": ParagraphStyle("section_label", fontName="Helvetica-Bold",
            fontSize=8, textColor=GOLD, leading=12, alignment=TA_LEFT,
            spaceBefore=14, spaceAfter=6),
        "section_title": ParagraphStyle("section_title", fontName="Times-Bold",
            fontSize=15, textColor=DKGREEN, leading=20, alignment=TA_LEFT,
            spaceBefore=4, spaceAfter=8),
        "body": ParagraphStyle("body", fontName="Helvetica",
            fontSize=9.5, textColor=DARK, leading=15,
            alignment=TA_JUSTIFY, spaceAfter=8),
        "body_white": ParagraphStyle("body_white", fontName="Helvetica",
            fontSize=9.5, textColor=WHITE, leading=15, alignment=TA_JUSTIFY, spaceAfter=6),
        "cta_main": ParagraphStyle("cta_main", fontName="Times-Bold",
            fontSize=17, textColor=GOLD, leading=22, alignment=TA_CENTER, spaceAfter=6),
        "small_label": ParagraphStyle("small_label", fontName="Helvetica-Bold",
            fontSize=7.5, textColor=GOLD, leading=11, alignment=TA_CENTER),
        "table_head": ParagraphStyle("table_head", fontName="Helvetica-Bold",
            fontSize=8, textColor=WHITE, leading=11, alignment=TA_CENTER),
        "footnote": ParagraphStyle("footnote", fontName="Helvetica-Oblique",
            fontSize=7.5, textColor=colors.HexColor("#888888"), leading=11,
            alignment=TA_CENTER),
    }


def make_hero_pdf(styles, title, first_name, occupation, goal_label):
    full_title = f"{title} {first_name}"
    inner = [
        Paragraph("PRIVATE INVESTMENT BRIEF  |  ASSET BY ISRAEL  |  LAND REPUBLIC", styles["hero_badge"]),
        Spacer(1, 6),
        Paragraph(f"Prepared Exclusively for You, {full_title}", styles["hero_title"]),
        Spacer(1, 6),
        Paragraph(
            f"Mowe Prime Estate is for someone like you, a {occupation} whose primary focus is to {goal_label.lower()}",
            styles["hero_sub"]
        ),
        Spacer(1, 10),
        Paragraph("Mowe, Ogun State  |  29km from Lagos via the Lagos-Ibadan Expressway",
            ParagraphStyle("loc", fontName="Helvetica-Bold", fontSize=9,
                textColor=GOLD, alignment=TA_CENTER)),
    ]
    tbl = Table([[inner]], colWidths=[W - 2 * 25 * mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DKGREEN),
        ("TOPPADDING", (0, 0), (-1, -1), 28),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 24),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("LINEBELOW", (0, 0), (-1, -1), 3, GOLD),
    ]))
    return [tbl]


def make_stats_bar_pdf(styles):
    stats = [
        ("29km", "From Lagos"),
        ("12-18%", "Ann. Appreciation"),
        ("200K", "RCCG Residents"),
        ("60+", "Multinationals"),
        ("C of O", "Bankable Title"),
    ]
    row = []
    for num, label in stats:
        row.append([
            Paragraph(num, ParagraphStyle("sn", fontName="Helvetica-Bold",
                fontSize=12, textColor=DKGREEN, alignment=TA_CENTER, leading=15)),
            Paragraph(label, ParagraphStyle("sl", fontName="Helvetica",
                fontSize=6.5, textColor=DKGREEN, alignment=TA_CENTER, leading=9)),
        ])
    col_w = (W - 50 * mm) / len(stats)
    tbl = Table([row], colWidths=[col_w] * len(stats))
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LINEAFTER", (0, 0), (-2, -1), 0.5, colors.HexColor("#A08030")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return [tbl]


def make_investment_brief_pdf(styles, title, first_name, goal, goal_label):
    full_title = f"{title} {first_name}"
    elems = [Spacer(1, 14)]
    elems.append(Paragraph(
        f"{full_title.upper()}, THIS IS THE INVESTMENT BRIEF", styles["section_label"]
    ))
    elems.append(Paragraph("Mowe Prime Is for Someone Like You", styles["section_title"]))
    elems.append(Paragraph(GOAL_PARAGRAPHS.get(goal, GOAL_PARAGRAPHS["build wealth"]), styles["body"]))
    return elems


def make_corridor_section_pdf(styles, title, first_name):
    full_title = f"{title} {first_name}"
    elems = [Spacer(1, 14)]
    elems.append(Paragraph(
        f"{full_title.upper()}, LET US TALK ABOUT THE CORRIDOR", styles["section_label"]
    ))
    elems.append(Paragraph(
        "Mowe Has Already Arrived, but Permit Me to Say the Price Has Not Fully Arrived Yet",
        styles["section_title"]
    ))
    body = (
        "Mowe is not a new name in the real estate conversation. It is the corridor that Lagos outgrew into, "
        "the expressway junction that multinationals have been quietly building around for years, and the closest "
        "affordable titled land to a city that has already run out of it. What is new is that most retail buyers "
        "are still catching up to what institutional money already understood a decade ago. Nestle, AB InBev, CWAY, "
        "and Rite Foods did not build there by accident. RCCG did not build a 2,500-hectare city with 200,000 residents "
        "there by accident. And two state governments did not sign a joint infrastructure MOU for roads, rail, and waterways "
        "there by accident. The price of land in Mowe will eventually catch up to the fundamentals around it, "
        "and that gap between the current price and the underlying value is exactly where the opportunity sits right now."
    )
    elems.append(Paragraph(body, styles["body"]))

    loc_data = [
        ["Distance from Lagos", "29km via Lagos-Ibadan Expressway"],
        ["Minutes from Berger", "Approximately 20 to 30 minutes by road"],
        ["Multinationals Nearby", "60+ including Nestle, AB InBev, CWAY, Rite Foods"],
        ["RCCG City", "2,500 hectares, 200,000 residents, 197 countries of membership"],
        ["Infrastructure MOU", "Lagos-Ogun joint roads, rail, waterways (signed)"],
        ["Annual Appreciation", "12 to 18 percent documented over the past 5 years"],
    ]
    tbl = Table(loc_data, colWidths=[55 * mm, W - 50 * mm - 55 * mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E4F0E8")),
        ("ROWBACKGROUNDS", (1, 0), (1, -1), [CREAM, WHITE]),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("TEXTCOLOR", (0, 0), (0, -1), MDGREEN),
        ("TEXTCOLOR", (1, 0), (1, -1), DKGREEN),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#C0D8C0")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#A0C0A0")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elems.append(tbl)
    return elems


def make_land_case_pdf(styles, title, first_name):
    full_title = f"{title} {first_name}"
    elems = [Spacer(1, 14)]
    elems.append(Paragraph(
        f"{full_title.upper()}, HERE IS THE LAND INVESTMENT CASE", styles["section_label"]
    ))
    elems.append(Paragraph("A Functioning Estate, Not an Open Field", styles["section_title"]))

    body = (
        "Mowe Prime is not a raw land deal in an empty expanse. The estate already has over 100 homes with residents "
        "living in them, an operational school, its own internal transportation system, and functioning 24-hour security. "
        "When you buy here, you are buying into a community that already works, and that changes the investment risk profile entirely. "
        "The infrastructure is not a promise. It is already there. What is still growing is the price, and that window does not stay open forever."
    )
    elems.append(Paragraph(body, styles["body"]))

    body2 = (
        "Between Lagos getting saturated on one side and Ibadan growing on the other, Mowe sits at the exact midpoint "
        "of two of Nigeria's largest and fastest-growing cities. Access to both, priced like neither. "
        "That is the structural argument for this corridor in a single sentence."
    )
    elems.append(Paragraph(body2, styles["body"]))
    return elems


def make_tiers_pdf(styles, tier, title, first_name):
    full_title = f"{title} {first_name}"
    if tier == "standard":
        tier_label = "One Entry Point"
    elif tier == "premium":
        tier_label = "One Entry Point"
    else:
        tier_label = "Two Entry Points"

    elems = [Spacer(1, 14)]
    elems.append(Paragraph(
        f"{full_title.upper()}, WE HAVE {tier_label.upper()}", styles["section_label"]
    ))
    elems.append(Paragraph("Pick the One That Works Best for You", styles["section_title"]))

    all_tiers = {
        "standard": ("Standard", "N8,000,000", "300 SQM (50ft x 60ft)", "N2,000,000"),
        "premium":  ("Premium",  "N15,000,000", "500 SQM (60ft x 100ft)", "N2,000,000"),
    }
    show = ["standard", "premium"] if tier == "both" else [tier]

    headers = ["Tier", "Price", "Size", "Deposit", "Title"]
    header_row = [Paragraph(h, styles["table_head"]) for h in headers]
    rows = [header_row]
    for t in show:
        name, price, size, deposit = all_tiers[t]
        rows.append([
            Paragraph(name, ParagraphStyle("cn", fontName="Helvetica-Bold",
                fontSize=9, textColor=WHITE, alignment=TA_CENTER)),
            Paragraph(price, ParagraphStyle("cv", fontName="Helvetica-Bold",
                fontSize=12, textColor=GOLD, alignment=TA_CENTER)),
            Paragraph(size, ParagraphStyle("cv", fontName="Helvetica",
                fontSize=8.5, textColor=WHITE, alignment=TA_CENTER)),
            Paragraph(deposit, ParagraphStyle("cv", fontName="Helvetica",
                fontSize=8.5, textColor=WHITE, alignment=TA_CENTER)),
            Paragraph("C of O", ParagraphStyle("cv", fontName="Helvetica-Bold",
                fontSize=8.5, textColor=GOLD, alignment=TA_CENTER)),
        ])

    cw_total = W - 50 * mm
    col_ws = [cw_total * 0.15, cw_total * 0.22, cw_total * 0.28, cw_total * 0.18, cw_total * 0.17]
    tbl = Table(rows, colWidths=col_ws)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), DKGREEN),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#2A5A38")),
        ("BOX", (0, 0), (-1, -1), 1, MDGREEN),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    for i in range(1, len(rows)):
        bg = MDGREEN if i % 2 == 1 else LTGREEN
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))
    tbl.setStyle(TableStyle(style_cmds))
    elems.append(tbl)

    elems.append(Spacer(1, 6))
    docs_text = "Each plot comes with: " + "  |  ".join(DOCS_LIST)
    elems.append(Paragraph(docs_text,
        ParagraphStyle("docs", fontName="Helvetica", fontSize=8,
            textColor=MUTED, leading=12, spaceAfter=6)))

    notes_data = [
        [
            Paragraph("Pay Outright", ParagraphStyle("nl", fontName="Helvetica-Bold",
                fontSize=8, textColor=GOLD, alignment=TA_CENTER)),
            Paragraph("6 Months Interest-Free", ParagraphStyle("nl", fontName="Helvetica-Bold",
                fontSize=8, textColor=GOLD, alignment=TA_CENTER)),
            Paragraph("Bank Account", ParagraphStyle("nl", fontName="Helvetica-Bold",
                fontSize=8, textColor=GOLD, alignment=TA_CENTER)),
        ],
        [
            Paragraph("Instant allocation on payment", ParagraphStyle("nv", fontName="Helvetica",
                fontSize=8, textColor=WHITE, alignment=TA_CENTER)),
            Paragraph("Deposit from N2M, balance monthly", ParagraphStyle("nv", fontName="Helvetica",
                fontSize=8, textColor=WHITE, alignment=TA_CENTER)),
            Paragraph("LAND REPUBLIC LIMITED\n78 Finance Co or 78 MFB | 0001549819",
                ParagraphStyle("nv", fontName="Helvetica", fontSize=7.5, textColor=WHITE,
                    alignment=TA_CENTER, leading=11)),
        ],
    ]
    cw2 = cw_total / 3
    tbl2 = Table(notes_data, colWidths=[cw2] * 3)
    tbl2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0A2018")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LINEAFTER", (0, 0), (-2, -1), 0.5, colors.HexColor("#1A4A32")),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, GOLD),
        ("BOX", (0, 0), (-1, -1), 1, MDGREEN),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elems.append(tbl2)
    return elems


def make_why_works_pdf(styles, title, first_name):
    full_title = f"{title} {first_name}"
    elems = [Spacer(1, 14)]
    elems.append(Paragraph(
        f"{full_title.upper()}, AT A QUICK GLANCE, HERE IS WHY THIS GENERALLY WORKS",
        styles["section_label"]
    ))
    elems.append(Paragraph("Four Reasons This Investment Makes Sense", styles["section_title"]))

    reasons = [
        ("01", "Lagos Overflow Is Structural, Not a Trend",
         "Lagos is running out of affordable, titled land and what it cannot contain flows into Mowe via the expressway. "
         "That is the documented consequence of two cities growing toward each other, and it does not stop."),
        ("02", "60+ Multinationals Drive Constant Housing Demand",
         "Nestle, AB InBev, CWAY, Rite Foods, and dozens more employ tens of thousands of workers in this corridor. "
         "Those workers need housing nearby. Supply of titled, well-located land is already short."),
        ("03", "RCCG City Is an Anchor Nothing Can Replicate",
         "2,500 hectares. 200,000 residents. 197 countries of RCCG membership. Millions of annual visitors. "
         "This demand does not fluctuate with the economy. It only compounds."),
        ("04", "Lagos-Ogun Infrastructure MOU Has Been Signed",
         "Two state governments committed to joint roads, waterworks, rail, and waterways in this corridor. "
         "Government money follows where government signs, and property values follow government money."),
    ]

    for num, ttl, desc in reasons:
        row = [
            [Paragraph(num, ParagraphStyle("rn", fontName="Times-Bold", fontSize=22,
                textColor=GOLD, alignment=TA_CENTER, leading=28))],
            [
                Paragraph(ttl, ParagraphStyle("rt", fontName="Helvetica-Bold", fontSize=9.5,
                    textColor=DKGREEN, leading=13, spaceAfter=4)),
                Paragraph(desc, ParagraphStyle("rd", fontName="Helvetica", fontSize=8.5,
                    textColor=colors.HexColor("#333333"), leading=13)),
            ]
        ]
        tbl = Table([row[0:1] + [row[1]]], colWidths=[18 * mm, W - 50 * mm - 18 * mm])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#E4F0E8")),
            ("BACKGROUND", (1, 0), (1, 0), CREAM),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (0, 0), 4),
            ("LEFTPADDING", (1, 0), (1, 0), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#C0D8C0")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elems.append(tbl)
        elems.append(Spacer(1, 3))
    return elems


def make_bungalows_pdf(styles, title, first_name):
    full_title = f"{title} {first_name}"
    elems = [Spacer(1, 14)]
    elems.append(Paragraph(
        f"{full_title.upper()}, THERE IS ONE MORE THING", styles["section_label"]
    ))
    elems.append(Paragraph("Modern Bungalows Are Also Coming to Mowe Prime", styles["section_title"]))

    intro = (
        "We are not just selling land in this estate. We are also building modern 2-bedroom and 3-bedroom bungalows "
        "right here within Mowe Prime, on good roads, within a well laid-out estate with existing residents and "
        "functioning infrastructure already in place. Construction is starting soon and if a bungalow interests you "
        "alongside or instead of a land plot, we can also build for you as a company. "
        "Just mention it and we will walk you through what that looks like."
    )
    elems.append(Paragraph(intro, styles["body"]))

    bung_items = [
        ("2-Bedroom Bungalow",
         "Compact, modern, and efficient. Ideal for young families, rental income plays, or a personal property "
         "with strong resale upside as the corridor matures."),
        ("3-Bedroom Bungalow",
         "More space, more comfort, more value. Perfect for those who want a ready-made home without the stress "
         "of building, or investors targeting higher rental yields in a growing corridor."),
    ]
    cw = (W - 50 * mm - 8) / 2
    bung_row = []
    for bt, bb in bung_items:
        bung_row.append([
            Paragraph(bt, ParagraphStyle("bt", fontName="Helvetica-Bold", fontSize=10,
                textColor=DKGREEN, leading=14, spaceAfter=4)),
            Paragraph(bb, ParagraphStyle("bb", fontName="Helvetica", fontSize=8.5,
                textColor=DARK, leading=13)),
        ])
    tbl = Table([bung_row], colWidths=[cw, cw])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CREAM),
        ("LINEABOVE", (0, 0), (-1, 0), 2.5, GOLD),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("LINEAFTER", (0, 0), (0, -1), 0.5, colors.HexColor("#C0D8C0")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elems.append(tbl)

    note_row = [[
        Paragraph("Why this matters for your land: ", ParagraphStyle("nl2",
            fontName="Helvetica-Bold", fontSize=8.5, textColor=GOLD, leading=13)),
        Paragraph(
            "Modern finished homes within the same estate directly push up the value of surrounding plots. "
            "Your land benefits whether you build on it or not.",
            ParagraphStyle("nv2", fontName="Helvetica", fontSize=8.5,
                textColor=colors.HexColor("#D0E8D0"), leading=13)
        ),
    ]]
    tbl2 = Table([note_row], colWidths=[55 * mm, W - 50 * mm - 55 * mm])
    tbl2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DKGREEN),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elems.append(tbl2)
    return elems


def make_comparison_pdf(styles, title, first_name):
    full_title = f"{title} {first_name}"
    elems = [Spacer(1, 14)]
    elems.append(Paragraph(
        f"{full_title.upper()}, LET US DO A QUICK MARKET COMPARISON", styles["section_label"]
    ))
    elems.append(Paragraph("How Mowe Prime Compares to the Market", styles["section_title"]))

    headers = ["Factor", "Mowe Prime", "Magboro", "Ibadan Bodija", "Lagos VI"]
    rows = [
        headers,
        ["Price Range", "N8M to N15M", "N18M+", "N40M+", "N180M+"],
        ["Title", "C of O", "Varies", "Varies", "C of O"],
        ["5-Yr Potential", "300 to 450%", "N/A", "N/A", "Saturated"],
        ["Lagos Access", "29km / Expressway", "Closer, pricier", "Ibadan-based", "Already inside"],
        ["Market Status", "Growing corridor", "Expensive entry", "Different market", "No room to grow"],
    ]
    col_ws = [(W - 50 * mm) * f for f in [0.22, 0.22, 0.16, 0.20, 0.20]]
    tbl = Table(rows, colWidths=col_ws)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), DKGREEN),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, 1), (0, -1), DKGREEN),
        ("TEXTCOLOR", (1, 1), (1, -1), MDGREEN),
        ("TEXTCOLOR", (2, 1), (-1, -1), MUTED),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.HexColor("#C0D8C0")),
        ("BOX", (0, 0), (-1, -1), 1, MDGREEN),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    for i in range(1, len(rows)):
        bg = CREAM if i % 2 == 0 else WHITE
        style_cmds.append(("BACKGROUND", (0, i), (-1, i), bg))
        style_cmds.append(("BACKGROUND", (1, i), (1, i), colors.HexColor("#EBF4EE")))
        style_cmds.append(("FONTNAME", (1, i), (1, i), "Helvetica-Bold"))
    tbl.setStyle(TableStyle(style_cmds))
    elems.append(tbl)
    return elems


def make_cta_pdf(styles, agent_name, agent_phone, agent_email, property_url, agent_social, agent_tagline, title, first_name):
    full_title = f"{title} {first_name}"
    elems = [Spacer(1, 16)]

    inner = [
        Paragraph("NEXT STEP", ParagraphStyle("ct0", fontName="Helvetica-Bold",
            fontSize=8, textColor=colors.HexColor("#A8C8A8"), alignment=TA_CENTER, spaceAfter=6)),
        Paragraph(
            f"Your Plot at Mowe Prime Is Waiting, {full_title}",
            styles["cta_main"]
        ),
        Spacer(1, 6),
        Paragraph(
            "The land is real, the title is clean, the corridor is active, and the environment around it is growing. "
            "It only takes one conversation to get your allocation started and secure your own plot. "
            "Let us have a consultation call so we can talk about your preferred tier, payment structure, and any "
            "questions you might have. We can also arrange a site inspection so you see the estate for yourself.",
            ParagraphStyle("ctab", fontName="Helvetica", fontSize=9, textColor=WHITE,
                alignment=TA_CENTER, leading=14, spaceAfter=12)
        ),
        Spacer(1, 8),
    ]

    contact_row = [
        Paragraph(agent_phone, ParagraphStyle("ci", fontName="Helvetica-Bold",
            fontSize=9, textColor=GOLD, alignment=TA_CENTER)),
    ]
    if agent_email:
        contact_row.append(
            Paragraph(agent_email, ParagraphStyle("ci", fontName="Helvetica",
                fontSize=9, textColor=WHITE, alignment=TA_CENTER))
        )
    if property_url:
        contact_row.append(
            Paragraph(property_url.replace("https://", "").replace("http://", "").rstrip("/"),
                ParagraphStyle("ci", fontName="Helvetica-Oblique", fontSize=8.5,
                    textColor=colors.HexColor("#A8C8A8"), alignment=TA_CENTER))
        )

    cw = (W - 50 * mm) / len(contact_row)
    ctbl = Table([contact_row], colWidths=[cw] * len(contact_row))
    ctbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DKGREEN),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LINEAFTER", (0, 0), (-2, -1), 0.5, colors.HexColor("#1A4A32")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    inner.append(ctbl)

    inner.append(Spacer(1, 8))
    inner.append(Paragraph(
        "Account: LAND REPUBLIC LIMITED  |  78 Finance Company or 78 MFB  |  0001549819",
        ParagraphStyle("acct", fontName="Helvetica", fontSize=8,
            textColor=colors.HexColor("#A8C8A8"), alignment=TA_CENTER)
    ))
    inner.append(Spacer(1, 8))
    inner.append(Paragraph(
        f"Prepared by {agent_name}" + (f"  |  {agent_social}" if agent_social else "") + (f"  |  {agent_tagline}" if agent_tagline else ""),
        ParagraphStyle("sig", fontName="Helvetica-Oblique", fontSize=8,
            textColor=colors.HexColor("#A8C8A8"), alignment=TA_CENTER)
    ))

    tbl = Table([[inner]], colWidths=[W - 50 * mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), MDGREEN),
        ("TOPPADDING", (0, 0), (-1, -1), 20),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("LINEABOVE", (0, 0), (-1, 0), 3, GOLD),
    ]))
    elems.append(tbl)
    return elems


def build_pdf(form):
    title      = form.get("title", "Mr.")
    first_name = form.get("first_name", "Valued Investor")
    occupation = form.get("occupation", "Professional")
    goal       = form.get("goal", "build wealth")
    profile    = form.get("profile", "home")
    tier       = form.get("tier", "both")
    agent_name   = form.get("agent_name", "Israel Toluwalope OLALEYE")
    agent_phone  = form.get("agent_phone", "+2349033499271")
    agent_email  = form.get("agent_email", "")
    property_url = form.get("property_url", "landrepublic.co/mowe-prime")
    agent_social  = form.get("agent_social", "")
    agent_tagline = form.get("agent_tagline", "")

    goal_label = GOAL_LABELS.get(goal, "Build Long-Term Wealth")

    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=25 * mm, rightMargin=25 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm,
        title=f"Mowe Prime Pitch - {title} {first_name}"
    )

    styles = build_styles()
    story = []

    story += make_hero_pdf(styles, title, first_name, occupation, goal_label)
    story += make_stats_bar_pdf(styles)
    story += make_investment_brief_pdf(styles, title, first_name, goal, goal_label)
    story += make_corridor_section_pdf(styles, title, first_name)
    story += make_land_case_pdf(styles, title, first_name)
    story += make_tiers_pdf(styles, tier, title, first_name)
    story += make_why_works_pdf(styles, title, first_name)
    story += make_bungalows_pdf(styles, title, first_name)
    story += make_comparison_pdf(styles, title, first_name)
    story += make_cta_pdf(styles, agent_name, agent_phone, agent_email, property_url, agent_social, agent_tagline, title, first_name)

    doc.build(story)
    buf.seek(0)
    return buf


@app.route("/", methods=["GET"])
def index():
    return render_template_string(
        HTML, preview=False, full_title="", hero_sub="",
        goal_para="", show_standard=True, show_premium=True,
        tier_label="Two Entry Points",
        agent_name="", agent_phone="", agent_email="", property_url="",
        agent_social="", agent_tagline=""
    )


@app.route("/generate", methods=["POST"])
def generate():
    form = request.form
    action = form.get("action", "pdf")

    title      = form.get("title", "Mr.")
    first_name = form.get("first_name", "Valued Investor")
    occupation = form.get("occupation", "Professional")
    goal       = form.get("goal", "build wealth")
    profile    = form.get("profile", "home")
    tier       = form.get("tier", "both")
    agent_name   = form.get("agent_name", "Israel Toluwalope OLALEYE")
    agent_phone  = form.get("agent_phone", "+2349033499271")
    agent_email  = form.get("agent_email", "")
    property_url = form.get("property_url", "")
    agent_social  = form.get("agent_social", "")
    agent_tagline = form.get("agent_tagline", "")

    goal_label = GOAL_LABELS.get(goal, "Build Long-Term Wealth")
    full_title = f"{title} {first_name}"
    hero_sub = (
        f"Mowe Prime Estate is for someone like you, a {occupation} whose primary focus is to {goal_label.lower()}"
    )

    show_standard = tier in ("both", "standard")
    show_premium  = tier in ("both", "premium")
    tier_label = "Two Entry Points" if tier == "both" else "One Entry Point"

    if action == "preview":
        return render_template_string(
            HTML, preview=True,
            full_title=full_title,
            hero_sub=hero_sub,
            goal_para=GOAL_PARAGRAPHS.get(goal, GOAL_PARAGRAPHS["build wealth"]),
            show_standard=show_standard,
            show_premium=show_premium,
            tier_label=tier_label,
            agent_name=agent_name,
            agent_phone=agent_phone,
            agent_email=agent_email,
            property_url=property_url,
            agent_social=agent_social,
            agent_tagline=agent_tagline,
        )

    pdf_buf = build_pdf(form)
    fn_clean = first_name.replace(" ", "_")
    return send_file(
        pdf_buf, as_attachment=True,
        download_name=f"Mowe_Prime_Pitch_{fn_clean}.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    print("\n" + "=" * 54)
    print("  MOWE PRIME PITCH GENERATOR  v2")
    print("=" * 54)
    print("  Open on THIS device:  http://localhost:5000")
    print("=" * 54)
    print("  Press Ctrl+C to stop\n")
    app.run(debug=False, port=5000)
