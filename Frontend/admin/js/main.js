/* =========================================================
   main.js -- helper bersama untuk seluruh halaman admin.
   Menangani: token JWT, pemanggilan API, sidebar, notifikasi.
   ========================================================= */

const API_BASE = "/api";

// ---------------- Token & Auth ----------------
function getToken() {
  return localStorage.getItem("admin_token");
}

function setSession(token, user) {
  localStorage.setItem("admin_token", token);
  localStorage.setItem("admin_user", JSON.stringify(user || {}));
}

function getUser() {
  try {
    return JSON.parse(localStorage.getItem("admin_user") || "{}");
  } catch {
    return {};
  }
}

function clearSession() {
  localStorage.removeItem("admin_token");
  localStorage.removeItem("admin_user");
}

/** Panggil di awal setiap halaman admin (selain login.html). */
function requireAuth() {
  if (!getToken()) {
    window.location.href = "login.html";
  }
}

async function logout() {
  try {
    await apiFetch("/logout", { method: "POST" });
  } catch (e) {
    /* abaikan error logout, tetap lanjut hapus session lokal */
  }
  clearSession();
  window.location.href = "login.html";
}

// ---------------- API helper ----------------
async function apiFetch(path, options = {}) {
  const headers = Object.assign(
    { "Content-Type": "application/json" },
    options.headers || {}
  );

  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  // Jika body FormData, jangan set Content-Type (browser yang atur boundary)
  if (options.body instanceof FormData) delete headers["Content-Type"];

  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (response.status === 401) {
    clearSession();
    window.location.href = "login.html";
    throw new Error("Sesi berakhir, silakan login kembali.");
  }

  let data = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    throw new Error((data && (data.error || data.message)) || `HTTP ${response.status}`);
  }

  return data;
}

// ---------------- Sidebar ----------------
function renderSidebar(active) {
  const el = document.getElementById("sidebar");
  if (!el) return;

  const user = getUser();
  const items = [
    { key: "dashboard", label: "Dashboard", href: "dashboard.html", icon: "▦" },
    { key: "profiles", label: "Profil", href: "profiles.html", icon: "◐" },
    { key: "skills", label: "Skill", href: "skills.html", icon: "◆" },
    { key: "experience", label: "Pengalaman", href: "experience.html", icon: "▤" },
    { key: "projects", label: "Proyek", href: "projects.html", icon: "▢" },
    { key: "contacts", label: "Pesan Kontak", href: "contacts.html", icon: "✉" },
  ];

  el.innerHTML = `
    <div class="sidebar__brand">Admin<span>Panel</span></div>
    <nav class="sidebar__nav">
      ${items
        .map(
          (item) => `
        <a href="${item.href}" class="sidebar__link ${item.key === active ? "active" : ""}">
          <span class="sidebar__icon">${item.icon}</span> ${item.label}
        </a>`
        )
        .join("")}
    </nav>
    <div class="sidebar__footer">
      <div class="sidebar__user">${escapeHtml(user.username || "Admin")}</div>
      <button class="btn btn--ghost btn--sm" id="logout-btn">Logout</button>
    </div>
  `;

  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) logoutBtn.addEventListener("click", logout);
}

// ---------------- Toast / notifikasi ----------------
function showToast(message, type = "success") {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    document.body.appendChild(container);
  }
  const toast = document.createElement("div");
  toast.className = `toast toast--${type}`;
  toast.textContent = message;
  container.appendChild(toast);

  setTimeout(() => toast.classList.add("toast--show"), 10);
  setTimeout(() => {
    toast.classList.remove("toast--show");
    setTimeout(() => toast.remove(), 300);
  }, 3200);
}

// ---------------- Util ----------------
function escapeHtml(text) {
  if (text === null || text === undefined) return "";
  const map = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" };
  return String(text).replace(/[&<>"']/g, (m) => map[m]);
}

function confirmDelete(message = "Yakin ingin menghapus data ini?") {
  return window.confirm(message);
}
