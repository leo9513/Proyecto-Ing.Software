from tkinter import messagebox
import pymysql
from tkinter import *
import os



def ventana_inicio():
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

    Button(text="INICIAR SESIÓN",height=3,width="30",command=login).pack()
    Label(text="\n").pack ()
    Button(text="REGISTRAR",height=3,width="30",command=registro).pack()
  
  
  
    ventanaprincipal.mainloop()


def registro():
    global ventana1
    ventana1 = Toplevel(ventanaprincipal)
    ventana1.title("REGISTRO DE USUARIO")
    ventana1.geometry("250x250")
 
    global nomusuario
    global contrasena
    global ingresonombre
    global ingresocontrasena
    nomusuario = StringVar() 
    contrasena = StringVar() 
    Label(ventana1, text="INGRESE DATOS", bg="bisque").pack()
    Label(ventana1, text="").pack()
    nombre1 = Label(ventana1, text="NOMBRE DEL USUARIO  ")
    nombre1.pack()
    ingresonombre = Entry(ventana1, textvariable=nomusuario) 
    ingresonombre.pack()
    etiqueta_clave = Label(ventana1, text="CONTRASEÑA  ")
    etiqueta_clave.pack()
    ingresocontrasena = Entry(ventana1, textvariable=contrasena, show='*') 
    ingresocontrasena.pack()
    Label(ventana1, text="").pack()
    Button(ventana1, text="REGISTRARSE", width=10, height=1, bg="firebrick1", command = registro_usuario).pack() 

def login():
    global ventana_login
    ventana_login = Toplevel(ventanaprincipal)
    ventana_login.title("INGRESO A LA APP")
    ventana_login.geometry("300x250")
    Label(ventana_login, text="INGRESE EL USUARIO Y CONTRASEÑA",bg="bisque").pack()
    Label(ventana_login, text="").pack()
 
    global verificarusuario
    global verificarcontrasena
 
    verificarusuario = StringVar()
    verificarcontrasena = StringVar()
 
    global entrada_login_usuario
    global entrada_login_clave
 
    Label(ventana_login, text=" USUARIO: ").pack()
    entrada_login_usuario = Entry(ventana_login, textvariable=verificarusuario)
    entrada_login_usuario.pack()
    Label(ventana_login, text="").pack()
    Label(ventana_login, text="").pack()
    Label(ventana_login, text="CCONTRASEÑA:  ").pack()
    entrada_login_clave = Entry(ventana_login, textvariable=verificarcontrasena, show= '*')
    entrada_login_clave.pack()
    Label(ventana_login, text="").pack()
    Button(ventana_login, text="INGRESAR", width=10, height=2, command = verificar).pack()



def verificar():
    usuarioverfi = verificarusuario.get()
    contrasenaverifi1 = verificarcontrasena.get()
     
    lista_archivos = os.listdir() 
    if usuarioverfi in lista_archivos:
        archivo1 = open(usuarioverfi, "r") 
        verifica = archivo1.read().splitlines() 
        if contrasenaverifi1 in verifica:
           ingresoexitoso() 
        
        else:
            contrasenamal()
   
    else:
        usuariomal()



 
def ingresoexitoso():
    global ventana_exito
    ventana_exito = Toplevel(ventana_login)
    ventana_exito.title("EXITOSO")
    ventana_exito.geometry("400x400")
    Label(ventana_exito, text="INGRESO  EXITOSO").pack()
    Button(ventana_exito, text="OK").pack()
 

 
def contrasenamal():
    global ventana_no_clave
    ventana_no_clave = Toplevel(ventana_login)
    ventana_no_clave.title("ERROR")
    ventana_no_clave.geometry("400x400")
    Label(ventana_no_clave, text="CONTRASEÑA O USUARIO INCCORECTA ").pack()
    Button(ventana_no_clave, text="OK").pack()
 

 
def usuariomal():
    global ventana_no_usuario
    ventana_no_usuario = Toplevel(ventana_login)
    ventana_no_usuario.title("ERROR")
    ventana_no_usuario.geometry("150x100")
    Label(ventana_no_usuario, text="USUARIO O CONTRASEÑA INCORRECTA").pack()
    Button(ventana_no_usuario, text="OK").pack() 






def registro_usuario():
 
    usuario_info = nomusuario.get()
    clave_info = contrasena.get()
 
    file = open(usuario_info, "w") 
    file.write(usuario_info + "\n")
    file.write(clave_info)
    file.close()
 
    ingresonombre.delete(0, END)
    ingresocontrasena.delete(0, END)
 
    Label(ventana1, text="SE HA REGISTRADO CON EXITO", fg="blue", font=("calibri", 11)).pack()
 
 
ventana_inicio() 
 