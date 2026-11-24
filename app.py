"""Interface didática; todos os resultados vêm dos motores."""
import json
from pathlib import Path
import streamlit as st
from automatos.validador import executar, validar
from interface.gramatica import GRAMATICA_TEXTO, derivar, texto_derivacao
from interface.visuais import (
    FASES, arvore_derivacao, diagrama, fase_do_estado, fita_html, pilha_html,
)

st.set_page_config(page_title='TaskGuard', layout='wide')
st.title('TaskGuard')
st.caption('A/B: tarefas simples/pesadas · F/G: encerramentos · R/L: reserva/liberação · #: separador · cotas 1/2')
st.sidebar.markdown('### Alfabeto de entrada')
st.sidebar.code('Σ = {A, B, R, F, G, L, #}', language=None)
st.sidebar.caption('Somente estes sete símbolos, em maiúsculas. # separa os quatro blocos. Espaços e símbolos auxiliares não são entrada válida.')
pagina = st.sidebar.radio('Navegação', ['Início', 'Validador completo', 'Simulador AP', 'Simulador ALL', 'Modelagem formal', 'Testes'])


with st.container(border=True):
    st.subheader('Alfabeto e gramática do TaskGuard')
    esquerda_gramatica, direita_gramatica = st.columns([3, 2])
    with esquerda_gramatica:
        st.code(GRAMATICA_TEXTO, language=None)
    with direita_gramatica:
        st.markdown('**Significado dos terminais**')
        st.markdown('**A** abre tarefa simples · **B** abre tarefa pesada  \n**F** fecha tarefa simples · **G** fecha tarefa pesada  \n**R** reserva uma unidade · **L** libera uma unidade  \n**#** separa blocos')
        st.markdown('**V**: variáveis (não terminais) · **T = Σ**: terminais · **P**: produções · **S**: símbolo inicial.')
        st.info('Esta gramática gera L_AP. O ALL também exige as cotas: A demanda 1 unidade e B demanda 2 unidades de R e de L.')
    with st.expander('Alfabetos internos dos autômatos'):
        st.code('AP:  Γ = {X, Y, Z}\nALL: Γ = {A, B, R, F, G, L, #, a, b, r, f, g, l, ⊢, ⊣}', language=None)
        st.caption('X/Y representam tarefas A/B na pilha; Z é o fundo. As minúsculas são marcações de fita e ⊢/⊣ são bordas fixas; não podem ser digitadas na entrada.')


def mostrar_diagrama(modulo, estado=None, chave='modelo'):
    fonte = st.slider('Tamanho dos textos', 18, 40, 24, key=f'fonte_{chave}')
    horizontal = st.checkbox('Disposição horizontal', key=f'horizontal_{chave}')
    padrao = st.checkbox('Mostrar setas de rejeição padrão', value=False, key=f'padrao_{chave}') if modulo == 'ALL' else False
    opcoes_visuais = dict(fonte=fonte, direcao='LR' if horizontal else 'TB', mostrar_padrao=padrao)
    if modulo == 'ALL':
        opcoes = ['Fase atual', *FASES, 'Completo'] if estado else [*FASES, 'Completo']
        escolha = st.selectbox('Visualizar diagrama ALL', opcoes, key=f'fase_{chave}')
        fase = fase_do_estado(estado) if escolha == 'Fase atual' else None if escolha == 'Completo' else escolha
        dot = diagrama(modulo, estado, fase, **opcoes_visuais)
        st.caption('Arestas: leitura → escrita, movimento. As setas padrão ficam ocultas inicialmente para facilitar a leitura; todas as regras continuam em execução. Nós externos à fase mostram seus destinos.')
    else:
        dot = diagrama(modulo, estado, **opcoes_visuais)
        st.caption('Arestas: entrada, topo → substituição. ε retira o topo; combinações ausentes bloqueiam o AP.')
    st.graphviz_chart(dot, width='content', height=850)
    st.caption('Use a tela cheia no canto superior direito para ampliar. Role a área do diagrama para percorrer a imagem.')
    st.caption('Amarelo: estado atual · Verde: aceitação · Vermelho: rejeição ALL · Círculo duplo: estado de parada ALL ou estado final AP.')
    st.download_button('Baixar diagrama DOT', dot, f'automato_{modulo}.dot', key=f'dot_{chave}')


def mostrar_execucao(modulo, resultado, entrada, chave):
    st.subheader(f'{modulo}: {resultado["resultado"]}')
    st.write(resultado.get('motivo', ''))
    passos = resultado['passos']
    if not passos:
        st.info('Este módulo não possui passos executados.')
        return
    st.write('Transições executadas:', len(passos)-1)
    indice_key = f'indice_{chave}'
    st.session_state.setdefault(indice_key, 0)
    def mover(destino):
        st.session_state[indice_key] = destino
    n = min(st.session_state[indice_key], len(passos)-1)
    botoes = st.columns(4)
    for coluna, rotulo, destino in zip(botoes, ['⏮ Início', '◀ Anterior', 'Próximo ▶', 'Fim ⏭'], [0, max(0,n-1), min(len(passos)-1,n+1), len(passos)-1]):
        coluna.button(rotulo, key=f'{chave}_{rotulo}', on_click=mover, args=(destino,), disabled=destino==n)
    if len(passos)>1:
        n = st.slider('Passo '+modulo, 0, len(passos)-1, key=indice_key)
    atual = passos[n]
    st.markdown(f'**Passo {n} · Estado {atual["estado"]} · Posição {atual["posição"]} (base 0)**')
    st.caption('As visualizações abaixo usam a configuração real deste passo. O índice 0 representa a configuração inicial.')
    if modulo == 'AP':
        esquerda, direita = st.columns([1,3])
        with esquerda:
            st.markdown('**Pilha — topo acima**')
            st.markdown(pilha_html(atual['pilha']), unsafe_allow_html=True)
        with direita:
            st.markdown('**Entrada e próxima posição a ler**')
            st.markdown(fita_html(entrada, atual['posição']), unsafe_allow_html=True)
            if atual['posição']==len(entrada):
                st.caption('Entrada integralmente consumida; cabeçote após a última célula.')
            st.code(atual['restante'] or 'ε')
    else:
        st.markdown('**Fita limitada — índices incluem os marcadores**')
        st.markdown(fita_html(atual['fita'], atual['posição']), unsafe_allow_html=True)
        st.caption('Verde: símbolo marcado · Cinza: borda fixa · Amarelo: célula sob o cabeçote. A fita mantém o mesmo tamanho em todos os passos.')
    with st.expander('Diagrama do autômato', expanded=True):
        mostrar_diagrama(modulo, atual['estado'], chave)
    if modulo == 'AP':
        with st.expander('Árvore de derivação da cadeia', expanded=True):
            if resultado['resultado']=='ACEITA':
                fonte_arvore = st.slider('Tamanho dos textos da árvore', 18, 40, 26, key=f'fonte_arvore_{chave}')
                dot = arvore_derivacao(entrada, fonte=fonte_arvore)
                st.caption('GLC: S → C#E; C → ACF | BCG | A#D#F | B#D#G; D → RD | R; E → LE | L. Leia as folhas da esquerda para a direita.')
                st.graphviz_chart(dot, width='content', height=900)
                st.caption('Amplie pela tela cheia no canto superior direito. A área permite rolagem para árvores grandes.')
                st.download_button('Baixar árvore DOT', dot, 'arvore_derivacao.dot', key=f'arvore_{chave}')
                st.info('A árvore explica a aceitação da cadeia completa pelo AP; ela não corresponde a um passo parcial e não verifica as cotas do ALL.')
                st.markdown('### Derivações da cadeia aceita')
                st.caption('Cada seta aplica uma única produção. DEE expande a variável mais à esquerda; DED, a mais à direita. Ambas geram a mesma cadeia e são explicações externas ao motor.')
                aba_dee, aba_ded = st.tabs(['DEE — à esquerda', 'DED — à direita'])
                for aba, direcao in ((aba_dee, 'DEE'), (aba_ded, 'DED')):
                    with aba:
                        texto = texto_derivacao(derivar(entrada, direcao))
                        st.code(texto, language=None, wrap_lines=True)
                        st.download_button('Baixar '+direcao, texto, direcao+'.txt', key=f'derivacao_{direcao}_{chave}')
            else:
                st.info('Não existe árvore de derivação completa nesta gramática para uma cadeia rejeitada pelo AP.')
    with st.expander('Dados e tabela do rastreamento'):
        st.json(atual)
        st.dataframe(passos, use_container_width=True)
    st.download_button('Exportar rastreamento '+modulo, json.dumps(resultado, ensure_ascii=False), modulo+'.json', key=f'json_{chave}')


if pagina == 'Modelagem formal':
    a,b = st.tabs(['Diagramas', 'Especificação completa'])
    with a:
        st.subheader('Autômato com pilha'); mostrar_diagrama('AP', chave='formal_ap')
        st.subheader('Autômato linearmente limitado'); mostrar_diagrama('ALL', chave='formal_all')
    with b:
        st.markdown(Path(__file__).with_name('TaskGuard_Modelagem_Formal.md').read_text())
elif pagina == 'Testes':
    st.code('python -m pytest -q')
else:
    if pagina == 'Início':
        st.write('Explore os estados dos autômatos, a pilha, a fita limitada e a árvore de derivação. Execute um exemplo e navegue pelos passos abaixo.')
    exemplos = ['ABAB#RRRRRR#GFGF#LLLLLL', 'ABAB#RRRRRR#FGFG#LLLLLL', 'ABAB#RRRRR#GFGF#LLLLL', 'ABAB#RRRRRR#GFGF#LLLLLX']
    def trocar_exemplo():
        st.session_state['entrada'] = st.session_state['exemplo']
    st.selectbox('Exemplo', exemplos, key='exemplo', on_change=trocar_exemplo)
    entrada = st.text_input('Cadeia', value=exemplos[0], key='entrada')
    chave_resultado = 'execucao_'+pagina
    if st.button('Executar', type='primary'):
        resultados = validar(entrada) if pagina in ('Início','Validador completo') else {('AP' if pagina=='Simulador AP' else 'ALL'): executar(entrada, 'AP' if pagina=='Simulador AP' else 'ALL')}
        st.session_state[chave_resultado] = (entrada, resultados)
        for modulo in resultados:
            st.session_state[f'indice_{pagina}_{modulo}'] = 0
    if chave_resultado in st.session_state:
        executada, resultados = st.session_state[chave_resultado]
        if executada != entrada:
            st.warning('A entrada foi editada. Os resultados abaixo pertencem à última cadeia executada: '+executada)
        for modulo,r in resultados.items():
            mostrar_execucao(modulo, r, executada, f'{pagina}_{modulo}')
    else:
        st.info('Execute a cadeia para visualizar a pilha, a fita e o estado em cada passo.')
        mostrar_diagrama('AP' if pagina != 'Simulador ALL' else 'ALL', chave=pagina+'_inicial')
