from users.models import Usuario

def get_user_by_email(email):
    try:
        return Usuario.objects.get(email=email)
    except:
        return None

def create_usuario(nombre, apellidos, email, contrasenya, dni, fecha_nacimiento, direccion, telefono, verificado=False):
    usuario = Usuario(nombre=nombre, apellidos=apellidos, email=email, contrasenya=contrasenya, dni=dni, fecha_nacimiento=fecha_nacimiento, direccion=direccion, telefono=telefono, verificado=verificado)
    usuario.save()
    return usuario

def read_usuario(id=None): # El read es el get basicamente
    if id is not None:
        try:
            return Usuario.objects.get(id=id)
        except:
            return None
    else:
        return list(Usuario.objects.all())

def update_usuario(id, nombre=None, apellidos=None, email=None, contrasenya=None, dni=None, fecha_nacimiento=None, direccion=None, telefono=None, verificado=None):
    usuario = Usuario.objects.get(id=id)
    if nombre is not None:
        usuario.nombre = nombre
    if apellidos is not None:
        usuario.apellidos = apellidos
    if email is not None:
        usuario.email = email
    if contrasenya is not None:
        usuario.contrasenya = contrasenya
    if dni is not None:
        usuario.dni = dni
    if fecha_nacimiento is not None:
        usuario.fecha_nacimiento = fecha_nacimiento
    if direccion is not None:
        usuario.direccion = direccion
    if telefono is not None:
        usuario.telefono = telefono
    if verificado is not None:
        usuario.verificado = verificado
    usuario.save()
    return usuario

def delete_usuario(id):
    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    return True