# nTopScripts


Helpers for nTop's Python Console. The folder `C:\Users\<user>\Documents\nTopScripts\` is on the console's import path.

(Mostly written by Claude, tweaked by hand)

## Run (Example)

1. **View → Python Console** (Ctrl+`)
2. `import utils`
3. `utils.summary()` — prints a block summary of the open notebook:
   - a header: total blocks, top-level blocks, sections, custom blocks
   - a histogram of block counts by type
   - top-level blocks not used by any other block, with their section

## Summary

```python
utils.summary(md=r"C:\temp\blocks.md")   # also save as Markdown
```

After editing the code, run `utils.reload()`. No need to re-import.
