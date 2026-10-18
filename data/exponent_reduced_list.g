LoadPackage("anupq");
SetInfoLevel(InfoANUPQ, 0);
Run := function(G, p, e, cls, auts)
  local id, c, ord;
  id := PqStart(G : Prime := p, Exponent := e);
  PqPcPresentation(id : ClassBound := 1);
  if auts <> fail then PqSupplyAutomorphisms(id, auts); fi;
  for c in [2..cls] do
    PqNextClass(id : QueueFactor := 15);
    if PqPClass(id) < c then break; fi;
  od;
  ord := [PqFactoredOrder(id), PqPClass(id)];
  PqQuit(id);
  return ord;
end;
Pm := function(d) return PermutationMat(CycleFromList([1..d]), d); end;
Tv := function(d) local t; t := MutableCopyMat(IdentityMat(d)); t[1][2] := 1; return t; end;
TT := function(name, G, p, e, cls, autlist)
  local base, a, r;
  base := Run(G, p, e, cls, fail);
  Print(name, "  no auts: ", base, "\n");
  for a in autlist do
    r := Run(G, p, e, cls, a[2]);
    Print(name, "  ", a[1], ": ", r, "  ", 
          String(r = base), "\n");
  od;
end;
F4 := FreeGroup(4);; F2 := FreeGroup(2);; F3 := FreeGroup(3);;
TT("p=2 d=4 e=2", F4, 2, 2, 3, [
  ["identity", [IdentityMat(4)]],
  ["cycle", [Pm(4)]],
  ["transvection", [Tv(4)]],
  ["cycle+transv (GL)", [Pm(4), Tv(4)]]]);
TT("p=2 d=2 e=4", F2, 2, 4, 6, [
  ["identity", [IdentityMat(2)]],
  ["swap", [Pm(2)]],
  ["transvection", [Tv(2)]],
  ["swap+transv (GL)", [Pm(2), Tv(2)]]]);
TT("p=2 d=3 e=4", F3, 2, 4, 6, [
  ["cycle", [Pm(3)]],
  ["transvection", [Tv(3)]],
  ["cycle+transv (GL)", [Pm(3), Tv(3)]]]);
TT("p=3 d=2 e=3", F2, 3, 3, 4, [
  ["identity", [IdentityMat(2)]],
  ["SL gens", [[[0,1],[2,0]], Tv(2)]],
  ["diag(2,1)", [[[2,0],[0,1]]]],
  ["GL gens", [[[2,0],[0,1]], [[0,1],[2,0]], Tv(2)]]]);
TT("p=3 d=3 e=3", F3, 3, 3, 4, [
  ["identity", [IdentityMat(3)]],
  ["SL gens", [Pm(3), Tv(3)]],
  ["GL gens", [[[2,0,0],[0,1,0],[0,0,1]], Pm(3), Tv(3)]]]);
G := F2 / [F2.1^2];;
TT("<a,b|a^2> p=2 e=4", G, 2, 4, 6, [
  ["b->ab", [[[1,0],[1,1]]]]]);
QUIT;
