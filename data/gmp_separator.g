LoadPackage("anupq");;
p := 53;;
D := PqDescendants(CyclicGroup(p) : StepSize := 1);; Print("C_53: ", List(D, IdGroup), "\n");
D := PqDescendants(ElementaryAbelianGroup(p^2) : StepSize := 1);; Print("C_53^2: ", List(D, IdGroup), "\n");
QUIT;
