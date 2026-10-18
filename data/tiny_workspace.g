LoadPackage("anupq");
BreakOnError := false;
try := function(f)
  local r;
  r := CALL_WITH_CATCH(f, []);
  PqQuitAll();
  if r[1] then return r[2]; else return "ERR"; fi;
end;
G := SmallGroup(8,3);
for ws in [20, 40, 60, 64, 65, 66, 70, 80, 100, 150, 200, 250] do
  Print("WS ", ws, " desc ", try(function() return Length(PqDescendants(G : PqWorkspace := ws)); end), "\n");
  Print("WS ", ws, " pcover ", try(function() return Size(PqPCover(G : PqWorkspace := ws)); end), "\n");
od;
QUIT;
