# Reminder r012 – Area-Code Selector UI Revert + Manager UI Roadmap

r012 corrects the direction from r011.

## Decision

The normal Home Assistant Config/Options Flow should not receive an additional `plate_area_code` field. The desired UX is browser-like typeahead directly below the existing `plate` text field while the user types, not a separate selector field.

The standard HA Data Entry Flow is not the right place for that typeahead UI because it is schema/step based and does not provide our own live frontend component below a text input.

## Runtime state

r012 returns to the stable r010/r009 runtime behavior:

- no separate area-code field in the flow
- no `plate_area_code`/`plate_area_label` runtime attributes
- no bundled area-code database in the runtime package
- no hard validation against an area-code list
- free plate input remains unchanged

## Future path

Area-code suggestions move to the later Manager/Sidebar UI idea. That UI may use a bundled local list and implement real typeahead behavior, for example:

```text
Kennzeichen*
[ WIL AB 123 ]
  W   – Wuppertal
  WI  – Wiesbaden
  WIL – Bernkastel-Wittlich / Wittlich
```

The list must remain suggestions-only. The entered plate text is authoritative.
