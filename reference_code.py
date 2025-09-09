def pedir_numero(msg, min):
    num = int(input(f"{msg}(>{min}): "))
    while num <= min:
        num = int(input(f"Error. {msg} (>{min}): "))
    return num


def pedir_lista(dim):
    lista = []
    for i in range(dim):
        n = int(input(f"Introduce el elemento {i+1}: "))
        lista.append(n)
    return lista


def obtener_lista_medias(lista):
    lista2 = []
    for i in range(len(lista)):
        if i == 0:
            media = (lista[i] + lista[i + 1]) / 2
        elif i == (len(lista) - 1):
            media = (lista[i - 1] + lista[i]) / 2
        else:
            media = (lista[i - 1] + lista[i] + lista[i + 1]) / 3
        lista2.append(media)
    return lista2


def mostrar_lista(lista):
    for elemento in lista:
        print(f"{elemento:.2f}", end=" ")


def main():
    dimension = pedir_numero("Introduce el número de elementos de la lista", 2)
    lista = pedir_lista(dimension)
    lista2 = obtener_lista_medias(lista)
    print("El vector resultado es: ")
    mostrar_lista(lista2)


if __name__ == "__main__":
    main()