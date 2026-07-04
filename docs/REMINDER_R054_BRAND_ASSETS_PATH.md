# Reminder r054 – Brand Assets Path / Proxy Readiness

r054 fixes the project packaging for Home Assistant local brand images.

## Why this exists

Home Assistant 2026.3 introduced local brand images for custom integrations. The images must live inside the integration folder:

```text
custom_components/tuev_reminder/brand/icon.png
custom_components/tuev_reminder/brand/logo.png
```

Home Assistant can then serve them through the local brands proxy endpoint:

```text
/api/brands/integration/tuev_reminder/icon.png
/api/brands/integration/tuev_reminder/logo.png
```

## r054 change

Earlier ZIPs only carried the brand assets at repository root:

```text
brand/icon.png
brand/logo.png
```

r054 keeps those root-level files for repository/HACS compatibility and additionally packages the required integration-local assets:

```text
custom_components/tuev_reminder/brand/icon.png
custom_components/tuev_reminder/brand/logo.png
```

## Validation

New script:

```text
scripts/check_r054_brand_assets_path.py
```

The check fails if the manifest domain/version or either brand location is missing.

## Scope

No runtime behavior changed. The Sidebar CRUD work from r041-r053 remains unchanged.
