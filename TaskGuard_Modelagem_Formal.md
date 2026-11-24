# TaskGuard — especificação formal v1.0

## 1. Escopo e originalidade
Validador didático de registros de tarefas computacionais em Python + Streamlit. A/B abrem tarefas simples/pesadas, F/G fecham tarefas simples/pesadas, R reserva uma unidade de recurso, L libera uma unidade e # separa blocos. Uma tarefa simples demanda uma unidade; uma pesada demanda duas. O encerramento é LIFO. A proposta inicial de quatro blocos intercalados foi ampliada porque a aula 10, p. 8, já apresenta duas igualdades cruzadas. A solução combina tipos de tarefas, reversão e cotas ponderadas; não é apenas uma renomeação daquele exemplo. A equipe deve confirmar a originalidade em relação a exercícios não presentes nas fontes.

Alfabeto de ambos os módulos: Σ = {A,B,R,F,G,L,#}. Entrada estritamente sensível a maiúsculas; não remover espaços nem converter caixa. Cadeia vazia é entrada do alfabeto e deve ser rejeitada pelos autômatos; caracteres externos geram erro de entrada separado de rejeição formal. Não impor comprimento mínimo na linguagem: 18 é requisito dos exemplos principais, não condição de aceitação. Ambos os módulos podem rodar isoladamente; na integração a mesma cadeia integral vai ao AP e, somente se aceita, ao ALL.

## 2. Linguagens e gramática
Defina h(A)=F, h(B)=G, estendida símbolo a símbolo; w^R é a reversão. Seja k(w)=|w|_A+2|w|_B (notação matemática, não algoritmo de aceitação).

L_AP = { w#R^r#h(w^R)#L^l | w ∈ {A,B}+, r,l ≥ 1 }.

L_ALL = { w#R^k(w)#h(w^R)#L^k(w) | w ∈ {A,B}+ }.

L_ALL é subconjunto próprio de L_AP; por exemplo, B#R#G#L pertence apenas a L_AP. A menor cadeia de ambas é A#R#F#L, 7 símbolos; a vazia é rejeitada.

G = (V,T,P,S), V={S,C,D,E}, T=Σ, símbolo inicial S.
```
S → C#E
C → ACF | BCG | A#D#F | B#D#G
D → RD | R
E → LE | L
```
Derivação mais à esquerda (cada seta aplica uma produção):
```
S ⇒ C#E ⇒ ACF#E ⇒ ABCGF#E ⇒ ABACFGF#E
⇒ ABAB#D#GFGF#E ⇒ ABAB#RD#GFGF#E
⇒ ABAB#RRD#GFGF#E ⇒ ABAB#RRRD#GFGF#E
⇒ ABAB#RRRRD#GFGF#E ⇒ ABAB#RRRRRD#GFGF#E
⇒ ABAB#RRRRRR#GFGF#E ⇒ ABAB#RRRRRR#GFGF#LE
⇒ ABAB#RRRRRR#GFGF#LLE ⇒ ABAB#RRRRRR#GFGF#LLLE
⇒ ABAB#RRRRRR#GFGF#LLLLE ⇒ ABAB#RRRRRR#GFGF#LLLLLE
⇒ ABAB#RRRRRR#GFGF#LLLLLL
```
A cadeia tem 23 caracteres. Cada C acrescenta abertura e fechamento nas extremidades; a alternativa base garante uma abertura e uma finalização, com o bloco R positivo. E gera L positivo. Por indução, a gramática gera exatamente L_AP.

### Não regularidade de L_AP
Suponha regular e seja p≥1 seu comprimento de bombeamento. z=A^p#R#F^p#L pertence à linguagem. Para qualquer decomposição z=uvw com |uv|≤p e |v|>0, v=A^j, j≥1. Para i=0, uv^0w tem p-j aberturas e p fechamentos; não pertence. Contradição. Logo L_AP é Tipo 2, não Tipo 3.

### L_ALL não é livre de contexto
Suponha LLC e seja p≥1 o comprimento de bombeamento. Escolha z=A^p#R^p#F^p#L^p, pertencente a L_ALL. Para qualquer decomposição z=uvwxy com |vwx|≤p e |vx|>0, bombeie i=0. Se v ou x contém #, a cadeia perde um separador e fica inválida. Caso contrário, a remoção altera pelo menos um bloco, e o intervalo vwx pode alcançar no máximo dois blocos adjacentes (três blocos exigiriam atravessar um bloco de p símbolos inteiro e dois separadores). Pelo menos dois blocos permanecem com p símbolos. Como a cadeia resultante tem apenas tarefas A, os quatro blocos devem ter a mesma quantidade; isso é impossível. Logo uv^0wx^0y não pertence, contradizendo o lema. L_ALL não é LLC. A construção do ALL abaixo prova que é LSC, Tipo 1 estrito. Não é necessário apresentar GSC pela lauda.

## 3. AP determinístico
M_AP=(Q,Σ,Γ,δ,q0,Z,F_AP), Q={q0,...,q7}, Γ={X,Y,Z}, F_AP={q7}. X representa tarefa A e Y tarefa B; Z é fundo da pilha. Configuração inicial (q0, entrada integral, Z). Topo escrito à esquerda. Posição i começa em 0 e representa a próxima posição a ler, aumentando de 1 por transição. δ(q,s,t)=(q',γ) consome s, substitui somente t por γ, muda de estado; ε significa retirar o topo. Sem transições ε na entrada. Não há transição de rejeição: combinação ausente para a entrada restante ou fim fora de q7 implica rejeição. Aceitação por estado final com entrada integralmente consumida; Z permanece (invariante de q7).

| Estado | Função |
|---|---|
| q0 | Exigir primeira abertura |
| q1 | Empilhar aberturas adicionais |
| q2 | Exigir primeiro R |
| q3 | Ler reservas adicionais |
| q4 | Exigir primeira finalização correspondente |
| q5 | Desempilhar finalizações correspondentes; # só com Z |
| q6 | Exigir primeiro L |
| q7 | Ler liberações adicionais; final |

### Tabela completa: 21 transições
| Estado | Entrada | Topo | Destino | Substituição |
|---|---|---|---|---|
| q0 | `A` | Z | q1 | XZ |
| q0 | `B` | Z | q1 | YZ |
| q1 | `A` | X | q1 | XX |
| q1 | `A` | Y | q1 | XY |
| q1 | `B` | X | q1 | YX |
| q1 | `B` | Y | q1 | YY |
| q1 | `#` | X | q2 | X |
| q1 | `#` | Y | q2 | Y |
| q2 | `R` | X | q3 | X |
| q2 | `R` | Y | q3 | Y |
| q3 | `R` | X | q3 | X |
| q3 | `R` | Y | q3 | Y |
| q3 | `#` | X | q4 | X |
| q3 | `#` | Y | q4 | Y |
| q4 | `F` | X | q5 | ε |
| q4 | `G` | Y | q5 | ε |
| q5 | `F` | X | q5 | ε |
| q5 | `G` | Y | q5 | ε |
| q5 | `#` | Z | q6 | Z |
| q6 | `L` | Z | q7 | Z |
| q7 | `L` | Z | q7 | Z |

Invariante: após aberturas, a pilha representa w em ordem inversa (A→X, B→Y) sobre Z; R não altera pilha. Cada F/G só retira o topo compatível. O terceiro # exige Z. Os estados exigem os blocos positivos e ordem correta. Assim o AP reconhece exatamente a GLC. Cada transição consome um caractere e a máquina para ao terminar a entrada ou não encontrar transição: O(N) tempo, O(N) pilha (N= comprimento da entrada).

### Rastreamento AP da demonstração
Topo à esquerda. i é o número de símbolos já consumidos; a linha 0 é a configuração inicial.
| Passo/i | Estado | Pilha | Entrada restante |
|---|---|---|---|
| 0 | q0 | `Z` | `ABAB#RRRRRR#GFGF#LLLLLL` |
| 1 | q1 | `XZ` | `BAB#RRRRRR#GFGF#LLLLLL` |
| 2 | q1 | `YXZ` | `AB#RRRRRR#GFGF#LLLLLL` |
| 3 | q1 | `XYXZ` | `B#RRRRRR#GFGF#LLLLLL` |
| 4 | q1 | `YXYXZ` | `#RRRRRR#GFGF#LLLLLL` |
| 5 | q2 | `YXYXZ` | `RRRRRR#GFGF#LLLLLL` |
| 6 | q3 | `YXYXZ` | `RRRRR#GFGF#LLLLLL` |
| 7 | q3 | `YXYXZ` | `RRRR#GFGF#LLLLLL` |
| 8 | q3 | `YXYXZ` | `RRR#GFGF#LLLLLL` |
| 9 | q3 | `YXYXZ` | `RR#GFGF#LLLLLL` |
| 10 | q3 | `YXYXZ` | `R#GFGF#LLLLLL` |
| 11 | q3 | `YXYXZ` | `#GFGF#LLLLLL` |
| 12 | q4 | `YXYXZ` | `GFGF#LLLLLL` |
| 13 | q5 | `XYXZ` | `FGF#LLLLLL` |
| 14 | q5 | `YXZ` | `GF#LLLLLL` |
| 15 | q5 | `XZ` | `F#LLLLLL` |
| 16 | q5 | `Z` | `#LLLLLL` |
| 17 | q6 | `Z` | `LLLLLL` |
| 18 | q7 | `Z` | `LLLLL` |
| 19 | q7 | `Z` | `LLLL` |
| 20 | q7 | `Z` | `LLL` |
| 21 | q7 | `Z` | `LL` |
| 22 | q7 | `Z` | `L` |
| 23 | q7 | `Z` | `ε` |

## 4. ALL determinístico
M_ALL=(Q,Σ,Γ,δ,q0,q25,q26), Q={q0,...,q26}, Σ={A,B,R,F,G,L,#}, Γ=Σ ∪ {a,b,r,f,g,l,⊢,⊣}. q0 inicial; q25 aceitação; q26 rejeição. Marcadores fixos ⊢ e ⊣. Para entrada w de N caracteres, fita inicial ⊢w⊣, com N células graváveis, índices 1..N, e marcadores 0 e N+1. Cabeçote inicial índice 1 (para vazia está no marcador direito). A fita é inicializada uma vez, nunca redimensionada. O controle só consulta o símbolo sob o cabeçote, o estado e a tabela. Em δ(q,s)=(q',t,d), escrever t na célula atual, mover uma posição L (esquerda) ou R (direita), ou S (parado, usado somente para parar), e mudar estado. Marcadores só podem ser reescritos pelo mesmo símbolo (implementação: não escrever de fato) e não podem ser ultrapassados. Não existem transições saindo dos estados de parada. Qualquer par estado não final/símbolo de Γ não previsto vai a q26 preservando símbolo e cabeçote (S). Assim, 133 pares explícitos + 242 de rejeição padrão = 375 transições para 25 estados não terminais × 15 símbolos. Não são permitidos caracteres auxiliares na entrada externa.

### Estados (27)
| Estado | Papel |
|---|---|
| q0 | Exigir A/B inicial |
| q1 | Percorrer bloco de aberturas |
| q2 | Exigir primeiro R |
| q3 | Percorrer reservas |
| q4 | Exigir primeiro F/G |
| q5 | Percorrer finalizações |
| q6 | Exigir primeiro L |
| q7 | Percorrer liberações e detectar borda direita |
| q8 | Retornar à borda esquerda para novo ciclo |
| q9 | Selecionar e marcar próxima abertura A/B; se #, verificar resíduos |
| q10 | Para A, buscar início do bloco L/l |
| q11 | Para B, buscar início do bloco L/l |
| q12 | Para A, atravessar último # à esquerda |
| q13 | Para B, atravessar último # à esquerda |
| q14 | Para A, procurar F não marcado mais à direita e marcar f |
| q15 | Para B, procurar G não marcado mais à direita e marcar g |
| q16 | Retornar à borda esquerda após fechar A |
| q17 | Retornar à borda esquerda após fechar B |
| q18 | Buscar e marcar primeiro R para A |
| q19 | Buscar e marcar primeiro R para B |
| q20 | Exigir e marcar segundo R para B |
| q21 | Buscar e marcar primeiro L para A |
| q22 | Buscar e marcar primeiro L para B |
| q23 | Exigir e marcar segundo L para B |
| q24 | Confirmar ausência de símbolos não marcados nos blocos restantes |
| q25 | Aceitar e parar |
| q26 | Rejeitar e parar |

### Tabela de transições compacta e completa por convenção
Cada grupo de leitura representa uma regra para cada símbolo listado, nunca uma leitura de vários caracteres. T = Γ sem os marcadores = {A,B,R,F,G,L,#,a,b,r,f,g,l}. `=` significa manter o símbolo lido. L/R/S são movimentos e não símbolos escritos. Os estados q0..q7 validam somente o formato. Todas as combinações ausentes têm a regra padrão q26, =, S. O motor deve expandir os grupos em chaves individuais, sem sobreposições. A fita e as regras são a única fonte da decisão.

| Estado | Lê | Destino | Escreve | Move |
|---|---|---|---|---|
| q0 | `A,B` | q1 | `=` | R |
| q1 | `A,B` | q1 | `=` | R |
| q1 | `#` | q2 | `=` | R |
| q2 | `R` | q3 | `=` | R |
| q3 | `R` | q3 | `=` | R |
| q3 | `#` | q4 | `=` | R |
| q4 | `F,G` | q5 | `=` | R |
| q5 | `F,G` | q5 | `=` | R |
| q5 | `#` | q6 | `=` | R |
| q6 | `L` | q7 | `=` | R |
| q7 | `L` | q7 | `=` | R |
| q7 | `⊣` | q8 | `=` | L |
| q8 | `T` | q8 | `=` | L |
| q8 | `⊢` | q9 | `=` | R |
| q9 | `a,b` | q9 | `=` | R |
| q9 | `A` | q10 | `a` | R |
| q9 | `B` | q11 | `b` | R |
| q9 | `#` | q24 | `=` | R |
| q10 | `#,A,B,F,G,R,f,g,r` | q10 | `=` | R |
| q10 | `L,l` | q12 | `=` | L |
| q11 | `#,A,B,F,G,R,f,g,r` | q11 | `=` | R |
| q11 | `L,l` | q13 | `=` | L |
| q12 | `#` | q14 | `=` | L |
| q13 | `#` | q15 | `=` | L |
| q14 | `f,g` | q14 | `=` | L |
| q14 | `F` | q16 | `f` | L |
| q15 | `f,g` | q15 | `=` | L |
| q15 | `G` | q17 | `g` | L |
| q16 | `T` | q16 | `=` | L |
| q16 | `⊢` | q18 | `=` | R |
| q17 | `T` | q17 | `=` | L |
| q17 | `⊢` | q19 | `=` | R |
| q18 | `#,A,B,a,b,r` | q18 | `=` | R |
| q19 | `#,A,B,a,b,r` | q19 | `=` | R |
| q18 | `R` | q21 | `r` | R |
| q19 | `R` | q20 | `r` | R |
| q20 | `R` | q22 | `r` | R |
| q21 | `#,F,G,R,f,g,l,r` | q21 | `=` | R |
| q22 | `#,F,G,R,f,g,l,r` | q22 | `=` | R |
| q21 | `L` | q8 | `l` | L |
| q22 | `L` | q23 | `l` | R |
| q23 | `L` | q8 | `l` | L |
| q24 | `#,f,g,l,r` | q24 | `=` | R |
| q24 | `⊣` | q25 | `=` | S |


### Correção e parada
Após validação de formato (q0..q7), a máquina retorna à esquerda. A cada ciclo completo, marca a primeira abertura ainda maiúscula como a/b. Busca o fechamento ainda maiúsculo mais à direita, exige F para A ou G para B e marca f/g. Retorna e marca o primeiro R e o primeiro L disponíveis; para B exige dois de cada. A ordem de escolha garante prefixos marcados nos blocos R e L e sufixo marcado no bloco de fechamentos. Após j ciclos, exatamente j aberturas e j fechamentos correspondentes foram marcados, e a quantidade de R/L marcados é a soma das cotas das j aberturas. Quando não restam aberturas, q24 só atravessa r,f,g,l,# e aceita na borda direita. Falta de par, fechamento incompatível ou reserva/liberação insuficiente rejeita antes; sobras rejeitam em q24. Assim aceita exatamente L_ALL, independentemente do AP.

Cada fase move o cabeçote em uma direção até encontrar um símbolo ou rejeitar. Cada ciclo completo marca uma nova abertura; nunca desmarca. Há no máximo N ciclos e um número constante de varreduras de comprimento O(N) por ciclo. Portanto termina em O(N²) transições e usa O(N) espaço de trabalho (exatamente N células graváveis), além do controle finito e cabeçote. O registro de rastreamento e a interface são observadores externos à máquina; nunca são consultados pelo motor para aceitar/rejeitar. Guardar cópia integral da fita por passo pode usar O(N³) memória no simulador, não no modelo formal. Não usar contador, índice de bloco, pilha, regex, split, count, comparação de strings ou outra memória auxiliar para a decisão do ALL; o índice do cabeçote e tamanho para limites físicos são permitidos. Passos podem ser numerados somente para exibição. O motor não precisa de timeout arbitrário para rejeitar.

### Rastreamento resumido ALL
A cadeia de demonstração percorre 380 transições (incluindo a transição final) com esta tabela, 25 células totais e 23 graváveis. As linhas seguintes são configurações selecionadas após a primeira, segunda, terceira e quarta rodadas, na borda esquerda antes de começar novo ciclo. A interface deve apresentar TODOS os passos, não apenas os ciclos.
| Ciclo | Fita |
|---|---|
| 0 | `⊢ABAB#RRRRRR#GFGF#LLLLLL⊣` |
| 1 | `⊢aBAB#rRRRRR#GFGf#lLLLLL⊣` |
| 2 | `⊢abAB#rrrRRR#GFgf#lllLLL⊣` |
| 3 | `⊢abaB#rrrrRR#Gfgf#llllLL⊣` |
| 4 | `⊢abab#rrrrrr#gfgf#llllll⊣` |
Após q24 verificar toda a parte restante, q25 aceita na borda direita. Cada ciclo marca as cotas de acordo com o tipo de tarefa; nenhuma célula nova é criada.

## 5. Testes obrigatórios
Os 32 casos a seguir têm pelo menos 18 caracteres, são distintos dentro de cada módulo e usam somente Σ. A decisão obtida abaixo refere-se à simulação de referência das tabelas, NÃO ao software final. O Codex deve reproduzir estes testes na implementação e exportar resultados obtidos reais.

### AP — aceitas
| Entrada | N | Esperado | Referência | Regra |
|---|---:|---|---|---|
| `AAAA#RRRR#FFFF#LLLL` | 19 | Aceita | Aceita | LIFO e formato |
| `ABAB#RRRRRR#GFGF#LLLLLL` | 23 | Aceita | Aceita | LIFO e formato |
| `BBBB#RRRRRRRR#GGGG#LLLLLLLL` | 27 | Aceita | Aceita | LIFO e formato |
| `BABA#RRRRRR#FGFG#LLLLLL` | 23 | Aceita | Aceita | LIFO e formato |
| `AABB#RRRRR#GGFF#LLLLLLL` | 23 | Aceita | Aceita | R/L independentes no AP |
| `BBAA#RRRRRRR#FFGG#LLLLL` | 23 | Aceita | Aceita | R/L independentes no AP |
| `AAAAA#RRRR#FFFFF#LLLLLL` | 23 | Aceita | Aceita | R/L independentes no AP |
| `ABAAB#RRRRRRRR#GFFGF#LLLLLLLL` | 29 | Aceita | Aceita | R/L independentes no AP |

### AP — rejeitadas
| Entrada | N | Esperado | Referência | Regra |
|---|---:|---|---|---|
| `ABAB#RRRRRR#FGFG#LLLLLL` | 23 | Rejeita | Rejeita | Fechamento fora de ordem |
| `AAAA#RRRR#FFF#LLLL` | 18 | Rejeita | Rejeita | F insuficiente |
| `BBBB#RRRRRRRR#GGGGG#LLLLLLLL` | 28 | Rejeita | Rejeita | G excedente |
| `ABAB#RRRRRR#GGFF#LLLLLL` | 23 | Rejeita | Rejeita | Tipo incompatível |
| `ABAB##GFGF#LLLLLLLLLLLL` | 23 | Rejeita | Rejeita | Bloco R vazio |
| `ABAB#RRRRRRRRRRRR#GFGF#` | 23 | Rejeita | Rejeita | Bloco L vazio |
| `ABABRRRRRR#GFGF#LLLLLL` | 22 | Rejeita | Rejeita | Separador ausente |
| `ABAB#RRARRR#GFGF#LLLLLL` | 23 | Rejeita | Rejeita | A no bloco R |

### ALL — aceitas
| Entrada | N | Esperado | Referência | Regra |
|---|---:|---|---|---|
| `AAAA#RRRR#FFFF#LLLL` | 19 | Aceita | Aceita | LIFO e cotas corretas |
| `ABAB#RRRRRR#GFGF#LLLLLL` | 23 | Aceita | Aceita | LIFO e cotas corretas |
| `BBBB#RRRRRRRR#GGGG#LLLLLLLL` | 27 | Aceita | Aceita | LIFO e cotas corretas |
| `BABA#RRRRRR#FGFG#LLLLLL` | 23 | Aceita | Aceita | LIFO e cotas corretas |
| `AABB#RRRRRR#GGFF#LLLLLL` | 23 | Aceita | Aceita | LIFO e cotas corretas |
| `BBAA#RRRRRR#FFGG#LLLLLL` | 23 | Aceita | Aceita | LIFO e cotas corretas |
| `AAAAA#RRRRR#FFFFF#LLLLL` | 23 | Aceita | Aceita | LIFO e cotas corretas |
| `ABAAB#RRRRRRR#GFFGF#LLLLLLL` | 27 | Aceita | Aceita | LIFO e cotas corretas |

### ALL — rejeitadas
| Entrada | N | Esperado | Referência | Regra |
|---|---:|---|---|---|
| `ABAB#RRRRR#GFGF#LLLLLL` | 22 | Rejeita | Rejeita | R insuficiente |
| `ABAB#RRRRRRR#GFGF#LLLLLL` | 24 | Rejeita | Rejeita | R excedente |
| `ABAB#RRRRRR#GFGF#LLLLL` | 22 | Rejeita | Rejeita | L insuficiente |
| `ABAB#RRRRRR#GFGF#LLLLLLL` | 24 | Rejeita | Rejeita | L excedente |
| `ABAB#RRRRR#GFGF#LLLLL` | 21 | Rejeita | Rejeita | R/L iguais mas abaixo da cota |
| `ABAB#RRRRRRR#GFGF#LLLLLLL` | 25 | Rejeita | Rejeita | R/L iguais mas acima da cota |
| `ABAB#RRRRRR#FGFG#LLLLLL` | 23 | Rejeita | Rejeita | Fechamento fora de ordem |
| `ABAB##GFGF#LLLLLLLLLLLL` | 23 | Rejeita | Rejeita | Bloco R vazio |

### Casos-limite adicionais (por módulo)
| Entrada | AP | ALL | Regra |
|---|---|---|---|
| ε (string vazia) | Rejeita | Rejeita | Todos os blocos obrigatórios |
| `A#R#F#L` | Aceita | Aceita | Menor cadeia aceita |
| `B#RR#G#LL` | Aceita | Aceita | Menor tarefa pesada válida |
| `B#R#G#L` | Aceita | Rejeita | Tarefa pesada demanda duas unidades |

### Integração e alfabeto
| Entrada | AP | ALL | Regra |
|---|---|---|---|
| `ABAB#RRRRRR#GFGF#LLLLLL` | Aceita | Aceita | Tudo correto |
| `ABAB#RRRRRR#FGFG#LLLLLL` | Rejeita | Não executado | Ordem de fechamento incorreta |
| `ABAB#RRRRR#GFGF#LLLLL` | Aceita | Rejeita | Reservas e liberações iguais, porém insuficientes |
| `ABAB#RRRRRR#GFGF#LLLLLX` | Não executado | Não executado | Erro de alfabeto: símbolo 'X' fora do alfabeto na posição 23 (índice 22). |

Testar também símbolos auxiliares, marcadores, espaços e minúsculas como entrada inválida. Verificar todas as configurações de teste: tamanho fixo, bordas imutáveis, movimento de um passo (ou S na parada), escrita somente na posição anterior do cabeçote e consistência com δ. AP: avanço unitário, alteração apenas no topo, final q7 com Z e entrada consumida. Testar alcance de todos os estados, ausência de chaves duplicadas, integração não invocar ALL se AP rejeitar e execução isolada do ALL sem AP. Nenhuma configuração futura ou oráculo pode decidir a aceitação.

Validação preliminar feita com um simulador independente de referência: 21 transições AP, 133 regras explícitas ALL, 29.561 entradas comparadas com um oráculo matemático exclusivo dos testes (21.760 combinações estruturadas; 5.000 mutações pseudoaleatórias com seed 42; 2.801 cadeias arbitrárias de comprimento 0..4 sobre Σ). Sem divergências observadas. Não é prova por testes nem evidência de implementação do aplicativo final. A prova formal está acima.

## 6. Referências didáticas e limitações
SOUZA, Daniel Leal. Linguagens Formais e Autômatos. CESUPA, 2024. Materiais fornecidos: aula 06 (expressões regulares), p. 4, notações; aula 07 (linguagens não regulares), p. 7 e 17–18, bombeamento; aula 08 (linguagens livres de contexto), p. 14 e 19–21, GLC e derivação; aula 09 (autômato com pilha), p. 18–23, tupla, transições, configuração e diagramas; aula 10 (lema do bombeamento para LLC), p. 7–8, lema e dependências cruzadas; aula 11 (linguagens sensíveis ao contexto), p. 13 e 16–17, fita limitada e hierarquia. As regras, tabelas e testes são modelagem do TaskGuard, não transcrição dos exercícios. A notação de ALL é uma especificação própria, compatível com a lauda e o conceito de fita limitada.

Limitações a discutir: registro é um modelo abstrato em quatro fases, não representa tarefas concorrentes arbitrárias nem identidade individual; aceita apenas cotas discretas 1/2; custo quadrático das varreduras e potencial custo cúbico de guardar snapshots completos. A equipe deverá medir o desempenho do aplicativo final e relatar observações reais. Não afirmar que a ferramenta garante correção de sistemas reais.
