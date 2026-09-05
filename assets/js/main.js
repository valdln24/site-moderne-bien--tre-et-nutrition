// Vitalis — comportements globaux du site
(function () {
  "use strict";

  // Navigation mobile
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav-desktop");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      nav.classList.toggle("open");
      var expanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!expanded));
    });
    // Accordéon des sous-menus en mobile
    document.querySelectorAll(".dropdown > a").forEach(function (link) {
      link.addEventListener("click", function (e) {
        if (window.innerWidth <= 960) {
          var parent = link.closest(".dropdown");
          var isOpen = parent.classList.contains("open");
          if (!isOpen) {
            e.preventDefault();
            document.querySelectorAll(".dropdown.open").forEach(function (d) { d.classList.remove("open"); });
            parent.classList.add("open");
          }
        }
      });
    });
  }

  // Fermer le menu mobile au clic sur un lien simple
  document.querySelectorAll(".nav-desktop a:not(.dropdown > a)").forEach(function (a) {
    a.addEventListener("click", function () {
      if (nav) nav.classList.remove("open");
    });
  });

  // Année dynamique dans le footer
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // Révélation douce au scroll
  var reveals = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.style.opacity = "1";
            entry.target.style.transform = "none";
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    reveals.forEach(function (el, i) {
      el.style.opacity = "0";
      el.style.transform = "translateY(18px)";
      el.style.transition = "opacity .6s ease " + Math.min(i * 60, 300) + "ms, transform .6s ease " + Math.min(i * 60, 300) + "ms";
      io.observe(el);
    });
  }

  // Bandeau cookies (RGPD) — consentement stocké localement, aucun cookie tiers par défaut
  var banner = document.querySelector("[data-cookie-banner]");
  if (banner) {
    try {
      var consent = localStorage.getItem("vitalis_cookie_consent");
      if (!consent) banner.hidden = false;
    } catch (err) {
      banner.hidden = false;
    }
    var accept = banner.querySelector("[data-cookie-accept]");
    var decline = banner.querySelector("[data-cookie-decline]");
    function closeBanner(value) {
      try { localStorage.setItem("vitalis_cookie_consent", value); } catch (err) {}
      banner.hidden = true;
    }
    if (accept) accept.addEventListener("click", function () { closeBanner("accepted"); });
    if (decline) decline.addEventListener("click", function () { closeBanner("declined"); });
  }

  // Formulaire de contact / newsletter — retour visuel simple (sans backend)
  document.querySelectorAll("form[data-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      var action = form.getAttribute("action");
      var hasRealAction = action && action.indexOf("REMPLACER") === -1 && action.trim() !== "" && action.trim() !== "#";
      if (!hasRealAction) {
        e.preventDefault();
        var note = form.querySelector("[data-form-note]");
        if (note) {
          note.textContent = "Merci ! Ce formulaire est un modèle de démonstration : connectez-le à votre messagerie ou à un outil comme Formspree / Brevo pour recevoir réellement les messages (voir le README).";
          note.style.color = "var(--terracotta-deep)";
        }
      }
    });
  });
})();
