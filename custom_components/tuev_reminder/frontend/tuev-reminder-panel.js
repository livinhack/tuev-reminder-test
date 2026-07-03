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

  _statusLabel(status) {
    if (status === "valid") return "gültig";
    if (status === "due") return "fällig";
    if (status === "expired") return "abgelaufen";
    return status || "unbekannt";
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

    return `
      <div class="vehicle-list">
        ${this._vehicles.map((vehicle) => `
          <article class="vehicle-card">
            <div>
              <h3>${this._escape(vehicle.vehicle_name || vehicle.title || "Fahrzeug")}</h3>
              <p class="plate">${this._escape(vehicle.plate_display || vehicle.plate || "—")}</p>
            </div>
            <dl>
              <div><dt>HU</dt><dd>${this._escape(String(vehicle.month || "--")).padStart(2, "0")}/${this._escape(String(vehicle.year || "----"))}</dd></div>
              <div><dt>Status</dt><dd>${this._escape(this._statusLabel(vehicle.status))}</dd></div>
              <div><dt>Typ</dt><dd>${this._escape(vehicle.plate_kind || "standard")}</dd></div>
            </dl>
          </article>
        `).join("")}
      </div>
    `;
  }

  _escape(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  _render() {
    if (!this.shadowRoot) {
      return;
    }

    const apiVersion = this._metadata?.api_version ?? "—";
    const writeApi = this._metadata?.write_api === true ? "aktiv" : "read-only";
    const vehicleCount = this._vehicles.length;

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
          max-width: 1040px;
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
        .subtitle, .muted {
          color: var(--secondary-text-color);
        }
        .grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
          gap: 16px;
          margin-bottom: 16px;
        }
        .card, .vehicle-card {
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
        .actions {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          margin: 16px 0;
        }
        button.action {
          border: 0;
          border-radius: 8px;
          padding: 10px 14px;
          background: var(--primary-color);
          color: var(--text-primary-color);
          cursor: pointer;
          font-weight: 500;
        }
        button.action[disabled] {
          cursor: not-allowed;
          opacity: 0.55;
        }
        .vehicle-list {
          display: grid;
          gap: 12px;
        }
        .vehicle-card {
          display: grid;
          grid-template-columns: minmax(0, 1fr) auto;
          gap: 16px;
          align-items: center;
        }
        .vehicle-card h3 {
          margin-bottom: 4px;
          font-size: 18px;
        }
        .plate {
          margin-bottom: 0;
          font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
          font-size: 20px;
          letter-spacing: 0.04em;
        }
        dl {
          display: grid;
          grid-template-columns: repeat(3, auto);
          gap: 14px;
          margin: 0;
        }
        dt {
          color: var(--secondary-text-color);
          font-size: 12px;
        }
        dd {
          margin: 2px 0 0;
          text-align: right;
        }
        .error {
          color: var(--error-color);
        }
        @media (max-width: 700px) {
          .page { padding: 16px; }
          .vehicle-card { grid-template-columns: 1fr; }
          dl { grid-template-columns: repeat(3, 1fr); }
          dd { text-align: left; }
        }
      </style>
      <main class="page">
        <header>
          <button class="menu" title="Menü öffnen" aria-label="Menü öffnen">☰</button>
          <div>
            <h1>TÜV Reminder</h1>
            <p class="subtitle">Manager-Shell für die spätere komfortable Entitäten-Erstellung. Keine Card-Funktionen, keine Dashboard-Vermischung.</p>
          </div>
        </header>

        <section class="grid" aria-label="Manager Status">
          <div class="card">
            <p class="muted">Fahrzeuge</p>
            <div class="metric">${vehicleCount}</div>
          </div>
          <div class="card">
            <p class="muted">Manager API</p>
            <div class="metric">v${apiVersion}</div>
          </div>
          <div class="card">
            <p class="muted">Schreibzugriff</p>
            <div class="metric">${writeApi}</div>
          </div>
        </section>

        <section class="card">
          <h2>Fahrzeuge</h2>
          <div class="actions">
            <button class="action" id="refresh" ${this._loading ? "disabled" : ""}>Aktualisieren</button>
            <button class="action" disabled title="Kommt mit der Create-API in einer späteren Reminder-Version">Neues Fahrzeug anlegen</button>
          </div>
          ${this._renderVehicles()}
        </section>
      </main>
    `;

    const refreshButton = this.shadowRoot.querySelector("#refresh");
    if (refreshButton) {
      refreshButton.addEventListener("click", () => this._refresh());
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
