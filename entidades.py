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
    peso_anterior_del_ganado : float
    peso_actual_del_ganado : float
    dosis_por_vacas: str

@dataclass
class costo :
    id_costos: int
    id_vaca: int
    fecha: str
    precio: float
    decripción: str

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
    cantidad: float
    fecha: str
