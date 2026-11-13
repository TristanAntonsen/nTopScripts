# nTopScripts

nTop's Python Console has this folder on its import path. Nothing here runs
automatically: each console session needs `from utils import ...`.

## Layout

- The helper code lives here, self-contained (standard library only).
  - `block_summary.py`: `block_summary()` prints a notebook's block summary
    (sections, unused top-level blocks, block-count histogram); `md=` also
    saves that output as a Markdown file.
- `utils.py` imports the helper modules and wraps each function, so one
  `from utils import ...` covers them all.
  - After editing a helper, run `utils.reload()` in the console.
  - To add a helper: import its module in `utils.py`, add it to `reload()`,
    and add a wrapper function.
- Don't add modules whose names shadow common packages. The console imports
  from this folder first.

## Testing

- Use `ntc.ps1` (SSH to localhost:2222) from the skills repo
  (`C:\Users\tristanantonsen\Desktop\code\ntop-api-skills`). It only works
  while the Python Console panel is open in nTop (Ctrl+`).

  ```
  skills\ntop-notebook-api\scripts\ntc.ps1 -Lines 'import utils; utils.reload()' 'utils.block_summary()'
  ```

- Modules already imported in a console session stay cached until nTop
  restarts, or until `utils.reload()`.
