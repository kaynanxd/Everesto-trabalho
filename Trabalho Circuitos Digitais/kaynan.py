def avaliar_porta(tipo, entradas):
    #avalia as operacoes e retorna o valor correto do calculo
    operacoes = {
        'and': all(entradas),
        'nand': not all(entradas),
        'or': any(entradas),
        'nor': not any(entradas),
        'not': not entradas[0],
        'xor': sum(entradas) % 2 == 1,
        'nxor': sum(entradas) % 2 == 0
    }
    return int(operacoes.get(tipo, 0)) # Retorna 0 se o tipo não for encontrado

def ler_arquivo_circuito(nome_arquivo):
    #Ler o arquivo do circuito e armazena nas variaveis
    circuito = {}
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:          
            chave, valor = linha.split(':', 1)
            chave, valor = chave.strip(), valor.strip()
            # Converte listas de string para listas reais
            if valor.startswith('[') and valor.endswith(']'):
                valor = [item.strip().strip("'").strip('"') for item in valor[1:-1].split(',')]
            circuito[chave] = valor
    return circuito

def avaliar_circuito(circuito, entradas_usuario):
    #Calcula o resultado das portas
    resultados = {entrada: valor for entrada, valor in zip(circuito['entradas'], entradas_usuario)}
    for porta in circuito['gates']:
        tipo, *entradas = circuito[porta]
        valores = [resultados[entrada] for entrada in entradas]
        resultados[porta] = avaliar_porta(tipo.lower(), valores)
    return resultados[circuito['gates'][-1]]

def principal():
    #Executa o programa e por ultimo escreve a tabela verdade
    try:
        #Ler o circuito do arquivo
        nome_arquivo_circuito = 'C1.txt' ################################################
        circuito = ler_arquivo_circuito(nome_arquivo_circuito)
        
        #Tabela verdade: gera todas as combinações possiveis com as variaveis de entrada
        tabela_verdade = []
        num_entradas = len(circuito['entradas'])
        for i in range(2 ** num_entradas):
            entradas = [(i >> j) & 1 for j in range(num_entradas - 1, -1, -1)]
            saida = avaliar_circuito(circuito, entradas)
            tabela_verdade.append(entradas + [saida])
        
        # Escreve a tabela verdade em um arquivo
        with open('R1.txt', 'w') as saida:   ################################################
            saida.write(f'{nome_arquivo_circuito} - Entradas e Saida\n')
            saida.write(' '.join(circuito['entradas'] + circuito['saidas']).upper() + '\n')
            for linha in tabela_verdade:
                saida.write(' '.join(map(str, linha)) + '\n')
        print("Arquivo em txt com tabela verdade gerado com sucesso!")
    except Exception as erro:
        print(f"Erro: {erro}")

#executa a funcao principal#
if __name__ == "__main__":
    principal()

"""Para ler os outros TXT é só trocar o numero 1 de 'C1.txt' na linha 42, 
recomendo trocar também o nome do arquivo de saída 'R1.txt' na linha 53, para não ser salvo por cima do outro resultado. """


