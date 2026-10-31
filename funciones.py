from entidades import vaca, usuario, finca, medicamento, costo, producción, factura, alimentación
from Datos import lista_vacas, lista_finca, lista_usuario, lista_medicamento, lista_costo, lista_producción, lista_factura, lista_detalle_de_venta, lista_alimentación
#===========
#Registrar un usuario
#===========
def registrar_usuario(id_usuario=None, nombre="", correo="", contraseña="", cedula="", celular="", apellidos=""):
    try:
        id_usuario = len(lista_usuario) + 1 if id_usuario is None else int(id_usuario)
    except (TypeError, ValueError) as error:
        raise ValueError("El ID de usuario debe ser un número entero.") from error

    nombre = str(nombre or "").strip()
    apellidos = str(apellidos or "").strip()
    cedula = str(cedula or "").strip()
    celular = str(celular or "").strip()
    contraseña = str(contraseña or "")
    if id_usuario <= 0 or not nombre or not apellidos or not cedula or not celular or not contraseña:
        raise ValueError("Completa nombre, apellidos, cédula, celular y contraseña.")
    if any(registrado.id_usuario == id_usuario or registrado.cedula == cedula for registrado in lista_usuario):
        raise ValueError("Ya existe un usuario con ese ID o cédula.")

    usuario_nuevo = usuario(
        id_usuario=id_usuario,
        nombres=nombre,
        apellidos=apellidos,
        cedula=cedula,
        celular=celular,
        contraseña=contraseña,
    )
    lista_usuario.append(usuario_nuevo)
    return usuario_nuevo


def listar_usuario():
    return lista_usuario

def buscar_usuario(id_usuario):
    try:
        id_usuario = int(id_usuario)
    except (TypeError, ValueError):
        return None
    for usuario_nuevo in lista_usuario:
        if usuario_nuevo.id_usuario == id_usuario:
            return usuario_nuevo
    return None

def eliminar_usuario(id_usuario):
    usuario_encontrado= buscar_usuario(id_usuario)
    if usuario_encontrado in lista_usuario:
         lista_usuario.remove(usuario_encontrado)
         return True
    return False

def iniciar_sesion(cédula, contraseña):
    cedula_ingresada = str(cédula or "").strip()
    contraseña_ingresada = str(contraseña or "")
    for u in lista_usuario:
        if u.cedula == cedula_ingresada and u.contraseña == contraseña_ingresada:
            return u
    return None 


#================
#Registrar la finca
# ============ 
def registrar_finca(id_finca=None, id_usuario=None, departamento="", ubicacion="", nombre_finca=""):
    try:
        id_usuario = int(id_usuario)
    except (TypeError, ValueError) as error:
        raise ValueError("Selecciona un usuario dueño válido.") from error

    if buscar_usuario(id_usuario) is None:
        raise ValueError("Registra primero al usuario que será dueño de la finca.")
    departamento = str(departamento or "").strip()
    ubicacion = str(ubicacion or "").strip()
    nombre_finca = str(nombre_finca or "").strip()
    if not departamento or not ubicacion or not nombre_finca:
        raise ValueError("Departamento, ubicación y nombre de finca son obligatorios.")

    nueva_finca = finca(
        id_finca=len(lista_finca) + 1,
        id_usuario=id_usuario,
        departamento=departamento,
        ubicación=ubicacion,
        nombre_finca=nombre_finca,
    )
    lista_finca.append(nueva_finca)
    return nueva_finca

def listar_fincas():
    return lista_finca

def buscar_finca(id_finca):
    try:
        id_finca = int(id_finca)
    except (TypeError, ValueError):
        return None
    for finca_a_registrar in lista_finca:
        if finca_a_registrar.id_finca == id_finca:
            return finca_a_registrar
    return None

def actualizar_usuario(id_finca, departamento, ubicacion, raza, nombre_finca):
     usuario = buscar_usuario(id_finca)

     if usuario :
         usuario.id_finca=id_finca,
         usuario.departamento=departamento,
         usuario.ubicación=ubicacion,
         usuario.raza=raza,
         usuario.nombre_finca=nombre_finca
         return True
     return False

def eliminar_finca(id_finca):
     finca_encontrada= buscar_finca(id_finca)

     if finca_encontrada:
            lista_finca.remove(finca_encontrada)
            return True

#==========
#Registrar una vaca 
#===========
def registrar_vaca(id_usuario, id_finca, nombre_vaca, raza, color, peso, imagen="", en_catalogo=False):
    try:
        id_usuario = int(id_usuario)
        id_finca = int(id_finca)
        peso = float(peso)
    except (TypeError, ValueError) as error:
        raise ValueError("Los IDs deben ser enteros y el peso debe ser numérico.") from error

    if id_usuario <= 0 or id_finca <= 0:
        raise ValueError("Los IDs de usuario y finca deben ser mayores que cero.")
    if buscar_usuario(id_usuario) is None:
        raise ValueError("Registra primero al usuario dueño de la vaca.")
    finca_vaca = buscar_finca(id_finca)
    if finca_vaca is None:
        raise ValueError("Selecciona una finca registrada.")
    if finca_vaca.id_usuario != id_usuario:
        raise ValueError("La finca seleccionada pertenece a otro usuario.")
    nombre_vaca = str(nombre_vaca or "").strip()
    raza = str(raza or "").strip()
    color = str(color or "").strip()
    imagen = str(imagen or "").strip()
    if not nombre_vaca or not raza or not color:
        raise ValueError("Nombre, raza y color son obligatorios.")
    if peso <= 0:
        raise ValueError("El peso debe ser mayor que cero.")

    nueva_vaca = vaca(
        id_vaca=len(lista_vacas) + 1,
        id_usuario=id_usuario,
        id_finca=id_finca,
        nombre_vaca=nombre_vaca,
        raza=raza,
        color=color,
        peso=peso,
        imagen=imagen,
        en_catalogo=bool(en_catalogo),
    )
    lista_vacas.append(nueva_vaca)
    return nueva_vaca

def listar_vacas():
    return lista_vacas

def buscar_vaca(id_vaca):
    for vaca in lista_vacas:
        if vaca.id_vaca == int(id_vaca):
            return vaca
    return None

def actualizar_vaca(id_vaca, id_usuario, id_finca, nombre_vaca, raza, peso, color ):
     vaca = buscar_vaca(id_vaca)

     if vaca :
         vaca.id_vaca=id_vaca,
         vaca.id_usuario=id_usuario,
         vaca.id_finca=id_finca,
         vaca.nombre=nombre_vaca,
         vaca.raza=raza,
         vaca.peso=peso,
         
         vaca.color=color
         return True
     return False

def eliminar_vaca(id_vaca):
    vaca_encontrada= buscar_vaca(id_vaca)

    if vaca_encontrada:
        lista_vacas.remove(vaca_encontrada)
        return True
    return False

#============
#Costo
#===========
def regitrar_costo(id_costo, id_finca, nombre_costo, valor):


    id_costo = len(lista_costo) + 1

    costo_nuevo = costo(
        id= int(id_costo),
        id_finca=(id_finca),
        nombre=nombre_costo,
        valor=float(valor)
    )
    lista_costo.append(costo_nuevo)


def listar_costos():
    return lista_costo


def registrar_costo_vaca(id_vaca, descripcion, fecha, precio):
    try:
        id_vaca = int(id_vaca)
        precio = float(precio)
    except (TypeError, ValueError) as error:
        raise ValueError("El ID de vaca debe ser entero y el precio debe ser numérico.") from error

    if buscar_vaca(id_vaca) is None:
        raise ValueError("No se encontró la vaca seleccionada.")
    descripcion = str(descripcion or "").strip()
    fecha = str(fecha or "").strip()
    if not descripcion or not fecha:
        raise ValueError("La descripción y la fecha son obligatorias.")
    if precio <= 0:
        raise ValueError("El precio debe ser mayor que cero.")

    nuevo_costo = costo(
        id_costos=len(lista_costo) + 1,
        id_vaca=id_vaca,
        fecha=fecha,
        precio=precio,
        descripcion=descripcion,
    )
    lista_costo.append(nuevo_costo)
    return nuevo_costo

def buscar_costo(id_costo):
    for costo_nuevo in lista_costo:
        if costo_nuevo.id_costo==id_costo:
            return costo_nuevo
        return None

def  actualizar_costo(id_costo, id_finca, nombre_costo, valor):
    costo = buscar_costo(id_costo)

    if costo:
        costo.id_costo=id_costo,
        costo.id_finca=id_finca,
        costo.nombre=nombre_costo,
        costo.valor=valor
        return True
    return False

def eliminar_costo(id_costo):
    costo_encontrado= buscar_costo(id_costo)

    if costo_encontrado:
        lista_costo.remove(costo_encontrado)
        return True
    return False

def comparar_costos_por_vaca(id_finca):
    costos_encontrados = []
    for costo_nuevo in lista_costo:
        if costo_nuevo.id_finca == id_finca:
            costos_encontrados.append(costo)
    return costos_encontrados


#====================
#factura
#================

def crear_factura(
    id_factura=None,
    monto_pagado=0.0,
    fecha="",
    id_vendedor=0,
    id_comprador=0,
    id_vaca=None,
    nombre_comprador="",
    cedula_comprador="",
    nombre_vendedor="",
    cedula_vendedor="",
):
    if id_factura is None:
        id_factura = len(lista_factura) + 1

    if any(factura_actual.id_factura == int(id_factura) for factura_actual in lista_factura):
        return False  # La factura ya existe, no se puede crear una nueva con el mismo ID

    factura_nueva = factura(
        id_factura=int(id_factura),
        monto_pagado=float(monto_pagado),
        fecha=fecha,
        ID_vendedor=int(id_vendedor),
        ID_comprador=int(id_comprador),
        id_vaca=int(id_vaca) if id_vaca is not None else None,
        nombre_comprador=nombre_comprador,
        cedula_comprador=cedula_comprador,
        nombre_vendedor=nombre_vendedor,
        cedula_vendedor=cedula_vendedor,
    )

    lista_factura.append(factura_nueva)
    return factura_nueva

def listar_factura():
    return lista_factura

def buscar_factura(id_factura):
    for factura_nueva in lista_factura:
        if factura_nueva.id_factura==id_factura:
            return factura_nueva
        return None

def actualizar_factura(id_factura, monto_pagado, fecha, id_vendedor, id_comprador):
     factura_nueva= buscar_factura (id_factura)



     if factura_nueva:
         factura_nueva.id_factura=id_factura,
         factura_nueva.monto_pagado= monto_pagado,
         factura_nueva.fecha= fecha,
         factura_nueva.id_vendedor=id_vendedor,
         factura_nueva.id_comprador= id_comprador
         return True
     return False

    
def eliminar_factura(id_factura):
    factura_encontrada=buscar_factura(id_factura)

    if factura_encontrada:
        lista_factura.remove(factura_encontrada)
        return True
    return False




#========================
#detalle de la venta
#========================

def crear_descripción_de_la_venta(id_detalle, id_vaca, cantidad, precio):
    id_detalle = len(lista_detalle_de_venta ) + 1

    detalle = lista_detalle_de_venta(
        id_detalle=int(id_detalle),
        id_vaca= int(id_vaca),
        cantidad= int(cantidad),
        precio= float(precio)
    )


    lista_detalle_de_venta.append(detalle)
    return detalle

def historial_detalle():
    return lista_detalle_de_venta



def buscar_detalle_de_venta(id_detalle):
    for detalle_nuevo in lista_detalle_de_venta:

        if detalle_nuevo.id_detalle==id_detalle:
            return detalle_nuevo
        return None

def actualiza_detalle(id_detalle, id_vaca, cantidad, precio):
    detalle_nuevo= buscar_detalle_de_venta(id_detalle)


    if detalle_nuevo:
        detalle_nuevo.id_detalle=id_detalle,
        detalle_nuevo.id_vaca=id_vaca,
        detalle_nuevo.cantidad=cantidad,
        detalle_nuevo.precio=precio

        return True
    return False
def listar_detalle_de_venta():
    return lista_detalle_de_venta


def eliminar_detalle(id_detalle):
    detalle_encontrado=buscar_detalle_de_venta(id_detalle)

    if detalle_encontrado:
        lista_detalle_de_venta.remove(detalle_encontrado)
        return True
    return False






#===========
#registro de medicamento
#==============
def registrar_medicamento(id_medicamento, id_vaca, remedio, fecha, peso_anterior_de_la_vaca, peso_actual_de_la_vaca, dosis_por_vacas):
    id_medicamento = len(lista_medicamento) + 1
    
    nuevo_medicamento = medicamento(
           id_medicamento = int(id_medicamento),
           id_vaca= int(id_vaca), 
           remedio = remedio,
           fecha = fecha,
           peso_anterior_del_ganado = float(peso_anterior_de_la_vaca),
           peso_actual_del_ganado = float(peso_actual_de_la_vaca),
           dosis_por_vacas = float (dosis_por_vacas)
       )

    lista_medicamento.append(nuevo_medicamento)
    return nuevo_medicamento

def listar_medicamento():
    return lista_medicamento

def buscar_medicamento(id_medicamento):
    for nuevo_medicamento in lista_medicamento:
        if nuevo_medicamento.id_medicamento == id_medicamento:
            return nuevo_medicamento
        return None

    
def actualizar_medicamento(id_medicamento, id_vaca, remedio, fecha, peso_anterior_de_la_vaca, peso_actual_de_la_vaca, dosis_por_vacas):
        medicamento= buscar_medicamento(id_medicamento)


        if medicamento: 
            medicamento.id_medicamento = id_medicamento,
            medicamento.id_vaca = id_vaca,
            medicamento.remedio = remedio,
            medicamento.fecha = fecha,
            medicamento.peso_anterior_del_ganado = peso_anterior_de_la_vaca,
            medicamento.peso_actual_del_ganado = peso_actual_de_la_vaca,
            medicamento.dosis_por_vacas = dosis_por_vacas

            return True
        return False

def eliminar_medicamento(id_medicamento):
    medicamento_encontrado= buscar_medicamento(id_medicamento)


    if medicamento_encontrado:
        lista_medicamento.remove(medicamento_encontrado)
        return True
    return False




#=========
#producción
#=========
def registrar_producción(id_producción, id_vaca, cantidad, Litros, fecha):
    id_producción = len(lista_producción) + 1

    nueva_producción = producción(
        id_producción = int(id_producción),
        id_vaca = int(id_vaca),
        cantidad = int(cantidad),
        Litros = float (Litros),
        fecha = float(fecha)
    )


    lista_producción.append (nueva_producción)
    return nueva_producción

def listar_producciones():
    return lista_producción

def buscar_producción(id_producción):
    for nueva_producción in lista_producción:

        if nueva_producción.id_producción==id_producción:
            return nueva_producción

def actualizar_producción(id_producción, id_vaca, cantidad, Litros, fecha):
    nueva_producción= buscar_producción(id_producción)


    if nueva_producción:
        producción.id_producción=id_producción,
        producción.id_vaca=id_vaca,
        producción.cantidad=cantidad,
        producción.Litros=Litros,
        producción.fecha=fecha
        return True
    return False





def eliminar_producción(id_producción):
    producción_encontrada= buscar_producción(id_producción)
    if producción_encontrada:
        lista_producción.remove(producción_encontrada)
        return True
    return False



def registrar_alimentación(id_alimentación, tipo_de_alimento, descripción, cantidad, fecha, costo_alimento, id_vaca=None):

    id_alimentación = len(lista_alimentación) +1

    nueva_alimentación = alimentación (
        id_alimentación=int(id_alimentación),
        tipo_de_alimento=tipo_de_alimento,
        descripción=descripción,
        cantidad= float(cantidad),
        fecha=float(fecha),
        costo_alimento=float(costo_alimento),
        id_vaca=int(id_vaca) if id_vaca else None
    )


    lista_producción.append (nueva_alimentación)
    return nueva_alimentación


def listar_alimentación():
    return lista_alimentación


def buscar_alimentación(id_alimentación):
    for nueva_alimentación in lista_producción:

        if nueva_alimentación.id_alimentación==id_alimentación:
            return nueva_alimentación

def actualizar_alimentación(id_alimentación, tipo_de_alimento, descripción, cantidad, fecha, costo_alimento):
    nueva_alimentación= buscar_alimentación(id_alimentación)


    if nueva_alimentación:
        alimentación.id_alimentación=id_alimentación,
        alimentación.tipo_de_alimento=tipo_de_alimento,
        alimentación.descripción=descripción,
        alimentación.cantidad=cantidad,
        alimentación.fecha=fecha,
        alimentación.costo_alimento=costo_alimento
        return True
    return False


def eliminar_alimentación(id_alimentación):
    alimentación_encontrada= buscar_alimentación(id_alimentación)

    if alimentación_encontrada:
        lista_alimentación.remove(alimentación_encontrada)
        return True
    return False

def listar_vacas_en_catalogo():
    todas_las_vacas = lista_vacas

    vacas_seleccionadas = [v for v in todas_las_vacas if v.en_catalogo==True]

    return vacas_seleccionadas

def actualizar_estado_y_foto_catalogo(id_vaca, en_catalogo, imagen):
    vaca_encontrada = buscar_vaca(id_vaca)
    if vaca_encontrada: 
        vaca_encontrada.en_catalogo = en_catalogo
        vaca_encontrada.imagen =imagen
        return True
    return False
    