from dataclasses import dataclass

@dataclass
class vaca:
    id_vaca:int
    id_usuario: int
    id_finca:int
    nombre_vaca: str
    raza: str
    color: str
    peso: float
    imagen: str = ""
    en_catalogo: bool = False

@dataclass
class usuario:
    id_usuario: int
    nombres: str
    apellidos:str
    cedula: str
    celular: str
    contraseña: str

@dataclass
class finca:
    id_finca: int
    id_usuario:int
    departamento: str
    ubicación: str
    nombre_finca: str 
    


@dataclass
class medicamento:
    id_medicamento: int 
    id_vaca: int
    remedio: str
    fecha: str
    peso_anterior_de_la_vaca : float
    peso_actual_de_la_vaca: float
    dosis_por_vacas: str

@dataclass
class costo :
    id_costos: int
    id_vaca: int
    fecha: str
    precio: float
    descripcion: str

@dataclass
class producción :
    id_producción: int
    id_vaca: int    
    cantidad: int
    Litros: int
    fecha: str

@dataclass
class factura :
    id_factura: int 
    monto_pagado: float
    fecha: str
    ID_vendedor: int
    ID_comprador: int
    id_vaca: int | None = None
    nombre_comprador: str = ""
    cedula_comprador: str = ""
    nombre_vendedor: str = ""
    cedula_vendedor: str = ""

@dataclass
class detalle_de_venta:
    id_detalle: int
    id_vaca: int
    peso: float
    precio: float

@dataclass
class alimentación:
    id_alimentacion: int
    tipo_de_alimento: str
    descripción: str
    cantidad: float
    fecha: str
    costo_alimento: float
    id_vaca: int | None


@dataclass
class catalogo:
    id_vaca: int
    nombre: str
    imagen: str
    peso: float
    preció: float
    en_catalogo: bool= False