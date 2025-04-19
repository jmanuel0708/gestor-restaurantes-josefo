from tkinter import Tk, Menu, Label, Frame, Entry, Button, Radiobutton, IntVar, StringVar, PhotoImage, messagebox as MessageBox
import sqlite3

# CONFIGURACION DEL ARCHIVO
base_de_datos = "restaurante_hybridge.db"
main_font = "Times New Roman"

# Crear la base de datos
def crear_bd():
    conexion = sqlite3.connect(base_de_datos)
    cursor = conexion.cursor()

    # Creación de la tabla CATEGORIAS en la base de datos
    try:
        cursor.execute("""CREATE TABLE categorias(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nombre_categoria TEXT UNIQUE NOT NULL)""")
        cursor.execute("""INSERT INTO categorias (nombre_categoria) VALUES 
                       ('Entradas'),
                       ('Platos Fuertes'),
                       ('Postres'),
                       ('Bebidas')""")
    except sqlite3.OperationalError:
        pass
    
    # Creación de la tabla PLATILLOS en la base de datos
    try:
        cursor.execute("""CREATE TABLE platillos(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nombre TEXT UNIQUE NOT NULL,
                       precio FLOAT NOT NULL,
                       categoria_id INTEGER NOT NULL,
                       FOREIGN KEY (categoria_id) REFERENCES categorias(id))""")
        cursor.execute("""INSERT INTO platillos (nombre,precio,categoria_id) VALUES 
                       ('Papas a la Francesa',55.0,1),
                       ('Alitas',80.0,1),
                       ('Hamburguesa',120.0,2),
                       ('Pizza',150.0,2),
                       ('Hot Dog',70.0,2),
                       ('Helado',45.0,3),
                       ('Pay de Manzana',50.0,3),
                       ('Refresco',35.0,4),
                       ('Aguas Frescas',25.0,4),
                       ('Cerveza',50.0,4)""")
    except sqlite3.OperationalError:
        pass

    conexion.commit()
    conexion.close()

# CREACION DE MENUS SUPERIORES
def base_root():
    # MENÚ SUPERIOR
    # Creación del menú de comandos
    menubar = Menu(root)
    root.config(menu=menubar)

    # Creación de elementos del menú comandos
    showmenu = Menu(menubar, tearoff=0)
    showmenu.add_command(label="Vizualizar menú", command=menu_final)

    catmenu = Menu(menubar, tearoff=0)
    catmenu.add_command(label="Agregar categoría", command=crear_categoria)
    catmenu.add_command(label="Editar categoría", command=modificar_categoria)
    catmenu.add_command(label="Eliminar categoría", command=eliminar_categoria)

    platmenu = Menu(menubar, tearoff=0)
    platmenu.add_command(label="Agregar platillo",command=crear_platillo)
    platmenu.add_command(label="Editar platillo", command=modificar_platillo)
    platmenu.add_command(label="Eliminar platillo", command=eliminar_platillo)

    # Añadir el menú de comandos
    menubar.add_cascade(label="Menu", menu=showmenu)
    menubar.add_cascade(label="Categorías", menu=catmenu)
    menubar.add_cascade(label="Platillos", menu=platmenu)

# LIMPIAR PANTALLA
def limpiar_pantalla():
    for widget in root.winfo_children():
        widget.destroy()

# PÁGINA DE BIENVENIDA
def menu_final():
    limpiar_pantalla()
    base_root()

    # Titulo Menu
    Label(root, text="   Restaurante Josefo   ", fg="darkgreen", font=(main_font,28,"bold italic")).pack()

    # Subtitulo Menu
    Label(root, text="Menú del día", fg="black", font=(main_font, 24,"bold")).pack()

    # Separador de títulos y categorías
    Label(root, text="").pack()


    # Conexión a la base de datos
    conexion = sqlite3.connect(base_de_datos)
    cursor = conexion.cursor()

    # CONSULTA A LA BASE DE DATOS

    # Consulta las categorias
    categorias = cursor.execute("SELECT * FROM categorias").fetchall()
    for categoria in categorias:
        # Imprime las categorías
        Label(root, text=categoria[1], fg="black", font=(main_font,20,"bold italic")).pack()

        # Consulta los platillos
        platillos = cursor.execute("SELECT * FROM platillos WHERE categoria_id= ?",(categoria[0],)).fetchall()
        for p in platillos:
            # Crea un frame para alinear el nombre y el precio
            frame = Frame(root)
            frame.pack(fill='x')

            # Imprime el nombre del platillo alineado a la izquierda
            Label(frame, text=p[1], fg="black", font=(main_font, 14), anchor='w').pack(side='left', fill='x', expand=True)

            # Imprime el precio del platillo alineado a la derecha
            Label(frame, text=f"${p[2]:>3.2f}", fg="black", font=(main_font, 14), anchor='e').pack(side='right')

        # Separador de categorías
        Label(root, text="").pack()

    # Cerrar la base de datos
    conexion.close()

# Mostrar categorias
def mostrar_categorias():
    conexion = sqlite3.connect(base_de_datos)
    cursor = conexion.cursor()

    # Seleccionar todos los valores de categoria
    cursor.execute("SELECT * FROM categorias ORDER BY id")
    # Asignar los valores a una variable
    categorias = cursor.fetchall()

    # Creación de la variable en formato de numero
    categoria_seleccionada = IntVar()
    categoria_seleccionada.set(0) # Valor por defecto

    # Creación de un frame para ingresar los radiobuttons
    frame = Frame(root)
    frame.pack(fill="x")

    # Iteración para imprimir todas las categorias
    for categoria in categorias:       
        Radiobutton(frame, text=f"{categoria[1]}", fg="black", variable=categoria_seleccionada, value=categoria[0]).pack()

    # Separador de texto
    Label(root, text="").pack()

    return categoria_seleccionada

# Mostrar platillos
def mostrar_platillos():
    conexion = sqlite3.connect(base_de_datos)
    cursor = conexion.cursor()

    # Seleccionar los valores de id, nombre, precio y categoria y ordenarlos por categoria
    cursor.execute("""SELECT pla.id, pla.nombre, pla.precio, cat.nombre_categoria
                   FROM platillos pla
                   JOIN categorias cat ON pla.categoria_id=cat.id
                   ORDER BY cat.id""")
    # Asignar los valores seleccionados a una variable
    platillos = cursor.fetchall()

    # Iteración para imprimir todos los platillos
    for platillo in platillos:
        # Creación de un Frame para poder alinear los platillos
        frame = Frame(root)
        frame.pack(fill="x")

        Label(frame, text=f"{platillo[3]:<15}", fg="black", font=(main_font,14), anchor="w", width=15).pack(side="left")
        Label(frame, text=f"{platillo[1]:<20}", fg="black", font=(main_font,14), anchor="w", width=20).pack(side="left")
        Label(frame, text=f"${platillo[2]:<7.2f}", fg="black", font=(main_font,14), anchor="w", width=7).pack(side="right")

    # Separador de texto
    Label(root,text="------------------", fg="black").pack()

# MANIPULACION DE CATEGORÍAS
# Creación de categoría
def crear_categoria():
    limpiar_pantalla()
    base_root()

    # Guardar la nueva categoría
    def guardar():
        conexion = sqlite3.connect(base_de_datos)
        cursor = conexion.cursor()

        # Verificación para que no haya un texto vacio
        if nueva_categoria.get() == "":
            MessageBox.showerror("Error","No has ingresado ningun valor")
        else:
            # Solicitar confirmación para agregar el valor a la base de datos
            confirmacion = MessageBox.askyesno("Confirmar",f"Estas a punto de agregar '{nueva_categoria.get()}' como una nueva categoria\n\n¿Deseas continuar?")
            if confirmacion == True:
                # Verificación para evitar valores duplicados
                try:
                    # Función para ingresar el valor a la base de datos
                    cursor.execute("INSERT INTO categorias (nombre_categoria) VALUES (?)",(nueva_categoria.get(),))
                    conexion.commit()
                    conexion.close()

                    # Función para regresar al menú inicial después de haber actualizado la base de datos
                    menu_final()
                except sqlite3.IntegrityError:
                    # Mostrar alerta de error en caso de un valor duplicado
                    MessageBox.showerror("Error",f"No se ha podido guardar la categoria '{nueva_categoria.get()}' porque ya existe")
            else:
                # En caso de no confirmar vaciar la entrada de texto
                nueva_categoria.set("")

    # Cancelar creación de nueva categoría
    def cancelar():
        # Validación de texto antes de cancelar
        if nueva_categoria.get() != "":
            confirmacion = MessageBox.askyesno("Cancelar","¿Deseas regresar sin guardar?")
            # Si el cliente confirma que quiere salir sin guardar los cambios regresa al menú principal
            if confirmacion == True:
                menu_final()
        # Si no hay texto regresar automaticamente al menú principal
        else:
            menu_final()
    
    # Titulo de la página
    Label(root, text="Agregar otra categoría", fg="black", font=(main_font, 24,"bold")).pack()

    # Separador de texto
    Label(root, text="").pack()

    # Creación de la variable en formato de texto
    nueva_categoria = StringVar()

    # Creación de un frame para ingresar las instrucciones y campo de texto a la misma altura
    frame = Frame(root)
    frame.pack()

    # Texto con instrucciones
    Label(frame, text="Ingresa el nombre de la nueva categoria:").pack(side="left")
    # Campo para ingresar texto
    Entry(frame, justify="center", textvariable=nueva_categoria).pack(side="right")

    # Separador de texto
    Label(root, text="").pack()

    # Botones para completar o cancelar la solicitud
    Button(root, text="Agregar", command=guardar).pack()
    Button(root, text="Cancelar", command=cancelar).pack()    

# Modificación de categoría
def modificar_categoria():
    limpiar_pantalla()
    base_root()

    # Después de haber seleccionado la categoría a editar esto te llevara al siguiente menu para cambiar el nombre
    def siguiente():
        limpiar_pantalla()
        base_root()

        # Actualizar los cambios en la base de datos
        def guardar_cambios():
            conexion = sqlite3.connect(base_de_datos)
            cursor = conexion.cursor()

            # Verificación de que se haya ingresado un valor en la entrada de texto
            if nuevo_nombre.get() == "":
                MessageBox.showerror("Error","No has ingresado ningun valor")
            else:
                # En caso que si haya texto confirmar con el usuario antes de realizar los cambios
                confirmacion = MessageBox.askyesno("Confirmar",f"Estas a punto de cambiar el nombre de la categoria '{categoria_a_editar[0]}' a '{nuevo_nombre.get()}'\n¿Deseas continuar?")
                
                # Una vez que el usuario haya confirmado los cambios aplicarlos en la base de datos
                if confirmacion == True:
                    # Intentar actualizar la base de datos
                    try:
                        cursor.execute("UPDATE categorias SET nombre_categoria=(?) WHERE id=?",(nuevo_nombre.get(),categoria_seleccionada.get()))
                        conexion.commit()

                        # Regresar al menu principal después de haber ejecutado los cambios
                        menu_final()

                    # En caso de error por duplicidad de categorías informar al usuario que ya existe esa categoría
                    except sqlite3.IntegrityError:
                        MessageBox.showerror("Error",f"No se ha podido editar la categoria '{nuevo_nombre.get()}' porque ya existe")

                else:
                    # Si el usuario decide no confirmar los cambios reseteas la entrada de texto
                    nuevo_nombre.set("")
            
            # Cerrar la conexion con la base de datos
            conexion.close()

        # Regresar al menu para seleccionar las categorías
        def regresar():
            # Validar si existe un texto antes de regresar
            if nuevo_nombre.get() != "":
                # En caso de haber texto confirmar con el usuario si quiere regresar sin guardar
                confirmacion = MessageBox.askyesno("Cancelar","¿Deseas regresar sin guardar?")
                if confirmacion == True:
                    modificar_categoria()
            else:
                modificar_categoria()

        # Creación de la variable 'categoria_id' para obtener el valor del usuario seleccionado en el radiobutton en mostrar_categorias()
        categoria_id = categoria_seleccionada.get()
        
        # Verificar que el usuario haya seleccionado una opción antes de continuar
        if categoria_id != 0:        
            limpiar_pantalla()
            base_root()

            conexion = sqlite3.connect(base_de_datos)
            cursor = conexion.cursor()

            # Buscar en la base de datos el nombre de la categoría a editar
            categoria_a_editar = cursor.execute("SELECT nombre_categoria FROM categorias WHERE id = ?", (categoria_id,)).fetchone()

            # Imprimir el nombre de la categoría que se esta editando
            Label(root, text=f"Estas editando la categoria '{categoria_a_editar[0]}'.", fg="black", font=(main_font,16, "bold")).pack()

            # Separador de texto
            Label(root, text="").pack()

            # Creación de frame para empacar el texto y la entrada de texto a la misma altura
            frame = Frame(root)
            frame.pack()

            # Le indicas al programa que la variable nuevo_nombre es de tipo texto
            nuevo_nombre = StringVar()

            # Creas el lugar donde el usuario introducira el nuevo nombre de la categoría
            Label(frame, text="Introduce el nuevo nombre de la categoría:", fg="black", font=(main_font,14)).pack(side="left")
            Entry(frame, justify="center", textvariable=nuevo_nombre).pack(side="right")

            # Separador de texto
            Label(root, text="").pack()

            # Botónes para guardar los cambios y regresar
            Button(root, text="Guardar cambios", command=guardar_cambios).pack()
            Button(root, text="Regresar", command=regresar).pack()
        
        # Lanzar un error en caso de que el usuario no haya seleccionado ninguna opción
        else:
            MessageBox.showerror("Error","No has seleccionado ninguna categoría para editar")
            modificar_categoria()

    # Regresar al menú principal en caso de cancelar
    def cancelar():
        menu_final()

    # Título de la página
    Label(root, text="Modificar categoría", fg="black", font=(main_font, 24,"bold")).pack()

    # Separador de texto
    Label(root, text="").pack()

    # Imprimir categorías en forma de radiobutton
    categoria_seleccionada = mostrar_categorias()

    # Imprimir botónes de acción
    Button(root, text="Siguiente", command=siguiente).pack()
    Button(root, text="Cancelar", command=cancelar).pack()

# Eliminar categoría
def eliminar_categoria():
    limpiar_pantalla()
    base_root()

    # Creación de la funcion para eliminar una categoría
    def eliminar():
        conexion = sqlite3.connect(base_de_datos)
        cursor = conexion.cursor()

        # Imprimir las categorías en forma de radiobuttons desde mostrar_categorias() y obtener el valor seleccionado por el usuario
        categoria_id = categoria_seleccionada.get()

        # Verificación de selección
        if categoria_id != 0: 
            # Validar si la categoría que vamos a intentar eliminar tiene algun platillo registrado
            validacion = cursor.execute("SELECT * FROM platillos WHERE categoria_id = ?",(categoria_id,)).fetchall()
            if not validacion:
                # Seleccionas el nombre de la categoría que vas a eliminar y lo asignas a la variable categoria_a_eliminar
                categoria_a_eliminar = cursor.execute("SELECT nombre_categoria FROM categorias WHERE id = ?",(categoria_id,)).fetchone()
                # Mensaje para confirmar con el usuario que quiere eliminar la categoría
                confirmacion = MessageBox.askyesno("Eliminar",f"Estas a punto de elimina permanentemente la categoría '{categoria_a_eliminar[0]}'\n\n¿Deseas confirmar los cambios?")
                # En caso de confirmar ejecutamos los cambios en la base de datos
                if confirmacion == True:
                    cursor.execute("DELETE FROM categorias WHERE id=?",(categoria_id,))
                    conexion.commit()
                    conexion.close()

                    # Regresamos al usuario al menú principal despues de ejecutar los cambios
                    menu_final()

            else:
                MessageBox.showerror("Error","No se puede eliminar una categoría que tiene platillos publicados.\n\nElimina los platillos y vuelvelo a intentar")
                eliminar_categoria()

        # Notificamos al usuario que no ha seleccionado ninguna categoría para eliminar
        else:
            MessageBox.showerror("Error","No has seleccionado ninguna categoría para eliminar")
            # Le volvemos a imprimir la lista de categorías
            eliminar_categoria()

    # Función para regresar al usuario al menú principal
    def cancelar():
        menu_final()

    # Título de la página
    Label(root, text="Eliminar categoría", fg="black", font=(main_font, 24,"bold")).pack()

    # Separador de texto
    Label(root, text="").pack()

    # Imprimir categorías en forma de radiobutton
    categoria_seleccionada = mostrar_categorias()

    # Imprimir botónes de acción
    Button(root, text="Eliminar", command=eliminar).pack()
    Button(root, text="Cancelar", command=cancelar).pack()

# MANIPULACIÓN DE PLATILLOS
# Creación de platillo
def crear_platillo():
    limpiar_pantalla()
    base_root()
    
    def guardar():
        conexion = sqlite3.connect(base_de_datos)
        cursor = conexion.cursor()

        # Verificar que todos los campos tengan un valor seleccionado y mandar error si no
        if nuevo_platillo.get() == "" or precio_nuevo_platillo.get() == "" or categoria_seleccionada.get() == 0:
            MessageBox.showerror("Error","No has ingresado, precio o categoría del platillo.\n\nPor favor vuelve a intentarlo")
        else:
            # Intentar convertir el valor ingresado en 'Precio' a un numero flotante
            try:
                numero = float(precio_nuevo_platillo.get().replace(",",""))
            # En caso de error por no haber escrito números mostrar un mensaje de error
            except ValueError:
                MessageBox.showerror("Error","No has ingresado un número válido en el precio.\n\nPor favor vuelve a intentarlo")
                # Vaciar el campo de texto
                precio_nuevo_platillo.set("")
            else:
                # En caso de que el usuario si haya ingresado un número obtener el nombre de la categoría seleccionada
                categoria = cursor.execute("SELECT nombre_categoria FROM categorias WHERE id =?",(categoria_seleccionada.get(),)).fetchone()
                # Popup para confirmar con el cliente el nuevo platillo
                confirmacion = MessageBox.askyesno("Confirmar",f"Estas seguro que deseas agregar el platillo '{nuevo_platillo.get()}' a la categoria '{categoria[0]}' con un precio de ${numero:.2f}")
                # En caso de confirmar agregar el platillo a la base de datos
                if confirmacion == True:
                    cursor.execute("INSERT INTO platillos (nombre,precio,categoria_id) VALUES (?,?,?)",(nuevo_platillo.get(),numero,categoria_seleccionada.get()))
                    # Confirmar los cambios en la base de datos
                    conexion.commit()
                    # Regresar al menú principal una vez todos los cambios se hayan ejecutado
                    menu_final()
            
        # Cerrar la conexión a la base de datos
        conexion.close()


    # Función para regresar al menú principal
    def cancelar():
        # Verificación de texto en los campos para regresar al menú principal
        if nuevo_platillo.get() == "" and precio_nuevo_platillo.get() == "":
            menu_final()
        else:
            confirmacion = MessageBox.askyesno("Cancelar","¿Deseas regresar sin guardar los cambios?")
            # Si el cliente confirma que que quiere salir sin guardar regresar al menú principal
            if confirmacion == True:
                menu_final()


    # Titulo de la página
    Label(root, text="Agregar otro platillo", fg="black", font=(main_font, 24,"bold")).pack()

    # Separador de texto
    Label(root, text="").pack()

    # Creación de la variables en formato de texto y numero
    nuevo_platillo = StringVar()
    precio_nuevo_platillo = StringVar()

    # Creación de un frame para ingresar las instrucciones y campo de texto a la misma altura
    frame_1 = Frame(root)
    frame_1.pack()

    # Texto con instrucciones
    Label(frame_1, text="Ingresa el nombre del nuevo platillo:").pack(side="left")
    # Campo para ingresar texto
    Entry(frame_1, justify="center", textvariable=nuevo_platillo).pack(side="right")

    # Creación de un segundo frame para ingresar el precio
    frame_2 = Frame(root)
    frame_2.pack()

    # Texto con instrucciones
    Label(frame_2, text="Ingresa el precio del nuevo platillo: $").pack(side="left")
    # Campo para ingresar texto
    Entry(frame_2, justify="center", textvariable=precio_nuevo_platillo).pack(side="right")

    # Separador de texto
    Label(root, text="---------------", fg="black", font=(main_font,14,"bold")).pack()

    # Mostrar categorias en forma de radiobuttons y asignar el valor seleccionado a una variable
    Label(root, text="Selecciona la categoría a la que quieres asignar este platillo:\n").pack()
    categoria_seleccionada = mostrar_categorias()

    # Botones para completar o cancelar la solicitud
    Button(root, text="Agregar", command=guardar).pack()
    Button(root, text="Cancelar", command=cancelar).pack()   

# Modificación de platillo
def modificar_platillo():
    limpiar_pantalla()
    base_root()

    conexion = sqlite3.connect(base_de_datos)
    cursor = conexion.cursor()

    # Función para obtener la categoría seleccionada
    def siguiente():

        # Funcion para crear la siguiente página
        def platillo_a_editar():
            limpiar_pantalla()
            base_root()

            # Función para obtener el platillo seleccionado
            def avanzar():
                
                # Función para crear la siguiente página
                def edicion_platillo():  
                    limpiar_pantalla()
                    base_root()  

                    # Función para obtener la acción seleccionada por el usuario
                    def avanzar_2():
                        
                        # Función para crear la siguiente página
                        def nuevos_valores():
                            limpiar_pantalla()
                            base_root()

                            # Creación de un frame para alinear las instrucciones y la entrada de texto
                            frame_int_2 = Frame(root)
                            regresar_texto = "¿Estas seguro de que deseas salir sin guardar los cambios?"
                            menu_texto = "¿Estas seguro de que deseas salir sin guardar los cambios?"

                            # Función en caso que el usario haya seleccionado editar el nombre
                            if valor == 1:
                                # Función para guardar el nuevo nombre
                                def guardar_nuevo_nombre():
                                    # Obtener el nombre asignado por el usuario
                                    new_name = nuevo_nombre.get()

                                    # Verificar que el usuario haya ingresado texto
                                    if new_name == "":
                                        # Mostrar error si no hay texto
                                        MessageBox.showerror("Error","No has ingresado el nuevo nombre del platillo.\n\nPor favor intentalo nuevamente")
                                    else:
                                        # Obtener el nombre antiguo del platillo que se va a editar
                                        old_name = cursor.execute("SELECT nombre FROM platillos WHERE id= ?",(platillo_id,)).fetchone()

                                        # Solicitar confirmación del usuario antes de ejecutar los cambios
                                        confirmacion = MessageBox.askyesno("Guardar",f"¿Deseas confirmar el cambio de nombre del platillo '{old_name[0]}' a '{new_name}'")
                                        # En caso de confirmar ejecitar los cambios en la base de datos
                                        if confirmacion == True:
                                            cursor.execute("UPDATE platillos SET nombre=? WHERE id=?",(new_name,platillo_id))
                                            conexion.commit()
                                            conexion.close()
                                            # Regresar al menú principal después de ejecutar los cambios
                                            menu_final()
                                        # En caso que el usuario no confirme los cambios resetar el campo de texto
                                        else:
                                            nuevo_nombre.set("")

                                # Función para verificar entradas de texto antes de regresar a la página anterios        
                                def regresar_ant_nombre():
                                    new_name = nuevo_nombre.get()

                                    # Verificar si hay texto en las entradas antes de regresar a la página anterior
                                    if new_name != "":
                                        # En caso que si haya texto confirmar con el usuario si desea salir sin guardar los cambios
                                        confirmacion = MessageBox.askyesno("Salir",regresar_texto)
                                        if confirmacion == True:
                                            edicion_platillo()
                                    else:
                                        # En caso de que no haya texto regresar a la página anterior
                                        edicion_platillo()

                                # Función para verificar entradas de texto antes de regresar al menú principal
                                def regresar_menu_nombre():
                                    new_name = nuevo_nombre.get()

                                    # Verificar si hay texto en las entradas antes de regresar a la página anterior
                                    if new_name != "":
                                        # En caso que si haya texto confirmar con el usuario si desea salir sin guardar los cambios
                                        confirmacion = MessageBox.askyesno("Salir",menu_texto)
                                        if confirmacion == True:
                                            menu_final()
                                    else:
                                        # En caso de que no haya texto regresar al menú principal
                                        menu_final()                                
                                
                                # Imprimir el título de la página
                                Label(root,text="Nuevo nombre", fg="black", font=(base_de_datos,24,"bold")).pack()

                                # Separador de texto
                                Label(root, text="").pack()

                                # Insertar el frame creado anteriormente
                                frame_int_2.pack(fill="x")

                                # Creación de variable para asignarle posteriormente el valor ingresado por el usuario
                                nuevo_nombre = StringVar()

                                # Solicitud de entrada y entrada de texto
                                Label(frame_int_2, text="Introduce el nuevo nombre del platillo").pack(side="left")
                                Entry(frame_int_2, justify="center", textvariable=nuevo_nombre).pack(side="right")

                                # Separador de texto
                                Label(root, text="").pack()

                                # Imprimir botónes de acción
                                Button(root, text="Guardar", command=guardar_nuevo_nombre).pack()
                                Button(root, text="Regresar", command=regresar_ant_nombre).pack()
                                Button(root, text="Cancelar", command=regresar_menu_nombre).pack()


                            # Función en caso que el usario haya seleccionado editar el precio
                            elif valor == 2:

                                # Creación de función para guardar el nuevo precio
                                def guardar_nuevo_precio():
                                    
                                    # Verificar el el usuario haya ingresado texto
                                    if nuevo_precio.get() == "":
                                        # En caso de que no se haya ingresado texto mostrar un error
                                        MessageBox.showerror("Error","No has ingresado el nuevo precio del platillo.\n\nPor favor intentalo nuevamente")

                                    else:
                                        # Intentar convertir el valor ingresado por el usuario de str a float
                                        try:
                                            # Eliminar las comas ingresadas por el usuario
                                            new_price = float(nuevo_precio.get().replace(",",""))
                                        except ValueError:
                                            # En caso que el usuario no haya ingresado números mostrar un error
                                            MessageBox.showerror("Error","No has ingresado un número válido en el precio.\n\nPor favor vuelve a intentarlo")
                                            # Resetear la caja de texto y dejarla en blanco
                                            nuevo_precio.set("")    
                                        else:
                                            # En caso que el usuario si haya ingresado un número obtener los valores del antigua platillo
                                            old_platillo = cursor.execute("SELECT * FROM platillos WHERE id=?",(platillo_id,)).fetchone()

                                            # Solicitar confirmación del usaurio antes de ejecutar los cambios
                                            confirmacion = MessageBox.askyesno("Guardar",f"Confirmar el cambio de precio del platillo {old_platillo[1]} de:\n\nAntiguo: ${old_platillo[2]:.2f}\nNuevo: ${new_price:.2f}")

                                            if confirmacion == True:
                                                # En caso de confirmación ejecutar los cambios en la base de datos
                                                cursor.execute("UPDATE platillos SET precio=? WHERE id=?",(new_price,platillo_id))
                                                conexion.commit()
                                                conexion.close()

                                                # Rgresar al menú principal después de ejecutar los cambios
                                                menu_final()
                                            else:
                                                # En caso de que el usuario no haya confirmado resetear la caja de texto
                                                nuevo_precio.set("")

                                # Función para verificar entradas de texto antes de regresar a la página anterior
                                def regresar_ant_precio():
                                    new_price = nuevo_precio.get()
                                    
                                    # Verificar si hay texto
                                    if new_price != "":
                                        # En caso de que no haya texto solicitar confirmación del usuario antes de regresar
                                        confirmacion = MessageBox.askyesno("Salir",regresar_texto)
                                        if confirmacion == True:
                                            # En caso de confirmar regresar a la página anterior
                                            edicion_platillo()
                                    else:
                                        # En caso de que no haya texto regresar a la página anterior
                                        edicion_platillo()
                                
                                # Función para verificar entradas de texto antes de regresar al menú principal
                                def regresar_menu_precio():
                                    new_price = nuevo_precio.get()
                                    
                                    # Verificar si hay texto
                                    if new_price != "":
                                        # En caso de que haya texto solicitar confirmación del usuario antes de cancelar
                                        confirmacion = MessageBox.askyesno("Salir",menu_texto)
                                        if confirmacion == True:
                                            # En caso de confirmación regresar al menú principal
                                            menu_final()
                                    else:
                                        # En caso de que no haya texto regresar al menú principal
                                        menu_final()
                                
                                # Imprimir el nombre de la página
                                Label(root,text="Nuevo precio", fg="black", font=(base_de_datos,24,"bold")).pack()

                                # Separador de texto
                                Label(root, text="").pack()


                                # Insertar el frame creado para alinear las instrucciones y entrada de texto
                                frame_int_2.pack(fill="x")
                                
                                # Creación de variable para obtener posteriormente el valor en la entrada de texto
                                nuevo_precio = StringVar()

                                # Imprimir instrucciones y entrada de texto
                                Label(frame_int_2, text="Introduce el nuevo precio de tu platillo: $").pack(side="left")
                                Entry(frame_int_2, justify="center", textvariable=nuevo_precio).pack(side="right")

                                # Separador de texto
                                Label(root, text="").pack()

                                # Imprimir botones de acción
                                Button(root, text="Guardar", command=guardar_nuevo_precio).pack()
                                Button(root, text="Regresar", command=regresar_ant_precio).pack()
                                Button(root, text="Cancelar",command=regresar_menu_precio).pack()

                            # Función en caso que el usario haya seleccionado editar la categoría
                            elif valor == 3:
                                def guardar_nueva_categoria():
                                    # Obtener el valor asignado por el usuario por medio de los radiobuttons
                                    new_categoria_id = categoria_seleccionada.get()

                                    # Verificar si el usuario selecciono alguna categoría
                                    if new_categoria_id == 0:
                                        # Mostrar error en caso de no haber seleccionado ninguna categoría
                                        MessageBox.showerror("Error","No has seleccionado ninguna categoria")
                                    else:
                                        # Obtener los valores de la antigua categoría
                                        old_categoria = cursor.execute("""SELECT pla.nombre, cat.nombre_categoria 
                                                                       FROM platillos pla
                                                                       JOIN categorias cat ON pla.categoria_id = cat.id
                                                                       WHERE pla.id=?""",(platillo_id,)).fetchone()
                                        # Obtener los valores por asignar de la nueva categoría
                                        new_categoria = cursor.execute("SELECT nombre_categoria FROM categorias WHERE id=?",(new_categoria_id,)).fetchone()
                                                    
                                        # Solicitar confirmación al usuario antes de ejecutar los cambios
                                        if MessageBox.askyesno("Guardar",f"¿Estás seguro que deseas cambiar la categoria del platillo '{old_categoria[0]}', de '{old_categoria[1]}' a '{new_categoria[0]}'") == True:
                                            # Ejecutar los cambios en la base de datos
                                            cursor.execute("UPDATE platillos SET categoria_id=? WHERE id=?",(new_categoria_id,platillo_id))
                                            conexion.commit()
                                            conexion.close()

                                            # Regresar al menú principal
                                            menu_final()

                                # Función para verificar si hay alguna categoría seleccionada antes de regresar al menu principal
                                def regresar_menu_categoria():
                                    new_categoria_id = categoria_seleccionada.get()

                                    # En caso de que no haya ninguna categoría seleccionada regresar al menú principal
                                    if new_categoria_id == 0:
                                        menu_final()
                                    # En caso de que si haya alguna categoría seleccionada solicitar confirmación del usuario antes de regresar al menú principal
                                    else:
                                        if MessageBox.askyesno("Salir","¿Estas seguro que deseas salir sin guardar los cambios?") == True:
                                            menu_final()
                                
                                # Imprimir el título de la página
                                Label(root,text="Nueva categoría", fg="black", font=(base_de_datos,24,"bold")).pack()

                                # Separador de texto
                                Label(root, text="").pack()

                                # Imprimir instrucciones
                                Label(root, text="Selecciona la nueva categoria:").pack()

                                # Imprimir categorias en forma de radiobuttons
                                categoria_seleccionada = mostrar_categorias()

                                # Imprimir botónes de acción
                                Button(root, text="Guardar", command=guardar_nueva_categoria).pack()
                                Button(root, text="Regresar", command=edicion_platillo).pack()
                                Button(root, text="Cancelar", command=regresar_menu_categoria).pack()

                        # Creación de variable para obtener la acción seleccionada por el usuario
                        valor = valor_a_editar.get()

                        # Verificar que el usuario haya seleccionado una opción
                        if valor != 0:
                            # Invocar la función para pasar a la siguiente página
                            nuevos_valores()
                        else:
                            # Mostrar error en caso de que no haya selección
                            MessageBox.showerror("Error","No has seleccionado ningún valor")
                        
                    # Creación de variable para obtener el valor que se quiere editar    
                    valor_a_editar = IntVar()
                    valor_a_editar.set(0)

                    # Asignar de la base de datos el nombre del platillo seleccionado
                    nombre = cursor.execute("SELECT nombre FROM platillos WHERE id=?",(platillo_id,)).fetchone()

                    # Imprimir el nombre en la página
                    Label(root, text=nombre[0], fg="black", font=(main_font, 24,"bold")).pack()
                    
                    # Separador de texto
                    Label(root, text="").pack()

                    # Imprimir etiqueta con instrucciones
                    Label(root, text="¿Qué valor quieres editar?", fg="black").pack()

                    # Creación de marco para alinear los radiobuttons
                    frame_int = Frame(root)
                    frame_int.pack(fill="x")

                    # Imprimir las opciones que se pueden realizar en forma de radiobuttons
                    Radiobutton(frame_int, variable=valor_a_editar, value=1, text="Nombre").pack(side="left")
                    Radiobutton(frame_int, variable=valor_a_editar, value=2, text="Precio").pack(side="left")
                    Radiobutton(frame_int, variable=valor_a_editar, value=3, text="Categoría").pack(side="left")

                    # Separador de texto
                    Label(root, text="").pack()

                    # Imprimir los botones de acción
                    Button(root, text="Siguiente", command=avanzar_2).pack()
                    Button(root, text="Regresar", command=platillo_a_editar).pack()
                    Button(root, text="Cancelar", command=menu_final).pack()

                # Creación de variable para obtener el id del platillo seleccionado
                platillo_id = platillo_seleccionado.get()

                # Verificar que el usuario haya seleccionado una categoria
                if platillo_id != 0:
                    # Solicitar al sistema la siguiente página
                    edicion_platillo()
                else:
                    # En caso de no haber ninguna selección mostrar error
                    MessageBox.showerror("Error","No has seleccionado ningún platillo")

            # Obtener los platillos de la categoría seleccionada
            platillos = cursor.execute("SELECT * FROM platillos WHERE categoria_id =?",(id_categoria,)).fetchall()

            # Creación de variable para asignarle el platillo que se va a editar
            platillo_seleccionado = IntVar()
            # Defaultear el valor del platillo a 0
            platillo_seleccionado.set(0)

            # Variable con el nombre de la categoría seleccionada
            categoria = cursor.execute("SELECT nombre_categoria FROM categorias WHERE id=?",(id_categoria,)).fetchone()
            # Imprimir el título de la página con el nombre de la categoría
            Label(root, text=categoria[0], fg="black", font=(main_font, 24,"bold")).pack()

            # Separador de texto
            Label(root, text="", font=(main_font,12)).pack()

            # Iteración para imprimir todos los platillos
            for platillo in platillos:
                # Creación de un frame para imprimir los platillos
                frame = Frame(root)
                frame.pack(fill="x")

                # Imprimir el nombre del platillo y su precio en forma de radiobuttons para su selección
                Radiobutton(frame, variable=platillo_seleccionado, value=platillo[0],text=f"{platillo[1]:<20}", fg="black", font=(main_font,14), anchor="w", width=20).pack(side="left")
                Label(frame, text=f"${platillo[2]:<7.2f}", fg="black", font=(main_font,14), anchor="w", width=7).pack(side="left")
            
            # Separador de texto
            Label(root,text="").pack()

            # Imprimir los botones de acción
            Button(root, text="Siguiente", command=avanzar).pack()
            Button(root, text="Regresar", command=modificar_platillo).pack()
            Button(root, text="Cancelar", command=menu_final).pack()

        # Obtener el valor seleccionado por el usuario de las categorías
        id_categoria = categoria_seleccionada.get()
        
        # Verificación de selección
        if id_categoria != 0:
            # En caso que el usario haya eleccionado una opción verificar si la categoría tiene platillos registrados
            platillos_registrados = cursor.execute("SELECT * FROM platillos WHERE categoria_id=?",(id_categoria,)).fetchall()
            if not platillos_registrados:
                # En caso de no tener platillos mostrar error
                MessageBox.showerror("Error","Esta categoría todavía no tiene ningun platillo registrado")
            else:
                # En caso de si tener platillos pasar a la siguiente página
                platillo_a_editar()
        else:
            # En caso de que el usuario no haya seleccionado ninguna opción mostrar error
            MessageBox.showerror("Error","No has seleccionado ninguna categoría")



    # Título de la página
    Label(root, text="Modificar platillo", fg="black", font=(main_font, 24,"bold")).pack()

    # Separador de texto
    Label(root, text="").pack()

    # Imprimir categorías en forma de radiobutton
    mostrar_platillos()

    # Imprimir etiqueta de instrucciones
    Label(root, text="Selecciona la categoría del platillo que quieres modificar", fg="black", font=(main_font,16,"bold")).pack()

    # Separador de texto
    Label(root, text="").pack()

    # Imprimpir categorias y asignarlas a una variable para manipulación
    categoria_seleccionada = mostrar_categorias()

    # Imprimir botónes de acción
    Button(root, text="Siguiente", command=siguiente).pack()
    Button(root, text="Cancelar", command=menu_final).pack()

# Eliminar platillo
def eliminar_platillo():
    limpiar_pantalla()
    base_root()

    conexion = sqlite3.connect(base_de_datos)
    cursor = conexion.cursor()

    # Función para obtener el valor de la categoría seleccionada por el usuario
    def siguiente():
        
        # Creación de la siguiente página
        def platillo_a_eliminar():
            limpiar_pantalla()
            base_root()

            def eliminar():

                # Obtener el id del platillo seleccionado por el usuario y asignarlo a la variable
                id_platillo = platillo_seleccionado.get()
                
                # Verificar que el usuario haya seleccionado una opción
                if id_platillo == 0:
                    # Mostrar un error en caso que el usuario no haya seleccionado ninguna opción
                    MessageBox.showerror("Error","No has seleccionado ningun platillo")
                else:
                    # Ingresar a la base de datos y asignar el nombre del platillo a la variable
                    nombre_platillo = cursor.execute("SELECT nombre FROM platillos WHERE id=?",(id_platillo,)).fetchone()
                    # Confirmación del usuario antes de realizar los cambios
                    if MessageBox.askyesno("Confirmar",f"¿Estás seguro que deseas eliminar el platillo '{nombre_platillo[0]}'?") == True:
                        # Ejecutar los cambios en la base de datos 
                        cursor.execute("DELETE FROM platillos WHERE id=?",(id_platillo,))
                        conexion.commit()
                        conexion.close()

                        # Regresar al menú principal después de ejecutar los cambios
                        menu_final()



            # Obtener los platillos de la categoría seleccionada
            platillos = cursor.execute("SELECT * FROM platillos WHERE categoria_id=?",(id_categoria,)).fetchall()

            # Crear variable para obtener el platillo seleccionado por el usuario
            platillo_seleccionado = IntVar()
            platillo_seleccionado.set(0)

            # Obtener el nombre de la categoría seleccionada
            categoria = cursor.execute("SELECT * FROM categorias WHERE id=?",(id_categoria,)).fetchone()

            # Imprimir el título de la página con el nombre la categoría
            Label(root, text=categoria[1], fg="black", font=(main_font, 24,"bold")).pack()

            # Separador de texto
            Label(root, text="", font=(main_font,12)).pack()

            # Iteración para imprimir todos los platillos
            for platillo in platillos:
                # Creación de un frame para imprimir los platillos
                frame = Frame(root)
                frame.pack(fill="x")

                # Imprimir el nombre del platillo y su precio en forma de radiobuttons para su selección
                Radiobutton(frame, variable=platillo_seleccionado, value=platillo[0],text=f"{platillo[1]:<20}", fg="black", font=(main_font,14), anchor="w", width=20).pack(side="left")
                Label(frame, text=f"${platillo[2]:<7.2f}", fg="black", font=(main_font,14), anchor="w", width=7).pack(side="left")
            
            # Separador de texto
            Label(root,text="").pack()

            # Imprimir los botones de acción
            Button(root, text="Siguiente", command=eliminar).pack()
            Button(root, text="Regresar", command=modificar_platillo).pack()
            Button(root, text="Cancelar", command=menu_final).pack()


        # Creas una variable para obtener el nombre de la categoría 
        id_categoria = categoria_seleccionada.get()
        
        
        # Verificar que el usuario haya seleccionado una categoría
        if id_categoria == 0:
            # Mostrar error en caso de que no lo haya hecho
            MessageBox.showerror("Error", "No has seleccionado ninguna categoría")
        else:
            # Verificar que en la categoría seleccionada haya algun platillo registrado
            platillos_registrados = cursor.execute("SELECT * FROM platillos WHERE categoria_id = ?",(id_categoria,)).fetchall()
            if not platillos_registrados:
                # En caso que no haya ningún platillo en la categoría mostrar un error
                MessageBox.showerror("Error", "La categoría seleccionada no tiene ningun platillo asignado")
            else:
                # Ejecutar la función para ir a la siguiente página
                platillo_a_eliminar()


    # Imprimir título de la página
    Label(root, text="Elimar platillo", fg="black", font=(main_font, 24,"bold")).pack()

    # Separador de texto
    Label(root, text="").pack()

    # Imprimir categorías en forma de radiobutton
    mostrar_platillos()

    # Imprimir etiqueta de instrucciones
    Label(root, text="Selecciona la categoría del platillo que quieres eliminar", fg="black", font=(main_font,16,"bold")).pack()

    # Separador de texto
    Label(root, text="").pack()

    # Imprimpir categorias y asignarlas a una variable para manipulación
    categoria_seleccionada = mostrar_categorias()

    # Imprimir botónes de acción
    Button(root, text="Siguiente", command=siguiente).pack()
    Button(root, text="Cancelar", command=menu_final).pack()

# Creación de la base de datos
crear_bd()

# Configuración de la raiz
root = Tk()
root.title("Gestor de Restaurantes")
root.resizable(0,0)
root.iconphoto(False,PhotoImage(file="Icono Restaurante.png"))
root.config(bd=10)

# Empieza el programa mostrando la aplicación
menu_final()

# Bucle de la aplicación
root.mainloop()