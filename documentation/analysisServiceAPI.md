# Analysis service API

### (POST) api/data_analysis/
- **data**: { files, fragments }, where fragments is array of { top: integer, bottom: integer, dlImg: string, uvImg: string }.
*dlImg* and *uvImg* reference images, which contains in *files*
- **returns**: JSON with structure: { "markup": { "rock", "oil", "carbon", "disruption" } }. "rock", "oil", "carbon",
"disruption" are arrays of { "class": string, "top": integer, "bottom": integer }.
