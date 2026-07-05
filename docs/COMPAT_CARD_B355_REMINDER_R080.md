# Compatibility – Card b355 with Reminder r080

Reminder r080 does not change the Reminder entity attributes consumed by Card b355.

## Preserved bridge contract

- Existing Reminder entities remain available through the same Home Assistant entity model.
- Card b355 does not need a code change for r080.
- r080 changes only the Reminder Sidebar Manager frontend filter controls.

## Separation note

No Card source files are bundled into the Reminder integration. The Lovelace Card remains a separate project.
