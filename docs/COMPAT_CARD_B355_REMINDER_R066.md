# Compatibility – Card b355 / Reminder r066

Reminder r066 only changes Sidebar create/edit form state normalization before Manager API writes.

The Card-facing entity attributes and the Reminder/Card bridge remain unchanged. Existing Card b355 compatibility is preserved.

The Card remains a separate Dashboard/Lovelace project and is not bundled, imported, rendered or action-duplicated by the Reminder Sidebar.
