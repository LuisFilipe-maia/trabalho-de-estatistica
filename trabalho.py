import math
import re

SEPARADORES = re.compile(r"[,;\s]+")
LINHA_DUPLA = "=" * 53
LINHA = "-" * 53


def _eh_numero(token):
    try:
        return math.isfinite(float(token))
    except ValueError:
        return False


def converter_texto(texto, origem="entrada"):
    valores = []
    for n_linha, linha in enumerate(texto.splitlines(), 1):
        for token in SEPARADORES.split(linha.strip()):
            if not token:
                continue
            if not _eh_numero(token):
                raise ValueError(f"valor inválido '{token}' ({origem}, linha {n_linha}).")
            valores.append(float(token))
    if not valores:
        raise ValueError("nenhum valor numérico foi encontrado.")
    return valores


def ler_terminal():
    texto = input("Digite os valores separados por vírgula: ")
    return converter_texto(texto, "terminal")


def ler_csv(caminho):
    try:
        with open(caminho.strip().strip('"'), encoding="utf-8-sig") as f:
            linhas = f.read().splitlines()
    except FileNotFoundError:
        raise ValueError(f"arquivo '{caminho}' não encontrado.")
    except UnicodeDecodeError:
        raise ValueError("o arquivo não está em texto UTF-8 válido.")
    except OSError as e:
        raise ValueError(f"não foi possível abrir o arquivo ({e.strerror}).")

    if len(linhas) > 1:
        tokens = [t for t in SEPARADORES.split(linhas[0].strip()) if t]
        if any(not _eh_numero(t) for t in tokens):
            linhas = linhas[1:]
    return converter_texto("\n".join(linhas), "arquivo")


# PARTE 1
def parte1_calcular(dados):
    import statistics
    return {
        "media": statistics.mean(dados),
        "mediana": statistics.median(dados),
        "moda": statistics.mode(dados),
    }


# PARTE 2
def p2_construir_tabela(dados):
    contagem = {}
    for x in dados:
        contagem[x] = contagem.get(x, 0) + 1
    tabela, acumulada = [], 0
    for xi in sorted(contagem):
        acumulada += contagem[xi]
        tabela.append((xi, contagem[xi], acumulada))
    return tabela


def p2_media(tabela):
    n = tabela[-1][2]
    return sum(fi * xi for xi, fi, _ in tabela) / n


def p2__valor_na_posicao(tabela, pos):
    for xi, _, Fi in tabela:
        if Fi >= pos:
            return xi


def p2_mediana(tabela):
    n = tabela[-1][2]
    if n % 2:
        return p2__valor_na_posicao(tabela, (n + 1) // 2)
    return (p2__valor_na_posicao(tabela, n // 2) + p2__valor_na_posicao(tabela, n // 2 + 1)) / 2


def p2_modas(tabela):
    maior = max(fi for _, fi, _ in tabela)
    return [xi for xi, fi, _ in tabela if fi == maior]


def p2_moda(tabela):
    return p2_modas(tabela)[0]


# PARTE 3
def p3_construir_tabela(dados):
    n = len(dados)
    menor, maior = min(dados), max(dados)
    amplitude_total = maior - menor
    k = max(1, round(1 + 3.322 * math.log10(n)))
    h = amplitude_total / k if amplitude_total > 0 else 1.0
    if amplitude_total == 0:
        k = 1

    limites = [menor + i * h for i in range(k + 1)]
    limites[-1] = max(limites[-1], maior)
    freq = [0] * k
    for x in dados:
        i = 0
        while i < k - 1 and x >= limites[i + 1]:
            i += 1
        freq[i] += 1

    classes, acumulada = [], 0
    for i in range(k):
        acumulada += freq[i]
        classes.append((limites[i], limites[i + 1], freq[i], acumulada))
    return {"n": n, "k": k, "h": h, "classes": classes}


def p3_media(t):
    soma = sum(fi * (li + ls) / 2 for li, ls, fi, _ in t["classes"])
    return soma / t["n"]


def p3_separatriz(t, fracao):
    alvo = fracao * t["n"]
    anterior = 0
    for li, ls, fi, Fi in t["classes"]:
        if Fi >= alvo and fi > 0:
            return li + ((alvo - anterior) / fi) * (ls - li)
        anterior = Fi
    return t["classes"][-1][1]


def p3__classe_modal(t):
    cl = t["classes"]
    i = max(range(len(cl)), key=lambda j: cl[j][2])
    f_ant = cl[i - 1][2] if i > 0 else 0
    f_post = cl[i + 1][2] if i < len(cl) - 1 else 0
    return cl[i], f_ant, f_post


def p3_moda_czuber(t):
    (li, ls, fi, _), f_ant, f_post = p3__classe_modal(t)
    d1, d2 = fi - f_ant, fi - f_post
    if d1 + d2 == 0:
        return (li + ls) / 2
    return li + d1 / (d1 + d2) * (ls - li)


def p3_moda_king(t):
    (li, ls, _, _), f_ant, f_post = p3__classe_modal(t)
    if f_ant + f_post == 0:
        return (li + ls) / 2
    return li + f_post / (f_ant + f_post) * (ls - li)


def fmt(x):
    return str(int(x)) if float(x).is_integer() else f"{x:.2f}"


def cabecalho(titulo):
    print(f"\n{LINHA}\n{titulo}\n{LINHA}")


def mostrar_parte1(dados):
    cabecalho("PARTE 1: DADOS NÃO AGRUPADOS (Módulo Statistics)")
    r = parte1_calcular(dados)
    print(f"Média: {r['media']:.2f}")
    print(f"Mediana: {r['mediana']:.2f}")
    print(f"Moda: {r['moda']:.2f}")


def mostrar_parte2(dados):
    cabecalho("PARTE 2: DISTRIBUIÇÃO DE FREQUÊNCIA (SEM INTERVALO)")
    tabela = p2_construir_tabela(dados)
    print(f"{'Valor (xi)':>12} | {'Freq. Absoluta (fi)':>19} | {'Freq. Acumulada (Fi)':>20}")
    for xi, fi, Fi in tabela:
        print(f"{fmt(xi):>12} | {fi:>19} | {Fi:>20}")
    todas = p2_modas(tabela)
    print(f"Calculados via tabela: Média = {p2_media(tabela):.2f} | "
          f"Mediana = {p2_mediana(tabela):.2f} | Moda = {p2_moda(tabela):.2f}")
    if len(todas) > 1:
        print("Obs.: distribuição multimodal -> modas: " + ", ".join(fmt(m) for m in todas))


def mostrar_parte3(dados):
    cabecalho("PARTE 3: DISTRIBUIÇÃO DE FREQUÊNCIA (COM INTERVALO)")
    t = p3_construir_tabela(dados)
    print(f"n = {t['n']} | classes (Sturges) k = {t['k']} | amplitude h = {t['h']:.2f}\n")
    print(f"{'Classe':<20} | {'fi':>6} | {'Fi':>6}")
    ultima = len(t["classes"]) - 1
    for i, (li, ls, fi, Fi) in enumerate(t["classes"]):
        fecha = "]" if i == ultima else ")"
        print(f"{f'[{li:.2f} - {ls:.2f}{fecha}':<20} | {fi:>6} | {Fi:>6}")

    s = lambda p: p3_separatriz(t, p)
    print("\nCalculados via Fórmulas de Interpolação:")
    print(f"-> Média: {p3_media(t):.2f} | Mediana: {s(0.5):.2f} | "
          f"Moda (Czuber): {p3_moda_czuber(t):.2f} | Moda (King): {p3_moda_king(t):.2f}")
    print(f"-> Quartis: Q1 = {s(0.25):.2f} | Q3 = {s(0.75):.2f}")
    print(f"-> Decis: D2 = {s(0.2):.2f} | D7 = {s(0.7):.2f}")
    print(f"-> Percentis: P15 = {s(0.15):.2f} | P22 = {s(0.22):.2f} | "
          f"P63 = {s(0.63):.2f} | P70 = {s(0.70):.2f}")


def obter_dados():
    while True:
        print("[1] Inserir dados via terminal (separados por vírgula)")
        print("[2] Carregar arquivo .csv")
        print("[0] Sair")
        opcao = input("\nEscolha a opção: ").strip()
        try:
            if opcao == "1":
                return ler_terminal()
            if opcao == "2":
                return ler_csv(input("Caminho do arquivo .csv: "))
            if opcao == "0":
                return None
            print("Opção inválida.\n")
        except ValueError as erro:
            print(f"Erro: {erro}\n")


def main():
    print(f"{LINHA_DUPLA}\n   ANALISADOR ESTATÍSTICO - ENGENHARIA DE SOFTWARE\n{LINHA_DUPLA}")
    dados = obter_dados()
    if dados is None:
        return
    print(f"Dados carregados com sucesso! (n = {len(dados)} elementos)")
    mostrar_parte1(dados)
    mostrar_parte2(dados)
    mostrar_parte3(dados)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrado.")
    try:
        input("\nPressione Enter para sair...")
    except (KeyboardInterrupt, EOFError):
        pass
