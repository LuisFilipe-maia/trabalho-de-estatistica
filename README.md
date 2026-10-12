# Analisador Estatístico em Python

## O que é

É um programa de terminal que recebe uma lista de números, digitada na hora ou lida de um arquivo `.csv`, e calcula média, mediana e moda de três jeitos diferentes: com os dados soltos, com uma tabela de frequências e com os dados agrupados em classes. Na última parte ele também calcula quartis, decis e percentis.

Todo o código está no arquivo `trabalho.py`.

## Como rodar

Abra o terminal na pasta onde estão os arquivos e rode:

```
python trabalho.py
```

(no Windows, se `python` não funcionar, tente `py trabalho.py`)

O programa mostra um menu. Escolha `1` para digitar os números separados por vírgula, por exemplo `18,19,19,20,22`, ou `2` para ler um arquivo, por exemplo `dados_exemplo.csv`. Depois é só olhar o resultado das três partes.

Algumas observações sobre os dados:
- Para números decimais use ponto (`2.5`) e não vírgula.
- No `.csv`, se a primeira linha tiver texto, o programa entende que é cabeçalho e ignora.
- Se tiver letra no meio dos números, o arquivo não existir ou estiver vazio, o programa avisa o erro e volta para o menu, sem travar.

## Como o código está organizado

Ficou tudo em um arquivo só, mas separado em funções:

- **Entrada de dados:** `ler_terminal`, `ler_csv` e `converter_texto`, que cuidam de ler e validar o que o usuário passou.
- **Parte 1:** `parte1_calcular` usa só o pacote `statistics` do Python (`mean`, `median` e `mode`) direto nos dados.
- **Parte 2:** as funções que começam com `p2_` montam a tabela de frequências e calculam tudo olhando só para ela.
- **Parte 3:** as funções que começam com `p3_` agrupam os dados em classes e calculam as fórmulas na mão, sem usar nenhuma biblioteca estatística.
- **Tela:** `main` e as funções `mostrar_parte1`, `mostrar_parte2` e `mostrar_parte3` cuidam do menu e de mostrar os resultados.

Como a Parte 3 não pode usar o `statistics`, ele é importado só dentro da função da Parte 1. Assim as outras partes nem enxergam o módulo.

## Parte 2: como funciona

A tabela tem três colunas: o valor (`xi`), quantas vezes ele aparece (`fi`) e a frequência acumulada (`Fi`).

- **Média:** soma de `fi · xi` dividida por `n`.
- **Mediana:** se `n` é ímpar, pegamos o valor da posição `(n+1)/2`. Se é par, fazemos a média dos valores das posições `n/2` e `n/2 + 1`. Para achar cada posição, procuramos a primeira linha em que `Fi` chega nela.
- **Moda:** é o valor com maior `fi`. Se mais de um empatar, o programa mostra o primeiro e avisa que existem outras modas.

## Parte 3: como funciona

Primeiro o programa decide as classes:

- O número de classes vem da fórmula de Sturges: `k = 1 + 3,322 · log10(n)`, arredondado.
- A amplitude de cada classe é `h = (maior − menor) / k`.
- Cada classe é do tipo `[a, b)`, ou seja, inclui o `a` e não inclui o `b`. A última é fechada dos dois lados para o maior valor não ficar de fora.

Depois vêm as medidas:

- **Média:** `Σ(fi · xi) / n`, onde `xi` é o ponto médio de cada classe.
- **Mediana, quartis, decis e percentis:** todos usam a mesma fórmula de interpolação, só muda a fração:

  `valor = li + ((fração · n − F_anterior) / fi) · h`

  Aqui `li` é o limite inferior da classe onde a posição cai, `F_anterior` é a frequência acumulada da classe de trás e `fi` é a frequência da própria classe. A fração é 0,5 para a mediana, 0,25 para Q1, 0,75 para Q3, 0,2 para D2, 0,7 para D7, e 0,15, 0,22, 0,63 e 0,70 para P15, P22, P63 e P70. No código isso é uma função só, `p3_separatriz`.
- **Moda:** o programa mostra duas versões.
  - Czuber: `li + d1 / (d1 + d2) · h`, com `d1 = f − f_anterior` e `d2 = f − f_posterior`.
  - King: `li + f_posterior / (f_anterior + f_posterior) · h`.

  Nas duas, `f` é a frequência da classe com mais dados.
