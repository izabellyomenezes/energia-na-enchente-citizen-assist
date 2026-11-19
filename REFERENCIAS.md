# Referências

Antes de entregar, precisamos conferir cada valor, porque preços e tarifas mudam com o tempo e a região. Também vamos anotar a data em que consultamos cada fonte.

Os valores marcados como "estimado" não foram medidos por nós.

| Valor usado | Onde é usado | Fonte | Tipo |
|---|---|---|---|
| Radiação global horária, Porto Alegre (A801), 2024 | Seções 2 e 4 | INMET, Banco de dados históricos: <https://portal.inmet.gov.br/dadoshistoricos> | real |
| Gasolina: R$ 6,30/L | Seção 3 | ANP, Levantamento de Preços de Combustíveis (média RS): <https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos> | conferir |
| CO2: 1,62 kg por litro de gasolina C | Seção 3 | IPCC 2006 Guidelines, vol. 2, cap. 3 (Mobile Combustion): <https://www.ipcc-nggip.iges.or.jp/public/2006gl/vol2.html> e MCTI, fatores de emissão / Inventário Nacional: <https://www.gov.br/mcti/pt-br> | conferir |
| Horas de sol pleno, rendimento de cerca de 0,75 | Seção 4 | CRESESB/CEPEL, Manual de Engenharia para Sistemas Fotovoltaicos e SunData: <https://cresesb.cepel.br/> | referência |
| Tarifa: R$ 0,95/kWh | Seções 5 e assistente | ANEEL, tarifas residenciais por distribuidora: <https://www.gov.br/aneel/pt-br> | conferir |
| Sistema sem bateria desliga quando a rede cai; cadastro de equipamento essencial à vida | Seção 4 e assistente | ANEEL, Resolução Normativa nº 1.000/2021: <https://www2.aneel.gov.br/cedoc/ren20211000.html> | referência |
| Regras de geração distribuída | Limitações | Lei 14.300/2022: <https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14300.htm> | referência |
| Geladeira com cerca de 28 kWh/mês; TV, chuveiro, lâmpadas | `aparelhos.csv` | Inmetro (Programa Brasileiro de Etiquetagem): <https://www.gov.br/inmetro/pt-br/assuntos/avaliacao-da-conformidade/programa-brasileiro-de-etiquetagem> e Procel: <http://www.procelinfo.com.br> | estimado |
| Concentrador de oxigênio: 320 W | `aparelhos.csv` | Manuais de concentradores domésticos de 5 L/min (faixa típica de 300 a 350 W) | estimado |
| Consumo do gerador × carga | `gerador_manual.csv` | EXEMPLO: trocar pelo manual de um gerador real | exemplo |
| Preço do gerador, painéis (R$ 4,50/W) e bateria (R$ 2.800/kWh) | Seções 3 a 5 | Pesquisa de preços em lojas | estimado |
| Segurança elétrica e monóxido de carbono | Assistente | Defesa Civil RS: <https://www.defesacivil.rs.gov.br/> e Defesa Civil Nacional: <https://www.gov.br/mdr/pt-br/assuntos/protecao-e-defesa-civil> | referência |
| Telefones de emergência | Assistente | 193 Bombeiros, 199 Defesa Civil, 192 SAMU | oficial |
