"""Block summary of an nTop notebook: sections, unused top-level blocks, and a
histogram of block counts by function name.

    >>> summary()                           # the open notebook
    >>> summary(md=r"C:\\temp\\blocks.md")   # also save as Markdown
"""

import os
import sys
import time


def _find_notebook(nb):
    if nb is not None:
        return nb
    main = sys.modules.get('__main__')
    if main is not None and hasattr(main, 'notebook'):
        return main.notebook
    f = sys._getframe(1)
    while f is not None:                     # whoever called us at the console
        if 'notebook' in f.f_globals:
            return f.f_globals['notebook']
        f = f.f_back
    raise RuntimeError("Can't find the console's notebook object; pass it: "
                       "summary(notebook=notebook)")


def _short(fid, custom):
    base = fid.split('<')[0]
    if base in custom:
        return custom[base]
    if base in ('core.var', 'core.list'):
        return fid.split('[')[0]
    return base


def _collect(nb):
    var_ids = {v['id'] for v in nb.list_variables()}
    custom = {c['id'].split('<')[0]: c['name'] for c in nb.list_custom_blocks()}
    blocks, seen, used = [], set(), set()

    def walk(bid, section, depth, parent, inp):
        fid = nb.get_block_func_id(bid)
        if depth > 0:
            used.add(bid)                    # something takes this block's output
        if bid in seen or (bid in var_ids and depth > 0):
            return                           # wired to a block counted where it sits
        seen.add(bid)
        isvar = bid in var_ids or fid.startswith('core.var<')
        blocks.append(dict(id=bid, func_id=fid, section=section, depth=depth,
                           parent=parent, input=inp, isvar=isvar))
        inner = None
        if isvar:
            try:
                inner = nb.get_block_inside_variable(bid)
            except Exception:
                inner = None
        if inner:
            walk(inner['id'], section, depth + 1, bid, '(contents)')
        try:
            inputs = nb.list_block_inputs(bid)
        except Exception:
            return
        for i in inputs:
            if i['isReturnValue']:
                continue
            try:
                m = nb.get_block_input_meta(bid, i['name'])
            except Exception:
                continue                     # property references, list-into-scalar
            if m.get('type') != 'block':
                continue
            if inner and m['blockId'] == inner['id']:
                continue                     # a variable's "Input" is its contents
            walk(m['blockId'], section, depth + 1, bid, i['name'])

    sections = nb.list_sections()
    for s in sections:
        for b in nb.list_blocks(s['id']):
            if b['funcId'] != 'floating_comment':
                walk(b['id'], s['name'], 0, '', '')
    for vid in var_ids:                      # a variable in no section's top level
        if vid not in seen:
            walk(vid, '(unplaced)', 0, '', '')

    counts = {}
    for b in blocks:
        b['name'] = _short(b['func_id'], custom)
        counts[b['name']] = counts.get(b['name'], 0) + 1
    unused = [dict(name=b['id'] if b['isvar'] else b['name'], section=b['section'])
              for b in blocks if b['depth'] == 0 and b['id'] not in used]
    return dict(sections=[s['name'] for s in sections], blocks=blocks, counts=counts,
                unused=unused, custom_blocks=sorted(custom.values()))


UNUSED = 'Not used by any other block'


def _format(s, width):
    """The header line and histogram, then the unused blocks as '- name (section)' lines."""
    n_sec = len(s['sections'])
    top = sum(1 for b in s['blocks'] if b['depth'] == 0)
    cb = ('custom blocks: ' + ', '.join(s['custom_blocks'])) if s['custom_blocks'] \
        else 'no custom blocks'
    lines = ['%d blocks (%d top-level) | %d section%s | %s'
             % (len(s['blocks']), top, n_sec, '' if n_sec == 1 else 's', cb), '']
    rows = sorted(s['counts'].items(), key=lambda kv: (-kv[1], kv[0].lower()))
    if rows:
        top_n = rows[0][1]
        labels = ['%s (%d)' % (k, v) for k, v in rows]
        pad = max(len(l) for l in labels)
        for label, (_, v) in zip(labels, rows):
            lines.append('%s : %s' % (label.ljust(pad), '#' * max(1, round(v / top_n * width))))
    unused = ['- %s (%s)' % (u['name'], u['section']) for u in s['unused']]
    return '\n'.join(lines), '\n'.join(unused)


def _console(title, body, unused):
    text = title + '\n' + body
    return text + ('\n\n%s:\n%s' % (UNUSED, unused) if unused else '')


def _write_md(path, title, body, unused):
    text = '# %s - Blocks\n\n%s\n\n```\n%s\n```\n' % (title, time.strftime('%Y-%m-%d'), body)
    if unused:
        text += '\n### %s\n\n%s\n' % (UNUSED, unused)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def summary(md=None, title=None, width=40, quiet=False, notebook=None):
    """Print a block-count histogram for the open notebook.
    md: also write it to this .md file. title: the heading name (default: the .md
    file name, else 'Open notebook')."""
    nb = _find_notebook(notebook)
    if nb.current_open_custom_block().get('id'):
        nb.close_current_open_custom_block()
    s = _collect(nb)
    if title is None:                        # the API can't tell us the open notebook's name
        title = os.path.splitext(os.path.basename(md))[0] if md else 'Open notebook'
    body, unused = _format(s, width)
    if md:
        _write_md(md, title, body, unused)
    if quiet:
        return s
    print(_console(title, body, unused))
    if md:
        print('Saved to ' + os.path.abspath(md))
