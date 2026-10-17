# Does PqDescendants(G) depend on the pc presentation of G?
# For G = SmallGroup(n, k), n = 32, 64, 128, p-class >= 3, every third k, compare the step-1
# descendants (as multisets of IdGroup) of G with those of three isomorphic copies:
#   - the pc group of a special pcgs of G,
#   - the pc group of a permutation representation of G,
#   - pq's own presentation of the fp group of G.
LoadPackage("anupq");
Reset(GlobalMersenneTwister, 7);
PermCopy := G -> Image(IsomorphismPcGroup(Image(IsomorphismPermGroup(G))));
bad := 0; n := 0;
for ord in [32, 64, 128] do
  for k in [1 .. NumberSmallGroups(ord)] do
    G := SmallGroup(ord, k);
    if PClassPGroup(G) < 3 or k mod 3 <> 0 then continue; fi;
    want := SortedList(List(PqDescendants(G : StepSize := 1), IdGroup));
    for H in [Image(IsomorphismSpecialPcGroup(G)), PermCopy(G),
              Pq(Image(IsomorphismFpGroup(G)) : Prime := 2, ClassBound := PClassPGroup(G))] do
      got := SortedList(List(PqDescendants(H : StepSize := 1), IdGroup));
      n := n + 1;
      if got <> want then bad := bad + 1;
        Print("DIFF ", [ord, k], " ", Length(want), " vs ", Length(got), "\n"); fi;
    od;
  od;
  Print("# ", ord, " compared ", n, " bad ", bad, "\n");
od;
QUIT;
