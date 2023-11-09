# Projeto de Correção de Texto em Python

## Descrição
Este projeto implementa uma aplicação simples em Python para correção de texto usando programação concorrente. Ele inclui a leitura de um arquivo CSV, criação de threads para correção paralela, e aplicação de correções específicas usando a classe `Correcter`.

## Requisitos
- Python 3.x
- Bibliotecas: pandas, tqdm


## Uso
1. Coloque seus textos no arquivo CSV `teste.csv`.
2. Execute o script Python: `python gramatical.py`

## Configuração
- A classe `Correcter` pode ser personalizada com lógica de correção específica. Atualmente, ela substitui abreviações comuns.
- A estratégia de desativação da barra de progresso pode ser ajustada no método `get_disable_strategy` no script.

