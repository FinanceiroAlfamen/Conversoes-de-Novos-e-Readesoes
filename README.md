# Conversão de Novos Pacientes e Readesão

Abra `index.html` no navegador. O HTML contém os dados, a logo, a textura da marca, a fonte e os gráficos; funciona também sem internet.

## Relatório online

[Abrir o painel publicado](https://financeiroalfamen.github.io/Conversoes-de-Novos-e-Readesoes/)

Esta publicação corresponde à versão atual de `index.html`. O arquivo inclui dados e recursos visuais para uso online ou offline.

## Estrutura

Conversão de Novos e Conversão de Readesão possuem as abas Consultor, Médico, Clínica, Parecer Técnico e Ações Sugeridas. Quantidade Prevista de Readesões possui Visão Geral, Clínica, Evolução Mensal, Parecer Técnico e Ações Sugeridas.

O período é global. Os seletores de clínica são independentes em cada cartão; os gráficos de evolução permitem selecionar várias clínicas ao mesmo tempo e exibem uma leitura mensal por unidade. No acumulado por profissional, ano, mês e clínica ficam agrupados no nome do consultor ou médico e não ocupam colunas próprias. As abas têm atalhos para as seções; gráficos podem ser ampliados; tooltips dos indicadores também podem ser abertos pelo teclado. As tabelas permitem ordenar colunas, localizar registros e exportar uma versão HTML formatada. Os totais continuam considerando todo o filtro mesmo quando a busca reduz as linhas visíveis. Imprimir / Salvar permite escolher todo o documento, o relatório selecionado ou apenas a aba ativa.

## Atualização mensal

1. Mantenha o PDF de 2025 na pasta Base de Dados.
2. Substitua `BADE DE DADOS - 2026.pdf` pelo arquivo com o novo mês fechado, preservando o nome e as cinco páginas do modelo.
3. Peça a atualização do relatório nesta conversa. A extração e o HTML serão reconstruídos a partir dos PDFs.

As ferramentas de atualização ficam em `scripts/extrair_bases.py` e `scripts/montar_relatorio.py`. A base consolidada fica em `dados/bases.json`. Os elementos da identidade visual estão em `assets/marca.json`, para preservar a logo, a textura e a fonte sem depender de acesso à internet na atualização. Os dados do relatório de referência não entram neste projeto.

## Regras de cálculo

Os acumulados somam as linhas mensais disponíveis, sem deduplicar pacientes entre meses. Os PDFs não contêm identificadores individuais que permitam essa deduplicação. As datas inicial e final selecionam os meses abrangidos; não há rateio por dia.

- Aproveitamento: fechamentos / atendidos.
- Não convertidos (%): não convertidos / atendidos.
- Atendimentos para fechar um: atendidos / fechamentos.
- Valor médio por tratamento: valor total / tratamentos.
- Conversão por tratamento: tratamentos / atendidos. Informação interna, mantida na tabela.
- Aproveitamento geral de readesões previstas: readeriu / total previsto.
- Aproveitamento entre elegíveis: readeriu / (total previsto − liberado / alta / desmame).
- Aproveitamento entre decisões: readeriu / (readeriu + não readeriu).

As taxas acumuladas usam os totais como numerador e denominador, sem média simples dos percentuais. Denominadores vazios ou iguais a zero aparecem como N/D. Células vazias de quantidade no PDF representam ausência de evento e são acumuladas como zero; as células originais permanecem na base consolidada.

Consultores e médicos são visões separadas dos atendimentos. A aba Clínica usa médicos como referência, pois a tabela de consultores de novos de dezembro/2025 está cortada. Os registros “Verificar Consultor” e “Verificar Médico” permanecem identificados como aparecem na fonte.

## Conferência da fonte

Há diferenças entre alguns totais gerais impressos nos PDFs e a soma das linhas mensais. As quantidades exibidas neste HTML vêm das linhas disponíveis e podem diferir dos totais do Power BI. A janela Gerenciar contém a seção Revisão dos dados, com busca por arquivo, página, mês, clínica e profissional, além de filtros por ano e clínica. As divergências de totais, a cobertura incompleta e os cadastros pendentes ficam centralizados nessa revisão, sem avisos nas abas analíticas. Diferenças entre totais gerais sem detalhamento não são atribuídas a uma clínica. Quantidades fracionárias de tratamentos são preservadas como aparecem na fonte e não são consideradas erros apenas por serem fracionárias.

Em novos de 2025, consultores: linhas disponíveis somam 6.620 atendimentos e 2.978 fechamentos; o PDF imprime 6.671 e 3.000. A página termina nas linhas de dezembro antes de exibir todos os consultores. Os valores ausentes não foram estimados.

Na quantidade prevista de 2026: as linhas somam 2.455 no total previsto, 995 em Readeriu e 626 em Não compareceu; o rodapé imprime 2.429, 993 e 606. Algumas linhas também possuem situações cuja soma difere da coluna Total. O HTML preserva essa coluna e informa a diferença.

Comparações entre anos utilizam os mesmos meses e clínicas com dados. Pareceres descrevem tendências e prioridades de investigação; não atribuem causas sem evidência operacional. Responsáveis e rotinas nas ações sugeridas são propostas para validação da gestão.

## Identidade visual

Referência: https://financeiroalfamen.github.io/Gestao-de-Novos-pacientes/

Porto Alegre: verde. Belo Horizonte: azul. Campinas: azul escuro. Curitiba: laranja.

O cabeçalho usa a mesma logo, textura e fonte da referência, com bordas arredondadas, linha laranja e efeito ao passar o mouse. O relatório inclui modo noturno, botão de voltar ao topo, tabelas com cores suaves por coluna e impressão em A4 paisagem.

## Resumo mensal das situações

O cartão Situações por mês inclui quantidades e percentuais de cada situação nos tooltips. O denominador é o total previsto registrado para o mês e para as clínicas selecionadas, sem substituir esse total pela soma das situações.


O resumo de situações apresenta somente a média dos totais mensais no período e nas clínicas filtradas; meses sem registros não são preenchidos com zero.

## Leitura gerencial e acompanhamento

Análise técnica: leitura executiva, comparação anual pelos mesmos pares clínica/mês, evolução mensal, equilíbrio entre conversão e valor e acompanhamento profissional com destaques de resultados e pontos de atenção, sem classificar qualidade pessoal. A comparação individual anual mantém também a identidade da pessoa. A triagem de 100 atendimentos e 3 meses é uma regra operacional, não garantia estatística; as comparações não ajustam perfil clínico ou registros repetidos.

Plano de ação: evidência, hipótese, ação, meta proposta, acompanhamento, responsável sugerido e prazo relativo ao início aprovado pela gestão. Cenários recuperam a própria referência anual quando aplicável ou mostram um piloto hipotético de 2 p.p.; não prometem resultados ou receita. Grupos abaixo da triagem ficam exploratórios.

Consultores e médicos não são somados. A revisão compara suas quantidades por clínica e mês, sem presumir qual visão está correta. Em Porto Alegre, janeiro/2026, readesão, as páginas 3 e 4 divergem em um atendimento e um fechamento. Conferir os PDFs de origem.

Dados adicionais propostos (ainda não disponíveis): motivos, propostas recusadas, descontos, datas do processo, origem, tipo de tratamento, capacidade, custos, recebimentos, cancelamentos e experiência. O arquivo continua sem configuração de senha ou acesso restrito.

## Legibilidade da análise técnica

As tabelas separam atendimentos, fechamentos, taxa atual e taxa anterior. A variação identifica os anos e o indicador comparado. Vermelho representa sinal negativo (redução) e verde, positivo (aumento), independentemente de o indicador ser desejável; reduzir perdas pode ser uma melhoria. O comparativo geral usa eixo central, esquerda para redução e direita para aumento.

A comparação financeira usa apenas valor médio do tratamento e valor total vendido, com suas variações anuais. O acompanhamento individual tem uma linha resumida e explicações expansíveis por pessoa, com valores de ambos os anos, contexto dos demais profissionais da mesma clínica e passos de revisão. Os destaques exigem a triagem descrita acima. Na impressão, as explicações individuais são abertas para incluir o conteúdo completo.

## Filtros sincronizados da análise técnica

O filtro à direita do título Análise técnica controla todos os cartões, com uma seleção por área: clínica (todas ou uma), consultor ou médico (uma pessoa, identificada também pela clínica). Ao mudar para uma categoria profissional, a lista aparece e exige escolher uma pessoa. As opções respeitam o período superior e são ordenadas alfabeticamente. A leitura executiva, os valores vendidos e o acompanhamento individual usam o mesmo recorte. Na previsão há somente seleção de clínica, pois a fonte não atribui profissionais.

A comparação individual mantém pessoa, clínica e meses também na referência anterior; não compara uma pessoa com o total anterior da clínica. Contexto dos pares e de outras clínicas usa a mesma categoria e meses do profissional selecionado. Os detalhes identificam, mês a mês, quedas e melhoras com valores de ambos os anos, além de comparar valor médio e total vendido. O cartão redundante de conversão por clínica foi removido. Números nos textos explicativos recebem destaque em negrito, inclusive na impressão.

O seletor da análise usa lista personalizada com nomes em caixa alta e pontos coloridos pela clínica. As categorias ficam na ordem CLÍNICAS, CONSULTORES, MÉDICOS, com ícones verde, azul e roxo. A lista possui bordas arredondadas, animação suave, seleção única e suporte a Tab, setas, Home, End e Escape; a preferência de movimento reduzido é respeitada.
