LoadPackage("anupq"); SetInfoLevel(InfoANUPQ, 4);
F := FreeGroup("a", "b");; G := F / [ F.1^4, F.2^4 ];;
procId := PqStart(G);;
PqPcPresentation(procId : Prime := 2, ClassBound := 1);;
PqSetupTablesForNextClass(procId);;
PqTails(procId, 0);;
PqDoConsistencyChecks(procId, 0, 0);;
PqCollect(procId, "x1");          # word of weight 1, not homogeneous of class 2
Print("echelonise x1: ", PqEchelonise(procId), "\n");
PqCollect(procId, "x1^2");
Print("echelonise x1^2: ", PqEchelonise(procId), "\n");
PqEliminateRedundantGenerators(procId);;
PqDisplayPcPresentation(procId);
QUIT;
