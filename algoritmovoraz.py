import math
import time

N = 8
INF = 99999

NOMBRES = ["Almacen","C1","C2","C3","C4","C5","C6","C7"]

X = [0,2,5,3,7,9,6,1]
Y = [0,4,2,7,5,2,9,9]

H_INI = [0,8,9,8,10,11,9,8]
H_FIN = [24,14,15,14,16,17,15,14]

VEH = ["Moto","Auto","Camioneta"]
CAP = [20,60,150]
VEL = [40,60,80]

ARISTAS = [
    (0,1),(0,2),(1,3),(1,7),
    (2,4),(2,5),(3,6),
    (3,7),(4,5),(4,6),(5,6)
]

def distancia(a,b):
    return math.sqrt((X[a]-X[b])**2 + (Y[a]-Y[b])**2)

def floyd():
    d = [[INF]*N for _ in range(N)]
    for i in range(N):
        d[i][i] = 0
    for a,b in ARISTAS:
        d[a][b] = distancia(a,b)
        d[b][a] = d[a][b]
    for k in range(N):
        for i in range(N):
            for j in range(N):
                d[i][j] = min(d[i][j],d[i][k]+d[k][j])
    return d

def distancia_ruta(ruta,d):
    total = d[0][ruta[0]]
    for i in range(len(ruta)-1):
        total += d[ruta[i]][ruta[i+1]]
    return total + d[ruta[-1]][0]

def voraz(d,pesos,cap,vel):
    visitados = [False]*N
    visitados[0] = True

    ruta = []
    nodo = 0
    tiempo = 8
    peso = 0

    while len(ruta) < N-1:
        mejor = -1
        menor = INF
        for c in range(1,N):
            if not visitados[c]:
                llegada = tiempo + d[nodo][c]/vel
                if (peso + pesos[c] <= cap 
                    and llegada <= H_FIN[c]
                    and d[nodo][c]<menor):
                    mejor = c
                    menor = d[nodo][c]
        if mejor == -1:
            break
        visitados[mejor] = True
        ruta.append(mejor)
        tiempo += d[nodo][mejor]/vel
        tiempo = max(tiempo,H_INI[mejor])
        peso += pesos[mejor]
        nodo = mejor
    return ruta

def mostrar(ruta):
    print(
        " -> ".join(
            ["Almacen"]+
            [NOMBRES[i] for i in ruta]+
            ["Almacen"]
        )
    )

def main():
    pesos = [0]*N

    print("\nSISTEMA DE RUTAS - METODO VORAZ")
    print("-"*40)

    for i in range(1, N):
        while True:
            entrada = input(f"Peso pedido {NOMBRES[i]}: ")
            if entrada == "":
                print("Cantidad inválida")
                continue
            try:
                peso = float(entrada)
                if peso <= 0:
                    print("Cantidad inválida")
                    continue
                pesos[i] = peso
                break
            except ValueError:
                print("Cantidad inválida")

    total = sum(pesos)
    print(f"\nPeso total: {total}")

    print("\nVehiculos disponibles:")
    for i in range(3):
        print(f"{i+1} {VEH[i]} {CAP[i]} kg")

    while True:
        try:
            op = int(input("Seleccione vehículo (1-3): "))
            if op < 1 or op > 3:
                print("Opción inválida")
                continue
            if total <= CAP[op - 1]:
                break
            print("Capacidad insuficiente")
        except ValueError:
            print("Opción inválida")

    cap = CAP[op-1]
    vel = VEL[op-1]

    d = floyd()

    print("\n--- CALCULANDO RUTA VORAZ ---")
    inicio = time.time()
    
    rv = voraz(d,pesos,cap,vel)
    
    tv = (time.time()-inicio)*1000
    dv = distancia_ruta(rv,d) if rv else INF

    print(f"\nClientes visitados: {len(rv)}/{N-1}")
    print(f"Distancia total: {dv:.2f} km")
    print(f"Tiempo de ejecucion: {tv:.5f} ms")
    print("\nRuta calculada:")
    mostrar(rv)

if __name__ == "__main__":
    main()
