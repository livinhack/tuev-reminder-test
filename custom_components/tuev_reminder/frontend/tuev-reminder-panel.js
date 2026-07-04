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
    this._actionSheetVehicle = null;
    this._actionSheetOpenedAt = 0;
    this._actionSheetCloseGuardUntil = 0;
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
    return this._sortDirection === "desc" ? " ↓" : " ↑";
  }

  _sortHeader(label, key, extraClass = "") {
    const active = this._sortKey === key ? " active" : "";
    return `<th class="${this._escape(extraClass)}"><button class="sort-header${active}" type="button" data-sort-key="${this._escape(key)}" aria-label="Nach ${this._escape(label)} sortieren">${this._escape(label)}<span>${this._escape(this._sortIndicator(key))}</span></button></th>`;
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

  _formPlateText() {
    if (this._form.plate_kind === "change") {
      const common = this._normalizePlate(this._form.change_plate_common_text);
      const digit = String(this._form.change_plate_vehicle_digit || "").trim();
      return `${common}${digit ? ` ${digit}` : ""}`.trim();
    }
    let plate = this._normalizePlate(this._form.plate);
    const suffix = `${this._form.plate_suffix_h ? "H" : ""}${this._form.plate_suffix_e ? "E" : ""}`;
    return `${plate}${suffix ? ` ${suffix}` : ""}`.trim();
  }

  _normalizePlate(value) {
    return String(value || "").trim().replace(/\s+/g, " ").toUpperCase();
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

  _formValidation() {
    const errors = [];
    if (!String(this._form.vehicle_name || "").trim()) errors.push("Fahrzeugname fehlt.");
    if (this._form.plate_kind === "change") {
      if (!String(this._form.change_plate_common_text || "").trim()) errors.push("Gemeinsamer Wechselkennzeichen-Text fehlt.");
      if (!String(this._form.change_plate_vehicle_digit || "").trim()) errors.push("Fahrzeugziffer für Wechselkennzeichen fehlt.");
    } else if (!String(this._form.plate || "").trim()) {
      errors.push("Kennzeichen fehlt.");
    }
    const month = Number(this._form.month);
    const year = Number(this._form.year);
    const offset = Number(this._form.reminder_offset_days);
    if (!Number.isInteger(month) || month < 1 || month > 12) errors.push("HU-Monat muss zwischen 1 und 12 liegen.");
    if (!Number.isInteger(year) || year < 1900 || year > 2100) errors.push("HU-Jahr muss zwischen 1900 und 2100 liegen.");
    const interval = Number(this._form.interval);
    if (!Number.isInteger(interval) || ![1, 2].includes(interval)) errors.push("Prüfintervall muss 1 oder 2 Jahre betragen.");
    if (!Number.isInteger(offset) || offset < 0 || offset > 365) errors.push("Erinnerungs-Vorlauf muss zwischen 0 und 365 Tagen liegen.");
    if (["seasonal", "green_seasonal"].includes(this._form.plate_kind)) {
      const start = Number(this._form.season_start_month);
      const end = Number(this._form.season_end_month);
      if (!Number.isInteger(start) || start < 1 || start > 12 || !Number.isInteger(end) || end < 1 || end > 12) {
        errors.push("Saisonmonate müssen zwischen 1 und 12 liegen.");
      }
    }
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

  _handleRowAction(action, vehicle) {
    this._openMenuIndex = null;
    this._openMenuEntryId = null;
    this._actionSheetVehicle = null;
    this._actionSheetOpenedAt = 0;
    this._actionSheetCloseGuardUntil = 0;
    if (action === "edit") {
      this._openDetailForm(vehicle);
      return;
    }
    if (action === "delete") {
      this._openDeleteConfirm(vehicle);
    }
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

  _confirmDiscardChanges() {
    if (!["create", "detail"].includes(this._view) || !this._formDirty()) {
      return true;
    }
    return window.confirm("Ungespeicherte Änderungen verwerfen?");
  }

  _openDeleteConfirm(vehicle) {
    this._openMenuIndex = null;
    this._openMenuEntryId = null;
    this._actionSheetVehicle = null;
    this._selectedVehicle = vehicle;
    this._formError = null;
    this._formInfo = null;
    this._view = "delete";
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
    this._view = "create";
    this._rememberFormSnapshot();
    this._render();
  }

  _openDetailForm(vehicle) {
    this._openMenuIndex = null;
    this._openMenuEntryId = null;
    this._actionSheetVehicle = null;
    this._selectedVehicle = vehicle;
    this._formError = null;
    this._formInfo = null;
    this._form = {
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
    };
    this._view = "detail";
    this._rememberFormSnapshot();
    this._render();
  }

  _closeForm(options = {}) {
    if (this._saving || this._deleting) return;
    if (!options.force && !this._confirmDiscardChanges()) return;
    this._view = "list";
    this._selectedVehicle = null;
    this._formError = null;
    this._formInfo = null;
    this._formSnapshot = null;
    this._render();
  }

  _formPayload() {
    const payload = {
      vehicle_name: String(this._form.vehicle_name || "").trim(),
      plate: this._normalizePlate(this._form.plate),
      month: Number(this._form.month),
      year: Number(this._form.year),
      interval: Number(this._form.interval || 2),
      reminder_offset_days: Number(this._form.reminder_offset_days || 0),
      plate_kind: this._form.plate_kind || "standard",
      plate_format: this._form.plate_format || "single_line",
      plate_suffix_h: this._form.plate_suffix_h === true,
      plate_suffix_e: this._form.plate_suffix_e === true,
      season_start_month: Number(this._form.season_start_month || 4),
      season_end_month: Number(this._form.season_end_month || 10),
      change_plate_common_text: this._normalizePlate(this._form.change_plate_common_text),
      change_plate_vehicle_digit: String(this._form.change_plate_vehicle_digit || "").trim(),
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
    this._form = { ...this._form, [name]: value };
    if (name === "plate_kind" && !["seasonal", "green_seasonal"].includes(value)) {
      this._form.season_start_month = "4";
      this._form.season_end_month = "10";
    }
    if (name === "plate_kind" && value === "green") {
      this._form.plate_suffix_h = false;
      this._form.plate_suffix_e = false;
    }
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

    const seasonal = ["seasonal", "green_seasonal"].includes(this._form.plate_kind);
    const green = ["green", "green_seasonal"].includes(this._form.plate_kind);
    const errors = this._formValidation();

    const preview = this.shadowRoot.querySelector(".large-preview");
    if (preview) {
      preview.innerHTML = this._platePreviewFromText(this._formPlateText(), {
        green,
        seasonal,
        seasonStart: this._form.season_start_month,
        seasonEnd: this._form.season_end_month,
      });
    }

    const summary = {
      name: this._form.vehicle_name || "—",
      hu: `${String(this._form.month || "—").padStart(2, "0")}/${this._form.year || "—"}`,
      kind: this._kindLabel(this._form.plate_kind),
      format: this._formatLabel(this._form.plate_format),
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
      return `<p class="state muted">Noch keine TÜV-Reminder-Fahrzeuge gefunden. Nutze „+“, um ein neues Fahrzeug anzulegen.</p>`;
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
              <tr data-entry-id="${this._escape(vehicle.entry_id)}" data-row-index="${index}">
                <td class="name-cell">
                  <div class="vehicle-title">${this._escape(vehicle.vehicle_name || vehicle.title || "Fahrzeug")}</div>
                  <div class="mobile-plate-text">${this._escape(vehicle.plate_display || vehicle.plate || "—")}</div>
                </td>
                <td class="hu-cell">
                  <div class="main-value">${this._escape(this._monthYear(vehicle))}</div>
                </td>
                <td class="reminder-cell">
                  <div class="main-value">${this._escape(this._dateLabel(vehicle.reminder_date))}</div>
                </td>
                <td class="status-cell"><span class="status-pill status-${this._escape(this._statusClass(vehicle.status))}">${this._escape(this._statusLabel(vehicle.status))}</span></td>
                <td class="preview-cell">${this._platePreview(vehicle)}</td>
                <td class="menu-cell">
                  <button type="button" class="row-menu" data-menu-index="${index}" data-menu-entry-id="${this._escape(vehicle.entry_id || "")}" title="Aktionen öffnen" aria-label="Aktionen für Fahrzeug öffnen" aria-expanded="${this._openMenuEntryId === vehicle.entry_id ? "true" : "false"}"><span aria-hidden="true">⋮</span></button>
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

  _renderDeleteConfirm() {
    const vehicle = this._selectedVehicle || {};
    const name = vehicle.vehicle_name || vehicle.title || "Fahrzeug";
    const plate = vehicle.plate_display || vehicle.plate || "—";
    return `
      <section class="modal-backdrop" aria-label="Fahrzeug löschen" role="dialog" aria-modal="true">
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
    const errors = this._formValidation();
    const seasonal = ["seasonal", "green_seasonal"].includes(this._form.plate_kind);
    const green = ["green", "green_seasonal"].includes(this._form.plate_kind);
    const change = this._form.plate_kind === "change";
    const plateKinds = this._metadata?.plate_kinds || [
      { value: "standard", label: "Standard" },
      { value: "seasonal", label: "Saisonkennzeichen" },
      { value: "change", label: "Wechselkennzeichen" },
      { value: "green", label: "Grünes Kennzeichen" },
      { value: "green_seasonal", label: "Grünes Kennzeichen + Saison" },
    ];
    const plateFormats = this._metadata?.plate_formats || [
      { value: "single_line", label: "Einzeilig" },
      { value: "two_line", label: "Zweizeilig" },
      { value: "small_two_line", label: "Verkleinert zweizeilig" },
      { value: "motorcycle", label: "Motorrad" },
    ];

    return `
      <section class="modal-backdrop" aria-label="${isDetail ? "Fahrzeugdetails" : "Neues Fahrzeug"}" role="dialog" aria-modal="true">
        <div class="form-shell">
        <div class="form-head">
          <div>
            <h2>${isDetail ? "Fahrzeugdetails" : "Neues Fahrzeug anlegen"}</h2>
            <p>${isDetail ? "Bestehende Reminder-Entität bearbeiten und über die Manager-API speichern." : "Legt ein neues Fahrzeug als normale TÜV-Reminder-ConfigEntry-Entität an."}</p>
          </div>
        </div>

        <div class="form-grid">
          <div class="form-card fields-card">
            <h3>Basisdaten</h3>
            <label>Fahrzeugname<input data-field="vehicle_name" value="${this._escape(this._form.vehicle_name)}" placeholder="z. B. Golf, Anhänger, Motorrad"></label>
            <div class="field-pair">
              <label>HU-Monat<select data-field="month">${this._renderMonthOptions(this._form.month)}</select></label>
              <label>HU-Jahr<input data-field="year" type="number" inputmode="numeric" min="1900" max="2100" step="1" value="${this._escape(this._form.year)}"></label>
            </div>
            <div class="field-pair">
              <label>Intervall<select data-field="interval">${this._renderIntervalOptions(this._form.interval)}</select></label>
              <label>Erinnerungs-Vorlauf Tage<input data-field="reminder_offset_days" type="number" inputmode="numeric" min="0" max="365" step="1" value="${this._escape(this._form.reminder_offset_days)}"></label>
            </div>

            <h3>Kennzeichen</h3>
            <label>Kennzeichenart<select data-field="plate_kind">${this._renderOptionList(plateKinds, this._form.plate_kind)}</select></label>
            <label>Format<select data-field="plate_format">${this._renderOptionList(plateFormats, this._form.plate_format)}</select></label>

            ${change ? `
              <div class="field-pair">
                <label>Gemeinsamer Text<input data-field="change_plate_common_text" value="${this._escape(this._form.change_plate_common_text)}" placeholder="z. B. B AB"></label>
                <label>Fahrzeugziffer<input data-field="change_plate_vehicle_digit" inputmode="numeric" maxlength="1" pattern="[0-9]" value="${this._escape(this._form.change_plate_vehicle_digit)}" placeholder="z. B. 1"></label>
              </div>
            ` : `
              <label>Kennzeichen<input data-field="plate" value="${this._escape(this._form.plate)}" placeholder="z. B. B AB 123"></label>
              <div class="check-row ${green ? "disabled-row" : ""}">
                <label><input type="checkbox" data-field="plate_suffix_h" ${this._form.plate_suffix_h ? "checked" : ""} ${green ? "disabled" : ""}> H-Kennzeichen</label>
                <label><input type="checkbox" data-field="plate_suffix_e" ${this._form.plate_suffix_e ? "checked" : ""} ${green ? "disabled" : ""}> E-Kennzeichen</label>
              </div>
            `}

            ${seasonal ? `
              <h3>Saison</h3>
              <div class="field-pair">
                <label>Startmonat<select data-field="season_start_month">${this._renderMonthOptions(this._form.season_start_month)}</select></label>
                <label>Endmonat<select data-field="season_end_month">${this._renderMonthOptions(this._form.season_end_month)}</select></label>
              </div>
            ` : ""}
          </div>

          <aside class="form-card preview-card">
            <h3>Vorschau</h3>
            <div class="large-preview">${this._platePreviewFromText(this._formPlateText(), {
              green,
              seasonal,
              seasonStart: this._form.season_start_month,
              seasonEnd: this._form.season_end_month,
            })}</div>
            <dl>
              <div><dt>Name</dt><dd data-summary="name">${this._escape(this._form.vehicle_name || "—")}</dd></div>
              <div><dt>HU</dt><dd data-summary="hu">${this._escape(String(this._form.month).padStart(2, "0"))}/${this._escape(this._form.year || "—")}</dd></div>
              <div><dt>Art</dt><dd data-summary="kind">${this._escape(this._kindLabel(this._form.plate_kind))}</dd></div>
              <div><dt>Format</dt><dd data-summary="format">${this._escape(this._formatLabel(this._form.plate_format))}</dd></div>
            </dl>
            <div class="validation ${errors.length ? "has-errors" : "ok"}">
              ${this._validationHtml(errors)}
            </div>
            <p class="note">Erstellen und Bearbeiten laufen über die Reminder-eigene WebSocket-API. Die Card bleibt davon getrennt und liest danach nur die aktualisierten Entities/Attribute.</p>
            <div class="form-actions modal-bottom-actions">
              ${isDetail
                ? `<button class="action" id="save-update" ${errors.length || this._saving || !this._formDirty() ? "disabled" : ""}>${this._saving ? "Speichert …" : "Speichern"}</button>`
                : `<button class="action" id="save-create" ${errors.length || this._saving ? "disabled" : ""}>${this._saving ? "Speichert …" : "Speichern"}</button>`}
              <button class="ghost" id="back-to-list">Schließen</button>
            </div>
          </aside>
        </div>
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
    const visibleCount = this._visibleVehicles().length;
    const listMode = true;
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
        .version { color: var(--secondary-text-color); font-size: 12px; white-space: nowrap; }
        .toolbar {
          display: ${listMode ? "grid" : "none"};
          grid-template-columns: minmax(240px, 1fr) auto auto;
          gap: 8px;
          padding: 10px 16px;
          border-bottom: 1px solid var(--divider-color);
          background: var(--secondary-background-color);
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
        input[type="search"] { padding: 0 12px 0 40px; }
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
          width: auto;
          min-width: 0;
          height: auto;
          padding: 0;
          border: 0;
          border-radius: 0;
          background: transparent;
          color: var(--primary-text-color);
          font-size: 30px;
          font-weight: 300;
          line-height: 1;
          box-shadow: none;
        }
        .list-add-row {
          display: ${listMode ? "flex" : "none"};
          align-items: center;
          justify-content: flex-end;
          padding: 10px 16px;
          border-bottom: 1px solid var(--divider-color);
          background: var(--primary-background-color);
        }
        .list-add-row.bottom {
          border-top: 1px solid var(--divider-color);
          border-bottom: 0;
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
          display: ${listMode ? "flex" : "none"};
          flex-wrap: wrap;
          gap: 16px;
          padding: 10px 16px;
          color: var(--secondary-text-color);
          font-size: 13px;
          border-bottom: 1px solid var(--divider-color);
        }
        .summary-strip strong { color: var(--primary-text-color); font-weight: 500; }
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
        .list-shell { overflow-x: auto; width: 100%; }
        .manager-table { width: 100%; min-width: 940px; border-collapse: collapse; }
        th, td { padding: 10px 14px; text-align: left; vertical-align: middle; border-bottom: 1px solid var(--divider-color); }
        th { height: 32px; color: var(--secondary-text-color); font-size: 12px; font-weight: 600; }
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
        .sort-header:hover, .sort-header.active { color: var(--primary-text-color); }
        .col-preview .sort-header { justify-content: flex-end; }
        tbody tr { cursor: default; }
        tbody tr:hover { background: var(--secondary-background-color); }
        .col-name { width: 38%; }
        .col-preview { width: 240px; text-align: right; }
        .col-menu { width: 48px; }
        .menu-cell { position: relative; text-align: right; overflow: visible; }
        .row-action-menu {
          position: absolute;
          right: 10px;
          top: 40px;
          z-index: 20;
          min-width: 148px;
          padding: 6px 0;
          border: 1px solid var(--divider-color);
          border-radius: 8px;
          background: var(--card-background-color);
          box-shadow: 0 8px 24px rgba(0,0,0,.26);
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
        .row-action-menu button:hover { background: var(--secondary-background-color); }
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
        .vehicle-title { font-weight: 600; line-height: 1.25; }
        .mobile-plate-text { display: none; margin-top: 2px; color: var(--secondary-text-color); font-size: 11px; line-height: 1.2; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .muted { color: var(--secondary-text-color); font-size: 12px; line-height: 1.35; }
        .main-value { font-weight: 500; line-height: 1.25; }
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
        .status-expired { color: var(--error-color); }
        .status-due { color: var(--warning-color, var(--state-icon-active-color)); }
        .status-valid { color: var(--success-color, var(--primary-color)); }
        .tag-row { display: flex; flex-wrap: wrap; gap: 5px; }
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
        .preview-cell { text-align: right; }
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
        .large-preview .plate-preview { height: 54px; max-width: 320px; min-width: 220px; }
        .large-preview .plate-text { font-size: 24px; }
        .large-preview .plate-eu { width: 32px; font-size: 12px; }
        .large-preview .plate-season { min-width: 36px; font-size: 11px; }
        .plate-preview-green { color: #0a7d28; border-color: #0a7d28; }
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
          width: 40px;
          height: 40px;
          min-width: 40px;
          min-height: 40px;
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
        .row-menu:focus-visible {
          background: var(--secondary-background-color);
          color: var(--primary-text-color);
          outline: none;
        }
        .row-menu span {
          pointer-events: none;
          transform: translateY(-1px);
        }
        .state { padding: 24px 16px; }
        .error { color: var(--error-color); }
        .form-shell {
          width: min(1120px, 100%);
          max-height: min(860px, calc(100vh - 64px));
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
        .form-grid { display: grid; grid-template-columns: minmax(360px, 680px) minmax(280px, 420px); gap: 18px; align-items: start; }
        .form-card {
          border: 1px solid var(--divider-color);
          border-radius: 10px;
          background: var(--card-background-color);
          padding: 18px;
          box-sizing: border-box;
        }
        label { display: block; color: var(--secondary-text-color); font-size: 12px; font-weight: 500; }
        label input, label select { margin-top: 6px; color: var(--primary-text-color); font-size: 14px; }
        .field-pair { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
        .check-row { display: flex; flex-wrap: wrap; gap: 18px; margin-top: 10px; }
        .check-row label { display: inline-flex; align-items: center; gap: 8px; color: var(--primary-text-color); font-size: 13px; }
        .check-row input { width: auto; height: auto; margin: 0; }
        .disabled-row { opacity: .55; }
        .preview-card dl { margin: 18px 0; }
        .preview-card dl div { display: flex; justify-content: space-between; gap: 16px; padding: 7px 0; border-bottom: 1px solid var(--divider-color); }
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
          .toolbar { grid-template-columns: 1fr; }
          select, button.action { width: 100%; }
          .summary-strip { gap: 8px 14px; }
          .form-head { grid-template-columns: 1fr; }
          .form-grid { grid-template-columns: 1fr; }
        }
        @media (max-width: 1100px) {
          .toolbar { padding: 8px 10px; }
          .summary-strip { padding: 8px 10px; }
          .list-add-row { padding: 8px 10px; }
          .list-shell { overflow-x: hidden; width: 100%; }
          .manager-table {
            width: 100%;
            min-width: 0;
            table-layout: fixed;
          }
          th, td {
            padding: 8px 6px;
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
          .col-menu { width: 52px; }
          .col-preview, .preview-cell { display: none; }
          .sort-header { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
          .vehicle-title, .main-value { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
          .mobile-plate-text { display: block; }
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
          .version { display: none; }
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
          <button class="action" id="refresh" ${this._loading ? "disabled" : ""}>Aktualisieren</button>
        </section>

        <section class="summary-strip" aria-label="Manager Status">
          <span><strong>${vehicleCount}</strong> Fahrzeuge</span>
          <span><strong>${visibleCount}</strong> Treffer</span>
          <span><strong>${(counts.due || 0) + (counts.expired || 0)}</strong> fällig/abgelaufen</span>
          <span>Reminder-eigene Seite · Create-/Update-/Delete-API aktiv · Duplicate-Schutz · Dirty-Guard · Responsive Tabelle · lokale Formularvalidierung auf Backend-Regeln abgestimmt · nur Drei-Punkte-Menü öffnet Aktionen · sortierbare Spalten · keine Card-Funktionen</span>
        </section>

        ${this._flashMessage ? `<section class="flash ${this._escape(this._flashMessage.tone || "success")}" role="status">${this._escape(this._flashMessage.message)}</section>` : ""}

        <section class="list-add-row top" aria-label="Fahrzeug oben hinzufügen">
          <button class="action icon-action" data-create-trigger="top" title="Neues Fahrzeug anlegen" aria-label="Neues Fahrzeug anlegen">+</button>
        </section>

        <section class="content">
          ${this._renderVehicles()}
        </section>

        <section class="list-add-row bottom" aria-label="Fahrzeug unten hinzufügen">
          <button class="action icon-action" data-create-trigger="bottom" title="Neues Fahrzeug anlegen" aria-label="Neues Fahrzeug anlegen">+</button>
        </section>
        ${formOpen ? (this._view === "delete" ? this._renderDeleteConfirm() : this._renderCreateForm()) : ""}
        ${actionSheetOpen ? this._renderActionSheet() : ""}
      </main>
    `;

    const refreshButton = this.shadowRoot.querySelector("#refresh");
    if (refreshButton) refreshButton.addEventListener("click", () => this._refresh());

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

    const statusFilter = this.shadowRoot.querySelector("#status-filter");
    if (statusFilter) {
      statusFilter.addEventListener("change", (event) => {
        this._statusFilter = event.target.value;
        this._openMenuIndex = null;
        this._openMenuEntryId = null;
        this._renderPreservingListUiState();
      });
    }

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

    const actionSheetBackdrop = this.shadowRoot.querySelector(".action-sheet-backdrop");
    if (actionSheetBackdrop) {
      window.setTimeout(() => actionSheetBackdrop.focus({ preventScroll: true }), 0);
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
        if (event.key === "Escape") this._closeActionSheet({ force: true });
      });
    }

    const modalBackdrop = this.shadowRoot.querySelector(".modal-backdrop");
    if (modalBackdrop) {
      modalBackdrop.addEventListener("click", (event) => {
        if (event.target === modalBackdrop) this._closeForm();
      });
      modalBackdrop.addEventListener("keydown", (event) => {
        if (event.key === "Escape") this._closeForm();
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
