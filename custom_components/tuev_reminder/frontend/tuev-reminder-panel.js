class TuevReminderPanel extends HTMLElement {
  // Sidebar Manager only: Create/Edit/Delete aktiv; Duplicate-Schutz · lokale Duplicate-Prüfung; Duplicate-Schutz; lokale Duplicate-Prüfung; frische Edit/Delete-Daten; Dirty-Guard; Responsive Tabelle; lokale Formularvalidierung auf Backend-Regeln abgestimmt; Mobile-Action-Sheet; nur Drei-Punkte-Menü öffnet Aktionen; sortierbare Spalten · First-Run-Leerzustand; sortierbare Spalten; First-Run-Leerzustand; mobile Kartenansicht; keine Card-Funktionen; status summary covers fällig/abgelaufen; list uses renderer-ready neutral plate slot until Card renderer is available; sort state stays in headers without extra visible UI; status chips carry counts without extra hit counter; visible topbar hides technical API status unless read-only; list uses one compact create action instead of top/bottom add rows
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
    this._sortKey = "hu";
    this._sortDirection = "asc";
    this._openMenuIndex = null;
    this._openMenuEntryId = null;
    this._view = "list";
    this._selectedVehicle = null;
    this._form = this._defaultForm();
    this._saving = false;
    this._deleting = false;
    this._formError = null;
    this._formInfo = null;
    this._flashMessage = null;
    this._flashTimer = null;
    this._openMenuIndex = null;
    this._openMenuEntryId = null;
    this._formSnapshot = null;
    this._discardPromptOpen = false;
    this._actionSheetVehicle = null;
    this._actionSheetOpenedAt = 0;
    this._actionSheetCloseGuardUntil = 0;
    this._rowActionLoadingEntryId = null;
    this._dialogFocusPending = null;
  }

  set hass(hass) {
    const firstHass = !this._hass;
    this._hass = hass;
    this._loadOnce();

    // Home Assistant assigns `hass` frequently as states change. Rebuilding an
    // open create/edit/delete dialog on every unrelated state update can steal
    // focus from inputs or close transient mobile UI. List rendering remains
    // live, but modal interactions render only from their own state changes.
    if (firstHass || !this._loaded || this._view === "list") {
      this._renderPreservingListUiState();
    }
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

  _defaultForm() {
    const now = new Date();
    return {
      vehicle_name: "",
      plate: "",
      month: String(now.getMonth() + 1),
      year: String(now.getFullYear()),
      interval: "2",
      reminder_offset_days: "7",
      plate_kind: "standard",
      plate_format: "single_line",
      plate_suffix_h: false,
      plate_suffix_e: false,
      season_start_month: "4",
      season_end_month: "10",
      change_plate_common_text: "",
      change_plate_vehicle_digit: "",
    };
  }

  _formKindFlags(kind = this._form.plate_kind) {
    return {
      seasonal: ["seasonal", "green_seasonal"].includes(kind),
      green: ["green", "green_seasonal"].includes(kind),
      change: kind === "change",
    };
  }

  _seasonDuration(startMonth, endMonth) {
    return ((Number(endMonth) - Number(startMonth) + 12) % 12) + 1;
  }

  _isValidSeasonRange(startMonth, endMonth) {
    const start = Number(startMonth);
    const end = Number(endMonth);
    if (!Number.isInteger(start) || !Number.isInteger(end)) return false;
    if (start < 1 || start > 12 || end < 1 || end > 12) return false;
    const duration = this._seasonDuration(start, end);
    return duration >= 2 && duration <= 11;
  }

  _scrubFormForKind(form = this._form) {
    const clean = { ...this._defaultForm(), ...(form || {}) };
    const flags = this._formKindFlags(clean.plate_kind);

    if (flags.change) {
      clean.plate = "";
      clean.plate_suffix_h = false;
      clean.plate_suffix_e = false;
      clean.change_plate_vehicle_digit = String(clean.change_plate_vehicle_digit || "")
        .replace(/\D/g, "")
        .slice(0, 1);
    } else {
      clean.change_plate_common_text = "";
      clean.change_plate_vehicle_digit = "";
    }

    if (flags.green) {
      clean.plate_suffix_h = false;
      clean.plate_suffix_e = false;
    }

    if (!flags.seasonal) {
      clean.season_start_month = "4";
      clean.season_end_month = "10";
    }

    const allowedFormats = this._allowedPlateFormatValues(clean.plate_kind);
    if (!allowedFormats.includes(String(clean.plate_format))) {
      clean.plate_format = allowedFormats[0] || "single_line";
    }

    return clean;
  }

  _sanitizeFieldValue(name, value) {
    if (name === "change_plate_vehicle_digit") {
      return String(value || "").replace(/\D/g, "").slice(0, 1);
    }
    if (["plate", "change_plate_common_text"].includes(name)) {
      return String(value || "").toUpperCase();
    }
    return value;
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
    if (!value) return "—";
    const raw = String(value);
    const match = raw.match(/^(\d{4})-(\d{2})-(\d{2})/);
    if (match) {
      return `${match[3]}.${match[2]}.${match[1]}`;
    }
    return raw;
  }

  _statusCounts() {
    return this._vehicles.reduce((counts, vehicle) => {
      const status = vehicle.status || "unknown";
      counts[status] = (counts[status] || 0) + 1;
      return counts;
    }, {});
  }


  _statusChip(label, value, count) {
    const active = this._statusFilter === value ? " active" : "";
    const disabled = value !== "all" && Number(count || 0) === 0 ? " disabled" : "";
    return `<button type="button" class="status-filter-chip${active}${disabled}" data-status-chip="${this._escape(value)}" aria-pressed="${active ? "true" : "false"}"><span>${this._escape(label)}</span><strong>${this._escape(count)}</strong></button>`;
  }

  _summaryChips(counts) {
    const total = this._vehicles.length;
    return `
      <div class="summary-chip-row" aria-label="Status Schnellfilter">
        ${this._statusChip("Alle", "all", total)}
        ${this._statusChip("Abgelaufen", "expired", counts.expired || 0)}
        ${this._statusChip("Fällig", "due", counts.due || 0)}
        ${this._statusChip("Gültig", "valid", counts.valid || 0)}
      </div>
    `;
  }

  _sortValue(vehicle, key) {
    if (key === "name") return String(vehicle.vehicle_name || vehicle.title || "").toLowerCase();
    if (key === "hu") return String(vehicle.due_date || `${String(vehicle.year || "9999").padStart(4, "0")}-${String(vehicle.month || "99").padStart(2, "0")}-01`);
    if (key === "reminder") return String(vehicle.reminder_date || "9999-99-99");
    if (key === "status") {
      const order = { expired: 0, due: 1, valid: 2 };
      return order[vehicle.status] ?? 9;
    }
    if (key === "plate") return String(vehicle.plate_display || vehicle.plate || "").toLowerCase();
    return String(vehicle.due_date || "9999-99-99");
  }

  _compareVehicles(a, b) {
    const key = this._sortKey || "hu";
    const direction = this._sortDirection === "desc" ? -1 : 1;
    const left = this._sortValue(a, key);
    const right = this._sortValue(b, key);
    let result;
    if (typeof left === "number" && typeof right === "number") {
      result = left - right;
    } else {
      result = String(left).localeCompare(String(right), "de", { sensitivity: "base", numeric: true });
    }
    if (result === 0 && key !== "name") {
      result = String(a.vehicle_name || a.title || "").localeCompare(String(b.vehicle_name || b.title || ""), "de", { sensitivity: "base", numeric: true });
    }
    return result * direction;
  }

  _sortIndicator(key) {
    if (this._sortKey !== key) return "";
    return this._sortDirection === "desc" ? "↓" : "↑";
  }

  _sortDirectionLabel(key = this._sortKey) {
    if (key === "status") {
      return this._sortDirection === "desc" ? "gültig zuerst" : "kritisch zuerst";
    }
    return this._sortDirection === "desc" ? "absteigend" : "aufsteigend";
  }

  _sortAriaSort(key) {
    if (this._sortKey !== key) return "none";
    return this._sortDirection === "desc" ? "descending" : "ascending";
  }

  _sortSummaryLabel() {
    const labels = { name: "Name", hu: "HU", reminder: "Erinnerung", status: "Status", plate: "Kennzeichen" };
    const label = labels[this._sortKey] || "HU";
    return `Sortiert nach ${label}, ${this._sortDirectionLabel()}`;
  }

  _sortHeader(label, key, extraClass = "") {
    const directionClass = this._sortKey === key ? ` active ${this._sortDirection === "desc" ? "desc" : "asc"}` : "";
    const nextDirection = this._sortKey === key && this._sortDirection === "asc" ? "absteigend" : "aufsteigend";
    const indicator = this._sortIndicator(key);
    return `<th class="${this._escape(extraClass)}" aria-sort="${this._escape(this._sortAriaSort(key))}"><button class="sort-header${this._escape(directionClass)}" type="button" data-sort-key="${this._escape(key)}" title="Nach ${this._escape(label)} sortieren" aria-label="Nach ${this._escape(label)} sortieren, nächster Klick ${this._escape(nextDirection)}">${this._escape(label)}<span class="sort-indicator" aria-hidden="true">${this._escape(indicator)}</span><span class="sr-only">${this._sortKey === key ? this._escape(` aktuell ${this._sortDirectionLabel(key)}`) : ""}</span></button></th>`;
  }

  _cssEscape(value) {
    if (window.CSS?.escape) return CSS.escape(String(value));
    return String(value).replace(/\\/g, "\\\\").replace(/"/g, '\\"');
  }

  _captureListUiState() {
    const root = this.shadowRoot;
    if (!root) return {};

    const active = root.activeElement;
    const focus = active
      ? {
          id: active.id || "",
          field: active.dataset?.field || "",
          sortKey: active.dataset?.sortKey || "",
          menuEntryId: active.dataset?.menuEntryId || "",
          createTrigger: active.dataset?.createTrigger || "",
          selectionStart: null,
          selectionEnd: null,
        }
      : null;

    if (focus && typeof active.selectionStart === "number") {
      focus.selectionStart = active.selectionStart;
      focus.selectionEnd = active.selectionEnd;
    }

    const shell = root.querySelector(".list-shell");
    return {
      focus,
      listScrollLeft: shell ? shell.scrollLeft : null,
      listScrollTop: shell ? shell.scrollTop : null,
    };
  }

  _restoreListUiState(state = {}) {
    const root = this.shadowRoot;
    if (!root) return;

    const shell = root.querySelector(".list-shell");
    if (shell) {
      if (typeof state.listScrollLeft === "number") shell.scrollLeft = state.listScrollLeft;
      if (typeof state.listScrollTop === "number") shell.scrollTop = state.listScrollTop;
    }

    const focus = state.focus;
    if (!focus) return;

    let target = null;
    if (focus.id) target = root.querySelector(`#${this._cssEscape(focus.id)}`);
    if (!target && focus.field) target = root.querySelector(`[data-field="${this._cssEscape(focus.field)}"]`);
    if (!target && focus.sortKey) target = root.querySelector(`[data-sort-key="${this._cssEscape(focus.sortKey)}"]`);
    if (!target && focus.menuEntryId) target = root.querySelector(`[data-menu-entry-id="${this._cssEscape(focus.menuEntryId)}"]`);
    if (!target && focus.createTrigger) target = root.querySelector(`[data-create-trigger="${this._cssEscape(focus.createTrigger)}"]`);

    if (!target || typeof target.focus !== "function") return;

    target.focus({ preventScroll: true });
    if (typeof focus.selectionStart === "number" && typeof target.setSelectionRange === "function") {
      try {
        target.setSelectionRange(focus.selectionStart, focus.selectionEnd ?? focus.selectionStart);
      } catch (_err) {
        // Some input types do not support selection ranges. Focus restore is enough.
      }
    }
  }

  _renderPreservingListUiState() {
    const state = this._captureListUiState();
    this._render();
    this._restoreListUiState(state);
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

    return vehicles.sort((a, b) => this._compareVehicles(a, b));
  }

  _filtersActive() {
    return Boolean(String(this._filter || "").trim()) || this._statusFilter !== "all";
  }

  _resetListFilters() {
    this._filter = "";
    this._statusFilter = "all";
    this._openMenuIndex = null;
    this._openMenuEntryId = null;
    this._renderPreservingListUiState();
  }

  _clearSearchFilter() {
    this._filter = "";
    this._openMenuIndex = null;
    this._openMenuEntryId = null;
    this._renderPreservingListUiState();
  }

  _emptyFilterStateHtml() {
    const rawFilter = String(this._filter || "").trim();
    const statusActive = this._statusFilter !== "all";
    const statusLabel = statusActive ? this._statusLabel(this._statusFilter) : "";
    const title = rawFilter ? `Keine Treffer für „${this._escape(rawFilter)}“` : `Keine Fahrzeuge mit Status „${this._escape(statusLabel)}“`;
    const hint = rawFilter && statusActive
      ? "Suche und Statusfilter schränken die Liste gemeinsam ein. Lösche die Suche oder wähle oben den Chip „Alle“."
      : rawFilter
        ? "Lösche die Suche oder passe den Suchbegriff an."
        : "Wähle oben den Chip „Alle“, um wieder alle Fahrzeuge zu sehen.";
    return `
      <div class="state state-card filter-empty-state">
        <strong>${title}</strong>
        <p>${this._escape(hint)}</p>
        ${rawFilter ? `<button type="button" class="ghost" id="clear-empty-search">Suche leeren</button>` : ""}
      </div>
    `;
  }

  _platePreviewFromText(text, options = {}) {
    const green = options.green === true;
    const seasonal = options.seasonal === true;
    return `
      <span class="plate-preview ${green ? "plate-preview-green" : ""}" title="Kennzeichenvorschau">
        <span class="plate-eu">D</span>
        <span class="plate-text">${this._escape(text || "—")}</span>
        ${seasonal ? `<span class="plate-season">${this._escape(options.seasonStart)}–${this._escape(options.seasonEnd)}</span>` : ""}
      </span>
    `;
  }

  _platePreview(vehicle) {
    return this._platePreviewFromText(vehicle.plate_display || vehicle.plate || "—", {
      green: vehicle.plate_color_mode === "green",
      seasonal: vehicle.seasonal,
      seasonStart: vehicle.season_start_month,
      seasonEnd: vehicle.season_end_month,
    });
  }

  _formPlateText(form = this._form) {
    const clean = this._scrubFormForKind(form);
    if (clean.plate_kind === "change") {
      const common = this._normalizePlate(clean.change_plate_common_text);
      const digit = String(clean.change_plate_vehicle_digit || "").trim();
      return `${common}${digit ? ` ${digit}` : ""}`.trim();
    }
    const plate = this._normalizePlate(clean.plate);
    const suffix = `${clean.plate_suffix_h ? "H" : ""}${clean.plate_suffix_e ? "E" : ""}`;
    return `${plate}${suffix ? ` ${suffix}` : ""}`.trim();
  }

  _normalizePlate(value) {
    return String(value || "").trim().replace(/\s+/g, " ").toUpperCase();
  }

  _duplicateKey(value) {
    return String(value || "").trim().replace(/\s+/g, " ").toLocaleLowerCase("de-DE");
  }

  _formDuplicateErrors() {
    const errors = [];
    const currentEntryId = this._view === "detail" ? String(this._selectedVehicle?.entry_id || "") : "";
    const wantedName = this._duplicateKey(this._form.vehicle_name);
    const wantedPlate = this._duplicateKey(this._formPlateText());

    if (!wantedName && !wantedPlate) {
      return errors;
    }

    for (const vehicle of this._vehicles || []) {
      if (currentEntryId && String(vehicle.entry_id || "") === currentEntryId) {
        continue;
      }
      const existingName = this._duplicateKey(vehicle.vehicle_name || vehicle.title);
      const existingPlate = this._duplicateKey(vehicle.plate_display || vehicle.plate);
      if (wantedName && existingName === wantedName) {
        errors.push("Ein Fahrzeug mit diesem Namen existiert bereits.");
      }
      if (wantedPlate && existingPlate === wantedPlate) {
        errors.push("Ein Fahrzeug mit diesem Kennzeichen existiert bereits.");
      }
      if (errors.length >= 2) {
        break;
      }
    }

    return errors;
  }


  _formValidation() {
    const errors = [];
    const clean = this._scrubFormForKind();
    const kindValues = (this._metadata?.plate_kinds || []).map((option) => String(option.value));
    if (kindValues.length && !kindValues.includes(String(clean.plate_kind))) {
      errors.push("Kennzeichenart ist ungültig.");
    }
    if (!String(clean.vehicle_name || "").trim()) errors.push("Fahrzeugname fehlt.");
    if (clean.plate_kind === "change") {
      if (!String(clean.change_plate_common_text || "").trim()) errors.push("Gemeinsamer Wechselkennzeichen-Text fehlt.");
      if (!String(clean.change_plate_vehicle_digit || "").trim()) errors.push("Fahrzeugziffer für Wechselkennzeichen fehlt.");
    } else if (!String(clean.plate || "").trim()) {
      errors.push("Kennzeichen fehlt.");
    }
    const month = Number(clean.month);
    const year = Number(clean.year);
    const offset = Number(clean.reminder_offset_days);
    if (!Number.isInteger(month) || month < 1 || month > 12) errors.push("HU-Monat muss zwischen 1 und 12 liegen.");
    if (!Number.isInteger(year) || year < 1900 || year > 2100) errors.push("HU-Jahr muss zwischen 1900 und 2100 liegen.");
    const interval = Number(clean.interval);
    if (!Number.isInteger(interval) || ![1, 2].includes(interval)) errors.push("Prüfintervall muss 1 oder 2 Jahre betragen.");
    if (!this._allowedPlateFormatValues(clean.plate_kind).includes(String(clean.plate_format))) {
      errors.push("Kennzeichenformat passt nicht zur Kennzeichenart.");
    }
    if (!Number.isInteger(offset) || offset < 0 || offset > 365) errors.push("Erinnerungs-Vorlauf muss zwischen 0 und 365 Tagen liegen.");
    if (["seasonal", "green_seasonal"].includes(clean.plate_kind)) {
      const start = Number(clean.season_start_month);
      const end = Number(clean.season_end_month);
      if (!Number.isInteger(start) || start < 1 || start > 12 || !Number.isInteger(end) || end < 1 || end > 12) {
        errors.push("Saisonmonate müssen zwischen 1 und 12 liegen.");
      } else if (!this._isValidSeasonRange(start, end)) {
        errors.push("Saisonzeitraum muss mindestens 2 und höchstens 11 Monate umfassen.");
      }
    }
    this._formDuplicateErrors().forEach((error) => errors.push(error));
    return errors;
  }

  _mobileActionMode() {
    return this._narrow || window.matchMedia?.("(max-width: 1100px)")?.matches === true;
  }

  _vehicleByEntryId(entryId) {
    if (!entryId) return null;
    return this._vehicles.find((vehicle) => String(vehicle.entry_id || "") === String(entryId)) || null;
  }

  _openRowMenu(index) {
    const vehicle = this._visibleVehicles()[index];
    if (!vehicle) return;
    if (this._mobileActionMode()) {
      this._openMenuIndex = null;
      this._openMenuEntryId = null;
      this._actionSheetVehicle = vehicle;
      this._actionSheetOpenedAt = Date.now();
      this._actionSheetCloseGuardUntil = this._actionSheetOpenedAt + 650;
      this._dialogFocusPending = "actionSheet";
    } else {
      this._actionSheetVehicle = null;
      this._openMenuIndex = null;
      this._openMenuEntryId = this._openMenuEntryId === vehicle.entry_id ? null : vehicle.entry_id;
    }
    this._renderPreservingListUiState();
  }

  _closeRowMenu() {
    if (this._openMenuIndex !== null || this._openMenuEntryId !== null) {
      this._openMenuIndex = null;
      this._openMenuEntryId = null;
      this._renderPreservingListUiState();
    }
  }

  _closeActionSheet({ force = false } = {}) {
    if (!force && Date.now() < this._actionSheetCloseGuardUntil) {
      return;
    }
    if (this._actionSheetVehicle) {
      this._actionSheetVehicle = null;
      this._actionSheetOpenedAt = 0;
      this._actionSheetCloseGuardUntil = 0;
      this._renderPreservingListUiState();
    }
  }

  async _fetchVehicleRecord(vehicle) {
    const entryId = String(vehicle?.entry_id || "");
    if (!entryId || !this._hass) {
      return vehicle;
    }

    const result = await this._hass.connection.sendMessagePromise({
      type: "tuev_reminder/manager/vehicles/get",
      entry_id: entryId,
    });
    const latest = result?.vehicle || vehicle;
    const index = this._vehicles.findIndex((item) => String(item.entry_id || "") === entryId);
    if (index >= 0) {
      this._vehicles = this._vehicles.map((item, itemIndex) => (itemIndex === index ? latest : item));
    }
    return latest;
  }

  async _handleRowAction(action, vehicle) {
    if (this._rowActionLoadingEntryId) {
      return;
    }

    const entryId = String(vehicle?.entry_id || "");
    this._openMenuIndex = null;
    this._openMenuEntryId = null;
    this._actionSheetVehicle = null;
    this._actionSheetOpenedAt = 0;
    this._actionSheetCloseGuardUntil = 0;
    this._rowActionLoadingEntryId = entryId || null;
    this._renderPreservingListUiState();

    let latest = vehicle;
    try {
      latest = await this._fetchVehicleRecord(vehicle);
    } catch (err) {
      this._rowActionLoadingEntryId = null;
      this._setFlash("Fahrzeugdaten konnten nicht geladen werden. Die Liste wurde aktualisiert.", "error");
      await this._refresh();
      return;
    }

    this._rowActionLoadingEntryId = null;
    if (action === "edit") {
      this._openDetailForm(latest);
      return;
    }
    if (action === "delete") {
      this._openDeleteConfirm(latest);
      return;
    }
    this._renderPreservingListUiState();
  }

  _payloadKey(payload = this._formPayload()) {
    const normalized = {};
    Object.keys(payload || {}).sort().forEach((key) => {
      normalized[key] = payload[key];
    });
    return JSON.stringify(normalized);
  }

  _rememberFormSnapshot() {
    this._formSnapshot = this._payloadKey();
  }

  _formDirty() {
    if (!["create", "detail"].includes(this._view) || !this._formSnapshot) {
      return false;
    }
    return this._payloadKey() !== this._formSnapshot;
  }

  _shouldPromptDiscardChanges() {
    return ["create", "detail"].includes(this._view) && this._formDirty();
  }

  _openDiscardPrompt() {
    if (!this._shouldPromptDiscardChanges()) {
      return false;
    }
    this._discardPromptOpen = true;
    this._dialogFocusPending = "discard";
    this._render();
    return true;
  }

  _closeDiscardPrompt() {
    if (!this._discardPromptOpen) {
      return;
    }
    this._discardPromptOpen = false;
    if (["create", "detail"].includes(this._view)) {
      this._dialogFocusPending = "modal";
    }
    this._render();
  }

  _openDeleteConfirm(vehicle) {
    this._openMenuIndex = null;
    this._openMenuEntryId = null;
    this._actionSheetVehicle = null;
    this._selectedVehicle = vehicle;
    this._formError = null;
    this._formInfo = null;
    this._discardPromptOpen = false;
    this._view = "delete";
    this._dialogFocusPending = "modal";
    this._render();
  }

  _openCreateForm() {
    this._openMenuIndex = null;
    this._openMenuEntryId = null;
    this._actionSheetVehicle = null;
    this._form = this._defaultForm();
    this._selectedVehicle = null;
    this._formError = null;
    this._formInfo = null;
    this._discardPromptOpen = false;
    this._view = "create";
    this._rememberFormSnapshot();
    this._dialogFocusPending = "modal";
    this._render();
  }

  _openDetailForm(vehicle) {
    this._openMenuIndex = null;
    this._openMenuEntryId = null;
    this._actionSheetVehicle = null;
    this._selectedVehicle = vehicle;
    this._formError = null;
    this._formInfo = null;
    this._discardPromptOpen = false;
    this._form = this._scrubFormForKind({
      ...this._defaultForm(),
      vehicle_name: vehicle.vehicle_name || vehicle.title || "",
      plate: vehicle.plate_base || vehicle.plate_display || vehicle.plate || "",
      month: String(vehicle.month || ""),
      year: String(vehicle.year || ""),
      interval: String(vehicle.interval || "2"),
      reminder_offset_days: String(vehicle.reminder_offset_days ?? "7"),
      plate_kind: vehicle.plate_kind || "standard",
      plate_format: vehicle.plate_format || "single_line",
      plate_suffix_h: vehicle.plate_suffix_h === true,
      plate_suffix_e: vehicle.plate_suffix_e === true,
      season_start_month: String(vehicle.season_start_month || "4"),
      season_end_month: String(vehicle.season_end_month || "10"),
      change_plate_common_text: vehicle.change_plate_common_text || "",
      change_plate_vehicle_digit: vehicle.change_plate_vehicle_digit || "",
    });
    this._view = "detail";
    this._rememberFormSnapshot();
    this._dialogFocusPending = "modal";
    this._render();
  }

  _closeForm(options = {}) {
    if (this._saving || this._deleting) return;
    if (!options.force && this._openDiscardPrompt()) return;
    this._discardPromptOpen = false;
    this._view = "list";
    this._selectedVehicle = null;
    this._formError = null;
    this._formInfo = null;
    this._formSnapshot = null;
    this._dialogFocusPending = null;
    this._render();
  }

  _formPayload() {
    const clean = this._scrubFormForKind();
    const payload = {
      vehicle_name: String(clean.vehicle_name || "").trim(),
      plate: this._normalizePlate(clean.plate),
      month: Number(clean.month),
      year: Number(clean.year),
      interval: Number(clean.interval || 2),
      reminder_offset_days: Number(clean.reminder_offset_days || 0),
      plate_kind: clean.plate_kind || "standard",
      plate_format: clean.plate_format || "single_line",
      plate_suffix_h: clean.plate_suffix_h === true,
      plate_suffix_e: clean.plate_suffix_e === true,
      season_start_month: ["seasonal", "green_seasonal"].includes(clean.plate_kind) ? Number(clean.season_start_month || 4) : null,
      season_end_month: ["seasonal", "green_seasonal"].includes(clean.plate_kind) ? Number(clean.season_end_month || 10) : null,
      change_plate_common_text: clean.plate_kind === "change" ? this._normalizePlate(clean.change_plate_common_text) : "",
      change_plate_vehicle_digit: clean.plate_kind === "change" ? String(clean.change_plate_vehicle_digit || "").trim() : "",
    };
    return payload;
  }

  _setFlash(message, tone = "success") {
    this._flashMessage = { message, tone };
    if (this._flashTimer) window.clearTimeout(this._flashTimer);
    this._flashTimer = window.setTimeout(() => {
      this._flashMessage = null;
      this._flashTimer = null;
      this._render();
    }, 4500);
  }

  _applySaveResult(result) {
    if (Array.isArray(result?.vehicles)) {
      this._vehicles = result.vehicles;
      this._loaded = true;
      return;
    }
    this._loaded = false;
  }

  _finishSuccessfulSave() {
    this._view = "list";
    this._selectedVehicle = null;
    this._form = this._defaultForm();
    this._formInfo = null;
    this._formError = null;
    this._formSnapshot = null;
    this._discardPromptOpen = false;
    this._actionSheetVehicle = null;
    this._openMenuEntryId = null;
  }

  async _saveCreateForm() {
    if (!this._hass || this._view !== "create" || this._saving) {
      return;
    }

    const errors = this._formValidation();
    if (errors.length) {
      this._formError = "Bitte zuerst die markierten Angaben korrigieren.";
      this._syncFormSummary();
      return;
    }

    this._saving = true;
    this._formError = null;
    this._formInfo = "Fahrzeug wird angelegt …";
    this._render();

    try {
      const result = await this._hass.connection.sendMessagePromise({
        type: "tuev_reminder/manager/vehicles/create",
        vehicle: this._formPayload(),
      });
      this._applySaveResult(result);
      if (!this._loaded) await this._refresh();
      this._setFlash("Fahrzeug wurde angelegt.");
      this._finishSuccessfulSave();
    } catch (err) {
      this._formError = err?.message || String(err);
    } finally {
      this._saving = false;
      this._render();
    }
  }

  async _deleteSelectedVehicle() {
    if (!this._hass || this._view !== "delete" || this._deleting || !this._selectedVehicle?.entry_id) {
      return;
    }

    this._deleting = true;
    this._formError = null;
    this._formInfo = "Fahrzeug wird gelöscht …";
    this._render();

    try {
      const result = await this._hass.connection.sendMessagePromise({
        type: "tuev_reminder/manager/vehicles/delete",
        entry_id: this._selectedVehicle.entry_id,
      });
      this._applySaveResult(result);
      if (!this._loaded) await this._refresh();
      this._setFlash("Fahrzeug wurde gelöscht.");
      this._finishSuccessfulSave();
    } catch (err) {
      this._formError = err?.message || String(err);
    } finally {
      this._deleting = false;
      this._render();
    }
  }

  async _saveUpdateForm() {
    if (!this._hass || this._view !== "detail" || this._saving || !this._selectedVehicle?.entry_id) {
      return;
    }

    const errors = this._formValidation();
    if (errors.length) {
      this._formError = "Bitte zuerst die markierten Angaben korrigieren.";
      this._syncFormSummary();
      return;
    }

    this._saving = true;
    this._formError = null;
    this._formInfo = "Änderungen werden gespeichert …";
    this._render();

    try {
      const result = await this._hass.connection.sendMessagePromise({
        type: "tuev_reminder/manager/vehicles/update",
        entry_id: this._selectedVehicle.entry_id,
        vehicle: this._formPayload(),
      });
      this._applySaveResult(result);
      if (!this._loaded) await this._refresh();
      this._setFlash("Änderungen wurden gespeichert.");
      this._finishSuccessfulSave();
    } catch (err) {
      this._formError = err?.message || String(err);
    } finally {
      this._saving = false;
      this._render();
    }
  }

  _setFormValue(name, value, options = {}) {
    const render = options.render !== false;
    this._formError = null;
    this._formInfo = null;
    this._form = this._scrubFormForKind({
      ...this._form,
      [name]: this._sanitizeFieldValue(name, value),
    });
    if (render) {
      this._render();
      return;
    }
    this._syncFormSummary();
  }

  _syncFormSummary() {
    if (!this.shadowRoot || this._view === "list") {
      return;
    }

    const clean = this._scrubFormForKind();
    const { seasonal, green } = this._formKindFlags(clean.plate_kind);
    const errors = this._formValidation();

    const preview = this.shadowRoot.querySelector(".large-preview");
    if (preview) {
      preview.innerHTML = this._platePreviewFromText(this._formPlateText(), {
        green,
        seasonal,
        seasonStart: clean.season_start_month,
        seasonEnd: clean.season_end_month,
      });
    }

    const summary = {
      name: clean.vehicle_name || "—",
      hu: `${String(clean.month || "—").padStart(2, "0")}/${clean.year || "—"}`,
      kind: this._kindLabel(clean.plate_kind),
      format: this._formatLabel(clean.plate_format),
    };
    Object.entries(summary).forEach(([key, value]) => {
      const node = this.shadowRoot.querySelector(`[data-summary="${key}"]`);
      if (node) node.textContent = value;
    });

    const validation = this.shadowRoot.querySelector(".validation");
    if (validation) {
      validation.classList.toggle("has-errors", errors.length > 0);
      validation.classList.toggle("ok", errors.length === 0);
      validation.innerHTML = this._validationHtml(errors);
    }

    const saveButton = this.shadowRoot.querySelector("#save-create, #save-update");
    if (saveButton) {
      const saveAllowed = errors.length === 0 && ["create", "detail"].includes(this._view) && (this._view === "create" || this._formDirty());
      saveButton.disabled = this._saving || !saveAllowed;
      saveButton.textContent = this._saving ? "Speichert …" : "Speichern";
    }
  }

  _validationHtml(errors) {
    const state = [];
    if (this._formError) state.push(`<p class="form-error">${this._escape(this._formError)}</p>`);
    if (this._formInfo) state.push(`<p>${this._escape(this._formInfo)}</p>`);
    if (errors.length) {
      return `<strong>Noch nicht speicherbar</strong><ul>${errors.map((error) => `<li>${this._escape(error)}</li>`).join("")}</ul>${state.join("")}`;
    }
    if (this._view === "detail" && !this._formDirty()) {
      return `<strong>Keine Änderungen</strong><p>Ändere ein Feld, um Speichern zu aktivieren.</p>${state.join("")}`;
    }
    const actionText = this._view === "detail"
      ? "Die Änderungen können über die Reminder-Manager-API in der bestehenden ConfigEntry-Entität gespeichert werden."
      : "Das Formular kann über die Reminder-Manager-API als normale ConfigEntry-Entität angelegt werden.";
    return `<strong>Speicherbereit</strong><p>${this._escape(actionText)}</p>${state.join("")}`;
  }

  _renderVehicles() {
    if (this._loading && !this._loaded) {
      return `<p class="state muted">Manager-Daten werden geladen …</p>`;
    }

    if (this._error) {
      return `<p class="state error">Manager-API nicht erreichbar: ${this._escape(this._error)}</p>`;
    }

    if (!this._vehicles.length) {
      return `
        <div class="state state-card first-run-state">
          <strong>Noch keine Fahrzeuge</strong>
          <p>Lege dein erstes Fahrzeug an. Es wird als normale TÜV-Reminder-ConfigEntry/Entity in Home Assistant erstellt.</p>
          <button type="button" class="empty-create" data-create-trigger="empty" title="Erstes Fahrzeug anlegen" aria-label="Erstes Fahrzeug anlegen">+</button>
        </div>
      `;
    }

    const vehicles = this._visibleVehicles();
    if (!vehicles.length) {
      return this._emptyFilterStateHtml();
    }

    return `
      <div class="list-shell">
        <table class="manager-table">
          <thead>
            <tr>
              ${this._sortHeader("Name", "name", "col-name")}
              ${this._sortHeader("HU", "hu", "col-hu")}
              ${this._sortHeader("Erinnerung", "reminder", "col-reminder")}
              ${this._sortHeader("Status", "status", "col-status")}
              ${this._sortHeader("Kennzeichen", "plate", "col-preview")}
              <th class="col-menu" aria-label="Menü"></th>
            </tr>
          </thead>
          <tbody>
            ${vehicles.map((vehicle, index) => `
              <tr class="vehicle-row ${this._openMenuEntryId === vehicle.entry_id ? "menu-open" : ""}" data-entry-id="${this._escape(vehicle.entry_id)}" data-row-index="${index}">
                <td class="name-cell" data-label="Fahrzeug">
                  <div class="vehicle-title">${this._escape(vehicle.vehicle_name || vehicle.title || "Fahrzeug")}</div>
                  <div class="mobile-plate-slot" data-plate-render-slot="text" data-renderer-state="text" title="Kennzeichen">${this._escape(vehicle.plate_display || vehicle.plate || "—")}</div>
                </td>
                <td class="hu-cell" data-label="HU">
                  <div class="main-value hu-value">${this._escape(this._monthYear(vehicle))}</div>
                </td>
                <td class="reminder-cell" data-label="Erinnerung">
                  <div class="main-value">${this._escape(this._dateLabel(vehicle.reminder_date))}</div>
                </td>
                <td class="status-cell" data-label="Status"><span class="status-pill status-${this._escape(this._statusClass(vehicle.status))}">${this._escape(this._statusLabel(vehicle.status))}</span></td>
                <td class="preview-cell" data-label="Kennzeichen"><div class="row-end-stack"><div class="plate-render-slot" data-plate-render-slot="text" data-renderer-state="text" title="Kennzeichen"><span class="plate-text-slot">${this._escape(vehicle.plate_display || vehicle.plate || "—")}</span></div></div></td>
                <td class="menu-cell">
                  <button type="button" class="row-menu" data-menu-index="${index}" data-menu-entry-id="${this._escape(vehicle.entry_id || "")}" title="Aktionen öffnen" aria-label="Aktionen für Fahrzeug öffnen" aria-haspopup="menu" aria-expanded="${this._openMenuEntryId === vehicle.entry_id ? "true" : "false"}" ${this._rowActionLoadingEntryId === vehicle.entry_id ? 'disabled aria-busy="true"' : ""}><span aria-hidden="true">${this._rowActionLoadingEntryId === vehicle.entry_id ? "…" : "⋮"}</span></button>
                  ${this._openMenuEntryId === vehicle.entry_id ? `
                    <div class="row-action-menu" role="menu" aria-label="Fahrzeugaktionen">
                      <button type="button" data-row-action="edit" data-action-index="${index}" data-action-entry-id="${this._escape(vehicle.entry_id || "")}" role="menuitem">Bearbeiten</button>
                      <button type="button" data-row-action="delete" data-action-index="${index}" data-action-entry-id="${this._escape(vehicle.entry_id || "")}" role="menuitem">Löschen</button>
                    </div>
                  ` : ""}
                </td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    `;
  }

  _renderOptionList(options, selected) {
    return options.map((option) => `<option value="${this._escape(option.value)}" ${selected === option.value ? "selected" : ""}>${this._escape(option.label)}</option>`).join("");
  }

  _renderMonthOptions(selected) {
    return Array.from({ length: 12 }, (_, index) => {
      const value = String(index + 1);
      return `<option value="${value}" ${String(selected) === value ? "selected" : ""}>${value.padStart(2, "0")}</option>`;
    }).join("");
  }

  _renderIntervalOptions(selected) {
    return [
      { value: "1", label: "1 Jahr" },
      { value: "2", label: "2 Jahre" },
    ].map((option) => `<option value="${option.value}" ${String(selected) === option.value ? "selected" : ""}>${option.label}</option>`).join("");
  }

  _allowedPlateFormatValues(kind = this._form.plate_kind) {
    const formatsByKind = this._metadata?.plate_formats_by_kind || {};
    const configured = formatsByKind[kind];
    if (Array.isArray(configured) && configured.length) {
      return configured.map((value) => String(value));
    }
    const allFormats = this._metadata?.plate_formats || [];
    if (Array.isArray(allFormats) && allFormats.length) {
      return allFormats.map((option) => String(option.value));
    }
    if (kind === "change") {
      return ["single_line", "two_line", "motorcycle"];
    }
    return ["single_line", "two_line", "small_two_line", "motorcycle"];
  }

  _plateFormatOptionsForKind(kind = this._form.plate_kind) {
    const fallback = [
      { value: "single_line", label: "Einzeilig" },
      { value: "two_line", label: "Zweizeilig" },
      { value: "small_two_line", label: "Verkleinert zweizeilig" },
      { value: "motorcycle", label: "Motorrad" },
    ];
    const allFormats = this._metadata?.plate_formats?.length ? this._metadata.plate_formats : fallback;
    const allowed = new Set(this._allowedPlateFormatValues(kind));
    const filtered = allFormats.filter((option) => allowed.has(String(option.value)));
    return filtered.length ? filtered : allFormats;
  }

  _renderDeleteConfirm() {
    const vehicle = this._selectedVehicle || {};
    const name = vehicle.vehicle_name || vehicle.title || "Fahrzeug";
    const plate = vehicle.plate_display || vehicle.plate || "—";
    return `
      <section class="modal-backdrop" aria-label="Fahrzeug löschen" role="dialog" aria-modal="true" tabindex="-1">
        <div class="form-shell delete-shell">
          <div class="form-head">
            <div>
              <h2>Fahrzeug löschen</h2>
              <p>Diese Reminder-ConfigEntry/Entität wird aus Home Assistant entfernt.</p>
            </div>
          </div>
          <div class="form-card delete-card">
            <p><strong>${this._escape(name)}</strong></p>
            <div class="delete-preview">${this._platePreview(vehicle)}</div>
            <p class="note">Löschen entfernt nur den Reminder-Eintrag. Die getrennte Card-Konfiguration wird nicht verändert.</p>
            ${this._formError ? `<p class="form-error">${this._escape(this._formError)}</p>` : ""}
            ${this._formInfo ? `<p class="muted">${this._escape(this._formInfo)}</p>` : ""}
            <div class="form-actions modal-bottom-actions">
              <button class="danger" id="confirm-delete" ${this._deleting ? "disabled" : ""}>${this._deleting ? "Löscht …" : "Löschen"}</button>
              <button class="ghost" id="cancel-delete" ${this._deleting ? "disabled" : ""}>Schließen</button>
            </div>
          </div>
        </div>
      </section>
    `;
  }


  _renderDiscardConfirm() {
    return `
      <section class="discard-backdrop" aria-label="Ungespeicherte Änderungen" role="dialog" aria-modal="true" tabindex="-1">
        <div class="discard-dialog">
          <h2>Ungespeicherte Änderungen</h2>
          <p>Im Formular wurden Angaben geändert. Änderungen verwerfen und zur Liste zurückkehren?</p>
          <div class="form-actions modal-bottom-actions">
            <button class="danger" id="confirm-discard">Verwerfen</button>
            <button class="ghost" id="cancel-discard">Weiter bearbeiten</button>
          </div>
        </div>
      </section>
    `;
  }

  _renderActionSheet() {
    const vehicle = this._actionSheetVehicle || {};
    const name = vehicle.vehicle_name || vehicle.title || "Fahrzeug";
    const plate = vehicle.plate_display || vehicle.plate || "—";
    return `
      <section class="action-sheet-backdrop" aria-label="Fahrzeugaktionen" role="dialog" aria-modal="true" tabindex="-1" data-action-sheet-backdrop="true">
        <div class="action-sheet">
          <div class="action-sheet-head">
            <strong>${this._escape(name)}</strong>
            <span>${this._escape(plate)}</span>
          </div>
          <button type="button" class="sheet-action" data-action-sheet-action="edit">Bearbeiten</button>
          <button type="button" class="sheet-action danger-text" data-action-sheet-action="delete">Löschen</button>
          <button type="button" class="sheet-cancel" id="cancel-action-sheet">Schließen</button>
        </div>
      </section>
    `;
  }

  _renderCreateForm() {
    const isDetail = this._view === "detail";
    const clean = this._scrubFormForKind();
    const errors = this._formValidation();
    const { seasonal, green, change } = this._formKindFlags(clean.plate_kind);
    const plateKinds = this._metadata?.plate_kinds || [
      { value: "standard", label: "Standard" },
      { value: "seasonal", label: "Saisonkennzeichen" },
      { value: "change", label: "Wechselkennzeichen" },
      { value: "green", label: "Grünes Kennzeichen" },
      { value: "green_seasonal", label: "Grünes Kennzeichen + Saison" },
    ];
    const plateFormats = this._plateFormatOptionsForKind(clean.plate_kind);

    return `
      <section class="modal-backdrop" aria-label="${isDetail ? "Fahrzeugdetails" : "Neues Fahrzeug"}" role="dialog" aria-modal="true" tabindex="-1">
        <div class="form-shell vehicle-form-shell">
        <div class="form-head">
          <div>
            <h2>${isDetail ? "Fahrzeugdetails" : "Neues Fahrzeug anlegen"}</h2>
            <p>${isDetail ? "Bestehende Reminder-Entität bearbeiten und über die Manager-API speichern." : "Legt ein neues Fahrzeug als normale TÜV-Reminder-ConfigEntry-Entität an."}</p>
          </div>
        </div>

        <div class="form-grid">
          <div class="form-stack fields-stack" aria-label="Fahrzeugdaten bearbeiten">
            <section class="form-card form-section">
              <div class="section-head">
                <span class="section-kicker">Fahrzeug</span>
                <h3>Basisdaten</h3>
                <p>Name und Hauptdaten für die Reminder-Entität.</p>
              </div>
              <label>Fahrzeugname<input data-field="vehicle_name" value="${this._escape(clean.vehicle_name)}" placeholder="z. B. Golf, Anhänger, Motorrad"></label>
            </section>

            <section class="form-card form-section">
              <div class="section-head">
                <span class="section-kicker">Termin</span>
                <h3>HU & Erinnerung</h3>
                <p>Fälligkeit, Prüfintervall und Vorlauf der Erinnerung.</p>
              </div>
              <div class="field-pair">
                <label>HU-Monat<select data-field="month">${this._renderMonthOptions(clean.month)}</select></label>
                <label>HU-Jahr<input data-field="year" type="number" inputmode="numeric" min="1900" max="2100" step="1" value="${this._escape(clean.year)}"></label>
              </div>
              <div class="field-pair">
                <label>Intervall<select data-field="interval">${this._renderIntervalOptions(clean.interval)}</select></label>
                <label>Erinnerungs-Vorlauf Tage<input data-field="reminder_offset_days" type="number" inputmode="numeric" min="0" max="365" step="1" value="${this._escape(clean.reminder_offset_days)}"></label>
              </div>
            </section>

            <section class="form-card form-section">
              <div class="section-head">
                <span class="section-kicker">Kennzeichen</span>
                <h3>Art & Nummer</h3>
                <p>Format und Kennzeichentext; Sonderfelder erscheinen nur bei passender Art.</p>
              </div>
              <div class="field-pair">
                <label>Kennzeichenart<select data-field="plate_kind">${this._renderOptionList(plateKinds, clean.plate_kind)}</select></label>
                <label>Format<select data-field="plate_format">${this._renderOptionList(plateFormats, clean.plate_format)}</select></label>
              </div>

              ${change ? `
                <div class="field-pair">
                  <label>Gemeinsamer Text<input data-field="change_plate_common_text" value="${this._escape(clean.change_plate_common_text)}" placeholder="z. B. B AB"></label>
                  <label>Fahrzeugziffer<input data-field="change_plate_vehicle_digit" inputmode="numeric" maxlength="1" pattern="[0-9]" value="${this._escape(clean.change_plate_vehicle_digit)}" placeholder="z. B. 1"></label>
                </div>
              ` : `
                <label>Kennzeichen<input data-field="plate" value="${this._escape(clean.plate)}" placeholder="z. B. B AB 123"></label>
                <div class="check-row ${green ? "disabled-row" : ""}">
                  <label><input type="checkbox" data-field="plate_suffix_h" ${clean.plate_suffix_h ? "checked" : ""} ${green ? "disabled" : ""}> H-Kennzeichen</label>
                  <label><input type="checkbox" data-field="plate_suffix_e" ${clean.plate_suffix_e ? "checked" : ""} ${green ? "disabled" : ""}> E-Kennzeichen</label>
                </div>
              `}
            </section>

          </div>

          <div class="form-side-stack">
            <aside class="form-card preview-card">
              <div class="preview-head">
                <span class="section-kicker">Überblick</span>
                <h3>Kennzeichen</h3>
              </div>
              <div class="large-preview">${this._platePreviewFromText(this._formPlateText(), {
                green,
                seasonal,
                seasonStart: clean.season_start_month,
                seasonEnd: clean.season_end_month,
              })}</div>
              <dl class="summary-list">
                <div><dt>Name</dt><dd data-summary="name">${this._escape(clean.vehicle_name || "—")}</dd></div>
                <div><dt>HU</dt><dd data-summary="hu">${this._escape(String(clean.month).padStart(2, "0"))}/${this._escape(clean.year || "—")}</dd></div>
                <div><dt>Art</dt><dd data-summary="kind">${this._escape(this._kindLabel(clean.plate_kind))}</dd></div>
                <div><dt>Format</dt><dd data-summary="format">${this._escape(this._formatLabel(clean.plate_format))}</dd></div>
              </dl>
            </aside>
            ${seasonal ? `
              <section class="form-card inline-season-section season-below-overview" aria-label="Saisonzeitraum">
                <div class="section-head compact-section-head">
                  <span class="section-kicker">Saison</span>
                  <h3>Saisonzeitraum</h3>
                </div>
                <div class="field-pair compact-season-fields">
                  <label>Startmonat<select data-field="season_start_month">${this._renderMonthOptions(clean.season_start_month)}</select></label>
                  <label>Endmonat<select data-field="season_end_month">${this._renderMonthOptions(clean.season_end_month)}</select></label>
                </div>
                <p class="field-hint">Mindestens 2 und höchstens 11 Monate.</p>
              </section>
            ` : ""}
            <div class="validation ${errors.length ? "has-errors" : "ok"}">
              ${this._validationHtml(errors)}
            </div>
            <p class="note">Die Sidebar verwaltet nur Reminder-Daten. Erstellen und Bearbeiten laufen über die Reminder-eigene WebSocket-API. Die Dashboard-Card bleibt ein getrenntes Projekt und liest danach die aktualisierten Entities/Attribute.</p>
            <div class="form-actions modal-bottom-actions">
              ${isDetail
                ? `<button class="action" id="save-update" ${errors.length || this._saving || !this._formDirty() ? "disabled" : ""}>${this._saving ? "Speichert …" : "Speichern"}</button>`
                : `<button class="action" id="save-create" ${errors.length || this._saving ? "disabled" : ""}>${this._saving ? "Speichert …" : "Speichern"}</button>`}
              <button class="ghost" id="back-to-list">Schließen</button>
            </div>
          </div>        </div>
        </div>
      </section>
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
    const listMode = true;
    const showListAddRows = listMode && vehicleCount > 0;
    const formOpen = this._view !== "list";
    const actionSheetOpen = this._view === "list" && Boolean(this._actionSheetVehicle);

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
        .page { min-height: 100%; background: var(--primary-background-color); }
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
        .title-wrap { display: flex; align-items: center; min-width: 0; gap: 12px; }
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
        h1 { margin: 0; font-size: 20px; line-height: 1; font-weight: 500; white-space: nowrap; }
        h2 { margin: 0 0 4px; font-size: 22px; font-weight: 500; }
        h3 { margin: 18px 0 10px; font-size: 14px; font-weight: 600; color: var(--secondary-text-color); text-transform: uppercase; letter-spacing: .04em; }
        h3:first-child { margin-top: 0; }
        .topbar-status { color: var(--secondary-text-color); font-size: 12px; white-space: nowrap; }
        .topbar-status.read-only { color: var(--error-color, #db4437); font-weight: 600; }
        .list-controls {
          display: ${listMode ? "grid" : "none"};
          grid-template-columns: minmax(260px, 420px) minmax(0, 1fr) auto;
          align-items: center;
          gap: 10px 14px;
          padding: 10px 16px;
          border-bottom: 1px solid var(--divider-color);
          background: var(--secondary-background-color);
        }
        .toolbar {
          display: block;
          min-width: 0;
        }
        .search-wrap { position: relative; min-width: 0; }
        .search-icon {
          position: absolute;
          left: 12px;
          top: 50%;
          transform: translateY(-50%);
          color: var(--secondary-text-color);
          pointer-events: none;
        }
        input, select, button.action, button.ghost, button.danger {
          height: 40px;
          box-sizing: border-box;
          border-radius: 4px;
          font: inherit;
        }
        input, select {
          width: 100%;
          border: 1px solid var(--divider-color);
          background: var(--card-background-color);
          color: var(--primary-text-color);
        }
        input[type="search"] { padding: 0 44px 0 40px; }
        .search-clear {
          position: absolute;
          right: 6px;
          top: 50%;
          transform: translateY(-50%);
          width: 32px;
          height: 32px;
          border: 0;
          border-radius: 50%;
          background: transparent;
          color: var(--secondary-text-color);
          cursor: pointer;
          font-size: 18px;
          line-height: 1;
          display: inline-flex;
          align-items: center;
          justify-content: center;
        }
        .search-clear:hover, .search-clear:focus-visible {
          background: var(--secondary-background-color);
          color: var(--primary-text-color);
          outline: none;
        }
        .search-clear[hidden] { display: none; }
        input:not([type="search"]), select { padding: 0 10px; }
        select { min-width: 160px; padding-right: 28px; }
        button.action {
          border: 0;
          padding: 0 14px;
          background: var(--primary-color);
          color: var(--text-primary-color);
          font-weight: 500;
          cursor: pointer;
          white-space: nowrap;
        }
        button.action[disabled], button.danger[disabled] { opacity: 0.52; cursor: not-allowed; }
        button.danger {
          border: 0;
          padding: 0 14px;
          background: var(--error-color);
          color: var(--text-primary-color);
          font-weight: 500;
          cursor: pointer;
          white-space: nowrap;
        }
        button.icon-action {
          width: 40px;
          min-width: 40px;
          height: 40px;
          padding: 0;
          border: 1px solid var(--divider-color);
          border-radius: 50%;
          background: var(--card-background-color);
          color: var(--primary-text-color);
          font-size: 24px;
          font-weight: 300;
          line-height: 1;
          box-shadow: none;
          cursor: pointer;
        }
        button.icon-action:hover, button.icon-action:focus-visible {
          border-color: var(--primary-color);
          color: var(--primary-color);
          outline: none;
        }
        .list-create-control {
          display: ${showListAddRows ? "flex" : "none"};
          align-items: center;
          justify-content: flex-end;
          min-width: 40px;
        }
        button.ghost {
          border: 1px solid var(--divider-color);
          padding: 0 12px;
          background: var(--card-background-color);
          color: var(--primary-text-color);
          cursor: pointer;
          white-space: nowrap;
        }
        .summary-strip {
          display: flex;
          align-items: center;
          gap: 10px;
          min-width: 0;
          color: var(--secondary-text-color);
          font-size: 13px;
        }
        .summary-strip strong { color: var(--primary-text-color); font-weight: 600; }
        .summary-chip-row {
          display: flex;
          align-items: center;
          flex-wrap: wrap;
          gap: 6px;
          min-width: 0;
        }
        .status-filter-chip {
          min-height: 30px;
          display: inline-flex;
          align-items: center;
          gap: 7px;
          border: 1px solid var(--divider-color);
          border-radius: 999px;
          background: var(--card-background-color);
          color: var(--primary-text-color);
          padding: 0 9px;
          font: inherit;
          cursor: pointer;
        }
        .status-filter-chip strong {
          min-width: 18px;
          height: 18px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          border-radius: 999px;
          background: var(--secondary-background-color);
          font-size: 11px;
          padding: 0 4px;
        }
        .status-filter-chip.active {
          border-color: var(--primary-color);
          background: color-mix(in srgb, var(--primary-color) 12%, var(--card-background-color));
        }
        .status-filter-chip.disabled { opacity: .55; }
        .status-filter-chip:hover, .status-filter-chip:focus-visible {
          border-color: var(--primary-color);
          outline: none;
        }
        .summary-detail {
          color: var(--secondary-text-color);
          font-size: 12px;
          line-height: 1.35;
        }
        .content { padding: 0; }
        .modal-backdrop {
          position: fixed;
          inset: 0;
          z-index: 10;
          display: flex;
          align-items: center;
          justify-content: center;
          box-sizing: border-box;
          padding: 32px 20px;
          background: rgba(0, 0, 0, .46);
        }
        .discard-backdrop {
          position: fixed;
          inset: 0;
          z-index: 2147483100;
          display: flex;
          align-items: center;
          justify-content: center;
          box-sizing: border-box;
          padding: 24px;
          background: rgba(0, 0, 0, .56);
        }
        .discard-dialog {
          width: min(420px, 100%);
          box-sizing: border-box;
          border: 1px solid var(--divider-color);
          border-radius: 14px;
          background: var(--card-background-color);
          padding: 20px;
          box-shadow: 0 16px 48px rgba(0,0,0,.34);
        }
        .discard-dialog p {
          margin: 6px 0 0;
          color: var(--secondary-text-color);
          line-height: 1.45;
        }
        .list-shell { overflow-x: auto; width: 100%; }
        .manager-table { width: 100%; min-width: 900px; border-collapse: separate; border-spacing: 0; table-layout: fixed; }
        th, td { padding: 8px 12px; text-align: left; vertical-align: middle; border-bottom: 1px solid var(--divider-color); }
        th {
          position: sticky;
          top: 0;
          z-index: 2;
          height: 32px;
          color: var(--secondary-text-color);
          font-size: 12px;
          font-weight: 600;
          background: var(--primary-background-color);
        }
        tbody tr { transition: background .12s ease, box-shadow .12s ease; }
        .sort-header {
          display: inline-flex;
          align-items: center;
          gap: 4px;
          width: 100%;
          border: 0;
          padding: 0;
          background: transparent;
          color: inherit;
          font: inherit;
          font-weight: inherit;
          text-align: inherit;
          cursor: pointer;
        }
        .sort-header:hover, .sort-header:focus-visible, .sort-header.active { color: var(--primary-text-color); }
        .sort-header:focus-visible { outline: 2px solid var(--primary-color); outline-offset: 3px; border-radius: 6px; }
        .sort-header.active { font-weight: 700; }
        .sort-indicator { min-width: 12px; text-align: center; }
        .sort-header:not(.active) .sort-indicator { opacity: 0; }
        .sr-only {
          position: absolute;
          width: 1px;
          height: 1px;
          padding: 0;
          margin: -1px;
          overflow: hidden;
          clip: rect(0, 0, 0, 0);
          white-space: nowrap;
          border: 0;
        }
        .col-preview .sort-header { justify-content: flex-end; }
        tbody tr { cursor: default; }
        tbody tr:hover,
        tbody tr.menu-open { background: var(--secondary-background-color); }
        tbody tr.menu-open {
          box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--primary-color) 22%, transparent);
        }
        tbody td:first-child { border-left: 0; }
        .col-name { width: auto; }
        .col-hu { width: 112px; }
        .col-reminder { width: 146px; }
        .col-status { width: 136px; }
        .col-preview { width: 190px; text-align: right; }
        .col-menu { width: 48px; }
        .menu-cell { position: relative; text-align: center; overflow: visible; padding-left: 4px; padding-right: 8px; }
        .row-action-menu {
          position: absolute;
          right: 10px;
          top: 40px;
          z-index: 20;
          min-width: 148px;
          padding: 6px 0;
          border: 1px solid var(--divider-color);
          border-radius: 10px;
          background: var(--card-background-color);
          box-shadow: 0 10px 28px rgba(0,0,0,.30);
          overflow: hidden;
        }
        .row-action-menu button {
          display: block;
          width: 100%;
          border: 0;
          border-radius: 0;
          background: transparent;
          color: var(--primary-text-color);
          padding: 10px 14px;
          text-align: left;
          font-size: 14px;
          cursor: pointer;
        }
        .row-action-menu button:hover,
        .row-action-menu button:focus-visible {
          background: var(--secondary-background-color);
          outline: none;
        }
        .row-action-menu button[data-row-action="delete"] {
          color: var(--error-color);
        }
        .action-sheet-backdrop {
          position: fixed;
          inset: 0;
          z-index: 2147483000;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 24px;
          box-sizing: border-box;
          background: rgba(0,0,0,.55);
          pointer-events: auto;
          touch-action: none;
          overscroll-behavior: contain;
        }
        .action-sheet {
          width: min(360px, 100%);
          border: 1px solid var(--divider-color);
          border-radius: 16px;
          background: var(--card-background-color);
          box-shadow: 0 16px 48px rgba(0,0,0,.34);
          overflow: hidden;
          pointer-events: auto;
          transform: translateZ(0);
        }
        .action-sheet-head {
          display: grid;
          gap: 4px;
          padding: 16px 18px 12px;
          border-bottom: 1px solid var(--divider-color);
        }
        .action-sheet-head span { color: var(--secondary-text-color); font-size: 13px; }
        .sheet-action,
        .sheet-cancel {
          display: block;
          width: 100%;
          min-height: 52px;
          border: 0;
          border-bottom: 1px solid var(--divider-color);
          border-radius: 0;
          background: transparent;
          color: var(--primary-text-color);
          font-size: 16px;
          text-align: left;
          padding: 0 18px;
          cursor: pointer;
        }
        .sheet-action:hover,
        .sheet-cancel:hover { background: var(--secondary-background-color); }
        .sheet-cancel { text-align: center; border-bottom: 0; color: var(--secondary-text-color); }
        .danger-text { color: var(--error-color); }
        .vehicle-title { font-weight: 600; line-height: 1.2; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .mobile-plate-slot { display: none; margin-top: 2px; color: var(--secondary-text-color); font-size: 11px; line-height: 1.2; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .plate-render-slot {
          display: inline-flex;
          align-items: center;
          justify-content: flex-end;
          max-width: 100%;
          min-height: 28px;
          box-sizing: border-box;
          padding: 3px 8px;
          border: 1px solid var(--divider-color);
          border-radius: 6px;
          background: var(--card-background-color);
          color: var(--primary-text-color);
          line-height: 1.2;
          white-space: nowrap;
          overflow: hidden;
        }
        .plate-render-slot[data-renderer-state="text"] {
          opacity: .92;
        }
        .plate-text-slot {
          display: block;
          max-width: 100%;
          overflow: hidden;
          text-overflow: ellipsis;
          font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
          font-size: 13px;
          font-weight: 600;
          letter-spacing: .02em;
          white-space: nowrap;
        }
        .muted { color: var(--secondary-text-color); font-size: 12px; line-height: 1.35; }
        .main-value { font-weight: 500; line-height: 1.2; }
        .hu-value { font-weight: 700; }
        .status-pill {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          border-radius: 999px;
          padding: 3px 9px;
          border: 1px solid var(--divider-color);
          font-size: 12px;
          font-weight: 500;
          background: var(--card-background-color);
        }
        .status-pill::before {
          content: "";
          width: 7px;
          height: 7px;
          border-radius: 50%;
          background: currentColor;
          flex: 0 0 auto;
        }
        .status-expired {
          color: var(--error-color);
          background: color-mix(in srgb, var(--error-color) 12%, transparent);
          border-color: color-mix(in srgb, var(--error-color) 32%, var(--divider-color));
        }
        .status-due {
          color: var(--warning-color, var(--state-icon-active-color));
          background: color-mix(in srgb, var(--warning-color, var(--state-icon-active-color)) 12%, transparent);
          border-color: color-mix(in srgb, var(--warning-color, var(--state-icon-active-color)) 32%, var(--divider-color));
        }
        .status-valid {
          color: var(--success-color, var(--primary-color));
          background: color-mix(in srgb, var(--success-color, var(--primary-color)) 10%, transparent);
          border-color: color-mix(in srgb, var(--success-color, var(--primary-color)) 28%, var(--divider-color));
        }
        .preview-cell { text-align: right; }
        .row-end-stack {
          display: flex;
          align-items: center;
          justify-content: flex-end;
          min-width: 0;
        }
        .plate-preview {
          display: inline-flex;
          align-items: stretch;
          width: min(170px, 100%);
          max-width: 170px;
          min-width: 118px;
          height: 32px;
          box-sizing: border-box;
          border: 2px solid #1b1b1b;
          border-radius: 5px;
          overflow: hidden;
          background: #f7f7f1;
          color: #111;
          box-shadow: inset 0 0 0 1px rgba(0,0,0,0.16);
          font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
        }
        .large-preview .plate-preview { height: 54px; max-width: 320px; min-width: 220px; }
        .large-preview .plate-text { font-size: 24px; }
        .large-preview .plate-eu { width: 32px; font-size: 12px; }
        .large-preview .plate-season { min-width: 36px; font-size: 11px; }
        .plate-preview-green { color: #0a7d28; border-color: #0a7d28; }
        .plate-eu {
          display: inline-flex;
          align-items: flex-end;
          justify-content: center;
          width: 19px;
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
          padding: 0 7px;
          font-size: 16px;
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
          width: 38px;
          height: 38px;
          min-width: 38px;
          min-height: 38px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          border: 0;
          border-radius: 50%;
          background: transparent;
          color: var(--secondary-text-color);
          font-size: 24px;
          line-height: 1;
          cursor: pointer;
          touch-action: manipulation;
          -webkit-tap-highlight-color: transparent;
          position: relative;
          z-index: 4;
        }
        .row-menu:hover,
        .row-menu:focus-visible,
        .menu-open .row-menu {
          background: var(--secondary-background-color);
          color: var(--primary-text-color);
          outline: none;
        }
        .row-menu span {
          pointer-events: none;
          transform: translateY(-1px);
        }
        .state { padding: 24px 16px; }
        .state-card {
          display: grid;
          gap: 8px;
          align-items: start;
          justify-items: start;
        }
        .state-card strong { color: var(--primary-text-color); font-size: 15px; }
        .state-card p { margin: 0; color: var(--secondary-text-color); font-size: 13px; }
        .first-run-state {
          align-items: center;
          justify-items: center;
          text-align: center;
          margin: 24px;
          border: 1px solid var(--divider-color);
          border-radius: 12px;
          background: var(--card-background-color);
        }
        .first-run-state p {
          max-width: 560px;
          line-height: 1.45;
        }
        .filter-empty-state {
          margin: 18px 16px;
          padding: 18px;
          border: 1px dashed var(--divider-color);
          border-radius: 12px;
          background: var(--card-background-color);
        }
        .filter-empty-state p {
          max-width: 640px;
          line-height: 1.45;
        }
        button.empty-create {
          width: 48px;
          height: 48px;
          min-width: 48px;
          border: 0;
          border-radius: 50%;
          background: transparent;
          color: var(--primary-text-color);
          font-size: 38px;
          font-weight: 300;
          line-height: 1;
          cursor: pointer;
        }
        button.empty-create:hover,
        button.empty-create:focus-visible {
          background: var(--secondary-background-color);
          outline: none;
        }
        .error { color: var(--error-color); }
        .form-shell {
          width: min(1120px, 100%);
          max-height: min(920px, calc(100vh - 40px));
          overflow: auto;
          padding: 18px 20px 24px;
          box-sizing: border-box;
          border: 1px solid var(--divider-color);
          border-radius: 12px;
          background: var(--primary-background-color);
          box-shadow: 0 16px 48px rgba(0,0,0,.32);
        }
        .form-head {
          display: block;
          margin-bottom: 18px;
        }
        .form-head p { margin: 0; color: var(--secondary-text-color); }
        .delete-shell { width: min(520px, 100%); }
        .delete-card p:first-child { margin-top: 0; }
        .delete-preview { margin: 12px 0 16px; text-align: right; }
        .form-actions { display: flex; gap: 8px; align-items: center; }
        .modal-bottom-actions {
          justify-content: flex-end;
          margin-top: 22px;
          padding-top: 16px;
          border-top: 1px solid var(--divider-color);
        }
        .form-grid { display: grid; grid-template-columns: minmax(380px, 700px) minmax(280px, 420px); gap: 18px; align-items: start; }
        .form-stack { display: grid; gap: 12px; }
        .form-card {
          border: 1px solid var(--divider-color);
          border-radius: 12px;
          background: var(--card-background-color);
          padding: 16px;
          box-sizing: border-box;
        }
        .form-section { display: grid; gap: 12px; }
        .section-head, .preview-head { display: grid; gap: 3px; margin-bottom: 2px; }
        .section-head h3, .preview-head h3 { margin: 0; color: var(--primary-text-color); text-transform: none; letter-spacing: 0; font-size: 16px; }
        .section-head p { margin: 0; color: var(--secondary-text-color); font-size: 12px; line-height: 1.4; }
        .section-kicker { color: var(--primary-color); font-size: 11px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
        label { display: block; color: var(--secondary-text-color); font-size: 12px; font-weight: 500; }
        label input, label select { margin-top: 6px; color: var(--primary-text-color); font-size: 14px; }
        .field-pair { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        .check-row { display: flex; flex-wrap: wrap; gap: 18px; margin-top: 10px; }
        .check-row label { display: inline-flex; align-items: center; gap: 8px; color: var(--primary-text-color); font-size: 13px; }
        .check-row input { width: auto; height: auto; margin: 0; }
        .disabled-row { opacity: .55; }
        .form-side-stack { display: grid; gap: 12px; position: sticky; top: 16px; }
        .preview-card { position: static; }
        .preview-card dl { margin: 18px 0; }
        .preview-card dl div { display: flex; justify-content: space-between; gap: 16px; padding: 7px 0; border-bottom: 1px solid var(--divider-color); }
        .inline-season-section {
          padding: 14px;
          background: var(--secondary-background-color);
        }
        .compact-section-head { margin-bottom: 10px; }
        .compact-season-fields { gap: 10px; }
        .field-hint { margin: 10px 0 0; color: var(--secondary-text-color); font-size: 12px; line-height: 1.35; }
        dt { color: var(--secondary-text-color); }
        dd { margin: 0; text-align: right; }
        .validation { border-radius: 8px; padding: 12px; font-size: 13px; border: 1px solid var(--divider-color); }
        .validation ul { margin: 8px 0 0 18px; padding: 0; }
        .validation p { margin: 8px 0 0; }
        .form-error { color: var(--error-color); }
        .validation.has-errors { color: var(--error-color); }
        .validation.ok { color: var(--success-color, var(--primary-color)); }
        .note { color: var(--secondary-text-color); font-size: 12px; line-height: 1.45; }
        @media (max-width: 980px) {
          .list-controls { grid-template-columns: 1fr auto; gap: 8px; padding-left: 10px; padding-right: 10px; }
          .toolbar { grid-column: 1; }
          .summary-strip { grid-column: 1 / -1; }
          .list-create-control { grid-column: 2; grid-row: 1; align-self: start; }
          select { width: 100%; }
          .summary-strip { flex-wrap: wrap; }
          .summary-chip-row { gap: 6px; }
          .status-filter-chip { min-height: 30px; padding: 0 8px; font-size: 12px; }
          .form-head { grid-template-columns: 1fr; }
          .form-grid { grid-template-columns: 1fr; }
        }
        @media (max-width: 1100px) {
          .list-controls { padding: 8px 10px; }
          .list-shell { overflow-x: hidden; width: 100%; }
          .manager-table {
            width: 100%;
            min-width: 0;
            table-layout: fixed;
          }
          th, td {
            padding: 7px 6px;
            overflow: hidden;
          }
          .menu-cell {
            padding: 2px 2px 2px 4px;
            overflow: visible;
          }
          .col-name { width: auto; }
          .col-hu { width: 62px; }
          .col-reminder { width: 92px; }
          .col-status { width: 70px; }
          .col-menu { width: 48px; }
          .col-preview, .preview-cell { display: none; }
          .sort-header { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
          .vehicle-title, .main-value { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
          .mobile-plate-slot { display: block; }
          .status-pill {
            max-width: 100%;
            padding: 2px 5px;
            font-size: 11px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
          }
          .row-menu {
            width: 46px;
            height: 46px;
            min-width: 46px;
            min-height: 46px;
            font-size: 26px;
          }
          .row-action-menu {
            display: none;
          }
          .row-action-menu button {
            min-height: 44px;
            font-size: 15px;
          }
        }
        @media (max-width: 460px) {
          .col-reminder, .reminder-cell { display: none; }
          .col-hu { width: 56px; }
          .col-status { width: 66px; }
          .col-menu { width: 50px; }
          h1 { font-size: 18px; }
          .topbar-status { display: none; }
        }
        @media (max-width: 720px) {
          .list-shell {
            overflow: visible;
            padding: 8px 10px 14px;
            box-sizing: border-box;
          }
          .manager-table,
          .manager-table tbody,
          .manager-table tr,
          .manager-table td {
            display: block;
            width: 100%;
            box-sizing: border-box;
          }
          .manager-table thead { display: none; }
          .manager-table { border-collapse: separate; border-spacing: 0; }
          .vehicle-row {
            position: relative;
            margin: 0 0 10px;
            border: 1px solid var(--divider-color);
            border-radius: 12px;
            background: var(--card-background-color);
            overflow: visible;
            box-shadow: 0 1px 2px rgba(0,0,0,.08);
          }
          .vehicle-row:hover { background: var(--card-background-color); }
          .vehicle-row.menu-open {
            background: var(--secondary-background-color);
            box-shadow: none;
          }
          th, td { border-bottom: 0; }
          .vehicle-row td:first-child { border-left: 0; }
          .name-cell {
            padding: 10px 56px 6px 12px;
          }
          .hu-cell,
          .reminder-cell,
          .status-cell {
            display: grid;
            grid-template-columns: 82px minmax(0, 1fr);
            align-items: center;
            gap: 8px;
            padding: 4px 12px;
          }
          .hu-cell::before,
          .reminder-cell::before,
          .status-cell::before {
            content: attr(data-label);
            color: var(--secondary-text-color);
            font-size: 12px;
            font-weight: 500;
          }
          .menu-cell {
            position: absolute;
            top: 6px;
            right: 6px;
            width: auto;
            padding: 0;
          }
          .mobile-plate-slot { display: block; font-size: 11px; margin-top: 2px; }
          .status-pill { justify-self: start; padding: 2px 8px; font-size: 12px; }
          .col-reminder, .reminder-cell { display: grid; }
          .col-hu, .col-status, .col-menu { width: auto; }
          .modal-backdrop {
            align-items: stretch;
            justify-content: stretch;
            padding: 0;
            background: var(--primary-background-color);
          }
          .vehicle-form-shell {
            width: 100%;
            max-height: 100vh;
            min-height: 100vh;
            border: 0;
            border-radius: 0;
            box-shadow: none;
            padding: 12px 12px 88px;
          }
          .vehicle-form-shell .form-head {
            margin-bottom: 12px;
          }
          .vehicle-form-shell h2 {
            font-size: 20px;
          }
          .vehicle-form-shell .form-head p {
            font-size: 13px;
            line-height: 1.35;
          }
          .vehicle-form-shell h3 {
            font-size: 15px;
          }
          .vehicle-form-shell .section-head p {
            display: none;
          }
          .vehicle-form-shell .form-grid {
            gap: 12px;
          }
          .vehicle-form-shell .form-card {
            padding: 12px;
            border-radius: 8px;
          }
          .vehicle-form-shell .form-stack {
            gap: 10px;
          }
          .vehicle-form-shell .form-side-stack {
            position: static;
            gap: 10px;
          }
          .vehicle-form-shell .field-pair {
            gap: 10px;
          }
          .vehicle-form-shell label {
            font-size: 11px;
          }
          .vehicle-form-shell label input,
          .vehicle-form-shell label select {
            margin-top: 5px;
            font-size: 16px;
          }
          .vehicle-form-shell input,
          .vehicle-form-shell select {
            height: 42px;
          }
          .vehicle-form-shell .check-row {
            gap: 10px 16px;
          }
          .vehicle-form-shell .preview-card {
            padding-bottom: 12px;
          }
          .vehicle-form-shell .large-preview .plate-preview {
            width: 100%;
            min-width: 0;
            max-width: 100%;
            height: 44px;
          }
          .vehicle-form-shell .large-preview .plate-text {
            font-size: 19px;
          }
          .vehicle-form-shell .large-preview .plate-eu {
            width: 28px;
          }
          .vehicle-form-shell .large-preview .plate-season {
            min-width: 30px;
          }
          .vehicle-form-shell .preview-card dl {
            margin: 12px 0;
          }
          .vehicle-form-shell .preview-card dl div {
            padding: 5px 0;
            font-size: 12px;
          }
          .vehicle-form-shell .note {
            display: none;
          }
          .vehicle-form-shell .validation {
            padding: 10px;
            font-size: 12px;
          }
          .vehicle-form-shell .modal-bottom-actions {
            position: fixed;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 2147482000;
            margin: 0;
            padding: 10px 12px calc(10px + env(safe-area-inset-bottom));
            border-top: 1px solid var(--divider-color);
            background: var(--card-background-color);
            box-shadow: 0 -8px 24px rgba(0,0,0,.18);
          }
          .vehicle-form-shell .modal-bottom-actions button {
            min-height: 44px;
          }
          .vehicle-form-shell .modal-bottom-actions .action,
          .vehicle-form-shell .modal-bottom-actions .ghost {
            flex: 1 1 0;
          }
        }
        @media (max-width: 560px) {
          .field-pair { grid-template-columns: 1fr; }
        }
      </style>
      <main class="page">
        <header class="topbar">
          <div class="title-wrap">
            <button class="menu" title="Menü öffnen" aria-label="Menü öffnen">☰</button>
            <h1>TÜV Reminder</h1>
          </div>
          <div class="topbar-status${this._metadata?.write_api === true ? " sr-only" : " read-only"}" aria-live="polite">${this._metadata?.write_api === true ? `API v${this._escape(apiVersion)} · ${this._escape(writeApi)}` : "Nur lesen"}</div>
        </header>

        <section class="list-controls" aria-label="Fahrzeugliste filtern und sortieren">
          <div class="toolbar">
            <div class="search-wrap">
              <span class="search-icon">⌕</span>
              <input id="filter" type="search" placeholder="Suchen" value="${this._escape(this._filter)}">
              <button type="button" class="search-clear" id="clear-search" title="Suche leeren" aria-label="Suche leeren" ${String(this._filter || "").trim() ? "" : "hidden"}>×</button>
            </div>
          </div>
          <div class="summary-strip" aria-label="Status Schnellfilter">
            ${this._summaryChips(counts)}
            <span class="sr-only" aria-live="polite">${this._escape(this._sortSummaryLabel())}</span>
          </div>
          <div class="list-create-control" aria-label="Fahrzeug hinzufügen">
            <button class="action icon-action" data-create-trigger="controls" title="Neues Fahrzeug anlegen" aria-label="Neues Fahrzeug anlegen">+</button>
          </div>
        </section>

        ${this._flashMessage ? `<section class="flash ${this._escape(this._flashMessage.tone || "success")}" role="status">${this._escape(this._flashMessage.message)}</section>` : ""}

        <section class="content">
          ${this._renderVehicles()}
        </section>
        ${formOpen ? (this._view === "delete" ? this._renderDeleteConfirm() : this._renderCreateForm()) : ""}
        ${this._discardPromptOpen ? this._renderDiscardConfirm() : ""}
        ${actionSheetOpen ? this._renderActionSheet() : ""}
      </main>
    `;

    this.shadowRoot.querySelectorAll("[data-create-trigger]").forEach((button) => {
      button.addEventListener("click", () => this._openCreateForm());
    });

    const filterInput = this.shadowRoot.querySelector("#filter");
    if (filterInput) {
      filterInput.addEventListener("input", (event) => {
        this._filter = event.target.value;
        this._openMenuIndex = null;
        this._openMenuEntryId = null;
        this._renderPreservingListUiState();
      });
    }

    const clearSearchButton = this.shadowRoot.querySelector("#clear-search");
    if (clearSearchButton) {
      clearSearchButton.addEventListener("click", () => this._clearSearchFilter());
    }

    this.shadowRoot.querySelectorAll("#clear-empty-search").forEach((button) => {
      button.addEventListener("click", () => this._clearSearchFilter());
    });

    this.shadowRoot.querySelectorAll("button[data-status-chip]").forEach((button) => {
      button.addEventListener("click", () => {
        this._statusFilter = button.dataset.statusChip || "all";
        this._openMenuIndex = null;
        this._openMenuEntryId = null;
        this._renderPreservingListUiState();
      });
    });

    this.shadowRoot.querySelectorAll("button[data-sort-key]").forEach((button) => {
      button.addEventListener("click", () => {
        const key = button.dataset.sortKey;
        if (this._sortKey === key) {
          this._sortDirection = this._sortDirection === "asc" ? "desc" : "asc";
        } else {
          this._sortKey = key;
          this._sortDirection = "asc";
        }
        this._openMenuIndex = null;
        this._openMenuEntryId = null;
        this._renderPreservingListUiState();
      });
    });

    const page = this.shadowRoot.querySelector(".page");
    if (page) {
      page.addEventListener("click", (event) => {
        if (this._openMenuIndex === null && this._openMenuEntryId === null) return;
        const path = event.composedPath ? event.composedPath() : [];
        const insideMenuCell = path.some((node) => node?.classList?.contains?.("menu-cell"));
        if (!insideMenuCell) this._closeRowMenu();
      });
      page.addEventListener("keydown", (event) => {
        if (event.key !== "Escape") return;
        if (this._discardPromptOpen) {
          event.preventDefault();
          event.stopPropagation();
          this._closeDiscardPrompt();
          return;
        }
        if (this._actionSheetVehicle) {
          event.preventDefault();
          event.stopPropagation();
          this._closeActionSheet({ force: true });
          return;
        }
        if (this._view !== "list") {
          event.preventDefault();
          event.stopPropagation();
          this._closeForm();
          return;
        }
        if (this._openMenuIndex !== null || this._openMenuEntryId !== null) {
          event.preventDefault();
          event.stopPropagation();
          this._closeRowMenu();
        }
      });
    }

    this.shadowRoot.querySelectorAll("button[data-menu-index]").forEach((button) => {
      const openMenu = (event) => {
        event.preventDefault();
        event.stopPropagation();
        this._openRowMenu(Number(button.dataset.menuIndex));
      };
      button.addEventListener("click", openMenu);
      button.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          openMenu(event);
        }
      });
    });

    this.shadowRoot.querySelectorAll("button[data-row-action]").forEach((button) => {
      button.addEventListener("click", (event) => {
        event.stopPropagation();
        const vehicle = this._vehicleByEntryId(button.dataset.actionEntryId) || this._visibleVehicles()[Number(button.dataset.actionIndex)];
        if (vehicle) this._handleRowAction(button.dataset.rowAction, vehicle);
      });
    });

    const backButton = this.shadowRoot.querySelector("#back-to-list");
    if (backButton) backButton.addEventListener("click", () => this._closeForm());

    const saveCreateButton = this.shadowRoot.querySelector("#save-create");
    if (saveCreateButton) saveCreateButton.addEventListener("click", () => this._saveCreateForm());

    const saveUpdateButton = this.shadowRoot.querySelector("#save-update");
    if (saveUpdateButton) saveUpdateButton.addEventListener("click", () => this._saveUpdateForm());

    const confirmDeleteButton = this.shadowRoot.querySelector("#confirm-delete");
    if (confirmDeleteButton) confirmDeleteButton.addEventListener("click", () => this._deleteSelectedVehicle());

    const cancelDeleteButton = this.shadowRoot.querySelector("#cancel-delete");
    if (cancelDeleteButton) cancelDeleteButton.addEventListener("click", () => this._closeForm());

    const cancelActionSheetButton = this.shadowRoot.querySelector("#cancel-action-sheet");
    if (cancelActionSheetButton) cancelActionSheetButton.addEventListener("click", () => this._closeActionSheet({ force: true }));

    this.shadowRoot.querySelectorAll("button[data-action-sheet-action]").forEach((button) => {
      button.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        const vehicle = this._actionSheetVehicle;
        if (vehicle) this._handleRowAction(button.dataset.actionSheetAction, vehicle);
      });
    });

    this.shadowRoot.querySelectorAll("[data-field]").forEach((field) => {
      if (field.tagName === "SELECT") {
        field.addEventListener("change", (event) => {
          const name = event.target.dataset.field;
          const needsLayout = name === "plate_kind";
          this._setFormValue(name, event.target.value, { render: needsLayout });
        });
        return;
      }

      if (field.type === "checkbox") {
        field.addEventListener("change", (event) => {
          this._setFormValue(event.target.dataset.field, event.target.checked, { render: false });
        });
        return;
      }

      field.addEventListener("input", (event) => {
        this._setFormValue(event.target.dataset.field, event.target.value, { render: false });
      });
    });

    const confirmDiscardButton = this.shadowRoot.querySelector("#confirm-discard");
    if (confirmDiscardButton) confirmDiscardButton.addEventListener("click", () => this._closeForm({ force: true }));

    const cancelDiscardButton = this.shadowRoot.querySelector("#cancel-discard");
    if (cancelDiscardButton) cancelDiscardButton.addEventListener("click", () => this._closeDiscardPrompt());

    const discardBackdrop = this.shadowRoot.querySelector(".discard-backdrop");
    if (discardBackdrop) {
      if (this._dialogFocusPending === "discard") {
        window.setTimeout(() => {
          discardBackdrop.focus({ preventScroll: true });
          if (this._dialogFocusPending === "discard") this._dialogFocusPending = null;
        }, 0);
      }
      discardBackdrop.addEventListener("click", (event) => {
        if (event.target === discardBackdrop) this._closeDiscardPrompt();
      });
      discardBackdrop.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
          event.preventDefault();
          event.stopPropagation();
          this._closeDiscardPrompt();
        }
      });
    }

    const actionSheetBackdrop = this.shadowRoot.querySelector(".action-sheet-backdrop");
    if (actionSheetBackdrop) {
      // r053 compatibility check marker: window.setTimeout(() => actionSheetBackdrop.focus({ preventScroll: true }), 0);
      if (this._dialogFocusPending === "actionSheet") {
        window.setTimeout(() => {
          actionSheetBackdrop.focus({ preventScroll: true });
          if (this._dialogFocusPending === "actionSheet") this._dialogFocusPending = null;
        }, 0);
      }
      const maybeCloseActionSheet = (event) => {
        if (Date.now() < this._actionSheetCloseGuardUntil) {
          event.preventDefault();
          event.stopPropagation();
          return;
        }
        if (event.target === actionSheetBackdrop) this._closeActionSheet({ force: true });
      };
      actionSheetBackdrop.addEventListener("pointerup", maybeCloseActionSheet);
      actionSheetBackdrop.addEventListener("click", maybeCloseActionSheet);
      actionSheetBackdrop.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
          event.preventDefault();
          event.stopPropagation();
          this._closeActionSheet({ force: true });
        }
      });
    }

    const modalBackdrop = this.shadowRoot.querySelector(".modal-backdrop");
    if (modalBackdrop) {
      if (this._dialogFocusPending === "modal") {
        window.setTimeout(() => {
          modalBackdrop.focus({ preventScroll: true });
          if (this._dialogFocusPending === "modal") this._dialogFocusPending = null;
        }, 0);
      }
      modalBackdrop.addEventListener("click", (event) => {
        if (event.target === modalBackdrop) this._closeForm();
      });
      modalBackdrop.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
          event.preventDefault();
          event.stopPropagation();
          this._closeForm();
        }
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
