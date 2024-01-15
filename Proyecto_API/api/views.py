from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.core.exceptions import ValidationError
from datetime import datetime
import secrets

# Elementos necesarios para que el API REST funcione 
from rest_framework import status
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status

# Importando Modelos y Servicios
from api.models import Usuario, Cliente, Producto, ProductoHasCategoria, Categoria, Pedido, DetallesPedido, Empleado, FoodTruck
from api.services import sendEmail, random_password


# JSON FE: { "nombre": "Oscar David", "apellido": "Romero Hernández", "usuario": "dfg161", "correo": "(tu correo)@outlook.com", "password": "12345" }
# JSON BE: { 'mensaje': '¡Se ha registrado correctamente el usuario, para verificar la cuenta se ha enviado un enlace a tu correo!' }
@api_view(['POST'])
def registro(request):
    if request.method == 'POST':
        try:
            # Obtener los datos del cuerpo de la solicitud POST
            data = request.data

            # Validar datos
            if 'password' not in data or 'usuario' not in data or 'correo' not in data:
                raise ValidationError('Los campos password, usuario y correo son obligatorios.')

            # Verificar si el correo ya está en uso
            if Usuario.objects.filter(email=data['correo']).exists():
                return Response({'error': 'El correo electrónico ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)

            # Generar token
            token = secrets.token_hex(int(20/2))

            # Crear usuario y cliente dentro de una transacción
            with transaction.atomic():
                nuevo_usuario = Usuario.objects.create_user(
                    password=data['password'],
                    username=data['usuario'],
                    email=data['correo'],
                    is_superuser=0,
                    is_staff=0,
                    is_active=1,
                    codigo=token,
                    verificacion="NO",
                    tipo="user"
                )

                cliente = Cliente(nombre=data['nombre'], apellido=data['apellido'], usuario=nuevo_usuario)
                cliente.save()

                sendEmail(data['correo'], "register", token)

            # Enviar una respuesta JSON de vuelta
            respuesta = {'mensaje': '¡Se ha registrado correctamente el usuario, para verificar la cuenta se ha enviado un enlace a tu correo!'}
            return Response(respuesta, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Ocurrió un error al procesar la solicitud.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Si la solicitud no es POST, devolver un error
    return Response({'error': 'Se esperaba una solicitud POST'}, status=status.HTTP_400_BAD_REQUEST)

# JSON BE: { 'mensaje/error': Depende el mensaje o error' }
@api_view(['GET'])
def verificar_cuenta(request):
    if request.method == 'GET':
        try:
            # Obtener el valor del parámetro de consulta "token"
            token = request.GET.get('token', None)

            if token is not None:
                # Buscar el usuario con el código proporcionado
                usuario = Usuario.objects.get(codigo=token)

                usuario.verificacion = "YES"
                usuario.save()
                mensaje = 'La cuenta ha sido verificada correctamente'

                # Renderizar la plantilla con el mensaje
                return render(request, 'verificar_cuenta.html', {'mensaje': mensaje})

            else:
                return render(request, 'verificar_cuenta.html', {'error': 'El parámetro de consulta "token" es obligatorio en la solicitud GET'})

        except ObjectDoesNotExist:
            # Usuario no encontrado
            return render(request, 'verificar_cuenta.html', {'error': 'No se encontró ningún usuario para verificar'})

    # Si la solicitud no es GET, devolver un error
    return render(request, 'verificar_cuenta.html', {'error': 'Se esperaba una solicitud GET'})


# JSON FE: { "user": "dfg161", "password": "12345"}
# JSON BE: { "mensaje": "Se inició sesión correctamente", "token": "2a9abeed3f70e3769f9c"}
@api_view(['POST'])
def iniciar_sesion(request):
    if request.method == 'POST':
        try:
            # Obtener los datos del cuerpo de la solicitud POST
            data = request.data
            username = data["user"]
            password = data["password"]

            # Obtener el usuario
            try:
                usuario = Usuario.objects.get(username=username)
                token = usuario.codigo

                # Verificar si la cuenta ya se validó
                if usuario.verificacion == "NO":
                    return Response({'error': 'La cuenta no ha sido verificada. Por favor, verifica tu cuenta antes de iniciar sesión.'},
                                    status=status.HTTP_401_UNAUTHORIZED)

                # Verificar la contraseña
                if check_password(password, usuario.password):
                    # Contraseña válida, usuario autenticado
                    respuesta = {'mensaje': 'Se inició sesión correctamente', 'token': token}
                    return Response(respuesta, status=status.HTTP_200_OK)
                else:
                    # Contraseña no válida
                    return Response({'error': 'Nombre de usuario o contraseña incorrectos'},
                                    status=status.HTTP_401_UNAUTHORIZED)
            except ObjectDoesNotExist:
                # Usuario no encontrado
                return Response({'error': 'Nombre de usuario o contraseña incorrectos'},
                                status=status.HTTP_401_UNAUTHORIZED)

        except KeyError:
            # Claves faltantes en los datos de la solicitud
            return Response({'error': 'Los datos de usuario y contraseña son obligatorios en la solicitud POST'},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        # Si la solicitud no es POST, devolver un error
        return Response({'error': 'Se esperaba una solicitud POST'}, status=status.HTTP_400_BAD_REQUEST)


# JSON FE: { "correo": "javiermartinez506@yahoo.com"}
# JSON BE: {'mensaje': 'Se ha enviado con éxito una nueva contraseña a su correo.'}
@api_view(['POST'])
def recuperar_password(request):
    if request.method == 'POST':
        # Obtener los datos del cuerpo de la solicitud POST
        data = request.data

        # Validar datos
        if 'correo' not in data:
            raise ValidationError('El campo email es obligatorio.')

        # Verificar si el correo existe en la base de datos
        try:
            usuario = Usuario.objects.get(email=data['correo'])
            new_password = random_password(6)
            usuario.set_password(new_password)
            usuario.save()
            
            sendEmail(data['correo'], "recover_password", new_password)

            return Response({'mensaje': 'Se ha enviado con éxito una nueva contraseña a su correo.'}, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'error': 'El correo electrónico no existe en la base de datos.'}, status=status.HTTP_404_NOT_FOUND)

    # Si la solicitud no es POST, devolver un error
    return Response({'error': 'Se esperaba una solicitud POST'}, status=status.HTTP_400_BAD_REQUEST)

# JSON BE: {'productos': [{'nombre': <str>, 'descripcion': <str>, 'precio': <float>, 'imagen': <str>}, ...]}
@api_view(['GET'])
def ver_productos(request):
    if request.method == 'GET':
        try:
            # Obtener todos los productos disponibles
            productos = Producto.objects.all()

            # Crear una lista de diccionarios con los datos de los productos para los usuarios
            lista_productos = [
                {
                    'id': producto.id,
                    'nombre': producto.nombre,
                    'descripcion': producto.descripcion,
                    'precio': producto.precio,
                    'imagen': producto.imagen,
                    'id_foodtruck': producto.foodtruck_id,
                }
                for producto in productos
            ]

            # Devolver la lista de productos en formato JSON
            respuesta = {'productos': lista_productos}
            return Response(respuesta, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Ocurrió un error al procesar la solicitud.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Se esperaba una solicitud GET'}, status=status.HTTP_400_BAD_REQUEST)

# JSON FE: {"categoria": "tacos"}
# JSON BE: {'productos': [{'nombre': <str>, 'descripcion': <str>, 'precio': <float>}, ...]}
@api_view(['POST'])
def filtrar_productos_categoria(request):
    if request.method == 'POST':
        try:
            # Obtener el nombre de la categoría del cuerpo de la solicitud
            categoria_nombre = request.data.get('categoria')

            # Validar si se proporcionó el nombre de la categoría
            if not categoria_nombre:
                return Response({'error': 'El nombre de la categoría es obligatorio en la solicitud POST'}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener productos asociados a la categoría
            categoria = Categoria.objects.get(categoria=categoria_nombre)
            productos_categoria = ProductoHasCategoria.objects.filter(categoria=categoria)
            productos = [detalle.producto for detalle in productos_categoria]

            # Crear una lista de diccionarios con la información básica de los productos
            lista_productos = [
                {
                    'id': producto.id,
                    'nombre': producto.nombre,
                    'descripcion': producto.descripcion,
                    'precio': producto.precio,
                    'imagen': producto.imagen,
                    'id_foodtruck': producto.foodtruck_id,
                }
                for producto in productos
            ]

            # Devolver la respuesta en formato JSON
            respuesta = {'productos': lista_productos}
            return Response(respuesta, status=status.HTTP_200_OK)

        except Categoria.DoesNotExist:
            return Response({'error': 'La categoría especificada no existe'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Ocurrió un error al procesar la solicitud.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Se esperaba una solicitud POST con el nombre de la categoría'}, status=status.HTTP_400_BAD_REQUEST)

# JSON FE: {"id_foodtruck": "1"}
# JSON BE: {'productos': [{'nombre': <str>, 'descripcion': <str>, 'precio': <float>}, ...]}
@api_view(['POST'])
def filtrar_productos_foodtruck(request):
    if request.method == 'POST':
        try:
            # Obtener el id_foodtruck del cuerpo de la solicitud
            id_foodtruck = request.data.get('id_foodtruck')

            # Validar si se proporcionó el id_foodtruck
            if not id_foodtruck:
                return Response({'error': 'El id_foodtruck es obligatorio en la solicitud POST'}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener productos asociados al id_foodtruck
            productos = Producto.objects.filter(foodtruck_id=id_foodtruck)

            # Crear una lista de diccionarios con la información básica de los productos
            lista_productos = [
                {
                    'id': producto.id,
                    'nombre': producto.nombre,
                    'descripcion': producto.descripcion,
                    'precio': producto.precio,
                    'imagen': producto.imagen,
                    'id_foodtruck': producto.foodtruck_id,
                }
                for producto in productos
            ]

            # Devolver la respuesta en formato JSON
            respuesta = {'productos': lista_productos}
            return Response(respuesta, status=status.HTTP_200_OK)

        except FoodTruck.DoesNotExist:
            return Response({'error': 'El foodtruck especificado no existe'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Ocurrió un error al procesar la solicitud.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Se esperaba una solicitud POST con el id_foodtruck'}, status=status.HTTP_400_BAD_REQUEST)

# JSON BE: {'foodtrucks': []}
@api_view(['GET'])
def obtener_foodtrucks(request):
    if request.method == 'GET':
        try:
            # Obtener todos los FoodTrucks
            foodtrucks = FoodTruck.objects.all()

            # Crear una lista de diccionarios con los atributos de cada FoodTruck
            lista_foodtrucks = []
            for foodtruck in foodtrucks:
                foodtruck_info = {
                    'id': foodtruck.id,
                    'nombre': foodtruck.nombre,
                    'descripcion': foodtruck.descripcion,
                }
                lista_foodtrucks.append(foodtruck_info)

            return Response({'foodtrucks': lista_foodtrucks}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Ocurrió un error al procesar la solicitud.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Se esperaba una solicitud GET'}, status=status.HTTP_400_BAD_REQUEST)

# JSON FE: {"user": "dfg161"}
# JSON BE: {'pedidos': []}
@api_view(['GET'])
def ver_pedidos(request):
    if request.method == 'GET':
        try:
            # Obtener el nombre de usuario del cuerpo de la solicitud
            username = request.data.get('user')
            
            # Obtener el objeto Usuario basado en el nombre de usuario
            usuario = Usuario.objects.get(username=username)
            cliente = Cliente.objects.get(usuario_id=usuario.id)

            # Obtener todos los pedidos asociados a ese usuario
            pedidos = Pedido.objects.filter(usuario_id=usuario.id)

            # Crear una lista de diccionarios con la información de cada pedido
            lista_pedidos = []
            for pedido in pedidos:
                pedido_info = {
                    'id': pedido.id,
                    'precio_total': pedido.precio_total,
                    'fecha_pedido': pedido.fecha_pedido,
                    'fecha_entrega': pedido.fecha_entrega,
                    'fecha_repartidor': pedido.fecha_repartidor,
                    'estado': pedido.estado,
                    'direccion': pedido.direccion,
                    'foodtruck': pedido.foodtruck.nombre,
                    'empleado': pedido.empleado.nombre,
                    'usuario': pedido.usuario.username,
                    'cliente': f"{cliente.nombre} {cliente.apellido}",
                }
                lista_pedidos.append(pedido_info)

            return Response({'pedidos': lista_pedidos}, status=status.HTTP_200_OK)

        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Ocurrió un error al procesar la solicitud.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Se esperaba una solicitud GET'}, status=status.HTTP_400_BAD_REQUEST)

# JSON FE: { "pedido_id": "1"}
# JSON BE: {'detalles_pedido': []}
@api_view(['GET'])
def ver_detalles_pedido(request):
    if request.method == 'GET':
        try:
            # Obtener el pedido asociado al pedido_id
            pedido_id = request.data.get('pedido_id')
            print(pedido_id)
            pedido = Pedido.objects.get(id=pedido_id)

            # Obtener los detalles del pedido
            detalles_pedido = DetallesPedido.objects.filter(pedido=pedido)

            # Crear una lista de diccionarios con la información básica de los detalles del pedido
            detalles_pedido_info = [
                {
                    'cantidad': detalle.cantidad,
                    'producto_nombre': detalle.producto.nombre,
                    'producto_descripcion': detalle.producto.descripcion,
                    'producto_precio': detalle.producto.precio,
                }
                for detalle in detalles_pedido
            ]

            # Devolver la respuesta
            return Response({'detalles_pedido': detalles_pedido_info}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'error': 'Pedido no encontrado'}, status=404)

    return Response({'error': 'Se esperaba una solicitud GET'})


# JSON FE: { "pedido_id": "1"}
# JSON BE: {'mensaje': 'Pedido cancelado exitosamente'}
@api_view(['PATCH'])
def cancelar_pedido(request):
    if request.method == 'PATCH':
        try:
            # Obtener el pedido que se va a cancelar
            pedido_id = request.data.get('pedido_id')
            pedido = Pedido.objects.get(id=pedido_id)

            # Verificar si el pedido ya está cancelado
            if pedido.estado == 'Cancelado':
                return Response({'error': 'El pedido ya está cancelado'}, status=400)

            # Actualizar el estado del pedido a 'Cancelado'
            pedido.estado = 'Cancelado'
            pedido.save()

            return Response({'mensaje': 'Pedido cancelado exitosamente'}, status=200)


        except ObjectDoesNotExist:
            return Response({'error': 'Pedido no encontrado'}, status=404)

    return Response({'error': 'Se esperaba una solicitud DELETE'})

# JSON FE: { "pedido_id": "1", "empleado_id": "3"}
# JSON BE: {'mensaje': 'Pedido cancelado exitosamente'}
@api_view(['PATCH'])
def asignar_pedido_a_empleado(request):
    if request.method == 'PATCH':
        try:
            # Obtener el pedido_id y el empleado_id del cuerpo de la solicitud
            pedido_id = request.data.get('pedido_id')
            empleado_id = request.data.get('empleado_id')

            # Verificar si se proporcionaron ambos IDs
            if not pedido_id or not empleado_id:
                return Response({'error': 'Se esperaban los IDs del pedido y del empleado en la solicitud PATCH'}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener el pedido y el empleado asociados a los IDs proporcionados
            pedido = Pedido.objects.get(id=pedido_id)
            empleado = Empleado.objects.get(id=empleado_id)

            # Verificar si el pedido ya está asignado a un empleado
            if pedido.empleado is not None:
                return Response({'error': 'El pedido ya está asignado a un empleado'}, status=status.HTTP_400_BAD_REQUEST)

            # Asignar el pedido al empleado
            pedido.empleado = empleado
            pedido.fecha_repartidor = datetime.now()
            pedido.estado = "En Curso"
            pedido.save()

            return Response({'mensaje': 'Pedido asignado exitosamente a empleado'}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'error': 'Pedido o empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'error': 'Se esperaba una solicitud PATCH'}, status=status.HTTP_400_BAD_REQUEST)

# JSON FE: { "empleado_id": "3"}
# JSON BE: {'pedidos': []}
@api_view(['GET'])
def consultar_pedidos_asignados(request):
    if request.method == 'GET':
        try:
            # Obtener el empleado_id del parámetro de consulta "empleado_id"
            empleado_id = request.data.get('empleado_id')

            # Verificar si se proporcionó el ID del empleado
            if not empleado_id:
                return Response({'error': 'El parámetro de consulta "empleado_id" es obligatorio en la solicitud GET'}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener el empleado y los pedidos asignados a él
            empleado = Empleado.objects.get(id=empleado_id)
            pedidos_asignados = Pedido.objects.filter(empleado=empleado)

            # Crear una lista de diccionarios con la información de cada pedido asignado
            lista_pedidos_asignados = []
            for pedido in pedidos_asignados:
                pedido_info = {
                    'id': pedido.id,
                    'precio_total': pedido.precio_total,
                    'fecha_pedido': pedido.fecha_pedido,
                    'fecha_entrega': pedido.fecha_entrega,
                    'estado': pedido.estado,
                    'direccion': pedido.direccion,
                    'foodtruck': pedido.foodtruck.nombre,
                    'usuario': pedido.usuario.username,
                }
                lista_pedidos_asignados.append(pedido_info)

            return Response({'pedidos_asignados': lista_pedidos_asignados}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'error': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'error': 'Se esperaba una solicitud GET'}, status=status.HTTP_400_BAD_REQUEST)

# JSON FE: {"user": "dfg161"}
# JSON BE: {'repartidores': []}
@api_view(['GET'])
def obtener_repartidores(request):
    if request.method == 'GET':
        try:
            # Obtener el empleado que realiza la solicitud
            usuario_solicitante = request.data.get('user')
            usuario_id = Usuario.objects.get(username = usuario_solicitante)
            empleado_solicitante = Empleado.objects.get(usuario_id=usuario_id)

            # Verificar si el empleado tiene asignado un FoodTruck
            if empleado_solicitante.foodtruck is None:
                return Response({'error': 'El empleado no tiene asignado un FoodTruck'}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener todos los empleados que pertenecen al mismo FoodTruck del empleado solicitante
            empleados = Empleado.objects.filter(foodtruck=empleado_solicitante.foodtruck, rol="Repartidor")

            # Crear una lista de diccionarios con los atributos de cada empleado
            lista_empleados = []
            for empleado in empleados:
                empleado_info = {
                    'id': empleado.id,
                    'nombre': empleado.nombre,
                    'rol': empleado.rol,
                    'foodtruck': empleado.foodtruck.nombre,
                    'usuario': empleado.usuario.username,
                }
                lista_empleados.append(empleado_info)

            return Response({'repartidores': lista_empleados}, status=status.HTTP_200_OK)

        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Empleado.DoesNotExist:
            return Response({'error': 'Empleado no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'Ocurrió un error al procesar la solicitud.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Se esperaba una solicitud GET'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def entregar_pedido(request):
    if request.method == 'PATCH':
        try:
            # Obtener el pedido_id del cuerpo de la solicitud
            pedido_id = request.data.get('pedido_id')
            estado_pedido = request.data.get('estado_pedido')

            # Verificar si se proporcionó el ID del pedido
            if not pedido_id:
                return Response({'error': 'El ID del pedido es obligatorio en la solicitud PATCH'}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener el pedido y actualizar su estado a "Entregado"
            pedido = Pedido.objects.get(id=pedido_id)
            pedido.estado = estado_pedido
            pedido.fecha_entrega = datetime.now()
            pedido.save()

            return Response({'mensaje': 'Estado del pedido actualizado exitosamente'}, status=status.HTTP_200_OK)

        except Pedido.DoesNotExist:
            return Response({'error': 'Pedido no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'error': 'Se esperaba una solicitud PATCH'}, status=status.HTTP_400_BAD_REQUEST)

# JSON FE: { "productos": [ {"id": 6, "cantidad": 2, "foodtruck_id": 2}, {"id": 7, "cantidad": 1, "foodtruck_id": 2}, {"id": 8, "cantidad": 3, "foodtruck_id": 2} ], "direccion": "Calle Principal 123", "user": "testUser"}
# JSON BE: {'mensaje feo'}
@api_view(['POST'])
def realizar_pedido(request):

    if request.method == 'POST':
        # Obtener los datos del cuerpo de la solicitud POST
        data = request.data

        # Obtener el nombre de usuario del cuerpo de la solicitud
        username = data.get('user')

        try:
            # Obtener el objeto Usuario basado en el nombre de usuario
            usuario = Usuario.objects.get(username=username)

            # Crear un objeto Pedido
            pedido = Pedido.objects.create(
                precio_total=0,  # Puedes calcular esto más tarde
                direccion=data['direccion'],
                foodtruck_id=data['productos'][0]['foodtruck_id'],  # Supongamos que todos los productos pertenecen al mismo foodtruck
                usuario=usuario
            )

            # Inicializar el total del pedido
            total_pedido = 0

            # Iterar sobre los productos en la solicitud y crear DetallesPedido
            for producto_data in data['productos']:
                producto_id = producto_data['id']
                cantidad = producto_data['cantidad']

                producto = Producto.objects.get(id=producto_id)

                DetallesPedido.objects.create(
                    cantidad=cantidad,
                    pedido=pedido,
                    producto=producto
                )

                # Calcular el costo del producto y sumarlo al total del pedido
                total_pedido += producto.precio * cantidad

            # Actualizar el total del pedido
            pedido.precio_total = total_pedido
            pedido.fecha_pedido = datetime.now()
            pedido.save()

            return Response({'success': 'Pedido realizado con éxito'}, status=status.HTTP_201_CREATED)

        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'error': 'Se esperaba una solicitud POST'}, status=status.HTTP_400_BAD_REQUEST)
