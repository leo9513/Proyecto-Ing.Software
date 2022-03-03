# Proyecto-Ing.Software
from ast import If
from cProfile import label
from fileinput import close
from pickle import GLOBAL
import tkinter
import sqlite3
from tkinter import*
from tkinter import messagebox
import pymysql
def menu():
      
    global ventanaprincipal
    ventanaprincipal=Tk()
    ventanaprincipal.geometry("400x400")
    ventanaprincipal.title("BIENVENIDO A TOPOAPP")
    ventanaprincipal.iconbitmap(r'C:\Users\Personal\Desktop\TRABAJOFINALINGE\mt.ico')




    imagen = PhotoImage(file = r"C:\Users\Personal\Desktop\TRABAJOFINALINGE\topoga.png")

    ventanaprincipal = Label(image = imagen, text = "fondo")
    ventanaprincipal.place(x = 0, y = 00, relwidth = 1, relheight = 1)
        
    Label(text="INGRESO AL SISTEMA",bg="royal blue",fg="white",width="20",height="2",font=("Consolas",15)).pack()
    Label(text="\n").pack ()
    Label(text="\n").pack ()

    Button(text="INICIAR SESIÓN",height=3,width="30",command= inicio_sesion).pack()
    Label(text="\n").pack ()
    Button(text="REGISTRAR",height=3,width="30",command= regristro).pack()
    
    
    
    ventanaprincipal.mainloop()
   










def inicio_sesion():
    global ventana1
    ventana1= Toplevel(ventanaprincipal)
    ventana1.geometry("400x250")
    ventana1.title("INICIO DE SESIÓN")
    Label(ventana1, text="").pack()
    Button(ventana1,text="INICIAR SESIÓN",height=1,width="15",command=validar).pack()
    Label(ventana1, text="").pack()



    Label(ventana1, text= "POR FAVOR INGRESE SU USUARIO Y CONTRASEÑA",bg="royal blue",fg="white",width="40",height="2",font=("Consolas",8)).pack()
    Label(ventana1, text="").pack()

    global nombreusuario_verificar  
    global contrasenausuario_verificar


    nombreusuario_verificar=StringVar
    contrasenausuario_verificar=StringVar

    global nombre_usuario_entrada
    global contrasena_usuario_entrada

    Label(ventana1, text="Usuario").pack()
    nombre_usuario_entrada=Entry(ventana1, textvariable=nombreusuario_verificar)
    nombre_usuario_entrada.pack()
    Label(ventana1).pack()

    Label(ventana1, text="Contraseña").pack()
    contrasena_usuario_entrada=Entry(ventana1, textvariable=contrasenausuario_verificar)
    contrasena_usuario_entrada.pack()
    Label(ventana1).pack()


def regristro():
    global ventana2
    ventana2= Toplevel (ventanaprincipal)
    ventana2.geometry("400x250")
    ventana2.title("REGISTRO")

    Label(ventana2, text="").pack()
    Label(ventana2, text="").pack()

    global nombreusuario_entrada
    global contrasena_entrada

    nombreusuario_entrada =float()
    contrasena_entrada =float()
    Label(ventana2,text="Por favor ingrese un usuario y contraseña").pack()
    Label(ventana2,text="").pack()
    Label(ventana2, text="Usuario").pack()
    nombreusuario_entry=Entry(ventana2,)
    nombreusuario_entry.pack()
    Label(ventana2).pack()

    Label(ventana2, text="contraseña").pack()
    contrasena_entry=Entry(ventana2)
    contrasena_entry.pack()
    Label(ventana2).pack()
    Button(ventana2,text="registrar",command=ingrese_datos).pack()




def ingrese_datos():
    bd=pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        db="basedatos1"
        )
    fcursor=bd.cursor()
    sql="INSERT INTO login (USUARIO,CONTRASENA) VALUES ('{0}','{1}' ) ".format(nombreusuario_entrada.get(),contrasena_entrada.get())

    try:
        fcursor.execute(sql)
        bd.commit()
        messagebox.showinfo(message="registro exitoso",title="Aviso")
    except:
        bd.rollback()
        messagebox.showinfo(message=" no se registro",title="Aviso")
    bd.close()
   
def validar():
    bd=pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        db="basedatos1"
        )
    fcursor=bd.cursor()
    fcursor.execute("SELECT CONTRASENA FROM login WHERE USUARIO= "+nombreusuario_verificar+" and CONTRASENA = "+contrasenausuario_verificar+ "")
    if fcursor.fetchall():
        messagebox.showinfo(title="inicio de sesion exitoso",message="usuario y contraseña correcta")
    else:
        messagebox.showinfo(title="inicio de sesion fallido",message="usuario o contraseña incorrecta")
    bd.close()






menu()
