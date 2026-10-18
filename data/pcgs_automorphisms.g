LoadPackage("anupq");; BreakOnError := false;;
# 1. Aut(C2^2) = S3 is soluble; AutPGrp gives two involutions, which ANUPQ sends as a "PAG sequence"
G := ElementaryAbelianGroup(4);;
d0 := PqDescendants(G : ClassBound := 3);;
d1 := PqDescendants(G : ClassBound := 3, PcgsAutomorphisms);;
Print("C2^2, ClassBound 3: default ", Length(d0), " ", Collected(List(d0, Size)), "\n");
Print("C2^2, ClassBound 3: Pcgs    ", Length(d1), " ", Collected(List(d1, Size)), "\n");
c16 := g -> Collected(List(Filtered(g, h -> Size(h) <= 64), IdGroup));;
Print("  order<=64 default: ", c16(d0), "\n  order<=64 Pcgs:    ", c16(d1), "\n");
# 2. Aut(C2^3) = GL(3,2) is insoluble; the option is accepted without a check
truth := Number(AllSmallGroups(32), H -> RankPGroup(H) = 3 and PClassPGroup(H) = 2);;
Print("C2^3: immediate descendants of order 32 that exist: ", truth, "\n");
QUIT;
