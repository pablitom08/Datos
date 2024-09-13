import tkinter as tk
from tkinter import *
from tkinter import ttk, Text, Label, Menu, messagebox
from threading import Thread
from tkinter import filedialog
import serial.tools.list_ports
import os

import time
from datetime import datetime
import getpass
from tkinter import messagebox, ttk
from tkinter import filedialog

from threading import Thread, Event
import test_serial
import pystray
from PIL import Image

from cryptography.fernet import Fernet
import win32api
import win32file
import win32con


cnx = test_serial.RCTest()
directorio=""

# Establecer la carpeta predeterminada
username = getpass.getuser()
default_folder2 = os.path.join('C:', os.sep, 'Users', username, 'Documents', 'TecniloggerV2','Image')
dirpswd=getpass.getuser()
ruta_archivospswd = f"C:/Users/{dirpswd}/Documents/TecniloggerV2/Logs/pswdc.txt"
apoyodir=getpass.getuser()
actual ="C:/Users/"+apoyodir+"/Documents/TecniloggerV2/Informes"

puerto=0
sbaudios=0
paridad=0
contraseña_verificada = False


cuadroTexto2 = None  # Asignar más tarde en la inicialización de la GUI
lista_desplegable = StringVar()
lista_desplegable1 = StringVar()
lista_desplegable2 = StringVar()
lista_desplegable3 = StringVar()
lista_desplegable4 = StringVar()
lista_desplegable5 = StringVar()  # Asumido que es un StringVar para directorio

# Función para verificar la contraseña
def verificar_contraseña():
    global contraseña_verificada
    contraseña = entry_contraseña.get()
    with open(ruta_archivospswd, "r") as f:
        contraseña_guardada = f.read().strip()
    
    if contraseña == contraseña_guardada:
        contraseña_verificada = True  # Marcamos que la contraseña ha sido verificada
        notebook.select(1)  # Cambia a la pestaña de configuración
        top.destroy()  # Cierra la ventana emergente
    else:
        messagebox.showerror("Error", "Contraseña incorrecta")  # Muestra un error si la contraseña es incorrecta



# Función para pedir contraseña al intentar acceder a la configuración
def pedir_contraseña():
    global top, entry_contraseña
    top = tk.Toplevel()  # Ventana emergente
    top.title("Ingrese la contraseña")

    label = tk.Label(top, text="Contraseña:", font=('Classic Robot', 9))
    label.pack(pady=5)
    
    # tk.Label(top, text="Contraseña:").pack(pady=5).font=('Classic Robot',12)


    entry_contraseña = tk.Entry(top, show="*", width=10)  # Campo de entrada de la contraseña
    entry_contraseña.pack(pady=5)
    top.iconbitmap("tecni.ico")
    
    button = tk.Button(top, text="Aceptar", command=verificar_contraseña,font=('Classic Robot',10), relief=RAISED, borderwidth=5)
    button.pack(pady=5)


stop_threads = Event()  # Evento para controlar la ejecución de hilos
# funcion para confirmar la salida del sistema
def confirmar_salida():
    respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas salir?")
    if respuesta:
        stop_threads.set()  # Indica a los hilos que deben detenerse
        raiz.quit()


# Función para gestionar el cambio de pestaña
def on_tab_change(event):
    global contraseña_verificada
    
    selected_tab = notebook.index("current")
    
    # Si la pestaña seleccionada es la de configuración (índice 1)
    if selected_tab == 1 and not contraseña_verificada:
        notebook.select(0)  # Regresa inmediatamente a la pestaña de visualización
        pedir_contraseña()  # Llama a la función para pedir la contraseña


# Conexion con la comunicacion serial
def conexion():
    time.sleep(1)
    puerto  = lista_desplegable.get()
    baudios = lista_desplegable1.get()
    tambyte = lista_desplegable2.get()
    paridad = lista_desplegable3.get()
    bitpar  = lista_desplegable4.get()
    apoyodir=getpass.getuser()
    actual ="C:/Users/"+apoyodir+"/Documents/TecniloggerV2/Informes"

    if puerto!="" and baudios!= "" and tambyte!= "" and paridad!= "" and bitpar!= "":
        botonenvio['state'] = DISABLED
        estado=1
        print("El Serial:",puerto+","+baudios+","+tambyte+","+paridad+","+bitpar)
        # cuadroTexto2=Label(tab1, bg="white", text="      ")
        # cuadroTexto2.place(x=150, y=410)
        # cuadroTexto2=Label(tab1, bg="white", text="  CONECTADO    ",font=('Classic Robot', 17), fg="green")
        # cuadroTexto2.place(x=103, y=410)

        if os.path.exists(directorio):
            data1 = cnx.steer(puerto,baudios,8,paridad, 1, directorio, areaTexto)
        elif not os.path.exists(directorio):
            data1 = cnx.steer(puerto,baudios,8,paridad, 1, actual, areaTexto)
        else:
            messagebox.showwarning('Mensaje','NO HA INGRESADO UN DIRECTORIO DONDE ALMACENAR EL ARCHIVO!!')
            print("The path is either for a file or not valid")  
    else:
        botonenvio['state']==NORMAL
        messagebox.showwarning('Mensaje','Debe llenar todos los campos de configuración')

# Desconexion con la comunicacion serial
def desconexion():
    time.sleep(1)
    cnx.cerrar()
    if botonsalir['state']==NORMAL:
        botonenvio['state'] = NORMAL
        # cuadroTexto2=Label(miFrame, bg="white", text="")
        # cuadroTexto2.place(x=150, y=360)
        # cuadroTexto2=Label(miFrame, bg="white", text="NO CONECTADO", font=('Classic Robot', 17), fg="red")
        # cuadroTexto2.place(x=100, y=410)
        stop_threads.set()  # Indica a los hilos que deben detenerse


def codigoBoton():
    # # conexion()formatted_data = self.format_data(Hour_time, datos).strip()
    global hilo1
    hilo1=Thread(target=conexion)
    hilo1.daemon = True 
    hilo1.start()

def codigoBoton2():
    desconexion()

def carpeta(tab2):
    global directorio, actual
    directorio=filedialog.askdirectory()
    nombre_directorio = os.path.basename(directorio)
    cuadroTexto2=Label(tab2, text="                                                                   ",font=('Classic Robot',12))
    cuadroTexto2.place(x=160, y=330)
    time.sleep(1)
    cuadroTexto2=Label(tab2, text=nombre_directorio,font=('Classic Robot',12))
    cuadroTexto2.place(x=170, y=330)
    if directorio!="":
        os.chdir(directorio)


def encontrar_puertos_serial():
    """Función para listar los puertos seriales disponibles."""
    puertos = serial.tools.list_ports.comports()
    puertos_disponibles = [puerto.device for puerto in puertos]
    return puertos_disponibles

def actualizar_puertos():
    """Función para actualizar la lista de puertos en la lista desplegable."""
    puertos = encontrar_puertos_serial()
    if puertos:
        lista_desplegable['values'] = puertos
        lista_desplegable.set(puertos[0])  # Seleccionar el primero automáticamente
    else:
        lista_desplegable['values'] = ["No hay puertos"]
        lista_desplegable.set("No hay puertos")

import json

def codigoSave():
    global directorio, cuadroTexto2 
    config = {
        'puerto': lista_desplegable.get(),
        'baud': lista_desplegable1.get(),
        'tam_datos': lista_desplegable2.get(),
        'paridad': lista_desplegable3.get(),
        'bits_parada': lista_desplegable4.get(),
        'directorio': actual  # Añade la ruta del directorio aquí
    }
    
    with open('configuracion.json', 'w') as f:
        json.dump(config, f, indent=4)

    cuadroTexto2.config(text=os.path.basename(actual))


def cargar_configuracion():
    global directorio, cuadroTexto2 
    try:
        with open('configuracion.json', 'r') as f:
            config = json.load(f)
        
        lista_desplegable.set(config.get('puerto', 'COM4'))
        lista_desplegable1.set(config.get('baud', '9600'))
        lista_desplegable2.set(config.get('tam_datos', '8'))
        lista_desplegable3.set(config.get('paridad', 'N'))
        lista_desplegable4.set(config.get('bits_parada', '1'))

        directorio = config.get('directorio', actual)  # Usa la ruta guardada o una cadena vacía si no hay
        if directorio:
            lista_desplegable5.set(directorio)  # Mostrar la ruta en el desplegable si es necesario
            cuadroTexto2.config(text=os.path.basename(directorio))  # Mostrar la ruta del directorio
        else:
            cuadroTexto2.config(text="No hay directorio seleccionado")  # Texto por defecto si no hay ruta guardada
    except FileNotFoundError:
        # Si no hay archivo de configuración, usamos valores por defecto
        cuadroTexto2.config(text="No hay directorio seleccionado")  # Texto por defecto si no se encuentra el archivo


# CODIGO PARA LA LICENCIA
def find_drives():
    drives = []
    for drive in win32api.GetLogicalDriveStrings().split('\000')[:-1]:
        if win32file.GetDriveType(drive) == win32con.DRIVE_REMOVABLE:
            drives.append(drive)
    return drives

def find_license_file(drives):
    for drive in drives:
        license_path = os.path.join(drive, 'license.lic')
        key_path = os.path.join(drive, 'license_key.key')
        if os.path.exists(license_path) and os.path.exists(key_path):
            return drive  # Retorna la unidad que contiene los archivos
    return None

def read_and_verify_license(license_path, key_path):
    with open(key_path, 'rb') as key_file:
        key = key_file.read()
    cipher = Fernet(key)
    with open(license_path, 'rb') as license_file:
        encrypted_token = license_file.read()
        token = cipher.decrypt(encrypted_token)
        return token.decode()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("USB License Monitor")
        self.label = tk.Label(root, text="TECNILOGGER CANDADO")
        self.label.pack(pady=20)
        self.license_valid = False

    def update_label_on_extraction(self):
        self.label.config(text="Se ha extraído la licencia.")
        self.show_message("Se ha extraído la licencia, el programa se cerrara.")
        self.root.destroy()  # Opcional: cerrar la aplicación


    def show_message(self, message):
        messagebox.showwarning("Advertencia", message)


def initial_license_check():
    """ Verifica la presencia inicial de la licencia """
    drives = find_drives()
    license_folder = find_license_file(drives)

    valid_license_numbers = ["137982", "397125", "123456", "456789"]
    
    if license_folder:
        license_path = os.path.join(license_folder, 'license.lic')
        key_path = os.path.join(license_folder, 'license_key.key')
        
        # return read_and_verify_license(license_path, key_path) == "137982"
        for license_number in valid_license_numbers:
            if read_and_verify_license(license_path, key_path) == license_number:
                return True
    return False

def monitor_license():
    """ Monitorea continuamente la presencia de la licencia """
    while True:
        if not initial_license_check():
            # desconexion()
            messagebox.showerror("Error de Licencia", "Licencia extraída. El programa se cerrará.")

            raiz.after(500, raiz.destroy)
            break
        time.sleep(3)


def main():
    global hilo1, raiz, miFrame, areaTexto, context_menu, tab1, tb2
    global lista_desplegable, lista_desplegable1, lista_desplegable2, lista_desplegable3, lista_desplegable4
    global botonenvio, botonsalir, hilo2, stop_threads, notebook,cuadroTexto2  

    ########## Entradas
    raiz = tk.Tk()   
    raiz.title("Software de Captura de datos")
    raiz.geometry("500x450")  # Ajustamos el tamaño de la ventana a 500x450
    raiz.resizable(0, 0)  # ancho, alto de tipo booleano, sirve para redimensionar
    raiz.iconbitmap("tecni.ico")

    # Crear el contenedor de pestañas
    notebook = ttk.Notebook(raiz)
    notebook.pack(expand=True, fill='both')

    style = ttk.Style()
    style.configure('TNotebook.Tab', font=('Classic Robot', 10), padding=[10, 5], 
                foreground='blue', background='lightgray', borderwidth=5)


    style.map('TNotebook.Tab', background=[('selected', 'black')], 
          expand=[('selected', [3, 3, 3, 3])])  # Ajuste para relieve

    # Crear el frame de la primera pestaña (Visualización de datos)
    idata = PhotoImage(file=default_folder2+'/'+'idata.png')
    tab1 = ttk.Frame(notebook)
    notebook.add(tab1, text="Datos",image=idata, compound='left')
    tab1.idata = idata
    
    # Crear el frame de la segunda pestaña (Configuración)


    iconfi = PhotoImage(file=default_folder2+'/'+'confi2.png')
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="Configuración", image=iconfi, compound='left')
    tab2.iconfi = iconfi


    # --------- Primera pestaña (Visualización de datos) ---------
    miLabel = tk.Label(tab1, text="TECNILOGGER", font=('Classic Robot', 15))
    miLabel.pack(pady=10)

    # Área de texto para visualizar datos
    label_area = tk.Label(tab1, text="PESO", font=('Classic Robot', 10))
    label_area.pack(pady=5)
    
    areaTexto = Text(tab1, width=30, height=1, font=('Classic Robot', 85), bg='white', fg='blue')
    areaTexto.pack(pady=10)
    areaTexto.config(state=tk.DISABLED)


    botonenvio=Button(tab1, text="Iniciar", command=codigoBoton,state=NORMAL,font=('Classic Robot',12), relief=RAISED, borderwidth=5)
    botonenvio.place(x=100, y=250, width=97)

    botonsalir=Button(tab1, text="Detener", command=codigoBoton2, state=NORMAL,font=('Classic Robot',12), relief=RAISED, borderwidth=5)
    botonsalir.place(x=250, y=250, width=97)



    # --------- Segunda pestaña (Configuración) ---------
    miLabel2 = tk.Label(tab2, text="Parametros de configuracion Serial", font=('Classic Robot', 16))
    miLabel2.grid(row=2, column=2, padx=70, pady=10)


    nombreLabel2 = tk.Label(tab2, text="Puerto", font=('Classic Robot', 12))
    nombreLabel2.place(x=30, y=45)

    # Crear la lista desplegable
    lista_desplegable = ttk.Combobox(tab2, width=8, state="readonly", font=('Classic Robot', 10))
    lista_desplegable.place(x=30, y=70)

        # Botón para actualizar puertos
    iupdate = PhotoImage(file=default_folder2+'/'+'iupdate.png')
    boton_actualizar = Button(tab2, text="Update", image=iupdate, command=actualizar_puertos,font=('Classic Robot',12), relief=RAISED, borderwidth=5,  compound="left")
    boton_actualizar.place(x=140, y=65)
    boton_actualizar.image = iupdate 


    # Llamar a la función de actualización inicialmente para llenar la lista
    actualizar_puertos()

    nombreLabel3 = tk.Label(tab2, text="Baud", font=('Classic Robot', 12))
    nombreLabel3.place(x=30, y=90)

    lista_desplegable1 = ttk.Combobox(tab2, width=8, state="readonly", font=('Classic Robot', 10))
    opciones1 = ["600", "1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"]
    lista_desplegable1['values'] = opciones1
    lista_desplegable1.set("9600")
    lista_desplegable1.place(x=30, y=115)


    nombreLabel3= Label(tab2,text="Tam. datos",font=('Classic Robot',12))
    nombreLabel3.place(x=30, y=140)

    lista_desplegable2 = ttk.Combobox(tab2,width=8, state="readonly",font=('Classic Robot',10))
    opciones2 = ["8","7"] 
    lista_desplegable2['values']=opciones2
    lista_desplegable2.set("8")
    lista_desplegable2.place(x=30, y=165)


    nombreLabel4= Label(tab2, text="Paridad",font=('Classic Robot',12))
    nombreLabel4.place(x=30, y=190)

    lista_desplegable3 = ttk.Combobox(tab2,width=8,state="readonly",font=('Classic Robot',10))
    opciones3 = ["N","E","O"]
    lista_desplegable3['values']=opciones3
    lista_desplegable3.set("N")
    lista_desplegable3.place(x=30, y=215)


    nombreLabel4= Label(tab2, text="BitsP",font=('Classic Robot',12))
    nombreLabel4.place(x=30, y=240)

    lista_desplegable4 = ttk.Combobox(tab2,width=8,state="readonly",font=('Classic Robot',10))
    opciones4 = ["1","2"]
    lista_desplegable4['values']=opciones4
    lista_desplegable4.set("1")
    lista_desplegable4.place(x=30, y=265)

#-------------- para guardar el archivo
    miLabel2= Label(tab2,text="Ruta creacion archivo",font=('Classic Robot',13))
    miLabel2.place(x=30, y=300)

    # fondo = PhotoImage(file=default_folder2+'/'+'LogoTC2.png')

    # botonminimizar=Button(tab2, image=fondo, command=minimize_to_tray,font=('Classic Robot', 10))
    # botonminimizar.place(x=340, y=385)

    # miLabel2= Label(tab2, bg="white",text="Status de conexion",font=('Classic Robot',18))
    # miLabel2.place(x=100, y=385)

    # botondirectorio=Button(tab2, text="seleccionar", command=carpeta, state=NORMAL,font=('Classic Robot',10), relief=RAISED, borderwidth=5)

    icarpeta = PhotoImage(file=default_folder2+'/'+'icarpeta2.png')
    botondirectorio = Button(tab2, text="seleccionar",image=icarpeta, command=lambda: carpeta(tab2), state=tk.NORMAL, font=('Classic Robot', 12), relief=tk.RAISED, borderwidth=5,  compound="left")
    botondirectorio.place(x=30, y=325)
    botondirectorio.image = icarpeta 


    iconosave = PhotoImage(file=default_folder2+'/'+'icosave2.png')
    BotonGuardarC=Button(tab2, text="Grabar", image=iconosave, command=codigoSave, state=NORMAL,font=('Classic Robot',12), relief=RAISED, borderwidth=5,  compound="left")
    BotonGuardarC.place(x=350, y=180, width=100, height=50)
    BotonGuardarC.image = iconosave 


    cuadroTexto2 = Label(tab2, text="", font=('Classic Robot', 12))
    cuadroTexto2.place(x=180, y=330)

    cargar_configuracion()

    # Agregar un evento para pedir la contraseña al intentar cambiar a la pestaña de configuración
    notebook.bind("<<NotebookTabChanged>>", on_tab_change)


    # Archivo de contraseña por defecto (solo si no existe)
    try:
        with open(ruta_archivospswd, "w") as f:
            f.write("7913")  # Contraseña por defecto
    except FileExistsError:
        pass  # Si ya existe, no hacer nada


    # Más opciones de configuración aquí (agregar las demás listas desplegables)


# ------------------------Seccion de codigo para validar la licencia-------------------
    if not initial_license_check():
        messagebox.showerror("Error de Licencia", "No se encontró licencia válida. El programa se cerrará.")
        raiz.after(500, raiz.destroy)
    else:
        hilo_licencia = Thread(target=monitor_license, daemon=True)
        hilo_licencia.start()
# --------------------------------------------------------------------------------------

    # Inicialización de la ventana principal
    raiz.protocol("WM_DELETE_WINDOW", confirmar_salida)
    raiz.mainloop()

if __name__ == "__main__":
    main()
