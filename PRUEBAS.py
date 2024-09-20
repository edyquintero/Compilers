# Definición de tipos de tokens
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

# Funciones auxiliares para el análisis léxico
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

# Función para tokenizar el texto de entrada
def tokenizar(input):
    tokens = []
    pos = 0
    while pos < len(input):
        if input[pos].isspace():
            pos += 1
            continue

        if input.startswith('INICIO', pos):
            tokens.append(('INICIO', 'INICIO'))
            pos += len('INICIO')
            continue
        elif input.startswith('FIN SI', pos):
            tokens.append(('FIN SI', 'FIN SI'))
            pos += len('FIN SI')
            continue
        elif input.startswith('FIN', pos):
            tokens.append(('FIN', 'FIN'))
            pos += len('FIN')
            continue
        elif input.startswith('ASIGNAR A', pos):
            tokens.append(('ASIGNAR A', 'ASIGNAR A'))
            pos += len('ASIGNAR A')
            continue
        elif input.startswith('ENTONCES', pos):
            tokens.append(('ENTONCES', 'ENTONCES'))
            pos += len('ENTONCES')
            continue
        elif input.startswith('SINO', pos):
            tokens.append(('SINO', 'SINO'))
            pos += len('SINO')
            continue
        elif input.startswith('SI', pos):
            tokens.append(('SI', 'SI'))
            pos += len('SI')
            continue
        elif input.startswith('imprimir', pos):
            tokens.append(('IMPRIMIR', 'imprimir'))
            pos += len('imprimir')
            continue

        if input[pos:pos+2] in tokenTypes['OPERADOR_RELACIONAL']:
            tokens.append(('OPERADOR_RELACIONAL', input[pos:pos+2]))
            pos += 2
            continue
        elif input[pos] in tokenTypes['OPERADOR_ARITMETICO']:
            tokens.append(('OPERADOR_ARITMETICO', input[pos]))
            pos += 1
            continue
        elif input[pos] == '=':
            tokens.append(('ASIGNACION', '='))
            pos += 1
            continue

        if input[pos] == '(':
            tokens.append(('PARENTESIS_IZQUIERDO', '('))
            pos += 1
            continue
        elif input[pos] == ')':
            tokens.append(('PARENTESIS_DERECHO', ')'))
            pos += 1
            continue

        if esIdentificador(input[pos]):
            lexema, pos = extraerIdentificador(input, pos)
            if lexema in tokenTypes['BOOLEANO']:
                tokens.append(('BOOLEANO', lexema))
            else:
                tokens.append(('IDENTIFICADOR', lexema))
            continue

        if esDigito(input[pos]):
            lexema, pos = extraerNumero(input, pos)
            if '.' in lexema:
                tokens.append(('REAL', lexema))
            else:
                tokens.append(('ENTERO', lexema))
            continue

        if input[pos] == '"':
            lexema, pos = extraerCadena(input, pos)
            tokens.append(('CADENA', lexema))
            continue

        pos += 1

    return tokens

# Variables globales para el análisis sintáctico
currentTokenPos = 0
tokens = []

# Funciones para el análisis sintáctico
def match(expected_token):
    global currentTokenPos
    global tokens
    if currentTokenPos < len(tokens) and tokens[currentTokenPos][0] == expected_token:
        print(f"Se consumió el token: {tokens[currentTokenPos]}")
        currentTokenPos += 1
    else:
        raise SyntaxError(f"Se esperaba {expected_token} pero se encontró {tokens[currentTokenPos][0]}")

def programa():
    match('INICIO')
    lista_instrucciones()
    match('FIN')

def lista_instrucciones():
    if currentTokenPos < len(tokens) and tokens[currentTokenPos][0] in ['ASIGNAR A', 'SI', 'IMPRIMIR']:
        instruccion()
        lista_instrucciones()

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
    match('ASIGNACION')  # El operador de asignación '='
    expresion()

def estructura_condicional():
    match('SI')
    expresion()
    match('ENTONCES')
    lista_instrucciones()
    if currentTokenPos < len(tokens) and tokens[currentTokenPos][0] == 'SINO':
        match('SINO')
        lista_instrucciones()
    match('FIN SI')

def imprimir():
    match('IMPRIMIR')
    match('PARENTESIS_IZQUIERDO')
    match('CADENA')
    match('PARENTESIS_DERECHO')

def expresion():
    if tokens[currentTokenPos][0] in ['IDENTIFICADOR', 'ENTERO', 'REAL', 'BOOLEANO']:
        match(tokens[currentTokenPos][0])

        if currentTokenPos < len(tokens) and tokens[currentTokenPos][0] == 'OPERADOR_RELACIONAL':
            match('OPERADOR_RELACIONAL')

            if tokens[currentTokenPos][0] in ['IDENTIFICADOR', 'ENTERO', 'REAL', 'BOOLEANO']:
                match(tokens[currentTokenPos][0])
                return

# Entrada de ejemplo
inputText = '''
INICIO
ASIGNAR A x = 5
ASIGNAR A y = 10
SI x < y ENTONCES
  imprimir("x es menor que y")
SINO
  imprimir("x no es menor que y")
FIN SI
FIN
'''

# Tokenizar el texto de entrada
tokens = tokenizar(inputText)

# Mostrar tokens generados
print("Tokens generados:")
for token in tokens:
    print(f"TOKEN = {{TYPE: {token[0]} | LEXEMA: {token[1]}}}")

# Análisis sintáctico
try:
    programa()
    print("Análisis sintáctico completado sin errores.")
except SyntaxError as e:
    print(f"Error de sintaxis: {e}")
