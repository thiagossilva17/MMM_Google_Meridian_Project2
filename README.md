# TCC — Marketing Mix Modeling com Google Meridian

## Comece por um único notebook

**[Abrir a EDA completa](notebooks/01_EDA_COMPLETA.ipynb)**

Toda a etapa exploratória está nesse arquivo: explicação didática, código integral, resultados históricos, figuras, revisão dos alertas e conclusões. O notebook pode ser lido sem executar e não importa módulos de `src` nem depende de outros notebooks. Para recalcular, execute de cima para baixo em ambiente Python 3.12+ / Colab CPU novo, com internet para instalar a versão fixada do Meridian e obter os dados, caso ainda não estejam locais.

[**Guia didático original**](docs/EDA_DIDACTIC_GUIDE.md) — cópia integral, sem alterações de conteúdo. Seus links para os antigos notebooks são históricos; o ponto de entrada deste projeto é o notebook único acima.

> **Estado desta entrega:** consolidação publicada neste repositório. Notebook e resultados históricos preservados; limites de validação descritos abaixo.

[**Abrir no Google Colab**](https://colab.research.google.com/github/thiagossilva17/MMM_Google_Meridian_Project2/blob/main/notebooks/01_EDA_COMPLETA.ipynb)

## O que está concluído

A EDA analisa uma base **simulada** oficial com 40 geos × 156 semanas, cinco canais pagos, mídia orgânica, controles e Promo. Preserva as análises e conclusões da versão `ef39d0a7629e849d31582cea6cefccb581f7a445` do [repositório original](https://github.com/thiagossilva17/MMM_Google_Meridian_Project/tree/ef39d0a7629e849d31582cea6cefccb581f7a445).

Há variação geo-temporal adicional potencialmente informativa, inclusive por habitante. Isso **não demonstra** identificação causal, ganho preditivo, ROI ou contribuição incremental. Os seis REVIEW oficiais e suas decisões foram mantidos. Não houve estimação posterior.

O notebook incorpora as **79 figuras** e as tabelas/sínteses exibidas no master original. Tabelas extensas têm visualização amostral e resumos; todos os CSVs completos permanecem preservados. Códigos auxiliares, documentos e resultados estão organizados como suporte: não é necessário navegar por eles para acompanhar a investigação.

## Como as pastas se relacionam

| Caminho | Função | Preciso abrir para estudar a EDA? |
|---|---|---|
| `notebooks/01_EDA_COMPLETA.ipynb` | Única entrada: história, código, evidência e conclusão | **Sim, comece aqui** |
| `data/raw/` | Base original imutável | Não |
| `data/processed/` | Painel preparado, sem alterar os dados brutos | Não |
| `data/metadata/` | Origem, licença e registros de preservação/validação | Para auditoria |
| `src/` | Códigos originais para rastreabilidade e adaptação de infraestrutura do notebook | Não; todo o código usado está no notebook |
| `outputs/figures/` | Figuras vetoriais para o TCC | Apenas para exportar |
| `outputs/tables/` | Tabelas completas, inclusive as muito extensas | Apenas para consultar todas as linhas |
| `outputs/reports/` | Relatórios históricos e HTML interativo oficial | Complementar |
| `outputs/logs/`, `outputs/audit/` | Evidências históricas da execução e auditoria | Para auditoria |
| `outputs/models/` | Local reservado para modelos futuros; ainda vazio | Não |
| `docs/` | Guia, decisões, achados, metodologia e histórico | Complementar |

As subdivisões de figuras e os nomes das tabelas foram mantidos para não quebrar as referências das evidências existentes. A compactação principal é a **entrada única de leitura e execução**, em vez de apagar resultados auditáveis.

`src/` preserva o código de origem para comparação; os antigos scripts de execução e testes estão em `docs/EDA_SUPORTE_ORIGINAL.zip`. A forma suportada de executar esta entrega é o notebook consolidado. Não use o antigo gerador para reconstruir os notebooks separados. O guia original mantém referências históricas aos notebooks antigos, que continuam no repositório de origem.

## Etapas do TCC

| Etapa | Estado |
|---|---|
| Preparação, entendimento dos dados e EDA temporal/geográfica/mídia | Consolidados no notebook único |
| Desenho causal, especificação e priors | A fazer |
| Baseline Meridian | A fazer |
| Diagnósticos de convergência | A fazer |
| Ajuste e avaliação preditiva | A fazer |
| Análise da posterior | A fazer |
| ROI e contribuição | A fazer |
| Curvas de resposta | A fazer |
| Heterogeneidade geográfica do modelo | A fazer |
| Holdout e comparação nacional × geo | A fazer |
| Sensibilidade | A fazer |
| Otimização de orçamento | A fazer |

A definição do holdout e dos critérios de comparação deverá ocorrer **antes** de ajustar os modelos; a ordem desta lista não autoriza olhar a validação somente no final. Não foram criados notebooks vazios para etapas ainda não executadas.

## Reprodutibilidade e limites da verificação

- Código e dados oficiais fixados no commit `02111531f8661373aa7b6ba31c316c67d72d1dd2` do Meridian.
- Dados brutos conferidos por SHA-256; nenhuma imputação, winsorização ou remoção de extremos foi introduzida.
- As saídas visíveis no notebook são **históricas preservadas**; a validação da consolidação está em [CONSOLIDACAO_VALIDACAO.md](docs/CONSOLIDACAO_VALIDACAO.md).
- A infraestrutura nova separa seu manifesto de execução do manifesto antigo e verifica mudanças em funções e arquivos antes da síntese.
- A etapa oficial Meridian e a execução em uma sessão real do Google Colab **não foram repetidas nesta consolidação**. Não interpretar saídas salvas como prova de uma execução integral nova.

Os arquivos históricos de validação permanecem com seu conteúdo original. Eles descrevem a versão anterior; o registro de consolidação descreve especificamente esta entrega.
