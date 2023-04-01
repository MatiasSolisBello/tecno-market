from django.forms import ValidationError

#validador personalizado
class MaxSizeFileValidator:

    #constructor con 5MB
    def __init__(self, max_file_size = 5):
        self.max_file_size = max_file_size
    
    
    def __call__(self, value):
        size = value.size                           #obtener peso del archivo en bytes
        max_size = self.max_file_size * 1048576     # peso maximo en bytes
        
        # si archivo es mayor a 5MB, muestra error
        if(size > max_size):                        
            raise ValidationError(f"El peso maximo del archivo debe ser de {self.max_file_size}MB")
        return value