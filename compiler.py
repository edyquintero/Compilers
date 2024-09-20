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

tokens = tokenizar(inputText)

for token in tokens:
    tipo, lexema = token
    print(f"TOKEN = {{TYPE: {tipo} | LEXEMA: {lexema}}}")

print(tokens)
