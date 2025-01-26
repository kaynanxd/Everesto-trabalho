def avaliar_porta(tipo, entradas):
             #avalia as operacoes e retorna o valor
    operacoes = {
        'and': all(entradas),
        'nand': not all(entradas),
        'or': any(entradas),
        'nor': not any(entradas),
        'not': not entradas[0],
        'xor': sum(entradas) % 2 == 1,
        'nxor': sum(entradas) % 2 == 0
    }
    return int(operacoes.get(tipo, 0))

def ler_arquivo_circuito(nome_arquivo):
                # Ler o arquivo do circuito
    circuito = {}
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            chave, valor = linha.split(':', 1)
            chave, valor = chave.strip(), valor.strip()
                          # Converte as strings para listas
            if valor.startswith('[') and valor.endswith(']'):
                valor = [item.strip().strip("'").strip('"') for item in valor[1:-1].split(',')]
            circuito[chave] = valor
    return circuito

def avaliar_circuito(circuito, entradas_usuario):
                         # avalia o circuito a partir das entradas
    resultados = {entrada: valor for entrada, valor in zip(circuito['entradas'], entradas_usuario)}
    pendentes = set(circuito['gates'])  # gates que precisam ser avaliados
    while pendentes:
        resolvidos_antes = len(pendentes)
        for porta in list(pendentes):
            dados_porta = circuito[porta]
                     # Identifica tipo, entradas e saida
            tipo = dados_porta[0].lower()
            possiveis_saidas = [item for item in dados_porta[1:] if item not in resultados]

            if len(possiveis_saidas) != 1:
                continue  # Espera ate que tudo seja resolvido

            saida = possiveis_saidas[0]
            entradas = [item for item in dados_porta[1:] if item != saida]

                       # Verifica se todas as entradas deste gate foram resolvidas
            if all(entrada in resultados for entrada in entradas):
                valores = [resultados[entrada] for entrada in entradas]
                resultados[saida] = avaliar_porta(tipo, valores)
                pendentes.remove(porta)   # Marca este gate como resolvido

           # Verifica se deu erro de looping infinito para encontrar as saidas
        if len(pendentes) == resolvidos_antes:
            raise ValueError("erro de looping ")    
        
             # Retorna o resultado das saídas
    return [resultados[saida] for saida in circuito['saidas']]

def principal():
            # Executa o programa e escreve a tabela verdade
    try:
             # Ler o circuito do arquivo
        nome_arquivo_circuito = input("Digite o nome do arquivo : ").strip()
        circuito = ler_arquivo_circuito(nome_arquivo_circuito)

              # De acordo com as entradas gera as combinacoes para a tabela verdade
        tabela_verdade = []
        num_entradas = len(circuito['entradas'])
        for i in range(2 ** num_entradas):
            entradas = [(i >> j) & 1 for j in range(num_entradas - 1, -1, -1)]
            saidas = avaliar_circuito(circuito, entradas)
            tabela_verdade.append(entradas + saidas)

                     # Escreve a tabela verdade em um arquivo
        nome_arquivo_saida = 'TV ' + nome_arquivo_circuito
        with open(nome_arquivo_saida, 'w') as saida: 
            saida.write(f'{nome_arquivo_circuito} - Entradas e Saidas\n')
            saida.write(' '.join(circuito['entradas'] + circuito['saidas']).upper() + '\n')
            for linha in tabela_verdade:
                saida.write(' '.join(map(str, linha)) + '\n')
        print("Arquivo txt com tabela verdade criado")
                   # Imprime erro caso encontre algum problema
    except Exception as erro:
        print(f"Erro: {erro}")
# Executa o codigo
if __name__ == "__main__":
    principal()
