import sys

#Essa função converte um número decimal, positivo ou negativo, para binário com uma quantidade determinada de bits
def conversao_binario(numero,bits):
        numero=int(numero)
        #Conversão de números maiores ou iguais a zero
        if numero >=0:
            binario = ""
            while numero > 0:
                binario=str(numero%2)+binario
                numero=numero//2
        #No caso de números negativos, calcula-se o complemento de dois
        else:
            binario = ""
            numero=-numero
            #Conversão para binário
            while numero > 0:
                binario=str(numero%2)+binario
                numero=numero//2

            binario=binario.zfill(bits)
            #Inversão de bits
            b_invertido=""
            for bit in binario:
                if bit=='0':
                    b_invertido+='1'
                else:
                    b_invertido+='0'
            #Adição do carry 1
            binario=bin(int(b_invertido, 2) + 1)[2:]

        return str(binario).zfill(bits)

#Essa função converte um número hexadecimal para decimal
def conversao_hexa(numero):
    numero = numero.upper().replace("0X", "")
    digitos_hex = {'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7,
                   '8':8, '9':9, 'A':10, 'B':11, 'C':12, 'D':13, 'E':14, 'F':15}
    soma=0
    aux=0

    for i in reversed(numero):
        soma+=digitos_hex[i]*16**aux
        aux+=1
    return str(soma)


def tipo_r(instru, rd, rs1, rs2):
    saida = ""
    # Encontra o funct7 da instrução
    if (instru == "add" or instru == "sll" or instru == "xor" or instru == "srl" or instru == "sra" or instru == "or" or instru == "and"):
        funct7 = "0000000"
    elif (instru == "sub"):
        funct7 = "0100000"
    elif (instru == "lr.d"):
        funct7 = "0001000"
    elif (instru == "sc.d"):
        funct7 = "0001100"

    #converte os endereços rs2,rs1,rd para binario com 5 bits
    rd = conversao_binario(rd,5)
    rs2 = conversao_binario(rs2,5)
    rs1 = conversao_binario(rs1,5)

    # Encontra o funct3 da instrução
    if (instru == "add" or instru == "sub"):
        funct3 = "000"
    elif (instru == "sll"):
        funct3 = "001"
    elif (instru == "xor"):
        funct3 = "100"
    elif (instru == "srl" or instru == "sra"):
        funct3 = "101"
    elif (instru == "or"):
        funct3 = "110"
    elif (instru == "and"):
        funct3 = "111"
    elif (instru == "lr.d" or instru == "sc.d"):
        funct3 = "011"

    # Seta o opcode correto para as instruções do tipo R
    opcode = "0110011"

    #concatena as strings de bits para formar umas instrução de 32 bits
    saida = funct7 + rs2 + rs1 + funct3 +  rd +  opcode
    return saida
    

def tipo_s(instru, rs2, imme, rs1):
    #Conversão para binário
    imme = conversao_binario(imme, 12)
    rs1 = conversao_binario(rs1,5)
    rs2 = conversao_binario(rs2,5)
    saida = ""

    # Encontra o funct3 da instrução
    if (instru == "sb"):
        funct3 = "000"
    elif (instru == "sh"):
        funct3 = "001"
    elif (instru == "sw"):
        funct3 = "010"
    elif (instru == "sd"):
        funct3 = "111"

    # Define o opcode do tipo S
    opcode = "0100011"

    #imprime a saida
    saida = imme[:7] + rs2 + rs1 + funct3 + imme[7:]+ opcode
    return saida

def tipo_sb(instru, rs1, rs2, imme):
    # Encontra o funct3 da instrução
    imme = conversao_binario(imme, 12)
    rs1 = conversao_binario(rs1,5)
    rs2 = conversao_binario(rs2,5)

    saida = ""

    if (instru == "beq"):
        funct3 = "000"
    elif (instru == "bne"):
        funct3 = "001"
    elif (instru == "blt"):
        funct3 = "100"
    elif (instru == "bge"):
        funct3 = "101"
    elif (instru == "bltu"):
        funct3 = "110"
    elif (instru == "bgeu"):
        funct3 = "111"

    # Define o opcode do tipo SB
    opcode = "1100111"

    #imprime a saida
    saida = imme[11] + imme[1:7] + rs2 + rs1 + funct3 + imme[7:11] + imme[0] + opcode

    return saida


def tipo_U(instrucao,rd,imediato):
    
    if instrucao=='lui':
        #Define o opcode
        opcode='0110111' 
         #Converte os parâmetros para binário e monta a instrução no formato imediato + rd + opcode
        instrucao_gerada=conversao_binario(imediato,20)+conversao_binario(rd,5)+opcode

    return instrucao_gerada

def tipo_UJ(instrucao,rd,imediato):

    if instrucao=='jal':
        opcode='1101111' #Define o opcode
        
        imediato_shift=int(imediato)>>1 #Desloca um bit para direita
        imediato_bin = conversao_binario(imediato_shift, 20) #Converte o imediato para binário de 20 bits

        #Armazena intervalos de acordo a posição dos bits
        im_20 = imediato_bin[0]      
        im_19_12 = imediato_bin[1:9]    
        im_11 = imediato_bin[9]         
        im_10_1 = imediato_bin[10:19] 

        #Realiza a montagem do imediato segundo o formato: imm[20] imm[10:1] imm[11] imm[19:12]
        imediato_tratado = im_20 + im_10_1 + im_11 + im_19_12

        #Monta a instrução completa no formato imediato + rd + opcode
        instrucao_gerada=imediato_tratado+conversao_binario(rd,5)+opcode

    return instrucao_gerada

def tipo_i(instrucao,rd,rs1,imediato):
    #Definição de parâmetros das instruções tipo I
    instrucoes={

        "lb":{"opcode":"0000011","funct3":"000","funct7": None},
        "lh":{"opcode":"0000011","funct3":"001","funct7": None},
        "lw":{"opcode":"0000011","funct3":"010","funct7": None},
        "ld":{"opcode":"0000011","funct3":"011","funct7": None},
        "lbu":{"opcode":"0000011","funct3":"100","funct7": None},
        "lhu":{"opcode":"0000011","funct3":"101","funct7": None},
        "lwu":{"opcode":"0000011","funct3":"110","funct7": None},
        "addi":{"opcode":"0010011","funct3":"000","funct7": None},
        "slli":{"opcode":"0010011","funct3":"001","funct7": "0000000"},
        "xori":{"opcode":"0010011","funct3":"100","funct7": None},
        "srli":{"opcode":"0010011","funct3":"101","funct7": "0000000"},
        "srai":{"opcode":"0010011","funct3":"101","funct7": "0100000"},
        "ori":{"opcode":"0010011","funct3":"110","funct7": None},
        "andi":{"opcode":"0010011","funct3":"111","funct7": None},
        "jalr":{"opcode":"1100111","funct3":"000","funct7": None},
    }
    #Acessa informações referentes à instrução a ser executada
    dados=instrucoes[instrucao]
    opcode=dados["opcode"]
    funct3=dados["funct3"]
    funct7=dados["funct7"]

    #Realiza a montagem das instruções de acordo com a sua estrutura
    if instrucao in ['addi','xori','ori','andi']: 
        #imediato + rs1 + funct3 + rd + opcode
        instrucao_gerada=conversao_binario(imediato,12)+conversao_binario(rs1,5)+funct3+conversao_binario(rd,5)+opcode


    elif instrucao in ['lw','lh','lb','lbu','ld','lhu','lwu','jalr']:
        #A sintaxe dessas instruções definem que a leitura do imediato vem antes do registrador base, por isso será feita a troca de valores
        rs1, imediato = imediato, rs1
        #imediato + rs1 + funct3 + rd + opcode
        instrucao_gerada=conversao_binario(imediato,12)+conversao_binario(rs1,5)+funct3+conversao_binario(rd,5)+opcode


    elif instrucao in ['srli','slli','srai']:
        #funct7 + shamt + rs1 + funct3 + rd + opcode
        instrucao_gerada=funct7+conversao_binario(imediato,5)+conversao_binario(rs1,5)+funct3+conversao_binario(rd,5)+opcode

    return instrucao_gerada

def tipo_pseudo(instrucao,rd,rs_or_imm):
    #Identifica a pseudo instrução e chama a montagem do seu formato equivalente

    if instrucao=="li": #li equivale a addi,rd,x0,im
        return tipo_i('addi',rd,0,rs_or_imm)
    elif instrucao=="mv": #mv equivale a addi,rd,rs1,0
        return tipo_i('addi',rd,rs_or_imm,0)
    elif instrucao == "not": #not equivale a xori,rd,rs1,-1
        return tipo_i('xori',rd,rs_or_imm,-1)
    else:
        print("Pseudo instrução inválida")


def chr_remove(old, to_remove):
    new_string = old
    for x in to_remove:
        new_string = new_string.replace(x, ' ')
    return new_string

def main():
    #Verifica se está sendo apssado um arquivo .asm
    if sys.argv[1][-4:] != ".asm":
            print("Entrada inválida")
            exit()    
    forma =""
    # verifica se a saida será por terminal ou arquivo

    if len(sys.argv) == 2:
        forma = "terminal"
    elif len(sys.argv) == 4 and sys.argv[2] == "-o":
        forma = "arquivo"

    #abre o arquivo de leitura
    try:
        arq = open(sys.argv[1], "r")
    except:
        print("Erro ao abri o arquivo de entrada!")
        exit()
    # Se a saida for por arquivo, abre tambem o arquivo de saída
    if forma == "arquivo":
        try:
            saida = open(sys.argv[3], "w")
        except:
            print("Erro ao abri o arquivo de saída!")

    # Armazena as linhas do arquivo  
    instrucoes = arq.readlines()

    if forma == "arquivo":
        for linha in instrucoes:
            linha = chr_remove(linha, ",&()")
            linha = linha.split()
            instru = linha[0]
            #Faz a remoção de do caractere 'x' ou identifica imediatos na base hexadecimal para conversão
            for i in range(1,len(linha)):
                if linha[i].startswith("0x"):
                    linha[i]=conversao_hexa(linha[i])
                elif linha[i].startswith("x"):
                    linha[i] = chr_remove(linha[i], "x")

            #Verifica o tipo da instrução para realizar a montagem
            if (instru == "add" or instru == "sub" or instru == "sll" or instru == "xor" or instru == "srl" or instru == "sra" or instru == "or" or instru == "and" or instru == "lr.d" or instru == "sc.d"):
                instrucao_gerada = tipo_r(instru, linha[1], linha[2], linha[3])
                saida.write(instrucao_gerada + "\n")
            elif (instru == "sb" or instru == "sh" or instru == "sw" or instru == "sd"):
                instrucao_gerada=tipo_s(instru, linha[1], linha[2], linha[3])
                saida.write(instrucao_gerada + "\n")
            elif (instru == "beq" or instru == "bne" or instru == "blt" or instru == "bge" or instru == "bltu" or instru == "bgeu"):
                instrucao_gerada=tipo_sb(instru, linha[1], linha [2], linha[3])
                saida.write(instrucao_gerada + "\n")
            elif (instru == "lui"):
                instrucao_gerada=tipo_U(instru,linha[1],linha[2])
                saida.write(instrucao_gerada + "\n")
            elif (instru == "jal"):
                instrucao_gerada=tipo_UJ(instru,linha[1],linha[2])
                saida.write(instrucao_gerada + "\n")
            elif (instru == "lb" or instru == "lh" or instru == "lw" or instru == "ld" or instru == "lbu" or instru == "lhu" or instru == "lwu" or instru == "addi" or instru == "slli" or instru == "xori" or instru == "srli" or instru == "srai" or instru == "ori" or instru == "andi" or instru == "jalr"):
                instrucao_gerada=tipo_i(instru, linha[1], linha[2], linha[3])
                saida.write(instrucao_gerada + "\n")
            elif (instru=="li" or instru=="not" or instru=="mv"):
                instrucao_gerada=tipo_pseudo(instru,linha[1],linha[2])
                saida.write(instrucao_gerada + "\n")
            else:
                print("Instrucao inválida")
                break

    elif forma == "terminal":
        #Recebe o nome do arquivo a ser lido, que foi passado pelo terminal
        local_arquivo = sys.argv[1]

        for linha in instrucoes:
            linha = chr_remove(linha, ",&()")
            linha = linha.split()
            instru = linha[0]

            #Faz a remoção de do caractere 'x' ou identifica imediatos na base hexadecimal para conversão
            for i in range(1,len(linha)):
                if linha[i].startswith("0x"):
                    linha[i]=conversao_hexa(linha[i])
                elif linha[i].startswith("x"):
                    linha[i] = chr_remove(linha[i], "x")

            print(linha)

            #Verifica o tipo da instrução para realizar a montagem
            if (instru == "add" or instru == "sub" or instru == "sll" or instru == "xor" or instru == "srl" or instru == "sra" or instru == "or" or instru == "and" or instru == "lr.d" or instru == "sc.d"):
                instrucao_gerada=tipo_r(instru, linha[1], linha[2], linha[3])
                print(f"{instrucao_gerada}")
            elif (instru == "sb" or instru == "sh" or instru == "sw" or instru == "sd"):
                instrucao_gerada=tipo_s(instru, linha[1], linha[2], linha[3] )
                print(instrucao_gerada)
            elif (instru == "beq" or instru == "bne" or instru == "blt" or instru == "bge" or instru == "bltu" or instru == "bgeu"):
                instrucao_gerada=tipo_sb(instru, linha[1], linha [2], linha[3])
                print(instrucao_gerada)
            elif (instru == "lui"):
                instrucao_gerada=tipo_U(instru,linha[1],linha[2])
                print(instrucao_gerada)
            elif (instru == "jal"):
                instrucao_gerada=tipo_UJ(instru,linha[1],linha[2])
                print(instrucao_gerada)
            elif (instru == "lb" or instru == "lh" or instru == "lw" or instru == "ld" or instru == "lbu" or instru == "lhu" or instru == "lwu" or instru == "addi" or instru == "slli" or instru == "xori" or instru == "srli" or instru == "srai" or instru == "ori" or instru == "andi" or instru == "jalr"):
                instrucao_gerada=tipo_i(instru, linha[1], linha[2], linha[3])
                print(instrucao_gerada)
            elif (instru=="li" or instru=="not" or instru=="mv"):
                instrucao_gerada=tipo_pseudo(instru,linha[1],linha[2])
                print(instrucao_gerada)
            else:
                print("Instrucao inválida")
                break

if __name__ == "__main__":
    main()