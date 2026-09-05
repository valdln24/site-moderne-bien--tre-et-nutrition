// Vitalis — Quiz de diagnostic bien-être (qualification du prospect)
(function () {
  "use strict";
  var shell = document.querySelector("[data-quiz]");
  if (!shell) return;

  var RESULTS = {
    energie: {
      badge: "Votre priorité : Énergie & Vitalité",
      text: "Vos réponses évoquent une fatigue plus fonctionnelle qu'un simple manque de sommeil : rythme soutenu, coups de mou dans la journée, motivation en dents de scie. La priorité est de soutenir votre organisme au quotidien (hydratation, micronutrition, activité) avant d'envisager des compléments ciblés.",
      pillarHref: "energie-vitalite.html",
      pillarLabel: "Explorer le pilier Énergie & Vitalité",
      rangeHref: "gammes-lr.html#mind-master",
      rangeLabel: "Découvrir la gamme Mind Master",
    },
    recuperation: {
      badge: "Votre priorité : Récupération & Sommeil",
      text: "Ce que vous décrivez ressemble à une récupération incomplète : sommeil peu réparateur, tensions physiques, sensation de ne jamais vraiment repartir à zéro. Travailler la qualité du repos et l'équilibre du système nerveux est le premier levier avant tout le reste.",
      pillarHref: "recuperation-sommeil.html",
      pillarLabel: "Explorer le pilier Récupération & Sommeil",
      rangeHref: "gammes-lr.html#health-mission",
      rangeLabel: "Découvrir la gamme Health Mission",
    },
    foie: {
      badge: "Votre priorité : Foie & Détox cellulaire",
      text: "Vous cherchez avant tout à alléger votre organisme : digestion lourde après les repas, sensation de fatigue post-prandiale, envie de faire une pause détox saisonnière. La santé hépatique et cellulaire est votre point d'entrée.",
      pillarHref: "foie-detox.html",
      pillarLabel: "Explorer le pilier Foie & Détox",
      rangeHref: "gammes-lr.html#aloe-vera",
      rangeLabel: "Découvrir la gamme Aloe Vera",
    },
    digestion: {
      badge: "Votre priorité : Confort intestinal & Microbiote",
      text: "Ballonnements, transit irrégulier, inconfort après certains repas : votre équilibre intestinal mérite une attention particulière. Un microbiote choyé est aussi la base d'une bonne immunité et d'une belle énergie.",
      pillarHref: "digestion-microbiote.html",
      pillarLabel: "Explorer le pilier Digestion & Microbiote",
      rangeHref: "gammes-lr.html#health-mission",
      rangeLabel: "Découvrir la gamme Health Mission",
    },
    immunite: {
      badge: "Votre priorité : Système immunitaire",
      text: "Changements de saison, fatigue qui traîne, sensibilité accrue aux petits maux du quotidien : vos défenses naturelles ont besoin d'être soutenues avant l'hiver ou après une période difficile.",
      pillarHref: "immunite.html",
      pillarLabel: "Explorer le pilier Immunité",
      rangeHref: "gammes-lr.html#super-omega",
      rangeLabel: "Découvrir la gamme Super Omega-3",
    },
    poids: {
      badge: "Votre priorité : Perte de poids",
      text: "Vous souhaitez retrouver une silhouette qui vous ressemble, en douceur et sans frustration. Un accompagnement structuré (alimentation, activité, rituel) associé à un programme nutritionnel adapté fera toute la différence.",
      pillarHref: "nutrition-objectifs.html#perte-de-poids",
      pillarLabel: "Explorer le programme Perte de poids",
      rangeHref: "gammes-lr.html#body-mission",
      rangeLabel: "Découvrir la gamme Body Mission",
    },
    masse: {
      badge: "Votre priorité : Prise de masse & Performance",
      text: "Vous voulez progresser, construire du muscle et mieux récupérer entre vos séances. Un apport protéique adapté et une bonne récupération sont vos deux meilleurs alliés.",
      pillarHref: "nutrition-objectifs.html#prise-de-masse",
      pillarLabel: "Explorer le programme Prise de masse",
      rangeHref: "gammes-lr.html#body-mission",
      rangeLabel: "Découvrir la gamme Body Mission",
    },
  };

  var state = { step: 0, goal: null, answers: {} };
  var steps = shell.querySelectorAll(".quiz-step");
  var progressBar = shell.querySelector(".quiz-progress-bar");
  var resultPanel = shell.querySelector(".quiz-result");

  function showStep(i) {
    steps.forEach(function (s, idx) {
      s.classList.toggle("active", idx === i);
    });
    if (progressBar) {
      progressBar.style.width = Math.round(((i + 1) / (steps.length + 1)) * 100) + "%";
    }
  }

  shell.addEventListener("click", function (e) {
    var opt = e.target.closest(".quiz-option");
    if (!opt) return;
    var group = opt.closest(".quiz-step");
    group.querySelectorAll(".quiz-option").forEach(function (o) { o.classList.remove("selected"); });
    opt.classList.add("selected");
    var key = group.getAttribute("data-question");
    state.answers[key] = opt.getAttribute("data-value");
    if (key === "objectif") state.goal = opt.getAttribute("data-value");

    setTimeout(function () {
      var next = state.step + 1;
      if (next < steps.length) {
        state.step = next;
        showStep(next);
      } else {
        renderResult();
      }
    }, 260);
  });

  shell.querySelectorAll("[data-quiz-back]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (state.step > 0) {
        state.step -= 1;
        showStep(state.step);
      }
    });
  });

  function renderResult() {
    steps.forEach(function (s) { s.classList.remove("active"); });
    if (progressBar) progressBar.style.width = "100%";
    var result = RESULTS[state.goal] || RESULTS.energie;
    resultPanel.querySelector("[data-result-badge]").textContent = result.badge;
    resultPanel.querySelector("[data-result-text]").textContent = result.text;
    var pillarLink = resultPanel.querySelector("[data-result-pillar]");
    pillarLink.href = result.pillarHref;
    pillarLink.textContent = result.pillarLabel;
    var rangeLink = resultPanel.querySelector("[data-result-range]");
    rangeLink.href = result.rangeHref;
    rangeLink.textContent = result.rangeLabel;
    resultPanel.classList.add("active");
  }

  showStep(0);
})();
