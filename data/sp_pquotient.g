BreakOnError := false; LoadPackage("anupq");
Key := F -> List(RelatorsOfFpGroup(F), LetterRepAssocWord);
G := SmallGroup(64, 6);;                              # 2-class 3
Q := PcGroupCode(33300, 16);;                         # a copy of its class-2 quotient
Print(IdGroup(Q), " ", IdGroup(Pq(G : Prime := 2, ClassBound := 2)), "\n");
Print("SP same as for G: ", Key(StandardPresentation(G : pQuotient := Q, ClassBound := 3)) = Key(StandardPresentation(G)), "\n");
H := SmallGroup(64, 112);;
Q := PcGroupCode(2768831001, 32);;
Print(IdGroup(Q), " ", IdGroup(Pq(H : Prime := 2, ClassBound := 2)), "\n");
Print("SP same as for H: ", Key(StandardPresentation(H : pQuotient := Q, ClassBound := 3)) = Key(StandardPresentation(H)), "\n");
QUIT;
