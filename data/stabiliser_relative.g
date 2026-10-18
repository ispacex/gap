LoadPackage("anupq");
for x in [[3,1],[2,2]] do
  Q := Pq(FreeGroup(x[1]) : Prime := 2, ClassBound := x[2]);
  for G in PqDescendants(Q : StepSize := 1) do
    a := ANUPQAutomorphisms(G);
    # relOrders has one duplicated last entry (finding 23), hence -1
    Print(x, " autos=", Length(a.centralAutos) + Length(a.otherAutos),
          " soluble=", Length(a.relativeOrders) - 1, "\n");
  od;
od;
QUIT;
