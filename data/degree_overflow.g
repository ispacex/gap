LoadPackage("anupq");
G := PcGroupCode( 5720184869874057666191942025326282294078349057, 2^9 );
Print("rank=", RankPGroup(G), " class=", NilpotencyClassOfGroup(G), "\n");
r := CALL_WITH_CATCH(StandardPresentation, [G]);
Print("CATCH: ", r[1], "\n");
if r[1] = true then Print("RESULT: ", r[2], "\n"); fi;
QUIT;
