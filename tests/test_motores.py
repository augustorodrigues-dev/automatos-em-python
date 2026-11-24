import json
from pathlib import Path
import pytest
from automatos.validador import executar
from automatos.transicoes_ap import TRANSICOES as AP
from automatos.transicoes_all import TRANSICOES as ALL
@pytest.mark.parametrize('modulo,entrada,esperado',json.loads(Path('dados/exemplos.json').read_text()))
def test_casos(modulo,entrada,esperado):
    assert executar(entrada,modulo)['resultado']==esperado
def test_tabelas():
    assert len(AP)==21 and len(ALL)==133
def test_demonstracao():
    r=executar('ABAB#RRRRRR#GFGF#LLLLLL','ALL')
    assert len(r['passos'])==381
