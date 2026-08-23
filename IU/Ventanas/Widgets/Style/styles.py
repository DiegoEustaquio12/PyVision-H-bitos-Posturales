class Colores:
    FONDO_TARJETA = "rgba(255,255,255,40)"
    FONDO_TARJETA_HOVER = "rgba(255,255,255,60)"
    BORDE_NORMAL = "rgba(255,255,255,80)"
    BORDE_SESION = "yellow"
    BORDE_COMPLETADA = "green"
    TEXTO_COMPLETADA = "rgba(255,255,255,120)"
    BOTON_AGREGAR = "#23614a"
    BOTON_AGREGAR_HOVER = "#3a8066"
    BOTON_AGREGAR_PRESSED = "#3d9e7a"


def estilo_tarea_normal() -> str:
    return f'''
    QFrame{{
        background-color: {Colores.FONDO_TARJETA};
        border: 1px solid {Colores.BORDE_NORMAL};
        border-radius: 14px;
    }}
    QFrame::hover {{
        background-color: {Colores.FONDO_TARJETA_HOVER};
        border-radius: 14px;
    }}
    '''

def estilo_tarea_en_sesion() -> str:
    return f'''
    QFrame{{
        background-color: {Colores.FONDO_TARJETA};
        border: 3px solid {Colores.BORDE_SESION};
        border-radius: 14px;
    }}
    QFrame::hover {{
        background-color: {Colores.FONDO_TARJETA_HOVER};
        border-radius: 14px;
    }}
    '''

def estilo_tarea_completada() -> str:
    return f'''
    QFrame{{
        background-color: transparent;
        border: 1px solid {Colores.BORDE_COMPLETADA};
        border-color: {Colores.BORDE_COMPLETADA};
        border-radius: 14px;
    }}
    '''

def estilo_label_normal() -> str:
    return '''
    font-size:12px;
    border-color: transparent;
    font-weight:bold;
    background-color: transparent;
    '''

def estilo_label_completada() -> str:
    return f'''
    font-size:12px;
    border-color: transparent;
    font-weight:bold;
    background-color: transparent;
    color: {Colores.TEXTO_COMPLETADA};
    text-decoration: line-through;
    '''