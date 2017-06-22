%BASE DE CONHECIMENTO

%Verifica se professor abre sala
nao_abre_sala(X, A) :- aula(X, A, B), aula(Y, N, A).
abre_sala(X, A) :- not(nao_abre_sala(X, A)), aula(X, A, B).

%Verifica se professor fecha sala
fecha_sala(X, B) :- aula(X, A, B), not(aula(Y, B, M)).

%Verifica qual a aula atual
aula_atual(X, HORA) :- aula(X, A, B), A =< HORA, B > HORA.

%Verifica qual professor dara a prox aula
prox_aux(X, A, HORA) :- aula(Y, N, M), N >= A, N > HORA.                      
prox_aula(X, HORA, A, B) :- aula(X, A, B), A > HORA, prox_aux(X, A, HORA).    

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Plano para preparar a sala

plan(Start,Start,[]).
plan(Start, End, [Action|Actions]) :- schedule(Start, Next, Action), plan(Next, End, Actions).

%Transicoes
%INFORMACOES GERAIS TRANSICOES:
%0 = AULA EM ANDAMENTO, 1 = AULA CONCLUIDA
%P = PROFESSOR, A = HORA INICIO AULA, B = HORA FIM AULA
%PROX_PROF = PROXIMO PROFESSOR, INI = HORA INICIO AULA PROX_PROF, FIM = HORA FIM AULA PROX_PROF
%PROX_PROF2 = PROXIMO PROFESSOR DO PROXIMO PROFESSOR, INI2 = HORA INICIO AULA PROX_PROF2, FIM2 = HORA FIM AULA PROX_PROF2
%X = SALA FECHADA OU ABERTA
%Y = AR LIGADO OU DESLIGADO
%Z = DATASHOW LIGADO OU DESLIGADO
%W = PC LIGADO OU DESLIGADO
%K = LUZ LIGADA OU DESLIGADA

%Iniciando plano com professor inicial -> (prox_aula(P, 0, A, B))
schedule(inicio, status(prof(P, A, B), sala(fechada), ar(desligado, -273), datashow(desligado), pc(desligado), luz(desligada), 0, proximo_prof(PROX_PROF, INI, FIM)), iniciar) :- prox_aula(P, 0, A, B), (prox_aula(PROX_PROF, A, INI, FIM) ; not(prox_aula(PROX_PROF, A, INI, FIM))).

%Abrindo sala
schedule(status(prof(P, A, B), sala(fechada), Y, Z, W, K, 0, proximo_prof(PROX_PROF, INI, FIM)), status(prof(P, A, B), sala(aberta), Y, Z, W, K, 0, proximo_prof(PROX_PROF, INI, FIM)), abrir_sala(P)).

%Ligando luz
schedule(status(prof(P, A, B), X, Y, Z, W, luz(desligada), 0, proximo_prof(PROX_PROF, INI, FIM)), status(prof(P, A, B), X, Y, Z, W, luz(ligada), 0, proximo_prof(PROX_PROF, INI, FIM)), ligar_luz(P)).

%Ligar ou nao o ar
schedule(status(prof(P, A, B), X, ar(desligado, TEMP_INI), Z, W, K, 0, proximo_prof(PROX_PROF, INI, FIM)), status(prof(P, A, B), X, ar(ligado, TEMP_INI), Z, W, K, 0, proximo_prof(PROX_PROF, INI, FIM)), liga_ar(P)) :- usa_ar(P, TEMP).

%Ajusta temperatura
schedule(status(prof(P, A, B), X, ar(ligado, TEMP_INI), Z, W, K, 0, proximo_prof(PROX_PROF, INI, FIM)), status(prof(P, A, B), X, ar(ligado, TEMP), Z, W, K, 0, proximo_prof(PROX_PROF, INI, FIM)), ajusta_temp(P, TEMP)) :- usa_ar(P, TEMP), TEMP =\= TEMP_INI.

%Ligar ou nao o pc
schedule(status(prof(P, A, B), X, Y, Z, pc(desligado), K, 0, proximo_prof(PROX_PROF, INI, FIM)), status(prof(P, A, B), X, Y, Z, pc(ligado), K, 0, proximo_prof(PROX_PROF, INI, FIM)), ligar_pc(P)) :- usa_pc(P).

%Ligar ou nao o datashow
schedule(status(prof(P, A, B), X, Y, datashow(desligado), W, K, 0, proximo_prof(PROX_PROF, INI, FIM)), status(prof(P, A, B), X, Y, datashow(ligado), W, K, 0, proximo_prof(PROX_PROF, INI, FIM)), ligar_datashow(P)) :- usa_datashow(P).

%Desligar ou nao o datashow
schedule(status(prof(P, A, B), X, Y, datashow(ligado), W, K, 0, proximo_prof(PROX_PROF, INI, FIM)), status(prof(P, A, B), X, Y, datashow(desligado), W, K, 1, proximo_prof(PROX_PROF, INI, FIM)), desligar_datashow(P)) :- fecha_sala(P, B) ; not(usa_datashow(PROX_PROF)).

%Desligar ou nao o pc
schedule(status(prof(P, A, B), X, Y, Z, pc(ligado), K, END, proximo_prof(PROX_PROF, INI, FIM)), status(prof(P, A, B), X, Y, Z, pc(desligado), K, 1, proximo_prof(PROX_PROF, INI, FIM)), desligar_pc(P)) :- fecha_sala(P, B) ; not(usa_pc(PROX_PROF)).

%Desligar ou nao o ar
schedule(status(prof(P, A, B), X, ar(ligado, TEMP), Z, W, K, END, proximo_prof(PROX_PROF, INI, FIM)), status(prof(P, A, B), X, ar(desligado, -273), Z, W, K, 1, proximo_prof(PROX_PROF, INI, FIM)), desligar_ar(P)) :- fecha_sala(P, B) ; not(usa_ar(PROX_PROF, TEMP_ARBITRARIA)).

%Desligar ou nao o luz
schedule(status(prof(P, A, B), X, Y, Z, W, luz(ligada), END, proximo_prof(PROX_PROF, INI, FIM)), status(prof(P, A, B), X, Y, Z, W, luz(desligada), 1, proximo_prof(PROX_PROF, INI, FIM)), desligar_luz(P)) :- fecha_sala(P, B).

%Fecha ou nao a sala
schedule(status(prof(P, A, B), sala(aberta), Y, Z, W, K, END, proximo_prof(PROX_PROF, INI, FIM)), status(prof(P, A, B), sala(fechada), Y, Z, W, K, 1, proximo_prof(PROX_PROF, INI, FIM)), fechar_sala(P)) :- fecha_sala(P, B).

%Nao ha proxima aula (ESTADO FINAL)
schedule(status(prof(P, A, B), sala(fechada), ar(desligado, -273), datashow(desligado), pc(desligado), luz(desligada), 1, SEM_AULA), fim, finalizou_aulas) :- not(prox_aula(PROX_PROF, A, INI, FIM)).

%Trocar professor
schedule(status(prof(P, A, B), X, Y, Z, W, K, END, proximo_prof(PROX_PROF, INI, FIM)), status(prof(PROX_PROF, INI, FIM), X, Y, Z, W, K, 0, proximo_prof(PROX_PROF2, INI2, FIM2)), troca_professor ) :- aula(PROX_PROF, INI, FIM), (prox_aula(PROX_PROF2, INI, INI2, FIM2) ; not(prox_aula(PROX_PROF2, INI, INI2, FIM2))).