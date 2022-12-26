class EngineSettings:    
    DEFAULT_VARIABLES = {
        "BACKGROUND_COLOR": "black",
        "FPS": 60
    }
    
    VARIABLES = DEFAULT_VARIABLES.copy()
    
    BLACK_LIST = (
        '__builtins__', '__cached__', '__doc__', '__file__',
        '__loader__', '__name__', '__package__', '__spec__'
    )
    
    ADDITIONAL_BLACK_LIST = set()
    
    @staticmethod
    def load_file(settings_file):
        for var in dir(settings_file):
            if var in EngineSettings.BLACK_LIST or var in EngineSettings.ADDITIONAL_BLACK_LIST:
                continue
            
            EngineSettings.VARIABLES[var] = settings_file.__dict__.get(var)

    @staticmethod
    def get_var(var_name: str):
        return EngineSettings.VARIABLES.get(var_name, None)
    
    @staticmethod
    def get_all_vars():
        return EngineSettings.VARIABLES

    @staticmethod
    def add_black_list(var_name: str):
        EngineSettings.ADDITIONAL_BLACK_LIST.add(var_name)
    
    @staticmethod
    def remove_black_list(var_name: str):
        EngineSettings.ADDITIONAL_BLACK_LIST.remove(var_name)
        
    @staticmethod
    def get_black_list():
        return EngineSettings.ADDITIONAL_BLACK_LIST
    