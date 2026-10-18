LoadPackage("anupq");; epi:=0;; G:=0;; img:=0;; rels:=0;;
F := FreeGroup("a","b","c"); a := F.1; b := F.2; c := F.3;
for rels in [ [a^2*b^3*c^5, c^2], [a^2*b^3*c^5, Comm(a,b)^7*Comm(b,c)^11*c^2] ] do
for p in [32749, 32771] do
  G := F / rels;
  epi := PqEpimorphism(G : Prime := p, ClassBound := 1);
  img := List(GeneratorsOfGroup(G), g -> ExponentsOfPcElement(Pcgs(Image(epi)), Image(epi, g)));
  Print("p=", p, " rels=", rels, " |Q|=p^", LogInt(Size(Image(epi)), p), " a,b,c -> ", img,
        " relators hold: ", List(rels, r -> IsOne(MappedWord(r, [a,b,c], List(GeneratorsOfGroup(G), g -> Image(epi, g))))), "\n");
od; od;
QUIT;
