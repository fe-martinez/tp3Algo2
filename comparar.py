f = open('comunidad-chile.txt', 'r')
boca = f.readline()
f.close
e = open('resultado.txt', 'r')
resultado = e.readline()
e.close

lista_boca = boca.split(",")
lista_resultado = resultado.split(",")

lista_resultado_final = []
for element in lista_resultado:
    lista_resultado_final.append(element.strip())

lista_boca_final = []
for element in lista_boca:
    lista_boca_final.append(element.lstrip())

main_list = list(set(lista_resultado_final)-set(lista_boca_final))
print(main_list)
print(len(main_list), len(lista_boca_final), len(lista_resultado_final))
