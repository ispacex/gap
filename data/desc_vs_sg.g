# Differential check: PqDescendants against the SmallGroups library.
# For a p-group H of p-class c >= 2, its parent is H/P_c(H) and the step is log_p |P_c(H)|.
# So for G and s the immediate descendants of G of step s are exactly the H of order |G| p^s
# with H/P_c(H) = G. We compare, for every G of order p^m (m < N) and every s with m + s <= N,
# the multiset of IdGroup of PqDescendants(G : StepSize := s) with that set.
# Usage: P := 2;; N := 7;; Read("desc_vs_sg.g");
LoadPackage("anupq");
pc := function(H, p) local S; S := PCentralSeries(H, p); return Length(S) - 1; end;
Parent_ := function(H, p) local S; S := PCentralSeries(H, p);
  return [ IdGroup(H / S[Length(S) - 1]), LogInt(Size(S[Length(S) - 1]), p) ]; end;
expect := rec();   # key "m_i_s" -> sorted list of ids of H
for n in [2 .. N] do
  for k in [1 .. NumberSmallGroups(P^n)] do
    H := SmallGroup(P^n, k);
    if pc(H, P) >= 2 then
      x := Parent_(H, P);
      key := Concatenation(String(LogInt(x[1][1], P)), "_", String(x[1][2]), "_", String(x[2]));
      if not IsBound(expect.(key)) then expect.(key) := []; fi;
      Add(expect.(key), [P^n, k]);
    fi;
  od;
od;
bad := 0; checked := 0;
for m in [1 .. N - 1] do
  for k in [1 .. NumberSmallGroups(P^m)] do
    G := SmallGroup(P^m, k);
    for s in [1 .. N - m] do
      key := Concatenation(String(m), "_", String(k), "_", String(s));
      want := [];
      if IsBound(expect.(key)) then want := SortedList(expect.(key)); fi;
      if IsElementaryAbelian(G) and m >= 5 and s >= 2 then
        Print("# skip elementary abelian ", [P^m, k], " s=", s, "\n"); continue;
      fi;
      D := PqDescendants(G : StepSize := s);
      got := SortedList(List(D, IdGroup));
      checked := checked + 1;
      if got <> want then
        bad := bad + 1;
        Print("MISMATCH G=", [P^m, k], " s=", s, " pq=", Length(got), " SG=", Length(want),
              " missing=", Difference(want, got), " extra/dup=", Filtered(got, x -> not x in want or Number(got, y -> y = x) > 1), "\n");
      fi;
    od;
  od;
  Print("# order ", P^m, " done, pairs checked ", checked, ", mismatches ", bad, "\n");
od;
Print("RESULT p=", P, " N=", N, " pairs=", checked, " mismatches=", bad, "\n");
QUIT;
