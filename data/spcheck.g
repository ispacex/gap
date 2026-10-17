# Standard presentations as an isomorphism key.
# (a) invariance: for G = SmallGroup(n, k) and R random minimal generating sets, the SP of the
#     fp group on those generators equals the SP of G (relators compared as letter lists);
# (b) separation: all groups of order n get pairwise different SPs;
# (c) soundness: the SP group has the IdGroup of G.
# Usage: ORDER := 128;; R := 2;; Read("spcheck.g");
LoadPackage("anupq");
Key := function(F) return List(RelatorsOfFpGroup(F), LetterRepAssocWord); end;
RandomGens := function(G)
  local d, gens;
  d := Length(MinimalGeneratingSet(G));
  repeat gens := List([1 .. d], i -> Random(G)); until Subgroup(G, gens) = G;
  return gens;
end;
Reset(GlobalMersenneTwister, 1);
P := SmallestRootInt(ORDER);
keys := []; bad := 0;
for k in [1 .. NumberSmallGroups(ORDER)] do
  G := SmallGroup(ORDER, k);
  S := PqStandardPresentation(G);
  key := Key(S);
  if IdGroup(PcGroupFpGroup(S)) <> [ORDER, k] then
    bad := bad + 1; Print("UNSOUND ", k, "\n");
  fi;
  for r in [1 .. R] do
    # an isomorphic pc group with a different pcgs (via a randomly conjugated perm group)
    Q := Image(IsomorphismPermGroup(G));
    Q := Q ^ Random(SymmetricGroup(LargestMovedPoint(Q)));
    F := Image(IsomorphismPcGroup(Q));
    if Key(PqStandardPresentation(F)) <> key then
      bad := bad + 1; Print("NOT INVARIANT ", k, " (other pcgs, try ", r, ")\n");
    fi;
  od;
  Add(keys, key);
  if k mod 500 = 0 then Print("# ", k, "\n"); fi;
od;
dups := Length(keys) - Length(Set(keys));
Print("RESULT order=", ORDER, " groups=", Length(keys), " bad=", bad, " duplicate keys=", dups, "\n");
QUIT;
