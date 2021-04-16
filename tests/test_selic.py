"""
objetivo do exemplo: mostrar parametrização
Testes de cálculo do imposto de renda a pagar com tesouro selic
Regra: atendimento da tabela regressiva. Aliquota aplicada sobre o lucro

-------------------------------
período (dias) | alíquota (%)
-------------------------------
      180      |  22.5
-------------------------------
    181-360    |  20
-------------------------------
    361-720    |  17.5
-------------------------------
     720+      |  15
-------------------------------


Entradas:
    - valor aplicado (em reais)
    - Período (em dias)
    - Rentabilidade (em % a.m.)
    - Calculo nos periodos fracionados (pro_rata_die ou não aplicado)
Saídas:
    - valor total
    - imposto a pagar (em reais)
    - lucro bruto (em reais)
    - lucro liquido (em reais)
"""
from investimentos.calculadora import *
from investimentos.investimentos import Selic, Carteira
import pytest
from datetime import datetime


# testes tradicionais
def test_selic_valor_total():
    # arrange
    valor_aplicado = 100
    periodo = 30
    rentabilidade = 0.2

    expected = 100.2

    # act
    result = total_com_juros(
        valor_aplicado=valor_aplicado,
        periodo=periodo,
        rentabilidade=rentabilidade
    )

    # assert
    assert result == expected


def test_selic_imposto_a_pagar_30_dias():
    # arrange
    valor_aplicado = 100
    periodo = 30
    rentabilidade = 0.2

    expected = 0.05  # 0.2 * 0.225

    # act
    result = imposto_a_pagar(
        valor_aplicado=valor_aplicado,
        periodo=periodo,
        rentabilidade=rentabilidade
    )

    # assert
    assert result == expected


def test_selic_imposto_a_pagar_181_dias():
    # arrange
    valor_aplicado = 100
    periodo = 181
    rentabilidade = 0.2

    expected = 0.24  # 1.21 * 0.2

    # act
    result = imposto_a_pagar(
        valor_aplicado=valor_aplicado,
        periodo=periodo,
        rentabilidade=rentabilidade
    )

    # assert
    assert result == expected


def test_selic_imposto_a_pagar_365_dias():
    # arrange
    valor_aplicado = 100
    periodo = 365
    rentabilidade = 0.2

    expected = 0.43  # 2.43 * 0.175

    # act
    result = imposto_a_pagar(
        valor_aplicado=valor_aplicado,
        periodo=periodo,
        rentabilidade=rentabilidade
    )

    # assert
    assert result == expected


def test_selic_imposto_a_pagar_730_dias():
    # arrange
    valor_aplicado = 100
    periodo = 730
    rentabilidade = 0.2

    expected = 0.75  # 4.91 * 0.15

    # act
    result = imposto_a_pagar(
        valor_aplicado=valor_aplicado,
        periodo=periodo,
        rentabilidade=rentabilidade
    )

    # assert
    assert result == expected


# Mark.Parametrize

@pytest.mark.parametrize(("valor_aplicado,periodo,rentabilidade,esperado"), [(100, 30, 0.2, 0.05),
                                                                             (100, 181, 0.2, 0.24),
                                                                             (100, 365, 0.2, 0.43),
                                                                             (100, 730, 0.2, 0.75)])
def test_selic_imposto_a_pagar(valor_aplicado, periodo, rentabilidade, esperado):
    # act
    result = imposto_a_pagar(
        valor_aplicado=valor_aplicado,
        periodo=periodo,
        rentabilidade=rentabilidade
    )

    # assert
    assert result == esperado


@pytest.mark.parametrize(("periodo,esperado"), [(30, 0.05),
                                                (181, 0.24),
                                                (365, 0.43),
                                                (730, 0.75)])
def test_selic_imposto_a_pagar(periodo, esperado):
    # arrange
    selic = Selic(valor_inicial=100, rentabilidade=0.2)

    # act
    result = selic.imposto_a_pagar(
        periodo=periodo
    )

    # assert
    assert result == esperado


def test_imposto_medio():
    # arrange
    carteira = Carteira(saldo=5000)
    dias = [
        datetime(2020, 12, 1),  # 30 dias
        datetime(2020, 7, 4),  # 181 dias
        datetime(2020, 1, 2),  # 365 dias
        datetime(2019, 1, 2)  # 730 dias
    ]
    for dia in dias:
        selic = Selic(valor_inicial=100, rentabilidade=0.2)
        carteira.novo_investimento(investimento=selic, data=dia)

    esperado = (0.05 + 0.24 + 0.43 + 0.75) / 4

    result = carteira.imposto_medio(data=datetime(2021, 1, 1))

    assert result == esperado


# fixtures
@pytest.fixture
def carteira_cheia():
    carteira = Carteira(saldo=5000)
    dias = [
        datetime(2020, 12, 1),  # 30 dias
        datetime(2020, 7, 4),  # 181 dias
        datetime(2020, 1, 2),  # 365 dias
        datetime(2019, 1, 2)  # 730 dias
    ]
    for dia in dias:
        selic = Selic(valor_inicial=100, rentabilidade=0.2)
        carteira.novo_investimento(investimento=selic, data=dia)
    return carteira


def test_imposto_medio_com_fixture(carteira_cheia):
    esperado = (0.05 + 0.24 + 0.43 + 0.75) / 4

    result = carteira_cheia.imposto_medio(data=datetime(2021, 1, 1))

    assert result == esperado


# raises
def test_novo_investimento_com_carteira_vazia():
    carteira = Carteira()
    investimento = Selic(valor_inicial=100, rentabilidade=0.5)
    with pytest.raises(Exception) as exc:
        carteira.novo_investimento(investimento, data=datetime(2021, 1, 1))
    assert "Não há saldo suficiente" == str(exc.value)