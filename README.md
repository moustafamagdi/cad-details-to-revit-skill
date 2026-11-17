# CAD Details to Revit — Codex Skill

An agent skill for recreating DWG/DXF installation details as editable Revit drafting views and checking the result against native AutoCAD output.

It combines analytic CAD geometry, native plotted appearance, source typography, displayed dimension fidelity and native filled regions. It includes the practical fixes for cached dimensions, tiny linetype fragments, font wrapping, full-circle evaluation and CAD-to-Revit hatch segment conventions.

## Install

Copy the `cad-details-to-revit` folder into your Codex skills directory. Keep this repository's root README and tests outside that directory. Then invoke:

> Use $cad-details-to-revit to convert this CAD detail into an editable drafting view in the active Revit model and compare the result with native CAD.

The skill supports normal automatic selection as well as explicit invocation. Follow your client's skill discovery/reload behavior.

## Requirements and scope

- A connected Revit scripting runtime, such as pyRevit MCP, with permitted model edits.
- Licensed AutoCAD for native DWG plotting, or a supplied native vector plot.
- Optional local analysis libraries: ezdxf, PyMuPDF, fontTools and Poppler. None are vendored.
- The included standalone helpers use Python 3.9+ and the standard library only. Revit-side scripts must use the runtime's supported Python/.NET syntax.

This is a guided workflow and tested math/export-script helpers, **not** a universal unattended converter or compiled add-in. It does not bundle a production Revit importer. Dimensions recreated as lines/text remain nonassociative unless explicitly built with valid Revit references. Font availability and rendering differences require visual QA.

The underlying workflow was exercised in Revit 2024 and AutoCAD 2027. The generalized helpers are unit-tested with synthetic data; this public package has not been certified across other product versions or drawing families.

## Validate

```console
python -m unittest discover -s tests -v
python cad-details-to-revit/scripts/make_cad_script.py --help
```

No tests modify a live model or require customer data. Read `cad-details-to-revit/SKILL.md` for the workflow and links to deeper references.

## Privacy

The repository contains instructions, generic helpers and synthetic tests only. It excludes source drawings, models, screenshots, job manifests, machine paths, element IDs, fonts, credentials and diagnostic logs. Keep all real conversion inputs/outputs in a separate local job folder.

MIT licensed. Third-party applications and libraries retain their own licenses.
