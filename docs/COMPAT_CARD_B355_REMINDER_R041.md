# Compatibility – Card b355+ / b356 RC with Reminder r042

Reminder r042 preserves the Card-facing bridge contract from the previous r040 state.

The change is limited to the Reminder-owned Sidebar create form save path. Sensor attributes, services, calendar behavior, Card renderer behavior and Dashboard Card configuration remain unchanged.

The Card should continue to consume Reminder entities exactly as before. Newly created Reminder entries should become ordinary Reminder entities and can then be selected/used by the Card through the existing entity/attribute contract.
