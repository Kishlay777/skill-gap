// Page routing is handled server-side by Flask (see app.py).
// This file wires up small client-side interactions: the mobile sidebar,
// modals on the Skills page, the Jobs search filter, and FAQ toggles.

document.addEventListener("DOMContentLoaded", () => {
  // ---- Mobile sidebar toggle -------------------------------------------
  const hamb = document.getElementById("hamb");
  const sidebar = document.getElementById("sidebar");
  const overlay = document.getElementById("sidebarOverlay");

  function closeSidebar() {
    sidebar && sidebar.classList.remove("open");
    overlay && overlay.classList.remove("show");
  }

  if (hamb && sidebar) {
    hamb.addEventListener("click", () => {
      sidebar.classList.toggle("open");
      overlay && overlay.classList.toggle("show");
    });
  }
  if (overlay) overlay.addEventListener("click", closeSidebar);
  window.addEventListener("resize", () => {
    if (window.innerWidth > 1000) closeSidebar();
  });

  // ---- Auto-dismiss flash messages --------------------------------------
  document.querySelectorAll(".flash").forEach((el) => {
    setTimeout(() => {
      el.style.transition = "opacity .4s ease";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 400);
    }, 4000);
  });

  // ---- Jobs page: simple client-side search filter ----------------------
  const jobSearch = document.getElementById("jobSearch");
  if (jobSearch) {
    jobSearch.addEventListener("input", () => {
      const q = jobSearch.value.trim().toLowerCase();
      document.querySelectorAll("[data-job-card]").forEach((card) => {
        const text = card.textContent.toLowerCase();
        card.style.display = text.includes(q) ? "" : "none";
      });
    });
  }

  // ---- Support page: FAQ expand/collapse ---------------------------------
  document.querySelectorAll(".faq-row").forEach((row) => {
    row.addEventListener("click", () => row.classList.toggle("open"));
  });

  // ---- Close a modal when clicking its dark overlay ----------------------
  document.querySelectorAll(".modal-overlay").forEach((overlayEl) => {
    overlayEl.addEventListener("click", (e) => {
      if (e.target === overlayEl) overlayEl.classList.remove("show");
    });
  });

  // ---- Escape key closes any open modal ----------------------------------
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      document.querySelectorAll(".modal-overlay.show").forEach((el) => el.classList.remove("show"));
    }
  });
});

function openModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.add("show");
}

function closeModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.remove("show");
}

function openAssessModal(name, score) {
  document.getElementById("assessSkillName").textContent = name;
  document.getElementById("assessSkillNameInput").value = name;
  document.getElementById("assessScoreInput").value = score;
  openModal("assessModal");
}
