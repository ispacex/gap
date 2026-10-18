# Finding 18: too little workspace reserved for a commutator relation with an exponent.
# master: 128 with PqWorkspace := 210 (right: 64); fixed: "Ran out of space".
LoadPackage("anupq");
F := FreeGroup("a", "b");; G := F / [Comm(F.2, F.1)^3];;
Print(Size(Pq(G : Prime := 2, ClassBound := 3, Relators := ["[b,a]^3"])), "\n");                       # 64
Print(Size(Pq(G : Prime := 2, ClassBound := 3, Relators := ["[b,a]^3"], PqWorkspace := 210)), "\n");  # 128 on master
QUIT;
