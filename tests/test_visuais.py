"""Verificações da derivação exibida e da navegação pelos estados reais."""
import json
import re
import pytest
from streamlit.testing.v1 import AppTest
from interface.visuais import arvore_derivacao, diagrama, FASES
from automatos.transicoes_ap import TRANSICOES as AP
from automatos.transicoes_all import TRANSICOES as ALL

@pytest.mark.parametrize('entrada', ['A#R#F#L','B#RR#G#LL','ABAB#RRRRRR#GFGF#LLLLLL'])
def test_folhas_da_arvore(entrada):
    dot=arvore_derivacao(entrada)
    labels={n:json.loads(label) for n,label in re.findall(r'(n\d+) \[label=(".*?"), shape=box\]',dot)}
    ordem=re.search(r'\{ rank=same; (.*?); \}',dot).group(1).split('; ')
    assert ''.join(labels[n] for n in ordem)==entrada

def test_diagramas_derivados_das_tabelas():
    ap=diagrama('AP','q3')
    assert 'q3 • atual' in ap
    for (origem,simbolo,topo),(destino,sub) in AP.items():
        assert f'{origem} -> {destino}' in ap
        assert f'{simbolo}, {topo} → {sub or "ε"}' in ap
    for fase in FASES:
        dot=diagrama('ALL',fase=fase)
        for (origem,s),(destino,escrito,mov) in ALL.items():
            if origem in FASES[fase]:
                assert f'{origem} -> {destino}' in dot
                assert f'{s} → {escrito}, {mov}' in dot

def clicar(app,label):
    next(b for b in app.button if b.label==label).click().run()
    assert not app.exception

def test_interface_arvore_e_passos():
    app=AppTest.from_file('app.py').run()
    assert not app.exception
    clicar(app,'Executar')
    assert len(app.get('graphviz_chart'))==3
    clicar(app,'Próximo ▶')
    assert app.session_state['indice_Início_AP']==1
    clicar(app,'Fim ⏭')
    assert app.session_state['indice_Início_AP']==23
    assert 'XZ' not in app.session_state['execucao_Início'][1]['AP']['passos'][-1]['pilha']

@pytest.mark.parametrize('pagina',['Simulador AP','Simulador ALL','Modelagem formal'])
def test_paginas_visuais(pagina):
    app=AppTest.from_file('app.py').run()
    app.sidebar.radio[0].set_value(pagina).run()
    assert not app.exception
    if pagina!='Modelagem formal':clicar(app,'Executar')
    assert app.get('graphviz_chart')

def test_trocar_exemplo_e_rejeicao_sem_arvore():
    app=AppTest.from_file('app.py').run()
    app.selectbox[0].set_value('ABAB#RRRRRR#FGFG#LLLLLL').run()
    assert app.text_input[0].value=='ABAB#RRRRRR#FGFG#LLLLLL'
    clicar(app,'Executar')
    assert len(app.get('graphviz_chart'))==1
    assert app.session_state['execucao_Início'][1]['AP']['resultado']=='REJEITA'
