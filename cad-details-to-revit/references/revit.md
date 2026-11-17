# Revit construction

## Runtime boundaries

Discover the active session/document and query available ViewFamilyType, TextNoteType, FilledRegionType and graphics styles. Choose drafting types by ViewFamily.Drafting. Never hard-code IDs or use another model's types. For a new view, generate a collision-free name. For an update, verify the intended existing view and job ownership manifest.

Use the connected runtime's documented imports, transactions and dry-run mechanism. Typical native APIs are ViewDrafting.Create, NewDetailCurve, TextNote.Create and FilledRegion.Create. Inspect current runtime API signatures before unfamiliar calls. UI navigation and screenshot/export tools have different transaction restrictions from model mutation.

Create all geometry in the drafting plane. Use view.Scale explicitly. Revit internal geometric units are feet; text-size parameters are paper-space feet. Type changes affect every instance of that type: duplicate task-specific types instead of modifying project-wide styles.

## Lines and dimensions

Use native lines, arcs and circles. Apply task-scoped line styles and weights. Preserve meaningful dash/dot differences and effective linetype scales. Resolve ByLayer and ByBlock inheritance with block transforms. A linetype called HIDDEN or CENTER is not sufficient to determine its visible print appearance.

Preserve displayed dimension values, positions and arrows from native CAD. Strokes plus TextNotes are editable but **not associative dimensions**. Rebuilding dimensions from malformed or overridden definition points can move dimension lines, alter arrowheads and produce incorrect values. Use associative Dimension elements only when the required geometric references and scale semantics are established.

Do not normalize every Curve.Evaluate call: a full-circle arc can be unbound. For spatial tests, use its center or a valid nonnormalized parameter. Respect app.ShortCurveTolerance and report any geometry requiring approximation.

## Filled regions: signed CAD vs Revit grids

Prefer five native regions to thousands of hatch strokes when there are five actual hatch areas; do not make the original project's region count a requirement.

Map hatch boundaries to planar CurveLoops, including holes and separate islands. Reject self-intersections and short edges that cannot be represented faithfully. Use the correct solid/foreground/background pattern settings and verify IsMasking. Avoid inheriting unwanted white masking or background fills.

For each CAD hatch family with angle a and offset vector (dx, dy):

```
u = (cos(a), sin(a))
n = (-sin(a), cos(a))
shift  = dot(offset, u)
offset = dot(offset, n)
```

Revit accepts signed grid offsets. Preserve a consistent offset/shift pair. Convert drawing lengths to paper feet for a drafting pattern using the intended view scale. Grid origins must be transformed into the same local frame; verify alignment in the actual region, since host orientation and origin behavior can vary.

**CAD pattern dash arrays use positive strokes, negative gaps and zero dots. Revit FillGrid.SetSegments uses alternating nonnegative stroke and gap lengths. Do not pass CAD's signed array directly.** A technically accepted negative array produced a flat gray region instead of concrete in the observed workflow.

Use `scripts/conversion_math.py` for conventional alternating dash/gap arrays. Its helper deliberately rejects more complex encodings instead of guessing a phase. Represent a dot with a small positive stroke and shorten the following gap to preserve the repeat length. Validate the dot size against the source output. Avoid a repeated ExpandDots call that changes already-expanded patterns.

FillPatternElement creation/update, task-scoped FilledRegionTypes and FilledRegion.Create form the native route. After creation, inspect pattern contrast at the intended output resolution. FilledRegionType.LineWeight affects pattern appearance: the tested drawing needed a heavier pattern weight than the initial choice. **The successful numeric weight from one project is not universal**; use the current project's line-weight table and native CAD print reference.

## Optimization and reruns

- Parse and deduplicate outside Revit; preserve a source-to-element map.
- Prefer analytic curves and native fill patterns from the first pass.
- Batch stable creation work into a focused transaction; use short targeted transactions for subsequent typography/graphics fixes.
- Do not silently catch and skip entity failures. Return a bounded error summary and roll back a failed batch.
- On reruns, compare ownership and current edits before replacing existing content. If the manifest is missing, inspect and establish ownership rather than deleting the whole view.
- Preserve old working content until the replacement has passed a dry run. An unchanged view name alone is not an ownership boundary.
- Leave model save/sync to the user's instruction and the runtime's capabilities; report what actually happened.
