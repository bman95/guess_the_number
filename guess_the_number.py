import random
import pandas as pd
import matplotlib.pyplot as plt
from stdiomask import getpass


def main():
    while True:
        menu_principal()
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            menu_dificultad()
            dificultad = input("Selecciona la dificultad: ")
            menu_dificultad_intervalo()
            dificultad_intervalo = input(
                "Selecciona la dificultad (en cuanto a intervalo a adivinar): ")
            modo_solitario(dificultad, dificultad_intervalo)
        elif opcion == '2':
            menu_dificultad()
            dificultad = int(input("Selecciona la dificultad: "))
            menu_dificultad_intervalo()
            dificultad_intervalo = int(
                input("Selecciona la dificultad (en cuanto a intervalo a adivinar): "))
            modo_dos_jugadores(dificultad, dificultad_intervalo)
        elif opcion == '3':
            estadisticas()
            filtrado_estadistica()
        elif opcion == '4':
            print("¡Gracias por jugar!\n")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.\n")


def menu_principal():
    print("\nBienvenido al juego de adivinanzas:")
    print("1. Partida modo solitario")
    print("2. Partida 2 Jugadores")
    print("3. Estadística")
    print("4. Salir")


def menu_dificultad():
    print("\nSelecciona la dificultad:")
    print("1. Fácil (20 intentos)")
    print("2. Media (12 intentos)")
    print("3. Difícil (5 intentos)")


def menu_dificultad_intervalo():
    print("\nSelecciona la dificultad (en cuanto a intervalo a adivinar):")
    print("1. Fácil (entre 1 y 500)")
    print("2. Media (entre 1 y 1000)")
    print("3. Difícil (entre 1 y 5000)")


def transform_dificultad(x):
    if x == '1':
        return 20
    elif x == '2':
        return 12
    else:
        return 5


def modo_solitario(dificultad, dificultad_intervalo):
    if dificultad_intervalo == "1":
        limite_superior = 500
    elif dificultad_intervalo == "2":
        limite_superior = 1000
    elif dificultad_intervalo == "3":
        limite_superior = 5000

    intentos_posibles = transform_dificultad(dificultad)
    numero_a_adivinar = random.randint(1, limite_superior)
    juego(intentos_posibles, numero_a_adivinar,
          dificultad, limite_superior, num_jug='un jugador')


def modo_dos_jugadores(dificultad):
    while True:

        numero_a_adivinar = int(
            getpass("Primer jugador, introduce el número a adivinar (entre 1 y 1000): ", mask=''))
        if 1 <= numero_a_adivinar <= 1000:
            break
        else:
            print(f'{numero_a_adivinar} no está entre 1 y 1000')
    intentos_posibles = transform_dificultad(dificultad)

    if not (1 <= dificultad <= 3):
        print("Dificultad no válida.")
        return

    juego(intentos_posibles, numero_a_adivinar,
          dificultad, num_jug='dos jugadores')


def juego(intentos_posibles, numero_a_adivinar, dificultad, limite_superior, num_jug='un jugador'):
    if num_jug == 'un jugador':
        num_jug = f'(entre 1 y {limite_superior})'
    else:
        num_jug = '(Segundo jugador)'

    intentos = 0
    while intentos < intentos_posibles:
        intento_usuario = int(
            input(f"Intenta adivinar el número {num_jug}: "))
        intentos += 1
        if intento_usuario == numero_a_adivinar:
            print("¡Felicidades! ¡Adivinaste!")
            registrar_estadistica("Modo Dos Jugadores",
                                  "Ganado", dificultad, intentos)
            return
        elif intento_usuario < numero_a_adivinar:
            print("El número buscado es mayor.")
        else:
            print("El número buscado es menor.")
    print("Lo siento, has agotado tus intentos. El número correcto era",
          numero_a_adivinar)
    registrar_estadistica("Modo Dos Jugadores", "Perdido",
                          dificultad, intentos_posibles)


def estadisticas():
    df = pd.read_excel('game_data.xlsx')
    print(df, '\n')
    grafico_df = df.groupby(['Jugador']).size()
    grafico_df.plot(kind='bar')
    plt.ylabel('Partidas')
    plt.show()


def filtrado_estadistica():
    df = pd.read_excel('estadisticas_tarea.xlsx')
    while True:
        filtrado = input(
            "¿Desea hacer filtrado de estadísticas? (Presione 's' para si, 'n' para no )  ").strip()
        if filtrado == 's':
            grupo_jugadores = set(df['Jugador'])
            print(grupo_jugadores)
            f_jugador = input(
                'Introduzca nombre de jugador a buscar: ').strip()
            if f_jugador in list(df['Jugador']):
                player_data = df[df['Jugador'] == f_jugador]
                win_loss_counts = player_data['Resultado'].value_counts()

                plt.pie(win_loss_counts.values,
                        labels=win_loss_counts.index, autopct='%1.1f%%')
                print(df.loc[df['Jugador'] == f_jugador])
                plt.ylabel('Partidas')
                plt.show()

            else:
                print("No hay registros de ese jugador")
        elif filtrado == 'n':
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.\n")


def registrar_estadistica(modo, resultado, dificultad, intentos):
    if dificultad == 1:
        dificultad = "Fácil"
    elif dificultad == 2:
        dificultad = "Media"
    else:
        dificultad = "Difícil"
    jugador = input("Ingresa tu nombre: ")
    df = pd.read_excel('estadisticas_tarea.xlsx')

    nueva_fila = {
        'Jugador': jugador,
        'Modo': modo,
        'Resultado': resultado,
        'Dificultad': dificultad,
        'Intentos': intentos
    }

    df = df._append(nueva_fila, ignore_index=True)
    print(df, '\n')
    df.to_excel('estadisticas_tarea.xlsx', index=False)


if __name__ == "__main__":
    main()
