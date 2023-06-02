# import json
# from datetime import date, datetime

# def usunZadanie():
#         with open("to_do_lista/lista_zadan.json", "r", encoding="utf-8") as plik:
#             lista_zadan = json.load(plik)
#         task_do_usuniecia = int(input("Wprowadź ID zadania, które chcesz usunąć: "))
#         lista = [element for element in lista_zadan if element['ID'] != task_do_usuniecia]
#         print(lista)

# usunZadanie()

lista = [element for element in listaZadan if element['ID'] != do_usuniecia]
