---
name: cad-details-to-revit
description: Recreate DWG or DXF installation details as editable Revit drafting views, with native CAD visual comparison, text and dimension fidelity, analytic curves, and native filled regions. Use for CAD detail conversion or correcting a previous conversion; not for 3D modeling or merely linking CAD.
---

# CAD details to editable Revit

Produce editable detail curves, TextNotes and FilledRegions in the user's intended model. Preserve the source's visible content and composition; a successful API transaction is not evidence of visual fidelity.

## Start with evidence

1. Identify the active Revit document, process, version, policy and view through the connected Revit tool. Never reuse process, document, view, type or element IDs from another task. If a modal dialog blocks access, let the user resolve it.
2. Read the runtime's scripting guidance before running model code. Use its dry-run and approval mechanisms; do not bypass them with another execution channel. The pyRevit runtime used during development blocks save, sync and export inside guarded scripts. Its separate view-capture tool is suitable for QA.
3. Inspect CAD units, extents, layers, fonts, block transforms, dimensions and hatch definitions. Record source identity and calibration in a local job manifest. Keep it outside this skill and outside any public repository.
4. Obtain a native AutoCAD plot **before conversion**. Compare this with the extracted DXF and PDF primitives. Stale dimension graphics, nonzero Z, block transforms and misleading unit metadata can make extraction look broken while AutoCAD displays the drawing correctly. Do not blame the source until native output confirms the defect.

Read [the extraction workflow](references/extraction.md) for native plotting, calibration, text and geometry handling.

## Choose the conversion route

- Prefer **analytic DXF geometry** for lines, arcs, circles and polyline bulges. Transform nested blocks exactly once and project the intended 2D drawing onto its drafting plane.
- Use a **native CAD vector plot as the appearance reference** and, when useful, as the source for displayed dimension strokes, arrowheads, text baselines and explicit line breaks. A PDF is evidence, not a substitute image placed in Revit.
- Preserve circles/arcs as native analytic curves. Prefer source geometry to thousands of micro-segments. Map CAD linetypes using their actual effective scale, not merely their name.
- Preserve source font families, dimensions and positions. Resolve installed fonts locally; do not redistribute font files. Use a measured fallback only if the original is unavailable, and report the substitution.
- Convert patterned hatches to **native FilledRegions** where feasible, with separate fill types/patterns scoped to the task. Avoid tens of thousands of point circles and short detail lines.
- Keep dimension values as displayed in the source. Unless the user requests associative Revit dimensions and reliable references exist, use editable strokes and text and clearly report that limitation. Do not silently infer replacement measurements from schematic geometry.

Read [Revit construction](references/revit.md) before edits, and [verified pitfalls and remedies](references/fidelity.md) when diagnosing discrepancies.

## Build efficiently and reversibly

Compute and validate a neutral geometry/text/fill payload outside Revit. Inspect unsupported entities, extents, text inventory and element estimates before model changes. Helpers in `scripts/conversion_math.py` implement calibration and hatch conversions; they do not modify Revit.

Create or update the intended drafting view with task-owned types. A job manifest should record the created view and element IDs, source hash, calibration, view scale, conversion choices and any approximations. On reruns, inspect the view and replace only the prior job's owned elements. Never delete every element in an existing view merely because its name matches.

Dry-run first, then commit the reviewed change. Roll back on unhandled failures. Record short/unsupported geometry explicitly; do not stretch, silently discard or replace it with arbitrary strokes. Do not repeatedly rebuild the whole view for typography or pattern adjustments: make targeted, verified corrections.

## Finish with visual proof

Read [the QA checklist](references/qa.md). Capture the Revit result, compare it with native CAD at matching extents, and inspect enlarged crops of every distinct detail. Check text, dimensions, arrowheads, outlines, linetypes, hatch density and border placement. Confirm no ImportInstance, image or PDF remains as the drawing's visible substitute.

Fix discrepancies and recapture after the last change. Never claim a percentage or exact match without a defined measurement. Report the view name, what was corrected, known approximations, whether dimensions are associative, and actual save/sync status. Save comparison artifacts only to the user's task outputs.

## Local prerequisites

This is an agent workflow, not a one-click Revit add-in. It needs a connected Revit scripting runtime. Native DWG plotting additionally needs a licensed AutoCAD installation or a user-provided native vector plot. Offline analysis may use ezdxf, PyMuPDF, fontTools and Poppler as available. Discover tool and executable paths on the current machine. No dependency, account, credential or model path is bundled.
