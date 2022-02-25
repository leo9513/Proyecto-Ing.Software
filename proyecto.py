#Programa para leer archivo excel y devolver valores como una lista

import pandas as pd
import math as m

inputfile=r"C:\Users\leoda\Desktop\Materias U\Materias 5 semestre\Ing de software\proyecto_ing_software\basePolCerrada.xlsx"

df=pd.read_excel(inputfile)

df_datos=df[df['Ang.Obs(GGGMMSS)']!=0]

angulos_list=df_datos['Ang.Obs(GGGMMSS)'].tolist()


dist_list=df_datos['Dist'].tolist()

vertices= len(angulos_list)-1


class Topoutils():
    def gms_angle_to_decimals(self, gms_angle):
        minutes, degree_part = m.modf(gms_angle / 10000)
        seconds, minutes= m.modf(minutes*100)
        seconds *=100

        self.decimal_angle =  degree_part + minutes/60 + seconds /3600
        return self.decimal_angle

    def decimal_angle_to_gms(self, decimal_angle, total_decimals =0):
        minutes, degree_part = m.modf(decimal_angle)
        seconds, minutes = m.modf(minutes*60)

        self.gms_angle= "{}° {}' {}'' ".format(int(degree_part),int(minutes),round(seconds,total_decimals))
        return self.gms_angle

    def suma_ang(self,angulos_list):
        suma=0
        for angulo in angulos_list:
            angulo_decimal = self.gms_angle_to_decimals(angulo)
            suma+=angulo_decimal
        self.suma=suma
        return self.suma

    def error_angular(self,suma_angulo):
        sentido = float(input("digite '1' si la poligonal tiene angulos internos, digite '2' si son externos: \n"))
        if sentido==1:
                angulos_i = suma_angulo
                angulos_it = float((vertices-2)*180+360)
                cierre = float(angulos_i-angulos_it)
        else:
            angulos_e = suma_angulo
            angulos_et = float((vertices+2)*180)
            cierre = float(angulos_e-angulos_et)
        self.cierre=cierre
        return self.cierre   
    
    def correccion_error(self,error):
        if error>0:
            corr_error=-error/(vertices+1)
        if error<0:
            corr_error=abs(error)/(vertices+1)
        self.corr_error=corr_error
        return self.corr_error

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
        x1=float(input('Digite la coordenada X1: '))
        y1=float(input('Digite la coordenada Y1: '))
        x2=float(input('Digite la coordenada X2: '))
        y2=float(input('Digite la coordenada Y2: '))
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
        self.azimut_corr=azimut[:-1]
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

        sumacoord_x=0
        centinela=0
        index=0
        for coordenada in coord:
            while centinela!=len(azimut_corr):
                sumacoord_x+=coordenada[index]
                centinela+=1
                break
        
        sumacoord_y=0
        centinela=0
        index=1
        for coordenada in coord:
            while centinela!=len(azimut_corr):
                sumacoord_y+=coordenada[index]
                centinela+=1
                break

        self.suma_coord=[sumacoord_x,sumacoord_y]
        return self.suma_coord
        

def main():
    info_topo =Topoutils()

    suma_ang=info_topo.suma_ang(angulos_list)

    error_ang=info_topo.error_angular(suma_ang)

    corr_error=info_topo.correccion_error(error_ang)
  
    suma_and_list_ang=info_topo.suma_and_corr_ang(angulos_list,corr_error)
    
    rumbo=info_topo.bearing_and_distance()

    azimut_inicial=info_topo.azimut_ini(rumbo)

    azimut_corr=info_topo.azimut_and_contra(azimut_inicial, suma_and_list_ang[1])
 
    list_coord=info_topo.coord_list(azimut_corr,dist_list)
    
    suma_coord=info_topo.suma_coord(list_coord,azimut_corr)

    
if __name__ == main():
    main()