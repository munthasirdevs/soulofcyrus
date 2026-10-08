REX PORTFOLIO — EXTRACT ALL FOUR ZIP FILES

This delivery contains four ordinary, independently extractable ZIP files:
1. REX-Portfolio-01-Source.zip — code, content, developer README and checksums
2. REX-Portfolio-02-Media.zip — media part 1
3. REX-Portfolio-03-Media.zip — media part 2
4. REX-Portfolio-04-Media.zip — media part 3

Download all four files. Extract ALL FOUR into the SAME parent directory,
allowing their REX-Portfolio folders to merge. No files need to be overwritten:
the source and media files are distributed between the ZIPs, not duplicated.
The resulting single REX-Portfolio folder must contain render_site.py, README.md,
validate_package.py, SHA256SUMS.txt and dist/ with its complete assets/ tree.

Some unzip apps create a separate folder for every ZIP automatically. If yours
does, merge the contents of the four REX-Portfolio folders into ONE REX-Portfolio
folder while preserving every subfolder and filename. Do not put one
REX-Portfolio folder inside another. Do not place the ZIP files inside dist/.

Once all four are extracted and merged, open REX-Portfolio/README.md for full
run, edit, build and hosting instructions. In that folder run:

  python3 validate_package.py
  python3 -m http.server 8000 --bind 127.0.0.1 --directory dist

Then open http://127.0.0.1:8000/ in a browser. On Windows, use py -3 if python3
is not available. The source ZIP alone is not a complete working media bundle.
All media files are web-ready assets from the current portfolio; original
editable design/video master files are not included.

The merged REX-Portfolio folder is byte-for-byte identical to the full source
handoff. Each ZIP is a normal ZIP; no multipart decompression software is needed.
This extraction guide is the only additional top-level file.
