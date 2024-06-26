import requests
from tkinter import messagebox
#import re
#from controladores import validaciones
#from front.controladores.validaciones import Validaciones
import sys
sys.path.append("controladores")
from Front. Controller.Validaciones import Validaciones
from Front.Views import VistasBafle
import requests
from tkinter import messagebox

class Peticiones():
    url_base  = 'http://127.0.0.1:8000/v1/bafle'
    @staticmethod
    def ingresar_bafle(txtMarca, txtTamaño, txtColor, txtPrecio):
        marca = txtMarca.get()
        tamaño = txtTamaño.get()
        color = txtColor.get()
        precio = txtPrecio.get()

        if not marca or not tamaño or not color or not precio:
            messagebox.showwarning("Error", "Por favor completa todos los campos.")
            return

        if (txtMarca.lblAdvertencia1.winfo_viewable() or
            txtTamaño.lblAdvertencia2.winfo_viewable() or
            txtColor.lblAdvertencia3.winfo_viewable() or
            txtPrecio.lblAdvertencia4.winfo_viewable()):
            messagebox.showwarning("Error", "Por favor completa todos los campos correctamente.")
            return

        data = {
            "marca": marca,
            "tamaño": tamaño,
            "color": color,
            "precio": precio
        }

        url = 'http://127.0.0.1:8000/v1/bafle'

        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                messagebox.showinfo("Éxito", "Bafle creado exitosamente!!")
            else:
                messagebox.showerror("Error", f"Error al crear el bafle: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al conectar con la API: {str(e)}")
  
    @staticmethod
    def Consultar(id):
        try:
            resultado = requests.get('http://127.0.0.1:8000/v1/bafle' + str(id))
            resultado.raise_for_status() 
            return resultado.json()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error al conectar con la API: {str(e)}")
            return None


    @staticmethod
    def Buscar(datos):
        try:
            url = 'http://127.0.0.1:8000/v1/bafle'
            for key, value in datos.items():
                if value:
                    url += f"{key}={value}&"
            
            resultado = requests.get(url)
            resultado.raise_for_status()
            return resultado.json()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error al conectar con la API: {str(e)}")
            return None

    @staticmethod 
    def actualizar(id, marca, tamaño, color, precio):
        try:
            data = {
                'marca': marca,
                'tamaño': tamaño,
                'color': color,
                'precio': precio
            }
            url = f'http://127.0.0.1:8000/v1/bafle/{id}/'
            resultado = requests.put(url, json=data)
            return resultado.status_code
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error al conectar con la API: {str(e)}")
            return None
    
    @staticmethod
    def GuardarBafle_Archivo():
        try:
            resultado = requests.get(Peticiones.url_base)
            resultado.raise_for_status()
            bafles = resultado.json()

            with open('bafle.txt', 'w', encoding='utf-8') as archivo:
                for bafle in bafles:
                    linea = f"ID: {bafle['id']}, Marca: {bafle['marca']}, Tamaño: {bafle['tamaño']}, Color: {bafle['color']}, Precio: {bafle['precio']}\n"
                    archivo.write(linea)
            messagebox.showinfo("Éxito", "Bafle guardado exitosamente en bafle.txt.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error al conectar con la API: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el archivo: {str(e)}")

  
