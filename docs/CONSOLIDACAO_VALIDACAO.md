# Consolidação da EDA — 21 de outubro de 2026

## O que foi preservado

Fonte: `thiagossilva17/MMM_Google_Meridian_Project`, commit `ef39d0a7629e849d31582cea6cefccb581f7a445`.

O repositório de origem foi apenas lido. A migração não substitui sua auditoria, suas validações ou sua história. O novo ponto de entrada é `notebooks/01_EDA_COMPLETA.ipynb`, o único notebook desta entrega.

Foram preservados os dados brutos e preparados, os códigos originais de referência, os documentos existentes, 129 tabelas CSV, 79 figuras SVG e os relatórios. O notebook incorpora as 79 figuras em PNG renderizado dos SVGs preservados, além de 14 repetições ilustrativas junto da narrativa para facilitar a leitura. Os SVGs originais não foram alterados. As tabelas exibidas e as conclusões calculadas do master foram mantidas; saídas extensas continuam com amostras e sínteses, enquanto os CSVs guardam todas as linhas.

O arquivo `docs/EDA_DIDACTIC_GUIDE.md` é uma cópia byte a byte. Seus links para os antigos notebooks continuam sendo referências históricas, que existem no repositório original. O novo notebook adapta a narrativa, acrescenta fórmulas e comentários técnicos e aponta suas referências históricas ao commit de origem.

## Alterações exclusivamente organizacionais e de infraestrutura

1. Retirada dos imports relativos entre módulos na versão embutida do notebook. As funções estão definidas no mesmo namespace.
2. Retirada do prefixo `plots.` nas chamadas às funções de desenho, cujas implementações também estão no notebook.
3. Instalação e diretório local independentes de clone: não é necessário baixar código Python externo ao notebook.
4. Preservação do pin do Meridian, da semente e do checksum da base.
5. Manifesto novo `outputs/logs/notebook_run_manifest.json`, separado do histórico. Registra ambiente, dados, configurações, funções carregadas e checksums dos resultados.
6. Exibição de todas as figuras, incluindo heatmaps anteriormente remetidos a apêndices externos.
7. README como mapa do TCC, com as etapas futuras identificadas como não executadas. Nenhum notebook vazio foi criado.

Os scripts de geração/execução e os testes históricos foram guardados em `docs/EDA_SUPORTE_ORIGINAL.zip`. `src/` mantém o código original para rastreabilidade; sua estrutura antiga de execução não é o ponto de entrada deste pacote. Use o notebook consolidado.

## Verificações realizadas nesta consolidação

| Verificação | Resultado |
|---|---|
| Schema do notebook | Válido (`nbformat`) |
| Compilação de todas as células de código | Sem erros de sintaxe |
| Equivalência estrutural de funções | **44 funções**, comparadas por AST após normalizar apenas imports relativos e prefixo de gráficos |
| Preservação dos arquivos de origem presentes na cópia | **293 arquivos byte a byte**; conferidos também contra seus hashes Git |
| Guia didático | Idêntico byte a byte |
| Figuras incorporadas | **79**, uma vez no conjunto de evidências; 14 também aparecem junto da narrativa |
| Reexecução das etapas próprias 00–05 | Todas concluíram |
| Comparação numérica das tabelas recalculadas | **80 tabelas iguais**, `rtol=1e-10`, `atol=1e-9`, sem exigir igualdade de dtype inferido pelo CSV |
| Proveniência: arquivo alterado | Rejeitado corretamente |
| Proveniência: função redefinida | Rejeitada corretamente |
| Nova execução da API oficial Meridian | **Não realizada** |
| Nova execução da função de conclusões | **Não realizada**; função equivalente por AST e resultados históricos preservados |
| Execução integral no serviço Google Colab | **Pendente** |

A reexecução de verificação usou as funções analíticas extraídas das células do notebook em uma pasta temporária separada, sem substituir as saídas históricas da entrega. Os wrappers de proveniência dependentes da instalação completa do Meridian não foram usados nessa reexecução parcial. Os dois testes de invalidação da infraestrutura foram realizados separadamente, com uma impressão digital de ambiente controlada. Portanto, estas verificações **não equivalem a um Run all integral em runtime novo**.

A lista das funções e das tabelas comparadas está em `data/metadata/consolidation_validation.json`. O log desta verificação está em `outputs/logs/consolidation_validation.log`.

## Limites substantivos mantidos

A base é simulada, não descreve uma empresa real e não identifica plataformas ou cidades reais. Há variação geo-temporal adicional potencialmente útil, mas isso não prova identificação causal, melhor previsão, incrementalidade ou retorno de mídia. Os seis REVIEW oficiais continuam preservados, com decisões e limites. Não houve ajuste posterior nem recomendação de orçamento.

As saídas oficiais incorporadas são históricas e vêm do commit de origem. A migração não as apresenta como se tivessem sido recalculadas. Uma futura execução integral deverá manter a origem fixada da API, concluir as etapas 00–07 e registrar seu próprio manifesto. A validação real do Colab permanece um item separado.

## Estado da publicação

A publicação inicialmente bloqueada por HTTP 403 foi retomada em 22 de outubro de 2026 após a liberação do acesso. O pacote foi recuperado e seus 307 checksums conferidos antes da atualização dos registros de publicação. O notebook anexado é idêntico byte a byte ao do pacote; todas as células de código passaram por compilação sintática nesta retomada. Não houve nova execução analítica. O repositório original não foi alterado.
