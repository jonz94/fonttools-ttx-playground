#! /usr/bin/python

# usage:
#   python build-hdmx-for-sarasa.py your-sarasa-font.ttf

# credit: https://github.com/be5invis/Sarasa-Gothic/issues/108#issuecomment-517240248

import sys
import math

from fontTools.ttLib import TTFont, newTable

headFlagInstructionsMayAlterAdvanceWidth = 0x0010
sarasaHintPpemMin = 11
sarasaHintPpemMax = 48

filename = sys.argv[1]

font = TTFont(filename, recalcBBoxes=False)

head_ = font["head"]
hmtx_ = font["hmtx"]
name_ = font["name"]

head_.flags |= headFlagInstructionsMayAlterAdvanceWidth

for entry in name_.names:
    if entry.nameID in [1, 3, 4, 16, 18, 21]:
        entry.string = (
            "hdmx: ".encode(
                "utf_16_be"
                if entry.platformID == 3 and entry.platEncID in [1, 10]
                else "ascii"
            )
            + entry.string
        )
    if entry.nameID in [6, 20]:
        entry.string = (
            "hdmx:".encode(
                "utf_16_be"
                if entry.platformID == 3 and entry.platEncID in [1, 10]
                else "ascii"
            )
            + entry.string
        )

hdmx_ = newTable("hdmx")
hdmx_.hdmx = {}

# build hdmx table for odd and hinted ppems only.
for ppem in range(math.floor(sarasaHintPpemMin / 2) * 2 + 1, sarasaHintPpemMax + 1, 2):
    halfUpm = head_.unitsPerEm / 2
    halfPpem = math.ceil(ppem / 2)
    hdmx_.hdmx[ppem] = {
        name: math.ceil(width / halfUpm) * halfPpem
        for name, (width, _) in hmtx_.metrics.items()
    }

font["hdmx"] = hdmx_

font.save("hdmx-" + filename)
