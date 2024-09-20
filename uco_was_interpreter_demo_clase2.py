import sys
import re

currentTokenPos = 0
currentToken = ""


def match(token):
    global currentTokenPos
    global currentToken
    global vec_tokenTypes
    currentToken = vec_tokenTypes[currentTokenPos]
    if currentToken == token:
        currentTokenPos = currentTokenPos + 1
        print("se consumio ", token, "\n")
    else:
        print("Syntax Error\n")


def ids():
    global currentTokenPos
    global currentToken
    global vec_tokenTypes
    currentToken = vec_tokenTypes[currentTokenPos]
    if currentToken == "id":
        match('id')
        match(';')
        ids()  # no else because ids can be epsilon


def showroom():
    match('SHOWROOM')
    match('{')
    ids()
    match('}')


def product():
    match('PRODUCT')
    match('{')
    match('PRDID')
    match('{')
    match('id')
    match('}')
    match('TITLE')
    match('{')
    match('str')
    match('}')
    match('DESC')
    match('{');
    match('str')
    match('}')
    match('PRICE')
    match('{')
    match('num')
    match('}')
    match('}')


def product_grp():
    global currentTokenPos
    global currentToken
    global vec_tokenTypes
    currentToken = vec_tokenTypes[currentTokenPos]
    if currentToken == "PRODUCT":
        product()
        product_grp()


# there is no else, because con be <product_grp> can be epsilon


def warehouse():
    match('WAREHOUSE')
    match('{')
    product_grp()
    match('}')


def store():
    match('STORE')
    match('{')
    match('TITLE')
    match('{')
    match('id')
    match('}')
    match('CONTACTINFO')
    match('{')
    match('str')
    match('}')
    warehouse()
    showroom()
    match('}')


# total arguments
n = len(sys.argv)
if n < 2:
    print("Error the program need at least one argument\n")

else:
    f = open(sys.argv[1], "r")
    inputstr = f.read()
    f.close()
    # 1. Ahora se borran los signos espacio, tabulador y linea nueva de la entreada
    print("1. Se eliminan las espacios, tabuladores y linea nueva, aquedando asi:")
    inputstr = re.sub(r"[\n\t\s]*", "", inputstr)
    print(inputstr)

    # 2. Ahora se agregan nuevos espacios, pero exclusivamente a partir de los { y }
    print("\n2. Ahora se agregan nuevos espacios, pero exclusivamente a partir de los {, ; y }: ")
    inputstr = re.sub(r"{", " { ", inputstr)
    inputstr = re.sub(r"}", " } ", inputstr)
    inputstr = re.sub(r";", " ; ", inputstr)
    print(inputstr)

    # 3. Ahora se realiza la clasificacion de lexemas
    inputstr = inputstr.split(" ")
    print("La lista de posibles lexemas es: ")
    print(inputstr)

    vec_tokenTypes = []
    vec_lexems = []
    dic_directTokens = {'STORE': 'STORE',
                        '{': '{',
                        'TITLE': 'TITLE',
                        '}': '}',
                        'CONTACTINFO': 'CONTACTINFO',
                        'WAREHOUSE': 'WAREHOUSE',
                        'PRODUCT': 'PRODUCT',
                        'PRDID': 'PRDID',
                        'DESC': 'DESC',
                        'PRICE': 'PRICE',
                        'SHOWROOM': 'SHOWROOM',
                        ';': ';'}
    for c in inputstr:
        r = dic_directTokens.get(c)
        if r:
            vec_tokenTypes.append(r)
            vec_lexems.append(r)
        elif re.match(r"^%[a-zA-Z0-9_]*%$", c):
            vec_tokenTypes.append('id')
            vec_lexems.append(c)
        elif re.match(r"\"*\"", c):
            vec_tokenTypes.append('str')
            vec_lexems.append(c)
        elif re.match(r"[0-9]+", c):
            vec_tokenTypes.append('num')
            vec_lexems.append(c)

    print("Tokentypes quedo:\n")
    print(vec_tokenTypes)
    print("Lexems quedo:\n")
    print(vec_lexems)

    # The syntax analize begin
    store()








