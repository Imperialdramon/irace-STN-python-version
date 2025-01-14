import os, re, time
from .Trajectories_Classes import Parameter, Parameter_Format, Location_Format, Configuration

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
    # Validación de la carpeta
    if not os.path.isdir(folder_path):
        raise ValueError(f"La carpeta especificada '{folder_path}' no existe o no es válida.")

    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(file_extension)]

    return file_paths

# Función para convertir las trayectorias en formato STN con vecindades
def trajectories_to_stn_format(
    folder_path: str,
    file_extension: str,
    output_file_path: str,
    parameters_format: list[ Parameter_Format ],
    locations_format: list[ Location_Format ],
    quality_type: str,
    significant_digits: int,
    show_elites: bool
) -> list[str]:
    """
    Convierte los archivos de trayectorias de irace en formato STN con vecindades.
    
    Args:
        folder_path (str): Ruta de la carpeta con los archivos de trayectorias de irace.
        file_extension (str): Extensión de archivo a buscar (por ejemplo, ".txt").
        output_file_path (str): Ruta del archivo de salida en formato STN.
        parameters_format (list[]) : Formato de los parámetros del algoritmo, donde cada elemento contiene el diccionario con el nombre del parámetro y una lista de sus valores posibles. Si es un valor de tipo entero o flotante, contendrá un rango de valores.
        locations_format (list[]) : Formato de las locaciones del algoritmo, donde cada elemento contiene el diccionario con el nombre de la locación y una lista de sus valores posibles. Si es un valor de tipo entero o flotante, contendrá un rango de valores.
        quality_type (str) : Tipo de calidad a considerar para las locaciones, puede ser 'mean' para la media de las calidades de las configuraciones en una locación o 'best' para la mejor calidad de las configuraciones en una locación.
        significant_digits (int) : Cantidad de dígitos significativos a considerar para los valores de los parámetros y la calidad de las configuraciones.
        show_elites (bool) : Indica si se deben mostrar las configuraciones élites en el archivo STN.
    Returns:
        List[str]: Lista de representaciones en formato STN para cada archivo.
    """
    try:
        # Validación de tamaños de listas
        if len(parameters_format) == 0:
            raise ValueError("La lista de formatos de parámetros no puede estar vacía.")
        elif len(locations_format) == 0:
            raise ValueError("La lista de formatos de locaciones no puede estar vacía.")
        elif len(parameters_format) != len(locations_format):
            raise ValueError("La cantidad de formatos de parámetros y locaciones debe ser la misma.")

        # Validación de los formatos de los otros parámetros
        if quality_type not in ['mean', 'best']:
            raise ValueError(f"El tipo de calidad '{quality_type}' no es válido.")
        elif significant_digits < 0:
            raise ValueError("La cantidad de dígitos significativos no puede ser negativa.")
        elif not isinstance(show_elites, bool):
            raise ValueError("El valor de mostrar élites debe ser un valor booleano.")

        # Leer los archivos desde la carpeta usando la función anterior
        file_paths = read_trajectories_files_folder(folder_path, file_extension)
        
        # Lista resumida de configuraciones de origen y destino por cada archivo e iteraciones, indicado el código de la locación
        # Ejemplo: [archivo 1 [ iteración 1 [ (trayectoria 1), (trayectoria 2) ], iteración 2 [ (...) ], ...], archivo 2 [ (...), ...], ...]
        files_iterations_trajectory_list = []
        
        # Lista resumida de las id de las configuraciones élites por cada archivo e iteración
        # Ejemplo: [archivo 1 [ iteración 1 [ élite 1, élite 2, ... ], iteración 2 [ élite1, ... ], ...], archivo 2 [ (...), ...], ...]
        files_iterations_elites_list = []

        # Expresión regular para capturar bloques entre paréntesis -> (...) (...) -> [ '...', '...' ]
        # trayectory_pattern = r'\((.*?)\)'

        # Recorre todos los archivos encontrados
        for file_index, file_path in enumerate(file_paths):

            # Leer contenido del archivo
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Lista de locaciones de origen y destino por cada iteración, indicado el código de la locación para un archivo
            # Ejemplo: [ iteración 1 [ (trayectoria 1), (trayectoria 2) ], iteración 2 [ (...) ], ...]
            iterations_trajectory_list = []

            # Lista de configuraciones de origen y destino para una iteración
            # Ejemplo: [ (trayectoria 1), (trayectoria 2) ]
            trajectory_list = []

            # Contador de iteraciones
            iteration = 1

            print(f'Inicio del procesamiento del archivo {file_index + 1} de {len(file_paths)} lineas...')

            start_time = time.time()

            # Se procesa por cada linea del archivo
            for line_index, line in enumerate(lines):

                # Se omite la primera línea del archivo (encabezado)
                if (line_index == 0): continue

                # Se obtienen ambos bloques de configuraciones (origen y destino) y se almacenan en una lista como strings
                # trajectory_blocks = re.findall(trayectory_pattern, line)
                trajectory_blocks = line.split('|')
                if len(trajectory_blocks) != 2:
                    raise ValueError(f"El archivo '{file_path}' no contiene dos bloques de trayectorias en la línea {line_index}.")

                # Datos de la configuración de origen
                origin_configuration = trajectory_blocks[0].split()
                origin_length = len(origin_configuration)
                if origin_length != 4 + len(parameters_format):
                    raise ValueError(f"El archivo '{file_path}' no contiene la cantidad correcta de parámetros en la línea {line_index}.")

                # Se obtiene la información de la configuración de origen
                origin_id = int(origin_configuration[0])
                origin_parameters_pre_cast = origin_configuration[1:origin_length - 3]
                origin_parameters = []
                for k, origin_parameter_value in enumerate(origin_parameters_pre_cast):
                    origin_parameter_format = parameters_format[k]
                    origin_parameter_name = origin_parameter_format.get_name()
                    origin_parameter = Parameter(origin_parameter_name, origin_parameter_value)
                    origin_parameter.set_value(origin_parameter_format.cast_parameter_value(origin_parameter))
                    origin_parameters.append(origin_parameter)
                origin_elite_state = origin_configuration[origin_length - 3]
                origin_new_iteration = int(origin_configuration[origin_length - 2]) # Se asume que es la misma iteración que la configuración de destino
                origin_quality = float(origin_configuration[origin_length - 1])

                # Se actualiza la iteración si es necesario, actualizando la lista de trayectorias
                if origin_new_iteration > iteration + 1:
                    iteration += 1
                    iterations_trajectory_list.append(trajectory_list)
                    trajectory_list = []

                # Se crea la configuración de origen
                origin_configuration = Configuration(id=origin_id, run=file_index, iteration=iteration, parameters=origin_parameters, elite_state=origin_elite_state, quality=origin_quality, location_code='')
                
                # Datos de la configuración de destino
                destination_configuration = trajectory_blocks[1].split()
                destination_length = len(destination_configuration)
                if destination_length != 4 + len(parameters_format):
                    raise ValueError(f"El archivo '{file_path}' no contiene la cantidad correcta de parámetros en la línea {line_index}.")

                # Se obtiene la información de la configuración de destino
                destination_id = int(destination_configuration[0])
                destination_parameters_pre_cast = destination_configuration[1:destination_length - 3]
                destination_parameters = []
                for k, destination_parameter_value in enumerate(destination_parameters_pre_cast):
                    destination_parameter_format = parameters_format[k]
                    destination_parameter_name = destination_parameter_format.get_name()
                    destination_parameter = Parameter(destination_parameter_name, destination_parameter_value)
                    destination_parameter.set_value(destination_parameter_format.cast_parameter_value(destination_parameter))
                    destination_parameters.append(destination_parameter)
                destination_elite_state = destination_configuration[destination_length - 3]
                destination_new_iteration = int(destination_configuration[destination_length - 2]) # Se asume que es la misma iteración que la configuración de origen
                destination_quality = float(destination_configuration[destination_length - 1])

                # Se crea la configuración de destino
                destination_configuration = Configuration(id=destination_id, run=file_index, iteration=iteration + 1, parameters=destination_parameters, elite_state=destination_elite_state, quality=destination_quality, location_code='')

                # Se añade la trayectoria a la lista
                trajectory_list.append((origin_configuration, destination_configuration))

            # Se identifica como élites las configuraciones de destino de la última iteración
            for _, destination_configuration in trajectory_list:
                destination_configuration.set_elite_state('e')

            # Se añade la lista de trayectorias de la última iteración
            iterations_trajectory_list.append(trajectory_list)

            iteration += 1

            # Se añade la lista de trayectorias por archivo
            files_iterations_trajectory_list.append(iterations_trajectory_list)

        end_time = time.time()

        print(f'Fin del procesamiento de los archivos. Tiempo total: {end_time - start_time} segundos.')

        # --------------------------------------------------------------------------------------------------

        print('Inicio del proceso de generación de locaciones...')

        start_time = time.time()

        # Diccionario global de locaciones con las configuraciones que pertenecen a cada una de estas
        # Ejemplo: { locación: [ Configuración, ... ], ... }
        locations_dict = {}

        # Se recorre la lista de configuraciones por archivo y se generan los códigos de locaciones
        for iterations_trajectory_list in files_iterations_trajectory_list:
            for trajectory_list in iterations_trajectory_list:
                for origin_configuration, destination_configuration in trajectory_list:

                    # Se calcula el código de locación de origen
                    origin_location_code = origin_configuration.generate_location_code(parameters_format, locations_format)

                    # Se añade la configuración de origen al diccionario de locaciones
                    if origin_location_code not in locations_dict:
                        locations_dict[origin_location_code] = [origin_configuration]
                    else:
                        locations_dict[origin_location_code].append(origin_configuration)

                    # Se calcula el código de locación de destino
                    destination_location_code = destination_configuration.generate_location_code(parameters_format, locations_format)

                    # Se añade la configuración de destino al diccionario de locaciones
                    if destination_location_code not in locations_dict:
                        locations_dict[destination_location_code] = [destination_configuration]
                    else:
                        locations_dict[destination_location_code].append(destination_configuration)

        end_time = time.time()

        print(f'Fin del proceso de generación de locaciones. Tiempo total: {end_time - start_time} segundos.')

        # --------------------------------------------------------------------------------------------------

        print('Inicio del proceso de cálculo de calidad de locaciones...')

        start_time = time.time()

        # Diccionario de las calidades y estado de élite de las locaciones calculadas
        # Ejemplo: { locación: [calidad, estado elite], ... }
        locations_quality_dict = {}

        # Se calcula la calidad de las locaciones
        for location_code, configurations in locations_dict.items():

            # Se calcula la calidad de la locación según el tipo de calidad
            if quality_type == 'best': # Se toma la mejor calidad de las configuraciones en la locación
                quality = max([configuration.get_quality() for configuration in configurations])
            elif quality_type == 'mean': # Se toma la media de las calidades de las configuraciones en la locación
                quality = sum([configuration.get_quality() for configuration in configurations]) / len(configurations)
            else:
                raise ValueError(f"El tipo de calidad '{quality_type}' no es válido.")

            # Se revisa si alguna de las configuraciones es élite
            elite = 'e' if any([configuration.get_elite_state() == 'e' for configuration in configurations]) else 'ne'

            locations_quality_dict[location_code] = [quality, elite]

        end_time = time.time()
        
        print(f'Fin del proceso de cálculo de calidad de locaciones. Tiempo total: {end_time - start_time} segundos.')
        
        # --------------------------------------------------------------------------------------------------
        
        print('Inicio del proceso de generación del archivo en formato STN...')
        
        start_time = time.time()

        # Lista de archivos en formato STN
        stn_format_files = []
        if show_elites:
            stn_format_files.append("Run Fitness1 Solution1 Elite1 Fitness2 Solution2 Elite2")
        else:
            stn_format_files.append("Run Fitness1 Solution1 Fitness2 Solution2")

        # Se realiza la creación de la lista en formato STN
        for file_index, iterations_trajectory_list in enumerate(files_iterations_trajectory_list):
            for trajectory_list in iterations_trajectory_list:
                for origin_configuration, destination_configuration in trajectory_list:

                    # Se obtiene el índice de la run
                    run = file_index + 1

                    # Se obtienen los códigos de locación de origen y destino
                    origin_location_code = origin_configuration.get_location_code()
                    destination_location_code = destination_configuration.get_location_code()

                    # Se obtienen las calidades de las locaciones (con la cantidad de dígitos significativos)
                    if significant_digits == 0:
                        quality1 = str(int(locations_quality_dict[origin_location_code][0]))
                        quality2 = str(int(locations_quality_dict[destination_location_code][0]))
                    else:
                        quality1 = f'{locations_quality_dict[origin_location_code][0]:.{significant_digits}f}'
                        quality2 = f'{locations_quality_dict[destination_location_code][0]:.{significant_digits}f}'
                    
                    # Se obtienen los estados élites de las configuraciones
                    elite1 = 'T' if locations_quality_dict[origin_location_code][1] == "e" else 'F'
                    elite2 = 'T' if locations_quality_dict[destination_location_code][1] == "e" else 'F'

                    # Se añade la línea al archivo en formato STN con o sin élites
                    if show_elites:
                        stn_format_files.append(f'{run} {quality1} {origin_location_code} {elite1} {quality2} {destination_location_code} {elite2}')
                    else:
                        stn_format_files.append(f'{run} {quality1} {origin_location_code} {quality2} {destination_location_code}')
        
        end_time = time.time()

        print(f'Fin del proceso de generación del archivo en formato STN. Tiempo total: {end_time - start_time} segundos.')

        # --------------------------------------------------------------------------------------------------

        # Escritura del archivo con el nombre indicado
        with open(output_file_path, 'w') as file:
            for line in stn_format_files:
                file.write(line + '\n')

        return stn_format_files
    except Exception as e:
        print(f'Error en la conversión de las trayectorias a formato STN: {e}')
        return []
    finally:
        print('Fin del proceso de conversión de las trayectorias a formato STN.')

# TODO: Aprovechar la información adicional recopilada en la ejecución para obtener otras cosas

# TODO: Modificar repo con la generación de archivos de trayectorias para que almacenen la información de las élites bien
# TODO: Cambiar el formato de las filas del archivo de trayectorias separando por un valor de tipo | o similar (por simplicidad)
