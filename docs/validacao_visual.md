# Validação das visualizações

Comando: `.venv/bin/python -m pytest -q`

Resultado real: **43 aprovados em 0,76 s**, incluindo 34 testes anteriores e 9 verificações das visualizações. Streamlit 1.51.0 e pytest 8.4.2.

Verificações: folhas das árvores recompõem três entradas aceitas; rótulos e arestas derivam das tabelas; AppTest percorre páginas, navega nos passos, atualiza exemplos e não apresenta árvore completa para rejeição. Compilação de app, interface, motores e testes concluída.

Não foi realizada inspeção visual em navegador. A tentativa de iniciar o servidor nesta sessão foi impedida pelo ambiente; AppTest executou a interface sem erros. O projeto completo ainda contém as pendências da versão inicial; este registro se refere às visualizações e aos testes existentes.
