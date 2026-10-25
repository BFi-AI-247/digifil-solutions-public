"""Minimal Hunspell affix expander (enough for igerman98 de_DE, single-char flags)."""
import re, sys, collections

def load_aff(path):
    rules = {}  # flag -> (kind, cross, [(strip, add, cond_re, contflags)])
    lines = open(path, encoding='utf-8', errors='replace').read().splitlines()
    i = 0
    while i < len(lines):
        p = lines[i].split()
        if len(p) >= 4 and p[0] in ('PFX', 'SFX') and p[2] in ('Y', 'N') and p[3].isdigit():
            kind, flag, cross, n = p[0], p[1], p[2] == 'Y', int(p[3])
            ents = []
            for j in range(1, n + 1):
                q = lines[i + j].split()
                strip = '' if q[2] == '0' else q[2]
                add = q[3]
                cont = ''
                if '/' in add:
                    add, cont = add.split('/', 1)
                if add == '0':
                    add = ''
                cond = q[4] if len(q) > 4 else '.'
                if cond == '.':
                    cre = None
                else:
                    cre = re.compile(('^' + cond) if kind == 'PFX' else (cond + '$'))
                ents.append((strip, add, cre, cont))
            rules[flag] = (kind, cross, ents)
            i += n + 1
        else:
            i += 1
    return rules

SPECIAL = set('xyzdcohwf')

def apply_sfx(word, ents):
    for strip, add, cre, cont in ents:
        if cre and not cre.search(word):
            continue
        if strip and not word.endswith(strip):
            continue
        base = word[:len(word) - len(strip)] if strip else word
        yield base + add, cont

def apply_pfx(word, ents):
    for strip, add, cre, cont in ents:
        if cre and not cre.search(word):
            continue
        if strip and not word.startswith(strip):
            continue
        base = word[len(strip):]
        yield add + base, cont

def expand(dic, aff):
    rules = load_aff(aff)
    out = set()
    forbidden = set()
    for line in open(dic, encoding='utf-8', errors='replace').read().splitlines()[1:]:
        if not line or line[0] in ' \t#':
            continue
        line = line.split('\t')[0].strip()
        if '/' in line:
            w, flags = line.split('/', 1)
        else:
            w, flags = line, ''
        if 'd' in flags:
            forbidden.add(w); continue
        if 'o' in flags:  # only in compounds
            continue
        forms = []
        if 'h' not in flags:
            forms.append(w)
        sfx = [rules[f] for f in flags if f in rules and rules[f][0] == 'SFX']
        pfx = [rules[f] for f in flags if f in rules and rules[f][0] == 'PFX']
        sforms = []
        for kind, cross, ents in sfx:
            for f1, cont in apply_sfx(w, ents):
                if 'o' in cont:
                    continue
                if 'f' not in cont:
                    sforms.append((f1, cross))
                for c in cont:
                    if c in rules and rules[c][0] == 'SFX':
                        for f2, cont2 in apply_sfx(f1, rules[c][2]):
                            if 'o' not in cont2 and 'f' not in cont2:
                                sforms.append((f2, cross))
        forms += [f for f, _ in sforms]
        for kind, cross, ents in pfx:
            for p1, cont in apply_pfx(w, ents):
                if 'f' not in cont and 'o' not in cont:
                    forms.append(p1)
            if cross:
                for f1, scross in sforms:
                    if scross:
                        for p1, cont in apply_pfx(f1, ents):
                            if 'f' not in cont and 'o' not in cont:
                                forms.append(p1)
        out.update(forms)
    return out - forbidden

if __name__ == '__main__':
    words = expand(sys.argv[1], sys.argv[2])
    for w in sorted(words):
        print(w)
