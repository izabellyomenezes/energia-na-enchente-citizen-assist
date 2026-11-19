# Citizen Assist AI - Energia na enchente
# Assistente de terminal com menu. Os números vêm do resultados/resultados.json,
# que o notebook analise_energia.ipynb cria. O assistente não pede nome, CPF nem endereço.

import json
import os

# caminho do resultados.json a partir da pasta deste arquivo,
# para funcionar mesmo rodando de outra pasta (ex.: python gs2/assistente.py)
PASTA_DO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_RESULTADOS = os.path.join(PASTA_DO_SCRIPT, "resultados", "resultados.json")
AVISO = "São estimativas, não garantias. Não é um canal oficial."
EMERGENCIA = "Em emergência: 193 Bombeiros / 199 Defesa Civil / 192 SAMU"


# funções de apoio

def carregar_resultados():
    # abre o arquivo do notebook; se ele não existir, avisa e devolve None
    try:
        with open(ARQUIVO_RESULTADOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        print("Não encontrei", ARQUIVO_RESULTADOS)
        print("Rode primeiro o notebook analise_energia.ipynb (até o final).")
        return None


def mostrar_fontes(fontes):
    # toda resposta termina com as fontes e o aviso
    print()
    print("Fontes:")
    for fonte in fontes:
        print("  -", fonte)
    print("Aviso:", AVISO)
    print()


def ler_numero(pergunta):
    # pede um número até a pessoa digitar um valor válido (aceita 1,5 ou 1.5)
    while True:
        texto = input(pergunta)
        texto = texto.replace(",", ".")
        try:
            numero = float(texto)
            if numero < 0:
                print("Digite um número positivo.")
            else:
                return numero
        except ValueError:
            print("Isso não é um número. Exemplo: 100 ou 1,5")


def buscar_aparelho(r, nome):
    # procura um aparelho pelo nome na lista salva pelo notebook
    for item in r["consumo"]["aparelhos"]:
        if item["aparelho"] == nome:
            return item
    return None


def frase_faixa_semanas(s):
    # frase com a pior e a melhor semana da enchente (seção 4b do notebook)
    data = s["pior_semana_inicio"]
    data_br = data[8:10] + "/" + data[5:7]     # "2024-04-27" vira "27/04"
    return (f"Mas em outras semanas da enchente o resultado variou de "
            f"{s['pior_semana_porcento']:.0f}% (semana de {data_br}) a {s['melhor_semana_porcento']:.0f}%.")


def formatar_reais(valor):
    # 1234.5 vira "R$ 1.234,50" (trocamos a vírgula e o ponto de lugar)
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return "R$ " + texto


# respostas do menu

def seguranca_eletrica(r):
    print("\n=== 1. Segurança elétrica na enchente ===")
    print("- ANTES de a água entrar: DESLIGUE o disjuntor geral (no quadro de luz).")
    print("- Se a casa JÁ ALAGOU: NÃO toque no quadro, em tomadas nem em aparelhos.")
    print("  Saia da água e chame os Bombeiros (193).")
    print("- Fio caído na rua: fique longe e avise a distribuidora de energia.")
    print("- Depois que a água baixar: religue SÓ depois de um eletricista revisar.")
    print("  Aparelhos que molharam precisam ser revisados antes de usar.")
    mostrar_fontes(["Defesa Civil (orientações para enchentes)",
                    "ANEEL e distribuidoras de energia (segurança com a rede elétrica)"])


def consumo_aparelhos(r):
    print("\n=== 2. Quanto meus aparelhos gastam (por dia) ===")
    for item in r["consumo"]["aparelhos"]:
        if item["essencial"] == "sim":
            marca = "ESSENCIAL"
        else:
            marca = "pode desligar"
        print(f"- {item['aparelho']}: {item['kwh_dia']:.2f} kWh/dia ({marca}, {item['tipo_dado']})")
    print()
    print(f"Tudo ligado:          {r['consumo']['total_kwh_dia']:.2f} kWh/dia")
    print(f"Só os essenciais:     {r['consumo']['essencial_kwh_dia']:.2f} kWh/dia")
    print(f"Economia desligando TV e chuveiro: {r['consumo']['economia_porcento']:.0f}%")
    print(f"O concentrador de oxigênio é o que mais gasta entre os essenciais.")
    mostrar_fontes(["Etiquetas Inmetro / selo Procel e manuais de aparelhos (valores estimados)",
                    "Cálculo: kWh = potência (W) x horas x quantidade / 1000"])


def gerador(r):
    g = r["gerador"]
    d = r["demanda"]
    dias = r["dias_sem_luz"]
    print("\n=== 3. Gerador: quanto gasta e como usar com segurança ===")
    print(f"Para manter só os essenciais por {dias} dias, um gerador de {d['potencia_gerador_kw']} kW gasta:")
    print(f"  - {g['litros_7_dias']:.1f} litros de gasolina")
    print(f"  - {formatar_reais(g['custo_7_dias'])}")
    print(f"  - {g['co2_kg_7_dias']:.1f} kg de CO2")
    print(f"(equação do manual: L/h = {g['equacao_a']:.3f} x carga + {g['equacao_b']:.3f})")
    print()
    # compara a demanda da casa com a potência do gerador
    if d["sem_chuveiro_kw"] <= d["potencia_gerador_kw"]:
        print(f"Demanda dos aparelhos SEM chuveiro: {d['sem_chuveiro_kw']:.2f} kW -> o gerador aguenta.")
    else:
        print(f"Demanda dos aparelhos SEM chuveiro: {d['sem_chuveiro_kw']:.2f} kW -> sobrecarga, "
              f"ligue um aparelho de cada vez.")

    if d["com_chuveiro_kw"] > d["potencia_gerador_kw"]:
        print(f"Demanda COM chuveiro: {d['com_chuveiro_kw']:.2f} kW -> sobrecarga. NUNCA ligue o chuveiro no gerador.")
    print()
    print("SEGURANÇA:")
    print("- NUNCA use o gerador dentro de casa, na garagem ou perto de janelas.")
    print("  Ele solta MONÓXIDO DE CARBONO, um gás sem cheiro que pode matar.")
    print("- Deixe-o ao ar livre, protegido da chuva e longe da água.")
    print("- Desligue e espere esfriar antes de colocar gasolina.")
    print("- Não ligue o gerador na tomada da casa: use extensões direto nos aparelhos.")
    mostrar_fontes(["Manual do gerador (dados de EXEMPLO neste projeto)",
                    "ANP (preço da gasolina)", "IPCC/MCTI (fator de CO2)",
                    "Defesa Civil (riscos de monóxido de carbono)"])


def solar(r):
    i = r["inmet"]
    s = r["solar"]
    print("\n=== 4. Energia solar funciona na enchente? ===")
    print("Depende. Um sistema solar COMUM (sem bateria) DESLIGA quando a luz da rua cai.")
    print("Isso é uma proteção obrigatória. Para ter energia na falta de luz, precisa de BATERIA.")
    print()
    print("O que os dados reais do INMET (Porto Alegre, 2024) mostraram:")
    print(f"  - Sol médio no ano:  {i['hsp_media_ano']:.2f} horas de sol pleno por dia")
    print(f"  - Sol médio em maio: {i['hsp_media_maio']:.2f} horas ({i['diferenca_maio_porcento']:+.0f}% em relação ao ano)")
    print()
    print(f"Simulação de {r['dias_sem_luz']} dias com {s['numero_paineis']} painéis ({s['kwp_instalado']} kWp) "
          f"e bateria de {s['bateria_kwh']} kWh:")
    for dia in s["simulacao"]:
        print(f"  {dia['dia']}: sol {dia['hsp']:.2f} h | gerou {dia['geracao_kwh']:.2f} kWh | "
              f"bateria {dia['bateria_fim_do_dia_kwh']:.2f} kWh | faltou {dia['faltou_kwh']:.2f} kWh")
    print(f"Resultado: atendeu {s['atendida_porcento']:.0f}% da necessidade.")
    print(frase_faixa_semanas(s))
    mostrar_fontes(["INMET - estação A801 Porto Alegre, dados horários de 2024",
                    "CRESESB (método de horas de sol pleno)",
                    "ANEEL Resolução 1.000/2021 (desligamento de geração quando a rede cai)"])


def comparar(r):
    g = r["gerador"]
    s = r["solar"]
    print("\n=== 5. Comparação das alternativas ===")
    print(f"Mesma necessidade (aparelhos essenciais) e mesmo período ({r['dias_sem_luz']} dias sem luz).")
    print()
    print(f"{'':22}{'Gerador':>16}{'Solar + bateria':>18}")
    print(f"{'Investimento':22}{formatar_reais(g['investimento']):>16}{formatar_reais(s['investimento']):>18}")
    print(f"{'Custo em 7 dias':22}{formatar_reais(g['custo_7_dias']):>16}{formatar_reais(0):>18}")
    print(f"{'Gasolina (L)':22}{g['litros_7_dias']:>16.1f}{0:>18.1f}")
    print(f"{'CO2 (kg)':22}{g['co2_kg_7_dias']:>16.1f}{0:>18.1f}")
    print(f"{'Atendeu (%)':22}{g['atendida_porcento']:>16.0f}{s['atendida_porcento']:>18.0f}")
    print()
    print("Observações:")
    print("- O gerador só atende 100% se houver gasolina (na enchente, postos fecharam).")
    print(f"- O solar economiza cerca de {formatar_reais(s['economia_anual'])} por ano na conta de luz")
    print(f"  e se paga em cerca de {s['anos_para_se_pagar']:.0f} anos.")
    inicio = s["simulacao"][0]["dia"]          # 1º dia da semana principal, ex.: "2024-05-04"
    print(f"- Na semana de {inicio[8:10]}/{inicio[5:7]} o solar atendeu {s['atendida_porcento']:.0f}%. "
          + frase_faixa_semanas(s))
    print()
    print("RECOMENDAÇÃO:")
    print(r["recomendacao"])
    mostrar_fontes(["Notebook analise_energia.ipynb (cálculos deste projeto)",
                    "INMET, ANP, ANEEL, IPCC/MCTI, CRESESB (ver REFERENCIAS.md)",
                    "Preços de painel, bateria e gerador: estimados"])


def calcular_aparelho(r):
    print("\n=== 6. Calcular um aparelho meu ===")
    print("(veja a potência em watts na etiqueta do aparelho)")
    potencia = ler_numero("Potência do aparelho (W): ")
    horas = ler_numero("Horas ligado por dia: ")
    while horas > 24:
        print("Um dia só tem 24 horas.")
        horas = ler_numero("Horas ligado por dia: ")

    kwh_dia = potencia * horas / 1000
    tarifa = r["premissas"]["tarifa_kwh"]
    print()
    print(f"Consumo: {kwh_dia:.2f} kWh por dia | {kwh_dia * 30:.1f} kWh por mês")
    print(f"Custo na conta de luz: cerca de {formatar_reais(kwh_dia * 30 * tarifa)} por mês")

    limite_w = r["demanda"]["potencia_gerador_kw"] * 1000
    if potencia > limite_w:
        print(f"Esse aparelho ({potencia:.0f} W) é mais forte que o gerador ({limite_w:.0f} W). Não ligue no gerador.")
    elif potencia > 1000:
        print("Aparelho forte: no gerador ou na bateria, use só se for realmente necessário.")
    mostrar_fontes(["Cálculo: kWh = potência (W) x horas / 1000",
                    f"Tarifa de R$ {tarifa:.2f}/kWh (ANEEL - conferir a da sua distribuidora)"])


def pergunta_livre(r):
    print("\n=== 7. Pergunta livre ===")
    print("Não digite nome, CPF ou endereço.")
    pergunta = input("Sua pergunta: ").lower()

    # a ordem importa: o primeiro teste que combinar é o que responde.
    # "deslig" vem antes de "gerador", e as palavras gerais (água, enchente, luz)
    # ficam por último para não pegar perguntas sobre outros assuntos.
    # Os testes mostraram que "desligar a energia quando enche" ia para o consumo
    # dos aparelhos, por isso essas frases de segurança vêm primeiro.
    if ("disjuntor" in pergunta or "choque" in pergunta or "alag" in pergunta
            or "tomada" in pergunta or "fio" in pergunta or "quadro de luz" in pergunta
            or "desligar a energia" in pergunta or "desligar a luz" in pergunta
            or "desliga a energia" in pergunta or "desliga a luz" in pergunta):
        seguranca_eletrica(r)
    elif "volta" in pergunta and ("luz" in pergunta or "energia" in pergunta):
        luz_volta(r)
    elif "oxig" in pergunta or "respir" in pergunta:
        oxigenio(r)
    elif "insulina" in pergunta or "geladeira" in pergunta:
        insulina(r)
    elif "deslig" in pergunta or "economizar" in pergunta or "chuveiro" in pergunta:
        consumo_aparelhos(r)
    elif "gerador" in pergunta or "gasolina" in pergunta:
        gerador(r)
    elif ("solar" in pergunta or "painel" in pergunta or "placa" in pergunta
            or "bateria" in pergunta):
        solar(r)
    elif ("melhor" in pergunta or "comparar" in pergunta or "recomend" in pergunta
            or "custa" in pergunta or "preço" in pergunta or "preco" in pergunta
            or "caro" in pergunta):
        comparar(r)
    elif "água" in pergunta or "agua" in pergunta or "enchente" in pergunta or "luz" in pergunta:
        seguranca_eletrica(r)
    else:
        print("Não sei. Em emergência: 193 Bombeiros / 199 Defesa Civil")
        mostrar_fontes(["Corpo de Bombeiros e Defesa Civil"])


def luz_volta(r):
    # pergunta que apareceu nos testes: o assistente não tem como saber isso
    print("\n=== Quando a luz volta? ===")
    print("- Não temos como saber quando a energia vai voltar na sua rua.")
    print("- Consulte a distribuidora de energia pelo site, aplicativo ou telefone.")
    print("  Ela informa a previsão de religamento da sua região.")
    print("- Enquanto isso, siga as orientações de segurança (opção 1 do menu).")
    mostrar_fontes(["Distribuidora de energia da sua região",
                    "ANEEL Resolução 1.000/2021 (direitos do consumidor)"])


def oxigenio(r):
    concentrador = buscar_aparelho(r, "concentrador de oxigênio")
    print("\n=== Pessoa que usa concentrador de oxigênio ===")
    print(f"- O concentrador gasta cerca de {concentrador['kwh_dia']:.2f} kWh por dia (ligado 24 h).")
    print("- Tenha SEMPRE um cilindro de oxigênio de reserva (fale com o fornecedor ou o serviço de saúde).")
    print("- Avise a distribuidora que na casa há equipamento essencial à vida (cadastro previsto")
    print("  na Resolução ANEEL 1.000/2021). Isso ajuda na prioridade, mas não garante luz.")
    print("- Se for usar gerador: SEMPRE fora de casa (monóxido de carbono).")
    print("- Se faltar oxigênio e a pessoa piorar: ligue 192 (SAMU) ou 193 (Bombeiros).")
    mostrar_fontes(["ANEEL Resolução 1.000/2021", "Manual do concentrador (potência estimada)",
                    "Defesa Civil / SAMU"])


def insulina(r):
    print("\n=== Insulina e geladeira sem luz ===")
    print("- Abra a geladeira o mínimo possível: assim ela fica fria por mais tempo.")
    geladeira = buscar_aparelho(r, "geladeira")
    print(f"- A geladeira gasta pouco (cerca de {geladeira['kwh_dia']:.2f} kWh/dia),")
    print("  então vale a pena mantê-la no gerador ou na bateria.")
    print("- Siga a bula da insulina sobre temperatura e tempo fora da geladeira.")
    print("- Em dúvida, procure um posto de saúde ou farmácia.")
    mostrar_fontes(["Bula do medicamento", "Selo Procel (consumo da geladeira, estimado)"])


# programa principal

resultados = carregar_resultados()

if resultados is not None:
    print("=" * 55)
    print(" Citizen Assist AI - Energia na enchente")
    print(" " + AVISO)
    print(" " + EMERGENCIA)
    print("=" * 55)

    opcao = ""
    while opcao != "0":
        print("1 - Segurança elétrica na enchente")
        print("2 - Quanto meus aparelhos gastam")
        print("3 - Gerador: quanto gasta e como usar com segurança")
        print("4 - Energia solar funciona na enchente?")
        print("5 - Comparar as alternativas e ver a recomendação")
        print("6 - Calcular um aparelho meu")
        print("7 - Pergunta livre")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            seguranca_eletrica(resultados)
        elif opcao == "2":
            consumo_aparelhos(resultados)
        elif opcao == "3":
            gerador(resultados)
        elif opcao == "4":
            solar(resultados)
        elif opcao == "5":
            comparar(resultados)
        elif opcao == "6":
            calcular_aparelho(resultados)
        elif opcao == "7":
            pergunta_livre(resultados)
        elif opcao == "0":
            print("Até logo. Cuide-se! " + EMERGENCIA)
        else:
            print("Opção inválida. Digite um número de 0 a 7.\n")
