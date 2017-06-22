%Aulas na sala
aula(aline, 7, 9).
aula(kali, 9, 11).
aula(ricardo, 11, 13).
aula(fernanda, 18, 20).
aula(aline, 20, 22).

%Verifica se professor usa o ar e em qual temperatura
usa_ar(aline, 20).
usa_ar(kali, 18).
usa_ar(fernanda, 20).

%Verifica se professor usa datashow
usa_datashow(aline).
usa_datashow(kali).
usa_datashow(fernanda).

%Verifica se professor usa pc
usa_pc(aline).
usa_pc(kali).

%Garante que todo usuario de datashow eh usuario de pc
usa_pc(X) :- usa_datashow(X).