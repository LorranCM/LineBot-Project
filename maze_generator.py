import random

def gerar_labirinto(largura, altura):
  """
  Gera um array bidimensional que representa um labirinto simples.

  Args:
    largura: A largura do labirinto (número de colunas).
    altura: A altura do labirinto (número de linhas).

  Returns:
    Uma lista de listas (array bidimensional) onde 1 representa uma parede e 0 um caminho.
  """
  # Inicializa o labirinto com paredes (1)
  labirinto = [[1 for _ in range(largura)] for _ in range(altura)]

  # Define um ponto inicial para a "escavação" do caminho
  x_inicial, y_inicial = 1, 1
  caminho = [(y_inicial, x_inicial)]
  labirinto[y_inicial][x_inicial] = 0

  while caminho:
    # Pega o ponto atual
    y_atual, x_atual = caminho[-1]

    # Encontra os vizinhos não visitados
    vizinhos = []
    # Cima
    if y_atual > 1 and labirinto[y_atual - 2][x_atual] == 1:
      vizinhos.append((y_atual - 2, x_atual))
    # Baixo
    if y_atual < altura - 2 and labirinto[y_atual + 2][x_atual] == 1:
      vizinhos.append((y_atual + 2, x_atual))
    # Esquerda
    if x_atual > 1 and labirinto[y_atual][x_atual - 2] == 1:
      vizinhos.append((y_atual, x_atual - 2))
    # Direita
    if x_atual < largura - 2 and labirinto[y_atual][x_atual + 2] == 1:
      vizinhos.append((y_atual, x_atual + 2))

    if vizinhos:
      # Escolhe um vizinho aleatoriamente
      y_novo, x_novo = random.choice(vizinhos)
      
      # "Escava" o caminho entre os dois pontos
      labirinto[y_novo][x_novo] = 0
      labirinto[y_atual + (y_novo - y_atual) // 2][x_atual + (x_novo - x_atual) // 2] = 0

      # Adiciona o novo ponto ao caminho para continuar a "escavação"
      caminho.append((y_novo, x_novo))
    else:
      # Se não houver vizinhos, volta para o ponto anterior (backtracking)
      caminho.pop()

  return labirinto

# Exemplo de uso
largura_labirinto = 15
altura_labirinto = 30

meu_labirinto = gerar_labirinto(largura_labirinto, altura_labirinto)

# Imprime a lista de listas (o array bidimensional)
for linha in meu_labirinto:
  print(linha)