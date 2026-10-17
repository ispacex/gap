# For each line  n k code  of codes.txt: the step-1 descendants of PcGroupCode(code, n) and of
# SmallGroup(n, k), compared as multisets of IdGroup (n < 256) or by number (n = 256).
# CHUNK := [r, m] runs only the lines i with i mod m = r; START := i starts at the i-th of
# those, PROGRESS := file records the line being processed (to restart after pq kills GAP).
# Prints one line per group whose answers differ or where pq failed; a summary at the end.
LoadPackage("anupq");
Key := function(D, n) if n < 256 then return SortedList(List(D, IdGroup)); fi; return Length(D); end;
lines := SplitString(StringFile(Concatenation(DIR, "/codes.txt")), "\n");
if IsBound(CHUNK) then lines := lines{Filtered([1 .. Length(lines)], i -> i mod CHUNK[2] = CHUNK[1])}; fi;
tot := 0; wrong := 0; fail_ := 0; sgfail := 0;
if not IsBound(START) then START := 1; fi;
for i in [START .. Length(lines)] do
  l := lines[i];
  if IsBound(PROGRESS) then PrintTo(PROGRESS, i, "\n"); fi;
  x := List(SplitString(l, " "), Int); n := x[1]; k := x[2];
  want := CALL_WITH_CATCH(function() return Key(PqDescendants(SmallGroup(n, k) : StepSize := 1), n); end, []);
  if not want[1] then sgfail := sgfail + 1; PqQuitAll(); Print("PQ FAILED ON THE SMALLGROUP ", [n, k], "\n"); continue; fi;
  want := want[2];
  r := CALL_WITH_CATCH(function() return Key(PqDescendants(PcGroupCode(x[3], n) : StepSize := 1), n); end, []);
  tot := tot + 1;
  if not r[1] then fail_ := fail_ + 1; PqQuitAll(); Print("PQ FAILED ", [n, k], "\n");
  elif r[2] <> want then wrong := wrong + 1;
    if n < 256 then Print("WRONG ", [n, k], " ", Length(r[2]), " descendants instead of ", Length(want), "\n");
    else Print("WRONG ", [n, k], " ", r[2], " descendants instead of ", want, "\n"); fi;
  fi;
od;
Print("RESULT copies=", tot, " wrong=", wrong, " pq failed=", fail_, " pq failed on the SmallGroup=", sgfail, "\n");
QUIT;
