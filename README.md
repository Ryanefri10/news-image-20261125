# The World in One Image — 25 November 2026

[![make.fun](https://make.fun/badge.svg)](https://make.fun/bounty/news-image-20261125)

Entry for [news-image-20261125](https://make.fun/bounty/news-image-20261125):
sum up Wednesday 25 November 2026's world news in one image.

## The image

`entry.png` — 1024x1024, 129,700 bytes,
sha256 `a915673ed866a7490f058533f848d323538c1dbf305bf7d31dde15ee65bf8f86`

A newspaper front page: masthead dated **WEDNESDAY · 25 NOVEMBER 2026**,
a hero panel on the Riyadh tower strike, a 2×2 grid of the day's other
big stories, and a footer strip of smaller items.

## Stories covered

1. **RIYADH — Houthi drone hits the PIF Tower (hero).** A drone struck
   the 80-storey Public Investment Fund Tower in Riyadh's financial
   district on Tuesday, wounding 11 people — the second hit on the
   skyscraper in five days; the Saudi-led coalition vows a decisive
   response. (Reuters / Saudi Civil Defence, reported 24–25 Nov.)
2. **UKRAINE — shipping war.** Zelenskiy confirms Ukraine's drone
   strike on the Russian cargo ship Sparta II in the Gulf of Finland,
   days after Ukraine sank the Russian corvette Merkury off Libya.
   (Reuters, 24 Nov.)
3. **WASHINGTON — Medal of Freedom.** Trump awards Rudy Giuliani the
   Presidential Medal of Freedom at the White House. (24 Nov.)
4. **CYBER — CIA/ODNI breach.** The CIA and the Director of National
   Intelligence's office suffered a cybersecurity breach of
   unclassified information. (Reuters, 24 Nov.)
5. **COURTS — Huawei verdict.** A US jury convicts Huawei of stealing
   trade secrets, acquitting it of racketeering. (24 Nov.)
6. **ALSO TODAY —** a 5.6-magnitude earthquake hits Nepal's Koshi
   Province; NATO plans early-warning aircraft for Poland; Trump
   pardons Thanksgiving turkeys Freedom and Feathers; Nvidia shares
   slide ~7%.

## How it runs

`main.py` is stdlib only (hashlib, os, struct, sys, pathlib, zlib). It
loads the vendored `entry.png`, validates the PNG signature, IHDR
(1024×1024, 8-bit RGB), every chunk's length and CRC through IEND,
the 1 MiB size cap and the sha256 digest, then copies it to
`$MAKEFUN_OUTPUT_DIR/entry.png`. Run twice, the outputs are
byte-identical.

## License

MIT — see `LICENSE`.
