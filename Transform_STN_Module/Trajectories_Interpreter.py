import os
from typing import List, Dict, Union

# Función para leer los archivos de una carpeta
def read_trajectories_files_folder(
    folder_path: str,
    file_extension: str
) -> List[str]:
    """
    Lee los archivos en una carpeta con una extensión específica y devuelve sus rutas completas.
    
    Args:
        folder_path (str): Ruta de la carpeta con los archivos.
        file_extension (str): Extensión de archivo a buscar (por ejemplo, ".txt").
    
    Returns:
        List[str]: Lista con las rutas completas de los archivos encontrados.
    """
    if not os.path.isdir(folder_path):
        raise ValueError(f"La carpeta especificada '{folder_path}' no existe o no es válida.")
    
    file_paths = [
        os.path.join(folder_path, file)
        for file in os.listdir(folder_path)
        if file.endswith(file_extension)
    ]
    
    return file_paths

# Función para convertir las trayectorias en formato STN con vecindades
def trajectories_to_stn_format(
    file_paths: List[str],
    neighborhoods: Dict[str, List[Union[str, int, float]]]
) -> List[str]:
    """
    Convierte los archivos de trayectorias de irace en formato STN con vecindades.
    
    Args:
        file_paths (List[str]): Lista con las rutas de los archivos de trayectorias de irace.
        neighborhoods (Dict[str, List[Union[str, int, float]]]): 
            Diccionario con las vecindades de cada tipo de parámetro.
    
    Returns:
        List[str]: Lista de representaciones en formato STN para cada archivo.
    """
    stn_format_files = []
    
    for file_path in file_paths:
        # Leer contenido del archivo (aquí se espera que sea texto)
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Convertir contenido según neighborhoods (lógica personalizada según tus necesidades)
        # Aquí puedes definir cómo se transforma `content` con base en `neighborhoods`
        # Por ahora, simplemente añadimos el contenido con un mensaje para ejemplo.
        transformed_content = f"STN Format for {file_path} with neighborhoods {neighborhoods}"
        stn_format_files.append(transformed_content)
    
    return stn_format_files
