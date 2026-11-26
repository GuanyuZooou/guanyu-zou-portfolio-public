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

  const filters = document.querySelector("[data-filters]");
  if (!filters) return;

  const buttons = [...filters.querySelectorAll("[data-category]")];
  const groups = [...document.querySelectorAll("[data-project-group]")];
  const status = document.querySelector("[data-filter-status]");

  function selectCategory(selected) {
    const category = selected.dataset.category;
    for (const button of buttons) button.setAttribute("aria-pressed", String(button === selected));
    for (const group of groups) group.hidden = category !== "all" && group.dataset.projectGroup !== category;
    const visible = groups.reduce((count, group) => count + (group.hidden ? 0 : group.querySelectorAll(".v2-project-row").length), 0);
    status.textContent = visible + " projects shown";
  }

  for (const button of buttons) button.addEventListener("click", () => selectCategory(button));
  filters.hidden = false;
  window.addEventListener("hashchange", () => {
    const target = document.getElementById(location.hash.slice(1));
    const group = target?.closest("[data-project-group]");
    if (group?.hidden) {
      selectCategory(buttons[0]);
      target.scrollIntoView();
    }
  });
})();
