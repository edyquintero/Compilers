import os

tokenTypes = {
    'INICIO': 'INICIO',
    'FIN': 'FIN',
    'ASIGNAR A': 'ASIGNAR A',
    'SI': 'SI',
    'ENTONCES': 'ENTONCES',
    'SINO': 'SINO',
    'FIN SI': 'FIN SI',
    'IMPRIMIR': 'IMPRIMIR',
    'OPERADOR_RELACIONAL': ['==', '!=', '<', '>', '<=', '>='],
    'OPERADOR_ARITMETICO': ['+', '-', '*', '/'],
    'ASIGNACION': '=',
    'PARENTESIS_IZQUIERDO': '(',
    'PARENTESIS_DERECHO': ')',
    'IDENTIFICADOR': 'IDENTIFICADOR',
    'ENTERO': 'ENTERO',
    'REAL': 'REAL',
    'CADENA': 'CADENA',
    'BOOLEANO': ['verdadero', 'falso']
}

def esIdentificador(caracter):
    return caracter.isalpha()

def esDigito(caracter):
    return caracter.isdigit()

def extraerIdentificador(input, pos):
    lexema = []
    while pos < len(input) and (input[pos].isalpha() or input[pos].isdigit() or input[pos] == '_'):
        lexema.append(input[pos])
        pos += 1
    return ''.join(lexema), pos

def extraerNumero(input, pos):
    lexema = []
    while pos < len(input) and input[pos].isdigit():
        lexema.append(input[pos])
        pos += 1
    if pos < len(input) and input[pos] == '.':
        lexema.append(input[pos])
        pos += 1
        while pos < len(input) and input[pos].isdigit():
            lexema.append(input[pos])
            pos += 1
    return ''.join(lexema), pos

def extraerCadena(input, pos):
    lexema = []
    pos += 1
    while pos < len(input) and input[pos] != '"':
        lexema.append(input[pos])
        pos += 1
    pos += 1
    return ''.join(lexema), pos

def tokenizar(input):
    tokens = []
    pos = 0
    fila = 0
    columna = 0
    while pos < len(input):
        if input[pos].isspace():
            if input[pos] == '\n':
                fila += 1
                columna = 0
            else:
                columna += 1
            pos += 1
            continue

        if input.startswith('INICIO', pos):
            tokens.append(('INICIO', 'INICIO', fila, columna + len('INICIO')))
            pos += len('INICIO')
            columna += len('INICIO')
            continue
        elif input.startswith('FIN SI', pos):
            tokens.append(('FIN SI', 'FIN SI', fila, columna + len('FIN SI')))
            pos += len('FIN SI')
            columna += len('FIN SI')
            continue
        elif input.startswith('FIN', pos):
            tokens.append(('FIN', 'FIN', fila, columna + len('FIN')))
            pos += len('FIN')
            columna += len('FIN')
            continue
        elif input.startswith('ASIGNAR A', pos):
            tokens.append(('ASIGNAR A', 'ASIGNAR A', fila, columna + len('ASIGNAR A')))
            pos += len('ASIGNAR A')
            columna += len('ASIGNAR A')
            continue
        elif input.startswith('ENTONCES', pos):
            tokens.append(('ENTONCES', 'ENTONCES', fila, columna + len('ENTONCES')))
            pos += len('ENTONCES')
            columna += len('ENTONCES')
            continue
        elif input.startswith('SINO', pos):
            tokens.append(('SINO', 'SINO', fila, columna + len('SINO')))
            pos += len('SINO')
            columna += len('SINO')
            continue
        elif input.startswith('SI', pos):
            tokens.append(('SI', 'SI', fila, columna + len('SI')))
            pos += len('SI')
            columna += len('SI')
            continue
        elif input.startswith('imprimir', pos):
            tokens.append(('IMPRIMIR', 'imprimir', fila, columna + len('imprimir')))
            pos += len('imprimir')
            columna += len('imprimir')
            continue

        if input[pos:pos + 2] in tokenTypes['OPERADOR_RELACIONAL']:
            tokens.append(('OPERADOR_RELACIONAL', input[pos:pos + 2], fila, columna + 2))
            pos += 2
            columna += 2
            continue
        elif input[pos] in tokenTypes['OPERADOR_ARITMETICO']:
            tokens.append(('OPERADOR_ARITMETICO', input[pos], fila, columna + 1))
            pos += 1
            columna += 1
            continue
        elif input[pos] == '=':
            tokens.append(('ASIGNACION', '=', fila, columna + 1))
            pos += 1
            columna += 1
            continue

        if input[pos] == '(':
            tokens.append(('PARENTESIS_IZQUIERDO', '(', fila, columna + 1))
            pos += 1
            columna += 1
            continue
        elif input[pos] == ')':
            tokens.append(('PARENTESIS_DERECHO', ')', fila, columna + 1))
            pos += 1
            columna += 1
            continue

        if esIdentificador(input[pos]):
            lexema, pos = extraerIdentificador(input, pos)
            if lexema in tokenTypes['BOOLEANO']:
                tokens.append(('BOOLEANO', lexema, fila, columna))
            else:
                tokens.append(('IDENTIFICADOR', lexema, fila, columna))
            columna += len(lexema)
            continue

        if esDigito(input[pos]):
            lexema, pos = extraerNumero(input, pos)
            if '.' in lexema:
                tokens.append(('REAL', lexema, fila, columna))
            else:
                tokens.append(('ENTERO', lexema, fila, columna))
            columna += len(lexema)
            continue

        if input[pos] == '"':
            lexema, pos = extraerCadena(input, pos)
            tokens.append(('CADENA', lexema, fila, columna + len(lexema)))
            columna += len(lexema) + 2
            continue

        pos += 1
        columna += 1

    return tokens

currentTokenPos = 0
tokens = []
codigo_traducido = []
lastToken = None

def match(expected_token):
    global currentTokenPos
    global tokens
    global lastToken

    if currentTokenPos < len(tokens) and tokens[currentTokenPos][0] == expected_token:
        lastToken = tokens[currentTokenPos]  # Almacenar el token actual antes de avanzar
        print(f"Se consumió el token: {lastToken}")
        currentTokenPos += 1
    else:
        token_actual = tokens[currentTokenPos]
        if lastToken:
            raise SyntaxError(
                f"Se esperaba '{expected_token}' pero se encontró '{token_actual[0]}' después del token en la posición (Fila: {lastToken[2]}, Columna: {lastToken[3]})")
        else:
            raise SyntaxError(f"Se esperaba '{expected_token}' pero se encontró '{token_actual[0]}'")

def programa():
    match('INICIO')
    lista_instrucciones()
    match('FIN')
    if currentTokenPos < len(tokens):
        token_restante = tokens[currentTokenPos]
        raise SyntaxError(
            f"Se encontró un token inesperado '{token_restante[0]}' en la posición (Fila: {token_restante[2]}, Columna: {token_restante[3]}) después del token FIN."
        )

def lista_instrucciones():
    while currentTokenPos < len(tokens) and tokens[currentTokenPos][0] in ['ASIGNAR A', 'SI', 'IMPRIMIR']:
        instruccion()

def instruccion():
    if tokens[currentTokenPos][0] == 'ASIGNAR A':
        asignacion()
    elif tokens[currentTokenPos][0] == 'SI':
        estructura_condicional()
    elif tokens[currentTokenPos][0] == 'IMPRIMIR':
        imprimir()

def asignacion():
    match('ASIGNAR A')
    match('IDENTIFICADOR')
    var = tokens[currentTokenPos - 1][1]
    match('ASIGNACION')
    if tokens[currentTokenPos][0] in ['ENTERO', 'REAL', 'CADENA', 'BOOLEANO']:
        match(tokens[currentTokenPos][0])
        valor = tokens[currentTokenPos][1]
        codigo_traducido.append(f"{var} = {valor}")
    else:
        token_actual = tokens[currentTokenPos]
        if lastToken:
            raise SyntaxError(
                f"Se esperaba un valor (ENTERO, REAL, CADENA o BOOLEANO) pero se encontró '{token_actual[0]}' en la posición (Fila: {lastToken[2]}, Columna: {lastToken[3]})")

def estructura_condicional():
    match('SI')

    # Construir condición
    variable_condicion = tokens[currentTokenPos][1]  # Identificador
    match('IDENTIFICADOR')

    operador = tokens[currentTokenPos][1]  # Operador relacional
    match('OPERADOR_RELACIONAL')

    valor = tokens[currentTokenPos][1]  # Valor (identificador o constante)
    if tokens[currentTokenPos][0] in ['IDENTIFICADOR', 'ENTERO', 'REAL', 'BOOLEANO']:
        match(tokens[currentTokenPos][0])
    else:
        raise SyntaxError(f"Se esperaba 'IDENTIFICADOR' o un valor, pero se encontró '{tokens[currentTokenPos][0]}'")

    condicion = f"{variable_condicion} {operador} {valor}"
    codigo_traducido.append(f"if {condicion}:")

    match('ENTONCES')
    lista_instrucciones()

    if currentTokenPos < len(tokens) and tokens[currentTokenPos][0] == 'SINO':
        match('SINO')
        codigo_traducido.append("else:")
        lista_instrucciones()

    match('FIN SI')


def imprimir():
    match('IMPRIMIR')
    match('PARENTESIS_IZQUIERDO')
    match('CADENA')
    mensaje = tokens[currentTokenPos - 1][1]
    match('PARENTESIS_DERECHO')
    codigo_traducido.append(f'print("{mensaje}")')

def analizar_desde_archivo(nombre_archivo):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, 'r') as archivo:
            input = archivo.read()
        global tokens, currentTokenPos, codigo_traducido
        tokens = tokenizar(input)
        currentTokenPos = 0
        codigo_traducido = []
        programa()
        print("Código traducido a Python:")
        print("\n".join(codigo_traducido))
    else:
        print("El archivo no existe.")

# Ejemplo de uso
name = input("Ingrese el nombre de su archivo: ")
analizar_desde_archivo(name)
