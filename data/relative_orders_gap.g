LoadPackage("anupq");
show := function(name, des)
  local i, a, S;
  for i in [1..Length(des)] do
    if HasANUPQAutomorphisms(des[i]) then
      a := ANUPQAutomorphisms(des[i]);
      S := PqSupplementInnerAutomorphisms(des[i]);
      Print(name, " des[", i, "] |G|=", Size(des[i]),
        " central=", Length(a.centralAutos), " other=", Length(a.otherAutos),
        " relOrders=", a.relativeOrders,
        "  agAutos=", Length(S.agAutos), " agOrder=", Length(S.agOrder),
        " IsPcgsAutomorphisms=", IsPcgsAutomorphisms(des[i]), "\n");
    else
      Print(name, " des[", i, "] no aut info\n");
    fi;
  od;
end;
Q := Pq( FreeGroup(2) : Prime := 3, ClassBound := 1 );
show("3^2", PqDescendants( Q : StepSize := 1 ));
Q := Pq( FreeGroup(2) : Prime := 2, ClassBound := 1 );
show("2^2", PqDescendants( Q : StepSize := 1 ));
Q := Pq( FreeGroup(3) : Prime := 2, ClassBound := 1 );
show("2^3", PqDescendants( Q : StepSize := 1 ));
Q := Pq( FreeGroup(2) : Prime := 2, ClassBound := 2 );
show("D8-ish", PqDescendants( Q : StepSize := 1 ));
QUIT;
