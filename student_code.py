def pedir_dimension():
    d = int(input("Introduce la dimension de la lista: "))
    while d<2:
        d = int(input("Eror, el número tiene que ser mayor o igual que 2: "))
    return(d)

def pedir_valores():
    l1 = []
    for i in range(d):
        valor = int(input(f"Introduce el elemento {i+1}: "))
        l1.append(valor)
    return(l1)

def medias():
    l2 = []
    for pos in range(d):
        if pos==0:
             M = (l1[pos]+l1[pos+1])/2
        elif pos==d-1:
             M = (l1[pos-1]+l1[pos])/2
        elif 0<pos<(d-1):
             M = (l1[pos-1]+l1[pos]+l1[pos+1])/3
        l2.append(M)
    return(l2)





def main(): 
    d = pedir_dimension()
    l1 = pedir_valores()
    l2 = medias()

    print(f"La lista original es {l1}")
    print(f"La lista resultado es {l2}")
    


if __name__ == "__main__":
    main()