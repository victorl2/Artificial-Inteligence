%Aulas na sala
aula(leandro, 7, 9).
aula(petrucio, 9, 11).
aula(rosseti, 11, 13).
aula(christiano, 14, 16).
aula(bruno, 16, 18).
aula(moises, 18, 22).

%Verifica se professor usa o ar e em qual temperatura
usa_ar(leandro, 16).
usa_ar(petrucio, 16).
usa_ar(rosseti, 18).
usa_ar(christiano, 18).
usa_ar(moises, 19).

%Verifica se professor usa datashow
usa_datashow(moises).
usa_datashow(leandro).
usa_datashow(petrucio).
usa_datashow(christiano).

%Verifica se professor usa pc
usa_pc(bruno).

%Garante que todo usuario de datashow eh usuario de pc
usa_pc(X) :- usa_datashow(X).