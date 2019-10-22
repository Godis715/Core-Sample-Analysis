# Analysis service API

### (POST) api/data_analysis/
- **data**: { fragments }, where fragments is array of { top: integer, bottom: integer, dlImg: binary, uvImg: binary }.
- **returns**: JSON with structure: { "markup": { "rock", "oil", "carbon", "disruption" } }. "rock", "oil", "carbon",
"disruption" are arrays of { "class": string, "begin": integer, "end": integer }.
