"""Generate a disposable AutoCAD model-space DXF/vector-PDF export script.

Does not launch AutoCAD, explode entities, save DWGs, or modify a model.
Validate installed plotter/paper/style names before running generated code.
"""
import argparse
from pathlib import Path


def lisp_string(value):
    # Reject control characters rather than letting paths become commands.
    if any(ord(c) < 32 for c in value):
        raise ValueError("Control characters are not allowed")
    return '"' + value.replace('\\', '/').replace('"', '\\"') + '"'


def make_script(dxf_path, pdf_path, window, plotter, paper, style):
    x0, y0, x1, y1 = window
    import math
    if not all(math.isfinite(v) for v in window) or x1 <= x0 or y1 <= y0:
        raise ValueError("Expected a finite nondegenerate plot window")
    args = ["_.-plot", "_Y", "Model", plotter, paper, "_Millimeters",
            "_Portrait", "_No", "_Window", "%g,%g" % (x0, y0),
            "%g,%g" % (x1, y1), "_Fit", "_Center", "_Yes", style,
            "_Yes", "_W", str(pdf_path), "_No", "_Yes"]
    return '\n'.join([
        '(setvar "FILEDIA" 0)', '(setvar "BACKGROUNDPLOT" 0)',
        '(command "_.dxfout" %s "16")' % lisp_string(str(dxf_path)),
        '(command %s)' % ' '.join(lisp_string(v) for v in args), ''])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--dxf', type=Path, required=True)
    parser.add_argument('--pdf', type=Path, required=True)
    parser.add_argument('--window', type=float, nargs=4, required=True,
                        metavar=('XMIN', 'YMIN', 'XMAX', 'YMAX'))
    parser.add_argument('--plotter', required=True)
    parser.add_argument('--paper', required=True)
    parser.add_argument('--style', required=True)
    args = parser.parse_args()
    paths = [p.resolve() for p in (args.output, args.dxf, args.pdf)]
    if len(set(paths)) != 3 or any(p.exists() for p in paths):
        parser.error('Use distinct new output paths; overwriting is refused')
    if [p.suffix.lower() for p in paths] != ['.scr', '.dxf', '.pdf']:
        parser.error('Expected .scr, .dxf and .pdf outputs')
    if not all(p.parent.is_dir() for p in paths):
        parser.error('Create output directories first')
    code = make_script(paths[1], paths[2], args.window,
                       args.plotter, args.paper, args.style)
    paths[0].write_text(code, encoding='utf-8')


if __name__ == '__main__':
    main()
