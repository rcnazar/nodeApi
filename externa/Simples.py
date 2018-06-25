import sys
import time
import data_cleansing_release

cdc = data_cleansing_release.conector_data_cleansing().ConectorDataCleansing()

while(True):
    a = sys.stdin.readline()
    print(cdc.normalizarEndereco(None, a, None, None, "BRASILIA", "DISTRITO FEDERAL", None))

# print("1: " + sys.argv[1])
# print("2: " + sys.argv[2])
# time.sleep(2)
# imprimir(a)