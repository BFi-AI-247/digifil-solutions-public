import re, collections
D='/root/src/dict/dictionaries/de/'
OK=re.compile(r'^[A-ZÄÖÜ]{5}$')
def norm(w): return w.replace('ß','ss').upper()
allw=[l.strip() for l in open('all.txt',encoding='utf-8')]
guesses=set()
for w in allw:
    if w.isupper() and len(w)>1: continue  # Abkürzungen
    n=norm(w)
    if OK.match(n): guesses.add(n)
# headwords
heads={}
for line in open(D+'index.dic',encoding='utf-8').read().splitlines()[1:]:
    if not line or line[0] in ' \t#': continue
    w,_,fl=line.split('\t')[0].strip().partition('/')
    if 'd' in fl or 'o' in fl or 'h' in fl: continue
    if w.isupper(): continue
    n=norm(w)
    if OK.match(n): heads.setdefault(n,set()).add(w)
freq={}
for i,l in enumerate(open('/root/src/freq/content/2018/de/de_full.txt',encoding='utf-8')):
    p=l.split()
    if len(p)!=2: continue
    n=norm(p[0])
    if OK.match(n) and n not in freq: freq[n]=(i,int(p[1]))
print('guesses',len(guesses),'heads',len(heads))
cand=sorted([h for h in heads if h in freq],key=lambda h:freq[h][0])
print('heads w/ freq',len(cand))
for lim in (5000,10000,20000,40000):
    print(lim,sum(1 for h in cand if freq[h][0]<lim))
open('cand.txt','w').write('\n'.join(f"{h}\t{freq[h][0]}\t{'|'.join(sorted(heads[h]))}" for h in cand))
open('guesses.txt','w').write('\n'.join(sorted(guesses)))
