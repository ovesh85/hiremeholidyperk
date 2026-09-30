/* Hire Me Holiday Parks — shared behaviour (no dependencies besides Lucide icons) */
(function () {
  "use strict";

  // Icons
  if (window.lucide) window.lucide.createIcons();

  // Header: compact + solid on scroll
  var header = document.querySelector(".site-header");
  function onScroll() { if (header) header.classList.toggle("is-scrolled", window.scrollY > 16); }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Mobile drawer
  var drawer = document.getElementById("mobile-menu");
  var openBtn = document.querySelector("[data-drawer-open]");
  var lastFocus = null;
  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle("is-open", open);
    drawer.setAttribute("aria-hidden", String(!open));
    document.body.classList.toggle("no-scroll", open);
    if (openBtn) openBtn.setAttribute("aria-expanded", String(open));
    drawer.querySelectorAll("a, button").forEach(function (el) { el.tabIndex = open ? 0 : -1; });
    if (open) { lastFocus = document.activeElement; drawer.querySelector("[data-drawer-close]").focus(); }
    else if (lastFocus) lastFocus.focus();
  }
  if (drawer) {
    setDrawer(false);
    openBtn && openBtn.addEventListener("click", function () { setDrawer(true); });
    drawer.querySelectorAll("[data-drawer-close]").forEach(function (el) { el.addEventListener("click", function () { setDrawer(false); }); });
    drawer.querySelectorAll("nav a").forEach(function (a) { a.addEventListener("click", function () { setDrawer(false); }); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && drawer.classList.contains("is-open")) setDrawer(false); });
  }

  // Simple form validation: fields with [required]; emails checked by pattern.
  // A form with [data-success] hides itself and reveals the element with that id.
  var EMAIL = /^\S+@\S+\.\S+$/;
  function showError(field, msg) {
    field.classList.add("is-invalid");
    field.setAttribute("aria-invalid", "true");
    var id = field.id + "-error";
    var el = document.getElementById(id);
    if (!el) { el = document.createElement("p"); el.id = id; el.className = "error-text"; (field.closest(".field-wrap") || field).insertAdjacentElement("afterend", el); }
    el.textContent = msg;
    field.setAttribute("aria-describedby", id);
  }
  function clearError(field) {
    field.classList.remove("is-invalid");
    field.removeAttribute("aria-invalid");
    var el = document.getElementById(field.id + "-error");
    if (el) el.remove();
  }
  document.querySelectorAll("form[data-validate]").forEach(function (form) {
    form.setAttribute("novalidate", "");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var firstBad = null;
      form.querySelectorAll("[required]").forEach(function (f) {
        clearError(f);
        var v = (f.type === "checkbox") ? f.checked : f.value.trim();
        var label = f.getAttribute("data-label") || "This field";
        if (!v) { showError(f, label + " is required."); firstBad = firstBad || f; }
        else if (f.type === "email" && !EMAIL.test(f.value)) { showError(f, "Enter an email address like name@example.com."); firstBad = firstBad || f; }
        else if (f.dataset.match) {
          var other = document.getElementById(f.dataset.match);
          if (other && other.value !== f.value) { showError(f, "Passwords don't match."); firstBad = firstBad || f; }
        }
      });
      if (firstBad) { firstBad.focus(); return; }
      // TODO: send the form data to the server here.
      var successId = form.getAttribute("data-success");
      if (successId) {
        var s = document.getElementById(successId);
        var email = form.querySelector("input[type=email]");
        var freq = form.querySelector("input[name=frequency]:checked");
        if (s) {
          s.querySelectorAll("[data-fill=email]").forEach(function (n) { n.textContent = email ? email.value : ""; });
          s.querySelectorAll("[data-fill=frequency]").forEach(function (n) { n.textContent = freq ? freq.value.toLowerCase() : ""; });
          form.hidden = true; s.hidden = false; s.focus();
        }
      }
    });
  });

  // Job search panels submit to jobs.html with query params
  document.querySelectorAll("form[data-job-search]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var p = new URLSearchParams();
      new FormData(form).forEach(function (v, k) { if (String(v).trim()) p.append(k, String(v).trim()); });
      var qs = p.toString();
      window.location.href = "jobs.html" + (qs ? "?" + qs : "");
    });
  });

  // Jobs page: prefill from URL and filter listed jobs client-side (replace with server search)
  var list = document.querySelector("[data-job-results]");
  if (list) {
    var params = new URLSearchParams(window.location.search);
    var form = document.querySelector("form[data-job-filter]");
    ["keywords", "location", "category"].forEach(function (k) {
      var el = form && form.elements[k];
      if (el && params.get(k)) el.value = params.get(k);
    });
    var state = params.get("state");
    if (state && form) { var box = form.querySelector('input[name=state][value="' + state + '"]'); if (box) box.checked = true; }

    function apply() {
      var kw = (form.elements.keywords.value || "").toLowerCase();
      var loc = (form.elements.location.value || "").toLowerCase();
      var cat = form.elements.category.value;
      var types = [].slice.call(form.querySelectorAll("input[name=type]:checked")).map(function (i) { return i.value; });
      var states = [].slice.call(form.querySelectorAll("input[name=state]:checked")).map(function (i) { return i.value; });
      var shown = 0;
      list.querySelectorAll(".job-row").forEach(function (row) {
        var d = row.dataset;
        var ok = (!kw || (d.title + " " + d.category).toLowerCase().indexOf(kw) > -1)
          && (!loc || (d.location + " " + d.state + " " + d.stateName).toLowerCase().indexOf(loc) > -1)
          && (!cat || d.category === cat)
          && (!types.length || types.indexOf(d.type) > -1)
          && (!states.length || states.indexOf(d.state) > -1);
        row.hidden = !ok; if (ok) shown++;
      });
      var count = document.querySelector("[data-result-count]");
      if (count) count.textContent = shown + (shown === 1 ? " job" : " jobs");
      var empty = document.querySelector("[data-empty]");
      if (empty) empty.hidden = shown > 0;
      list.hidden = shown === 0;
    }
    if (form) {
      form.addEventListener("submit", function (e) { e.preventDefault(); apply(); });
      form.addEventListener("change", apply);
      var reset = form.querySelector("[data-reset]");
      reset && reset.addEventListener("click", function () { setTimeout(apply, 0); });
    }
    apply();
  }

  // Filter toggle (mobile)
  var ft = document.querySelector("[data-filter-toggle]");
  if (ft) ft.addEventListener("click", function () {
    var f = document.getElementById(ft.getAttribute("aria-controls"));
    var open = !f.classList.contains("is-open");
    f.classList.toggle("is-open", open); ft.setAttribute("aria-expanded", String(open));
  });

  // Footer year
  document.querySelectorAll("[data-year]").forEach(function (n) { n.textContent = new Date().getFullYear(); });
})();
