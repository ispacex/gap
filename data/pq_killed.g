# Refuted item (pq death in the SP check): an external SIGTERM to pq (what `pkill -f ".../pq -G"` sends) while GAP is
# computing a stabiliser that pq asked for (pq is idle, waiting) gives exactly the error seen in the audit run of order 64.
LoadPackage("anupq");
orig := PQ_READ_AS_FUNC_WITH_VARS;
MakeReadWriteGlobal("PQ_READ_AS_FUNC_WITH_VARS");
PQ_READ_AS_FUNC_WITH_VARS := function(arg)
  local res;
  res := CallFuncList(orig, arg);
  if IsList(arg[1]) and not IsString(arg[1]) then  # the stabiliser request from ToPQ
    Exec("pkill -TERM -P $PPID -x pq; sleep 1");   # kill only this GAP's own pq child
  fi;
  return res;
end;
for k in [1 .. NumberSmallGroups(64)] do
  PqStandardPresentation(SmallGroup(64, k));      # the first k whose SP makes pq ask GAP for a stabiliser dies
od;
QUIT;
