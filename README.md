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

## Design

Palette vert forêt profond / crème, boutons pilule à pastille circulaire, cartes
« photo » en dégradé + grain avec badges flottants, bento-grid en page d'accueil,
accordéon de réassurance — inspiré des interfaces bien-être premium actuelles.

**Aucune vraie photo n'est utilisée** : les emplacements photo (`.photo-block`) sont
des dégradés vectoriels avec icône, pour éviter d'utiliser des images de personnes
sans droits. Dès que vous avez vos propres photos (vous, vos produits, votre
activité), elles s'intègrent facilement : dans `assets/css/style.css`, remplacez le
`background` de `.photo-block` par une vraie image (`background-image:url(...)` +
`background-size:cover`), ou ajoutez une balise `<img>` par carte dans `scripts/build.py`
à la place du `<div class="photo-block">`.

## ⚠️ À faire avant mise en ligne

L'essentiel est déjà renseigné dans `CONFIG` (coordonnées, eShop LR, LinkedIn, SIREN,
hébergeur Netlify). Il reste à mettre à jour `domain` une fois votre nom de domaine
choisi, et éventuellement `analytics_domain` (voir plus bas) :

```python
CONFIG = {
    "site_name": "Vitalis",                # gardez ou changez le nom de marque
    "partner_name": "Valentin Delaine",
    "partner_title": "Partenaire indépendant(e) LR Health & Beauty",
    "city": "Dole",
    "email": "delaineval@gmail.com",
    "phone": "06 36 47 01 31",
    "shop_url": "https://shop.lrworld.com/home?PHP=...",   # déjà renseigné
    "linkedin": "https://www.linkedin.com/in/...",         # déjà renseigné
    "siren": "103 127 288",                                # déjà renseigné
    "domain": "https://www.votre-domaine.fr",              # à mettre à jour une fois le domaine choisi
    "analytics_domain": "",                                # voir section « Statistiques »
}
```

Puis régénérez toutes les pages :

```bash
python3 scripts/build.py
```

Cette commande réécrit les 16 fichiers `.html` à la racine à partir des gabarits — ne
modifiez jamais un fichier `.html` directement à la racine, il serait écrasé au prochain
`build.py`. Modifiez le contenu dans `scripts/build.py` (textes, produits, FAQ...).

Il reste encore quelques `[À COMPLÉTER]` ponctuels dans `scripts/build.py` (date de
dernière mise à jour des pages légales, adresse postale complète, médiateur de la
consommation le cas échéant) — cherchez `[À COMPLÉTER]` dans le fichier.

Pensez aussi à :
- **faire relire l'ensemble par le service conformité/marketing LR** et, en cas de doute,
  par un professionnel du droit — voir `CONFORMITE.md` pour le détail des points de
  vigilance identifiés ;
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

## Formulaires (contact, quiz)

Le site étant hébergé sur **Netlify**, les deux formulaires (contact et quiz) utilisent
**Netlify Forms** — aucun compte tiers, aucune clé à configurer :

1. Déployez le site sur Netlify (voir ci-dessous). Netlify détecte automatiquement les
   formulaires marqués `data-netlify="true"` au moment du build.
2. Les soumissions apparaissent dans **Netlify → votre site → Forms**. Vous pouvez y
   activer une notification par email à chaque nouvelle soumission (Settings → Forms →
   Form notifications).
3. Un champ piège anti-spam (`bot-field`, invisible pour un humain) est déjà en place.

Après envoi, les deux formulaires redirigent vers `merci.html`, une page de
confirmation dédiée. Si vous changez un jour d'hébergeur, il faudra remplacer ce
système par un service tiers (Formspree, Brevo...) et retirer les attributs
`data-netlify`.

## Lancer le site en local

Aucune installation nécessaire :

```bash
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

## Déploiement (Netlify)

Le site est hébergé sur **Netlify** — mentions légales et politique de confidentialité
mises à jour en conséquence. Deux façons de déployer :

1. **Depuis GitHub (recommandé)** : sur [app.netlify.com](https://app.netlify.com),
   « Add new site → Import an existing project », connectez ce dépôt GitHub. Aucune
   commande de build n'est nécessaire (site déjà généré) — laissez « Build command »
   vide et « Publish directory » sur `.` (la racine). Chaque push sur la branche
   redéploiera automatiquement le site.
2. **Glisser-déposer** : sur app.netlify.com, faites glisser le dossier du projet
   directement dans l'interface « Deploys ».

Pensez à :
- configurer votre nom de domaine dans Netlify (Site settings → Domain management)
  puis mettre à jour `domain` dans `CONFIG` et régénérer le site ;
- activer les notifications email des formulaires (Site settings → Forms) ;
- vérifier que `404.html` est bien servi comme page d'erreur (Netlify le fait
  automatiquement pour un fichier à ce nom placé à la racine).

## SEO

- Chaque page a un `<title>`, une `meta description`, une URL canonique et des balises
  Open Graph + Twitter Card propres à son sujet (avec image de partage, voir plus bas).
- Les pages « piliers » embarquent un balisage `FAQPage` (JSON-LD) pour les questions
  fréquentes, favorable aux extraits enrichis Google.
- `sitemap.xml` et `robots.txt` sont générés automatiquement — pensez à soumettre le
  sitemap dans Google Search Console une fois le domaine final connu (mettez à jour
  `domain` dans `CONFIG` avant de régénérer).
- Une page **404 personnalisée** (`404.html`) est générée, marquée `noindex` et propose
  de revenir à l'accueil, au quiz ou à un pilier. Sur Netlify/Vercel/GitHub Pages elle
  est servie automatiquement ; sur un hébergeur classique, configurez la page d'erreur
  404 pour pointer vers ce fichier.

## Image de partage (réseaux sociaux)

`assets/img/og-image.png` (1200×630) est utilisée pour l'aperçu du lien sur
WhatsApp / Facebook / LinkedIn / X. Elle a été générée à partir de
`scripts/build.py` (palette + logo du site, sans photo). Si vous changez la palette,
le nom de marque ou souhaitez une vraie photo, régénérez-la avec votre propre outil
(Canva, Figma...) au même format et remplacez le fichier — le nom doit rester identique
pour que les balises `og:image` continuent de fonctionner.

## Statistiques (Analytics)

Aucun outil de mesure d'audience n'est activé par défaut. Pour en ajouter un sans
polluer la conformité RGPD déjà en place :

1. Créez un compte sur [Plausible](https://plausible.io) (respectueux de la vie privée,
   sans cookie de tracking) et renseignez votre domaine.
2. Dans `scripts/build.py`, remplissez `CONFIG["analytics_domain"]` avec ce domaine.
3. Régénérez le site (`python3 scripts/build.py`).

Le script ne se charge **qu'après acceptation du bandeau cookies** (`assets/js/main.js`,
fonction `loadAnalytics`) — tant que `analytics_domain` est vide, rien n'est chargé.
Pour utiliser Google Analytics à la place, adaptez cette fonction avec le snippet GA4.

## Accessibilité

- Lien d'évitement (« Aller au contenu ») visible au clavier en tout début de page.
- Contours de focus visibles sur tous les liens, boutons et champs (`:focus-visible`).
- Icônes décoratives marquées `aria-hidden` ; les boutons pilule portent un `aria-label`
  explicite même quand leur texte est masqué visuellement en mobile.
- Le site n'utilise aucune balise `<img>` (uniquement des dégradés et icônes SVG
  décoratives) : il n'y a donc pas de texte alternatif à renseigner. Le jour où vous
  ajoutez de vraies photos, pensez à leur donner un attribut `alt` descriptif.
- Toutes les animations respectent `prefers-reduced-motion : reduce` : si l'utilisateur
  a activé cette préférence système, les apparitions au scroll, la parallaxe et les
  animations de texte sont désactivées et le contenu s'affiche directement.

## Animations

Les interactions (apparition au scroll, survols de boutons/cartes, accordéons,
mosaïque héro) sont pilotées par `assets/css/style.css` et `assets/js/main.js`, avec
une régle générale : **transform + opacity uniquement** (performant, pas de saccades),
jamais de propriétés qui déclenchent un recalcul de mise en page. Tout est
automatiquement désactivé pour les utilisateurs qui préfèrent un mouvement réduit.
