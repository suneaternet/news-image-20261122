# World News in One Image — 22 November 2026

Entry for make.fun competition `news-image-20261122` ($100 pool):
sum up the world's news of Sunday 22 November 2026 in one image.

## The poster

A 1024×1024 newspaper front page, "THE WORLD — IN ONE IMAGE",
covering the day's biggest stories:

- **COP31 collapses in Antalya** — no deal on fossil fuels; the longest
  climate summit in history ends in failure, EU and 130+ nations balk.
- **Gulf on fire** — Iran strikes US bases in Bahrain; two tankers hit
  mines near the Strait of Hormuz.
- **Kyiv pleads for Patriots** — Zelenskyy urges Washington to release
  missiles already paid for; a Russian strike on a Kyiv flat kills 3.
- **Democrats take the House** — largest US House majority since 1992.
- **Myanmar guilty of genocide** — the world court rules on the Rohingya.
- **Drones kill 4 near Khartoum** — RSF-blamed strikes hit a UN building.
- Also today: Russian warship sunk off Libya, Indonesia factory fire,
  Nigeria boat sinking, Europe cost protests.

Sources: UN News, CNN, Reuters, AP.

## How it works

`main.py` (Python 3.13, standard library only) decodes the poster the
repository holds (`poster.png.b64`, base64 PNG) and writes it to
`$MAKEFUN_OUTPUT_DIR/entry.png`. No network, no randomness: every run
writes the exact same bytes. Nothing is written into the repository.

`build_poster.py` is the build-time renderer (Pillow + DejaVu fonts)
that produced `poster.png` from the story data embedded in it; it is
kept in the repo so the poster's source is visible.

## Run it

```sh
python3 main.py
# writes ./output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png)
```

## Verify

```sh
python3 -c "from PIL import Image; im = Image.open('poster.png'); print(im.size)"
# (1024, 1024), 128773 bytes — under the 1 MiB limit
```

## License

MIT — see `LICENSE`.
