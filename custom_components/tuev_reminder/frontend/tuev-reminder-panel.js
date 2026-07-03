class TuevReminderPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._hass = null;
    this._narrow = false;
    this._panel = null;
    this._loading = false;
    this._loaded = false;
    this._error = null;
    this._metadata = null;
    this._vehicles = [];
    this._filter = "";
    this._statusFilter = "all";
    this._sort = "due";
  }

  set hass(hass) {
    this._hass = hass;
    this._loadOnce();
    this._render();
  }

  set narrow(narrow) {
    this._narrow = Boolean(narrow);
    this._render();
  }

  set panel(panel) {
    this._panel = panel;
    this._render();
  }

  connectedCallback() {
    this._render();
    this._loadOnce();
  }

  async _loadOnce() {
    if (!this._hass || this._loading || this._loaded) {
      return;
    }
    await this._refresh();
  }

  async _refresh() {
    if (!this._hass || this._loading) {
      return;
    }

    this._loading = true;
    this._error = null;
    this._render();

    try {
      const [metadata, listResult] = await Promise.all([
        this._hass.connection.sendMessagePromise({
          type: "tuev_reminder/manager/metadata",
        }),
        this._hass.connection.sendMessagePromise({
          type: "tuev_reminder/manager/vehicles/list",
        }),
      ]);
      this._metadata = metadata;
      this._vehicles = Array.isArray(listResult?.vehicles) ? listResult.vehicles : [];
      this._loaded = true;
    } catch (err) {
      this._error = err?.message || String(err);
    } finally {
      this._loading = false;
      this._render();
    }
  }

  _escape(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  _statusLabel(status) {
    if (status === "valid") return "gültig";
    if (status === "due") return "fällig";
    if (status === "expired") return "abgelaufen";
    return status || "unbekannt";
  }

  _statusClass(status) {
    if (["valid", "due", "expired"].includes(status)) return status;
    return "unknown";
  }

  _kindLabel(kind) {
    const options = this._metadata?.plate_kinds || [];
    return options.find((option) => option.value === kind)?.label || kind || "Standard";
  }

  _formatLabel(format) {
    const options = this._metadata?.plate_formats || [];
    return options.find((option) => option.value === format)?.label || format || "Einzeilig";
  }

  _monthYear(vehicle) {
    const month = String(vehicle.month || "--").padStart(2, "0");
    const year = String(vehicle.year || "----");
    return `${month}/${year}`;
  }

  _dateLabel(value) {
    return value ? String(value) : "—";
  }

  _statusCounts() {
    return this._vehicles.reduce((counts, vehicle) => {
      const status = vehicle.status || "unknown";
      counts[status] = (counts[status] || 0) + 1;
      return counts;
    }, {});
  }

  _visibleVehicles() {
    const filter = this._filter.trim().toLowerCase();
    const vehicles = this._vehicles.filter((vehicle) => {
      if (this._statusFilter !== "all" && vehicle.status !== this._statusFilter) {
        return false;
      }
      if (!filter) {
        return true;
      }
      return [
        vehicle.vehicle_name,
        vehicle.title,
        vehicle.plate_display,
        vehicle.plate,
        vehicle.entity_id,
        vehicle.plate_kind,
        vehicle.plate_format,
      ]
        .filter(Boolean)
        .some((value) => String(value).toLowerCase().includes(filter));
    });

    return vehicles.sort((a, b) => {
      if (this._sort === "name") {
        return String(a.vehicle_name || a.title || "").localeCompare(String(b.vehicle_name || b.title || ""), "de", { sensitivity: "base" });
      }
      if (this._sort === "status") {
        const order = { expired: 0, due: 1, valid: 2 };
        return (order[a.status] ?? 9) - (order[b.status] ?? 9) || String(a.due_date || "").localeCompare(String(b.due_date || ""));
      }
      return String(a.due_date || "9999-99-99").localeCompare(String(b.due_date || "9999-99-99"));
    });
  }

  _platePreview(vehicle) {
    const text = this._escape(vehicle.plate_display || vehicle.plate || "—");
    const green = vehicle.plate_color_mode === "green";
    const seasonal = vehicle.seasonal;
    return `
      <span class="plate-preview ${green ? "plate-preview-green" : ""}" title="Kennzeichenvorschau">
        <span class="plate-eu">D</span>
        <span class="plate-text">${text}</span>
        ${seasonal ? `<span class="plate-season">${this._escape(vehicle.season_start_month)}–${this._escape(vehicle.season_end_month)}</span>` : ""}
      </span>
    `;
  }

  _vehicleMeta(vehicle) {
    const tags = [this._formatLabel(vehicle.plate_format), this._kindLabel(vehicle.plate_kind)];
    if (vehicle.seasonal) {
      tags.push(`Saison ${vehicle.season_start_month}–${vehicle.season_end_month}`);
    }
    if (vehicle.change_plate_enabled) {
      tags.push("Wechselkennzeichen");
    }
    return tags.filter(Boolean).map((tag) => `<span class="tag">${this._escape(tag)}</span>`).join("");
  }

  _renderVehicles() {
    if (this._loading && !this._loaded) {
      return `<p class="state muted">Manager-Daten werden geladen …</p>`;
    }

    if (this._error) {
      return `<p class="state error">Manager-API nicht erreichbar: ${this._escape(this._error)}</p>`;
    }

    if (!this._vehicles.length) {
      return `<p class="state muted">Noch keine TÜV-Reminder-Fahrzeuge gefunden.</p>`;
    }

    const vehicles = this._visibleVehicles();
    if (!vehicles.length) {
      return `<p class="state muted">Keine Fahrzeuge passen zum aktuellen Filter.</p>`;
    }

    return `
      <div class="list-shell">
        <table class="manager-table">
          <thead>
            <tr>
              <th class="col-name">Name</th>
              <th>Status</th>
              <th>HU</th>
              <th>Reminder</th>
              <th>Typ</th>
              <th class="col-preview">Vorschau</th>
              <th class="col-menu" aria-label="Menü"></th>
            </tr>
          </thead>
          <tbody>
            ${vehicles.map((vehicle) => `
              <tr>
                <td class="name-cell">
                  <div class="vehicle-title">${this._escape(vehicle.vehicle_name || vehicle.title || "Fahrzeug")}</div>
                  <div class="vehicle-sub">${this._escape(vehicle.entity_id || "Keine Sensor-Entity")}</div>
                </td>
                <td><span class="status-pill status-${this._escape(this._statusClass(vehicle.status))}">${this._escape(this._statusLabel(vehicle.status))}</span></td>
                <td>
                  <div class="main-value">${this._escape(this._monthYear(vehicle))}</div>
                  <div class="sub-value">${this._escape(this._dateLabel(vehicle.due_date))}</div>
                </td>
                <td>
                  <div class="main-value">${this._escape(this._dateLabel(vehicle.reminder_date))}</div>
                  <div class="sub-value">Ablauf ${this._escape(this._dateLabel(vehicle.expired_date))}</div>
                </td>
                <td><div class="tag-row">${this._vehicleMeta(vehicle)}</div></td>
                <td class="preview-cell">${this._platePreview(vehicle)}</td>
                <td class="menu-cell"><button class="row-menu" disabled title="Bearbeiten kommt mit der Create-/Update-Strecke" aria-label="Zeilenmenü">⋮</button></td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    `;
  }

  _render() {
    if (!this.shadowRoot) {
      return;
    }

    const apiVersion = this._metadata?.api_version ?? "—";
    const writeApi = this._metadata?.write_api === true ? "aktiv" : "read-only";
    const vehicleCount = this._vehicles.length;
    const counts = this._statusCounts();
    const visibleCount = this._visibleVehicles().length;

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          min-height: 100%;
          box-sizing: border-box;
          color: var(--primary-text-color);
          background: var(--primary-background-color);
          font-family: var(--paper-font-body1_-_font-family, Roboto, Arial, sans-serif);
        }
        .page {
          min-height: 100%;
          background: var(--primary-background-color);
        }
        .topbar {
          height: 48px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 16px;
          padding: 0 16px;
          border-bottom: 1px solid var(--divider-color);
          background: var(--app-header-background-color, var(--primary-background-color));
        }
        .title-wrap {
          display: flex;
          align-items: center;
          min-width: 0;
          gap: 12px;
        }
        .menu {
          display: ${this._narrow ? "inline-flex" : "none"};
          align-items: center;
          justify-content: center;
          width: 40px;
          height: 40px;
          border: 0;
          border-radius: 50%;
          color: var(--primary-text-color);
          background: transparent;
          cursor: pointer;
        }
        h1 {
          margin: 0;
          font-size: 20px;
          line-height: 1;
          font-weight: 500;
          white-space: nowrap;
        }
        .version {
          color: var(--secondary-text-color);
          font-size: 12px;
          white-space: nowrap;
        }
        .toolbar {
          display: grid;
          grid-template-columns: minmax(240px, 1fr) auto auto auto;
          gap: 8px;
          padding: 10px 16px;
          border-bottom: 1px solid var(--divider-color);
          background: var(--secondary-background-color);
        }
        .search-wrap {
          position: relative;
          min-width: 0;
        }
        .search-icon {
          position: absolute;
          left: 12px;
          top: 50%;
          transform: translateY(-50%);
          color: var(--secondary-text-color);
          pointer-events: none;
        }
        input, select, button.action {
          height: 40px;
          box-sizing: border-box;
          border-radius: 4px;
          font: inherit;
        }
        input, select {
          width: 100%;
          border: 1px solid transparent;
          background: var(--card-background-color);
          color: var(--primary-text-color);
        }
        input[type="search"] {
          padding: 0 12px 0 40px;
        }
        select {
          min-width: 160px;
          padding: 0 28px 0 10px;
        }
        button.action {
          border: 0;
          padding: 0 14px;
          background: var(--primary-color);
          color: var(--text-primary-color);
          font-weight: 500;
          cursor: pointer;
          white-space: nowrap;
        }
        button.action[disabled] {
          opacity: 0.52;
          cursor: not-allowed;
        }
        .summary-strip {
          display: flex;
          flex-wrap: wrap;
          gap: 16px;
          padding: 10px 16px;
          color: var(--secondary-text-color);
          font-size: 13px;
          border-bottom: 1px solid var(--divider-color);
        }
        .summary-strip strong {
          color: var(--primary-text-color);
          font-weight: 500;
        }
        .content {
          padding: 0;
        }
        .list-shell {
          overflow-x: auto;
        }
        .manager-table {
          width: 100%;
          min-width: 1040px;
          border-collapse: collapse;
        }
        th, td {
          padding: 10px 14px;
          text-align: left;
          vertical-align: middle;
          border-bottom: 1px solid var(--divider-color);
        }
        th {
          height: 32px;
          color: var(--secondary-text-color);
          font-size: 12px;
          font-weight: 600;
        }
        tbody tr:hover {
          background: var(--secondary-background-color);
        }
        .col-name {
          width: 30%;
        }
        .col-preview {
          width: 220px;
          text-align: right;
        }
        .col-menu {
          width: 40px;
        }
        .vehicle-title {
          font-weight: 600;
          line-height: 1.25;
        }
        .vehicle-sub, .sub-value, .muted {
          color: var(--secondary-text-color);
          font-size: 12px;
          line-height: 1.35;
        }
        .main-value {
          font-weight: 500;
          line-height: 1.25;
        }
        .status-pill {
          display: inline-flex;
          align-items: center;
          border-radius: 999px;
          padding: 3px 9px;
          border: 1px solid var(--divider-color);
          font-size: 12px;
          font-weight: 500;
          background: var(--card-background-color);
        }
        .status-expired {
          color: var(--error-color);
        }
        .status-due {
          color: var(--warning-color, var(--state-icon-active-color));
        }
        .status-valid {
          color: var(--success-color, var(--primary-color));
        }
        .tag-row {
          display: flex;
          flex-wrap: wrap;
          gap: 5px;
        }
        .tag {
          display: inline-flex;
          align-items: center;
          min-height: 20px;
          border-radius: 999px;
          padding: 1px 7px;
          border: 1px solid var(--divider-color);
          color: var(--secondary-text-color);
          font-size: 11px;
          white-space: nowrap;
        }
        .preview-cell {
          text-align: right;
        }
        .plate-preview {
          display: inline-flex;
          align-items: stretch;
          max-width: 210px;
          min-width: 132px;
          height: 34px;
          box-sizing: border-box;
          border: 2px solid #1b1b1b;
          border-radius: 5px;
          overflow: hidden;
          background: #f7f7f1;
          color: #111;
          box-shadow: inset 0 0 0 1px rgba(0,0,0,0.16);
          font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        }
        .plate-preview-green {
          color: #0a7d28;
          border-color: #0a7d28;
        }
        .plate-eu {
          display: inline-flex;
          align-items: flex-end;
          justify-content: center;
          width: 20px;
          padding-bottom: 3px;
          box-sizing: border-box;
          background: #17479e;
          color: #fff;
          font-size: 9px;
          font-weight: 700;
        }
        .plate-text {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          flex: 1 1 auto;
          padding: 0 8px;
          font-size: 17px;
          font-weight: 800;
          letter-spacing: 0.02em;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .plate-season {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          min-width: 26px;
          border-left: 1px solid rgba(0,0,0,0.25);
          font-size: 9px;
          font-weight: 700;
          writing-mode: vertical-rl;
          transform: rotate(180deg);
        }
        .row-menu {
          width: 32px;
          height: 32px;
          border: 0;
          border-radius: 50%;
          background: transparent;
          color: var(--secondary-text-color);
          font-size: 22px;
          line-height: 1;
          cursor: not-allowed;
        }
        .state {
          padding: 24px 16px;
        }
        .error {
          color: var(--error-color);
        }
        @media (max-width: 860px) {
          .toolbar {
            grid-template-columns: 1fr;
          }
          select, button.action {
            width: 100%;
          }
          .summary-strip {
            gap: 8px 14px;
          }
        }
      </style>
      <main class="page">
        <header class="topbar">
          <div class="title-wrap">
            <button class="menu" title="Menü öffnen" aria-label="Menü öffnen">☰</button>
            <h1>TÜV Reminder</h1>
          </div>
          <div class="version">API v${this._escape(apiVersion)} · ${this._escape(writeApi)}</div>
        </header>

        <section class="toolbar" aria-label="Fahrzeugliste filtern und sortieren">
          <div class="search-wrap">
            <span class="search-icon">⌕</span>
            <input id="filter" type="search" placeholder="Search" value="${this._escape(this._filter)}">
          </div>
          <select id="status-filter" aria-label="Statusfilter">
            <option value="all" ${this._statusFilter === "all" ? "selected" : ""}>Alle Status</option>
            <option value="expired" ${this._statusFilter === "expired" ? "selected" : ""}>Abgelaufen</option>
            <option value="due" ${this._statusFilter === "due" ? "selected" : ""}>Fällig</option>
            <option value="valid" ${this._statusFilter === "valid" ? "selected" : ""}>Gültig</option>
          </select>
          <select id="sort" aria-label="Sortierung">
            <option value="due" ${this._sort === "due" ? "selected" : ""}>HU-Datum</option>
            <option value="status" ${this._sort === "status" ? "selected" : ""}>Status</option>
            <option value="name" ${this._sort === "name" ? "selected" : ""}>Name</option>
          </select>
          <button class="action" id="refresh" ${this._loading ? "disabled" : ""}>Aktualisieren</button>
        </section>

        <section class="summary-strip" aria-label="Manager Status">
          <span><strong>${vehicleCount}</strong> Fahrzeuge</span>
          <span><strong>${visibleCount}</strong> Treffer</span>
          <span><strong>${(counts.due || 0) + (counts.expired || 0)}</strong> fällig/abgelaufen</span>
          <span>Reminder-eigene Seite · keine Card-Funktionen · keine Dashboard-Vermischung</span>
        </section>

        <section class="content">
          ${this._renderVehicles()}
        </section>
      </main>
    `;

    const refreshButton = this.shadowRoot.querySelector("#refresh");
    if (refreshButton) {
      refreshButton.addEventListener("click", () => this._refresh());
    }

    const filterInput = this.shadowRoot.querySelector("#filter");
    if (filterInput) {
      filterInput.addEventListener("input", (event) => {
        this._filter = event.target.value;
        this._render();
      });
    }

    const statusFilter = this.shadowRoot.querySelector("#status-filter");
    if (statusFilter) {
      statusFilter.addEventListener("change", (event) => {
        this._statusFilter = event.target.value;
        this._render();
      });
    }

    const sortSelect = this.shadowRoot.querySelector("#sort");
    if (sortSelect) {
      sortSelect.addEventListener("change", (event) => {
        this._sort = event.target.value;
        this._render();
      });
    }

    const menuButton = this.shadowRoot.querySelector(".menu");
    if (menuButton) {
      menuButton.addEventListener("click", () => {
        this.dispatchEvent(new CustomEvent("hass-toggle-menu", { bubbles: true, composed: true }));
      });
    }
  }
}

if (!customElements.get("tuev-reminder-panel")) {
  customElements.define("tuev-reminder-panel", TuevReminderPanel);
}
