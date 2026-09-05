// Vitalis — comportements globaux du site
(function () {
  "use strict";

  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Navigation mobile
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav-desktop");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      nav.classList.toggle("open");
      var expanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!expanded));
      toggle.classList.toggle("is-open");
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

  // Révélation douce au scroll (fondu + léger déplacement), désactivée si
  // l'utilisateur préfère un mouvement réduit : tout reste visible directement.
  var reveals = document.querySelectorAll("[data-reveal]");
  if (reduceMotion) {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  } else if ("IntersectionObserver" in window && reveals.length) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    reveals.forEach(function (el, i) {
      el.style.transitionDelay = Math.min(i % 5 * 70, 280) + "ms";
      io.observe(el);
    });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  }

  // Parallaxe très légère sur la mosaïque de la page d'accueil (désactivée si
  // mouvement réduit). Purement décorative, aucune incidence sur la mise en page.
  var bento = document.querySelector("[data-parallax]");
  if (bento && !reduceMotion) {
    var tiles = bento.querySelectorAll("[data-parallax-tile]");
    var ticking = false;
    function updateParallax() {
      var rect = bento.getBoundingClientRect();
      var progress = (window.innerHeight - rect.top) / (window.innerHeight + rect.height);
      progress = Math.max(0, Math.min(1, progress));
      tiles.forEach(function (tile, i) {
        var depth = (i % 2 === 0) ? 14 : 24;
        var shift = (progress - 0.5) * depth;
        tile.style.transform = "translateY(" + shift.toFixed(1) + "px)";
      });
      ticking = false;
    }
    window.addEventListener("scroll", function () {
      if (!ticking) {
        requestAnimationFrame(updateParallax);
        ticking = true;
      }
    }, { passive: true });
    updateParallax();
  }

  // Accordéons (feature-accordion et FAQ en <details>) : hauteur animée en
  // douceur au lieu du basculement instantané par défaut du navigateur.
  document.querySelectorAll("details").forEach(function (details) {
    var summary = details.querySelector("summary");
    var panel = details.querySelector(".panel") || (function () {
      // FAQ : tout ce qui suit <summary> sert de panneau
      var wrap = document.createElement("div");
      wrap.className = "panel";
      while (summary.nextSibling) wrap.appendChild(summary.nextSibling);
      details.appendChild(wrap);
      return wrap;
    })();
    if (reduceMotion) return;
    summary.addEventListener("click", function (e) {
      e.preventDefault();
      var isOpen = details.hasAttribute("open");
      if (isOpen) {
        var h = panel.scrollHeight;
        panel.style.height = h + "px";
        requestAnimationFrame(function () {
          panel.style.height = "0px";
        });
        panel.addEventListener("transitionend", function handler() {
          details.removeAttribute("open");
          panel.style.height = "";
          panel.removeEventListener("transitionend", handler);
        });
      } else {
        details.setAttribute("open", "");
        var target = panel.scrollHeight;
        panel.style.height = "0px";
        requestAnimationFrame(function () {
          panel.style.height = target + "px";
        });
        panel.addEventListener("transitionend", function handler() {
          panel.style.height = "";
          panel.removeEventListener("transitionend", handler);
        });
      }
    });
  });

  // Bandeau cookies (RGPD) — consentement stocké localement, aucun cookie tiers
  // n'est déposé avant acceptation explicite.
  function loadAnalytics() {
    var domain = window.__VITALIS_ANALYTICS__;
    if (!domain || document.querySelector("script[data-analytics]")) return;
    var s = document.createElement("script");
    s.defer = true;
    s.setAttribute("data-domain", domain);
    s.setAttribute("data-analytics", "1");
    s.src = "https://plausible.io/js/script.js";
    document.head.appendChild(s);
  }

  var banner = document.querySelector("[data-cookie-banner]");
  var storedConsent = null;
  try { storedConsent = localStorage.getItem("vitalis_cookie_consent"); } catch (err) {}
  if (storedConsent === "accepted") loadAnalytics();

  if (banner) {
    if (!storedConsent) banner.hidden = false;
    var accept = banner.querySelector("[data-cookie-accept]");
    var decline = banner.querySelector("[data-cookie-decline]");
    function closeBanner(value) {
      try { localStorage.setItem("vitalis_cookie_consent", value); } catch (err) {}
      banner.hidden = true;
      if (value === "accepted") loadAnalytics();
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
