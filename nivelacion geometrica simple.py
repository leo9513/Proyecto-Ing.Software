from ast import Return
import math as m
import re
import pandas as pd
import numpy as np

inputfile = r"C:\Users\julia\OneDrive\Escritorio\PYTHON\Input\NIVELACION_GEOMETRICA_SIMPLE_BASE.xlsx "
outputfile = r"C:\Users\julia\OneDrive\Escritorio\PYTHON\output"

df_nil = pd.read_excel(inputfile , sheet_name= "Hoja1", header = 0)
#print(nivelacion_file.shape)
#print(nivelacion_file.columns)
#print(df_nil["VI"])
Delta_list = df_nil["DELTA"].to_list()
Vmas_list = df_nil["Vista mas"].to_list()
Altura_ins_list = df_nil["Altura instrumental"].to_list()
Vmenos_list = df_nil["Vista menos"].to_list()
Vi_list = df_nil["Vista intermedia"].to_list()
Cota_list = df_nil["COTA"].to_list()

def Altura_ins(df_nil,Altura_ins_list):
    Altura_ins_list[1] = (df_nil["Vista mas"] + df_nil ["COTA"])
    print(Altura_ins_list[1])
    return(Altura_ins_list[1])

def cota (Altura_ins_list, Cota_list, Vi_list):
    Cota_list[2] = Altura_ins_list[1] - Vi_list[2]
    print(Cota_list[2])
    return(Cota_list[2])

cota (Altura_ins_list, Cota_list, Vi_list)





    









     





