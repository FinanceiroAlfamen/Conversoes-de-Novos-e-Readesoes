# Conversão de Novos Pacientes e Readesão

Abra `index.html` no navegador. O HTML contém os dados, a logo, a textura da marca, a fonte e os gráficos; funciona também sem internet.

## Duas versões para trabalhar

- `index.html`: relatório atual, com o layout anterior.
- `painel-flutuante-branco.html`: relatório completo com o painel lateral flutuante branco, os filtros e as ferramentas na lateral e as abas de análise acima dos cartões.

Os dois arquivos contêm a mesma base de dados e os mesmos recursos de análise, tooltips, ampliação, cópia e impressão. Cada arquivo pode ser aberto diretamente no navegador e ter seu layout aprimorado separadamente. Ao atualizar os dados, manter as duas versões atualizadas.

## Estrutura

Conversão de Novos e Conversão de Readesão possuem as abas Consultor, Médico, Clínica, Parecer Técnico e Ações Sugeridas. Quantidade Prevista de Readesões possui Visão Geral, Clínica, Evolução Mensal, Parecer Técnico e Ações Sugeridas.

O período é global. Os seletores de clínica são independentes em cada cartão; os gráficos de evolução permitem selecionar várias clínicas ao mesmo tempo e exibem uma leitura mensal por unidade. No acumulado por profissional, ano, mês e clínica ficam agrupados no nome do consultor ou médico e não ocupam colunas próprias. As abas têm atalhos para as seções; gráficos podem ser ampliados; tooltips dos indicadores também podem ser abertos pelo teclado. As tabelas permitem ordenar colunas, localizar registros e exportar uma versão HTML formatada. Os totais continuam considerando todo o filtro mesmo quando a busca reduz as linhas visíveis. Imprimir / Salvar permite escolher todo o documento, o relatório selecionado ou apenas a aba ativa.

## Atualização mensal

1. Mantenha o PDF de 2025 na pasta Base de Dados.
2. Substitua `BADE DE DADOS - 2026.pdf` pelo arquivo com o novo mês fechado, preservando o nome e as cinco páginas do modelo.
3. Execute a extração e a incorporação da base no relatório. A rotina de atualização preserva os dois layouts e recalcula todos os cartões, tabelas, gráficos, comparações e tooltips a partir dos PDFs.

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

Na quantidade prevista de 2026 até outubro: as linhas somam 2.710 no total previsto, 1.095 em Readeriu e 686 em Não compareceu; o rodapé imprime 2.679, 1.093 e 661. Há diferenças por clínica e mês entre a coluna Total e a soma das situações. O HTML preserva a coluna Total e informa as diferenças na revisão da fonte. Em readesão de 2026, as visões de consultores e médicos divergem em um atendimento e um fechamento; as duas visões permanecem separadas e o PDF deve ser conferido para conciliação.

Comparações entre anos utilizam os mesmos meses e clínicas com dados. Pareceres descrevem tendências e prioridades de investigação; não atribuem causas sem evidência operacional. Responsáveis e rotinas nas ações sugeridas são propostas para validação da gestão.

## Identidade visual

Referência: https://financeiroalfamen.github.io/Gestao-de-Novos-pacientes/

