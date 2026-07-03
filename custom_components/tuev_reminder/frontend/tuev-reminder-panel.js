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

  _renderVehicles() {
    if (this._loading && !this._loaded) {
      return `<p class="muted">Manager-Daten werden geladen …</p>`;
    }

    if (this._error) {
      return `<p class="error">Manager-API nicht erreichbar: ${this._escape(this._error)}</p>`;
    }

    if (!this._vehicles.length) {
      return `<p class="muted">Noch keine TÜV-Reminder-Fahrzeuge gefunden.</p>`;
    }

    const vehicles = this._visibleVehicles();
    if (!vehicles.length) {
      return `<p class="muted">Keine Fahrzeuge passen zum aktuellen Filter.</p>`;
    }

    return `
      <div class="table-wrap">
        <table class="vehicle-table">
          <thead>
            <tr>
              <th>Fahrzeug</th>
              <th>Kennzeichen</th>
              <th>HU</th>
              <th>Status</th>
              <th>Reminder</th>
              <th>Typ</th>
              <th>Entity</th>
            </tr>
          </thead>
          <tbody>
            ${vehicles.map((vehicle) => `
              <tr>
                <td>
                  <strong>${this._escape(vehicle.vehicle_name || vehicle.title || "Fahrzeug")}</strong>
                  <small>${this._escape(this._formatLabel(vehicle.plate_format))}</small>
                </td>
                <td><span class="plate">${this._escape(vehicle.plate_display || vehicle.plate || "—")}</span></td>
                <td>
                  <span>${this._escape(this._monthYear(vehicle))}</span>
                  <small>${this._escape(this._dateLabel(vehicle.due_date))}</small>
                </td>
                <td><span class="status status-${this._escape(vehicle.status || "unknown")}">${this._escape(this._statusLabel(vehicle.status))}</span></td>
                <td>
                  <span>${this._escape(this._dateLabel(vehicle.reminder_date))}</span>
                  <small>Ablauf: ${this._escape(this._dateLabel(vehicle.expired_date))}</small>
                </td>
                <td>
                  <span>${this._escape(this._kindLabel(vehicle.plate_kind))}</span>
                  ${vehicle.seasonal ? `<small>Saison ${this._escape(vehicle.season_start_month)}–${this._escape(vehicle.season_end_month)}</small>` : ""}
                  ${vehicle.change_plate_enabled ? `<small>Wechselkennzeichen</small>` : ""}
                </td>
                <td><code>${this._escape(vehicle.entity_id || "—")}</code></td>
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
          font-family: var(--paper-font-body1_-_font-family, Roboto, sans-serif);
        }
        .page {
          max-width: 1180px;
          margin: 0 auto;
          padding: 24px;
        }
        header {
          display: flex;
          align-items: center;
          gap: 16px;
          margin-bottom: 20px;
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
        h1, h2, h3, p {
          margin-top: 0;
        }
        h1 {
          margin-bottom: 4px;
          font-size: 28px;
          font-weight: 500;
        }
        .subtitle, .muted, small {
          color: var(--secondary-text-color);
        }
        .grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
          gap: 16px;
          margin-bottom: 16px;
        }
        .card {
          border-radius: 12px;
          background: var(--card-background-color);
          box-shadow: var(--ha-card-box-shadow, none);
          border: 1px solid var(--divider-color);
          padding: 16px;
        }
        .metric {
          font-size: 30px;
          line-height: 1.2;
          font-weight: 500;
        }
        .actions, .filters {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          margin: 16px 0;
          align-items: center;
        }
        button.action, select, input {
          border-radius: 8px;
          padding: 10px 12px;
          font: inherit;
        }
        button.action {
          border: 0;
          background: var(--primary-color);
          color: var(--text-primary-color);
          cursor: pointer;
          font-weight: 500;
        }
        button.action[disabled] {
          cursor: not-allowed;
          opacity: 0.55;
        }
        input, select {
          min-height: 40px;
          border: 1px solid var(--divider-color);
          background: var(--card-background-color);
          color: var(--primary-text-color);
        }
        input[type="search"] {
          min-width: min(360px, 100%);
          flex: 1 1 260px;
        }
        .table-wrap {
          overflow-x: auto;
          border: 1px solid var(--divider-color);
          border-radius: 12px;
        }
        .vehicle-table {
          width: 100%;
          border-collapse: collapse;
          min-width: 920px;
        }
        th, td {
          padding: 12px;
          text-align: left;
          vertical-align: top;
          border-bottom: 1px solid var(--divider-color);
        }
        th {
          color: var(--secondary-text-color);
          font-size: 12px;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.04em;
        }
        tbody tr:last-child td {
          border-bottom: 0;
        }
        td strong, td span, td code, td small {
          display: block;
        }
        .plate {
          font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
          font-size: 18px;
          letter-spacing: 0.04em;
          white-space: nowrap;
        }
        code {
          color: var(--secondary-text-color);
          font-size: 12px;
          word-break: break-all;
        }
        .status {
          display: inline-block;
          width: max-content;
          border-radius: 999px;
          padding: 3px 9px;
          border: 1px solid var(--divider-color);
          background: var(--secondary-background-color);
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
        .error {
          color: var(--error-color);
        }
        @media (max-width: 700px) {
          .page { padding: 16px; }
          .grid { grid-template-columns: 1fr 1fr; }
        }
      </style>
      <main class="page">
        <header>
          <button class="menu" title="Menü öffnen" aria-label="Menü öffnen">☰</button>
          <div>
            <h1>TÜV Reminder</h1>
            <p class="subtitle">Reminder-eigene Manager-Seite für Fahrzeug-/Entitäten-Verwaltung. Keine Card-Funktionen, keine Dashboard-Vermischung.</p>
          </div>
        </header>

        <section class="grid" aria-label="Manager Status">
          <div class="card">
            <p class="muted">Fahrzeuge</p>
            <div class="metric">${vehicleCount}</div>
          </div>
          <div class="card">
            <p class="muted">Gefiltert</p>
            <div class="metric">${visibleCount}</div>
          </div>
          <div class="card">
            <p class="muted">Fällig / abgelaufen</p>
            <div class="metric">${(counts.due || 0) + (counts.expired || 0)}</div>
          </div>
          <div class="card">
            <p class="muted">Manager API</p>
            <div class="metric">v${apiVersion}</div>
            <small>Schreibzugriff: ${writeApi}</small>
          </div>
        </section>

        <section class="card">
          <h2>Fahrzeuge</h2>
          <div class="actions">
            <button class="action" id="refresh" ${this._loading ? "disabled" : ""}>Aktualisieren</button>
            <button class="action" disabled title="Kommt mit der Create-API in einer späteren Reminder-Version">Neues Fahrzeug anlegen</button>
          </div>
          <div class="filters" aria-label="Fahrzeugliste filtern und sortieren">
            <input id="filter" type="search" placeholder="Suche nach Fahrzeug, Kennzeichen oder Entity" value="${this._escape(this._filter)}">
            <select id="status-filter" aria-label="Statusfilter">
              <option value="all" ${this._statusFilter === "all" ? "selected" : ""}>Alle Status</option>
              <option value="expired" ${this._statusFilter === "expired" ? "selected" : ""}>Nur abgelaufen</option>
              <option value="due" ${this._statusFilter === "due" ? "selected" : ""}>Nur fällig</option>
              <option value="valid" ${this._statusFilter === "valid" ? "selected" : ""}>Nur gültig</option>
            </select>
            <select id="sort" aria-label="Sortierung">
              <option value="due" ${this._sort === "due" ? "selected" : ""}>Sortierung: HU-Datum</option>
              <option value="status" ${this._sort === "status" ? "selected" : ""}>Sortierung: Status</option>
              <option value="name" ${this._sort === "name" ? "selected" : ""}>Sortierung: Name</option>
            </select>
          </div>
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
