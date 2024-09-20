import re

ERROR1 = "Error #1, la cadena no puede iniciar con un signo"
ERROR2 = "Error #2, la cadena no puede finalizar con un signo"
ERROR3 = "Error #3, la cadena no puede contar con dos signos seguidos"
ERROR4 = "Error #4, la cadena contiene un caracter inválido"


class Automata:
    def __init__(self):
        self.estados = set(f'q{i}' for i in range(3))
        self.alfabeto = {
            '[0-9]', '-', '+'
        }
        self.estadoInicial = 'q0'
        self.estadoFinal = {'q1'}

        self.transiciones = {
            # Q0
            ('q0', '[0-9]'): 'q1',
            # Q1
            ('q1', r'\+'): 'q2',
            ('q1', r'\-'): 'q2',
            ('q1', '[0-9]'): 'q1',
            # Q2
            ('q2', '[0-9]'): 'q1',
        }

    def esAceptado(self, string):
        counter = 0
        if string[0] in '+-':
            return False, ERROR1, counter

        if string[-1] in '+-':z
            return False, ERROR2, len(string) - 1

        estadoActual = self.estadoInicial
        last_symbol = ''
        for i, simbolo in enumerate(string):
            if not re.match(r'[0-9+\-]', simbolo):
                return False, ERROR4, i

            if last_symbol in '+-' and simbolo in '+-':
                return False, ERROR3, i

            transition_found = False
            for (estado, regex), nuevo_estado in self.transiciones.items():
                if estado == estadoActual and re.match(regex, simbolo):
                    estadoActual = nuevo_estado
                    transition_found = True
                    break
            if not transition_found:
                return False, "Error, transición no encontrada", i

            last_symbol = simbolo
        return estadoActual in self.estadoFinal, None, counter


def main():
    automata = Automata()
    strings = [
        '4+2',
        '123',
        '1-2',
        '12+3',
        '5-6+7',
        '+1',
        '44++4',
        '-2',
        '2-3-4-6-1-1-2-1212-121212-121212',
        '1*2',
        '1------1-'
    ]

    for stringActual in strings:
        aceptado, error, counter = automata.esAceptado(stringActual)
        if aceptado:
            print(f'\tLa cadena "{stringActual}" fue aceptada.')
        else:
            print(f'\tLa cadena "{stringActual}" no fue aceptada: {error} en la posición {counter + 1}')


if __name__ == "__main__":
    main()
