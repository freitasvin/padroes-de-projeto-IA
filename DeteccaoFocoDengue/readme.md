# Detecção de Foco de Dengue

Renan Soares, Emanuel Soares, Tiago de Lima e Cleverton Marcelo

O projeto utiliza aprendizado de máquina, especificamente regressão de floresta aleatória (Random Forest), para prever o número total de casos de dengue com base em diversos atributos.

Leitura dos Dados:
    O código começa importando bibliotecas e lendo dois conjuntos de dados: dengue_features_train.csv e dengue_labels_train.csv.

Pré-processamento dos Dados:
    São realizadas várias etapas de pré-processamento nos dados:
    Preenchimento de valores ausentes utilizando a média.
    Conversão do nome da cidade (San Juan e Iquitos) para valores numéricos (0 e 1).
    Extração de informações de ano, mês e data a partir da coluna week_start_date.
    Remoção da coluna week_start_date e adição da coluna total_cases do conjunto de rótulos ao conjunto de recursos.

Salvamento dos Dados Limpos:
    Utilizando o padrão de projeto Observer, os dados limpos são salvos em um arquivo chamado Dengue_Hotspot_Data.csv. Esse padrão permite notificar outros componentes do sistema quando os dados são salvos, sem acoplamento direto.

Treinamento do Modelo:
    Os dados são divididos em conjuntos de treinamento e teste.
    Os recursos são escalonados usando StandardScaler.
    Um modelo de regressão de floresta aleatória (RandomForestRegressor) é treinado usando validação cruzada e busca em grade para ajustar os hiperparâmetros.

Escolha do Modelo (Strategy Pattern):
    O padrão de projeto Strategy é aplicado para encapsular a escolha do modelo. Isso permite facilmente alterar o modelo de regressão no futuro sem modificar o código principal.

Avaliação do Modelo:
    O modelo treinado é avaliado usando o conjunto de teste.
    O erro quadrático médio (MSE) é calculado para avaliar o desempenho do modelo.
    Uma dispersão de pontos (scatter plot) é gerada para visualizar as predições em relação aos valores reais.

## Refatorações:

    Separar o Código em Funções:
    Funções para as diferentes etapas do código, como leitura de dados, pré-processamento, treinamento do modelo e avaliação do modelo.

    Utilizar Constantes para Caminhos dos Arquivos:
    Constantes para facilitar a manutenção e reusabilidade, substituindo os caminhos dos arquivos.

    Melhorar o Tratamento de Valores Ausentes:
    Métodos mais robustos para tratar valores ausentes, como o SimpleImputer do scikit-learn.

    Encapsular o Processo de Escalonamento:
    Função para lidar com o escalonamento dos dados.

    Organizar Importações:
    Importações de bibliotecas no início do código.

## Padrões de Projeto:

    Padrão de Projeto Observer (para salvar dados):
    Permite que diferentes partes do código possam ser notificadas quando os dados forem salvos. Isso pode ser útil se, no futuro, for adicionado a funcionalidade de notificação.

    Padrão de Projeto Strategy (para escolher o modelo):
    Permite encapsular os diferentes algoritmos de regressão, permitindo que seja facilmente alterado o modelo utilizado no futuro, sem modificar o código principal.