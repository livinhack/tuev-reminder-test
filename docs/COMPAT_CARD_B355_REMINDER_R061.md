# Compatibility – Card b355 with Reminder r061

r061 changes only the Reminder Manager write validation for `reminder_offset_days` and a Sidebar modal label. Sensor/Card bridge attributes, services, calendar behavior, Manager CRUD payload shape, brand asset paths, and Sidebar action behavior are unchanged from r060.

The Lovelace/Dashboard Card remains a separate project. Reminder r061 still provides the same Card-facing attributes and does not import Card code or duplicate Card actions.
