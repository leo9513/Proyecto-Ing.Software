#Programa para leer archivo excel y devolver valores como una lista

from http.client import PRECONDITION_FAILED
import pandas as pd
import math as m
#inputfile=input("Ingrese la ruta en la que se guardara el archivo base: \n")
inputfile=r"C:\Users\leoda\Desktop\Materias U\Materias 5 semestre\Ing de software\proyecto_ing_software\basePolCerrada.xlsx"

df=pd.read_excel(inputfile)

deltas_list=df['Δ'].to_list()

puntos_list=df['ο'].to_list()

ang_list_df_final=df['Ang.Obs(GGGMMSS)'].to_list()

dist_list_df_final=df['Dist'].to_list()

df_datos=df[df['Ang.Obs(GGGMMSS)']!=0]

angulos_list=df_datos['Ang.Obs(GGGMMSS)'].tolist()

dist_list=df_datos['Dist'].tolist()

dist_list=dist_list[:-1]

vertices= len(angulos_list)-1

list_parametros_ang=['\u03A3'+'OBS','\u03A3'+'Teo','e ang','e perm','corr ang']

list_parametros_proyecciones=['\u03A3'+'DIST','\u0394'+'PNS','\u0394'+'PEW','e dist','P']


class Topoutils():
    def gms_angle_to_decimals(self, gms_angle):
        minutes, degree_part = m.modf(gms_angle / 10000)
        seconds, minutes= m.modf(minutes*100)
        seconds *=100

        self.decimal_angle =  degree_part + minutes/60 + seconds /3600
        return self.decimal_angle

    def decimal_angle_to_gms(self, decimal_angle, total_decimals =0):
        if decimal_angle>=0:
            grados=int(decimal_angle)
            minutos=int((decimal_angle-grados)*60)
            segundos=round((((decimal_angle-grados)*60)-minutos)*60,0)
            self.gms_angle=("{}° {}'{}".format(grados,minutos,segundos))

        else:
            grados=int(abs(decimal_angle))
            minutos=int(abs(decimal_angle-grados)*60)
            segundos=round(abs(((decimal_angle-grados)*60)-minutos)*60,0)
            self.gms_angle=("-{}° {}'{}".format(grados,minutos,segundos))
        return self.gms_angle

    def suma_ang(self,angulos_list):
        suma=0
        for angulo in angulos_list:
            angulo_decimal = self.gms_angle_to_decimals(angulo)
            suma+=angulo_decimal
        self.suma=suma
        return self.suma

    def error_angular(self,suma_angulo):
        sentido = float(input("Digite '1' si la poligonal tiene angulos internos, digite '2' si son externos: \n"))
        if sentido==1:
                angulos_i = suma_angulo
                angulos_teo = float((vertices-2)*180+360)
                cierre = float(angulos_i-angulos_teo)
        else:
            angulos_e = suma_angulo
            angulos_teo = float((vertices+2)*180)
            cierre = float(angulos_e-angulos_teo)
        self.cierre_and_angTeo=[cierre,angulos_teo]
        return self.cierre_and_angTeo   
        
    def correccion_error(self,error):
        if error>0:
            corr_error=-error/(vertices+1)
        if error<0:
            corr_error=abs(error)/(vertices+1)
        self.corr_error=corr_error
        return self.corr_error

    def error_per(self, error_angular):

        precision_estacion=float(input("Ingrese el precisión a la que mide la estación GGGMMSS \n"))

        error_perm=precision_estacion*vertices
        error_permi=self.gms_angle_to_decimals(error_perm)
        error_permitido=self.decimal_angle_to_gms(error_permi)

        error_angular_gms=self.decimal_angle_to_gms(abs(error_angular[0]))

        if abs(error_angular[0])>=error_permi:
            print("Devuelvase a campo mi papá, tiene un error angular de "+str(error_angular_gms)+" y el permitido es de "+str(error_permitido))
            quit()
        self.error_permitido=error_permitido
        return error_permitido

    def suma_and_corr_ang(self,angulos_list,corr_error):
        suma_ang_corr=0
        ang_corr_list=[]
        for angulo in angulos_list:
            angulo_decimal = self.gms_angle_to_decimals(angulo)
            angulocorr=angulo_decimal+corr_error
            ang_corr_list.append(angulocorr)
            suma_ang_corr+=angulocorr
        self.suma_and_corr_ang=[suma_ang_corr,ang_corr_list]
        return self.suma_and_corr_ang

    def bearing_and_distance(self):
        global x1
        global y1

        """
        x1=float(input('Digite la coordenada X1: '))
        y1=float(input('Digite la coordenada Y1: '))
        x2=float(input('Digite la coordenada X2: '))
        y2=float(input('Digite la coordenada Y2: '))
        """
        x1=2161.421
        y1=1115.933
        x2=2160.644
        y2=1148.983
        dx = x2 -x1
        dy = y2-y1
        distancia_2d = m.sqrt(dx**2+dy**2)
        get_sign = lambda x: 1 if x>0 else -1 if x<0 else 0
        dx_sign = get_sign(dx)
        dy_sign = get_sign(dy)
        bearing = 'No es posible determinar el azimut'
        if dy_sign!=0:
            bearing= m.degrees(m.atan(dx/dy))
            if dx_sign==1:
                if dy_sign ==1:
                    cardinal_point=['N','E',0]
                else:
                    cardinal_point=['S','E',180]
            elif dx_sign==-1:
                if dy_sign==1:
                    cardinal_point=['N','W',360] 
                else:
                    cardinal_point=['S','W',180]
            else:
                if dy_sign==1:
                    cardinal_point=['N', '',0]
                else:
                    cardinal_point=['S', '',180]
        else:
            if dx_sign==1:
                cardinal_point=['E', '',90]
            elif dx_sign ==-1:
                cardinal_point=['W', '',270]
            else:
                cardinal_point=['', '','']
        self.polar_result=[bearing,cardinal_point, distancia_2d]
        return self.polar_result
    
    def azimut_ini(self,rumbo):
        azimut_inicial=rumbo[1][2]+rumbo[0]
        self.azimut=azimut_inicial
        return self.azimut
        
    def azimut_adyacente(self,azimut,angulo):
        azimut+=angulo

        if azimut>360:
            azimut-=360
        else:
            azimut=azimut
        
        contAzimut=azimut+180

        if contAzimut>360:
            contAzimut-=360
        else:
            contAzimut=contAzimut

        self.azimut=[azimut,contAzimut]

        return self.azimut
    def azimut_and_contra(self,azimut_inicial,ang_corr_list):
        azimut=[]
        contraAzimut=[azimut_inicial]
        lista=0
        for angulo in ang_corr_list:
            while lista!=len(ang_corr_list):
                azimut_ady= self.azimut_adyacente(contraAzimut[lista],angulo)
                lista+=1
                azimut.append(azimut_ady[0])
                contraAzimut.append(azimut_ady[1])
                break
        self.azimut_corr=[azimut,contraAzimut,azimut[:-1]]
        return self.azimut_corr

    def proy(self,azimut,dist):
        proy_y=((m.cos(m.radians(azimut))))*dist
        proy_x=((m.sin(m.radians(azimut))))*dist
        self.coord=[proy_y,proy_x]
        return self.coord
    
    def coord_list(self,azimut_corr,dist_list):
        coord_list=[]
        centinela=0
        for azimut in azimut_corr:
            while centinela!=len(azimut_corr):
                coord_px_py=self.proy(azimut,dist_list[centinela])
                coord_list.append(coord_px_py)
                centinela+=1
                break
        self.coord_list=coord_list
        return coord_list
    

    def suma_coord(self,coord,azimut_corr):

        sumacoord_y=0
        centinela=0
        index=0
        for coordenada in coord:
            while centinela!=len(azimut_corr):
                sumacoord_y+=coordenada[index]
                centinela+=1
                break
        
        sumacoord_x=0
        centinela=0
        index=1
        for coordenada in coord:
            while centinela!=len(azimut_corr):
                sumacoord_x+=coordenada[index]
                centinela+=1
                break

        self.suma_coord=[sumacoord_y,sumacoord_x]
        return self.suma_coord

    def error_dist_suma_dist_precision(self,suma_coord):

        error_dist=m.sqrt(m.pow(suma_coord[0],2) + m.pow(suma_coord[1],2))
        
        suma_dist=0
        for dist in dist_list:
            suma_dist+=dist
            
        precision=suma_dist/error_dist

        if precision<=9000:
            print("Devuelvase a campo mi papá, la precisión es de "+str(precision))
            quit()
        self.error_dist_suma_dist_precision=[error_dist,suma_dist,precision]
        return self.error_dist_suma_dist_precision

    def corr_error_proy(self,error, list_dist, suma_dist,centinela):
        if error>0:
            corr_error=-(list_dist[centinela]*error)/suma_dist
        if error<0:
            corr_error=(list_dist[centinela]*abs(error))/suma_dist
        self.corr_error=corr_error
        return self.corr_error

    def corr_proyecciones(self,list_coord,suma_coord,list_dist):
        suma_dist=0
        for dist in dist_list:
            suma_dist+=dist

        suma_proy_y_corr=0
        list_proy_y_corr=[]
        corr_error_y=[]
        centinela=0
        index=0
        for proy_y in list_coord:
            while centinela!=len(list_coord):
                error_proy_y=self.corr_error_proy(suma_coord[index],list_dist,suma_dist,centinela)
                corr_error_y.append(round(error_proy_y,3))
                proy_y_corr=proy_y[index]+error_proy_y
                list_proy_y_corr.append(proy_y_corr)
                suma_proy_y_corr+=proy_y_corr
                centinela+=1
                break
        suma_proy_y_corr=round(suma_proy_y_corr,3)


        suma_proy_x_corr=0
        list_proy_x_corr=[]
        corr_error_x=[]
        centinela=0
        index=1       
        for proy_x in list_coord:
            while centinela!=len(list_coord):
                error_proy_x=self.corr_error_proy(suma_coord[index],list_dist,suma_dist,centinela)
                corr_error_x.append(round(error_proy_x,3))
                proy_x_corr=proy_x[index]+error_proy_x
                list_proy_x_corr.append(proy_x_corr)
                suma_proy_x_corr+=proy_x_corr
                centinela+=1
                break
        suma_proy_x_corr=round(suma_proy_x_corr,3)
                
        self.corr_proyecciones=[list_proy_y_corr,list_proy_x_corr,corr_error_y,corr_error_x , suma_proy_y_corr,suma_proy_x_corr]
        return self.corr_proyecciones
    def coordenadas(self,list_proy_corr):

        list_coord_y=[y1]
        contador=0
        for coord in list_proy_corr[0]:
            coord_y=list_coord_y[contador]+coord
            contador+=1
            list_coord_y.append(round(coord_y,3))


        list_coord_x=[x1]
        contador=0
        for coord in list_proy_corr[1]:
            coord_x=list_coord_x[contador]+coord
            contador+=1
            list_coord_x.append(round(coord_x,3))
        
        self.coord_finales=[list_coord_y,list_coord_x]
        return self.coord_finales

    #Funciones Datafream
    def pd_list_ang(self,ang_list_df_final):

        list_ang=[]
        for ang in ang_list_df_final:
            angulo=self.gms_angle_to_decimals(ang)
            angulo_gms=self.decimal_angle_to_gms(angulo)
            list_ang.append(angulo_gms)

        self.list=list_ang
        return self.list

    def pd_list_corr(self,ang_list_df_final,corr_error):

        list_corr_df_final=[]
        for ang in ang_list_df_final:
            if ang!=0:
                correcion=self.decimal_angle_to_gms(corr_error)
                list_corr_df_final.append(correcion)
            else:
                list_corr_df_final.append('NaN')

        self.ang_corr=list_corr_df_final
        return self.ang_corr

    def pd_list_ang_corr(self,suma_and_list_ang):

        list_ang_corr_df_final=[]
        contador=0
        while contador!=len(suma_and_list_ang[1]):
            list_ang_corr_df_final.append('NaN')
            angulo_gms=self.decimal_angle_to_gms(suma_and_list_ang[1][contador])
            list_ang_corr_df_final.append(angulo_gms)
            contador+=1

        self.list=list_ang_corr_df_final
        return self.list

    def pd_list_azimut(self,azimut_corr):

        list_azimut_df_final=[]
        contador=0
        while contador!=len(azimut_corr[0]):
            contra_azimut=self.decimal_angle_to_gms(azimut_corr[1][contador])
            list_azimut_df_final.append(contra_azimut)
            azimut=self.decimal_angle_to_gms(azimut_corr[0][contador])
            list_azimut_df_final.append(azimut)
            contador+=1

        self.list=list_azimut_df_final
        return self.list
    def agregar_nan(self,list1,list2,list3):

        contador=len(list1)
        while len(list1)!=len(list2):
            list3.append('NaN')
            contador+=1
        self.list=list3
        return self.list

    def pd_list_proyeccionesN(self,list_coord,ang_list_df_final):

        list_proyecciones_N=[]
        contador=0
        while contador!=len(list_coord):
            list_proyecciones_N.append('NaN')
            list_proyecciones_N.append(round(list_coord[contador][0],3))
            contador+=1

        self.list_nan=self.agregar_nan(list_proyecciones_N, ang_list_df_final,list_proyecciones_N)
        return self.list_nan

    def pd_list_proyeccionesE(self,list_coord,ang_list_df_final):

        list_proyecciones_E=[]
        contador=0
        while contador!=len(list_coord):
            list_proyecciones_E.append('NaN')
            list_proyecciones_E.append(round(list_coord[contador][1],3))
            contador+=1

        self.list_nan=self.agregar_nan(list_proyecciones_E, ang_list_df_final,list_proyecciones_E)
        return self.list_nan

    def pd_list_corr_proy_y(self,list_proy_corr,ang_list_df_final):

        list_corr_y=[]
        contador=0
        index=2
        while contador!=len(list_proy_corr[2]):
            list_corr_y.append('NaN')
            list_corr_y.append(list_proy_corr[index][contador])
            contador+=1
            
        self.list_nan=self.agregar_nan(list_corr_y, ang_list_df_final,list_corr_y)
        return self.list_nan

    def pd_list_corr_proy_x(self, list_proy_corr,ang_list_df_final):

        list_corr_x=[]
        contador=0
        index=3
        while contador!=len(list_proy_corr[2]):
            list_corr_x.append('NaN')
            list_corr_x.append(list_proy_corr[index][contador])
            contador+=1

        self.list_nan=self.agregar_nan(list_corr_x, ang_list_df_final,list_corr_x)
        return self.list_nan
    
    def pd_list_coord_proy_y(self,coordenadas_finales):

        coordenadas_y=[]
        contador=0
        index=0
        while contador!=len(coordenadas_finales[index]):
            coordenadas_y.append('NaN')
            coordenadas_y.append(coordenadas_finales[index][contador])
            contador+=1

        self.list_nan=coordenadas_y
        return self.list_nan

    def pd_list_coord_proy_x(self,coordenadas_finales):

        coordenadas_x=[]
        contador=0
        index=1
        while contador!=len(coordenadas_finales[index]):
            coordenadas_x.append('NaN')
            coordenadas_x.append(coordenadas_finales[index][contador])
            contador+=1

        self.list_nan=coordenadas_x
        return self.list_nan

    def pd_list_parametros_ang(self, suma_ang,error_ang, error_per, corr_error):
        suma_obs=self.decimal_angle_to_gms(suma_ang)
        suma_teo=self.decimal_angle_to_gms(error_ang[1])
        error_ang=self.decimal_angle_to_gms(error_ang[0])
        corr=self.decimal_angle_to_gms(corr_error)
        list_parametros_ang=[suma_obs, suma_teo,error_ang,error_per,corr]
        self.list_parametros_ang=list_parametros_ang
        return self.list_parametros_ang

    def pd_list_parametros_proyecciones(self, error_dist_suma_dist_precision,suma_coord):
        list_parametros_proyecciones=[error_dist_suma_dist_precision[1],suma_coord[0],suma_coord[1],error_dist_suma_dist_precision[0],error_dist_suma_dist_precision[2]]
        self.list_parametros_proyecciones=list_parametros_proyecciones
        return self.list_parametros_proyecciones
def main():
    info_topo =Topoutils()

    suma_ang=info_topo.suma_ang(angulos_list)

    error_ang=info_topo.error_angular(suma_ang)

    error_per=info_topo.error_per(error_ang)

    corr_error=info_topo.correccion_error(error_ang[0])

    suma_and_list_ang=info_topo.suma_and_corr_ang(angulos_list,corr_error)
    
    rumbo=info_topo.bearing_and_distance()

    azimut_inicial=info_topo.azimut_ini(rumbo)

    azimut_corr=info_topo.azimut_and_contra(azimut_inicial, suma_and_list_ang[1])

    list_coord=info_topo.coord_list(azimut_corr[2],dist_list)
    
    suma_coord=info_topo.suma_coord(list_coord,azimut_corr)

    error_dist_suma_dist_precision=info_topo.error_dist_suma_dist_precision(suma_coord)

    list_proy_corr=info_topo.corr_proyecciones(list_coord,suma_coord,dist_list)

    coordenadas_finales=info_topo.coordenadas(list_proy_corr)



    #Funciones para datafream

    list_ang=info_topo.pd_list_ang(ang_list_df_final)

    list_corr_df_final=info_topo.pd_list_corr(ang_list_df_final,corr_error)
        
    list_ang_corr_df_final=info_topo.pd_list_ang_corr(suma_and_list_ang)

    list_azimut_df_final=info_topo.pd_list_azimut(azimut_corr)
    
    list_proyecciones_N=info_topo.pd_list_proyeccionesN(list_coord,ang_list_df_final)

    list_proyecciones_E=info_topo.pd_list_proyeccionesE(list_coord,ang_list_df_final)

    list_corr_y=info_topo.pd_list_corr_proy_y(list_proy_corr,ang_list_df_final)

    list_corr_x=info_topo.pd_list_corr_proy_x(list_proy_corr,ang_list_df_final)

    coordenadas_y=info_topo.pd_list_coord_proy_y(coordenadas_finales)

    coordenadas_x=info_topo.pd_list_coord_proy_x(coordenadas_finales)

    list_parametros_ang2=info_topo.pd_list_parametros_ang(suma_ang, error_ang,error_per,corr_error)

    list_parametros_proyecciones2=info_topo.pd_list_parametros_proyecciones(error_dist_suma_dist_precision,suma_coord)
        
    dic_pol={
        u'\u0394':deltas_list,
        u'\u03bf':puntos_list,
        'Ang.Obs(GGGMMSS)':list_ang,
        'Corr(GGGMMSS)':list_corr_df_final,
        'Ang.corr(GGGMMSS)':list_ang_corr_df_final,
        'Azimut(GGGMMSS)':list_azimut_df_final,
        'Dist':dist_list_df_final,
        'Proy Y':list_proyecciones_N,
        'Proy X':list_proyecciones_E
        }

    dic_2_pol={
        'Proy Y':list_proyecciones_N,
        'Proy X':list_proyecciones_E,
        'Corr Y':list_corr_y,
        'Corr X':list_corr_x,
        'Coord N':coordenadas_y,
        'Coord E':coordenadas_x
        }

    dic_3_pol={
        '':list_parametros_ang,
        ' ':list_parametros_ang2,
        '  ':list_parametros_proyecciones,
        '   ':list_parametros_proyecciones2,
        }

    df_pol=pd.DataFrame(dic_pol)
    df_pol=df_pol.replace("NaN"," ")
    df_pol=df_pol.fillna(" ")

    df_pol2=pd.DataFrame(dic_2_pol)
    df_pol2=df_pol2.replace("NaN"," ")
    df_pol2=df_pol2.fillna(" ")

    df_pol3=pd.DataFrame(dic_3_pol)
    df_pol3=df_pol3.replace("NaN"," ")
    df_pol3=df_pol3.fillna(" ")

    #ruta=input("Ingrese la ruta en la que quiere que se guarde el xlsx: \n")
    ruta=r"C:\Users\leoda\Desktop\Materias U\Materias 5 semestre\Ing de software\proyecto_ing_software"
    writer= pd.ExcelWriter(ruta+r'\Pol_rtas.xlsx')
    df_pol.to_excel(writer, sheet_name='Proyecciones', index=False)
    df_pol2.to_excel(writer, sheet_name='Coordenadas', index=False)
    df_pol3.to_excel(writer, sheet_name='Parametros Pol', index=False)
    writer.save()


if __name__ == main():
    main()