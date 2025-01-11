class Parameter:
    # Constructor de la clase
    def __init__(self, name: str, value: str | int | float | None):
        """
        Constructor de la clase Parameter.
        
        Args:
            name: Nombre del parámetro
            value: Valor del parámetro
        """
        self.name = name
        self.value = value

    # Método para obtener el nombre del parámetro
    def get_name(self) -> str:
        return self.name

    # Método para obtener el valor del parámetro
    def get_value(self) -> str | int | float | None:
        return self.value

    # Método para establecer el nombre del parámetro
    def set_name(self, name: str):
        self.name = name
    
    # Método para establecer el valor del parámetro
    def set_value(self, value: str | int | float | None):
        self.value = value

class Parameter_Format:
    # Constructor de la clase
    def __init__(self, name: str = "", type: str = "", value_type: str = "", possible_values: list[str | int | float] = []):
        """
        Constructor de la clase Parameter_Format.
        
        Args:
            name: Nombre del parámetro
            type: Tipo del parámetro (string -> s, integer -> i, float -> f)
            value_type: Tipo de los valores del parámetro (categorical -> c, numerical (real|integer) -> r | i, ordinal -> o)
            possible_values: Valores posibles del parámetro (lista de strings, enteros o flotantes)
        """
        self.name = name
        self.type = type
        self.value_type = value_type
        self.possible_values = possible_values

    # Método para obtener la representación de la clase como string
    def __repr__(self):
        return f"Parameter: {self.name} - Type: {self.type} - Possible Values: {self.possible_values}"

    # Método para obtener el nombre del parámetro
    def get_name(self) -> str:
        return self.name

    # Método para obtener los valores posibles del parámetro
    def get_type(self) -> str:
        return self.type
    
    # Método para obtener el tipo de los valores del parámetro
    def get_value_type(self) -> str:
        return self.value_type

    # Método para obtener los valores posibles del parámetro
    def get_possible_values(self) -> list[str | int | float]:
        return self.possible_values

    # Método para establecer el nombre del parámetro
    def set_name(self, name: str):
        self.name = name

    # Método para establecer el tipo del parámetro
    def set_type(self, type: str):
        self.type = type

    # Método para establecer el tipo de los valores del parámetro
    def set_value_type(self, value_type: str):
        self.value_type = value_type

    # Método para establecer los valores posibles del parámetro
    def set_possible_values(self, possible_values: list[str | int | float]):
        self.possible_values = possible_values

    # Método para obtener el valor de un parámetro en el formato correcto
    def cast_parameter_value(self, parameter: Parameter) -> str | int | float | None:
        try:
            # Verifica si el nombre del parámetro coincide
            if parameter.get_name() != self.name:
                raise ValueError(f"El nombre del parámetro {parameter.get_name()} no coincide con {self.name}")

            value = parameter.get_value()

            # Parámetro string
            if self.type == 's':

                value = str(value)

                # Verifica si el valor está en los valores posibles
                if self.value_type in ['c', 'o'] and value not in self.possible_values:
                    raise ValueError(f"El valor {value} no está en los valores posibles del parámetro {self.name}")

                return value

            # Parámetro entero
            elif self.type == "i":

                # Verifica si el valor es "NA"
                if value == "NA":
                    return None

                value = int(value)

                # Verifica si el valor está en los valores posibles
                if self.value_type in ['c', 'o'] and value not in self.possible_values:
                    raise ValueError(f"El valor {value} no está en los valores posibles del parámetro {self.name}")

                # Verifica si el valor está en el rango de valores posibles
                elif self.value_type in ['r', 'i'] and not (value >= self.possible_values[0] and value <= self.possible_values[1]):
                    raise ValueError(f"El valor {value} no está en el rango de valores posibles del parámetro {self.name}")

                return value

            # Parámetro flotante
            elif self.type == "f":

                # Verifica si el valor es "NA"
                if value == "NA":
                    return None

                value = float(value)

                # Verifica si el valor está en los valores posibles
                if self.value_type in ['c', 'o'] and value not in self.possible_values:
                    raise ValueError(f"El valor {value} no está en los valores posibles del parámetro {self.name}")

                # Verifica si el valor está en el rango de valores posibles
                elif self.value_type in ['r', 'i'] and not (value >= self.possible_values[0] and value <= self.possible_values[1]):
                    raise ValueError(f"El valor {value} no está en el rango de valores posibles del parámetro {self.name}")

                return value
            else:
                raise ValueError(f"Tipo no soportado: {self.type}")
        except ValueError as e:
            raise ValueError(f"Error en el casteo de parámetro '{parameter.get_name()}': {e}")

class Location_Format:
    """
    Clase para definir el formato de un parámetro.
    
    Attributes:
        name: Nombre del parámetro
        location_caster: Diccionario con los valores de casteo de locación para categorías y ordinales o lista con el valor que los subrangos de valores numéricos y la significancia
    """
    # Constructor de la clase
    def __init__(self, name: str = "", location_caster: dict[str] | list[int | float] = {} ):
        self.name = name
        self.location_caster = location_caster
    
    # Método para obtener el nombre del parámetro
    def get_name(self) -> str:
        return self.name

    # Método para obtener los valores de casteo de locación del parámetro
    def get_location_caster(self) -> dict[str] | list[int | float]:
        return self.location_caster

    # Método para establecer el nombre del parámetro
    def set_name(self, name: str):
        self.name = name

    # Método para establecer los valores de casteo de locación del parámetro
    def set_location_caster(self, location_caster: dict[str] | list[int | float]):
        self.location_caster = location_caster

    # Método para obtener el valor de un parámetro en el formato correcto
    def locate_parameter(self, parameter: Parameter, parameter_format: Parameter_Format) -> str:
        try:
            # Verifica si el nombre del parámetro coincide
            if parameter.get_name() != self.name:
                raise ValueError(f"El nombre del parámetro {parameter.get_name()} no coincide con {self.name}")

            # Verifica si el formato del parámetro coincide
            elif parameter_format.get_name() != self.name:
                raise ValueError(f"El nombre del parámetro {parameter_format.get_name()} no coincide con {self.name}")

            value = parameter.get_value()
            parameter_located = ''

            # Parámetro None o vacío
            if value is None and parameter_format.get_type() in ['i', 'f']:

                # Se obtienen los bordes de los valores posibles y la significancia
                _, upper_bound = parameter_format.get_possible_values()
                _, significance = self.location_caster
                
                # Se calcula el número de dígitos máximos
                max_digits = len(str(int(upper_bound))) + significance
                parameter_located = 'x' * max_digits
                return parameter_located

            # Parámetro categorico u ordinal (c|o)
            elif parameter_format.get_value_type() in ['c', 'o']:

                # Verifica si el casteador de locación es un diccionario
                if not isinstance(self.location_caster, dict):
                    raise ValueError(f"El formato de locación no es un diccionario para el parámetro {self.name}")

                # Verifica si el valor está en los valores posibles
                elif value not in self.location_caster.keys():
                    raise ValueError(f"El valor {value} no está en los valores posibles del parámetro {self.name}")

                parameter_located = str(self.location_caster[value])

                return parameter_located

            # Parámetro numérico (real|entero) (r|i)
            elif parameter_format.get_value_type() in ['r', 'i']:

                # Verifica que el casteador sea del tipo correcto
                if not isinstance(self.location_caster, list):
                    raise ValueError(f"El formato de locación no es una lista para el parámetro {self.name}")

                # Verifica que el casteador tenga dos elementos
                if not len(self.location_caster) == 2:
                    raise ValueError(f"El formato de locación no tiene dos elementos para el parámetro {self.name} (subrango, significancia)")

                lower_bound, upper_bound = parameter_format.get_possible_values()
                division, significance = self.location_caster

                # Verifica que el casteador permita particionar el rango de valores
                if division >= upper_bound - lower_bound:
                    raise ValueError(f"El formato de locación no permite particionar el rango de valores para el parámetro {self.name}")

                # Verifica que la significancia sea un entero positivo
                if not isinstance(significance, int) or significance < 0:
                    raise ValueError(f"La significancia no es un entero positivo para el parámetro {self.name} (location_caster = {division, significance})")

                # Calcula el subrango en el que se encuentra el valor (función piso)
                subrange_index = int((value - lower_bound) // division)
                calculated_value = lower_bound + subrange_index * division

                # Calcula la cantidad de dígitos máximos del borde superior
                max_upper_digits = len(str(int(upper_bound)))
                current_digits = len(str(int(calculated_value)))
                difference = max_upper_digits - current_digits

                # Multiplica el valor por 10^significance y convierte a entero
                scaled_value = int(calculated_value * 10**significance)

                # Convierte el valor escalado a cadena con ceros a la izquierda
                parameter_located = difference * "0" + str(scaled_value)

                return parameter_located
            else:
                raise ValueError(f"Tipo no soportado: {parameter_format.get_value_type()}")
        except ValueError as e:
            raise ValueError(f"Error en el casteo de parámetro '{parameter.get_name()}': {e}")

class Configuration:
    # Clase para definir una configuración.
    def __init__(self, id: int = 0, run: int = 0, iteration: int = 0, parameters: list[Parameter] = [], elite_state : str = '', quality: int | float = 0, location_code: str = ""):
        """
        Constructor de la clase Configuration.
        
        Args:
            id: Identificador de la configuración
            run: Número de ejecución
            iteration: Número de iteración
            parameters: Parámetros de la configuración
            elite_state: Estado de la configuración en la elite (ne|e) -> (no elite|elite)
            quality: Calidad de la configuración
            location_code: Código de la locación de la configuración
        """
        self.id = id
        self.run = run
        self.iteration = iteration
        self.parameters = parameters if parameters is not None else []
        self.elite_state = elite_state
        self.quality = quality
        self.location_code = location_code
    
    # Método para obtener el identificador de la configuración
    def get_id(self) -> int:
        return self.id
    
    # Método para obtener el número de ejecución
    def get_run(self) -> int:
        return self.run
    
    # Método para obtener el número de iteración
    def get_iteration(self) -> int:
        return self.iteration
    
    # Método para obtener los parámetros de la configuración
    def get_parameters(self) -> list[Parameter]:
        return self.parameters
    
    # Método para obtener el estado de la configuración en la elite
    def get_elite_state(self) -> str:
        return self.elite_state
    
    # Método para obtener la calidad de la configuración
    def get_quality(self) -> int | float:
        return self.quality
    
    # Método para obtener el código de la locación de la configuración
    def get_location_code(self) -> str:
        return self.location_code
    
    # Método para establecer el identificador de la configuración
    def set_id(self, id: int):
        self.id = id

    # Método para establecer el número de ejecución
    def set_run(self, run: int):
        self.run = run
        
    # Método para establecer el número de iteración
    def set_iteration(self, iteration: int):
        self.iteration = iteration
    
    # Método para establecer los parámetros de la configuración
    def set_parameters(self, parameters: list[Parameter]):
        self.parameters = parameters
    
    # Método para establecer el estado de la configuración en la elite
    def set_elite_state(self, elite_state: str):
        self.elite_state = elite_state
    
    # Método para establecer la calidad de la configuración
    def set_quality(self, quality: int | float):
        self.quality = quality
    
    # Método para establecer el código de la locación de la configuración
    def set_location_code(self, location_code: str):
        self.location_code = location_code
    
    # Método para añadir un parámetro a la configuración
    def add_parameter(self, parameter: Parameter):
        self.parameters.append(parameter)
    
    # Método para obtener la representación de la clase como string
    def __repr__(self):
        return f"ID: {self.id} - Run: {self.run} - Iteration: {self.iteration} - Parameters: {self.parameters} - Quality: {self.quality}"
    
    # Método para generar el código de la locación de la configuración
    def generate_location_code(self, parameters_format: list[Parameter_Format], locations_format: list[Location_Format]) -> str:
        try:
            # Verifica si el número de parámetros coincide con el número de formatos de locación
            if len(locations_format) != len(self.parameters):
                raise ValueError("Error en el número de parámetros al generar el código de la locación")
            elif len(parameters_format) != len(self.parameters):
                raise ValueError("Error en el número de formatos de parámetros al generar el código de la locación")

            # Genera el código de la locación
            location_code = ''
            for i, location_format in enumerate(locations_format):
                location_code += location_format.locate_parameter(self.parameters[i], parameters_format[i])

            self.location_code = location_code
            return location_code
        except ValueError as e:
            raise ValueError(f"Error al generar el código de la locación: {e}")

