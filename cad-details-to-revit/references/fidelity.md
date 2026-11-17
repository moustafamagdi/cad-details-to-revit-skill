# Observed pitfalls and successful remedies

These are lessons from a completed detail conversion, not guarantees for every DWG.

| Symptom | Investigation and remedy |
|---|---|
| Giant dimension text or remote geometry in DXF extraction | Compare an unmodified native CAD plot first. Cached graphics and regenerated dimension definitions can differ. Do not infer that the original is defective. |
| Native EXPLODE changes dimension values | Preserve displayed strokes/text from the original native vector plot; use the source for analytic nondimension geometry. |
| Arcs, door diagonals or conduit outlines look absent in Revit | Inspect tiny linetype fragments and output resolution before blaming the parser. Restore matching native lines/arcs when the intended plot appearance is effectively continuous. |
| Every linetype becomes one dashed style | Resolve effective scale and inheritance. Keep centerline/break patterns separate; do not classify by name alone. |
| Condensed labels become wide or collide with leaders | Use the installed source font, cap-height calibration and original baselines/line breaks. Do not fix globally by widening every note. |
| Second title line is left aligned | Preserve paragraph centering or position individual lines at their rendered coordinates. |
| Hatch is sparse or very expensive | Zero-length CAD dot strokes were omitted or became ineffective tiny circles. Use native FillGrids and FilledRegions. |
| Native hatch appears solid gray | Check signed CAD gaps incorrectly passed into Revit's alternating nonnegative segments before changing density. |
| Native hatch is too faint | Compare its line weight and color with native plotted CAD. Adjust task-specific pattern types, then recapture. |
| Full-circle spatial query throws | Unbound curves do not accept normalized evaluation. Use center/non-normalized parameters as appropriate. |
| A conversion reports success but still looks wrong | Transaction success proves persistence, not visual quality. Use side-by-side output and enlarged detail crops. |

Avoid retaining failed intermediate workarounds: guessed dimension reconstruction, one universal font, one dash pattern, a dot represented by thousands of tiny circles, or a claim of exact matching based only on element counts.
