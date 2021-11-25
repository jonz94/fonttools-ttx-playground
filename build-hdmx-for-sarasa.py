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

originFontHead = font["head"]
originFontHmtx = font["hmtx"]

originFontHead.flags |= headFlagInstructionsMayAlterAdvanceWidth

hdmxTable = newTable("hdmx")
hdmxTable.hdmx = {}

# build hdmx table for odd and hinted ppems only.
for ppem in range(math.floor(sarasaHintPpemMin / 2) * 2 + 1, sarasaHintPpemMax + 1, 2):
    halfUpm = originFontHead.unitsPerEm / 2
    halfPpem = math.ceil(ppem / 2)
    hdmxTable.hdmx[ppem] = {
        name: math.ceil(width / halfUpm) * halfPpem
        for name, (width, _) in originFontHmtx.metrics.items()
    }

font["hdmx"] = hdmxTable

font.save("hdmx-" + filename)
