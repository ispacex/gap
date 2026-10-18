LoadPackage("anupq");
G := PcGroupCode(723005982809892258877217511128, 256);   # an isomorphic copy of SmallGroup(256,1325)
Print(IdGroup(G), "\n");
Print("descendants: ", Length(PqDescendants(G : StepSize := 1)), "\n");
QUIT;
