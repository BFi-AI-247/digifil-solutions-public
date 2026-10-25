import random,json
EX="""Frank Peter David Paris Harry James Henry Billy Maria Steve Roger Louis Robin Alice Simon Grace Story Julia Marie Annie Jones China Klaus Texas Miami Carol Felix Paula Davis Jacob Betty Blair Japan Teddy Santa Oscar Diana Media Ralph Anton Homer Peggy Franz Bruno Lloyd Pablo Willy Boris Cathy Allah Polen Pedro Zorro Tokio Doris Marge Edgar Devon Heidi Busch Spike Cäsar Georg Oskar Moses Fritz Isaac Carlo Josef Jakob Elias Edith Willi Korea Sonja Sofia Flora Grimm Anita Jaffa Karin Cisco Dolly Freud Linus Dante Bryan Horst Erika Heinz Asien Meyer Adolf Helga Lotte Athen Kairo Obama Milan Tanja Erich Eliza Petra Orion Apple Gerda Guido Pippi Trump Seoul Alpen Nizza Weber Haiti Erwin Berta Malmö Hagen Artus Dubai Bambi Hades Chile Björn Tibet Dover Kongo Bernd Bosch Vista Rhein Troja Viola Karla Donau Kenia Katia Jemen Rolex Pluto Meier Kabul Sudan Huber Delhi Olymp Burma Beate Volvo Isaak Sodom Mekka Lenin Hilde Honda Kreml Pepsi Shell Hanne Prado UdSSR Dalai Anwar Silke Kreta Nepal Adria Argus Moser Malta Genua Saudi Plato Turin Lanka Dumas Grete Minsk Curie Linux Anden Indio Negro Neger Nutte Fotze Arsch Penis Lesbe Tunte Dildo Porno Hoden Möpse Busen Luder Zicke Dirne Fürze Arier Russe Türke Inder Brite Jüdin Rasse Queen First Flash Power Check Sound Image Cover Prime Order Patch Swing Crash Stunt Letzt Steig Hänge Talon Quint Lumen Franc Dinar Legat Hydra Photo huren alpha omega gamma kappa sigma theta Andre dritt viert fünft zweit leibt dünkt rätst Satan Wacht Mieze Gassi Faxen Major Stasi Venus Kripo""".split()
def norm(w): return w.replace('ß','ss').upper()
exn={norm(e) for e in EX}
g=set(open('guesses.txt').read().split())
sol=[]
for l in open('cand.txt',encoding='utf-8'):
    w,r,f=l.rstrip('\n').split('\t')
    if int(r)<40000 and w not in exn and w in g: sol.append(w)
print(len(sol), [w for w in sol[:5]])
rng=random.Random(20261025); rng.shuffle(sol)
open('solutions.txt','w').write('\n'.join(sol))
