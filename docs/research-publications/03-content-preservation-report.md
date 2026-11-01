# Content preservation report

PASS: 20 articles audited. See `preservation-audit.json` for every source-to-output file check and section hash, and `source-manifest.json` for the original baseline.

The check compares complete file bodies and attachment bytes, not only heading counts. Tests additionally check complete fenced code bodies and all Markdown citation destinations in the rendered article. Browser tests separately verify visible diagrams, mathematical markup, figures, and learning interactions.

| Problem | Source headings | File hashes matched | Tables | Code fences | Math rendered | Check type | Source heading gaps |
|---|---:|---|---:|---:|---:|---|---|
| 01 | 14 | 18 / 18 | 2 | 5 | 12 | reflection | why difficult, learning challenge, research references, takeaway |
| 02 | 15 | 14 / 14 | 2 | 1 | 6 | reflection | why difficult |
| 03 | 19 | 16 / 16 | 3 | 5 | 0 | reflection | why difficult, takeaway |
| 04 | 17 | 18 / 18 | 3 | 4 | 6 | reflection | research references |
| 05 | 23 | 18 / 18 | 2 | 6 | 7 | choice | None |
| 06 | 17 | 14 / 14 | 3 | 3 | 0 | choice | None |
| 07 | 19 | 13 / 13 | 4 | 5 | 0 | choice | None |
| 08 | 25 | 18 / 18 | 2 | 5 | 4 | choice | None |
| 09 | 28 | 17 / 17 | 4 | 5 | 2 | choice | None |
| 10 | 26 | 16 / 16 | 3 | 3 | 1 | choice | None |
| 11 | 23 | 20 / 20 | 3 | 4 | 11 | choice | None |
| 12 | 24 | 18 / 18 | 3 | 4 | 21 | choice | None |
| 13 | 13 | 14 / 14 | 1 | 3 | 6 | choice | takeaway |
| 14 | 20 | 21 / 21 | 1 | 5 | 11 | choice | None |
| 15 | 28 | 22 / 22 | 3 | 1 | 7 | choice | None |
| 16 | 25 | 22 / 22 | 2 | 4 | 7 | choice | None |
| 17 | 27 | 16 / 16 | 4 | 5 | 11 | choice | None |
| 18 | 32 | 23 / 23 | 1 | 6 | 8 | choice | None |
| 19 | 34 | 11 / 11 | 4 | 5 | 6 | choice | None |
| 20 | 25 | 15 / 15 | 4 | 5 | 1 | choice | research references |

A missing separate heading is reported as a source limitation, not filled with invented scientific text. For example, 01–03 organize some difficulty and challenge material differently. Problems 01 and 04 have no dedicated primary research citation list; clearly labeled background references were added separately. Problem 14 names primary research in plain text; the supplied `REFERENCES.md` is retained and clickable official links are added in metadata.

- Main Markdown and all supporting package files checked byte-for-byte against their recorded source SHA256.
- Public source attachments checked byte-for-byte; SVG attachments compared with the safe sanitized rendering.
- The original package Markdown is unchanged. Centering wrappers are removed only during rendering; code, mathematics, tables, and reference destinations have additional tests.
- The first article heading moves into the shared article header. A source navigation typo in problem 03 has an alias at the intended section.
- Plaintext originals retain export artifacts. Complete transcripts are expandable and downloadable, not substituted for the illustrated reading edition.
- Source HTML demos are downloadable as text, not executable within the site origin.
- Generated Python caches are the only excluded package entries. Source titles and scientific qualifications are retained.
