from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import uic
import sqlite3


class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()

        # Cargar interfaz de usuario
        uic.loadUi("contactos.ui", self)

        # Conectar a la base de datos
        self.conexion = sqlite3.connect('contactos.db')
        self.cursor = self.conexion.cursor()
        

            
        self.lista_usuario = []
       
        #Oculto los botones de editar(aceptar, cancelar)
        self.botones.hide()

        #Deshabilito los line edit llamando a la funcion
        self.on_of_lineedit(False)
        
        #Deshabilito los botones    
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.aceptar.setEnabled(False)
        self.cancelar.setEnabled(False)
        
        #mostrar texto en line edit
        self.lista.itemClicked.connect(self.on_mostrar)
        
        #Funciones de botones
        self.nuevo.clicked.connect(self.on_nuevo)
        self.aceptar.clicked.connect(self.on_aceptar)
        self.cancelar.clicked.connect(self.on_cancelar)
        self.editar.clicked.connect(self.on_editar)
        self.aceptar_editar.clicked.connect(self.on_aceptar_editar)
        self.cancelar_editar.clicked.connect(self.on_cancelar_editar)
        self.eliminar.clicked.connect(self.on_eliminar)
        
        self.inicio()
        
    def inicio(self):
        #Deshabilito los botones      
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.aceptar.setEnabled(False)
        self.cancelar.setEnabled(False)
        #llamo a la funcion on_cargar para caragr mi base de datos
        self.on_cargar()
            
    def on_cargar(self):
        self.cursor.execute('select * from contactos')
        usuarios = self.cursor.fetchall()
        
        for usuario in usuarios:
            
            #cargo base de datos en lista 
            self.lista.addItem(f'{usuario[0]} |{usuario[1]} | {usuario[2]} | {usuario[3]} | {usuario[4]} | {usuario[5]} | {usuario[6]} | {usuario[7]} | {usuario[8]}')
            
            usuario = {'id':usuario[0],'nombre':usuario[1],'apellido':usuario[2],'email':usuario[3],'telefono':usuario[4],
                    'direccion':usuario[5],'nacimiento':usuario[6],'altura':str(usuario[7]),'peso':str(usuario[8])}
            self.lista_usuario.append(usuario)
            
    def on_of_lineedit(self,bool):
        self.nombre.setEnabled(bool)
        self.apellido.setEnabled(bool)
        self.email.setEnabled(bool)
        self.telefono.setEnabled(bool)
        self.direccion.setEnabled(bool)
        self.nacimiento.setEnabled(bool)
        self.altura.setEnabled(bool)
        self.peso.setEnabled(bool)

    def limpiar_lineedit(self):
        self.nombre.setText('')
        self.apellido.setText('')
        self.email.setText('')
        self.telefono.setText('')
        self.direccion.setText('')
        self.nacimiento.setText('')
        self.altura.setText('')
        self.peso.setText('')
        
    
    def on_nuevo(self):
        self.limpiar_lineedit()
        self.on_of_lineedit(True)

        self.aceptar.setEnabled(True)
        self.cancelar.setEnabled(True)
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.nuevo.setEnabled(False)
        self.lista.setEnabled(False)
        self.botones.hide()   
    
    def on_aceptar(self):
        try:
            nombre = self.nombre.text()
            apellido = self.apellido.text()
            email = self.email.text()
            telefono = self.telefono.text()
            direccion = self.direccion.text()
            nacimiento = self.nacimiento.text()
            altura = float(self.altura.text())
            peso = float(self.peso.text())
        
                    
            #Agregar usuario a la base de datos contactos.db
            self.cursor.execute(f"INSERT INTO CONTACTOS(nombres,apellidos,email,telefono,direccion,fecha_nac,altura,peso) VALUES ('{nombre}','{apellido}','{email}','{telefono}','{direccion}','{nacimiento}','{altura}','{peso}')")
            self.conexion.commit()

            #nos devuelve el id automaticamente 'self.cursor.lastrowid'
            self.lista.addItem(f'{self.cursor.lastrowid} | {nombre} | {apellido} | {email} | {telefono} | {direccion} | {nacimiento} | {altura} | {peso}')
            usuario = {'id':self.cursor.lastrowid,'nombre':nombre,'apellido':apellido,'email':email,'telefono':telefono,
                    'direccion':direccion,'nacimiento':nacimiento,'altura':altura,'peso':peso}
            
            self.lista_usuario.append(usuario)
        
        
            
            self.limpiar_lineedit()
            
            self.nuevo.setEnabled(True)
            self.aceptar.setEnabled(False)
            self.cancelar.setEnabled(False)
            self.on_of_lineedit(False)
            self.lista.setEnabled(True)
        except ValueError:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Ingrese los datos correctamente')
            
            
            #Iconos
            msg.setIcon(QMessageBox.Information)
  
            msg.setStandardButtons(QMessageBox.Yes)
            
            resultado = msg.exec_()
            if resultado == QMessageBox.Yes:
                self.limpiar_lineedit()
                
                self.nuevo.setEnabled(True)
                self.aceptar.setEnabled(False)
                self.cancelar.setEnabled(False)
                self.on_of_lineedit(False)
                self.lista.setEnabled(True)
                
    def on_cancelar(self):
        self.nuevo.setEnabled(True)
        self.aceptar.setEnabled(False)
        self.cancelar.setEnabled(False)
        
        self.on_of_lineedit(False)
        self.limpiar_lineedit()
        self.lista.setEnabled(True)
        
        
    def on_mostrar(self):
        #self.setText(self.lista.currentItem().text())
        orden = self.lista.currentRow()
        usuario_actual = self.lista_usuario[orden]
        self.usuario_actual = self.lista_usuario[orden]
        
        self.nombre.setText(usuario_actual['nombre'])
        self.apellido.setText(usuario_actual['apellido'])
        self.email.setText(usuario_actual['email'])
        self.telefono.setText(usuario_actual['telefono'])
        self.direccion.setText(usuario_actual['direccion'])
        self.nacimiento.setText(usuario_actual['nacimiento'])
        self.altura.setText(str(usuario_actual['altura']))
        self.peso.setText(str(usuario_actual['peso']))
        
        print(usuario_actual)
        print(self.lista.currentRow())
        
        self.editar.setEnabled(True)
        self.eliminar.setEnabled(True)
        
        
    def on_editar(self):
        self.nuevo.setEnabled(False)
        self.editar.setEnabled(False)
        self.eliminar.setEnabled(False)
        self.on_of_lineedit(True)
        self.botones.show()
        self.lista.setEnabled(False)
        
    def on_aceptar_editar(self):
        nombre = self.nombre.text()
        apellido = self.apellido.text()
        email = self.email.text()
        telefono = self.telefono.text()
        direccion = self.direccion.text()
        nacimiento = self.nacimiento.text()
        altura = self.altura.text()
        peso = self.peso.text()
        
        orden = self.lista.currentRow()
        #selecciono contacto a editar
        #usuario_actual = self.lista_usuario[orden]
        
        usuario_editado = {'id':self.usuario_actual['id'],'nombre':nombre,'apellido':apellido,'email':email,'telefono':telefono,
                   'direccion':direccion,'nacimiento':nacimiento,'altura':altura,'peso':peso}
        
        #reemplazo usuario en lista_usuario
        self.lista_usuario[orden] = usuario_editado
        
        #actualiza la base de datos
        usuario_id = self.usuario_actual['id']
        self.cursor.execute(f"UPDATE contactos SET nombres='{nombre}',apellidos='{apellido}',email='{email}',telefono='{telefono}',direccion='{direccion}',fecha_nac='{nacimiento}',altura='{altura}',peso='{peso}' WHERE id='{usuario_id}'")
        self.conexion.commit()
        
        #actualizo lista que se muestra
        self.lista.currentItem().setText(f'{usuario_id} | {nombre} | {apellido} | {email} | {telefono} | {direccion} | {nacimiento} | {altura} | {peso}')
        
        self.botones.hide()
        self.on_of_lineedit(False)
        self.nuevo.setEnabled(True)
        self.lista.setEnabled(True)
        
    def on_cancelar_editar(self):
        self.botones.hide()
        self.on_of_lineedit(False)
        self.nuevo.setEnabled(True)
        self.lista.setEnabled(True)
        
    def on_eliminar(self):
        mensaje = QMessageBox()
        mensaje.setWindowTitle('Quitar Lista')
        mensaje.setText(f'Desea eliminar el contacto ?')
            
        #Icono mensaje
        mensaje.setIcon(QMessageBox.Warning)
            
        #Botones
        mensaje.setStandardButtons(QMessageBox.No | QMessageBox.Yes )
            
        resultado = mensaje.exec_()
        
        if resultado == QMessageBox.Yes:
            
            self.lista.takeItem(self.lista.currentRow()) 
            self.lista_usuario.remove(self.usuario_actual) 
            
            #Borro de la base de datos
            usuario_id = self.usuario_actual['id']
            self.cursor.execute(f"DELETE FROM contactos WHERE id='{usuario_id}'")
            self.conexion.commit()  
             
    #def closeEvent(self, event):
        #self.conexion.close()


app = QApplication([])

win = MiVentana()
win.show()

app.exec_()