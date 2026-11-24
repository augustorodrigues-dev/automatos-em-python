"""Gramática e derivações didáticas, externas aos motores dos autômatos.

A geração das derivações recebe somente cadeias previamente aceitas pelo AP.
Ela não é um validador e jamais é consultada para aceitar/rejeitar entradas.
"""
from collections import deque
from dataclasses import dataclass

VARIAVEIS = frozenset(('S', 'C', 'D', 'E'))
PRODUCOES = {
    'S': ('C#E',),
    'C': ('ACF', 'BCG', 'A#D#F', 'B#D#G'),
    'D': ('RD', 'R'),
    'E': ('LE', 'L'),
}
GRAMATICA_TEXTO = '''G = (V, T, P, S)

V = {S, C, D, E}
T = Σ = {A, B, R, F, G, L, #}
Símbolo inicial: S

P = {
    S → C#E
    C → ACF | BCG | A#D#F | B#D#G
    D → RD | R
    E → LE | L
}'''

@dataclass(frozen=True)
class PassoDerivacao:
    antes: str
    depois: str
    variavel: str
    producao: str
    posicao: int


def derivar(entrada: str, direcao: str) -> tuple[PassoDerivacao, ...]:
    """Expande uma variável por passo; entrada deve ter sido aceita pelo AP."""
    if direcao not in ('DEE', 'DED'):
        raise ValueError('Direção deve ser DEE ou DED')
    aberturas, reservas, _, liberacoes = entrada.split('#')
    expansoes_c = []
    for i, simbolo in enumerate(aberturas):
        fechamento = 'F' if simbolo == 'A' else 'G'
        expansoes_c.append(simbolo + ('#D#' if i == len(aberturas)-1 else 'C') + fechamento)
    pendentes = {
        'S': deque(['C#E']),
        'C': deque(expansoes_c),
        'D': deque(['RD'] * (len(reservas)-1) + ['R']),
        'E': deque(['LE'] * (len(liberacoes)-1) + ['L']),
    }
    atual = 'S'
    passos = []
    while any(s in VARIAVEIS for s in atual):
        indices = range(len(atual)) if direcao == 'DEE' else range(len(atual)-1, -1, -1)
        posicao = next(i for i in indices if atual[i] in VARIAVEIS)
        variavel = atual[posicao]
        producao = pendentes[variavel].popleft()
        depois = atual[:posicao] + producao + atual[posicao+1:]
        passos.append(PassoDerivacao(atual, depois, variavel, producao, posicao))
        atual = depois
    return tuple(passos)


def texto_derivacao(passos: tuple[PassoDerivacao, ...]) -> str:
    return 'S\n' + '\n'.join(
        f'⇒ {passo.depois}    [{passo.variavel} → {passo.producao}]'
        for passo in passos
    )
