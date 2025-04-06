import sys

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
        funct3 == "101"
    elif (instru == "or"):
        funct3 == "110"
    elif (instru == "and"):
        funct3 == "111"
    elif (instru == "lr.d" or instru == "sc.d"):
        funct3 == "011"

    # Seta o opcode correto para as instruções do tipo R
    opcode = "0110011"

    #concatena as strings de bits para formar umas instrução de 32 bits
    saida = funct7 + rs2 + rs1 + funct3 +  rd +  opcode

    print(saida)

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
    


def tipo_s(instrucao):
    return 1

def tipo_sb(instrucao):
    return 1

def tipo_U(instrucao):
    return 1

def tipo_UJ(instrucao):
    return 1

def tipo_i(instrucao):
    return 1

def chr_remove(old, to_remove):
    new_string = old
    for x in to_remove:
        new_string = new_string.replace(x, ' ')
    return new_string


for linha in sys.stdin:
    linha = chr_remove(linha, ",x&()")
    linha = linha.split()
    instru = linha[0]
    print(linha)
    print(instru)
    if (instru == "add" or instru == "sub" or instru == "sll" or instru == "xor" or instru == "srl" or instru == "sra" or instru == "or" or instru == "and" or instru == "lr.d" or instru == "sc.d"):
        tipo_r(instru, linha[1], linha[2], linha[3])
    elif (instru == "sb" or instru == "sh" or instru == "sw" or instru == "sd"):
        tipo_s()
    elif (instru == "beq" or instru == "bne" or instru == "blt" or instru == "bge" or instru == "bltu" or instru == "bgeu"):
        tipo_sb()
    elif (instru == "lui"):
        tipo_U()
    elif (instru == "jal"):
        tipo_UJ()
    elif (instru == "lb" or instru == "lh" or instru == "lw" or instru == "ld" or instru == "lbu" or instru == "lhu" or instru == "lwu" or instru == "addi" or instru == "slli" or instru == "xori" or instru == "srli" or instru == "srai" or instru == "ori" or instru == "andi" or instru == "jalr"):
        tipo_i()
    else:
        print("Instrucao iinválida")
        break