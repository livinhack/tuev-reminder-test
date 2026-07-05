# Compatibility – Card b355 / Reminder r065

Reminder r065 only changes Sidebar frontend keyboard/focus handling for dialogs and action overlays.

It does not change:

- sensor entity attributes,
- Card bridge attributes,
- service names,
- due-date calculation,
- Manager API payload semantics,
- plate data semantics,
- calendar behavior.

The Card remains a separate Dashboard/Lovelace project and is not bundled or imported by Reminder r065.
