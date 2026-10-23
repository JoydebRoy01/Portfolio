/* Portfolio interactions: mobile menu, active nav link, copy email,
   and a contact form that submits without reloading the page.
   Everything works without JavaScript too; this only improves it. */

(function () {
  "use strict";

  // ---------- Hero figure: fade it in as soon as the image has loaded ----------
  const figure = document.querySelector(".hero__figure");
  if (figure) {
    const show = () => requestAnimationFrame(() => figure.classList.add("is-ready"));
    if (figure.complete) show();
    else { figure.addEventListener("load", show, { once: true }); figure.addEventListener("error", show, { once: true }); }
  }

  // ---------- Header border on scroll ----------
  const header = document.querySelector("[data-header]");
  if (header) {
    const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // ---------- Mobile menu ----------
  const toggle = document.querySelector("[data-nav-toggle]");
  const nav = document.querySelector("[data-nav]");
  if (toggle && nav) {
    const label = toggle.querySelector(".nav-toggle__label");
    const setOpen = (open) => {
      toggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("is-open", open);
      if (header) header.classList.toggle("is-open", open);
      if (label) label.textContent = open ? "Close" : "Menu";
    };
    toggle.addEventListener("click", () => setOpen(toggle.getAttribute("aria-expanded") !== "true"));
    nav.addEventListener("click", (e) => { if (e.target.closest("a")) setOpen(false); });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && nav.classList.contains("is-open")) { setOpen(false); toggle.focus(); }
    });
    window.matchMedia("(min-width: 881px)").addEventListener("change", (mq) => { if (mq.matches) setOpen(false); });
  }

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  // ---------- Theme toggle (dark / light) ----------
  const themeBtn = document.querySelector("[data-theme-toggle]");
  const themeMeta = document.querySelector("[data-theme-color]");
  const syncThemeUi = () => {
    const theme = document.documentElement.getAttribute("data-theme");
    if (themeBtn) themeBtn.setAttribute("aria-label", theme === "dark" ? "Switch to light theme" : "Switch to dark theme");
    if (themeMeta) themeMeta.setAttribute("content", theme === "dark" ? "#0B0C13" : "#F5F4F7");
  };
  syncThemeUi();
  if (themeBtn) {
    themeBtn.addEventListener("click", () => {
      const next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      try { localStorage.setItem("theme", next); } catch (e) { /* private mode: theme just won't be remembered */ }
      syncThemeUi();
      document.dispatchEvent(new CustomEvent("themechange", { detail: next }));
    });
  }

  // ---------- Hero depth: layers move at different speeds with pointer and scroll ----------
  const hero = document.querySelector("[data-hero]");
  const layers = hero ? [...hero.querySelectorAll("[data-depth]")] : [];
  if (layers.length && !reduceMotion) {
    let mx = 0, my = 0, ticking = false;
    const update = () => {
      ticking = false;
      const scroll = Math.min(window.scrollY, window.innerHeight);
      layers.forEach((el) => {
        const d = parseFloat(el.dataset.depth);
        el.style.setProperty("--px", `${(mx * 30 * d).toFixed(1)}px`);
        el.style.setProperty("--py", `${(my * 20 * d + scroll * d * 0.6).toFixed(1)}px`);
      });
    };
    const request = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
    if (finePointer) {
      hero.addEventListener("pointermove", (e) => {
        mx = e.clientX / window.innerWidth - 0.5;
        my = e.clientY / window.innerHeight - 0.5;
        request();
      });
    }
    window.addEventListener("scroll", request, { passive: true });
  }

  // ---------- 3D reveal while scrolling ----------
  if (!reduceMotion && "IntersectionObserver" in window) {
    document.documentElement.classList.add("js-3d");
    const targets = document.querySelectorAll(
      ".section__head, .work-row, .mini-project, .service, .process__step, .principle, .quote, .faq__head, .faq__item, .cta__inner, " +
      ".timeline__item, .skills__head, .skills__group, .about__portrait, .about__text, .contact__intro, .contact__panel, " +
      ".footer-top > *, .case__visual, .case__layout, .case__next"
    );
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) { entry.target.classList.add("is-in"); io.unobserve(entry.target); }
      });
    }, { rootMargin: "0px 0px -10% 0px", threshold: 0.08 });
    targets.forEach((el) => {
      // Stagger items that sit in the same list
      const index = el.parentElement ? [...el.parentElement.children].indexOf(el) : 0;
      el.style.setProperty("--reveal-delay", `${Math.min(index, 5) * 0.08}s`);
      el.classList.add("reveal");
      io.observe(el);
    });
  }

  // ---------- Cards tilt toward the pointer (desktop only) ----------
  if (finePointer && !reduceMotion) {
    document.querySelectorAll(".work-row, .service, .process__step, .quote, .about__portrait img, .about__placeholder, .contact__panel").forEach((card) => {
      card.classList.add("tilt");
      const strength = card.classList.contains("work-row") ? 4 : card.classList.contains("contact__panel") ? 5 : 8;
      card.addEventListener("pointermove", (e) => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width;
        const y = (e.clientY - r.top) / r.height;
        card.style.setProperty("--mx", `${(x * 100).toFixed(1)}%`);
        card.style.setProperty("--my", `${(y * 100).toFixed(1)}%`);
        card.style.transform = `perspective(900px) rotateX(${((0.5 - y) * strength).toFixed(2)}deg) rotateY(${((x - 0.5) * strength).toFixed(2)}deg) translateZ(0)`;
      });
      card.addEventListener("pointerleave", () => { card.style.transform = ""; });
    });
  }

  // ---------- Highlight the nav link for the section in view ----------
  const navLinks = document.querySelectorAll("[data-nav-link]");
  const sections = [...navLinks]
    .map((a) => document.getElementById(a.dataset.navLink))
    .filter(Boolean);
  if (sections.length && "IntersectionObserver" in window) {
    const setActive = (id) => navLinks.forEach((a) => {
      const active = a.dataset.navLink === id;
      a.classList.toggle("is-active", active);
      if (active) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
    });
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => { if (entry.isIntersecting) setActive(entry.target.id); });
    }, { rootMargin: "-45% 0px -50% 0px" });
    sections.forEach((s) => observer.observe(s));
  }

  // ---------- Copy email ----------
  document.querySelectorAll("[data-copy]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const text = btn.dataset.copy;
      try {
        await navigator.clipboard.writeText(text);
        btn.textContent = "Copied";
        btn.classList.add("is-copied");
      } catch {
        btn.textContent = "Press Ctrl+C";
      }
      clearTimeout(btn._timer);
      btn._timer = setTimeout(() => { btn.textContent = "Copy"; btn.classList.remove("is-copied"); }, 2000);
    });
  });

  // ---------- Contact form ----------
  const form = document.querySelector("[data-contact-form]");
  if (!form) return;

  const submitBtn = form.querySelector("[data-submit]");
  const statusEl = form.querySelector("[data-form-status]");
  const success = document.querySelector("[data-form-success]");
  const successText = document.querySelector("[data-form-success-text]");
  const resetBtn = document.querySelector("[data-form-reset]");
  const submitLabel = submitBtn.textContent;

  const messages = {
    name: "Add your name so I know who to reply to.",
    emailMissing: "Add an email address so I can reply.",
    emailInvalid: "This email address looks incomplete. Check for a missing @ or domain.",
    message: "Write a short message. A couple of lines is enough.",
    messageShort: "This message is very short. Add a line about the role or project.",
  };

  // Link every input to its error text for screen readers.
  form.querySelectorAll("[data-field]").forEach((wrap) => {
    const input = wrap.querySelector("input, textarea");
    const err = wrap.querySelector("[data-error-for]");
    if (input && err) {
      input.setAttribute("aria-describedby", err.id);
      if (wrap.classList.contains("has-error")) input.setAttribute("aria-invalid", "true");
    }
  });

  function setError(name, text) {
    const wrap = form.querySelector(`[data-field="${name}"]`);
    if (!wrap) return;
    const input = wrap.querySelector("input, textarea");
    const err = wrap.querySelector("[data-error-for]");
    wrap.classList.toggle("has-error", Boolean(text));
    if (input) {
      if (text) input.setAttribute("aria-invalid", "true"); else input.removeAttribute("aria-invalid");
    }
    if (err) { err.textContent = text || ""; err.hidden = !text; }
  }

  function validateField(name) {
    const el = form.elements[name];
    if (!el) return true;
    const value = el.value.trim();
    let error = "";
    if (name === "name" && !value) error = messages.name;
    if (name === "email") {
      if (!value) error = messages.emailMissing;
      else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) error = messages.emailInvalid;
    }
    if (name === "message") {
      if (!value) error = messages.message;
      else if (value.length < 10) error = messages.messageShort;
    }
    setError(name, error);
    return !error;
  }

  // Check a field when the visitor leaves it, and clear errors as they fix them.
  ["name", "email", "message"].forEach((name) => {
    const el = form.elements[name];
    if (!el) return;
    el.addEventListener("blur", () => { if (el.value.trim()) validateField(name); });
    el.addEventListener("input", () => {
      if (el.closest(".field").classList.contains("has-error")) validateField(name);
    });
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    statusEl.textContent = "";

    const valid = ["name", "email", "message"].map(validateField).every(Boolean);
    if (!valid) {
      const firstBad = form.querySelector(".has-error input, .has-error textarea");
      if (firstBad) firstBad.focus();
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = "Sending…";

    try {
      const res = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { "X-Requested-With": "fetch" },
        credentials: "same-origin",
      });
      const data = await res.json().catch(() => ({}));

      if (res.ok && data.ok) {
        successText.textContent = data.message;
        form.hidden = true;
        success.hidden = false;
        success.focus();
        form.reset();
      } else if (data.errors) {
        Object.entries(data.errors).forEach(([field, errs]) => setError(field, errs.join(" ")));
        if (data.errors.__all__) statusEl.textContent = data.errors.__all__.join(" ");
        const firstBad = form.querySelector(".has-error input, .has-error textarea");
        if (firstBad) firstBad.focus();
      } else {
        throw new Error("Unexpected response");
      }
    } catch {
      const email = document.querySelector("[data-copy]")?.dataset.copy;
      statusEl.textContent = email
        ? `Your message wasn't sent because the connection failed. Try again, or email ${email} directly.`
        : "Your message wasn't sent because the connection failed. Check your connection and try again.";
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = submitLabel;
    }
  });

  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      success.hidden = true;
      form.hidden = false;
      form.elements.name?.focus();
    });
  }
})();
