from pathlib import Path

import pytest

from glyphsynth import Drawing, Properties, ShapeProperties, TextProperties

from .conftest import write_drawing
from .glyphs import CENTER, HALF, ORIGIN, UNIT, BasicDrawing, BasicParams


def test_group(output_dir: Path):
    drawing = BasicDrawing()

    g1 = drawing.create_group()
    g2 = drawing.create_group()

    g1.draw_circle((HALF, HALF), UNIT / 3, properties=ShapeProperties(fill="green"))
    g2.draw_circle((HALF, HALF), UNIT / 4, properties=ShapeProperties(fill="blue"))

    g1.insert_drawing(
        BasicDrawing(params=BasicParams(color1="orange", color2="yellow")).rotate(90)
    )

    write_drawing(output_dir, drawing)


def test_fill(output_dir: Path):
    drawing = Drawing(size=(UNIT, UNIT))

    gradient1 = drawing.create_linear_gradient(
        start=ORIGIN, end=(UNIT, UNIT), colors=["red", "purple"]
    )
    gradient2 = drawing.create_radial_gradient(
        center=(HALF, HALF),
        radius=HALF,
        focal=(HALF / 2, HALF / 2),
        colors=["blue", "yellow"],
    )

    rect = drawing.draw_rect(ORIGIN, (UNIT, UNIT))
    rect.fill(gradient=gradient1)

    circle = drawing.draw_circle(
        (HALF, HALF), HALF, properties=ShapeProperties(opacity=0.8)
    )
    circle.fill(gradient=gradient2)

    write_drawing(output_dir, drawing)


def test_path(output_dir: Path):
    drawing = Drawing(size=(UNIT, UNIT))

    path = (
        drawing.draw_path((10, 10), properties=ShapeProperties(stroke="black"))
        .line_to((40, 10))
        .horizontal_to(10, relative=True)
        .vertical_to(40)
        .cubic_to((60, 60), (70, 30), (90, 50))
        .smooth_cubic_to((80, 90), (50, 90))
        .quadratic_to((30, 90), (20, 70))
        .smooth_quadratic_to((10, 50))
        .arc_to((10, 30), 10, large_arc=True, sweep=False)
        .close()
    )
    path.fill("none")

    d = path._element.get_xml().get("d")
    assert d == (
        "M 10 10 L 40 10 h 10 V 40 C 60 60 70 30 90 50 S 80 90 50 90 "
        "Q 30 90 20 70 T 10 50 A 10 10 0 1 0 10 30 Z"
    )

    write_drawing(output_dir, drawing)


def test_arc(output_dir: Path):
    drawing = Drawing(size=(UNIT, UNIT))
    props = ShapeProperties(stroke="black", stroke_width=2, fill="none")

    # quarter arc, clockwise
    arc = drawing.draw_arc(CENTER, HALF / 2, 0, 90, properties=props)
    assert arc._element.get_xml().get("d") == "M 75.0 50.0 A 25.0 25.0 0 0 1 50.0 75.0"

    # large counterclockwise elliptical arc
    arc = drawing.draw_arc(CENTER, (40, 20), 0, -270, properties=props)
    assert arc._element.get_xml().get("d") == "M 90.0 50.0 A 40 20 0 1 0 50.0 70.0"

    # full circle split into two arcs
    arc = drawing.draw_arc(CENTER, 10, 0, 360, properties=props)
    assert arc._element.get_xml().get("d") == (
        "M 60.0 50.0 A 10 10 0 0 1 40.0 50.0 A 10 10 0 0 1 60.0 50.0"
    )

    # pie slice
    pie = drawing.draw_path(CENTER).arc(CENTER, 45, -90, 0).close()
    pie.fill("red", opacity_pct=50)
    assert pie._element.get_xml().get("d") == (
        "M 50.0 50.0 L 50.0 5.0 A 45 45 0 0 1 95.0 50.0 Z"
    )

    write_drawing(output_dir, drawing)


def test_text(output_dir: Path):
    drawing = Drawing(
        size=(UNIT, UNIT), properties=Properties(fill="blue", stroke_width=5)
    )

    text = drawing.draw_text(
        "Hello",
        (10, 30),
        properties=TextProperties(font_size="20px", font_family="sans-serif"),
    )
    text.add_span(" world", dy=5, properties=TextProperties(fill="red"))

    xml = text._element.get_xml()
    assert xml.get("font-size") == "20px"
    assert xml.get("fill") == "blue"
    assert xml.get("stroke-width") == "5"

    span = xml.find("tspan")
    assert span is not None
    assert span.text == " world"
    assert span.get("fill") == "red"
    assert span.get("dy") == "5"

    curve = drawing.draw_path((10, 80)).quadratic_to((50, 40), (90, 80))
    curve.fill("none")
    text_path = drawing.draw_text(
        properties=TextProperties(font_size="10px")
    ).add_text_path(curve, "along a curve", start_offset="10%")

    xml = text_path._element.get_xml()
    assert xml.text == "along a curve"
    assert xml.get("startOffset") == "10%"
    assert xml.get("xlink:href") == curve.iri

    write_drawing(output_dir, drawing)


def test_image(output_dir: Path):
    drawing = Drawing(size=(UNIT, UNIT))

    image = drawing.draw_image(
        "data:image/svg+xml;base64,"
        "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAx"
        "IDEiPjxyZWN0IHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9InJlZCIvPjwvc3ZnPg==",
        insert=(10, 10),
        size=(80, 40),
    )
    image.fit(horiz="left", vert="top", scale="slice").rotate(10)

    xml = image._element.get_xml()
    assert xml.get("preserveAspectRatio") == "xMinYMin slice"
    assert xml.get("x") == "10"

    write_drawing(output_dir, drawing)


def test_symbol_use(output_dir: Path):
    drawing = Drawing(size=(UNIT, UNIT))

    symbol = drawing.create_symbol().viewbox(0, 0, 10, 10)
    symbol.draw_circle((5, 5), 4, properties=ShapeProperties(fill="green"))

    use1 = drawing.draw_use(symbol, insert=(0, 0), size=(50, 50))
    use2 = drawing.draw_use(symbol.iri, insert=(50, 50), size=(50, 50))

    assert use1._element.get_xml().get("xlink:href") == symbol.iri
    assert use2._element.get_xml().get("xlink:href") == symbol.iri

    write_drawing(output_dir, drawing)


def test_marker(output_dir: Path):
    drawing = Drawing(size=(UNIT, UNIT))

    arrow = drawing.create_marker((4, 4), ref=(2, 2), units="strokeWidth")
    arrow.viewbox(0, 0, 4, 4)
    arrow.draw_polygon([(0, 0), (4, 2), (0, 4)], ShapeProperties(fill="black"))

    dot = drawing.create_marker((3, 3), ref=(1.5, 1.5), orient=None)
    dot.viewbox(0, 0, 3, 3)
    dot.draw_circle((1.5, 1.5), 1.5, ShapeProperties(fill="red"))

    line = drawing.draw_polyline(
        [(10, 90), (50, 50), (90, 20)],
        properties=ShapeProperties(stroke="black", stroke_width=3, fill="none"),
    ).markers(start=dot, mid=dot.iri, end=arrow)

    xml = line._element.get_xml()
    assert xml.get("marker-start") == dot.funciri
    assert xml.get("marker-mid") == dot.funciri
    assert xml.get("marker-end") == arrow.funciri

    marker_xml = arrow._element.get_xml()
    assert marker_xml.get("orient") == "auto"
    assert marker_xml.get("markerUnits") == "strokeWidth"

    write_drawing(output_dir, drawing)


def test_pattern(output_dir: Path):
    drawing = Drawing(size=(UNIT, UNIT))

    pattern = drawing.create_pattern((10, 10))
    pattern.draw_circle((5, 5), 3, ShapeProperties(fill="purple"))

    rect = drawing.draw_rect(ORIGIN, (UNIT, UNIT)).fill(pattern=pattern)
    circle = drawing.draw_circle(CENTER, 30).fill("none")
    circle.stroke(None, pattern=pattern, width=8)

    assert rect._element.get_xml().get("fill") == pattern.funciri
    assert circle._element.get_xml().get("stroke") == pattern.funciri
    assert pattern._element.get_xml().get("patternUnits") == "userSpaceOnUse"
    assert pattern.get_paint_server() == f"{pattern.funciri} none"

    write_drawing(output_dir, drawing)


def test_clip_mask(output_dir: Path):
    drawing = Drawing(size=(UNIT, UNIT))

    clip = drawing.create_clip_path(units="userSpaceOnUse")
    clip.draw_circle(CENTER, 40)

    mask = drawing.create_mask(insert=ORIGIN, size=(UNIT, UNIT), units="userSpaceOnUse")
    mask.draw_rect(ORIGIN, (UNIT, UNIT), properties=ShapeProperties(fill="white"))
    mask.draw_rect(ORIGIN, (HALF, UNIT), properties=ShapeProperties(fill="black"))

    rect = drawing.draw_rect(ORIGIN, (UNIT, UNIT)).fill("blue").clip_path(clip)
    group = drawing.create_group().mask(mask)
    group.draw_circle(CENTER, 20, ShapeProperties(fill="yellow"))

    assert rect._element.get_xml().get("clip-path") == clip.funciri
    assert group._element.get_xml().get("mask") == mask.funciri

    mask_xml = mask._element.get_xml()
    assert mask_xml.get("maskUnits") == "userSpaceOnUse"
    assert mask_xml.get("width") == str(UNIT)

    write_drawing(output_dir, drawing)


_SVG = """<?xml version="1.0"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="200" height="100" viewBox="10 10 100 50" fill="red">
  <defs><linearGradient id="lg"><stop offset="0" stop-color="blue"/></linearGradient></defs>
  <rect x="10" y="10" width="50" height="50" fill="url(#lg)"/>
  <text x="20" y="40">Hello <tspan>world</tspan></text>
  <use xlink:href="#lg"/>
</svg>
"""


def test_load_svg(output_dir: Path):
    drawing = Drawing(size=(UNIT, UNIT))

    imported = drawing.load_svg(_SVG)
    assert imported.size == (200, 100)
    assert imported.original_viewbox == (10, 10, 100, 50)

    imported.rotate(15, center=(50, 25)).translate(5, 5)

    out = drawing._drawing.tostring()
    assert "<svg" in out and out.count("<svg") >= 1
    assert 'xlink:href="#lg"' in out
    assert "Hello" in out and "<tspan>world</tspan>" in out
    assert 'fill="red"' in out
    assert "scale(2" in out and "translate(-10" in out

    # from file
    path = output_dir / "imported.svg"
    path.write_text(_SVG)
    assert drawing.load_svg(path).size == (200, 100)

    with pytest.raises(ValueError):
        drawing.load_svg("<html/>")

    write_drawing(output_dir, drawing)
