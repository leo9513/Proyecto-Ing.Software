import math as m
import pandas as pd

inputfile = r"C:\Users\julia\OneDrive\Escritorio\PYTHON\Input\NIVELACION_GEOMETRICA_SIMPLE_BASE.xlsx "
outputfile = r"C:\Users\julia\OneDrive\Escritorio\PYTHON\output"

nivelacion_file = pd.read_excel(inputfile , sheet_name= "Hoja1", header = 0)
#print(nivelacion_file.shape)
#print(nivelacion_file.columns)
#print(nivelacion_file["VI"])
