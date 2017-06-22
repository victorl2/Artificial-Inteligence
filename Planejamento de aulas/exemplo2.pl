%Aulas na sala
aula(jethro, 14, 16).
aula(leonardo, 16, 18).
aula(daniel, 18, 20).
aula(renata, 20, 22).

%Verifica se professor usa o ar e em qual temperatura
usa_ar(jethro, 16).
usa_ar(leonardo, 17).
usa_ar(daniel, 18).
usa_ar(renata, 19).

%Verifica se professor usa datashow
usa_datashow(jethro).
usa_datashow(leonardo).
usa_datashow(daniel).
usa_datashow(renata).

%Garante que todo usuario de datashow eh usuario de pc
usa_pc(X) :- usa_datashow(X).