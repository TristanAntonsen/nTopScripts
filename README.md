# nTopScripts

Helpers for nTop's Python Console. This folder is on the console's import path.

## Run

1. **View → Python Console** (Ctrl+`)
2. `import utils`
3. `utils.summary()` — prints a block summary of the open notebook:
   - a header: total blocks, top-level blocks, sections, custom blocks
   - a histogram of block counts by type
   - top-level blocks not used by any other block, with their section

## Options

```python
utils.summary(r"C:\path\part.ntop", restore=True)  # summarize a file, then reopen the current notebook
utils.summary(md=r"C:\temp\blocks.md")             # also save as Markdown
```

Opening a file by path replaces the open notebook; a backup is saved to `%TEMP%\ntop-blocks` first.

After editing the code, run `utils.reload()`. No need to re-import.
