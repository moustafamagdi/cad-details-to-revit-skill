# Extraction and source calibration

## Native appearance first

Keep the original DWG unchanged. Run read-only extraction and plotting against a scratch copy or an unsaved AutoCAD Core Console session. Redirect logs into the local job folder, run background processes hidden, and track only processes created by this job. Use bounded waits with progress updates. Never terminate a user's AutoCAD session to unblock a helper.

AutoCAD Core Console can export DXF and plot a specified model-space window. See `scripts/make_cad_script.py` for a parameterized command-file generator. Discover the installed executable, plotter configuration, paper name and plot style. Those vary across installations. The generator does not launch AutoCAD or save the DWG.

Observed command details:

- Set FILEDIA and BACKGROUNDPLOT to zero in the disposable session.
- `-PLOT`'s legacy wireframe option `_W` worked in the tested model-space workflow; the literal `_As displayed` caused the subsequent filename to be interpreted as a command. Inspect the log for the actual prompts and verify a nonempty PDF.
- Model and paper-space prompt sequences differ. Adapt rather than sending the same sequence blindly.
- DXFOUT with ASCII precision 16 provides analyzable geometry. A PDF viewer and a DXF renderer can disagree with native CAD for cached dimensions.
- Legacy EXPLODE command behavior can be single-entity in AutoLISP. If explosion is necessary, verify the command version and resulting entity counts. Repeatedly sending a nil selection can leave a command waiting for input.
- **Do not explode dimensions to obtain their appearance without verification.** Native explosion can regenerate previously cached dimensions and alter values, text heights or coordinates. Keep the unmodified plot as the authority for what the user asked to reproduce.

## Calibration

Use an actual CAD border or known reference geometry to align source and plot coordinates. Page size, plot window, margins, orientation and drawing extents are not interchangeable. PDF Y points down; Revit drafting Y points up. Validate a second independent length and both axes. Reject unexplained nonuniform scaling. Recenter the resulting detail near the view origin to avoid remote-coordinate problems.

Units in INSUNITS may conflict with the dimensions and schematic layout. Resolve the ambiguity using source geometry and native output; do not automatically assume inches or millimeters. Distinguish:

- geometric drawing units;
- annotation heights at the chosen view scale;
- PDF points and print scaling;
- Revit internal feet.

For a schematic detail, displayed dimension overrides are content, not reliable calibration lengths. A label can intentionally differ from the measured graphic length.

## Text

PDF text spans can supply the rendered font, baseline, rotation and explicit line breaks. Preserve them as native TextNotes. Splitting a multiline paragraph into correctly positioned single-line notes is a useful fidelity route when Revit and CAD wrap differently; disclose the resulting editing tradeoff if relevant.

Font point size is an em measure, whereas CAD text height often corresponds to capitals. Derive cap-height ratios from the installed font, not a universal constant. A baseline-to-top conversion must account for rotation. Verify against actual Revit output before applying the conversion to every text size.

Keep visible underline strokes or TextNote underlining, not both. Respect paragraph centering independently from the insertion-point attachment. Do not set every note to Arial or globally widen text boxes: this changes the drawing's composition and can create collisions. Font families such as condensed engineering fonts may already be installed locally.

## Geometry

Walk nested INSERTs with composed transforms once; evaluate OCS and polyline bulges. Project to the drawing plane only after the transforms. Nonzero Z by itself does not invalidate a 2D installation detail.

Native vector PDF extraction can provide curves and small stroke fragments. Check all emitted primitive types, clipping, closed paths, fill rules, quadrilaterals, orientation and zero-length round-cap dots. Separate fill topology from strokes. Complex fills may need polygon union or containment analysis; do not pass intersecting loops blindly to FilledRegion.Create.

Very fine CAD linetypes can look continuous in native plotting but become invisible when recreated as thousands of short Revit curves. This was an observed rendering difference, not proof that a PDF parser had omitted geometry. Compare analytic source lines with extracted fragments and restore continuous analytic lines only when their visible appearance supports that treatment. Do not globally convert architectural centerlines to solid lines.

Native circles and arcs are preferable to cubic spline reconstructions when the source offers them. When replacing fragments, confirm geometric correspondence and remove only their owned counterparts. Merely detecting one overlapping fragment is not a reliable full-coverage test.
