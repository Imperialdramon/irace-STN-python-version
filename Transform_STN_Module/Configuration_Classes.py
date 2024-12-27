class Parameter:
    """
    Clase para definir un parámetro.
    
    Attributes:
        name: Nombre del parámetro
        value: Valor del parámetro
    """
    # Constructor de la clase
    def __init__(self, name: str, value: str | int | float):
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
    def get_value(self) -> str | int | float:
        return self.value

    # Método para establecer el nombre del parámetro
    def set_name(self, name: str):
        self.name = name
    
    # Método para establecer el valor del parámetro
    def set_value(self, value: str | int | float):
        self.value = value

class Parameter_Format:
    """
    Clase para definir el formato de un parámetro.
    
    Attributes:
        name: Nombre del parámetro
        type: Tipo del parámetro (string -> s, integer -> i, float -> f)
        value_type: Tipo de los valores del parámetro (categorical -> c, numerical (real|integer) -> r | i, ordinal -> o)
        possible_values: Valores posibles del parámetro (lista de strings, enteros o flotantes)
    """
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

    # Método para obtener los valores posibles del parámetro
    def get_possible_values(self) -> list[str | int | float]:
        return self.possible_values

    # Método para establecer el nombre del parámetro
    def set_name(self, name: str):
        self.name = name

    # Método para establecer el tipo del parámetro
    def set_type(self, type: str):
        self.type = type

    # Método para establecer los valores posibles del parámetro
    def set_possible_values(self, possible_values: list[str | int | float]):
        self.possible_values = possible_values

    # Método para obtener el valor de un parámetro en el formato correcto
    def cast_parameter_value(self, parameter_value: str) -> str | int | float:
        if self.type == "s":
            return parameter_value
        elif self.type == "i":
            return int(parameter_value)
        elif self.type == "f":
            return float(parameter_value)
        else:
            return None

    # Método para validar el valor de un parámetro
    def validate_parameter_value(self, parameter: Parameter) -> bool:
        if parameter.get_name() != self.name:
            print(f"Error de parámetro")
            return False
        value = parameter.get_value()
        if self.type == "s" and (self.value_type == "c" or self.value_type == "o"):
            return value in self.possible_values
        elif (self.type == "i" or self.type == "f") and (self.value_type == "r" or self.value_type == "i"):
            return self.possible_values[0] <= value <= self.possible_values[1]
        else:
            print(f"Error de tipo de parámetro")
            return False

class Trajectory:
    """
    Clase para definir una configuración.
    
    Attributes:
        trajectory_iteration: Identificador de la iteración a la que pertenece la trayectoria
        origin_id: Identificador de la configuración de origen
        origin_parameters: Parámetros de la configuración de origen
        origin_iteration: Iteración de la configuración de origen
        origin_value: Valor de la configuración de origen
        destination_id: Identificador de la configuración de destino
        destination_parameters: Parámetros de la configuración de destino
        destination_iteration: Iteración de la configuración de destino
        destination_value: Valor de la configuración de destino
    """
    # Constructor de la clase Configuration
    def __init__(self, trajectory_iteration: int = 0, origin_id: int = 0, origin_parameters: list[Parameter] = [], origin_iteration: int = 0, origin_value: int | float = 0, destination_id: int = 0, destination_parameters: list[Parameter] = [], destination_iteration: int = 0, destination_value: int | float = 0):
        """
        Constructor de la clase Configuration.
        
        Args:
            trajectory_iteration: Identificador de la iteración a la que pertenece la trayectoria
            origin_id: Identificador de la configuración de origen
            origin_parameters: Parámetros de la configuración de origen
            origin_iteration: Iteración de la configuración de origen
            origin_value: Valor de la configuración de origen
            destination_id: Identificador de la configuración de destino
            destination_parameters: Parámetros de la configuración de destino
            destination_iteration: Iteración de la configuración de destino
            destination_value: Valor de la configuración de destino
        """
        self.origin_id = origin_id
        self.origin_parameters = origin_parameters if origin_parameters is not None else []
        self.origin_value = origin_value
        self.destination_id = destination_id
        self.destination_parameters = destination_parameters if destination_parameters is not None else []
        self.destination_value = destination_value

    # Método para obtener el identificador de la iteración de la trayectoria
    def get_trajectory_iteration(self) -> int:
        return self.trajectory_iteration

    # Método para obtener el identificador de la configuración de origen
    def get_origin_id(self) -> int:
        return self.origin_id
    
    # Método para obtener los parámetros de la configuración de origen
    def get_origin_parameters(self) -> list[Parameter]:
        return self.origin_parameters

    # Método para obtener la iteración de la configuración de origen
    def get_origin_iteration(self) -> int:
        return self.origin_iteration
    
    # Método para obtener el valor de la configuración de origen
    def get_origin_value(self) -> int | float:
        return self.origin_value
    
    # Método para obtener el identificador de la configuración de destino
    def get_destination_id(self) -> int:
        return self.destination_id
    
    # Método para obtener los parámetros de la configuración de destino
    def get_destination_parameters(self) -> list[Parameter]:
        return self.destination_parameters
    
    # Método para obtener la iteración de la configuración de destino
    def get_destination_iteration(self) -> int:
        return self.destination_iteration
    
    # Método para obtener el valor de la configuración de destino
    def get_destination_value(self) -> int | float:
        return self.destination_value

    # Método para establecer el identificador de la iteración de la trayectoria
    def set_trajectory_iteration(self, trajectory_iteration: int):
        self.trajectory_iteration = trajectory_iteration

    # Método para establecer el identificador de la configuración de origen
    def set_origin_id(self, origin_id: int):
        self.origin_id = origin_id
    
    # Método para establecer los parámetros de la configuración de origen
    def set_origin_parameters(self, origin_parameters: list[Parameter]):
        self.origin_parameters = origin_parameters
    
    # Método para establecer la iteración de la configuración de origen
    def set_origin_iteration(self, origin_iteration: int):
        self.origin_iteration = origin_iteration
    
    # Método para establecer el valor de la configuración de origen
    def set_origin_value(self, origin_value: int | float):
        self.origin_value = origin_value
        
    # Método para establecer el identificador de la configuración de destino
    def set_destination_id(self, destination_id: int):
        self.destination_id = destination_id
    
    # Método para establecer los parámetros de la configuración de destino
    def set_destination_parameters(self, destination_parameters: list[Parameter]):
        self.destination_parameters = destination_parameters
    
    # Método para establecer la iteración de la configuración de destino
    def set_destination_iteration(self, destination_iteration: int):
        self.destination_iteration = destination_iteration

    # Método para establecer el valor de la configuración de destino
    def set_destination_value(self, destination_value: int | float):
        self.destination_value = destination_value
    
    # Método para añadir un parámetro a la configuración de origen
    def add_origin_parameter(self, parameter: Parameter):
        self.origin_parameters.append(parameter)
    
    # Método para añadir un parámetro a la configuración de destino
    def add_destination_parameter(self, parameter: Parameter):
        self.destination_parameters.append(parameter)
    
    # Método para obtener la representación de la clase como string
    def to_stn_format(self) -> str:
        trajectory_iteration = self.trajectory_iteration
        origin_value = self.origin_value
        origin_node = ""
        for parameter in self.origin_parameters:
            origin_node += f"{parameter.get_value()}" # MODIFICAR: USAR ALGÚN TIPO DE FORMATO MÁS ESTANDAR
        destination_value = self.destination_value
        destination_node = ""
        for parameter in self.destination_parameters:
            destination_node += f"{parameter.get_value()}" # MODIFICAR: USAR ALGÚN TIPO DE FORMATO MÁS ESTANDAR
        return f"{trajectory_iteration} {origin_value:.4f} {origin_node} {destination_value:.4f} {destination_node}"

class Neighborhood: # MODIFICAR: DEFINIR UN FORMATO DE LA CLASE QUE RESULTE UTIL PARA LA DEFINICIÓN DE VECINDARIO
# RECORDANDO QUE SE DEBE OBTENER EL MÁXIMO VALOR Y OTROS VALORES DE INTERÉS -> REPRESENTATIVO DE LA CLASE
# PROBABLEMENTE HACER ALGO ASÍ COMO UNA LISTA SIMILAR A LA DE TRAJECTORY PERO QUE ME INDIQUE CUAL ES LA ACTUAL Y CUAL ES LA REPRESENTADA, ETC
    """
    Clase para definir una vecindad de un parámetro.
    
    Attributes:
        parameter_name: Nombre del parámetro
        neighborhood: Vecindad del parámetro
    """
    # Constructor de la clase
    def __init__(self, name: str = "", neighborhood: dict[str, str] = {}):
        """
        Constructor de la clase Neighborhood.
        
        Args:
            name: Nombre del parámetro
            neighborhood: Vecindad del parámetro
        """
        self.parameter_name = name
        self.neighborhood = neighborhood # MODIFICAR: USAR ALGÚN TIPO DE FORMATO MÁS ESTANDAR Y FUNCIONAL
    # Método para obtener la representación de la clase como string
    def __repr__(self):
        return f"Parameter: {self.parameter_name} - Neighborhood: {self.neighborhood}"

    # Método para obtener el nombre de la vecindad
    def get_parameter_name(self) -> str:
        return self.parameter_name

    # Método para obtener la vecindad
    def get_neighborhood(self) -> dict[str, str]:
        return self.neighborhood

    # Método para establecer el nombre de la vecindad
    def set_parameter_name(self, parameter_name: str):
        self.parameter_name = parameter_name

    # Método para establecer la vecindad
    def set_neighborhood(self, neighborhood: dict[str, str]):
        self.neighborhood = neighborhood
    
    def get_parameter_node(self, parameter: Parameter, parameter_format: Parameter_Format) -> str:
        if parameter.get_name() != self.parameter_name or parameter_format.get_name() != self.parameter_name:
            print(f"Error de parámetro o formato de parámetro")
            return None
        return "Test"

