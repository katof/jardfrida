#!/usr/bin/env python3
"""Byggir prentfílur: skjótir figurarnar og QR-kotuna inn í HTML-skjalið."""
import pathlib, sys, segno

HER = pathlib.Path(__file__).parent

# Adressan stendur bert her. Broyt hana, tá ið tilfarið flytur til snar.fo.
ADRESSUR = {
    "loggbok-malli": "https://snar.fo/jardfrida/gongdir/hvadani-kom-malli",
    "loggbok-tunnil": "https://snardev.ctrl.fo/jardfrida/gongdir/tunnil",
    "laerarvegleiding": "https://snardev.ctrl.fo/jardfrida",
    "samanberingarkort": "https://snardev.ctrl.fo/jardfrida",
    "kassatilfar": "https://snardev.ctrl.fo/jardfrida",
}

figurar = (HER / "figurar.svg").read_text(encoding="utf-8")
kortgrafikk = (HER / "kort-grafikk.svg").read_text(encoding="utf-8")


def qr_svg(adressa: str) -> str:
    import io
    buf = io.BytesIO()
    segno.make(adressa, error="m").save(
        buf, kind="svg", border=0, dark="#1F2428",
        xmldecl=False, svgns=True, omitsize=True, svgclass=None, lineclass=None,
    )
    return buf.getvalue().decode("utf-8")


def byggja(navn: str) -> pathlib.Path:
    kelda = HER / f"{navn}.kelda.html"
    html = kelda.read_text(encoding="utf-8")
    html = html.replace("<!--FIGURAR-->", figurar)
    html = html.replace("<!--KORTGRAFIKK-->", kortgrafikk)
    if "<!--QR-->" in html:
        html = html.replace("<!--QR-->", qr_svg(ADRESSUR[navn]))
    if "<!--QRINNI-->" in html:
        inni = qr_svg(ADRESSUR[navn])
        inni = inni[inni.index(">") + 1:inni.rindex("</svg>")]
        html = html.replace("<!--QRINNI-->", inni)
    ut = HER / f"{navn}.html"
    ut.write_text(html, encoding="utf-8")
    return ut


if __name__ == "__main__":
    for navn in sys.argv[1:] or ["loggbok-malli"]:
        print(byggja(navn))
