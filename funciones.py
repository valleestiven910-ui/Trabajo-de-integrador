from entidades import vaca, usuario, finca, medicamento, costo, producción, factura
from Datos import lista_vacas, lista_finca, lista_usuario, lista_medicamento, lista_costo, lista_producción, lista_factura, lista_detalle_de_venta, lista_alimentación
#===========
#Registrar un usuario
#===========
def registrar_usuario(id_usuario, nombre, correo, contraseña, cedula, celular):
  if id_usuario is None:
    id_usuario = len(lista_usuario) + 1
    usuario_nuevo = usuario(
        id=id_usuario,
        nombre=nombre,
        cédula=cedula,
        celular=celular,
        correo=correo,
        contraseña=contraseña
    )
    lista_usuario.append(usuario_nuevo)
    return usuario_nuevo 


def listar_usuario():
    return lista_usuario

def buscar_usuario(id_usuario):
    for usuario_nuevo in lista_usuario:
        if usuario_nuevo.id_usuario==id_usuario:
            return usuario_nuevo
        return None

def eliminar_usuario(id_usuario):
    usuario_encontrado= buscar_usuario(id_usuario)
    if usuario_encontrado in lista_usuario:
         lista_usuario.remove(usuario_encontrado)
         return True
    return False

def iniciar_sesion(cédula, contraseña):
    for u in lista_usuario: 
        if u.cédula == cédula and u.contraseña == contraseña:
            return u
    return None 


#================
#Registrar la finca
# ============ 
def registrar_finca(id_finca, id_usuario, departamento, ubicacion, nombre_finca ):
       
       
        id_finca=len (lista_finca) + 1


        finca_a_registrar=finca(
            id_de_finca= int(id_finca),
            id_de_usuario=int(id_usuario),
            departamento=departamento,
            ubicación=ubicacion,
            nombre_de_la_finca=nombre_finca

        )

        lista_finca. append (finca_a_registrar)

def listar_fincas():
    return lista_finca

def buscar_finca(id_finca):
    for finca_a_registrar in lista_finca:
        if finca_a_registrar.id_finca==id_finca:
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
def registrar_vaca(id_vaca , id_finca, nombre_vaca,raza,peso,):

    id_vaca = len(lista_vacas) + 1
    vaca= vaca(
        id=int(id_vaca),
       id_finca=(id_finca),
        nombre=nombre_vaca,
        raza=raza,
        peso=float(peso),
    

    )
    lista_vacas.append(vaca)

def listar_vacas():
    return vaca

def buscar_vaca(id_vaca):
    for vaca in lista_vacas:
        if vaca.id_vaca==id_vaca:
            return vaca
        return None

def actualizar_vaca(id_vaca, id_finca, nombre_vaca, raza, peso, color ):
     vaca = buscar_vaca(id_vaca)

     if vaca :
         vaca.nombre=nombre_vaca,
         vaca.raza=raza,
         vaca.peso=peso,
         vaca.id_finca=id_finca,
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

def crear_factura(id_factura=None, monto_pagado=0.0, fecha="", id_vendedor=0, id_comprador=0):
    if id_factura is None:
        id_factura = len(lista_factura) + 1

    if any(factura_actual.id_factura == int(id_factura) for factura_actual in lista_factura):
        return False  # La factura ya existe, no se puede crear una nueva con el mismo ID

    factura_nueva = factura(
        id_factura=int(id_factura),
        monto_pagado=float(monto_pagado),
        fecha=fecha,
        id_vendedor=int(id_vendedor),
        id_comprador=int(id_comprador)
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

def eliminar_detalle(id_detalle):
    detalle_encontrado=buscar_detalle_de_venta(id_detalle)

    if detalle_encontrado:
        lista_detalle_de_venta.remove(detalle_encontrado)
        return True
    return False






#===========
#registro de medicamento
#==============
def registrar_medicamento(id_medicamento, id_vaca, remedio, fecha, peso_anterior_del_ganado, peso_actual_del_ganado, dosis_por_vacas):
    id_medicamento = len(lista_medicamento) + 1
    
    nuevo_medicamento = medicamento(
           id_medicamento = int(id_medicamento),
           id_vaca= int(id_vaca), 
           remedio = remedio,
           fecha = fecha,
           peso_anterior_del_ganado = float(peso_anterior_del_ganado),
           peso_actual_del_ganado = float(peso_actual_del_ganado),
           dosis_por_vacas = float (dosis_por_vacas)
       )

    lista_medicamento.append(nuevo_medicamento)
    return nuevo_medicamento

def listar_medicamento():
    return medicamento

def buscar_medicamento(id_medicamento):
    for nuevo_medicamento in lista_medicamento:
        if nuevo_medicamento.id_medicamento == id_medicamento:
            return nuevo_medicamento
        return None

    
def actualizar_medicamento(id_medicamento, id_vaca, remedio, fecha, peso_anterior_del_ganado, peso_actual_del_ganado, dosis_por_vacas):
        medicamento= buscar_medicamento(id_medicamento)


        if medicamento: 
            medicamento.id_medicamento = id_medicamento,
            medicamento.id_vaca = id_vaca,
            medicamento.remedio = remedio,
            medicamento.fecha = fecha,
            medicamento.peso_anterior_del_ganado = peso_anterior_del_ganado,
            medicamento.peso_actual_del_ganado = peso_actual_del_ganado,
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
        fecha = fecha
    )


    lista_producción.append (nueva_producción)
    return nueva_producción

def listar_producciones():
    return producción

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
    