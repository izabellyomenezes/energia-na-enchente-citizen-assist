# Testes com usuários

Fizemos os testes presencialmente entre 16 e 19/11/2026, com 5 pessoas: familiares e colegas de trabalho. Cada pessoa usou o assistente (`python assistente.py`) sozinha, digitando as perguntas do seu jeito, enquanto nós cronometrávamos o tempo até ela encontrar a resposta. No final, cada uma deu uma nota de 1 a 5 para a clareza da resposta e comentou o que mudaria. Não anotamos nome, CPF nem endereço, só P1 a P5.

## Perfis

| Participante | Perfil |
|---|---|
| P1 | 67 anos, quase não usa computador, digita devagar e sem acento |
| P2 | 19 anos, estudante, usa muito o celular e escreve abreviado |
| P3 | 35 anos, técnica de enfermagem, usa computador no trabalho |
| P4 | 58 anos, eletricista aposentado, usa pouco o computador |
| P5 | 28 anos, trabalha com computador e prefere usar o menu |

## Situações

| # | Situação lida para a pessoa | Resposta esperada |
|---|---|---|
| 1 | A água está subindo na sua rua. O que você faz com a luz da casa? | Desligar o disjuntor antes da água entrar; se já alagou, não tocar e chamar o 193 |
| 2 | Pode deixar o gerador ligado na garagem para não molhar? | Não, por causa do monóxido de carbono; deixar ao ar livre |
| 3 | Sua mãe usa aparelho de oxigênio e a luz pode acabar. O que você faz? | Cilindro de reserva, avisar a distribuidora, gerador fora de casa, 192 se piorar |
| 4 | Um vizinho disse que painel solar resolve a falta de luz. É verdade? | Só com bateria, e mesmo assim depende do sol; o mais seguro é o híbrido |
| 5 | O que desligar para o gerador durar mais? | TV e chuveiro; nunca ligar o chuveiro no gerador |

Cada pessoa fez 2 situações, então cada situação foi testada 2 vezes.

## Resultados

| Participante | Situação | Como procurou (o que digitou) | Achou a resposta certa? | Tempo (s) | Nota (1 a 5) | Comentário |
|---|---|---|---|---|---|---|
| P1 | 1 | Pergunta livre: "a agua ta subindo oque eu faço com a luz" | Sim | 75 | 4 | Demorou para achar a opção 7 no menu. Achou o texto um pouco longo. |
| P1 | 2 | Pergunta livre: "posso deixar o gerador na garagem pra nao molhar" | Sim | 50 | 5 | Disse que não sabia do risco do monóxido. |
| P2 | 3 | Pergunta livre: "minha mae usa aquele aparelho de oxigenio e vai faltar luz e agr" | Sim | 25 | 5 | Gostou de ter os telefones de emergência na resposta. |
| P2 | 4 | Pergunta livre: "placa solar resolve msm?" | Sim | 20 | 4 | Achou interessante o dado de que maio teve menos sol. |
| P3 | 5 | Pergunta livre: "o que eu desligo pro gerador durar mais" | Sim | 35 | 4 | Queria que a lista dissesse direto "desligue a TV e o chuveiro". |
| P3 | 1 | Pergunta livre: "tem que desligar a energia quando enche?" | Não | 60 | 2 | O assistente mostrou o consumo dos aparelhos em vez da segurança. Depois ela achou pela opção 1 do menu. |
| P4 | 2 | Pergunta livre: "gerador dentro de casa da problema?" | Sim | 40 | 5 | Concordou com a orientação de nunca ligar o gerador na tomada. |
| P4 | 3 | Pergunta livre: "aparelho de respirar sem luz o que fazer" | Sim | 45 | 4 | Não sabia que dava para avisar a distribuidora. |
| P5 | 4 | Menu, opção 4 | Sim | 15 | 5 | Foi direto pela opção do menu. |
| P5 | 5 | Pergunta livre: "quais aparelhos desligo para o gerador aguentar mais tempo" | Sim | 20 | 4 | Achou boa a tabela de consumo. |

No final perguntamos o que cada pessoa mudaria. Duas perguntas extras não foram bem respondidas:

- P1 perguntou "quando a luz volta?" e o assistente mostrou a segurança elétrica, que não responde isso.
- P5 perguntou "quanto custa?" e o assistente respondeu "Não sei".

## Ajustes que fizemos

| Problema encontrado | Ajuste feito no `assistente.py` |
|---|---|
| "tem que desligar a energia quando enche?" ia para o consumo, por causa da palavra "desligar" (P3) | Frases como "desligar a energia", "desligar a luz" e "quadro de luz" agora vão primeiro para a segurança elétrica |
| "quando a luz volta?" não era respondido (P1) | Criamos uma resposta nova explicando que só a distribuidora sabe a previsão e indicando onde consultar |
| "quanto custa?" dava "Não sei" (P5) | As palavras "custa", "preço" e "caro" agora levam para a comparação, que mostra os custos |
| Aproveitamos e testamos "bateria", que também dava "Não sei" | "bateria" agora leva para a parte de energia solar |

Depois dos ajustes rodamos todas as perguntas de novo e todas foram para a resposta certa.

## Conclusão

Nos 10 testes, o assistente acertou 9 (90%). A nota média de clareza foi 4,2. As pessoas conseguiram usar a pergunta livre mesmo escrevendo sem acento e abreviado. O que mais confundiu foi uma palavra com dois sentidos ("desligar" para economizar ou para se proteger), e isso foi corrigido. Duas sugestões ficaram para depois: deixar as respostas mais curtas para quem não está acostumado a ler na tela e colocar no começo da resposta a frase mais importante.
