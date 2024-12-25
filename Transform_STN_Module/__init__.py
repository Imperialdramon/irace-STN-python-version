# Transform_STN_Module/__init__.py

# Importa funciones específicas de módulo de funciones de asignación de eventos
from .Trajectories_Interpreter import trajectories_to_stn_format

__all__ = [
    'trajectories_to_stn_format',
]