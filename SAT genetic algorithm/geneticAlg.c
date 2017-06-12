#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

/**************************************************
Autor: Victor Ferreira Teixeira da Silva
***************************************************
Algoritmo genético para o problema sat:
expressão: (D and A) and (C or D)  and (A and B and !E) and (!E and A) and (F) and (C or !F)
***************************************************
***************************************************/
//Encapsulando o cromossomo dentro de indivíduo
typedef struct individual {
  char * chromosome;
  int fitness;
}IND;

//Um elemento da lista
typedef struct NODE{
  struct NODE * next;
  IND * value;
}NODE;

//Lista de nós contendo indivíduos
typedef struct LIST {
  NODE * first;
}LIST;

int fitness(IND * c);

void deallocNode(NODE*n){
  if(!n)return;
  deallocNode(n->next);
  free(n->value);
  free(n);
}
void deallocList(LIST * l){
  if(!l)return
  deallocNode(l->first);
  free(l);
}
//Cria um novo indivíuo ( encapsulamento do cromossomo )
IND * createIndividual(int size){
  IND * new  = malloc(sizeof(IND));
  new->chromosome = calloc(size,sizeof(char));
  new->fitness = -1;
  return new;
}

//Cria uma nova lista
LIST * createList(){
  LIST * new = malloc(sizeof(LIST));
  new->first = NULL;
  return new;
}

//Cria um novo nó
NODE * createNode(){
  NODE * new = malloc(sizeof(NODE));
  new->value = NULL;
  new->next = NULL;
  return new;
}

/*Adiciona um novo elemento na lista ( ordenado por fitness* ).
A ordem facilitará o processo de elitismo no algoritmo genético*/
void addList(LIST * list , char * chromosome){
  if(!list || !chromosome) return;
  NODE * newNode = createNode();
  newNode->value = createIndividual(strlen(chromosome));
  strcpy(newNode->value->chromosome,chromosome);
  fitness(newNode->value);


  if(!list->first || list->first->value->fitness < newNode->value->fitness){
    newNode->next = list->first;
    list->first = newNode;
    return;
  }
  NODE * aux  = list->first;
  while(aux->next && aux->next->value->fitness > newNode->value->fitness)
    aux = aux->next;

  newNode->next = aux->next;
  aux->next = newNode;

}

//Aplica mutação a um cromossomo
void mutate(IND * current){
  int len = strlen(current->chromosome);
  int index = rand()%len;
  current->chromosome[index] = (current->chromosome[index] -'0') == 0 ? '1' : '0';
}

//Gera um novo cromossomo a partir da combinação de dois outros cromossomos
IND * reproduce(IND * first, IND * second){
  if(!first || !second) return NULL;
  int chromSize = strlen(first->chromosome);
  int index = rand()% chromSize;
  index = index > 0 ? index : 1; //o indice não pode ser 0 ( gerario pois 'son' seria igual a 'first')

  //gerando novo filho a partir de first e second
  IND * son = createIndividual(chromSize);
  strcpy(son->chromosome,first->chromosome);
  strcpy(son->chromosome+index,second->chromosome+index);
  return son;
}

//Gera uma popuplação aleatória de tamanho pré-definido
LIST * randomPopulation(int size,int chromSize){
  LIST * population = createList();

  int i;
  char chrom[chromSize];

  #define GENERATE(CROM,SIZE) do{ int __i; for(__i=0;__i<SIZE;__i++){CROM[__i]= rand()%2 + '0'; }  }while(0)
  for(i=0;i<size;i++){
    GENERATE(chrom,chromSize);
    addList(population,chrom);
  }

  return population;
}

//Char para int
int cti(char digit){
  return digit - '0';
}

/* Quantas clausulas são verdadeiras ?
(D && A) + (C || D)  + (A && B && !E) + (!E && A) + (F) + (C || !F)*/
int fitness(IND * c){
  if(!c)return -1;
  if(c->fitness != -1)return c->fitness;
  int A = cti(c->chromosome[0]);
  int B = cti(c->chromosome[1]);
  int C = cti(c->chromosome[2]);
  int D = cti(c->chromosome[3]);
  int E = cti(c->chromosome[4]);
  int F = cti(c->chromosome[5]);
  c->fitness = (D && A) + (C || D)  + (A && B && !E) + (!E && A) + (F) + (C || !F);
  return c->fitness;
}

int GEN = 1; //contando as gerações
char * BESTCHROMO;//melhor cromossomo parcial
int MAXFIT = 0;//melhor fitness parcial
int TOTALREP = 0;
int TOTALMUT = 0;

//Algoritmo Genético
IND * geneticAlgorithm(LIST * population,int goal,int mutateProbability,int elitismAmount){
  NODE * aux = population->first;

  //Calculando fitness de cada indivíduo e preparando a seleção de casais
  int sum = 0, pos = 0,i=0;
  int bestfit = 0,size = 0;
  char * chromo;

  while(aux){
    size++;
    sum+=fitness(aux->value);
    //encontrei um indivíduo que atinge o critério de parada ?
    if(aux->value->fitness >= goal) {
      IND * result = createIndividual(strlen(aux->value->chromosome));
      strcpy(result->chromosome,aux->value->chromosome);
      deallocList(population);
      return result;
    }
    if(aux->value->fitness >= bestfit){
      bestfit = aux->value->fitness;
      chromo = aux->value->chromosome;
    }
    aux = aux->next;
  }

  //Verifica se a geração atual produziu um indivíduo de máximo local
  if(bestfit > MAXFIT){
    MAXFIT = bestfit;
    BESTCHROMO = chromo;
  }

  //Exibe o melhor indivíduo de cada geração
  printf(">Best of GEN(%d):%s, fitness:%d, populacao:%d\n",GEN++,chromo,bestfit,size);

  int index1,index2;
  IND * father = NULL, *mother = NULL, *son = NULL;
  NODE* counter = NULL;
  LIST * newPopulation = createList();

  //Gerando nova população a partir da população atual
  for(counter = population->first ;counter ;counter = counter->next){
    //seleciona casais para reprodução
    pos = 0;
    index1 = rand()%sum;//posição do individuo 1 para reprodução
    index2 = rand()%sum;//posição do individuo 2 para reprodução
    father = NULL, mother = NULL;
    aux = population->first;
    int foundF = 0, foundM = 0;

    //Procurando pelos indivíduos nas posições definidas
    while(!mother || !father){
      pos+= aux->value->fitness;

      if(pos > index1 && !foundF) {
        father = aux->value;
        foundF = 1;
      }
      if(pos > index2 && !foundM) {
        mother = aux->value;
        foundM = 1;
      }
      aux = aux->next;
    }

    //Gerando filho a partir dos indivíduos selecionados
    son = reproduce(father, mother);
    TOTALREP++;

    //Aplicando mutação no filho com uma certa probabilidade
    if(rand()%100 <= mutateProbability){
      mutate(son);
      TOTALMUT++;
    }

    //Armazenando filho na nova população
    addList(newPopulation,son->chromosome);
  }

  aux = population->first;
  for(i=0;i<elitismAmount;i++){
    addList(newPopulation,aux->value->chromosome);
    aux = aux->next;
  }
  //Proxima Geração
  deallocList(population);
  return geneticAlgorithm(newPopulation,goal,mutateProbability,elitismAmount);
}

int main(int argc,char ** argv){
  srand(time(NULL));

  int mutationProbability = 8;//Probabilidade de realizar mutação em um filho gerado (% 0-100)
  int populationSize = 4;//tamanho da população inicial de indivíduos
  int elitismAmount =1;//QUantos dos melhores individuos irão prosseguir para proxima geração
  int chromSize = 6; //tamanho do cromossomo (1 para cada variável SAT)
  int goal = 6;//fitness desejado para concluir a execução

  IND * result = geneticAlgorithm(randomPopulation(populationSize,chromSize),goal,mutationProbability,elitismAmount);

  if(!result){
    printf("\nNao foi possivel encontrar um individuo satisfatorio\n");
    printf("O melhor cromossomo encontrado foi: %s, fitness:%d",BESTCHROMO,MAXFIT);
  }
  else{
    printf("\n\n************************************\n");
    printf("Individuo encontrado como solucao:\ncromossomo:%s, fitness:%d",result->chromosome,fitness(result));
    printf("\n************************************\n");
    printf("Geracoes percorridas:%d\nTotal de reproducoes:%d\nTotal de mutacoes:%d\n",GEN,TOTALREP,TOTALMUT);
  }

  free(result);
  return 0;
}
