from .transicoes_ap import TRANSICOES as AP
from .transicoes_all import TRANSICOES as ALL
ALFABETO = frozenset('ABRFGL#')
def executar(entrada, modulo):
    for i,s in enumerate(entrada):
        if s not in ALFABETO:
            return {'resultado':'ERRO_ALFABETO','motivo':f'Símbolo {s!r}: índice {i}, posição {i+1}', 'passos':[]}
    estado='q0'; i=0; pilha='Z'; fita=list('⊢'+entrada+'⊣'); cabeca=1; logs=[]
    def registrar():
        logs.append({'passo':len(logs),'estado':estado,'posição':i if modulo=='AP' else cabeca,'pilha':pilha if modulo=='AP' else '', 'fita':''.join(fita) if modulo=='ALL' else '', 'restante':entrada[i:] if modulo=='AP' else ''})
    registrar()
    if modulo=='AP':
        while i<len(entrada):
            regra=AP.get((estado,entrada[i],pilha[0]))
            if regra is None:break
            estado,sub=regra; pilha=sub+pilha[1:]; i+=1; registrar()
        aceita=i==len(entrada) and estado=='q7'
    else:
        while estado not in ('q25','q26'):
            lido=fita[cabeca]
            novo,escrito,mov=ALL.get((estado,lido),('q26',lido,'S'))
            if cabeca in (0,len(fita)-1):
                if escrito!=lido:raise RuntimeError('Borda alterada')
            else:fita[cabeca]=escrito
            cabeca += {'L':-1,'R':1,'S':0}[mov]
            if not 0<=cabeca<len(fita):raise RuntimeError('Cabeçote fora da fita')
            estado=novo; registrar()
        aceita=estado=='q25'
    return {'resultado':'ACEITA' if aceita else 'REJEITA','motivo':'Estado final e entrada consumida' if aceita else 'Ausência de transição AP ou transição de rejeição ALL','passos':logs}
def validar(entrada):
    ap=executar(entrada,'AP')
    return {'AP':ap,'ALL':executar(entrada,'ALL') if ap['resultado']=='ACEITA' else {'resultado':'NAO_EXECUTADO','passos':[]}}
