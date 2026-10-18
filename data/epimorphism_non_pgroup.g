LoadPackage("anupq"); SizeScreen([200,24]);
# is gens -> imgs a homomorphism G -> Q ?  (defining relators of G on gens, evaluated on imgs)
IsHomOnGens := function(G, gens, imgs)
  local iso, F;
  iso := IsomorphismFpGroupByGenerators(G, gens);
  F := FreeGroupOfFpGroup(Range(iso));
  return ForAll(RelatorsOfFpGroup(Range(iso)),
                r -> IsOne(MappedWord(r, GeneratorsOfGroup(F), imgs)));
end;
check := function(name, G, p, cls)
  local epi, Q, mg, R, imgs;
  Print("--- ", name, ": |G|=", Size(G), " GeneratorsOfGroup=", GeneratorsOfGroup(G),
        " Pcgs=", AsList(Pcgs(G)), "\n");
  epi := CALL_WITH_CATCH(function() return PqEpimorphism(G : Prime := p, ClassBound := cls); end, []);
  if epi[1] = false then Print("PqEpimorphism: ERROR\n"); else epi := epi[2];
  Q := Range(epi); mg := MappingGeneratorsImages(epi);
  Print("PqEpimorphism: |Q|=", Size(Q), " src=", mg[1], " imgs=", mg[2],
        " hom=", IsHomOnGens(G, mg[1], mg[2]),
        " onto=", Size(Group(mg[2], One(Q))) = Size(Q), "\n"); fi;
  epi := EpimorphismStandardPresentation(G : Prime := p, ClassBound := cls);
  Q := Range(epi); mg := MappingGeneratorsImages(epi);
  # SP comes back as an fp group listing only non-trivial pc relations; read it as a pc presentation
  R := PcGroupFpGroup(Q);
  imgs := List(mg[2], w -> MappedWord(UnderlyingElement(w), FreeGeneratorsOfFpGroup(Q), GeneratorsOfGroup(R)));
  Print("ESP: |Q|=", Size(R), " src=", mg[1], " imgs=", mg[2],
        " hom=", IsHomOnGens(G, mg[1], imgs),
        " onto=", Size(Group(imgs, One(R))) = Size(R), "\n");
end;
P := Image(IsomorphismPcGroup(DirectProduct(SymmetricGroup(3), CyclicGroup(4))));
BreakOnError := false;
try := function(name, G) local r;
  r := CALL_WITH_CATCH(check, [name, G, 2, 3]);
  if r[1] = false then Print("  -> ERROR (see message above)\n"); fi;
end;
try("A: S3xC4, gens = pcgs", P);
try("B: S3xC4, gens = reversed pcgs", Group(Reversed(GeneratorsOfGroup(P))));
try("C: subgroup of order 12, 2 gens", Group(P.1*P.3, P.2*P.4));
try("D: same subgroup, gens swapped", Group(P.2*P.4, P.1*P.3));
K := SmallGroup(72,42);; # S4 x C3
try("E: S4 x C3 on 2 gens", Group(K.1*K.3, K.2*K.4));
try("F: SmallGroup(72,42) itself", K);
QUIT;
