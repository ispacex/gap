# Finding 17: more than 65535 pc generators in one class (2-quotient of the free group of rank 361, class 2).
# master: no error, PqFactoredOrder gives [ 2, 65702 ] from a corrupted presentation; fixed: an error.
LoadPackage("anupq");
procId := PqStart(FreeGroup(361) : Prime := 2);;
PqPcPresentation(procId : ClassBound := 1);;
PqNextClass(procId);
Print(PqFactoredOrder(procId), "\n");
QUIT;
