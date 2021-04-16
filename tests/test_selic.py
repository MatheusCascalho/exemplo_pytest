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
