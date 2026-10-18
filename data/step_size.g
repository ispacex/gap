LoadPackage("anupq");
G := SmallGroup(4, 2);   # C2 x C2: nuclear rank 3
for s in [3, 4] do
  D := PqDescendants(G : StepSize := s, PcgsAutomorphisms);
  Print("PqDescendants(C2xC2 : StepSize := ", s, ", PcgsAutomorphisms): ", Length(D),
        " groups, orders ", Collected(List(D, Size)), "\n");
od;
QUIT;
