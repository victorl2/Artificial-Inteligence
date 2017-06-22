%Aulas na sala
aula(plastino, 7, 9).
aula(vanessa, 11, 13).
aula(luciana, 14, 16).
aula(karina, 18, 20).

%Verifica se professor usa o ar e em qual temperatura
usa_ar(plastino, 20).
usa_ar(vanessa, 20).
usa_ar(luciana, 20).
usa_ar(karina, 20).

%Verifica se professor usa pc
usa_pc(plastino).
usa_pc(vanessa).

%Verifica se professor usa datashow
usa_datashow(plastino).

%Garante que todo usuario de datashow eh usuario de pc
usa_pc(X) :- usa_datashow(X).
