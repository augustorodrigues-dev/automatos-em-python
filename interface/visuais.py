"""Observadores visuais: nunca participam da decisão dos motores."""
import json
from collections import defaultdict
from html import escape

from automatos.transicoes_ap import TRANSICOES as AP
from automatos.transicoes_all import TRANSICOES as ALL

FASES = {
    'Formato': tuple(f'q{i}' for i in range(8)),
    'Retorno e seleção': ('q8', 'q9'),
    'Correspondência dos fechamentos': tuple(f'q{i}' for i in range(10, 18)),
    'Consumo das cotas': tuple(f'q{i}' for i in range(18, 24)),
    'Verificação final': ('q24', 'q25', 'q26'),
}

def fase_do_estado(estado):
    return next(nome for nome, estados in FASES.items() if estado in estados)

def cotar(texto):
    return json.dumps(str(texto), ensure_ascii=False)

def diagrama(modulo, ativo=None, fase=None, direcao="TB", fonte=22, mostrar_padrao=False):
    """DOT derivado das tabelas; agrupa apenas arestas de mesma origem/destino."""
    fontes = set(FASES[fase]) if modulo == 'ALL' and fase else None
    arestas = defaultdict(list)
    finais = {'q7'} if modulo == 'AP' else {'q25', 'q26'}
    tabela = AP if modulo == 'AP' else ALL
    for chave, regra in tabela.items():
        origem, simbolo = chave[:2]
        if fontes is not None and origem not in fontes:
            continue
        destino = regra[0]
        if modulo == 'AP':
            rotulo = f'{simbolo}, {chave[2]} → {regra[1] or "ε"}'
        else:
            rotulo = f'{simbolo} → {regra[1]}, {regra[2]}'
        arestas[origem, destino].append(rotulo)
    if modulo == 'ALL' and mostrar_padrao:
        for i in range(25):
            origem = f'q{i}'
            if fontes is not None and origem not in fontes:
                continue
            ausentes = [s for s in 'ABRFGL#abrfgl⊢⊣' if (origem, s) not in ALL]
            if ausentes:
                arestas[origem, 'q26'].append('padrão: ' + ','.join(ausentes) + ' / mantém, S')
    estados = {x for par in arestas for x in par}
    estados.update(fontes or (f'q{i}' for i in range(8 if modulo == 'AP' else 27)))
    linhas = ['digraph {', f'rankdir={direcao};', 'bgcolor="#0f172a";',
              'graph [nodesep=0.18, ranksep=0.3, pad=0.15];',
              f'node [style=filled, fillcolor="#e2e8f0", fontcolor="#0f172a", fontname="Arial", fontsize={fonte}, margin=0.12];',
              f'edge [color="#cbd5e1", fontcolor="#e2e8f0", fontname="Arial", fontsize={fonte}, arrowsize=0.8];']
    if 'q0' in estados:
        linhas.extend(['inicio [shape=point];', 'inicio -> q0;'])
    for q in sorted(estados, key=lambda x: int(x[1:])):
        cor = '#fbbf24' if q == ativo else '#fca5a5' if q == 'q26' else '#86efac' if q in finais else '#e2e8f0'
        linhas.append(f'{q} [shape={"doublecircle" if q in finais else "circle"}, fillcolor="{cor}", label={cotar(q + (" • atual" if q == ativo else ""))}];')
    for (origem, destino), rotulos in arestas.items():
        padrao = destino == 'q26' and modulo == 'ALL'
        linhas.append(f'{origem} -> {destino} [label={cotar(chr(10).join(rotulos))}, style={"dashed" if padrao else "solid"}];')
    return '\n'.join(linhas + ['}'])

def arvore_derivacao(entrada, fonte=24):
    """Derivação da GLC para uma entrada JÁ aceita pelo AP, apenas para exibição."""
    aberturas, reservas, fechamentos, liberacoes = entrada.split('#')
    linhas = ['digraph {', 'bgcolor="#0f172a";', 'ordering=out;', 'graph [nodesep=0.12, ranksep=0.25, pad=0.15];',
              f'node [style=filled, fillcolor="#dbeafe", fontcolor="#0f172a", fontname="Arial", fontsize={fonte}, margin=0.1];',
              'edge [color="#94a3b8"];']
    folhas = []
    numero = 0
    def no(rotulo, pai=None, terminal=False):
        nonlocal numero
        nome = f'n{numero}'; numero += 1
        linhas.append(f'{nome} [label={cotar(rotulo)}, shape={"box" if terminal else "ellipse"}];')
        if pai is not None:
            linhas.append(f'{pai} -> {nome};')
        return nome
    def terminal(s, pai):
        return no(s, pai, True)
    raiz = no('S'); c = no('C', raiz)
    separador_final = terminal('#', raiz); e = no('E', raiz)
    fechamentos_pendentes = []
    for i, simbolo in enumerate(aberturas):
        folhas.append(terminal(simbolo, c))
        if i == len(aberturas) - 1:
            folhas.append(terminal('#', c)); d = no('D', c)
            separador_reserva = terminal('#', c)
            fechamento = terminal('F' if simbolo == 'A' else 'G', c)
        else:
            proximo = no('C', c)
            fechamento = terminal('F' if simbolo == 'A' else 'G', c)
            c = proximo
        fechamentos_pendentes.append(fechamento)
    for i in range(len(reservas)):
        folhas.append(terminal('R', d))
        if i < len(reservas)-1:
            d = no('D', d)
    folhas.extend([separador_reserva, *reversed(fechamentos_pendentes), separador_final])
    for i in range(len(liberacoes)):
        folhas.append(terminal('L', e))
        if i < len(liberacoes)-1:
            e = no('E', e)
    linhas.append('{ rank=same; ' + '; '.join(folhas) + '; }')
    linhas.append(' -> '.join(folhas) + ' [style=invis, weight=10];')
    return '\n'.join(linhas + ['}'])

def pilha_html(pilha):
    celulas = ''.join(f'<div style="border:2px solid {"#fbbf24" if i==0 else "#64748b"};padding:12px;background:#1e293b;color:white">{escape(s)} {"← topo" if i==0 else "← fundo" if s=="Z" else ""}</div>' for i,s in enumerate(pilha))
    return '<div style="max-height:420px;overflow:auto;width:150px;text-align:center">'+celulas+'</div>'

def fita_html(fita, cabeca):
    celulas = []
    for i,s in enumerate(fita):
        cor = '#fbbf24' if i == cabeca else '#86efac' if s in 'abrfgl' else '#94a3b8' if s in '⊢⊣' else '#dbeafe'
        celulas.append(f'<div style="min-width:48px;text-align:center"><div style="color:#94a3b8">{i}</div><div style="background:{cor};color:#0f172a;border:2px solid #475569;padding:10px">{escape(s)}</div><div style="color:#fbbf24">{"▲ cabeça" if i==cabeca else "&nbsp;"}</div></div>')
    return '<div style="display:flex;overflow-x:auto;padding:12px 0">'+''.join(celulas)+'</div>'
