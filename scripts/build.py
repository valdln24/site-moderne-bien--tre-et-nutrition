#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur statique du site Vitalis.
Toutes les pages HTML finales sont générées à partir des composants définis
ici (en-tête, pied de page, blocs répétés) pour garder une navigation et un
pied de page strictement identiques sur tout le site.

Utilisation : python3 scripts/build.py
Les fichiers .html sont (re)générés à la racine du dépôt.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------
# CONFIGURATION — à personnaliser (voir README.md)
# --------------------------------------------------------------------------
CONFIG = {
    "site_name": "Vitalis",
    "tagline": "Énergie, immunité & équilibre au naturel",
    "partner_name": "Valentin Delaine",
    "partner_title": "Partenaire indépendant(e) LR Health & Beauty",
    "city": "Dole",
    "email": "delaineval@gmail.com",
    "phone": "06 36 47 01 31",
    "shop_url": "https://shop.lrworld.com/home?PHP=LJp1okG7ANwL63NJr63rAA%3D%3D",
    "linkedin": "https://www.linkedin.com/in/valentin-delaine-61956533b",
    "siren": "103 127 288",
    "domain": "https://vitalisd.netlify.app",
    # Domaine Plausible (https://plausible.io) pour des statistiques respectueuses
    # de la vie privée, chargées uniquement après consentement aux cookies.
    # Laissez vide ("") pour ne pas activer d'analytics.
    "analytics_domain": "",
}

SHOP = CONFIG["shop_url"]

# --------------------------------------------------------------------------
# ICONES (SVG inline, traits fins, sans dépendance externe)
# --------------------------------------------------------------------------
ICONS = {
    "bolt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h7l-1 8 11-14h-7l0-6z"/></svg>',
    "moon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20c8 0 16-6 16-16-10 0-16 6-16 16Z"/><path d="M4 20c0-6 3-10 8-12"/></svg>',
    "loop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12a8 8 0 0 1 14-5.3M20 12a8 8 0 0 1-14 5.3"/><path d="M18 3v4h-4M6 21v-4h4"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/></svg>',
    "apple": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8c-3-3-8-2-8 3 0 5 4 9 7 9 1 0 1.5-.5 2-.5s1 .5 2 .5c2.5 0 6-3 7-7-3 0-4.5-1.5-4.5-3.5S18 6.5 19 5c-2-2-5-1-5 1"/><path d="M11 5c0-1.5 1-2.5 2-3"/></svg>',
    "dumbbell": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 7v10M18 7v10M2 10v4M22 10v4M6 12h12"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "chevron": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s7-7.4 7-12a7 7 0 1 0-14 0c0 4.6 7 12 7 12Z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 8v.01"/></svg>',
    "warn": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 2 20h20L12 3Z"/><path d="M12 10v4M12 17v.01"/></svg>',
    "cart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2 3h2l2.6 12.4a2 2 0 0 0 2 1.6h8.8a2 2 0 0 0 2-1.6L22 7H6"/></svg>',
    "gift": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="9" width="18" height="12" rx="1.5"/><path d="M3 13h18M12 9v12"/><path d="M12 9C9 9 8 6.5 9.5 5S12 6 12 9ZM12 9c3 0 4-2.5 2.5-4S12 6 12 9Z"/></svg>',
    "sparkle": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M18 6l-2.5 2.5M8.5 15.5 6 18"/></svg>',
    "drop": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3s7 8 7 13a7 7 0 1 1-14 0c0-5 7-13 7-13Z"/></svg>',
}


def icon(name, cls=""):
    svg = ICONS[name]
    attrs = 'aria-hidden="true" focusable="false"'
    if cls:
        attrs = 'class="%s" %s' % (cls, attrs)
    svg = svg.replace("<svg ", "<svg %s " % attrs, 1)
    return svg


# --------------------------------------------------------------------------
# NAVIGATION — structure des pages
# --------------------------------------------------------------------------
PILLARS = [
    ("energie-vitalite.html", "Énergie & Vitalité", "bolt"),
    ("recuperation-sommeil.html", "Récupération & Sommeil", "moon"),
    ("foie-detox.html", "Foie & Détox cellulaire", "leaf"),
    ("digestion-microbiote.html", "Digestion & Microbiote", "loop"),
    ("immunite.html", "Système immunitaire", "shield"),
]

NAV_MAIN = [
    ("nutrition-objectifs.html", "Nutrition sportive"),
    ("gammes-lr.html", "Gammes LR"),
    ("quiz.html", "Quiz bien-être"),
    ("a-propos.html", "À propos"),
    ("contact.html", "Contact"),
]

LEGAL_LINKS = [
    ("mentions-legales.html", "Mentions légales"),
    ("confidentialite-cookies.html", "Confidentialité & cookies"),
    ("cgu-avertissement.html", "CGU & avertissement santé"),
]

FOOD_SUPPLEMENT_DISCLAIMER = (
    "Les compléments alimentaires ne se substituent pas à une alimentation "
    "variée et équilibrée ni à un mode de vie sain. Respectez toujours la dose "
    "journalière indiquée sur l'emballage. Tenir hors de portée des jeunes "
    "enfants. Demandez conseil à un professionnel de santé en cas de grossesse, "
    "d'allaitement, de traitement médical en cours ou avant toute modification "
    "importante de votre alimentation."
)

INDEPENDENT_DISCLOSURE = (
    "%s est un site personnel et indépendant tenu par %s, %s. "
    "Ce site n'est ni édité ni exploité par LR Health & Beauty Systems GmbH ; "
    "il relaie une sélection de produits distribués sous le statut de Vendeur "
    "à Domicile Indépendant (VDI). Les commandes sont passées exclusivement sur "
    "la boutique en ligne officielle LR, seule plateforme autorisée pour la "
    "vente des produits LR." % (CONFIG["site_name"], CONFIG["partner_name"], CONFIG["partner_title"])
)


# --------------------------------------------------------------------------
# BRIQUES HTML PARTAGÉES
# --------------------------------------------------------------------------
def head(title, description, path, extra_jsonld="", noindex=False):
    canonical = CONFIG["domain"].rstrip("/") + "/" + (path if path != "index.html" else "")
    # `title` inclut déjà le nom du site (voir les appels à page()) : ne pas le rajouter ici.
    og_title = title
    og_image = CONFIG["domain"].rstrip("/") + "/assets/img/og-image.png"
    favicon = (
        "data:image/svg+xml,"
        "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
        "%3Ccircle cx='50' cy='50' r='48' fill='%230d4a32'/%3E"
        "%3Cpath d='M50 20c-16 16-16 44 0 60 16-16 16-44 0-60Z' fill='%23c96f4a'/%3E"
        "%3C/svg%3E"
    )
    return """<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:image" content="%s">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="fr_FR">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%s">
<meta name="twitter:description" content="%s">
<meta name="twitter:image" content="%s">
<meta name="robots" content="%s">
<link rel="icon" href="%s">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400..600&family=Work+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
<script>window.__VITALIS_ANALYTICS__=%s;</script>
%s
</head>""" % (
        og_title, description, canonical,
        CONFIG["site_name"], og_title, description, canonical, og_image,
        og_title, description, og_image,
        "noindex, nofollow" if noindex else "index, follow",
        favicon,
        json.dumps(CONFIG.get("analytics_domain", "") or None),
        extra_jsonld,
    )


def dropdown_pillars():
    return "\n".join(
        '<a href="%s">%s %s</a>' % (href, icon(ic, "pillar-icon"), label)
        for href, label, ic in PILLARS
    )


def btn(label, href="#", variant="primary", blank=False, sm=False, block=False, extra_class=""):
    cls = "btn btn-%s" % variant
    if sm:
        cls += " btn-sm"
    if block:
        cls += " btn-block"
    if extra_class:
        cls += " " + extra_class
    target = ' target="_blank" rel="noopener sponsored"' if blank else ""
    circle_icon = "cart" if blank else "arrow"
    return '<a class="%s" href="%s"%s aria-label="%s"><span class="btn-label">%s</span><span class="btn-circle">%s</span></a>' % (
        cls, href, target, label, label, icon(circle_icon)
    )


def header(active=""):
    pillar_links = dropdown_pillars()
    nav_items = ""
    is_pillar_active = active in [p[0] for p in PILLARS]
    nav_items += """
    <div class="dropdown">
      <a href="#" class="%s" onclick="return false;">Univers bien-être %s</a>
      <div class="dropdown-panel">%s</div>
    </div>""" % ("active" if is_pillar_active else "", icon("chevron", "pillar-icon"), pillar_links)
    for href, label in NAV_MAIN:
        cls = " active" if active == href else ""
        nav_items += '\n    <a href="%s" class="%s">%s</a>' % (href, cls.strip(), label)

    return """<header class="site-header">
  <div class="container">
    <a href="index.html" class="logo"><span class="dot"></span>%s</a>
    <nav class="nav-desktop" id="siteNav">%s
    </nav>
    <div class="nav-cta">
      %s
      <button class="nav-toggle" aria-label="Ouvrir le menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>""" % (CONFIG["site_name"], nav_items, btn("Ma boutique LR", SHOP, variant="primary", blank=True, sm=True))


def footer():
    pillar_li = "\n".join('<li><a href="%s">%s</a></li>' % (h, l) for h, l, _ in PILLARS)
    main_li = "\n".join('<li><a href="%s">%s</a></li>' % (h, l) for h, l in NAV_MAIN)
    legal_li = "\n".join('<li><a href="%s">%s</a></li>' % (h, l) for h, l in LEGAL_LINKS)
    return """<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div>
        <div class="footer-logo">%s</div>
        <p style="color:rgba(255,255,255,.65);max-width:320px;margin:0;">%s</p>
      </div>
      <div class="footer-badges">
        <a class="footer-badge" href="%s" target="_blank" rel="noopener sponsored">%s<span>Ma boutique<small>LR officielle</small></span></a>
        <a class="footer-badge" href="%s" target="_blank" rel="noopener">%s<span>LinkedIn<small>Me suivre</small></span></a>
      </div>
    </div>
    <div class="footer-grid">
      <div>
        <ul style="display:flex;gap:14px;">
          <li><a href="mailto:%s" aria-label="Email">%s</a></li>
          <li><a href="%s" target="_blank" rel="noopener">%s</a></li>
        </ul>
      </div>
      <div>
        <h4>Univers bien-être</h4>
        <ul>%s</ul>
      </div>
      <div>
        <h4>Navigation</h4>
        <ul>%s</ul>
      </div>
      <div>
        <h4>Informations légales</h4>
        <ul>%s</ul>
      </div>
    </div>
    <p class="footer-disclaimer">%s</p>
    <p class="footer-disclaimer">%s</p>
    <div class="footer-bottom">
      <span>© <span data-year></span> %s — %s</span>
      <span>Site indépendant · Vente exclusivement via la boutique officielle LR</span>
    </div>
  </div>
</footer>
<div class="cookie-banner" data-cookie-banner hidden>
  <p>Ce site utilise uniquement des cookies techniques nécessaires à son fonctionnement. Aucun cookie publicitaire n'est déposé sans votre consentement. En savoir plus dans notre <a href="confidentialite-cookies.html">politique de confidentialité</a>.</p>
  <div class="cookie-actions">
    <button type="button" class="btn btn-outline btn-sm" data-cookie-decline>Refuser</button>
    <button type="button" class="btn btn-primary btn-sm" data-cookie-accept>J'ai compris</button>
  </div>
</div>
<script src="assets/js/main.js"></script>""" % (
        CONFIG["site_name"],
        CONFIG["tagline"],
        SHOP, icon("cart"),
        CONFIG["linkedin"], icon("sparkle"),
        CONFIG["email"], icon("mail"),
        "tel:" + CONFIG["phone"].replace(" ", ""), icon("phone"),
        pillar_li,
        main_li,
        legal_li,
        INDEPENDENT_DISCLOSURE,
        FOOD_SUPPLEMENT_DISCLAIMER,
        CONFIG["site_name"], CONFIG["partner_name"],
    )


def page(slug, title, description, body, active="", extra_jsonld="", extra_scripts="", noindex=False):
    return """<!DOCTYPE html>
<html lang="fr">
%s
<body>
<a class="skip-link" href="#main-content">Aller au contenu</a>
%s
<main id="main-content">
%s
</main>
%s
%s
</body>
</html>""" % (head(title, description, slug, extra_jsonld, noindex=noindex), header(active), body, footer(), extra_scripts)


def notice(text, warn=False, ic="info"):
    return """<div class="notice%s" data-reveal>%s<p style="margin:0;">%s</p></div>""" % (
        " warn" if warn else "", icon(ic), text
    )


def promo_vip_band():
    return """<div class="promo-vip" data-reveal>
  <div class="icon-badge">%s</div>
  <div class="eyebrow">Budget serré ?</div>
  <div class="promo-headline">Prix VIP <em>-30%% à vie</em></div>
  <p>Créez votre compte avantage pour seulement 10&nbsp;€ et profitez de -30%% à vie sur tous vos produits LR. Une seule fois, pour toujours.</p>
  %s
</div>""" % (icon("gift"), btn("Contactez-moi", "contact.html", variant="white"))


def cta_band(title_text, text, primary_href, primary_label, secondary_href=None, secondary_label=None, primary_blank=False, secondary_blank=False):
    secondary = ""
    if secondary_href:
        secondary = btn(secondary_label, secondary_href, variant="white", blank=secondary_blank)
    return """<div class="cta-band" data-reveal>
  <div>
    <h2>%s</h2>
    <p>%s</p>
  </div>
  <div style="display:flex;gap:14px;flex-wrap:wrap;">
    %s
    %s
  </div>
</div>""" % (title_text, text, btn(primary_label, primary_href, variant="terracotta", blank=primary_blank), secondary)


def section_head(eyebrow, title, lede, center=False):
    return """<div class="section-head%s" data-reveal>
  <div class="eyebrow">%s</div>
  <h2>%s</h2>
  <p class="lede">%s</p>
</div>""" % (" center" if center else "", eyebrow, title, lede)


def initials(name):
    words = [w for w in re.split(r"[^A-Za-zÀ-ÿ]+", name) if len(w) >= 2 and w.upper() != "REMPLACER"]
    letters = "".join(w[0] for w in words[:2]).upper()
    return letters or "LR"


def word_reveal(text):
    raw = text.split(" ")
    words = []
    buffer = None
    for w in raw:
        if buffer is not None:
            buffer += " " + w
            if "</em>" in w:
                words.append(buffer)
                buffer = None
        elif "<em>" in w and "</em>" not in w:
            buffer = w
        else:
            words.append(w)
    if buffer:
        words.append(buffer)
    spans = []
    for i, w in enumerate(words):
        delay = round(i * 0.045, 3)
        spans.append('<span class="word" style="animation-delay:%ss">%s</span>' % (delay, w))
    return " ".join(spans)


def breadcrumb(label):
    return '<p class="breadcrumb"><a href="index.html">Accueil</a> &nbsp;/&nbsp; %s</p>' % label


def check_list(items, icon_name="check", modifier=""):
    lis = "\n".join('<li>%s<span>%s</span></li>' % (icon(icon_name), t) for t in items)
    cls = "check-list " + modifier if modifier else "check-list"
    return '<ul class="%s">%s</ul>' % (cls, lis)


def product_card(tag, title, desc, bullets, href, swatch_color, icon_name, bestseller=False, image=None):
    lis = "\n".join("<li>%s</li>" % b for b in bullets)
    bestseller_chip = (
        '<span class="chip-float chip--br dark">%s +60M vendues</span>' % icon("sparkle")
        if bestseller else ""
    )
    if image:
        swatch_cls = "swatch has-photo"
        swatch_style = ""
        visual = '<img src="%s" alt="%s" loading="lazy">' % (image, title)
    else:
        swatch_cls = "swatch photo-block"
        swatch_style = ' style="background:%s;"' % swatch_color
        visual = icon(icon_name)
    return """<div class="product-card" data-reveal>
  <div class="%s"%s>
    <span class="chip-float chip--tl">%s%s</span>
    %s
    %s
  </div>
  <div class="body">
    <h3>%s</h3>
    <p>%s</p>
    <ul>%s</ul>
    <a class="btn btn-outline btn-sm" href="%s" target="_blank" rel="noopener sponsored"><span class="btn-label">Voir sur ma boutique LR</span><span class="btn-circle">%s</span></a>
  </div>
</div>""" % (swatch_cls, swatch_style, icon("check"), tag, visual, bestseller_chip, title, desc, lis, href, icon("arrow"))


def pillar_teaser_card(href, title, ic, desc, tone="", kicker="Pilier bien-être"):
    tone_cls = ("tone-" + tone) if tone else ""
    return """<a href="%s" class="media-card" data-reveal style="display:block;">
  <div class="media photo-block ratio-wide %s">
    <span class="chip-float chip--tl">%s %s</span>
    %s
  </div>
  <div class="caption">
    <h3>%s</h3>
    <p>%s</p>
    <span class="card-link">Découvrir %s</span>
  </div>
</a>""" % (href, tone_cls, icon("sparkle"), kicker, icon(ic), title, desc, icon("arrow"))


def testimonial(stars, quote, author):
    return """<div class="testi" data-reveal>
  <span class="testi-quote">&ldquo;</span>
  <div class="stars">%s</div>
  <p>%s</p>
  <footer><span class="avatar" style="width:36px;height:36px;font-size:.72rem;">%s</span>%s</footer>
</div>""" % ("★" * stars, quote, initials(author), author)


ORG_JSONLD = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "%s",
  "jobTitle": "%s",
  "url": "%s",
  "worksFor": {"@type": "Organization", "name": "LR Health & Beauty Systems GmbH"}
}
</script>""" % (CONFIG["partner_name"], CONFIG["partner_title"], CONFIG["domain"])


# --------------------------------------------------------------------------
# GABARIT COMMUN DES PAGES "PILIERS" SANTÉ
# --------------------------------------------------------------------------
def build_pillar_page(cfg):
    signs_html = "\n".join(
        '<div class="card" data-reveal><div class="icon-badge terra">%s</div><h3>%s</h3><p>%s</p></div>' % (icon(s["icon"]), s["title"], s["text"])
        for s in cfg["signs"]
    )
    levers_html = "\n".join(
        '<div class="card" data-reveal><div class="icon-badge">%s</div><h3>%s</h3><p>%s</p></div>' % (icon(l["icon"]), l["title"], l["text"])
        for l in cfg["levers"]
    )
    products_html = "\n".join(product_card(**p) for p in cfg["products"])
    faq_html = "\n".join(
        '<details data-reveal style="background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px 24px;margin-bottom:14px;"><summary style="cursor:pointer;font-weight:600;font-family:var(--font-display);font-size:1.05rem;">%s</summary><p style="margin-top:12px;">%s</p></details>' % (f["q"], f["a"])
        for f in cfg["faq"]
    )
    faq_jsonld = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}
</script>""" % ",".join(
        '{"@type":"Question","name":%r,"acceptedAnswer":{"@type":"Answer","text":%r}}' % (f["q"], f["a"])
        for f in cfg["faq"]
    )

    hero_section = """<section class="page-hero">
  <div class="container">
    %s
    <div class="eyebrow">%s</div>
    <h1 style="max-width:820px;">%s</h1>
    <p class="lede" style="max-width:680px;">%s</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="quiz.html">Faire mon diagnostic bien-être %s</a>
      <a class="btn btn-outline" href="#gamme-associee">Voir la gamme associée</a>
    </div>
  </div>
</section>""" % (breadcrumb(cfg["title"]), cfg["eyebrow"], cfg["title"], cfg["lede"], icon("arrow"))

    notice_section = """<section class="section-tight">
  <div class="container">
    %s
  </div>
</section>""" % notice(cfg["intro_notice"])

    understand_section = """<section class="section section-alt">
  <div class="container">
    %s
    <div class="split">
      <div data-reveal>
        %s
      </div>
      <div class="split-visual" data-reveal>
        <h3 style="margin-bottom:18px;">%s</h3>
        %s
      </div>
    </div>
  </div>
</section>""" % (
        section_head("Comprendre", cfg["understand_title"], cfg["understand_lede"]),
        cfg["understand_body"],
        cfg["facts_title"],
        check_list(cfg["facts"]),
    )

    photo_section = ""
    if cfg.get("photo"):
        ph = cfg["photo"]
        photo_section = """<section class="section">
  <div class="container">
    <div class="split">
      <div class="pillar-photo" data-reveal>
        <img src="%s" alt="%s" loading="lazy" width="%s" height="%s">
      </div>
      <div data-reveal>
        <div class="eyebrow">%s</div>
        <h2>%s</h2>
        <p class="lede">%s</p>
      </div>
    </div>
  </div>
</section>""" % (ph["src"], ph["alt"], ph["w"], ph["h"], ph["eyebrow"], ph["title"], ph["text"])

    signs_section = """<section class="section">
  <div class="container">
    %s
    <div class="grid grid-4">
      %s
    </div>
  </div>
</section>""" % (
        section_head("Signaux à surveiller", "Ce que votre corps essaie de vous dire", "Ces manifestations sont fréquentes et généralement liées à l'hygiène de vie. Si elles sont intenses, inhabituelles ou persistantes, consultez un professionnel de santé : ce site n'a pas vocation à poser un diagnostic."),
        signs_html,
    )

    levers_section = """<section class="section section-sage">
  <div class="container">
    %s
    <div class="grid grid-4">
      %s
    </div>
  </div>
</section>""" % (
        section_head("Les leviers naturels", "Ce qui fait <em>vraiment</em> la différence au quotidien", "Avant tout complément, ce sont ces habitudes simples et régulières qui posent les fondations d'un bon équilibre."),
        levers_html,
    )

    merged_section = ""
    if cfg.get("merge_understand"):
        signs_items = ["%s — %s" % (s["title"], s["text"]) for s in cfg["signs"]]
        levers_items = ["%s — %s" % (l["title"], l["text"]) for l in cfg["levers"]]
        merged_section = """<section class="section section-alt" id="comprendre">
  <div class="container">
    %s
    <div class="understand-copy" data-reveal>
      %s
    </div>
    <div class="grid grid-2">
      <div data-reveal>
        <h3 class="mini-list-title warn">%s Signaux à surveiller</h3>
        %s
      </div>
      <div data-reveal>
        <h3 class="mini-list-title">%s Les leviers naturels</h3>
        %s
      </div>
    </div>
  </div>
</section>""" % (
            section_head("Comprendre & agir", cfg["understand_title"], cfg["understand_lede"]),
            cfg["understand_body"],
            icon("warn"), check_list(signs_items, icon_name="warn", modifier="warn-list"),
            icon("leaf"), check_list(levers_items),
        )

    products_section = """<section class="section" id="gamme-associee">
  <div class="container">
    %s
    <div class="grid %s">
      %s
    </div>
    <p class="form-note" style="margin-top:20px;">%s</p>
  </div>
</section>""" % (
        section_head("La gamme LR associée", cfg["range_title"], cfg["range_lede"]),
        cfg.get("products_grid", "grid-3"),
        products_html,
        FOOD_SUPPLEMENT_DISCLAIMER,
    )

    testimonials_section = """<section class="section section-alt">
  <div class="container">
    %s
    <div class="grid grid-2">
      %s
      %s
    </div>
  </div>
</section>""" % (
        section_head("Ils en parlent", "Des parcours, pas des promesses", "Témoignages personnels et non contractuels — les résultats varient selon chaque personne et son mode de vie."),
        testimonial(*cfg["testimonials"][0]),
        testimonial(*cfg["testimonials"][1]),
    )

    faq_section = """<section class="section">
  <div class="container" style="max-width:840px;">
    %s
    %s
  </div>
</section>""" % (
        section_head("Questions fréquentes", "Vous vous demandez peut-être...", ""),
        faq_html,
    )

    cta_section = """<section class="section-tight">
  <div class="container">
    %s
  </div>
</section>""" % cta_band(
        "Un <em>accompagnement</em> plutôt qu'une liste de produits",
        "Répondez à 3 questions pour recevoir une orientation personnalisée, puis échangeons ensemble de vos objectifs.",
        "quiz.html", "Faire le quiz gratuit",
        "contact.html", "Me contacter directement",
    )

    if cfg.get("merge_understand"):
        sections = [hero_section, notice_section, photo_section, products_section, merged_section, testimonials_section, faq_section, cta_section]
    else:
        sections = [hero_section, notice_section, understand_section, photo_section, signs_section, levers_section, products_section, testimonials_section, faq_section, cta_section]

    body = "\n\n".join(s for s in sections if s)
    return page(cfg["slug"], cfg["title"] + " — " + CONFIG["site_name"], cfg["meta_desc"], body, active=cfg["slug"], extra_jsonld=faq_jsonld)


PILLAR_PAGES = [
    dict(
        slug="energie-vitalite.html",
        products_grid="grid-4",
        merge_understand=True,
        eyebrow="Pilier bien-être",
        title="Énergie & Vitalité",
        lede="Retrouver un tonus stable du matin au soir, sans montagnes russes ni coups de barre à 16h : voici comment fonctionne réellement votre énergie, et comment la soutenir durablement.",
        meta_desc="Comprendre les causes du manque d'énergie et de fatigue au quotidien, et découvrir les leviers naturels et la gamme LR Mind Master pour retrouver de la vitalité.",
        intro_notice="Cette page a un objectif d'information générale sur l'hygiène de vie. Elle ne remplace pas un avis médical, en particulier en cas de fatigue intense, brutale ou qui persiste au-delà de quelques semaines.",
        photo=dict(
            src="assets/img/energie-silhouette.jpg",
            alt="Silhouette d'une femme bras ouverts face à l'horizon, symbole d'énergie retrouvée",
            w="1200", h="1984",
            eyebrow="Retrouver son élan",
            title="L'énergie, ça se <em>ressent</em> avant de se mesurer",
            text="Ce n'est pas qu'une question de volonté : quand le sommeil, l'hydratation et l'alimentation sont alignés, l'énergie revient naturellement — et ça se voit dans la façon de se tenir, de bouger, d'aborder sa journée.",
        ),
        understand_title="D'où vient vraiment la fatigue du quotidien ?",
        understand_lede="Le manque d'énergie n'a presque jamais une seule cause : c'est souvent la somme de petits déséquilibres.",
        understand_body="""<p>La fatigue « fonctionnelle » — celle qui touche la majorité des adultes actifs — résulte le plus souvent d'un cumul : nuits trop courtes ou de mauvaise qualité, hydratation insuffisante, repas déséquilibrés ou trop espacés, sédentarité, charge mentale et stress chronique. Le corps carbure alors en mode « économie d'énergie », avec cette sensation familière de devoir puiser dans ses réserves dès le milieu de matinée.</p><p>Avant de chercher une solution miracle, il est utile d'identifier lequel de ces facteurs pèse le plus dans votre quotidien : est-ce le sommeil, l'alimentation, le rythme, ou un peu des trois ? C'est exactement ce que le quiz bien-être vous aide à clarifier en quelques questions.</p>""",
        facts_title="4 repères à connaître",
        facts=[
            "Une baisse d'énergie en début d'après-midi est normale (rythme circadien) — elle ne signifie pas forcément un problème de fond.",
            "La déshydratation, même légère (1 à 2%), suffit à réduire la vigilance et la concentration.",
            "Les glucides rapides donnent un pic d'énergie... suivi d'une chute plus marquée une heure plus tard.",
            "L'activité physique régulière augmente l'énergie disponible à moyen terme, même si l'effet immédiat est une sensation de fatigue.",
        ],
        signs=[
            dict(icon="warn", title="Fatigue dès le réveil", text="Vous vous sentez fatigué(e) malgré une nuit complète : le sommeil profond est peut-être insuffisant."),
            dict(icon="warn", title="Coup de barre après le repas", text="Une somnolence marquée après le déjeuner peut signaler un repas trop riche en sucres rapides."),
            dict(icon="warn", title="Difficultés de concentration", text="Le cerveau consomme énormément d'énergie : le premier organe à en souffrir est souvent l'attention."),
            dict(icon="warn", title="Motivation en berne", text="La fatigue mentale et la fatigue physique sont liées : l'une entretient souvent l'autre."),
        ],
        levers=[
            dict(icon="moon", title="Un sommeil régulier", text="Se coucher et se lever à heures fixes, même le week-end, stabilise l'horloge interne."),
            dict(icon="drop", title="Une hydratation suffisante", text="1,5 L d'eau par jour en moyenne, davantage par temps chaud ou en cas d'activité physique."),
            dict(icon="apple", title="Des repas équilibrés", text="Associer protéines, bonnes graisses et fibres limite les pics puis les chutes de glycémie."),
            dict(icon="bolt", title="Du mouvement quotidien", text="20 à 30 minutes de marche active suffisent à relancer la circulation et l'oxygénation."),
        ],
        range_title="Mind Master — le coup de pouce ciblé",
        range_lede="Une gamme pensée pour accompagner la vigilance et l'énergie mentale au quotidien, à utiliser en complément (et non à la place) d'une bonne hygiène de vie.",
        products=[
            dict(
                tag="Mind Master Red", title="Mind Master Formula Red",
                desc="La variante rouge à la saveur fruitée de raisin, pour une vie active et énergique.",
                bullets=[
                    "Thiamine & B12 : métabolisme énergétique normal",
                    "B12 : bon fonctionnement du système nerveux et psychique",
                    "B12 & fer : réduisent la fatigue et l'épuisement",
                    "Vitamine E : protège les cellules du stress oxydant",
                ],
                href="https://shop.lrworld.com/product/fr/fr/lr_lifetakt_mind_master_formula_red.html?productAlias=80950-604&casrnc=cac57",
                swatch_color="linear-gradient(135deg,#c96f4a,#a8552f)", icon_name="bolt",
                image="assets/img/mind-master-red.jpg",
            ),
            dict(
                tag="Mind Master Gold", title="Mind Master Formula Gold",
                desc="Pour l'énergie, la performance et l'équilibre mental, quoi que le quotidien réserve.",
                bullets=[
                    "B12 : métabolisme énergétique normal, réduit la fatigue",
                    "Fer : fonction cognitive normale, transport de l'oxygène",
                    "Vitamine D : ossature et fonction musculaire normales",
                    "Vitamine E : protège les cellules du stress oxydatif",
                ],
                href="https://shop.lrworld.com/product/fr/fr/mind_master_formula_gold.html?productAlias=80940-4&casrnc=6ffb9",
                swatch_color="linear-gradient(135deg,#d9a441,#a8752c)", icon_name="sparkle",
                image="assets/img/mind-master-gold.jpg",
            ),
            dict(
                tag="Coup de fouet", title="Mind Master Extreme",
                desc="Le format stick à emporter partout, à consommer sans eau pour un coup de fouet rapide.",
                bullets=[
                    "Caféine du guarana : attention, concentration, endurance",
                    "B6, B12 & thiamine : soutiennent la fonction psychique",
                    "Vitamine C : fonctionnement normal du système immunitaire",
                    "100% des besoins journaliers en vitamines E et D",
                ],
                href="https://shop.lrworld.com/product/fr/fr/mind_master_extreme.html?productAlias=80980-398&casrnc=2ccd7",
                swatch_color="linear-gradient(135deg,#5f7a5a,#3f5a3c)", icon_name="bolt",
                image="assets/img/mind-master-extreme.jpg",
            ),
            dict(
                tag="Multivitamines", title="Vita Active Fruits Rouges",
                desc="Un concentré de 21 fruits et légumes et 10 vitamines essentielles, une cuillère à café par jour.",
                bullets=[
                    "Vitamines D & B6 : bon fonctionnement du système immunitaire",
                    "Vitamine B12 : favorise la division cellulaire",
                    "Vitamine B1 : contribue à une fonction cardiaque normale",
                    "21 fruits et légumes concentrés, pour toute la famille",
                ],
                href="https://shop.lrworld.com/product/fr/fr/vita_active_fruits_rouges.html?productAlias=80301-699&casrnc=2009b",
                swatch_color="linear-gradient(135deg,#d9a441,#a8752c)", icon_name="leaf",
                image="assets/img/vita-active.jpg",
            ),
        ],
        testimonials=[
            (5, "En ajustant mon sommeil et mon petit-déjeuner, j'ai retrouvé une énergie plus stable dans la journée. Le quiz du site m'a aidée à savoir par où commencer.", "Camille, 34 ans"),
            (5, "Je pensais avoir besoin de compléments, en fait c'est surtout mon rythme de sommeil qui posait problème. Contenu très honnête.", "Julien, 41 ans"),
        ],
        faq=[
            dict(q="Un complément alimentaire peut-il suffire à lui seul contre la fatigue ?", a="Non : un complément vient en soutien d'une alimentation variée et d'un mode de vie sain, il ne les remplace pas. Si la fatigue persiste, consultez un médecin pour écarter une cause à explorer médicalement."),
            dict(q="Combien de temps pour ressentir une différence sur mon énergie ?", a="Cela dépend entièrement de la personne et des habitudes mises en place. Les effets d'un changement d'hygiène de vie s'observent en général sur plusieurs semaines, avec de la régularité."),
            dict(q="Où puis-je commander les produits évoqués ?", a="Uniquement sur ma boutique en ligne officielle LR, seule plateforme autorisée pour la vente des produits — le lien est disponible en haut de chaque page."),
        ],
    ),
    dict(
        slug="recuperation-sommeil.html",
        eyebrow="Pilier bien-être",
        title="Récupération & Sommeil",
        lede="Le sommeil est le moment où le corps répare, régénère et consolide la mémoire. Mieux le comprendre, c'est se donner les moyens de vraiment récupérer — pas seulement de dormir plus longtemps.",
        meta_desc="Mieux comprendre la récupération et le sommeil : signaux d'alerte, leviers naturels et accompagnement Health Mission pour un repos vraiment réparateur.",
        intro_notice="Ce contenu est informatif et ne se substitue pas à un avis médical. En cas de troubles du sommeil sévères ou prolongés (insomnie, apnée suspectée...), consultez un professionnel de santé.",
        understand_title="Dormir plus ne veut pas dire récupérer mieux",
        understand_lede="La qualité du sommeil compte souvent davantage que sa durée brute.",
        understand_body="""<p>Une nuit se compose de plusieurs cycles de sommeil léger, profond et paradoxal. C'est le sommeil profond qui assure la récupération physique, et le sommeil paradoxal qui consolide la mémoire et régule les émotions. Le stress, les écrans en soirée, la caféine tardive ou un dîner trop copieux fragmentent ces cycles — on peut alors dormir 8 heures et se réveiller quand même fatigué.</p><p>La récupération concerne aussi le corps après l'effort physique ou une période de forte charge mentale : elle passe par le repos, mais aussi par l'hydratation, la nutrition et la gestion du stress.</p>""",
        facts_title="4 repères à connaître",
        facts=[
            "Un cycle de sommeil dure environ 90 minutes ; on en enchaîne 4 à 6 par nuit.",
            "La lumière bleue des écrans retarde la sécrétion de mélatonine, l'hormone du sommeil.",
            "La température idéale d'une chambre se situe autour de 18°C.",
            "Le magnésium et certaines plantes (valériane, mélisse) sont traditionnellement associés à la détente.",
        ],
        signs=[
            dict(icon="warn", title="Réveils nocturnes fréquents", text="Un sommeil fragmenté réduit fortement le temps passé en sommeil profond réparateur."),
            dict(icon="warn", title="Endormissement difficile", text="Un mental qui tourne en boucle le soir est souvent lié au stress ou à une surstimulation en soirée."),
            dict(icon="warn", title="Réveil non reposé", text="Se réveiller fatigué malgré une durée de sommeil correcte peut indiquer un sommeil peu profond."),
            dict(icon="warn", title="Tensions musculaires persistantes", text="Un corps qui ne récupère pas physiquement peut accumuler des tensions, notamment après l'effort."),
        ],
        levers=[
            dict(icon="moon", title="Un rituel du coucher", text="Diminuer les écrans 45 minutes avant de dormir et garder des horaires réguliers."),
            dict(icon="leaf", title="Une chambre apaisante", text="Obscurité, calme et fraîcheur favorisent un endormissement plus rapide."),
            dict(icon="drop", title="Limiter les excitants", text="Réduire caféine et alcool en fin de journée améliore nettement la qualité du sommeil."),
            dict(icon="apple", title="Un dîner léger", text="Un repas trop riche ou trop tardif retarde et perturbe l'endormissement."),
        ],
        range_title="Health Mission — le rituel détente",
        range_lede="Des formules pensées pour accompagner les moments de relâchement et soutenir l'organisme dans ses phases de récupération.",
        products=[
            dict(tag="Oméga-3", title="Capsules Super Omega", desc="Des oméga-3 marins pour le bien-être cardiaque, issus de la pêche durable.", bullets=["Huile de poisson riche en oméga-3", "Contribue au bien-être cardiaque", "Certifié Friend of the Sea"], href="https://shop.lrworld.com/product/fr/fr/capsules_super_omega.html?productAlias=80338-699&casrnc=333bd", swatch_color="linear-gradient(135deg,#c96f4a,#a8552f)", icon_name="drop"),
            dict(tag="Aloe Vera", title="Aloe Vera Drinking Gel", desc="À intégrer dans une routine bien-être quotidienne, en cure.", bullets=["Aloe Vera issu de culture contrôlée", "Format buvable", "Cure de 1 à 3 mois"], href=SHOP, swatch_color="linear-gradient(135deg,#d9a441,#a8752c)", icon_name="leaf"),
        ],
        testimonials=[
            (5, "Mon rituel du soir a tout changé : moins d'écran, une tisane, et une vraie sensation de récupération le matin.", "Sophie, 29 ans"),
            (4, "Après le sport, j'ai enfin arrêté d'ignorer la récupération. Résultat : moins de courbatures et un meilleur sommeil.", "Karim, 37 ans"),
        ],
        faq=[
            dict(q="Le magnésium peut-il aider en cas de stress ?", a="Le magnésium contribue à une fonction psychologique et musculaire normale et à réduire la fatigue, dans le cadre d'une alimentation équilibrée. Il ne traite pas un trouble anxieux, qui relève d'un accompagnement médical."),
            dict(q="Faut-il dormir 8 heures pile pour bien récupérer ?", a="Le besoin de sommeil varie d'une personne à l'autre (en général entre 7 et 9 heures pour un adulte). La régularité des horaires compte souvent plus que le chiffre exact."),
            dict(q="Ces produits provoquent-ils de la somnolence dans la journée ?", a="Suivez toujours les doses indiquées sur l'emballage et demandez conseil en cas de doute, en particulier avant la conduite ou l'utilisation de machines."),
        ],
    ),
    dict(
        slug="foie-detox.html",
        eyebrow="Pilier bien-être",
        title="Foie & Détox cellulaire",
        lede="Le foie est l'organe le plus sollicité de votre métabolisme : il filtre, transforme et élimine en continu. Comprendre son fonctionnement aide à savoir comment vraiment l'accompagner — sans mythes ni promesses irréalistes.",
        meta_desc="Comprendre le rôle du foie et du métabolisme cellulaire, les signaux d'un organisme surchargé, et les leviers naturels pour l'accompagner au quotidien.",
        intro_notice="Le foie fonctionne 24h/24 sans intervention extérieure nécessaire chez une personne en bonne santé. Aucun produit ne \"détoxifie\" le foie au sens médical : cette page vise à expliquer son rôle et comment ne pas le surcharger inutilement. En cas de troubles digestifs persistants ou de douleurs, consultez un médecin.",
        understand_title="Ce que fait vraiment votre foie chaque jour",
        understand_lede="Avant de parler « détox », comprenons ce que cet organe accomplit déjà, en permanence.",
        understand_body="""<p>Le foie assure plus de 500 fonctions : il transforme les nutriments issus de la digestion, stocke l'énergie, produit la bile nécessaire à la digestion des graisses, et neutralise les substances dont l'organisme n'a plus besoin (alcool, certains médicaments, déchets métaboliques). C'est un organe qui se régénère remarquablement bien — à condition de ne pas être en permanence sursollicité.</p><p>Le terme « détox » est souvent utilisé de façon marketing : en réalité, le foie et les reins assurent déjà ce rôle d'élimination en continu chez une personne en bonne santé. Le plus utile n'est donc pas de « détoxifier » mais d'éviter de le surcharger : excès d'alcool, de sucres, de graisses saturées, sédentarité prolongée.</p>""",
        facts_title="4 repères à connaître",
        facts=[
            "Le foie est le seul organe interne capable de se régénérer partiellement.",
            "Il stocke le glucose sous forme de glycogène pour le libérer en cas de besoin d'énergie.",
            "Une consommation d'alcool régulière et excessive est le principal facteur de surcharge évitable.",
            "Les repas très riches et espacés (raclette, fêtes...) sollicitent davantage le foie qu'une alimentation régulière.",
        ],
        signs=[
            dict(icon="warn", title="Digestion lourde après les repas", text="Une sensation de lourdeur peut apparaître après des repas riches en graisses."),
            dict(icon="warn", title="Fatigue en période de fêtes", text="Excès alimentaires et alcool ponctuels sollicitent davantage l'organisme."),
            dict(icon="warn", title="Teint terne", text="Souvent associé, à tort ou à raison, à une période de mauvaise hygiène alimentaire prolongée."),
            dict(icon="warn", title="Sensibilité aux odeurs de graisse", text="Un signal fréquemment rapporté après une période d'alimentation déséquilibrée."),
        ],
        levers=[
            dict(icon="apple", title="Limiter le sucre et les graisses saturées", text="Privilégier les bonnes graisses (huile d'olive, oléagineux, poissons gras)."),
            dict(icon="drop", title="Bien s'hydrater", text="L'eau participe à l'élimination naturelle des déchets métaboliques par les reins."),
            dict(icon="leaf", title="Faire des pauses alimentaires", text="Laisser un temps de digestion suffisant entre les repas, éviter le grignotage permanent."),
            dict(icon="bolt", title="Bouger régulièrement", text="L'activité physique améliore la sensibilité à l'insuline et le métabolisme des graisses."),
        ],
        range_title="Health Mission — le soin du foie et du métabolisme",
        range_lede="Liver Support en produit phare, associé à l'Aloe Vera et aux fibres pour accompagner le métabolisme hépatique, intestinal et cellulaire.",
        products=[
            dict(
                tag="Foie & métabolisme", title="LR LIFETAKT Liver Support",
                desc="La formule phare de la gamme Health Mission, ciblée sur le soutien du métabolisme hépatique et cellulaire.",
                bullets=["Formule ciblée métabolisme hépatique et cellulaire", "À utiliser en cure ponctuelle", "En complément d'une hygiène de vie équilibrée"],
                href="https://shop.lrworld.com/product/fr/fr/lr_lifetakt_liver_support.html?productAlias=81330-99&casrnc=101e0f",
                swatch_color="linear-gradient(135deg,#5f7a5a,#3f5a3c)", icon_name="leaf",
            ),
            dict(
                tag="Best-seller", title="Aloe Vera Drinking Gel Pêche",
                desc="98% de gel de feuilles d'Aloe Vera à la saveur pêche, sans sucres ajoutés.",
                bullets=["Métabolisme énergétique, système nerveux & immunitaire", "98% de gel de feuilles d'Aloe Vera", "100% des AJR en vitamine C par ration"],
                href="https://shop.lrworld.com/product/fr/fr/lr_lifetakt_aloe_vera_drinking_gel_peche.html?productAlias=80750-684&casrnc=ac73c",
                swatch_color="linear-gradient(135deg,#c96f4a,#a8552f)", icon_name="drop",
                bestseller=True,
            ),
            dict(tag="Body Mission", title="Fiber Boost", desc="Un apport en fibres pour accompagner un transit et un confort digestif normal.", bullets=["Fibres végétales", "Se mélange facilement", "Usage quotidien"], href=SHOP, swatch_color="linear-gradient(135deg,#d9a441,#a8752c)", icon_name="loop"),
        ],
        testimonials=[
            (5, "J'ai arrêté de chercher une solution miracle et j'ai simplement revu mes repas du soir : la différence sur ma digestion a été nette en quelques semaines.", "Nathalie, 46 ans"),
            (4, "La cure d'Aloe Vera s'intègre bien dans ma routine du matin, en complément d'une alimentation plus légère.", "Thomas, 33 ans"),
        ],
        faq=[
            dict(q="Existe-t-il un produit qui \"nettoie\" le foie ?", a="Non, aucun produit ne remplace la fonction naturelle du foie. Certaines plantes sont traditionnellement associées au confort digestif, mais toujours en complément d'une hygiène de vie adaptée."),
            dict(q="Une cure détox est-elle utile après les fêtes ?", a="Reprendre une alimentation équilibrée, bien s'hydrater et bouger davantage est le geste le plus efficace. Une cure peut accompagner cette reprise, sans se substituer à elle."),
            dict(q="Quand faut-il consulter un médecin ?", a="En cas de douleurs, de jaunisse, de troubles digestifs sévères ou persistants, une consultation médicale est indispensable — ce site ne remplace pas un diagnostic."),
        ],
    ),
    dict(
        slug="digestion-microbiote.html",
        eyebrow="Pilier bien-être",
        title="Digestion & Microbiote",
        lede="Ballonnements, transit capricieux, inconforts après le repas : votre microbiote intestinal joue un rôle central, bien au-delà de la digestion. Voici comment en prendre soin simplement.",
        meta_desc="Comprendre le rôle du microbiote intestinal dans la digestion et l'équilibre général, et découvrir les leviers naturels et compléments associés.",
        intro_notice="Ce contenu est informatif et généraliste. En cas de troubles digestifs sévères, de douleurs abdominales importantes ou de symptômes persistants, consultez un professionnel de santé.",
        understand_title="Le microbiote, un écosystème à part entière",
        understand_lede="Des milliers de milliards de bactéries vivent dans votre intestin — et leur équilibre influence bien plus que votre digestion.",
        understand_body="""<p>Le microbiote intestinal participe à la digestion, à la synthèse de certaines vitamines, et communique en permanence avec le système immunitaire (près de 70% des cellules immunitaires se trouvent au niveau de l'intestin) ainsi qu'avec le cerveau via ce que l'on appelle l'axe intestin-cerveau. Un microbiote déséquilibré peut se traduire par des ballonnements, un transit irrégulier, ou une sensation de fatigue digestive.</p><p>Cet équilibre se façonne au quotidien : diversité alimentaire, fibres, hydratation, gestion du stress et qualité du sommeil influencent directement la composition de cette flore intestinale.</p>""",
        facts_title="4 repères à connaître",
        facts=[
            "L'intestin abrite environ 100 000 milliards de bactéries, autant que de cellules dans le corps humain.",
            "Les fibres alimentaires nourrissent les bonnes bactéries intestinales (effet prébiotique).",
            "Le stress chronique peut modifier la composition du microbiote et la sensibilité digestive.",
            "Une alimentation variée (30 végétaux différents par semaine, selon certaines études) favorise la diversité du microbiote.",
        ],
        signs=[
            dict(icon="warn", title="Ballonnements récurrents", text="Souvent liés à l'alimentation, au stress ou à un déséquilibre transitoire de la flore."),
            dict(icon="warn", title="Transit irrégulier", text="Alternance de constipation et de selles molles : un signal à ne pas ignorer s'il persiste."),
            dict(icon="warn", title="Inconfort après certains aliments", text="Peut traduire une sensibilité digestive à identifier avec un professionnel si besoin."),
            dict(icon="warn", title="Fatigue après les repas", text="Une digestion difficile mobilise beaucoup d'énergie et peut accentuer la fatigue postprandiale."),
        ],
        levers=[
            dict(icon="apple", title="Diversifier son alimentation", text="Varier fruits, légumes, légumineuses et céréales complètes nourrit un microbiote riche."),
            dict(icon="loop", title="Manger lentement", text="Une mastication soignée facilite tout le travail digestif en amont."),
            dict(icon="drop", title="S'hydrater suffisamment", text="L'eau facilite le transit et le travail des fibres alimentaires."),
            dict(icon="moon", title="Gérer son stress", text="La cohérence cardiaque ou la marche peuvent apaiser l'axe intestin-cerveau."),
        ],
        range_title="Health Mission — le confort digestif",
        range_lede="Pro 12+ et Colostrum en formules ciblées, associés aux fibres pour accompagner l'équilibre digestif au quotidien.",
        products=[
            dict(
                tag="Digestion", title="Capsules Pro 12+",
                desc="Complexe TRIPLEBIOTIC à double encapsulation : prébiotiques, bactéries et postbiotiques réunis.",
                bullets=["1 milliard de bactéries par gélule", "12 souches bactériennes différentes", "Double encapsulation brevetée"],
                href="https://shop.lrworld.com/product/fr/fr/capsules_pro_12_+.html?productAlias=81180-99&casrnc=634a2",
                swatch_color="linear-gradient(135deg,#5f7a5a,#3f5a3c)", icon_name="loop",
            ),
            dict(
                tag="Immunité & digestion", title="LR LIFETAKT Colostrum Liquid",
                desc="Un produit haut de gamme à base de colostrum de vaches européennes, dégraissé et décaséiné.",
                bullets=["Premier lait de vaches exclusivement européennes", "Sans antibiotiques ni stéroïdes anabolisants", "Fabriqué en Allemagne, procédé à froid doux"],
                href="https://shop.lrworld.com/product/fr/fr/lr_lifetakt_colostrum_liquid.html?productAlias=80361-404&casrnc=827ed",
                swatch_color="linear-gradient(135deg,#c96f4a,#a8552f)", icon_name="shield",
            ),
            dict(tag="Body Mission", title="Fiber Boost", desc="Un complément en fibres à associer à une hydratation suffisante.", bullets=["Fibres solubles et insolubles", "Se mélange facilement", "Usage quotidien"], href=SHOP, swatch_color="linear-gradient(135deg,#d9a441,#a8752c)", icon_name="apple"),
        ],
        testimonials=[
            (5, "En mangeant plus varié et en buvant davantage d'eau, mes ballonnements ont nettement diminué en quelques semaines.", "Laura, 39 ans"),
            (4, "Le complément en fibres m'aide vraiment, mais c'est surtout le fait de manger plus lentement qui a tout changé pour moi.", "Marc, 52 ans"),
        ],
        faq=[
            dict(q="Faut-il prendre des probiotiques en continu ?", a="En général, une cure de 4 semaines renouvelable est recommandée, en fonction de vos besoins — demandez conseil pour un accompagnement personnalisé."),
            dict(q="Les probiotiques traitent-ils le syndrome de l'intestin irritable ?", a="Non, ce site n'a pas vocation à traiter une pathologie. En cas de syndrome diagnostiqué ou de douleurs importantes, seul un médecin ou un gastro-entérologue peut vous accompagner."),
            dict(q="Quels aliments favorisent un bon microbiote ?", a="Les fibres (légumes, légumineuses, céréales complètes) et les aliments fermentés (yaourt, choucroute, kéfir) sont généralement recommandés dans le cadre d'une alimentation variée."),
        ],
    ),
    dict(
        slug="immunite.html",
        products_grid="grid-4",
        eyebrow="Pilier bien-être",
        title="Système immunitaire",
        lede="Changement de saison, fatigue qui traîne, petits maux à répétition : vos défenses naturelles se construisent chaque jour, bien avant l'hiver. Voici comment les soutenir intelligemment.",
        meta_desc="Comprendre le fonctionnement du système immunitaire, les facteurs qui l'affaiblissent, et les leviers naturels et compléments pour soutenir vos défenses naturelles.",
        intro_notice="Ce contenu est informatif et généraliste et ne constitue pas un avis médical. En cas d'infections répétées ou de fièvre, consultez un professionnel de santé.",
        understand_title="Une immunité qui se construit toute l'année",
        understand_lede="Le système immunitaire n'est pas un simple bouclier : c'est un réseau qui dépend directement de votre mode de vie.",
        understand_body="""<p>Le système immunitaire est étroitement lié au sommeil, à la nutrition, à l'activité physique et... à l'intestin, puisque près de 70% des cellules immunitaires y sont concentrées. Le stress chronique, le manque de sommeil et les carences en certains micronutriments (vitamine D, zinc, vitamine C) sont des facteurs qui peuvent fragiliser les défenses naturelles.</p><p>Plutôt que d'attendre les premiers symptômes de l'hiver, l'idée est d'adopter des habitudes qui soutiennent l'immunité tout au long de l'année, avec un renfort ciblé lors des périodes plus à risque (changement de saison, fatigue accumulée, reprise après une maladie).</p>""",
        facts_title="4 repères à connaître",
        facts=[
            "La vitamine D, produite par exposition au soleil, est souvent insuffisante en hiver sous nos latitudes.",
            "Le zinc contribue au fonctionnement normal du système immunitaire.",
            "Un sommeil insuffisant réduit l'efficacité de certaines cellules immunitaires.",
            "L'intestin joue un rôle central : prendre soin de son microbiote soutient aussi l'immunité.",
        ],
        signs=[
            dict(icon="warn", title="Infections à répétition", text="Rhumes ou petites infections qui reviennent souvent peuvent traduire des défenses affaiblies."),
            dict(icon="warn", title="Fatigue persistante", text="Une fatigue qui s'installe peut solliciter davantage l'organisme face aux agressions extérieures."),
            dict(icon="warn", title="Convalescence longue", text="Un temps de récupération plus long après une infection est un signal à ne pas négliger."),
            dict(icon="warn", title="Stress chronique", text="Le stress prolongé impacte directement la réponse immunitaire de l'organisme."),
        ],
        levers=[
            dict(icon="moon", title="Prioriser le sommeil", text="7 à 9 heures de sommeil de qualité soutiennent la régénération des défenses naturelles."),
            dict(icon="apple", title="Miser sur les couleurs", text="Fruits et légumes variés apportent vitamines, minéraux et antioxydants naturels."),
            dict(icon="bolt", title="Bouger modérément", text="Une activité physique régulière et modérée soutient l'immunité (l'excès inverse l'effet)."),
            dict(icon="loop", title="Chouchouter son intestin", text="Un microbiote équilibré est l'un des meilliers alliés de vos défenses naturelles."),
        ],
        range_title="Reishi, Pro 12+, Cistus Incanus & Colostrum — le soutien ciblé",
        range_lede="Quatre approches complémentaires pour accompagner vos défenses naturelles lors des périodes de fatigue saisonnière ou de sollicitation accrue.",
        products=[
            dict(
                tag="Cœur & vitalité", title="Reishi Plus en gélules",
                desc="Un champignon utilisé depuis des siècles dans la tradition asiatique, associé à la vitamine C.",
                bullets=["Contribue à un métabolisme énergétique normal", "Aide à réduire la fatigue et l'épuisement", "Végan, sans lactose — 30 gélules"],
                href="https://shop.lrworld.com/product/fr/fr/reishi_plus_en_gelules.html?productAlias=80331-799&casrnc=29c02",
                swatch_color="linear-gradient(135deg,#5f7a5a,#3f5a3c)", icon_name="leaf",
            ),
            dict(
                tag="Digestion & immunité", title="Capsules Pro 12+",
                desc="Complexe TRIPLEBIOTIC à double encapsulation : prébiotiques, bactéries et postbiotiques.",
                bullets=["1 milliard de bactéries par gélule", "12 souches bactériennes différentes", "Double encapsulation brevetée"],
                href="https://shop.lrworld.com/product/fr/fr/capsules_pro_12_+.html?productAlias=81180-99&casrnc=634a2",
                swatch_color="linear-gradient(135deg,#c96f4a,#a8552f)", icon_name="loop",
            ),
            dict(
                tag="Immunité", title="Cistus Incanus en gélules",
                desc="Extrait concentré de Cistus Incanus, associé au zinc et à la vitamine C.",
                bullets=["Extrait de Cistus Incanus à 72%", "100% des AJR en vitamine C, 20% en zinc", "Gélules à enveloppe végétale — 60 gélules"],
                href="https://shop.lrworld.com/product/fr/fr/cistus_incanus_en_gelules.html?productAlias=80325-699&casrnc=f06f7",
                swatch_color="linear-gradient(135deg,#d9a441,#a8752c)", icon_name="shield",
            ),
            dict(
                tag="Immunité & digestion", title="LR LIFETAKT Colostrum Liquid",
                desc="Un produit haut de gamme à base de colostrum de vaches européennes, dégraissé et décaséiné.",
                bullets=["Premier lait de vaches exclusivement européennes", "Sans antibiotiques ni stéroïdes anabolisants", "Fabriqué en Allemagne, procédé à froid doux"],
                href="https://shop.lrworld.com/product/fr/fr/lr_lifetakt_colostrum_liquid.html?productAlias=80361-404&casrnc=827ed",
                swatch_color="linear-gradient(135deg,#5f7a5a,#3f5a3c)", icon_name="shield",
            ),
        ],
        testimonials=[
            (5, "Depuis que je fais attention à mon sommeil et que j'ai ajouté une cure de vitamines à l'automne, je suis beaucoup moins souvent malade.", "Elodie, 44 ans"),
            (4, "Le combo alimentation variée + Oméga-3 s'intègre facilement dans ma routine, sans y penser.", "Pierre, 50 ans"),
        ],
        faq=[
            dict(q="Un complément peut-il empêcher de tomber malade ?", a="Non, aucun complément ne prévient une maladie. Certains nutriments contribuent au fonctionnement normal du système immunitaire dans le cadre d'une alimentation équilibrée et d'un mode de vie sain."),
            dict(q="Quand commencer une cure pour l'hiver ?", a="Beaucoup de personnes commencent en septembre-octobre pour anticiper la baisse de luminosité et le changement de rythme, mais cela dépend de votre situation."),
            dict(q="Les oméga-3 sont-ils adaptés à tout le monde ?", a="Ils sont généralement bien tolérés, mais demandez conseil à un professionnel de santé en cas de traitement anticoagulant ou de pathologie particulière."),
        ],
    ),
]

# --------------------------------------------------------------------------
# PAGE D'ACCUEIL
# --------------------------------------------------------------------------
def build_home():
    def needs_list(items):
        return "\n".join(
            '<li><a href="%s">%s %s</a></li>' % (href, label, icon("arrow"))
            for href, label in items
        )

    needs_card_bienetre = """<div class="needs-card" data-reveal>
  <div class="needs-media"><img src="assets/img/bienetre-duo.jpg" alt="Un couple en extérieur, tapis d'exercice sous le bras, prêt pour une activité physique douce" loading="lazy" width="1400" height="2100"></div>
  <div class="needs-body">
    <span class="needs-tag">Bien-être</span>
    <p class="needs-sub">Des solutions nutritionnelles pour accompagner votre quotidien.</p>
    <ul class="needs-list">
      %s
    </ul>
  </div>
</div>""" % needs_list([
        ("energie-vitalite.html", "Énergie"),
        ("recuperation-sommeil.html", "Récupération"),
        ("foie-detox.html", "Foie & détox cellulaire"),
        ("digestion-microbiote.html", "Digestion"),
        ("immunite.html", "Système immunitaire"),
    ])

    needs_card_nutrition = """<div class="needs-card" data-reveal>
  <div class="needs-media"><img src="assets/img/nutrition-mesure.jpg" alt="Des mains tenant un mètre-ruban de couturier, pour le suivi d'un objectif nutritionnel" loading="lazy" width="1400" height="2100"></div>
  <div class="needs-body">
    <span class="needs-tag needs-tag--nutrition">Nutrition</span>
    <p class="needs-sub">Des solutions adaptées à votre objectif et à votre alimentation.</p>
    <ul class="needs-list">
      %s
    </ul>
  </div>
</div>""" % needs_list([
        ("nutrition-objectifs.html#perte-de-poids", "Perte de poids"),
        ("nutrition-objectifs.html#reequilibrage-alimentaire", "Rééquilibrage alimentaire"),
        ("nutrition-objectifs.html#prise-de-masse", "Prise de masse"),
    ])

    steps = [
        ("01", "Je fais le point", "3 minutes de quiz pour identifier votre priorité bien-être du moment (énergie, sommeil, digestion, immunité, poids...)."),
        ("02", "Je reçois une orientation claire", "Des explications honnestes, sans jargon, et une gamme LR adaptée à votre objectif."),
        ("03", "Je commande en toute sécurité", "Sur ma boutique officielle LR, la seule plateforme autorisée pour les produits."),
    ]
    steps_html = "\n".join(
        """<div class="card" data-reveal>
      <div class="icon-badge gold" style="font-family:var(--font-display);font-size:1.3rem;align-items:center;justify-content:center;">%s</div>
      <h3>%s</h3><p>%s</p>
    </div>""" % s for s in steps
    )

    body = """
<section class="hero-photo-section">
  <div class="container">
    <div class="hero-photo" data-reveal>
      <div class="hero-photo-media">
        <img src="assets/img/hero-woman.jpg" alt="Portrait en extérieur d'une femme souriante, en lumière naturelle — l'énergie et le bien-être au quotidien" loading="eager" fetchpriority="high" width="2000" height="1333">
      </div>
      <span class="chip-float chip--tl">%s Accompagnement humain, sans pression</span>
      <span class="chip-float chip--br dark">%s %s, France</span>
      <div class="hero-photo-content">
        <div class="eyebrow">%s</div>
        <h1>%s</h1>
        <p class="lede">%s, %s. J'aide celles et ceux qui veulent comprendre <em>vraiment</em> leur corps — énergie, récupération, foie, intestin, immunité — avant de choisir un complément adapté à leur objectif.</p>
        <div class="hero-actions">
          %s
          %s
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="hero-stats-row" data-reveal>
      <div><strong>5</strong><span>piliers bien-être expliqués</span></div>
      <div><strong>100%%</strong><span>contenu sans allégation médicale</span></div>
      <div><strong>1</strong><span>boutique officielle, sûre &amp; garantie</span></div>
    </div>
    <div class="quiz-teaser-card" data-reveal>
      <div class="icon-badge">%s</div>
      <div>
        <h3>Quel est votre vrai besoin du moment ?</h3>
        <p>Énergie, sommeil, digestion, immunité, poids, prise de masse... En 3 minutes, identifiez la priorité qui changera vraiment votre quotidien.</p>
        %s
      </div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:20px;">
  <div class="container">
    %s
    <div class="needs-grid">
      %s
      %s
    </div>
  </div>
</section>

<section class="section section-sage">
  <div class="container">
    %s
    <div class="grid grid-3">
      %s
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="stats-band" data-reveal>
      <div>
        <div class="eyebrow">Comment ça s'articule</div>
        <h2>Un accompagnement <em>qui se construit</em>, pas qui s'improvise</h2>
        <p>Avant toute recommandation, ce site explore 5 dimensions de votre bien-être. Le quiz croise vos réponses avec ces piliers pour ne vous proposer que ce qui a du sens.</p>
        <div class="stats-figures">
          <div><strong>5</strong><span>piliers explorés</span></div>
          <div><strong>3 min</strong><span>quiz de diagnostic</span></div>
          <div><strong>0</strong><span>allégation médicale</span></div>
        </div>
        %s
      </div>
      <div class="stats-card">
        <div class="stats-card-head"><span>Répartition des piliers explorés</span><span>Aperçu</span></div>
        <div class="bar-chart">
          <div class="bar" style="--h:55%%"></div>
          <div class="bar" style="--h:70%%"></div>
          <div class="bar is-lime" style="--h:100%%"></div>
          <div class="bar" style="--h:62%%"></div>
          <div class="bar" style="--h:80%%"></div>
        </div>
        <div class="stats-specialist">
          <div class="avatar">%s</div>
          <div>
            <strong>%s</strong>
            <span>%s</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    %s
  </div>
</section>

<section class="section">
  <div class="container">
    %s
    <div class="grid grid-2">
      %s
      %s
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    %s
  </div>
</section>
""" % (
        icon("sparkle"),
        icon("pin"), CONFIG["city"],
        CONFIG["tagline"],
        word_reveal("Votre énergie, votre immunité, votre équilibre — <em>sans détour</em> marketing."),
        CONFIG["partner_name"], CONFIG["partner_title"],
        btn("Faire mon diagnostic gratuit", "quiz.html", variant="primary"),
        btn("Ma boutique LR officielle", SHOP, variant="ghost", blank=True),
        icon("sparkle"),
        btn("Commencer le quiz", "quiz.html", variant="dark", block=True),
        section_head("Votre point de départ", "Deux besoins, <em>une approche</em> personnalisée", "Quel que soit votre objectif, le quiz identifie en 3 minutes la priorité qui a vraiment du sens pour vous — voici les deux grandes familles de besoins que j'accompagne.", center=True),
        needs_card_bienetre, needs_card_nutrition,
        section_head("Comment ça marche", "De la question à la solution, en 3 étapes", "Pas de vente sous pression : un parcours pensé pour vous aider à choisir en connaissance de cause."),
        steps_html,
        btn("Faire le quiz gratuit", "quiz.html", variant="ghost"),
        initials(CONFIG["partner_name"]), CONFIG["partner_name"], CONFIG["partner_title"],
        promo_vip_band(),
        section_head("Ils ont trouvé leur équilibre", "Des parcours inspirants", "Témoignages personnels et non contractuels."),
        testimonial(5, "Le quiz m'a évité d'acheter au hasard : j'ai enfin compris pourquoi j'étais fatiguée et ce qui pouvait vraiment m'aider.", "Aline, 38 ans"),
        testimonial(5, "Un site clair, honnête, qui explique avant de vendre. Ça change des publicités habituelles sur les compléments.", "Yohann, 45 ans"),
        cta_band(
            "Prêt(e) à faire le point sur votre <em>bien-être</em> ?",
            "3 minutes suffisent pour une orientation personnalisée, sans engagement.",
            "quiz.html", "Faire le quiz gratuit",
            "contact.html", "Poser une question",
        ),
    )
    return page("index.html", "%s — %s" % (CONFIG["site_name"], CONFIG["tagline"]),
                "Site indépendant d'accompagnement bien-être : énergie, récupération, foie, digestion, immunité et nutrition sportive. Diagnostic gratuit et gammes LR Health & Beauty.",
                body, active="", extra_jsonld=ORG_JSONLD)

# --------------------------------------------------------------------------
# NUTRITION — PERTE DE POIDS & PRISE DE MASSE
# --------------------------------------------------------------------------
def build_nutrition():
    body = """
<section class="page-hero">
  <div class="container">
    %s
    <div class="eyebrow">Nutrition sportive</div>
    <h1 style="max-width:820px;">Nutrition, perte de poids & prise de masse</h1>
    <p class="lede" style="max-width:680px;">Que votre objectif soit d'affiner votre silhouette ou de prendre du muscle, la réussite tient d'abord à quelques principes simples de nutrition — les compléments viennent ensuite, en soutien.</p>
    <div class="pillar-nav">
      <a href="#perte-de-poids" class="pillar-chip">Perte de poids</a>
      <a href="#reequilibrage-alimentaire" class="pillar-chip">Rééquilibrage alimentaire</a>
      <a href="#prise-de-masse" class="pillar-chip">Prise de masse</a>
      <a href="#gamme-associee" class="pillar-chip">Gamme Body Mission</a>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    %s
  </div>
</section>

<section class="section" id="perte-de-poids">
  <div class="container">
    %s
    <div class="split">
      <div data-reveal>
        <p>Perdre du poids durablement repose sur un déficit calorique modéré et tenable dans le temps — pas sur une restriction extrême, souvent suivie d'un effet rebond. L'objectif est de préserver la masse musculaire pendant la perte de poids, ce qui suppose un apport suffisant en protéines et une activité physique régulière, y compris du renforcement musculaire.</p>
        <p>Les repas minceur (shakes, soupes, en-cas) peuvent être utiles pour structurer certains repas de la semaine, en particulier lorsque le temps manque, mais ne doivent pas remplacer une alimentation variée sur le long terme.</p>
      </div>
      <div class="split-visual" data-reveal>
        <h3 style="margin-bottom:18px;">Les 4 piliers d'une perte de poids durable</h3>
        %s
      </div>
    </div>
  </div>
</section>

<section class="section section-alt" id="reequilibrage-alimentaire">
  <div class="container">
    %s
    <div class="split">
      <div data-reveal>
        <p>Rééquilibrer son alimentation ne veut pas dire la restreindre : c'est retrouver une structure de repas régulière, variée et sans aliment interdit, adaptée à votre rythme de vie réel plutôt qu'à un modèle unique.</p>
        <p>C'est souvent l'étape la plus utile avant même de viser une perte de poids ou une prise de masse — et celle qui tient le mieux dans la durée, parce qu'elle ne repose pas sur la privation.</p>
      </div>
      <div class="split-visual" data-reveal>
        <h3 style="margin-bottom:18px;">Les repères d'un rééquilibrage durable</h3>
        %s
      </div>
    </div>
  </div>
</section>

<section class="section" id="prise-de-masse">
  <div class="container">
    %s
    <div class="split reverse">
      <div class="split-visual" data-reveal>
        <h3 style="margin-bottom:18px;">Les 4 piliers d'une prise de masse propre</h3>
        %s
      </div>
      <div data-reveal>
        <p>Prendre du muscle suppose un léger surplus calorique associé à un entraînement en résistance progressif et régulier. L'apport en protéines est déterminant : réparti sur la journée, il soutient la reconstruction musculaire après l'effort. La récupération (sommeil, hydratation) joue un rôle tout aussi important que l'entraînement lui-même.</p>
        <p>Les compléments protéinés peuvent aider à atteindre les apports quotidiens recommandés, notamment lorsque l'alimentation seule ne suffit pas à couvrir les besoins liés à l'entraînement.</p>
      </div>
    </div>
  </div>
</section>

<section class="section" id="gamme-associee">
  <div class="container">
    %s
    <div class="grid grid-3">
      %s
    </div>
    <p class="form-note" style="margin-top:20px;">%s</p>
  </div>
</section>

<section class="section section-sage">
  <div class="container" style="max-width:840px;">
    %s
    %s
  </div>
</section>

<section class="section-tight">
  <div class="container">
    %s
  </div>
</section>
""" % (
        breadcrumb("Nutrition sportive"),
        notice("Ce contenu est informatif et généraliste. Toute modification importante de votre alimentation, en particulier en cas de pathologie, de grossesse ou de traitement médical, doit être discutée avec un professionnel de santé ou un diététicien."),
        section_head("Objectif minceur", "Perdre du poids sans le reprendre", "La régularité prime toujours sur l'intensité : voici les fondamentaux qui font vraiment la différence."),
        check_list([
            "Un déficit calorique modéré (300 à 500 kcal/jour en moyenne)",
            "Un apport en protéines suffisant pour préserver le muscle",
            "Une activité physique régulière, cardio et renforcement",
            "Un sommeil de qualité, qui régule l'appétit et le stockage des graisses",
        ]),
        section_head("Objectif rééquilibrage", "Retrouver une alimentation stable", "Pas de liste d'aliments interdits : des repères simples à tenir sur la durée."),
        check_list([
            "Des repas structurés et réguliers, sans sauter de repas",
            "Une alimentation variée, sans groupe alimentaire exclu",
            "Des apports ajustés à votre activité réelle, pas à un modèle tout fait",
            "De la constance plutôt que des régimes ponctuels à répétition",
        ]),
        section_head("Objectif prise de masse", "Construire du muscle, proprement", "Pas de raccourci : progression, régularité et récupération sont vos meilleurs alliés."),
        check_list([
            "Un léger surplus calorique, ajusté selon vos résultats",
            "1,6 à 2 g de protéines par kg de poids de corps environ, à titre indicatif",
            "Un entraînement en résistance progressif (charges, répétitions)",
            "Un temps de récupération suffisant entre les séances",
        ]),
        section_head("La gamme Body Mission", "Des repas et compléments pensés pour votre objectif", "Shakes, soupes, en-cas et compléments protéinés — à intégrer dans une alimentation globale équilibrée."),
        "\n".join([
            product_card(tag="Body Mission", title="Shake Repas Minceur", desc="Un repas complet et équilibré pour remplacer occasionnellement un repas classique.", bullets=["Riche en protéines", "Plusieurs saveurs", "Pratique en déplacement"], href=SHOP, swatch_color="linear-gradient(135deg,#5f7a5a,#3f5a3c)", icon_name="apple"),
            product_card(tag="Body Mission", title="Protein Power", desc="Un concentré de protéines pour soutenir la construction et le maintien musculaire.", bullets=["Haute teneur en protéines", "Idéal post-entraînement", "Se prépare en 30 secondes"], href=SHOP, swatch_color="linear-gradient(135deg,#c96f4a,#a8552f)", icon_name="dumbbell"),
            product_card(tag="Body Mission", title="Pro Balance", desc="Un complexe pensé pour accompagner une période de rééquilibrage alimentaire.", bullets=["Vitamines & minéraux", "Complément du régime", "Format pratique"], href=SHOP, swatch_color="linear-gradient(135deg,#d9a441,#a8752c)", icon_name="sparkle"),
        ]),
        FOOD_SUPPLEMENT_DISCLAIMER,
        section_head("Questions fréquentes", "Vous vous demandez peut-être...", ""),
        "\n".join(
            '<details data-reveal style="background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px 24px;margin-bottom:14px;"><summary style="cursor:pointer;font-weight:600;font-family:var(--font-display);font-size:1.05rem;">%s</summary><p style="margin-top:12px;">%s</p></details>' % (q, a)
            for q, a in [
                ("Peut-on remplacer tous ses repas par des shakes ?", "Non, ce n'est pas recommandé sur la durée. Les repas minceur sont conçus comme un substitut occasionnel, dans le cadre d'un régime alimentaire varié et équilibré, pas comme une solution exclusive."),
                ("Faut-il des protéines en poudre pour prendre du muscle ?", "Non, ce n'est pas indispensable si l'alimentation couvre déjà vos besoins. C'est un outil pratique pour atteindre plus facilement vos apports quotidiens, en complément de l'entraînement."),
                ("Combien de temps pour voir des résultats ?", "Cela varie énormément selon les personnes, l'entraînement et la régularité. En général, des changements visibles s'observent sur plusieurs semaines à quelques mois, avec de la constance."),
            ]
        ),
        cta_band(
            "Un programme adapté à VOTRE objectif",
            "Perte de poids, prise de masse, ou simplement plus d'énergie au quotidien : faites le point en 3 minutes.",
            "quiz.html", "Faire le quiz gratuit",
            "contact.html", "Échanger avec moi",
        ),
    )
    return page("nutrition-objectifs.html", "Nutrition sportive : perte de poids & prise de masse — %s" % CONFIG["site_name"],
                "Conseils nutrition pour la perte de poids et la prise de masse musculaire, et découverte de la gamme Body Mission LR Health & Beauty.",
                body, active="nutrition-objectifs.html")

# --------------------------------------------------------------------------
# GAMMES LR
# --------------------------------------------------------------------------
RANGES = [
    dict(
        id="health-mission",
        icon="leaf",
        kind="Gamme principale",
        kind_type="principale",
        name="Health Mission",
        subtitle="Foie, digestion, détente & immunité — la gamme santé au quotidien",
        desc="Notre gamme la plus importante : elle agit sur le métabolisme hépatique, cellulaire et intestinal, au sein d'une alimentation variée. Disponible en abonnement sur ma boutique officielle LR, pour ne jamais être à court.",
        products=[
            dict(
                tag="Best-seller", title="Aloe Vera Drinking Gel Pêche",
                desc="Le best-seller LR à la saveur pêche : 98% de gel de feuilles d'Aloe Vera, sans sucres ajoutés.",
                bullets=[
                    "Contribue au métabolisme énergétique, système nerveux & immunitaire",
                    "98% de gel de feuilles d'Aloe Vera",
                    "100% des AJR en vitamine C par ration",
                    "Certifié SGS Institut Fresenius & IASC",
                ],
                href="https://shop.lrworld.com/product/fr/fr/lr_lifetakt_aloe_vera_drinking_gel_peche.html?productAlias=80750-684&casrnc=ac73c",
                icon_name="leaf",
                bestseller=True,
            ),
            dict(
                tag="Foie & métabolisme", title="LR LIFETAKT Liver Support",
                desc="Une formule ciblée pour accompagner le foie dans ses fonctions naturelles, notamment lors des périodes de sollicitation accrue.",
                bullets=[
                    "Formule ciblée métabolisme hépatique et cellulaire",
                    "À utiliser en cure ponctuelle",
                    "Produit phare de la gamme Health Mission",
                    "En complément d'une hygiène de vie équilibrée",
                ],
                href="https://shop.lrworld.com/product/fr/fr/lr_lifetakt_liver_support.html?productAlias=81330-99&casrnc=101e0f",
                icon_name="leaf",
            ),
            dict(
                tag="Digestion", title="Capsules Pro 12+",
                desc="Complexe TRIPLEBIOTIC à double encapsulation : prébiotiques, bactéries et postbiotiques réunis.",
                bullets=[
                    "1 milliard de bactéries par gélule",
                    "12 souches bactériennes différentes",
                    "Prébiotiques + bactéries + postbiotiques",
                    "Double encapsulation brevetée",
                ],
                href="https://shop.lrworld.com/product/fr/fr/capsules_pro_12_+.html?productAlias=81180-99&casrnc=634a2",
                icon_name="loop",
            ),
            dict(
                tag="Immunité & digestion", title="LR LIFETAKT Colostrum Liquid",
                desc="Un produit haut de gamme à base de colostrum de vaches européennes, dégraissé et décaséiné.",
                bullets=[
                    "Premier lait de vaches exclusivement européennes",
                    "Sans antibiotiques ni stéroïdes anabolisants",
                    "Sans colorants ni conservateurs",
                    "Fabriqué en Allemagne, procédé à froid doux",
                ],
                href="https://shop.lrworld.com/product/fr/fr/lr_lifetakt_colostrum_liquid.html?productAlias=80361-404&casrnc=827ed",
                icon_name="shield",
            ),
        ],
        products_grid="grid-2",
        link="foie-detox.html",
        link_label="Comprendre le pilier Foie & Détox cellulaire",
    ),
    dict(
        id="body-mission",
        icon="dumbbell",
        kind="Gamme principale",
        kind_type="principale",
        name="Body Mission",
        subtitle="Substituts et soutiens de repas pour la silhouette et le sport",
        desc="Une gamme complète de shakes (substituts de repas) et de compléments (soutiens de repas) pour accompagner un objectif minceur ou une prise de masse maîtrisée.",
        products=[
            dict(tag="Substitut de repas", title="Shake Repas Minceur", desc="Un repas équilibré et riche en protéines, pratique au quotidien.", bullets=["Plusieurs saveurs", "Riche en protéines", "Faible en sucres ajoutés"]),
            dict(
                tag="Soutien de repas", title="Protein Power Vanille",
                desc="80% de protéines précieuses issues de 5 sources différentes, au bon goût vanille.",
                bullets=[
                    "80% de protéines de 5 sources différentes",
                    "Contribue au maintien et au développement musculaire",
                    "Avec magnésium & vitamine B6",
                    "Idéal après l'effort",
                ],
                href="https://shop.lrworld.com/product/fr/fr/lr_lifetakt_boisson_en_poudre_protein_power_vanille.html?productAlias=80550-411",
                icon_name="dumbbell",
            ),
            dict(
                tag="Soutien de repas", title="Pro Balance en comprimés",
                desc="Un mélange harmonisé de minéraux et oligoéléments basiques pour l'équilibre intérieur.",
                bullets=[
                    "Citrates, carbonates & gluconates",
                    "Pensé pour l'équilibre acido-basique",
                    "Sans lactose",
                    "Format comprimés pratique",
                ],
                href="https://shop.lrworld.com/product/fr/fr/pro_balance_en_comprimes.html?productAlias=80102-404&casrnc=b7b82",
                icon_name="leaf",
            ),
            dict(tag="Digestif", title="Fiber Boost", desc="Un apport en fibres pour un confort digestif normal.", bullets=["Fibres solubles/insolubles", "Se mélange facilement", "Sans arôme artificiel"]),
        ],
        products_grid="grid-2",
        link="nutrition-objectifs.html",
        link_label="Voir le programme nutrition associé",
    ),
    dict(
        id="mind-master",
        icon="bolt",
        kind="Spécialiste LR — Performance, énergie et récup",
        name="Mind Master",
        subtitle="Énergie mentale, concentration & vigilance",
        desc="Une gamme pensée pour les journées denses : boissons Formula Red et Gold, stick Extreme à emporter, et un concentré multivitamine avec Vita Active.",
        products=[
            dict(
                tag="Mind Master Red", title="Mind Master Formula Red",
                desc="La variante rouge à la saveur fruitée de raisin, pour une vie active et énergique.",
                bullets=[
                    "Thiamine & B12 : métabolisme énergétique normal",
                    "B12 : bon fonctionnement du système nerveux et psychique",
                    "B12 & fer : réduisent la fatigue et l'épuisement",
                    "Vitamine E : protège les cellules du stress oxydant",
                ],
                href="https://shop.lrworld.com/product/fr/fr/lr_lifetakt_mind_master_formula_red.html?productAlias=80950-604&casrnc=cac57",
                image="assets/img/mind-master-red.jpg",
            ),
            dict(
                tag="Mind Master Gold", title="Mind Master Formula Gold",
                desc="Pour l'énergie, la performance et l'équilibre mental, quoi que le quotidien réserve.",
                bullets=[
                    "B12 : métabolisme énergétique normal, réduit la fatigue",
                    "Fer : fonction cognitive normale, transport de l'oxygène",
                    "Vitamine D : ossature et fonction musculaire normales",
                    "Vitamine E : protège les cellules du stress oxydatif",
                ],
                href="https://shop.lrworld.com/product/fr/fr/mind_master_formula_gold.html?productAlias=80940-4&casrnc=6ffb9",
                image="assets/img/mind-master-gold.jpg",
            ),
            dict(
                tag="Coup de fouet", title="Mind Master Extreme",
                desc="Le format stick à emporter partout, à consommer sans eau pour un coup de fouet rapide.",
                bullets=[
                    "Caféine du guarana : attention, concentration, endurance",
                    "B6, B12 & thiamine : soutiennent la fonction psychique",
                    "Vitamine C : fonctionnement normal du système immunitaire",
                    "100% des besoins journaliers en vitamines E et D",
                ],
                href="https://shop.lrworld.com/product/fr/fr/mind_master_extreme.html?productAlias=80980-398&casrnc=2ccd7",
                image="assets/img/mind-master-extreme.jpg",
            ),
            dict(
                tag="Multivitamines", title="Vita Active Fruits Rouges",
                desc="Un concentré de 21 fruits et légumes et 10 vitamines essentielles, une cuillère à café par jour.",
                bullets=[
                    "Vitamines D & B6 : bon fonctionnement du système immunitaire",
                    "Vitamine B12 : favorise la division cellulaire",
                    "Vitamine B1 : contribue à une fonction cardiaque normale",
                    "21 fruits et légumes concentrés, pour toute la famille",
                ],
                href="https://shop.lrworld.com/product/fr/fr/vita_active_fruits_rouges.html?productAlias=80301-699&casrnc=2009b",
                image="assets/img/vita-active.jpg",
            ),
            dict(
                tag="Oméga-3", title="Capsules Super Omega",
                desc="Des oméga-3 marins pour le bien-être cardiaque, issus de la pêche durable.",
                bullets=["Huile de poisson riche en oméga-3", "Contribue au bien-être cardiaque", "Certifié Friend of the Sea", "60 gélules"],
                href="https://shop.lrworld.com/product/fr/fr/capsules_super_omega.html?productAlias=80338-699&casrnc=333bd",
                icon_name="drop",
            ),
        ],
        products_grid="grid-3",
        link="energie-vitalite.html",
        link_label="Comprendre le pilier Énergie & Vitalité",
    ),
    dict(
        id="nutriments",
        icon="apple",
        kind="Spécialiste LR",
        name="Faire le plein de nutriments",
        subtitle="Le socle nutritionnel du quotidien",
        desc="Oméga-3, minéraux et Aloe Vera : les trois piliers pour ne manquer de rien, quel que soit votre rythme de vie.",
        products=[
            dict(
                tag="Oméga-3", title="Capsules Super Omega",
                desc="Des oméga-3 marins pour le bien-être cardiaque, issus de la pêche durable.",
                bullets=["Huile de poisson riche en oméga-3", "Contribue au bien-être cardiaque", "Certifié Friend of the Sea", "60 gélules"],
                href="https://shop.lrworld.com/product/fr/fr/capsules_super_omega.html?productAlias=80338-699&casrnc=333bd",
                icon_name="drop",
            ),
            dict(
                tag="Équilibre", title="Pro Balance en comprimés",
                desc="Un mélange harmonisé de minéraux et oligoéléments basiques pour l'équilibre intérieur.",
                bullets=["Citrates, carbonates & gluconates", "Équilibre acido-basique", "Sans lactose"],
                href="https://shop.lrworld.com/product/fr/fr/pro_balance_en_comprimes.html?productAlias=80102-404&casrnc=b7b82",
                icon_name="leaf",
            ),
            dict(
                tag="Best-seller", title="Aloe Vera Drinking Gel Pêche",
                desc="Le best-seller LR à la saveur pêche : 98% de gel de feuilles d'Aloe Vera, sans sucres ajoutés.",
                bullets=[
                    "Contribue au métabolisme énergétique, système nerveux & immunitaire",
                    "98% de gel de feuilles d'Aloe Vera",
                    "100% des AJR en vitamine C par ration",
                    "Certifié SGS Institut Fresenius & IASC",
                ],
                href="https://shop.lrworld.com/product/fr/fr/lr_lifetakt_aloe_vera_drinking_gel_peche.html?productAlias=80750-684&casrnc=ac73c",
                icon_name="leaf",
                bestseller=True,
            ),
            dict(
                tag="Multivitamines", title="Vita Active Fruits Rouges",
                desc="Un concentré de 21 fruits et légumes et 10 vitamines essentielles, une cuillère à café par jour.",
                bullets=[
                    "Vitamines D & B6 : bon fonctionnement du système immunitaire",
                    "Vitamine B12 : favorise la division cellulaire",
                    "21 fruits et légumes concentrés, pour toute la famille",
                ],
                href="https://shop.lrworld.com/product/fr/fr/vita_active_fruits_rouges.html?productAlias=80301-699&casrnc=2009b",
                image="assets/img/vita-active.jpg",
            ),
            dict(
                tag="Ortie & miel", title="Aloe Vera Drinking Gel Intense Sivera",
                desc="L'Aloe Vera allié à l'extrait d'ortie et au miel véritable, en pack de 3.",
                bullets=["Extrait d'ortie & miel véritable", "Pack de 3 flacons", "Issu de la recherche LR"],
                href="https://shop.lrworld.com/product/fr/fr/aloe_vera_drinking_gel_intense_sivera_en_pack_de_3.html?productAlias=80823-405&casrnc=eff14",
                icon_name="drop",
            ),
            dict(
                tag="Articulations", title="Aloe Vera Drinking Gel Active Freedom",
                desc="Au goût fruité d'orange, enrichi en vitamines C et E pour soutenir l'appareil locomoteur.",
                bullets=[
                    "Vitamine C : formation normale de collagène (os, cartilage)",
                    "Vitamine E : protection des cellules",
                    "Pack de 3 flacons",
                ],
                href="https://shop.lrworld.com/product/fr/fr/aloe_vera_drinking_gel_active_freedom_en_set_de_3.html?productAlias=80883-482&casrnc=9153c",
                icon_name="dumbbell",
            ),
        ],
        products_grid="grid-3",
        link="energie-vitalite.html",
        link_label="Voir le pilier Énergie & Vitalité",
    ),
    dict(
        id="coeur-circulation",
        icon="drop",
        kind="Spécialiste LR",
        name="Cœur et circulation",
        subtitle="Accompagner le bien-être cardiovasculaire",
        desc="Des extraits traditionnels et de l'Aloe Vera pour soutenir l'énergie et la vitalité liées à une bonne circulation.",
        products=[
            dict(
                tag="Cœur & vitalité", title="Reishi Plus en gélules",
                desc="Un champignon utilisé depuis des siècles dans la tradition asiatique, associé à la vitamine C.",
                bullets=[
                    "Contribue à un métabolisme énergétique normal",
                    "Aide à réduire la fatigue et l'épuisement",
                    "Extraits et poudre de Reishi + vitamine C",
                    "Végan, sans lactose — 30 gélules",
                ],
                href="https://shop.lrworld.com/product/fr/fr/reishi_plus_en_gelules.html?productAlias=80331-799&casrnc=29c02",
                icon_name="leaf",
            ),
            dict(
                tag="Aloe Vera", title="Aloe Vera Drinking Gel Intense Sivera",
                desc="L'Aloe Vera allié à l'extrait d'ortie et au miel véritable, en pack de 3.",
                bullets=["Extrait d'ortie & miel véritable", "Pack de 3 flacons", "Issu de la recherche LR"],
                href="https://shop.lrworld.com/product/fr/fr/aloe_vera_drinking_gel_intense_sivera_en_pack_de_3.html?productAlias=80823-405&casrnc=eff14",
                icon_name="drop",
            ),
            dict(
                tag="Oméga-3", title="Capsules Super Omega",
                desc="Des oméga-3 marins pour le bien-être cardiaque, issus de la pêche durable.",
                bullets=["Huile de poisson riche en oméga-3", "Contribue au bien-être cardiaque", "Certifié Friend of the Sea", "60 gélules"],
                href="https://shop.lrworld.com/product/fr/fr/capsules_super_omega.html?productAlias=80338-699&casrnc=333bd",
                icon_name="drop",
            ),
        ],
        products_grid="grid-3",
        link="quiz.html",
        link_label="Faire le quiz pour cibler vos besoins",
    ),
    dict(
        id="immunite-gamme",
        icon="shield",
        kind="Spécialiste LR",
        name="Système immunitaire et digestion",
        subtitle="Renforcer les défenses naturelles et le confort digestif",
        desc="Reishi, probiotiques, plantes, colostrum et minéraux : plusieurs approches complémentaires pour soutenir l'immunité et la digestion selon vos besoins.",
        products=[
            dict(
                tag="Digestion & immunité", title="Capsules Pro 12+",
                desc="Complexe TRIPLEBIOTIC à double encapsulation : prébiotiques, bactéries et postbiotiques.",
                bullets=["1 milliard de bactéries par gélule", "12 souches bactériennes différentes", "Double encapsulation brevetée"],
                href="https://shop.lrworld.com/product/fr/fr/capsules_pro_12_+.html?productAlias=81180-99&casrnc=634a2",
                icon_name="loop",
            ),
            dict(
                tag="Immunité", title="Cistus Incanus en gélules",
                desc="Extrait concentré de Cistus Incanus, associé au zinc et à la vitamine C.",
                bullets=[
                    "Extrait de Cistus Incanus à 72%",
                    "100% des AJR en vitamine C, 20% en zinc",
                    "Zinc & vitamine C : fonctionnement normal du système immunitaire",
                    "Gélules à enveloppe végétale — 60 gélules",
                ],
                href="https://shop.lrworld.com/product/fr/fr/cistus_incanus_en_gelules.html?productAlias=80325-699&casrnc=f06f7",
                icon_name="shield",
            ),
            dict(
                tag="Équilibre", title="Pro Balance en comprimés",
                desc="Un mélange harmonisé de minéraux et oligoéléments basiques pour l'équilibre intérieur.",
                bullets=["Citrates, carbonates & gluconates", "Équilibre acido-basique", "Sans lactose"],
                href="https://shop.lrworld.com/product/fr/fr/pro_balance_en_comprimes.html?productAlias=80102-404&casrnc=b7b82",
                icon_name="leaf",
            ),
            dict(
                tag="Immunité & digestion", title="LR LIFETAKT Colostrum Liquid",
                desc="Un produit haut de gamme à base de colostrum de vaches européennes.",
                bullets=["Premier lait de vaches européennes", "Sans antibiotiques ni stéroïdes anabolisants", "Fabriqué en Allemagne, à froid"],
                href="https://shop.lrworld.com/product/fr/fr/lr_lifetakt_colostrum_liquid.html?productAlias=80361-404&casrnc=827ed",
                icon_name="shield",
            ),
            dict(
                tag="Cœur & vitalité", title="Reishi Plus en gélules",
                desc="Un champignon utilisé depuis des siècles dans la tradition asiatique, associé à la vitamine C.",
                bullets=[
                    "Contribue à un métabolisme énergétique normal",
                    "Aide à réduire la fatigue et l'épuisement",
                    "Extraits et poudre de Reishi + vitamine C",
                ],
                href="https://shop.lrworld.com/product/fr/fr/reishi_plus_en_gelules.html?productAlias=80331-799&casrnc=29c02",
                icon_name="leaf",
            ),
        ],
        products_grid="grid-3",
        link="immunite.html",
        link_label="Comprendre le pilier Système immunitaire",
    ),
    dict(
        id="os-articulations-muscles",
        icon="dumbbell",
        kind="Spécialiste LR",
        name="Os, articulations et muscles",
        subtitle="Soutenir l'appareil locomoteur",
        desc="Vitamines, minéraux et protéines pour accompagner une activité physique régulière et le bon fonctionnement de l'appareil locomoteur.",
        products=[
            dict(
                tag="Articulations", title="Aloe Vera Drinking Gel Active Freedom",
                desc="Au goût fruité d'orange, enrichi en vitamines C et E pour soutenir l'appareil locomoteur.",
                bullets=[
                    "Vitamine C : formation normale de collagène (os, cartilage)",
                    "Vitamine E : protection des cellules",
                    "Complexe actif pensé pour les articulations",
                    "Pack de 3 flacons",
                ],
                href="https://shop.lrworld.com/product/fr/fr/aloe_vera_drinking_gel_active_freedom_en_set_de_3.html?productAlias=80883-482&casrnc=9153c",
                icon_name="dumbbell",
            ),
            dict(
                tag="Soutien de repas", title="Protein Power Vanille",
                desc="80% de protéines précieuses issues de 5 sources différentes.",
                bullets=["Contribue au maintien et au développement musculaire", "Avec magnésium & vitamine B6", "Idéal après l'effort"],
                href="https://shop.lrworld.com/product/fr/fr/lr_lifetakt_boisson_en_poudre_protein_power_vanille.html?productAlias=80550-411",
                icon_name="dumbbell",
            ),
            dict(
                tag="Équilibre", title="Pro Balance en comprimés",
                desc="Minéraux et oligoéléments basiques harmonisés pour l'équilibre intérieur.",
                bullets=["Citrates, carbonates & gluconates", "Sans lactose"],
                href="https://shop.lrworld.com/product/fr/fr/pro_balance_en_comprimes.html?productAlias=80102-404&casrnc=b7b82",
                icon_name="leaf",
            ),
        ],
        products_grid="grid-3",
        link="nutrition-objectifs.html",
        link_label="Voir le programme nutrition sportive",
    ),
    dict(
        id="equilibre-hormonal",
        icon="loop",
        kind="Spécialiste LR",
        name="Équilibre hormonal",
        subtitle="Le bien-être féminin, notamment à la ménopause",
        desc="Une formule dédiée pour accompagner les femmes à chaque étape, avec un focus sur la santé osseuse autour de la ménopause.",
        products=[
            dict(
                tag="Équilibre hormonal", title="Woman Phyto en gélules",
                desc="Pensé pour le bien-être féminin général, notamment autour de la ménopause.",
                bullets=[
                    "Calcium : maintien d'une ossature normale",
                    "Vitamine D : conservation des os normaux",
                    "Formule phyto dédiée au bien-être féminin",
                ],
                href="https://shop.lrworld.com/product/fr/fr/woman_phyto_en_gelules.html?productAlias=80332-799&casrnc=10b99c",
                icon_name="loop",
            ),
        ],
        products_grid="grid-2",
        link="quiz.html",
        link_label="Faire le quiz pour cibler vos besoins",
    ),
    dict(
        id="beaute",
        icon="sparkle",
        kind="Spécialiste LR",
        name="La beauté vient de l'intérieur",
        subtitle="Un rituel quotidien, décliné au féminin et au masculin",
        desc="Deux shots quotidiens pensés différemment selon vos besoins : éclat et vitalité pour elle, force et énergie pour lui.",
        products=[
            dict(
                tag="Beauté — Femme", title="Beauty Elixir 5en1",
                desc="Un shot quotidien pensé pour révéler éclat, vitalité et confiance en soi.",
                bullets=[
                    "Gel d'Aloe Vera & collagène hydrolysé",
                    "Vitamines C, E, A et du groupe B",
                    "Zinc, cuivre & acide hyaluronique",
                    "Un rituel quotidien pour la peau",
                ],
                href="https://shop.lrworld.com/cms/FR/fr/bien-%C3%AAtre/sp%C3%A9cialistes/la_beaut%C3%A9_vient_de_l%27int%C3%A9rieur/la_beaut%C3%A9_vient_de_l%27int%C3%A9rieur.html?casrnc=87a50",
                icon_name="sparkle",
                swatch_color="linear-gradient(135deg,#e08bab,#a84e6c)",
            ),
            dict(
                tag="Beauté — Homme", title="5in1 Men's Shot",
                desc="Un shot quotidien pensé pour la force, l'énergie et le charisme au masculin.",
                bullets=[
                    "Gel d'Aloe Vera, collagène & extrait de ginseng",
                    "Acides aminés : leucine, valine, isoleucine",
                    "Vitamines C, E, D et zinc",
                    "Un rituel quotidien, un seul shot",
                ],
                href="https://shop.lrworld.com/cms/FR/fr/bien-%C3%AAtre/sp%C3%A9cialistes/la_beaut%C3%A9_vient_de_l%27int%C3%A9rieur/la_beaut%C3%A9_vient_de_l%27int%C3%A9rieur.html?casrnc=87a50",
                icon_name="shield",
                swatch_color="linear-gradient(135deg,#4a4a4a,#161616)",
            ),
        ],
        products_grid="grid-2",
        link="quiz.html",
        link_label="Faire le quiz pour cibler vos besoins",
    ),
    dict(
        id="aloe-vera",
        icon="leaf",
        kind="Spécialiste LR",
        name="LR Aloe Vera",
        subtitle="Best-seller historique : plus de 60 millions de bouteilles vendues",
        desc="Le produit fondateur de LR Health & Beauty : de l'Aloe Vera issu de culture contrôlée, décliné en plusieurs rituels bien-être.",
        products=[
            dict(
                tag="Best-seller", title="Aloe Vera Drinking Gel Pêche",
                desc="98% de gel de feuilles d'Aloe Vera à la saveur pêche, sans sucres ajoutés.",
                bullets=[
                    "Contribue au métabolisme énergétique, système nerveux & immunitaire",
                    "98% de gel de feuilles d'Aloe Vera",
                    "100% des AJR en vitamine C par ration",
                    "Certifié SGS Institut Fresenius & IASC",
                ],
                href="https://shop.lrworld.com/product/fr/fr/lr_lifetakt_aloe_vera_drinking_gel_peche.html?productAlias=80750-684&casrnc=ac73c",
                bestseller=True,
            ),
            dict(
                tag="Ortie & miel", title="Aloe Vera Drinking Gel Intense Sivera",
                desc="L'Aloe Vera allié à l'extrait d'ortie et au miel véritable, en pack de 3.",
                bullets=["Extrait d'ortie & miel véritable", "Pack de 3 flacons"],
                href="https://shop.lrworld.com/product/fr/fr/aloe_vera_drinking_gel_intense_sivera_en_pack_de_3.html?productAlias=80823-405&casrnc=eff14",
            ),
            dict(
                tag="Articulations", title="Aloe Vera Drinking Gel Active Freedom",
                desc="Au goût fruité d'orange, enrichi en vitamines C et E pour l'appareil locomoteur.",
                bullets=["Vitamine C : formation normale de collagène", "Pack de 3 flacons"],
                href="https://shop.lrworld.com/product/fr/fr/aloe_vera_drinking_gel_active_freedom_en_set_de_3.html?productAlias=80883-482&casrnc=9153c",
                icon_name="dumbbell",
            ),
        ],
        products_grid="grid-3",
        link="foie-detox.html",
        link_label="Comprendre le pilier Foie & Détox cellulaire",
    ),
]

SWATCHES = [
    "linear-gradient(135deg,#5f7a5a,#3f5a3c)",
    "linear-gradient(135deg,#c96f4a,#a8552f)",
    "linear-gradient(135deg,#d9a441,#a8752c)",
]


def build_gammes():
    range_blocks = []
    for r in RANGES:
        is_principale = r.get("kind_type") == "principale"
        cards = "\n".join(
            product_card(tag=p["tag"], title=p["title"], desc=p["desc"], bullets=p["bullets"], href=p.get("href", SHOP),
                         swatch_color=p.get("swatch_color", SWATCHES[i % len(SWATCHES)]), icon_name=p.get("icon_name", r["icon"]),
                         bestseller=p.get("bestseller", False), image=p.get("image"))
            for i, p in enumerate(r["products"])
        )
        info_col = """
        <div class="icon-badge%s">%s</div>
        <span class="kind-badge %s">%s</span>
        <h2>%s</h2>
        <p class="lede">%s</p>
        <p>%s</p>
        <a class="card-link" href="%s">%s %s</a>""" % (
            " on-dark" if is_principale else "", icon(r["icon"]),
            "principale" if is_principale else "specialiste", r.get("kind", "Spécialiste LR"),
            r["name"], r["subtitle"], r["desc"],
            r["link"], r["link_label"], icon("arrow"),
        )
        cards_col = '<div class="grid %s">%s</div>' % (r.get("products_grid", "grid-2"), cards)

        if is_principale:
            range_blocks.append("""
<section class="section" id="%s">
  <div class="container">
    <div class="mega-band">
      <div class="split" style="align-items:flex-start;">
        <div data-reveal>%s</div>
        <div data-reveal>%s</div>
      </div>
    </div>
  </div>
</section>""" % (r["id"], info_col, cards_col))
        else:
            range_blocks.append("""
<section class="section%s" id="%s">
  <div class="container">
    <div class="split" style="align-items:flex-start;">
      <div data-reveal>%s</div>
      <div data-reveal>%s</div>
    </div>
  </div>
</section>""" % (" section-alt" if RANGES.index(r) % 2 else "", r["id"], info_col, cards_col))

    intro = """
<section class="page-hero">
  <div class="container">
    %s
    <div class="eyebrow">Catalogue</div>
    <h1 style="max-width:820px;">Les gammes LR Health & Beauty</h1>
    <p class="lede" style="max-width:680px;">Une sélection pensée par objectif plutôt qu'un catalogue interminable. Chaque gamme est reliée au pilier bien-être qu'elle accompagne, pour choisir en toute logique.</p>
    <div class="pillar-nav">
      %s
    </div>
    %s
  </div>
</section>""" % (
        breadcrumb("Gammes LR"),
        "\n".join('<a href="#%s" class="pillar-chip">%s</a>' % (r["id"], r["name"]) for r in RANGES),
        notice("Toutes les commandes se font exclusivement sur ma boutique en ligne officielle LR — la seule plateforme autorisée pour la vente des produits LR Health & Beauty. Ce site ne traite aucun paiement.", ic="cart"),
    )

    tones_cycle = ["", "terracotta", "gold"]
    overview_cards = "\n".join(
        pillar_teaser_card(
            "#%s" % r["id"], r["name"], r["icon"], r["subtitle"],
            tone=tones_cycle[i % len(tones_cycle)],
            kicker=r.get("kind", "Spécialiste LR"),
        )
        for i, r in enumerate(RANGES)
    )
    overview_section = """
<section class="section-tight">
  <div class="container">
    %s
    <div class="grid grid-5">
      %s
    </div>
  </div>
</section>""" % (
        section_head("Vue d'ensemble", "Toutes les gammes, <em>en un coup d'œil</em>", "Cliquez sur une carte pour aller directement à la gamme qui vous intéresse."),
        overview_cards,
    )

    promo_section = """
<section class="section-tight">
  <div class="container">
    %s
  </div>
</section>""" % promo_vip_band()

    outro = """
<section class="section-tight">
  <div class="container">
    %s
  </div>
</section>""" % cta_band(
        "Un doute sur le produit qui vous correspond ?",
        "Le quiz bien-être vous oriente en 3 minutes vers la gamme la plus adaptée à votre objectif.",
        "quiz.html", "Faire le quiz gratuit",
        SHOP, "Accéder à ma boutique LR", secondary_blank=True,
    )

    body = intro + overview_section + promo_section + "".join(range_blocks) + outro
    return page("gammes-lr.html", "Gammes LR Health & Beauty : Body Mission, Health Mission, Mind Master... — %s" % CONFIG["site_name"],
                "Découvrez les gammes LR Health & Beauty (Body Mission, Health Mission, Mind Master, Super Omega, Aloe Vera) classées par objectif bien-être, avec accès direct à la boutique officielle.",
                body, active="gammes-lr.html")


# --------------------------------------------------------------------------
# QUIZ
# --------------------------------------------------------------------------
def build_quiz():
    q1_opts = [
        ("energie", "Retrouver de l'énergie au quotidien"),
        ("recuperation", "Mieux récupérer & dormir"),
        ("foie", "Alléger mon foie & ma digestion"),
        ("digestion", "Soulager ballonnements & confort intestinal"),
        ("immunite", "Renforcer mes défenses naturelles"),
        ("poids", "Perdre du poids"),
        ("masse", "Prendre du muscle"),
    ]
    q1_html = "\n".join('<button type="button" class="quiz-option" data-value="%s">%s %s</button>' % (v, l, icon("chevron")) for v, l in q1_opts)

    q2_opts = [("recent", "Quelques semaines"), ("moyen", "Plusieurs mois"), ("chronique", "Toute l'année, de façon récurrente")]
    q2_html = "\n".join('<button type="button" class="quiz-option" data-value="%s">%s %s</button>' % (v, l, icon("chevron")) for v, l in q2_opts)

    q3_opts = [("rien", "Rien de particulier encore"), ("alimentation", "J'ai déjà ajusté mon alimentation"), ("complements", "J'ai testé des compléments sans grand résultat"), ("pro", "Je suis déjà suivi(e) par un professionnel")]
    q3_html = "\n".join('<button type="button" class="quiz-option" data-value="%s">%s %s</button>' % (v, l, icon("chevron")) for v, l in q3_opts)

    body = """
<section class="page-hero">
  <div class="container">
    %s
    <div class="eyebrow center" style="justify-content:center;display:flex;">Diagnostic bien-être</div>
    <h1 class="center" style="max-width:720px;">Quel accompagnement vous correspond&nbsp;?</h1>
    <p class="lede center" style="max-width:600px;">3 questions, 2 minutes, une orientation claire — sans obligation d'achat.</p>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <div class="quiz-shell" data-quiz>
      <div class="quiz-progress"><div class="quiz-progress-bar"></div></div>

      <div class="quiz-step active" data-question="objectif">
        <h3>Quel est votre objectif principal en ce moment&nbsp;?</h3>
        <div class="quiz-options">%s</div>
      </div>

      <div class="quiz-step" data-question="duree">
        <h3>Depuis combien de temps ressentez-vous ce besoin&nbsp;?</h3>
        <div class="quiz-options">%s</div>
        <div class="quiz-nav"><button type="button" class="btn btn-outline btn-sm" data-quiz-back>%s Précédent</button></div>
      </div>

      <div class="quiz-step" data-question="essais">
        <h3>Qu'avez-vous déjà essayé&nbsp;?</h3>
        <div class="quiz-options">%s</div>
        <div class="quiz-nav"><button type="button" class="btn btn-outline btn-sm" data-quiz-back>%s Précédent</button></div>
      </div>

      <div class="quiz-result">
        <span class="result-badge" data-result-badge></span>
        <h3>Votre orientation personnalisée</h3>
        <p data-result-text></p>
        <div style="display:flex;gap:14px;flex-wrap:wrap;margin-top:22px;">
          <a class="btn btn-primary" data-result-pillar href="#"></a>
          <a class="btn btn-outline" data-result-range href="#" target="_blank" rel="noopener sponsored"></a>
        </div>
        <div style="margin-top:34px;border-top:1px solid var(--line);padding-top:28px;">
          <h3 style="font-size:1.1rem;">Recevoir mes conseils personnalisés par email</h3>
          <form data-form name="quiz" method="POST" data-netlify="true" data-netlify-honeypot="bot-field" action="/merci.html">
            <input type="hidden" name="form-name" value="quiz">
            <p hidden><label>Ne pas remplir : <input name="bot-field"></label></p>
            <div class="grid grid-2">
              <div class="field"><label for="qz-name">Prénom</label><input id="qz-name" name="prenom" type="text" required></div>
              <div class="field"><label for="qz-email">Email</label><input id="qz-email" name="email" type="email" required></div>
            </div>
            <input type="hidden" name="source" value="quiz-vitalis">
            <button class="btn btn-dark btn-block" type="submit">Recevoir mes conseils gratuits</button>
            <p class="form-note" data-form-note style="margin-top:10px;">Vos données ne sont utilisées que pour vous répondre. Voir notre politique de confidentialité.</p>
          </form>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container" style="max-width:760px;">
    %s
  </div>
</section>
""" % (
        breadcrumb("Quiz bien-être"),
        q1_html, q2_html, icon("arrow"), q3_html, icon("arrow"),
        notice("Ce quiz est un outil d'orientation générale et non un test médical ou diagnostique. Il ne remplace en aucun cas l'avis d'un professionnel de santé.", ic="info"),
    )
    return page("quiz.html", "Quiz bien-être gratuit : quel accompagnement vous correspond ? — %s" % CONFIG["site_name"],
                "Faites le point en 3 minutes sur votre priorité bien-être (énergie, sommeil, digestion, immunité, poids) et recevez une orientation personnalisée.",
                body, active="quiz.html", extra_scripts='<script src="assets/js/quiz.js"></script>')

# --------------------------------------------------------------------------
# À PROPOS
# --------------------------------------------------------------------------
def build_apropos():
    ranges_teaser = [
        ("Body Mission", "Silhouette & nutrition sportive", "leaf", "gammes-lr.html#body-mission", ""),
        ("Health Mission", "Digestion, détente & vitalité", "shield", "gammes-lr.html#health-mission", "terracotta"),
        ("Mind Master", "Énergie mentale & concentration", "bolt", "gammes-lr.html#mind-master", "gold"),
        ("Aloe Vera", "Le rituel bien-être quotidien", "drop", "gammes-lr.html#aloe-vera", ""),
    ]
    ranges_html = "\n".join(
        pillar_teaser_card(href, name, ic, desc, tone=tone, kicker="Gamme LR")
        for name, desc, ic, href, tone in ranges_teaser
    )

    feature_accordion = """<div class="feature-accordion" data-reveal>
  <details open>
    <summary>Transparence totale %s</summary>
    <div class="panel"><ul>
      <li>%sSite personnel et indépendant, clairement identifié comme tel</li>
      <li>%sAucune vente ni paiement traité sur ce site</li>
      <li>%sChaque lien produit renvoie vers ma boutique officielle LR</li>
    </ul></div>
  </details>
  <details>
    <summary>Conformité stricte %s</summary>
    <div class="panel"><ul>
      <li>%sAucune allégation de traitement ou de guérison</li>
      <li>%sMentions obligatoires rappelées sur chaque page</li>
      <li>%sTémoignages présentés comme non contractuels</li>
    </ul></div>
  </details>
  <details>
    <summary>Accompagnement humain %s</summary>
    <div class="panel"><ul>
      <li>%sUn quiz pour clarifier votre besoin réel, sans pression</li>
      <li>%sDes réponses possibles par email ou téléphone</li>
      <li>%sAucune obligation d'achat, à aucun moment</li>
    </ul></div>
  </details>
</div>""" % (
        icon("chevron", "chev"), icon("check"), icon("check"), icon("check"),
        icon("chevron", "chev"), icon("check"), icon("check"), icon("check"),
        icon("chevron", "chev"), icon("check"), icon("check"), icon("check"),
    )

    body = """
<section class="page-hero">
  <div class="container">
    %s
    <div class="eyebrow">À propos</div>
    <h1 style="max-width:760px;">Bonjour, je suis %s</h1>
    <p class="lede" style="max-width:640px;">%s, basé à %s. Les produits LR ne sont pas une découverte récente pour moi : je les connais depuis plus de 20 ans et je les utilise depuis toujours, bien avant de devenir partenaire. Le bien-être n'est pas un sujet que j'ai découvert un jour — c'est une valeur transmise par ma famille, pour qui il a toujours été une priorité.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split">
      <div class="split-visual" data-reveal>
        <div class="icon-badge">%s</div>
        <h3>Mon parcours</h3>
        <p>Je suis issu d'une famille pour qui le bien-être a toujours été une priorité : j'ai grandi avec ces produits au quotidien, bien avant de penser à en faire mon activité. Devenir partenaire indépendant a été la suite logique d'une conviction déjà ancrée depuis longtemps. Depuis, j'ai accompagné des dizaines de clients dans un changement durable de leurs habitudes de vie, toujours avec la même approche : comprendre avant de recommander.</p>
      </div>
      <div data-reveal>
        <div class="eyebrow">Ma philosophie</div>
        <h2>De l'information avant la vente</h2>
        <p>Je crois qu'un bon accompagnement commence par comprendre son propre corps — pas par acheter le premier produit venu. C'est pour ça que ce site prend le temps d'expliquer l'énergie, le sommeil, la digestion, l'immunité et la nutrition sportive, avant même de parler produits.</p>
        %s
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="split">
      <div data-reveal>
        <div class="eyebrow">Pourquoi ce site</div>
        <h2>Transformer une visite en <em>vraie clarté</em> — pas en pression commerciale</h2>
        <p>Trop de sites autour des compléments alimentaires promettent des miracles. Ici, l'objectif est inverse : vous donner une information honnête sur votre corps, pour que le produit vienne en toute logique — jamais comme un argument de vente isolé.</p>
        %s
      </div>
      <div style="position:relative;" data-reveal>
        <div class="photo-block ratio-tall tone-sage-light">%s</div>
        <span class="chip-float chip--tl">%s Contenu vérifié</span>
        <span class="chip-float chip--br dark">%s 0 allégation abusive</span>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    %s
    <div class="grid grid-3">
      <div class="card" data-reveal><div class="icon-badge">%s</div><h3>Statut transparent</h3><p>%s</p></div>
      <div class="card" data-reveal><div class="icon-badge terra">%s</div><h3>Zéro allégation abusive</h3><p>Aucun produit n'est présenté comme un traitement médical. L'information prime sur la promesse.</p></div>
      <div class="card" data-reveal><div class="icon-badge gold">%s</div><h3>Une seule boutique</h3><p>Toutes les commandes passent exclusivement par ma boutique officielle LR, sécurisée et garantie.</p></div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container">
    <div class="mega-band">
      <div class="section-head-row">
        <div class="section-head">
          <div class="eyebrow">Les gammes LR</div>
          <h2>Des produits pensés pour <em>chaque objectif</em></h2>
          <p class="lede" style="color:rgba(255,255,255,.75);">Body Mission, Health Mission, Mind Master, Aloe Vera... découvrez les gammes les plus adaptées à vos priorités du moment.</p>
        </div>
        %s
      </div>
      <div class="grid grid-4">
        %s
      </div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    %s
  </div>
</section>
""" % (
        breadcrumb("À propos"),
        CONFIG["partner_name"], CONFIG["partner_title"], CONFIG["city"],
        icon("sparkle"),
        check_list(["Contenu rédigé avec honnêteté, sans exagération", "Une approche par objectif, pas par catalogue", "Un accompagnement humain si vous le souhaitez"]),
        feature_accordion,
        icon("shield"),
        icon("sparkle"),
        icon("check"),
        section_head("Mes engagements", "Ce que vous pouvez attendre de moi", ""),
        icon("shield"),
        "Ce site est un espace personnel indépendant. LR Health & Beauty Systems GmbH n'édite ni ne contrôle son contenu éditorial.",
        icon("info"),
        icon("cart"),
        btn("Voir toutes les gammes", "gammes-lr.html", variant="white"),
        ranges_html,
        cta_band(
            "Une question avant de vous lancer ?",
            "Je suis disponible pour échanger sur votre situation, sans pression commerciale.",
            "contact.html", "Me contacter",
            "quiz.html", "Faire le quiz",
        ),
    )
    return page("a-propos.html", "À propos — %s" % CONFIG["site_name"],
                "Découvrez le parcours et la philosophie derrière %s, site d'accompagnement bien-être et partenaire indépendant LR Health & Beauty." % CONFIG["site_name"],
                body, active="a-propos.html")


# --------------------------------------------------------------------------
# CONTACT
# --------------------------------------------------------------------------
def build_contact():
    body = """
<section class="page-hero">
  <div class="container">
    %s
    <div class="eyebrow">Contact</div>
    <h1 style="max-width:700px;">Parlons de votre objectif bien-être</h1>
    <p class="lede" style="max-width:600px;">Une question sur un produit, besoin d'un conseil personnalisé, ou simplement envie d'échanger ? Écrivez-moi.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="split">
      <div data-reveal>
        <form data-form name="contact" method="POST" data-netlify="true" data-netlify-honeypot="bot-field" action="/merci.html" class="card">
          <input type="hidden" name="form-name" value="contact">
          <p hidden><label>Ne pas remplir : <input name="bot-field"></label></p>
          <div class="field"><label for="c-name">Nom & prénom</label><input id="c-name" name="nom" type="text" required></div>
          <div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" required></div>
          <div class="field"><label for="c-topic">Votre priorité du moment</label>
            <select id="c-topic" name="sujet">
              <option>Énergie & vitalité</option>
              <option>Récupération & sommeil</option>
              <option>Foie & détox cellulaire</option>
              <option>Digestion & microbiote</option>
              <option>Système immunitaire</option>
              <option>Nutrition sportive (poids / masse)</option>
              <option>Autre question</option>
            </select>
          </div>
          <div class="field"><label for="c-msg">Votre message</label><textarea id="c-msg" name="message" rows="5" required></textarea></div>
          <label style="display:flex;gap:10px;align-items:flex-start;font-size:.85rem;color:var(--ink-soft);margin-bottom:18px;">
            <input type="checkbox" required style="margin-top:4px;">
            <span>J'accepte que mes informations soient utilisées pour me recontacter, conformément à la <a href="confidentialite-cookies.html" style="text-decoration:underline;">politique de confidentialité</a>.</span>
          </label>
          <button class="btn btn-primary btn-block" type="submit">Envoyer mon message</button>
          <p class="form-note" data-form-note style="margin-top:12px;">Réponse sous 48h ouvrées en moyenne.</p>
        </form>
      </div>
      <div data-reveal>
        <div class="card" style="margin-bottom:24px;">
          <div class="icon-badge">%s</div>
          <h3>Email</h3>
          <p><a href="mailto:%s">%s</a></p>
        </div>
        <div class="card" style="margin-bottom:24px;">
          <div class="icon-badge terra">%s</div>
          <h3>Téléphone</h3>
          <p>%s</p>
        </div>
        <div class="card">
          <div class="icon-badge gold">%s</div>
          <h3>Secteur</h3>
          <p>%s — échanges possibles à distance partout en France.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="container" style="max-width:840px;">
    %s
  </div>
</section>
""" % (
        breadcrumb("Contact"),
        icon("mail"), CONFIG["email"], CONFIG["email"],
        icon("phone"), CONFIG["phone"],
        icon("pin"), CONFIG["city"],
        notice("Pour toute commande, rendez-vous directement sur ma boutique en ligne officielle LR : ce formulaire sert uniquement à échanger et vous conseiller.", ic="cart"),
    )
    return page("contact.html", "Contact — %s" % CONFIG["site_name"],
                "Contactez %s, %s, pour toute question sur l'énergie, l'immunité, la nutrition ou les produits LR Health & Beauty." % (CONFIG["partner_name"], CONFIG["partner_title"]),
                body, active="contact.html")

# --------------------------------------------------------------------------
# PAGES LÉGALES
# --------------------------------------------------------------------------
def legal_page(slug, title, meta_desc, content_html):
    body = """
<section class="page-hero">
  <div class="container">
    %s
    <div class="eyebrow">Informations légales</div>
    <h1 style="max-width:700px;">%s</h1>
  </div>
</section>
<section class="section-tight">
  <div class="container">
    <div class="legal-body" data-reveal>
      %s
    </div>
  </div>
</section>
""" % (breadcrumb(title), title, content_html)
    return page(slug, "%s — %s" % (title, CONFIG["site_name"]), meta_desc, body, active=slug)


def build_mentions_legales():
    content = """
<p><em>Dernière mise à jour : [À COMPLÉTER — date de mise en ligne].</em></p>

<h2>1. Éditeur du site</h2>
<p>Le présent site, %s (ci-après « le Site »), est édité à titre personnel par :</p>
<ul>
  <li>Nom et prénom : %s</li>
  <li>Statut professionnel : %s</li>
  <li>Ville : %s ([À COMPLÉTER — adresse postale complète ou domiciliation professionnelle])</li>
  <li>Numéro SIREN : %s</li>
  <li>Email : %s</li>
  <li>Téléphone : %s</li>
  <li>Directeur de la publication : %s</li>
</ul>

<h2>2. Statut et indépendance vis-à-vis de LR Health &amp; Beauty</h2>
<p>%s est Vendeur(se) à Domicile Indépendant(e) (VDI), partenaire commercial(e) indépendant(e) de la société LR Health &amp; Beauty Systems GmbH (Ahlen, Allemagne) et de sa filiale de distribution en France. Ce statut n'est ni un contrat de travail salarié, ni un mandat de représentation officielle de la marque.</p>
<p>Le Site est un outil de communication et d'information personnel. Il n'est ni développé, ni hébergé, ni contrôlé éditorialement par LR Health &amp; Beauty. Les visuels, marques et noms de gammes LR cités (Body Mission, Health Mission, Mind Master, Aloe Vera, Super Omega, etc.) restent la propriété exclusive de LR Health &amp; Beauty Systems GmbH et sont utilisés à titre purement descriptif et informatif, conformément à l'usage autorisé aux partenaires distributeurs pour la présentation de leur activité.</p>

<h2>3. Absence de vente en ligne sur ce Site</h2>
<p>Conformément aux règles contractuelles applicables aux partenaires LR, <strong>aucune commande, aucun paiement et aucune transaction ne sont réalisés sur ce Site</strong>. Chaque bouton « Boutique LR » ou « Commander » redirige vers la boutique en ligne officielle et personnelle du partenaire, hébergée et exploitée par LR Health &amp; Beauty, seule plateforme autorisée pour l'achat des produits de la marque. Ce Site ne constitue donc pas un site de commerce électronique au sens du droit de la consommation ; il a une vocation strictement informative et d'orientation.</p>

<h2>4. Hébergement</h2>
<p>Le Site est hébergé par : Netlify, Inc. — 512 2nd Street, Suite 200, San Francisco, CA 94107, États-Unis — <a href="https://www.netlify.com" target="_blank" rel="noopener">www.netlify.com</a>.</p>

<h2>5. Propriété intellectuelle</h2>
<p>Les contenus éditoriaux du Site (textes, structure, mise en page, code) sont la propriété de %s, sauf mention contraire. Toute reproduction non autorisée est interdite. Les marques, logos et dénominations LR Health &amp; Beauty restent la propriété de leur titulaire.</p>

<h2>6. Responsabilité</h2>
<p>Les informations diffusées sur le Site le sont à titre indicatif et général. Malgré le soin apporté à leur rédaction, l'éditeur ne peut garantir l'exactitude, la complétude ou l'actualité de l'ensemble des contenus. Voir également la page <a href="cgu-avertissement.html">CGU &amp; avertissement santé</a>.</p>

<h2>7. Droit applicable</h2>
<p>Le présent site et les présentes mentions légales sont soumis au droit français. En cas de litige, et à défaut de résolution amiable, les tribunaux français compétents seront seuls saisis.</p>

<h2>8. Contact</h2>
<p>Pour toute question relative au Site, vous pouvez écrire à <a href="mailto:%s">%s</a> ou utiliser le <a href="contact.html">formulaire de contact</a>.</p>
""" % (
        CONFIG["site_name"], CONFIG["partner_name"], CONFIG["partner_title"],
        CONFIG["city"], CONFIG["siren"],
        CONFIG["email"], CONFIG["phone"], CONFIG["partner_name"],
        CONFIG["partner_name"],
        CONFIG["partner_name"],
        CONFIG["email"], CONFIG["email"],
    )
    return legal_page("mentions-legales.html", "Mentions légales",
                       "Mentions légales du site %s : éditeur, hébergeur, statut de partenaire indépendant LR Health & Beauty et conditions d'utilisation." % CONFIG["site_name"],
                       content)


def build_confidentialite():
    content = """
<p><em>Dernière mise à jour : [À COMPLÉTER].</em></p>

<h2>1. Responsable du traitement</h2>
<p>%s, %s, est responsable du traitement des données personnelles collectées via ce Site. Contact : <a href="mailto:%s">%s</a>.</p>

<h2>2. Données collectées</h2>
<p>Le Site collecte des données personnelles uniquement lorsque vous les fournissez volontairement, via :</p>
<ul>
  <li>Le <strong>formulaire de contact</strong> : nom, email, sujet, message ;</li>
  <li>Le <strong>quiz bien-être</strong> : réponses au diagnostic, prénom et email si vous demandez à recevoir des conseils personnalisés ;</li>
  <li>D'éventuels <strong>cookies techniques</strong> nécessaires au bon fonctionnement du Site (mémorisation de votre choix concernant les cookies, par exemple).</li>
</ul>
<p>Le Site ne collecte aucune donnée de santé au sens du RGPD (les réponses au quiz reflètent un objectif de bien-être général, non une donnée médicale).</p>

<h2>3. Finalités et base légale</h2>
<ul>
  <li>Répondre à vos demandes de contact : exécution de mesures précontractuelles / intérêt légitime ;</li>
  <li>Vous adresser des conseils personnalisés suite au quiz, si vous en faites la demande explicite : consentement ;</li>
  <li>Amélioration du Site et statistiques de fréquentation anonymisées, le cas échéant : intérêt légitime / consentement selon l'outil utilisé.</li>
</ul>
<p>Aucune donnée n'est transmise à LR Health &amp; Beauty ni à un tiers à des fins commerciales sans votre consentement explicite. Aucune décision automatisée ni profilage au sens de l'article 22 du RGPD n'est réalisé.</p>

<h2>4. Durée de conservation</h2>
<p>Les données issues du formulaire de contact et du quiz sont conservées pendant une durée maximale de 3 ans à compter du dernier contact, sauf obligation légale contraire ou demande de suppression anticipée de votre part.</p>

<h2>5. Destinataires</h2>
<p>Seul(e) %s, ainsi que ses éventuels prestataires techniques (hébergeur, outil d'emailing ou de formulaire — voir ci-dessous), ont accès à ces données, dans la stricte limite de leurs missions.</p>
<p>Prestataires techniques utilisés : Netlify, Inc. (hébergement du Site et traitement des soumissions des formulaires de contact et du quiz). Netlify agit en tant que sous-traitant au sens du RGPD ; sa politique de confidentialité est consultable sur <a href="https://www.netlify.com/privacy/" target="_blank" rel="noopener">netlify.com/privacy</a>.</p>

<h2>6. Cookies</h2>
<p>Le Site utilise uniquement, par défaut, des cookies techniques strictement nécessaires (ex. mémorisation de votre consentement aux cookies). Aucun cookie publicitaire ou de mesure d'audience n'est déposé sans votre accord préalable via le bandeau prévu à cet effet. Si vous ajoutez un outil de statistiques (ex. Google Analytics, Plausible), pensez à mettre à jour cette section et à recueillir le consentement requis avant tout dépôt de cookie non essentiel.</p>

<h2>7. Vos droits</h2>
<p>Conformément au Règlement Général sur la Protection des Données (RGPD) et à la loi Informatique et Libertés, vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation, d'opposition et de portabilité de vos données. Vous pouvez exercer ces droits en écrivant à <a href="mailto:%s">%s</a>.</p>
<p>Vous disposez également du droit d'introduire une réclamation auprès de la Commission Nationale de l'Informatique et des Libertés (CNIL) — <a href="https://www.cnil.fr" target="_blank" rel="noopener">www.cnil.fr</a>.</p>

<h2>8. Sécurité</h2>
<p>Des mesures raisonnables sont mises en œuvre pour protéger vos données contre la perte, l'accès non autorisé ou la divulgation. Aucun système n'étant infaillible, une sécurité absolue ne peut être garantie.</p>
""" % (
        CONFIG["partner_name"], CONFIG["partner_title"],
        CONFIG["email"], CONFIG["email"],
        CONFIG["partner_name"],
        CONFIG["email"], CONFIG["email"],
    )
    return legal_page("confidentialite-cookies.html", "Confidentialité & cookies",
                       "Politique de confidentialité et de gestion des cookies du site %s, conforme au RGPD." % CONFIG["site_name"],
                       content)


def build_cgu():
    content = """
<p><em>Dernière mise à jour : [À COMPLÉTER].</em></p>

<h2>1. Objet</h2>
<p>Les présentes Conditions Générales d'Utilisation (CGU) régissent l'accès et l'utilisation du site %s. En naviguant sur le Site, vous acceptez sans réserve les présentes conditions.</p>

<h2>2. Nature du Site</h2>
<p>Le Site a une vocation exclusivement informative et d'orientation autour du bien-être (énergie, récupération, santé hépatique et intestinale, immunité, nutrition sportive). Il ne constitue ni un site de vente en ligne, ni un service médical, ni un avis médical personnalisé. Aucune commande n'est passée sur ce Site : tout achat de produit LR Health &amp; Beauty s'effectue exclusivement via la boutique officielle du partenaire, accessible depuis les liens prévus à cet effet.</p>

<h2>3. Avertissement santé important</h2>
<div class="notice warn" style="margin:24px 0;">
  <p style="margin:0;"><strong>Les contenus du Site sont fournis à titre d'information générale et ne remplacent en aucun cas un avis, un diagnostic ou un traitement médical.</strong> Ils ne doivent pas être interprétés comme des conseils médicaux personnalisés. En cas de symptôme persistant, inhabituel ou préoccupant, consultez un médecin ou un professionnel de santé qualifié.</p>
</div>
<p>Conformément à la réglementation applicable aux compléments alimentaires (règlement (CE) n°1924/2006 et code de la santé publique), les produits évoqués sur le Site ne sont présentés comme ayant ni la propriété de prévenir, traiter ou guérir une maladie humaine. %s</p>
<p>Les témoignages et retours d'expérience relayés sur le Site sont des avis personnels, non contractuels. Ils n'engagent que leurs auteurs et ne garantissent pas des résultats similaires pour toute autre personne, les effets pouvant varier selon chaque individu, son mode de vie et son état de santé.</p>

<h2>4. Propriété intellectuelle</h2>
<p>L'ensemble des éléments du Site (textes, mise en page, identité visuelle) est protégé par le droit de la propriété intellectuelle. Toute reproduction, représentation ou exploitation, totale ou partielle, sans autorisation préalable est interdite, à l'exception des marques et contenus appartenant à LR Health &amp; Beauty Systems GmbH, cités à titre purement informatif.</p>

<h2>5. Liens vers la boutique officielle et sites tiers</h2>
<p>Le Site contient des liens vers la boutique en ligne officielle LR Health &amp; Beauty (relation commerciale d'affiliation en tant que partenaire indépendant) ainsi que, le cas échéant, vers des sites tiers. L'éditeur du Site n'exerce aucun contrôle sur le contenu de ces sites externes et décline toute responsabilité quant à leur contenu, leurs pratiques ou leur politique de confidentialité.</p>

<h2>6. Limitation de responsabilité</h2>
<p>L'éditeur met tout en œuvre pour fournir des informations fiables, mais ne saurait être tenu responsable des erreurs, omissions ou de l'usage qui serait fait des informations diffusées sur le Site, ni des décisions prises sur cette seule base, notamment en matière de santé, de nutrition ou d'achat.</p>

<h2>7. Modification des CGU</h2>
<p>Les présentes CGU peuvent être modifiées à tout moment. La version applicable est celle en vigueur à la date de consultation du Site.</p>

<h2>8. Droit applicable et litiges</h2>
<p>Les présentes CGU sont soumises au droit français. Conformément à l'article L.616-1 du Code de la consommation, en cas de litige non résolu à l'amiable, le consommateur peut recourir gratuitement à un médiateur de la consommation en vue de la résolution amiable du litige [À COMPLÉTER : coordonnées du médiateur de la consommation compétent, si applicable à votre activité].</p>
""" % (
        CONFIG["site_name"],
        FOOD_SUPPLEMENT_DISCLAIMER,
    )
    return legal_page("cgu-avertissement.html", "CGU & avertissement santé",
                       "Conditions générales d'utilisation du site %s et avertissement santé sur les contenus liés aux compléments alimentaires." % CONFIG["site_name"],
                       content)

# --------------------------------------------------------------------------
# PAGE 404
# --------------------------------------------------------------------------
def build_404():
    pillar_links = "\n".join(
        '<a href="%s" class="pillar-chip">%s</a>' % (h, l) for h, l, _ in PILLARS
    )
    body = """
<section class="section" style="padding-top:110px;text-align:center;">
  <div class="container" style="max-width:640px;">
    <div class="eyebrow center" style="justify-content:center;display:flex;">Erreur 404</div>
    <h1 style="font-size:clamp(3.4rem,9vw,6rem);">Perdu·e en chemin ?</h1>
    <p class="lede center" style="margin:0 auto 8px;">
      Cette page n'existe pas ou plus — mais votre objectif bien-être, lui, existe toujours.
      Repartons du bon pied.
    </p>
    <div class="hero-actions" style="justify-content:center;margin-top:30px;">
      %s
      %s
    </div>
    <div class="pillar-nav" style="justify-content:center;">
      %s
    </div>
  </div>
</section>
""" % (
        btn("Retour à l'accueil", "index.html", variant="primary"),
        btn("Faire le quiz bien-être", "quiz.html", variant="outline"),
        pillar_links,
    )
    return page("404.html", "Page introuvable (404) — %s" % CONFIG["site_name"],
                "Cette page n'existe pas. Retrouvez l'accueil, le quiz bien-être ou les univers thématiques du site.",
                body, active="", noindex=True)


# --------------------------------------------------------------------------
# PAGE DE CONFIRMATION (formulaires Netlify)
# --------------------------------------------------------------------------
def build_merci():
    body = """
<section class="section" style="padding-top:110px;text-align:center;">
  <div class="container" style="max-width:600px;">
    <div class="icon-badge" style="margin:0 auto 24px;">%s</div>
    <div class="eyebrow center" style="justify-content:center;display:flex;">Message envoyé</div>
    <h1 style="font-size:clamp(2.4rem,6vw,3.4rem);">Merci !</h1>
    <p class="lede center" style="margin:0 auto 8px;">
      Votre message a bien été reçu. %s vous répond généralement sous 48h ouvrées.
    </p>
    <div class="hero-actions" style="justify-content:center;margin-top:30px;">
      %s
      %s
    </div>
  </div>
</section>
""" % (
        icon("check"),
        CONFIG["partner_name"],
        btn("Retour à l'accueil", "index.html", variant="primary"),
        btn("Découvrir les gammes LR", "gammes-lr.html", variant="outline"),
    )
    return page("merci.html", "Message envoyé — %s" % CONFIG["site_name"],
                "Votre message a bien été envoyé, merci de votre confiance.",
                body, active="", noindex=True)


# --------------------------------------------------------------------------
# GÉNÉRATION
# --------------------------------------------------------------------------
def main():
    pages = {}
    pages["index.html"] = build_home()
    for cfg in PILLAR_PAGES:
        pages[cfg["slug"]] = build_pillar_page(cfg)
    pages["nutrition-objectifs.html"] = build_nutrition()
    pages["gammes-lr.html"] = build_gammes()
    pages["quiz.html"] = build_quiz()
    pages["a-propos.html"] = build_apropos()
    pages["contact.html"] = build_contact()
    pages["mentions-legales.html"] = build_mentions_legales()
    pages["confidentialite-cookies.html"] = build_confidentialite()
    pages["cgu-avertissement.html"] = build_cgu()

    # sitemap.xml (avant l'ajout de la page 404, volontairement absente du plan du site)
    urls = "\n".join(
        "  <url><loc>%s/%s</loc></url>" % (CONFIG["domain"].rstrip("/"), slug if slug != "index.html" else "")
        for slug in pages
    )
    pages["404.html"] = build_404()
    pages["merci.html"] = build_merci()

    for slug, html in pages.items():
        with open(os.path.join(ROOT, slug), "w", encoding="utf-8") as f:
            f.write(html)
        print("✓ %s" % slug)
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>\n' % urls
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("✓ sitemap.xml")

    robots = "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % CONFIG["domain"].rstrip("/")
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)
    print("✓ robots.txt")

    print("\nTerminé : %d pages générées." % len(pages))


if __name__ == "__main__":
    main()
