# TaskGuard
Validador didático de tarefas por AP e ALL. Consulte a modelagem formal original.

Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```
No PowerShell: `python -m venv .venv` e `.venv\Scripts\Activate.ps1`.

O ALL usa fita fixa e transições documentadas. Snapshots são memória externa e podem custar O(N³). Modelo abstrato, sem garantia para sistemas reais. ChatGPT apoiou a modelagem; Codex implementou o protótipo. Revisão humana e confirmação de originalidade permanecem pendentes.

## Visualizações

Após executar uma cadeia, use os botões Início, Anterior, Próximo e Fim ou o seletor de passo. O estado amarelo no diagrama corresponde à configuração selecionada. A pilha mostra o topo acima; a fita mostra índices e destaca o cabeçote. O ALL pode ser visualizado por fase ou completo; arestas tracejadas representam as regras padrão de rejeição. Os diagramas são derivados das tabelas dos motores, sem alterar decisões.

Para cadeias aceitas pelo AP, a árvore de derivação mostra as produções da GLC e as folhas da esquerda para a direita recompõem a entrada. A árvore explica a cadeia completa, independentemente do passo selecionado; não verifica cotas ALL. Diagramas e árvore podem ser baixados em DOT. A renderização no Streamlit não exige instalar o executável Graphviz.

Os testes de interface usam Streamlit AppTest; não substituem uma inspeção visual em navegador. Execute `python -m pytest -q` para verificar motores e visualizações.

### Leitura dos diagramas

As fontes dos diagramas começam em 24 e da árvore em 26, ajustáveis até 40. O layout padrão é vertical e compacto; a opção horizontal continua disponível. As áreas têm 850/900 pixels de altura com rolagem e ampliação em tela cheia. As setas padrão de rejeição ALL ficam ocultas inicialmente para reduzir cruzamentos; marque a opção correspondente para exibi-las. Essa preferência só altera a representação, não as transições executadas.

### Alfabeto, gramática e derivações

O alfabeto de entrada permanece visível na barra lateral. O painel principal apresenta `G = (V, T, P, S)`, seus conjuntos e todas as produções da gramática original do TaskGuard. Os alfabetos internos da pilha e da fita ficam em um painel adicional.

Para entradas aceitas pelo AP, a seção da árvore contém abas DEE e DED: cada linha aplica uma produção à variável mais à esquerda ou mais à direita, respectivamente. Ambas recompõem a entrada executada e podem ser baixadas em texto. São explicações didáticas posteriores à decisão do motor. A gramática descreve L_AP; as cotas ponderadas de L_ALL continuam sendo verificadas pelas transições do ALL.
