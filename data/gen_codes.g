# For every SmallGroup(n, k) of p-class >= 3 (n = 64, 128; every 25th k <= 13550 for n = 256), an
# isomorphic pc group with another pcgs: the pc group of a randomly conjugated permutation
# representation. Writes lines  n k code  to codes.txt. Fixed seeds, so it can be rerun.
Reset(GlobalMersenneTwister, 2026); Reset(GlobalRandomSource, 2026);
out := OutputTextFile(Concatenation(DIR, "/codes.txt"), false);
SetPrintFormattingStatus(out, false);
for n in [64, 128, 256] do
  for k in [1 .. NumberSmallGroups(n)] do
    if n = 256 and (k mod 25 <> 0 or k > 13550) then continue; fi;
    G := SmallGroup(n, k);
    if PClassPGroup(G) < 3 then continue; fi;
    Q := Image(IsomorphismPermGroup(G));
    Q := Q ^ Random(SymmetricGroup(LargestMovedPoint(Q)));
    H := Image(IsomorphismPcGroup(Q));
    if CodePcGroup(H) = CodePcGroup(G) then continue; fi;
    PrintTo(out, n, " ", k, " ", CodePcGroup(H), "\n");
  od;
od;
CloseStream(out);
QUIT;
