"""Pure conversion helpers. No filesystem, network, or Revit mutations."""
import math


def pdf_calibration(pdf_border, cad_border, relative_tolerance=0.002):
    """Rectangles are (xmin, ymin, xmax, ymax). PDF Y is downward.

    CAD values must already be in the job's chosen drawing units. Reject
    unexplained nonuniform scaling; return (scale, x_offset, y_offset).
    """
    if not 0 <= relative_tolerance < 1:
        raise ValueError("Invalid relative tolerance")
    if len(pdf_border) != 4 or len(cad_border) != 4:
        raise ValueError("Expected two four-coordinate borders")
    if not all(math.isfinite(x) for x in tuple(pdf_border) + tuple(cad_border)):
        raise ValueError("Nonfinite border")
    px0, py0, px1, py1 = pdf_border
    cx0, cy0, cx1, cy1 = cad_border
    if px1 <= px0 or py1 <= py0 or cx1 <= cx0 or cy1 <= cy0:
        raise ValueError("Degenerate or reversed border")
    sx, sy = (cx1-cx0)/(px1-px0), (cy1-cy0)/(py1-py0)
    if abs(sx-sy)/max(sx, sy) > relative_tolerance:
        raise ValueError("Nonuniform scale: verify plot window and borders")
    scale = (sx+sy)/2
    return scale, cx0-scale*px0, cy1+scale*py0


def pdf_point(point, calibration):
    scale, ox, oy = calibration
    return point[0]*scale+ox, oy-point[1]*scale


def cad_point_to_feet(point, millimeters_per_unit, origin=(0, 0)):
    if not math.isfinite(millimeters_per_unit) or millimeters_per_unit <= 0:
        raise ValueError("A positive verified unit conversion is required")
    factor = millimeters_per_unit/304.8
    return ((point[0]-origin[0])*factor,
            (point[1]-origin[1])*factor, 0.0)


def hatch_grid(angle_degrees, offset, base, millimeters_per_unit,
               view_scale, local_origin=(0, 0)):
    """CAD offset vector -> Revit drafting grid values (radians, feet).

    Keep signed normal offset and shift consistent; do not invert only one.
    """
    if view_scale <= 0 or millimeters_per_unit <= 0:
        raise ValueError("Positive units and view scale are required")
    vals = (angle_degrees, *offset, *base, millimeters_per_unit,
            view_scale, *local_origin)
    if not all(math.isfinite(x) for x in vals):
        raise ValueError("Nonfinite grid input")
    a = math.radians(angle_degrees)
    u, n = (math.cos(a), math.sin(a)), (-math.sin(a), math.cos(a))
    factor = millimeters_per_unit/(304.8*view_scale)
    normal = offset[0]*n[0]+offset[1]*n[1]
    if abs(normal) < 1e-12:
        raise ValueError("Zero hatch family spacing")
    return {"angle": a, "offset": normal*factor,
            "shift": (offset[0]*u[0]+offset[1]*u[1])*factor,
            "origin": [(base[i]-local_origin[i])*factor for i in (0, 1)]}


def hatch_segments(cad_segments, feet_per_unit, dot_length_feet):
    """Convert conventional alternating CAD stroke/gap arrays.

    Revit takes nonnegative stroke/gap lengths. Preserve the repetition
    period when expanding dots. Complex CAD arrays require phase-aware
    preprocessing and are rejected, never silently reinterpreted.
    An empty array represents a continuous hatch family.
    """
    if not all(math.isfinite(x) and x > 0 for x in
               (feet_per_unit, dot_length_feet)):
        raise ValueError("Positive finite unit factor and dot length required")
    if len(cad_segments) % 2:
        raise ValueError("Expected complete alternating stroke/gap pairs")
    result = []
    for i in range(0, len(cad_segments), 2):
        stroke, gap = cad_segments[i:i+2]
        if not math.isfinite(stroke) or not math.isfinite(gap):
            raise ValueError("Nonfinite pattern segment")
        if stroke < 0 or gap >= 0:
            raise ValueError("Expected nonnegative CAD stroke then negative gap")
        stroke, gap = stroke*feet_per_unit, -gap*feet_per_unit
        if stroke == 0:
            if dot_length_feet >= gap:
                raise ValueError("Dot must be shorter than its following gap")
            stroke, gap = dot_length_feet, gap-dot_length_feet
        result.extend((stroke, gap))
    return result
