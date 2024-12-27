import os
import re
from Transform_STN_Module import Parameter, Parameter_Format, Trajectory, Neighborhood

# Función para leer los archivos de una carpeta
def read_trajectories_files_folder(
    folder_path: str,
    file_extension: str
) -> list[str]:
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
    folder_path: str,
    file_extension: str,
    parameters_format: list[ Parameter_Format ],
    neighborhoods: list[ Neighborhood ]
) -> list[str]:
    """
    Convierte los archivos de trayectorias de irace en formato STN con vecindades.
    
    Args:
        folder_path (str): Ruta de la carpeta con los archivos de trayectorias de irace.
        file_extension (str): Extensión de archivo a buscar (por ejemplo, ".txt").
        parameters_format (list[]) : Formato de los parámetros del algoritmo, donde cada elemento contiene el diccionario con el nombre del parámetro y una lista de sus valores posibles. Si es un valor de tipo entero o flotante, contendrá un rango de valores.
        neighborhoods (Dict[str, List[Union[str, int, float]]]): 
            Diccionario con las vecindades de cada tipo de parámetro.
    
    Returns:
        List[str]: Lista de representaciones en formato STN para cada archivo.
    """
    # Leer los archivos desde la carpeta usando la función anterior
    file_paths = read_trajectories_files_folder(folder_path, file_extension)

    # Lista para almacenar las líneas de las trayectorias con la clase Trajectory
    trajectories_list = []

    # Lista para almacenar las líneas de los archivos de trayectorias
    stn_format_files_pre_neighborhood = [
        ["Run Fitness1 Solution1 Fitness2 Solution2"]
    ]

    # Expresión regular para capturar bloques entre paréntesis
    trayectory_pattern = r'\((.*?)\)'

    # Recorre todos los archivos encontrados
    for i, file_path in enumerate(file_paths):
        # Leer contenido del archivo
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Se procesa por cada linea del archivo
        for j, line in enumerate(lines):

            # Se omite la primera línea del archivo (encabezado)
            if (j == 0): continue

            # Se obtienen ambos bloques de configuraciones (origen y destino) y se almacenan en una lista como strings
            trajectory_blocks = re.findall(trayectory_pattern, line)
            if len(trajectory_blocks) != 2:
                raise ValueError(f"El archivo '{file_path}' no contiene dos bloques de trayectorias en la línea {j}.")

            # Se crea una nueva instancia de la clase Trajectory
            trajectory = Trajectory(trajectory_iteration=i+1)

            # Se procesa la configuración de origen
            origin_configurations = trajectory_blocks[0].split()
            origin_length =len(origin_configurations)
            for k, origin_value in enumerate(origin_configurations):
                if k == 0:
                    trajectory.set_origin_id(int(origin_value))
                elif k == origin_length - 3:
                    continue
                elif k == origin_length - 2:
                    trajectory.set_origin_iteration(int(origin_value))
                elif k == origin_length - 1:
                    trajectory.set_origin_value(float(origin_value))
                else:
                    param_index = k - 1
                    param_format = parameters_format[param_index]
                    param_name = param_format.get_name()
                    param_value = param_format.cast_parameter_value(origin_value)
                    parameter = Parameter(param_name, param_value)
                    trajectory.add_origin_parameter(parameter)
            
            # Se procesa la configuración de destino
            destination_configuration = trajectory_blocks[1].split()
            destination_length = len(destination_configuration)
            for k, destination_value in enumerate(destination_configuration):
                if k == 0:
                    trajectory.set_destination_id(int(destination_value))
                elif k == destination_length - 3:
                    continue
                elif k == destination_length - 2:
                    trajectory.set_destination_iteration(int(destination_value))
                elif k == destination_length - 1:
                    trajectory.set_destination_value(float(destination_value))
                else:
                    param_index = k - 1
                    param_format = parameters_format[param_index]
                    param_name = param_format.get_name()
                    param_value = param_format.cast_parameter_value(destination_value)
                    parameter = Parameter(param_name, param_value)
                    trajectory.add_destination_parameter(parameter)

            # Se añade la instancia de la clase Trajectory a la lista de líneas de trayectorias
            trajectories_list.append(trajectory)

        # Se añade la representación en formato STN a la lista de líneas de trayectorias previo al casteo de estas con vecinades
        stn_format_files_pre_neighborhood.append(trajectory.to_stn_format())
    
    # Iniciar lista para las representaciones en formato STN
    stn_format_files = []

    # Recorre todas las filas de trayectorias y hace el procesamiento al formato STN con las vecindades

    return stn_format_files
