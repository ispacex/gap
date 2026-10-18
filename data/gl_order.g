LoadPackage("anupq");
SetInfoLevel(InfoANUPQ,2);
r := PqDescendants(ElementaryAbelianGroup(101^2) : OrderBound := 4, ClassBound := 2);
Print(Length(r),"\n");
QUIT;
