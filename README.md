# Vitalis — site bien-être & nutrition (partenaire LR Health & Beauty)

Site statique (HTML/CSS/JS, aucun framework, aucune base de données) conçu pour :

- expliquer 5 piliers bien-être : **Énergie & Vitalité**, **Récupération & Sommeil**,
  **Foie & Détox cellulaire**, **Digestion & Microbiote**, **Système immunitaire** ;
- couvrir la **nutrition sportive** (perte de poids / prise de masse) ;
- présenter les **gammes LR** (Body Mission, Health Mission, Mind Master, Super Omega,
  Aloe Vera...) classées par objectif plutôt qu'en catalogue brut ;
- qualifier un visiteur froid via un **quiz de diagnostic** (3 questions) qui l'oriente
  vers le bon pilier et la bonne gamme ;
- rediriger **toutes** les commandes vers la boutique en ligne **officielle** LR (aucune
  vente, aucun paiement traité sur ce site — voir `CONFORMITE.md`).

## ⚠️ À faire avant mise en ligne

Le site est fonctionnel mais contient des **placeholders** à remplacer. Ouvrez
`scripts/build.py` et modifiez le dictionnaire `CONFIG` en tête de fichier :

```python
CONFIG = {
    "site_name": "Vitalis",                # gardez ou changez le nom de marque
    "partner_name": "...",                 # VOTRE nom et prénom
    "partner_title": "Partenaire indépendant(e) LR Health & Beauty",
    "city": "...",                         # votre ville
    "email": "...",
    "phone": "...",
    "shop_url": "...",                     # lien de votre eShop LR personnel (lrworld.com/...)
    "instagram": "...",
    "facebook": "...",
    "domain": "https://www.votre-domaine.fr",
    "form_action": "...",                  # endpoint Formspree / Brevo / autre (voir plus bas)
}
```

Puis régénérez toutes les pages :

```bash
python3 scripts/build.py
```

Cette commande réécrit les 14 fichiers `.html` à la racine à partir des gabarits — ne
modifiez jamais un fichier `.html` directement à la racine, il serait écrasé au prochain
`build.py`. Modifiez le contenu dans `scripts/build.py` (textes, produits, FAQ...).

Pensez aussi à :
- compléter la page **`a-propos.html`** (généré depuis `build_apropos()`) avec votre
  vrai parcours — les crochets `[À COMPLÉTER]` marquent les passages à personnaliser ;
- compléter les 3 pages légales (`mentions-legales.html`, `confidentialite-cookies.html`,
  `cgu-avertissement.html`) : hébergeur, éventuel SIREN/RSAC, médiateur de la
  consommation — voir les `[À COMPLÉTER]` dans `scripts/build.py` ;
- **faire relire l'ensemble par le service conformité/marketing LR** et, en cas de doute,
  par un professionnel du droit — voir `CONFORMITE.md` pour le détail des points de
  vigilance identifiés.
- remplacer les icônes/illustrations vectorielles par de vraies photos si vous le
  souhaitez (le design fonctionne aussi très bien sans photo, en 100% vectoriel/typo).

## Structure du projet

```
index.html, energie-vitalite.html, ...   → pages générées (ne pas éditer à la main)
assets/css/style.css                     → design system (couleurs, typographie, composants)
assets/js/main.js                        → nav mobile, animations, bandeau cookies, formulaires
assets/js/quiz.js                        → logique du quiz de diagnostic
scripts/build.py                         → générateur : CONFIG + contenu de toutes les pages
robots.txt, sitemap.xml                  → SEO technique (générés par build.py)
CONFORMITE.md                            → note de cadrage légal (à lire avant publication)
```

## Formulaires (contact, quiz, newsletter)

Le site est statique : les formulaires ne font rien tant que `form_action` dans `CONFIG`
n'est pas renseigné. Deux options simples, sans backend à héberger :

1. **Formspree** (https://formspree.io) : créez un formulaire, copiez l'URL fournie
   dans `form_action`.
2. **Brevo / Sendinblue** ou un autre outil d'emailing : utilisez leur formulaire
   embarqué ou leur endpoint de collecte.

Tant que `form_action` contient le mot `REMPLACER`, le site affiche un message
explicatif à la place d'un envoi silencieux qui échouerait.

## Lancer le site en local

Aucune installation nécessaire :

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

## Déploiement

Le site est 100% statique : il se déploie tel quel sur **Netlify**, **Vercel**,
**GitHub Pages**, **Cloudflare Pages** ou tout hébergeur mutualisé classique (upload
FTP du dossier). Aucune base de données, aucun serveur applicatif requis.

## SEO

- Chaque page a un `<title>`, une `meta description`, une URL canonique et des balises
  Open Graph propres à son sujet.
- Les pages « piliers » embarquent un balisage `FAQPage` (JSON-LD) pour les questions
  fréquentes, favorable aux extraits enrichis Google.
- `sitemap.xml` et `robots.txt` sont générés automatiquement — pensez à soumettre le
  sitemap dans Google Search Console une fois le domaine final connu (mettez à jour
  `domain` dans `CONFIG` avant de régénérer).
