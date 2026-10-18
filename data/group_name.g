LoadPackage("anupq");
G := ElementaryAbelianGroup(4);
D := PqDescendants(G : GroupName := "my_G", OrderBound := 4);
Print("GroupName \"my_G\": ", Length(D), " descendants, orders ", List(D, Size), "\n");
QUIT;
