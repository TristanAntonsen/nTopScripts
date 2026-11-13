# nTopScripts

nTop's Python Console has this folder on its import path. Nothing here runs
automatically: each console session needs `from utils import ...`.

## Layout

- `utils.py` is a thin loader. It loads the real code by file path from
  `C:\Users\tristanantonsen\Desktop\code\ntop-api-skills\skills\ntop-notebook-api\scripts`
  and wraps each function.
  - Edit the repo copy, not this file, then run `utils.reload()` in the console.
  - To add a helper: add a `_load("<module>")` line in `reload()`, plus a
    wrapper function.
- Load scripts by path rather than adding the scripts folder to `sys.path`,
  because some scripts there run on import (`summarize_graph.py`).
- Don't add modules whose names shadow common packages. The console imports
  from this folder first.

## Testing

- Use `ntc.ps1` (SSH to localhost:2222) from the skills repo. It only works
  while the Python Console panel is open in nTop (Ctrl+`).

  ```
  skills\ntop-notebook-api\scripts\ntc.ps1 -Lines 'from utils import block_summary' 'block_summary()'
  ```

- Modules already imported in a console session stay cached until nTop
  restarts, or until `utils.reload()` for the loaded scripts.
