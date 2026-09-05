# Note de cadrage légal — site personnel de partenaire indépendant LR Health & Beauty

**Important** : ce document synthétise des recherches publiques (sites officiels
d'administrations françaises, presse spécialisée, communication publique de
LR Health & Beauty) pour orienter la conception du site. **Il ne constitue pas une
consultation juridique.** Avant mise en ligne définitive, faites valider le contenu par
le service conformité/marketing LR (voir point 1) et, si vous en avez la possibilité,
par un professionnel du droit — en particulier si votre activité prend de l'ampleur
(trafic, publicité payante, chiffre d'affaires).

## 1. Le point de départ : pourquoi LR encadre les sites de ses partenaires

LR Health & Beauty Systems GmbH dispose d'un système de gestion de la conformité
(Compliance Management System) et rappelle que ses partenaires doivent utiliser les
informations et supports produits fournis ou validés par l'entreprise. Les partenaires
disposent par ailleurs, gratuitement, d'un **eShop personnel officiel** hébergé par LR
(processus de commande, paiement, logistique, facturation gérés par LR elle-même).
C'est cette boutique qui doit rester **l'unique canal de vente**.

**Ce que cela implique pour le site que vous m'avez demandé de construire :**
- Le site est un **site de contenu et d'orientation**, pas un site marchand : aucun
  prix, aucun panier, aucun paiement n'y sont traités.
- Chaque bouton « Commander » / « Voir sur ma boutique LR » ouvre, dans un nouvel
  onglet, votre eShop officiel (`shop_url` dans la configuration) — c'est la seule
  destination transactionnelle.
- Les visuels/marques/noms de gammes LR (Body Mission, Health Mission, Mind Master,
  Super Omega, Aloe Vera...) sont utilisés à titre purement descriptif et informatif, de
  façon loyale, sans laisser croire que le site est un site officiel de la marque — un
  bandeau de transparence (« site personnel et indépendant », statut VDI) figure sur
  toutes les pages et dans les mentions légales.

**Action recommandée avant publication** : LR dispose d'une équipe conformité/marketing
qui peut, dans de nombreux réseaux de vente directe, valider les supports créés par les
partenaires (chartes graphiques, usage de marque, formulations autorisées). Je n'ai pas
pu accéder au détail exact de cette procédure pour votre pays (page bloquée depuis cet
environnement), donc **contactez votre upline ou le service partenaires LR** pour
confirmer la marche à suivre et les éventuelles règles d'usage de marque à respecter
(logo, couleurs, mentions obligatoires spécifiques à LR).

## 2. Compléments alimentaires : le cadre le plus sensible

Le site aborde des thèmes de santé (énergie, foie, digestion, immunité) et présente des
compléments alimentaires. En France, cette activité est strictement encadrée :

- **Règlement (CE) n°1924/2006** : seules les allégations nutritionnelles et de santé
  figurant sur la liste positive communautaire (registre UE) peuvent être utilisées.
  Il est interdit d'attribuer à un aliment ou complément des propriétés de
  **prévention, de traitement ou de guérison** d'une maladie humaine, ou même de le
  suggérer.
- La **DGCCRF** contrôle spécifiquement les sites de distributeurs de compléments
  alimentaires (pas seulement les fabricants) et sanctionne les discours anxiogènes,
  les promesses non prouvées et les allégations non autorisées.
- Un **jugement du Tribunal de commerce de Paris (4 septembre 2020)** a condamné une
  entreprise pour avoir relayé, via des témoignages clients sur les réseaux sociaux, des
  effets thérapeutiques non autorisés attribués à des compléments alimentaires — les
  témoignages ne sont donc pas un moyen de contourner l'interdiction des allégations
  santé.

**Comment le site que j'ai construit gère ce risque :**
- Chaque page « pilier » adopte une posture **explicative et non promotionnelle** :
  causes possibles, signaux à surveiller, leviers d'hygiène de vie *avant* le produit.
- Le vocabulaire produit reste volontairement prudent (« peut accompagner »,
  « traditionnellement associé à », « contribue à » plutôt que « soigne », « guérit »,
  « élimine les toxines »...). La page Foie & Détox déconstruit explicitement le
  mythe marketing de la « détox ».
- Un bandeau rappelle systématiquement que le contenu est informatif et ne remplace pas
  un avis médical, avec invitation à consulter en cas de symptôme persistant.
- La mention réglementaire obligatoire figure en pied de page de **toutes** les pages :
  *« Les compléments alimentaires ne se substituent pas à une alimentation variée et
  équilibrée ni à un mode de vie sain (...) »*.
- Les témoignages sont explicitement signalés comme personnels, non contractuels, avec
  résultats variables — jamais formulés en termes d'effet thérapeutique.

**Point de vigilance pour vous, en continu** : à chaque fois que vous ajouterez un
texte, une story, ou une nouvelle fiche produit, gardez ce réflexe — *« est-ce que je
suggère, même indirectement, qu'un produit prévient, traite ou guérit quelque chose ? »*
Si oui, reformulez. En cas de doute sur une allégation précise, le registre européen des
allégations de santé autorisées (base de données de la Commission européenne) fait foi.

## 3. Votre statut de Vendeur à Domicile Indépendant (VDI)

- En dessous d'un certain seuil d'activité, un VDI n'est pas tenu de s'immatriculer au
  Registre du Commerce (RCS) ou au Registre Spécial des Agents Commerciaux (RSAC).
  L'immatriculation au RSAC devient obligatoire uniquement après **3 années civiles
  consécutives** d'activité avec une rémunération brute annuelle dépassant **50 % du
  plafond annuel de la Sécurité sociale**. Vérifiez votre situation actuelle avant de
  compléter les mentions légales (champ SIREN/RSAC laissé en `[À COMPLÉTER]`).
- Le statut de VDI n'est pas un contrat de travail salarié : le site doit rester
  factuel sur ce point (c'est le cas dans les mentions légales générées).

## 4. Obligations générales d'un site internet français

- **Mentions légales** (loi LCEN, art. 6-III) : identité de l'éditeur, hébergeur,
  directeur de publication — généré dans `mentions-legales.html`, à compléter avec les
  coordonnées de votre hébergeur réel.
- **RGPD** : toute collecte de données (formulaire de contact, quiz avec email) suppose
  une information claire des personnes, une base légale, une durée de conservation
  définie, et le respect de leurs droits (accès, rectification, effacement...) —
  traité dans `confidentialite-cookies.html`.
- **Cookies** : un bandeau de consentement est intégré (`assets/js/main.js`) ; par
  défaut le site ne dépose aucun cookie non essentiel. Si vous ajoutez un outil de
  mesure d'audience (Google Analytics, Plausible, Meta Pixel...), il faudra recueillir
  le consentement **avant** le dépôt du cookie et mettre à jour la politique de
  confidentialité en conséquence.
- **Médiation de la consommation** (art. L.616-1 du Code de la consommation) : dans la
  mesure où ce site ne vend rien directement, l'obligation de désigner un médiateur de
  la consommation relève avant tout de la boutique officielle LR (qui vend réellement).
  Un champ `[À COMPLÉTER]` a néanmoins été laissé dans les CGU par précaution, à arbitrer
  avec LR/un juriste selon la qualification exacte de votre activité.

## 5. Nutrition sportive (perte de poids / prise de masse)

La page dédiée reste volontairement sur des repères généraux et prudents (déficit/
surplus calorique modéré, apport protéique indicatif, importance de l'activité physique
et du sommeil), avec un rappel explicite qu'un changement alimentaire important doit
être discuté avec un professionnel de santé ou un diététicien — notamment pour éviter
toute requalification en « conseil diététique personnalisé » qui relèverait d'une
profession réglementée.

## 6. Ce qu'il vous reste à faire, concrètement

1. Contacter votre upline / le service partenaires LR pour confirmer les règles d'usage
   de marque et, si elle existe, la procédure de validation des supports de
   communication personnels.
2. Compléter tous les champs `[À COMPLÉTER]` (identité, hébergeur, éventuel SIREN/RSAC).
3. Faire relire au minimum les pages **Foie & Détox**, **Digestion & Microbiote**,
   **Système immunitaire** et **Nutrition sportive** (les plus sensibles sur le plan des
   allégations) avant mise en ligne.
4. Conserver ce réflexe de vigilance sur les allégations à chaque mise à jour de
   contenu, et particulièrement sur les réseaux sociaux liés au site (les mêmes règles
   s'y appliquent).

## Sources principales consultées

- DGCCRF — [Les allégations de santé sur les sites internet de compléments alimentaires](https://www.economie.gouv.fr/dgccrf/allegations-sante-sur-sites-internet-complements-alimentaires)
- DGCCRF — [Étiquetage, présentation et publicité des compléments alimentaires](https://www.economie.gouv.fr/dgccrf/les-fiches-pratiques/etiquetage-presentation-et-publicite-des-complements-alimentaires-les-regles-connaitre)
- economie.gouv.fr — [Mentions obligatoires sur un site internet](https://www.economie.gouv.fr/entreprises/developper-son-entreprise/innover-et-numeriser-son-entreprise/mentions-sur-votre-site-internet-les-obligations-respecter)
- Service-Public.fr / LegalPlace — statut du Vendeur à Domicile Indépendant (VDI) et
  seuils d'immatriculation RSAC
- LRWorld.com — page « Compliance » (communication publique de LR Health & Beauty sur
  son dispositif de conformité)
- Recherches publiques sur les gammes LR (Body Mission, Health Mission, Mind Master,
  Super Omega, Aloe Vera) via sites de partenaires LR et communiqués publics
