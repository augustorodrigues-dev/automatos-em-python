"""Confere cada aplicação de produção, sua posição e a sentença derivada."""
import pytest
from streamlit.testing.v1 import AppTest
from interface.gramatica import PRODUCOES, VARIAVEIS, derivar

@pytest.mark.parametrize('entrada', [
    'A#R#F#L', 'B#RR#G#LL', 'B#R#G#L',
    'ABAB#RRRRRR#GFGF#LLLLLL', 'AABB#RRRRR#GGFF#LLLLLLL',
])
@pytest.mark.parametrize('direcao', ['DEE', 'DED'])
def test_producoes_e_ordem_da_derivacao(entrada, direcao):
    atual = 'S'
    for passo in derivar(entrada, direcao):
        assert passo.antes == atual
        indices = [i for i,s in enumerate(atual) if s in VARIAVEIS]
        assert passo.posicao == (indices[0] if direcao == 'DEE' else indices[-1])
        assert passo.variavel == atual[passo.posicao]
        assert passo.producao in PRODUCOES[passo.variavel]
        assert passo.depois == atual[:passo.posicao]+passo.producao+atual[passo.posicao+1:]
        atual = passo.depois
    assert atual == entrada
    assert not any(s in VARIAVEIS for s in atual)


def test_dee_e_ded_expandem_variaveis_distintas():
    entrada = 'ABAB#RRRRRR#GFGF#LLLLLL'
    dee = derivar(entrada, 'DEE')
    ded = derivar(entrada, 'DED')
    assert [p.depois for p in dee[:4]] == ['C#E', 'ACF#E', 'ABCGF#E', 'ABACFGF#E']
    assert [p.depois for p in ded[:4]] == ['C#E', 'C#LE', 'C#LLE', 'C#LLLE']
    assert dee[-1].depois == ded[-1].depois == entrada


def test_alfabeto_visivel_e_derivacoes_na_interface():
    app = AppTest.from_file('app.py').run()
    assert not app.exception
    assert any('Σ = {A, B, R, F, G, L, #}' in bloco.value for bloco in app.sidebar.code)
    assert any('G = (V, T, P, S)' in bloco.value for bloco in app.code)
    next(b for b in app.button if b.label == 'Executar').click().run()
    assert not app.exception
    assert any(t.label == 'DEE — à esquerda' for t in app.tabs)
    assert any(t.label == 'DED — à direita' for t in app.tabs)
    assert any('⇒ C#LE' in bloco.value for bloco in app.code)
