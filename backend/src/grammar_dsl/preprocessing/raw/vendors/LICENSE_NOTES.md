# License Notes

All vendor files under `raw/vendors/` should be treated as raw acquisition drops.

Rules:
- keep the original filename and source context when possible
- do not assume redistribution rights for the raw vendor file
- prefer importing a normalized subset into `raw/imported/` rather than shipping the full upstream dataset
- keep provenance in `vendor_manifest.json` and in each imported pack metadata
- review upstream terms before committing any large third-party raw export to a public repository

Recommended workflow:
1. drop the original file into the matching vendor folder
2. record or confirm the source in `vendor_manifest.json`
3. run the importer
4. inspect the normalized pack
5. compile the knowledge base
