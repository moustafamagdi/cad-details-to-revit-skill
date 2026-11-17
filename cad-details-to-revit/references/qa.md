# Visual acceptance and report

Compare an unmodified native AutoCAD plot with a final Revit capture using the **same verified drawing border**, not screenshots with arbitrary window margins. Retain readable labels showing which image is which. Inspect whole-sheet composition and enlarged crops; thumbnail agreement alone misses typography and dimension errors.

Acceptance checks:

- Same detail inventory, relative positions, border and separations.
- Door diagonals, inner frames, conduit offsets, curves, symbols and leader arrowheads are visible and correctly placed.
- Every source label and displayed dimension value is accounted for; no unexplained missing/extra text. A paragraph split into several TextNotes changes element count without changing content.
- Source font family or an explicitly documented measured fallback; comparable height, width, rotation, baseline and line breaks.
- Titles centered as in the source; no text-leader collisions introduced by conversion.
- Meaningful line patterns retained; no obvious line-weight or segmentation artifacts.
- Hatch shape, coverage, density and contrast comparable at the intended print size. Pattern phase or raster antialiasing may differ; disclose material differences.
- Native editable elements verified. No imported CAD, image or PDF is left as the visible drawing substitute.
- Unsupported geometry and approximations are listed, not hidden by broad exception handling.
- Capture taken **after** the last edit and rechecked against the reference.

Use evidence-based language: "corrected the listed discrepancies and visually checked the final output" is supportable. "100% identical" or an arbitrary similarity percentage is not. If requirements remain unmet, say which ones and continue work where authorized.

Completion report: view name, changes, comparison artifact, dimension associativity, known material differences and actual save/sync status. Keep source files, screenshots, job manifests and diagnostics local unless the user explicitly authorizes sharing them.
