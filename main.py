import yfinance as yf
import json

def obtener_precio_actual(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period='1d')['Close'].iloc[0]
def obtener_informacion_ticker(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period='5d')


def guardar_portafolio(portafolio):
    with open("portafolio.json", "w") as archivo:
        json.dump(portafolio, archivo, indent=4)
def cargar_portafolio():
    with open("portafolio.json", "r") as archivo:
        return json.load(archivo)

def crear_portafolio():
  try:
    with open("portafolio.json", "r") as archivo:
      # Si el archivo existe, no hacemos nada
      pass
  except FileNotFoundError:
    # Si el archivo no existe, lo creamos con un portafolio básico
    portafolio_basico = {
        "acciones": {},
        "balance": 10000  
    }
    with open("portafolio.json", "w") as archivo:
      json.dump(portafolio_basico, archivo, indent=4)


def comprar_accion(ticker, cantidad):
    
    portafolio = cargar_portafolio()
    
    precio = obtener_precio_actual(ticker)
    costo_total = precio * cantidad
    if portafolio["balance"] >= costo_total:
        if ticker in portafolio["acciones"]:
            portafolio["acciones"][ticker]["cantidad"] += cantidad
            portafolio["acciones"][ticker]["precio_total"] = portafolio["acciones"][ticker]["precio_total"] + costo_total
            portafolio["balance"] -= costo_total

            guardar_portafolio(portafolio)

            return True
        else:
            portafolio["acciones"][ticker] = {"cantidad": cantidad, "precio_unitario": round(precio,2), "precio_total": round(costo_total,2)}
            portafolio["balance"] = round(float(portafolio["balance"] - costo_total),2)

            guardar_portafolio(portafolio)

            return True

    else:
        print("Fondos insuficientes")
        return False

def vender_accion(ticker, cantidad):
    portafolio = cargar_portafolio()
    
    precio = obtener_precio_actual(ticker)
    costo_total = precio * cantidad
    if portafolio["acciones"][ticker]:
        portafolio["acciones"][ticker]["cantidad"] -= cantidad
        portafolio["acciones"][ticker]["precio_total"] -= round(costo_total,2)
        portafolio["balance"] += round(costo_total,2)

        if portafolio["acciones"][ticker]["cantidad"] == 0:
            portafolio["acciones"].pop(ticker)

        guardar_portafolio(portafolio)
        
        return True
    else:
        print("No hay acciones disponibles")
        return False
    
def ver_diferencia(ticker):
    try:
        portafolio = cargar_portafolio()
        precio_total_portafolio = portafolio["acciones"][ticker]["precio_total"]
        precio_actual_portafolio = portafolio["acciones"][ticker]["precio_unitario"]
        precio = obtener_precio_actual(ticker)
        precio_total_mercado = precio * portafolio["acciones"][ticker]["cantidad"]

        print("Valor actual: ",round(precio,2))
        print("Valor total en mercado: ",round(precio_total_mercado,2),"\n")
        print("Valor actual en portafolio: ",round(precio_actual_portafolio,2))
        print("Valor total en portafolio: ",round(precio_total_portafolio,2))
        
        if precio_total_portafolio > precio_total_mercado:
            diferencia = precio_total_portafolio - precio_total_mercado
            print("Valor total: ",round(precio_total_portafolio - diferencia,2))
            return "Pérdida: "+str(round(diferencia,2))
        
        elif precio_total_portafolio == precio_total_mercado:
            return "No hay ganancia ni pérdida"
        else:
            diferencia = precio_total_portafolio - precio_total_mercado
            print("Valor total: ",round(precio_total_portafolio + diferencia,2))
            return "Ganancia: "+str(round(diferencia,2))
    except KeyError:
        return "Ticker inválido"

        
    

salir = False
opc = 0
crear_portafolio()
while salir == False:
    try:
        opc = int(input("Ingrese la opción: \n 1. Ver portafolio \n 2. Comprar acción \n 3. Ver información de un ticker \n 4. Vender acción \n 5. Ver diferencia \n 6. Salir\n"))
        match opc:
            case 1:
                print("Tu información: \n",cargar_portafolio(),"\n")
            case 2:
                ticker = input("Ingrese el ticker de la acción: \n")
                print("Información del ticker: \n", round(obtener_precio_actual(ticker),2))
                cantidad = int(input("Ingrese la cantidad de acciones: \n"))
                comprar_accion(ticker.upper(), cantidad)
            case 3:
                ticker = input("Ver información de un ticker: \n")
                print("Información del ticker: \n", obtener_informacion_ticker(ticker.upper()))
                print("\n")
            case 4:
                ticker = input("Ingrese el ticker de la acción: \n")
                cantidad = int(input("Ingrese la cantidad de acciones: \n")) 
                vender_accion(ticker.upper(),cantidad)
            case 5:
                ticker = input("Ingrese el ticker de la acción: \n")
                print(ver_diferencia(ticker.upper()))
                print("\n")
            case _:
                salir = True
    except ValueError:
        print("Opción inválida. Por favor ingrese un número.")
