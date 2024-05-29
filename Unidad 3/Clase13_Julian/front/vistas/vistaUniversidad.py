import tkinter as tk
from tkinter import messagebox
import re
import requests
import sys
sys.path.append("Controladores")
from controladores.validaciones import Validaciones
from controladores.peticiones import Peticiones
from controladores.validaciones import Validaciones
from functools import partial
from tkinter import ttk
from vistas.tabla import Tabla
from controladores import peticiones


validaciones = Validaciones()

def mostrarInterfaz():
    titulos = ['Identificador', 'Docente', 'Estudiante', 'Salón', 'Local']
    columnas = ['id', 'docente', 'estudiante', 'salon', 'local']
    data = []

    # Crear la ventana principal
    principal = tk.Tk()
    principal.title("Vista Universidad")
    principal.geometry("1000x800")

    # Crear la instancia de Peticiones y Tabla
    peticiones = Peticiones()
    tabla = Tabla(principal, titulos, columnas, data)

    def actualizar_tabla():
        # Obtener los datos de la API y actualizar la tabla
        parametros_busqueda = {}  # Puedes agregar parámetros específicos si los necesitas
        resultado = peticiones.buscar(parametros_busqueda)
        if resultado is not None:
            data = []
            for elemento in resultado:
                data.append((
                    elemento.get('id'),
                    elemento.get('docente'),
                    elemento.get('estudiante'),
                    elemento.get('salon'),
                    elemento.get('local')
                ))
            tabla.refrescar(data)

    # Botón para actualizar la tabla
    

    

    # Funcion para la peticion de ingresar universidad
    def peticion_ingresar_universidad():
        Peticiones.ingresar_universidad(txtDocente, txtEstudiante, txtSalon, txtLocal)

    # Funcion para el boton de buscar
    def accion_buscar_boton(txtDocente, txtEstudiante, txtSalon, txtLocal, txtId, tabla):
        datos = {
            "docente": txtDocente.get(),
            "estudiante": txtEstudiante.get(),
            "salon": txtSalon.get(),
            "local": txtLocal.get(),
            "id": txtId.get()
        }
        resultados = Peticiones.buscar(datos)
        if resultados is not None:
            data = []
            for elemento in resultados:
                data.append((elemento.get('id'), elemento.get('docente'), elemento.get('estudiante'), elemento.get('salon'), elemento.get('local')))
            tabla.refrescar(data)

    def seleccionar_elemento(_):
            for i in tabla.tabla.selection():
                valores = tabla.tabla.item(i)['values']
                txtId.delete(0, tk.END)
                txtId.insert(0, str(valores[0]))
                txtDocente.delete(0, tk.END)
                txtDocente.insert(0, str(valores[1]))
                txtEstudiante.delete(0, tk.END)
                txtEstudiante.insert(0, str(valores[2]))
                txtSalon.delete(0, tk.END)
                txtSalon.insert(0, str(valores[3]))
                txtLocal.delete(0, tk.END)
                txtLocal.insert(0, str(valores[4]))

    '''def borrar_elemento(_):
            for i in tabla.tabla.selection():
                Peticiones.eliminar(tabla.tabla.item(i)['values'][0])
                tabla.tabla.delete(i)'''
    def borrar_elemento(event):
        for i in tabla.tabla.selection():
            id = tabla.tabla.item(i)['values'][0]
            print(f"Attempting to delete ID: {id}")  # Imprime el ID que se está intentando eliminar
            status_code = Peticiones.eliminar(id)
            if status_code == 200:
                tabla.tabla.delete(i)
            else:
                messagebox.showerror("Error", f"Error al eliminar universidad con ID {id}")

    frame = tk.Frame(principal, padx=10, pady=10)
    frame.pack(padx=10, pady=10)

    lblTitulo = tk.Label(frame, text='Ingresar Datos')
    lblTitulo.grid(row=0, column=0, columnspan=2) 

    lblDocente = tk.Label(frame, text='Docente:')
    lblDocente.grid(row=1, column=0, padx=5, pady=5)  
    lblEstudiante = tk.Label(frame, text='Estudiante:')
    lblEstudiante.grid(row=3, column=0, padx=5, pady=5)
    lblSalon = tk.Label(frame, text='Salón:')
    lblSalon.grid(row=5, column=0, padx=5, pady=5)
    lblLocal = tk.Label(frame, text='Local:')
    lblLocal.grid(row=7, column=0, padx=5, pady=5)
    lblConsulta = tk.Label(frame)
    lblConsulta.grid(row=11, column=1, columnspan=2)

    txtDocente = tk.Entry(frame, width=20)
    txtDocente.grid(row=1, column=1, padx=5, pady=5)
    txtDocente.lblAdvertencia = tk.Label(frame, text='Solo se permiten letras', fg="red")
    txtDocente.lblAdvertencia.grid(row=2, column=1, sticky="w")
    txtDocente.lblAdvertencia.grid_remove()

    txtEstudiante = tk.Entry(frame, width=20)
    txtEstudiante.grid(row=3, column=1, padx=5, pady=5)
    txtEstudiante.lblAdvertencia1 = tk.Label(frame, text='Solo se permiten letras', fg="red")
    txtEstudiante.lblAdvertencia1.grid(row=4, column=1, sticky="w")
    txtEstudiante.lblAdvertencia1.grid_remove()

    txtSalon = tk.Entry(frame, width=20)
    txtSalon.grid(row=5, column=1, padx=5, pady=5)
    txtSalon.lblAdvertencia = tk.Label(frame, text='Solo se permiten Numeros-Letras', fg="red")
    txtSalon.lblAdvertencia.grid(row=6, column=1, sticky="w")
    txtSalon.lblAdvertencia.grid_remove()

    txtLocal = tk.Entry(frame, width=20)
    txtLocal.grid(row=7, column=1, padx=5, pady=5)
    txtLocal.lblAdvertencia = tk.Label(frame, text='Solo se permiten Numeros-Letras', fg="red")
    txtLocal.lblAdvertencia.grid(row=8, column=1, sticky="w")
    txtLocal.lblAdvertencia.grid_remove()

    btnIngresar = tk.Button(frame, text='Ingresar', command=peticion_ingresar_universidad)
    btnIngresar.grid(row=12, column=1, columnspan=2)

    lblId = tk.Label(frame, text='ID:')
    lblId.grid(row=9, column=0, padx=5, pady=5)

    txtId = tk.Entry(frame, width=20)
    txtId.grid(row=9, column=1, padx=5, pady=5)

    btnConsultar = tk.Button(frame, text='Consultar', command=partial(Peticiones.accion_consultar_boton, txtId, lblConsulta))
    btnConsultar.grid(row=13, column=1, columnspan=2)

    btnConsultarTodos = tk.Button(frame, text='Consultar Todos', command=partial(accion_buscar_boton, txtDocente, txtEstudiante, txtSalon, txtLocal, txtId, tabla))
    btnConsultarTodos.grid(row=14, column=1, columnspan=2)

    boton_actualizar = tk.Button(principal, text="Actualizar", command=actualizar_tabla)
    boton_actualizar.pack(pady=10)

    #Mostrar la tabla
    tabla.tabla.pack(fill=tk.BOTH, expand=True)

    #tabla.bind('<<TreeviewSelect>>', seleccionar_elemento)
    tabla.tabla.bind('<<TreeviewSelect>>', seleccionar_elemento)
    tabla.tabla.bind('<Delete>', borrar_elemento)

    txtDocente.bind('<KeyRelease>', Validaciones.mostrar_advertencia)
    txtEstudiante.bind('<KeyRelease>', Validaciones.mostrar_advertencia1)
    txtSalon.bind('<KeyRelease>', Validaciones.mostrar_advertencia_salon)
    txtLocal.bind('<KeyRelease>', Validaciones.mostrar_advertencia_local)

    principal.mainloop()

# Ejecutar la interfaz
if __name__ == "__main__":
    mostrarInterfaz()