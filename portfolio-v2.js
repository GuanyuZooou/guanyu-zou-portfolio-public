(() => {
  const menu = document.querySelector(".v2-menu-toggle");
  const nav = document.querySelector(".v2-nav");
  const narrow = window.matchMedia("(max-width: 700px)");

  function updateMenu(open) {
    menu.hidden = !narrow.matches;
    menu.setAttribute("aria-expanded", String(narrow.matches && open));
    nav.hidden = narrow.matches && !open;
  }

  if (menu && nav) {
    updateMenu(false);
    narrow.addEventListener("change", () => updateMenu(false));
    menu.addEventListener("click", () => updateMenu(nav.hidden));
    nav.addEventListener("click", (event) => {
      if (event.target.closest("a")) updateMenu(false);
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && narrow.matches && !nav.hidden) {
        updateMenu(false);
        menu.focus();
      }
    });
  }

  const groups = [...document.querySelectorAll("[data-project-group]")].map(section => {
    const toggle = section.querySelector(".v2-category-toggle");
    return {
      section,
      toggle,
      label: section.querySelector("[data-category-label]"),
      panel: document.getElementById(toggle.getAttribute("aria-controls")),
      mobileOpen: section.dataset.projectGroup === "research",
    };
  });
  if (!groups.length) return;

  function hashGroup(hash = location.hash) {
    const target = document.getElementById(hash.slice(1));
    return groups.find(({section}) => section.contains(target));
  }

  function updateCatalogue() {
    const focus = document.activeElement;
    for (const group of groups) {
      const {toggle, label, panel} = group;
      if (narrow.matches && panel.contains(focus)) group.mobileOpen = true;

      const expanded = !narrow.matches || group.mobileOpen;
      toggle.hidden = !narrow.matches;
      toggle.setAttribute("aria-expanded", String(expanded));
      label.hidden = narrow.matches;
      panel.hidden = !expanded;

      if (!narrow.matches && focus === toggle) {
        panel.querySelector("a")?.focus({preventScroll: true});
      }
    }
  }

  for (const group of groups) {
    group.toggle.addEventListener("click", () => {
      group.mobileOpen = !group.mobileOpen;
      if (!group.mobileOpen && group.panel.contains(document.activeElement)) group.toggle.focus();
      updateCatalogue();
    });
  }

  const initialGroup = hashGroup();
  if (initialGroup && narrow.matches) initialGroup.mobileOpen = true;
  updateCatalogue();
  narrow.addEventListener("change", () => {
    const group = hashGroup();
    if (group && narrow.matches) group.mobileOpen = true;
    updateCatalogue();
  });

  document.addEventListener("click", (event) => {
    const href = event.target.closest('a[href^="#"]')?.getAttribute("href");
    if (!narrow.matches || href !== location.hash) return;
    const group = hashGroup(href);
    if (group) {
      group.mobileOpen = true;
      updateCatalogue();
    }
  });

  window.addEventListener("hashchange", () => {
    const group = hashGroup();
    if (group && narrow.matches) {
      group.mobileOpen = true;
      updateCatalogue();
      const target = document.getElementById(location.hash.slice(1));
      target.scrollIntoView();
    }
  });
})();
