# pq2048 with PQ2048_OWNCOVER=1 PQ2048_OWNDESC=1: children built in GAP, then PqDescendants on them.
# Compare PqDescendants(child) with PqDescendants of the SmallGroups copy of the child.
OWNCOVER := true;; OWNDESC := true;;
Read("../pq1024/lib.g"); Read("../pq1024/cover.g"); Read("steps.g");
tot := 0; bad := 0; vert := 0;
for ord in [16, 32, 64] do
  for k in [1 .. NumberSmallGroups(ord)] do
    V := SmallGroup(ord, k);
    if NilpotencyClassOfGroup(V) > 3 then continue; fi;
    ch := CH_Step1(V);
    if ch = fail then continue; fi;
    vert := vert + 1;
    for C in ch do
      if NilpotencyClassOfGroup(C) > 3 then continue; fi;
      a := SortedList(List(PqDescendants(C : StepSize := 1), IdGroup));
      b := SortedList(List(PqDescendants(SmallGroup(IdGroup(C)) : StepSize := 1), IdGroup));
      tot := tot + 1;
      if a <> b then bad := bad + 1;
        Print("child ", IdGroup(C), " of ", [ord, k], ": ", Length(a), " descendants, SmallGroups copy: ", Length(b), "\n");
      fi;
    od;
  od;
  Print("# parents of order ", ord, " done: children compared ", tot, ", differing ", bad, "\n");
od;
Print("RESULT vertices=", vert, " children=", tot, " differing=", bad, "\n");
QUIT;
