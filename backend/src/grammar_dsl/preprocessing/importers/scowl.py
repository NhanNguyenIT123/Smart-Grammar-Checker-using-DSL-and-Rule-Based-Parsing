from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import build_metadata, normalize_word, read_text, unique_sorted, write_import_pack


def import_scowl_pack(input_path: Path, output_dir: Path | None = None) -> dict[str, Any]:
    words: list[str] = []

    for raw_line in read_text(input_path).splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        word = normalize_word(line)
        if word:
            words.append(word)

    normalized_words = unique_sorted(words)
    payload = {
        "metadata": build_metadata(
            source_id="src-scowl-imported",
            source_type="lexicon",
            origin="scowl",
            description="Imported SCOWL word list snapshot normalized for spelling and dictionary enrichment.",
            license_note="See upstream SCOWL/wordlist license and README in the vendor drop.",
            source_files=[input_path.name],
            record_count=len(normalized_words),
        ),
        "dictionary_words": normalized_words,
    }
    write_import_pack("scowl_pack.json", payload, output_dir=output_dir)
    return payload
