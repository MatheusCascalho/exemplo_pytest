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


