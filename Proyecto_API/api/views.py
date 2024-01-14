from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.core.exceptions import ValidationError
import secrets

# Elementos necesarios para que el API REST funcione 
from rest_framework import status
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status

# Importando Modelos y Servicios
from api.models import Usuario, Cliente, Producto, ProductoHasCategoria, Categoria, Pedido, DetallesPedido, Empleado
from api.services import sendEmail, random_password


# JSON FORMAT: { "nombre": "Oscar David", "apellido": "Romero Hernández", "usuario": "dfg161", "correo": "(tu correo)@outlook.com", "password": "12345" }
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


# JSON FORMAT: { "usuario": "dfg161", "password": "12345"}
@api_view(['POST'])
def iniciar_sesion(request):
    if request.method == 'POST':
        try:
            # Obtener los datos del cuerpo de la solicitud POST
            data = request.data
            username = data["usuario"]
            password = data["password"]

            # Obtener el usuario
            try:
                usuario = Usuario.objects.get(username=username)

                # Verificar si la cuenta ya se validó
                if usuario.verificacion == "NO":
                    return Response({'error': 'La cuenta no ha sido verificada. Por favor, verifica tu cuenta antes de iniciar sesión.'},
                                    status=status.HTTP_401_UNAUTHORIZED)

                # Verificar la contraseña
                if check_password(password, usuario.password):
                    # Contraseña válida, usuario autenticado
                    respuesta = {'mensaje': 'Se inició sesión correctamente'}
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


# JSON FORMAT: { "correo": "javiermartinez506@yahoo.com"}
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


@api_view(['GET'])
def consultar_catalogo(request):
    if request.method == 'GET':
        try:
            # Obtener todos los productos disponibles
            productos = Producto.objects.all()

            # Crear una lista de diccionarios con los datos de los productos para los usuarios
            lista_productos = [
                {
                    'nombre': producto.nombre,
                    'descripcion': producto.descripcion,
                    'precio': producto.precio,
                    'imagen': producto.imagen
                }
                for producto in productos
            ]

            # Devolver la lista de productos en formato JSON
            return Response(lista_productos, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Ocurrió un error al procesar la solicitud.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Se esperaba una solicitud GET'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def filtrar_productos(request):
    if request.method == 'POST':
        # Obtener el nombre de la categoría del cuerpo de la solicitud
        categoria_nombre = request.data.get('categoria_nombre')

        # Filtrar productos por nombre de categoría usando la relación ProductoHasCategoria
        if categoria_nombre:
            categoria = Categoria.objects.get(categoria=categoria_nombre)
            productos_categoria = ProductoHasCategoria.objects.filter(categoria=categoria)
            productos = [detalle.producto for detalle in productos_categoria]
            # Crear una lista de diccionarios con la información básica de los productos
            productos_info = [{'nombre': producto.nombre, 'descripcion': producto.descripcion, 'precio': producto.precio} for producto in productos]
            # Devolver la respuesta
            return Response(productos_info)

    return Response({'error': 'Se esperaba una solicitud POST con el nombre de la categoría'})


@api_view(['GET'])
def ver_pedidos(request):
    if request.method == 'GET':
        # Verificar si el usuario es un empleado
        if request.user.is_authenticated and request.user.tipo == 'employee':
            # Si es un empleado, obtener los pedidos asignados a ese empleado
            pedidos = Pedido.objects.filter(empleado=request.user.empleado)
        else:
            # Si no es un empleado, obtener todos los pedidos
            pedidos = Pedido.objects.all()

        # Crear una lista de diccionarios con la información básica de los pedidos
        pedidos_info = [
            {
                'precio_total': pedido.precio_total,
                'fecha_pedido': pedido.fecha_pedido,
                'estado': pedido.estado,
                # Incluir cualquier otro campo que desees mostrar en la respuesta
            }
            for pedido in pedidos
        ]

        # Devolver la respuesta directamente sin serialización
        return Response(pedidos_info)

    return Response({'error': 'Se esperaba una solicitud GET'})


#path('api/cuenta/ver-detallles-pedido/1)
@api_view(['GET'])
def ver_detalles_pedido(request, pedido_id):
    if request.method == 'GET':
        try:
            # Obtener el pedido asociado al pedido_id
            pedido = Pedido.objects.get(id=pedido_id)

            # Verificar si el usuario autenticado es un empleado asociado al pedido
            if request.user.is_authenticated and request.user.tipo == 'employee' and pedido.empleado.usuario == request.user:
                # Obtener los detalles del pedido
                detalles_pedido = DetallesPedido.objects.filter(pedido=pedido)

                # Crear una lista de diccionarios con la información básica de los detalles del pedido
                detalles_pedido_info = [
                    {
                        'cantidad': detalle.cantidad,
                        'producto_nombre': detalle.producto.nombre,
                        'producto_descripcion': detalle.producto.descripcion,
                        'producto_precio': detalle.producto.precio,
                        # Incluir cualquier otro campo que desees mostrar en la respuesta
                    }
                    for detalle in detalles_pedido
                ]

                # Devolver la respuesta
                return Response(detalles_pedido_info)
            else:
                return Response({'error': 'No tienes permisos para ver los detalles de este pedido'}, status=403)

        except Pedido.DoesNotExist:
            return Response({'error': 'Pedido no encontrado'}, status=404)

    return Response({'error': 'Se esperaba una solicitud GET'})


@api_view(['POST'])
def cancelar_pedido(request, pedido_id):
    if request.method == 'POST':
        try:
            # Obtener el pedido que se va a cancelar
            pedido = Pedido.objects.get(id=pedido_id)

            # Verificar si el usuario autenticado es un empleado asociado al pedido
            if request.user.is_authenticated and request.user.tipo == 'employee' and pedido.empleado.usuario == request.user:
                # Verificar si el pedido ya está cancelado
                if pedido.estado == 'Cancelado':
                    return Response({'error': 'El pedido ya está cancelado'}, status=400)

                # Actualizar el estado del pedido a 'Cancelado'
                pedido.estado = 'Cancelado'
                pedido.save()

                return Response({'mensaje': 'Pedido cancelado exitosamente'}, status=200)
            else:
                return Response({'error': 'No tienes permisos para cancelar este pedido'}, status=403)

        except Pedido.DoesNotExist:
            return Response({'error': 'Pedido no encontrado'}, status=404)

    return Response({'error': 'Se esperaba una solicitud POST'})


@api_view(['POST'])
def asignar_pedido(request, pedido_id):
    if request.method == 'POST':
        try:
            # Obtener el pedido que se va a asignar
            pedido = Pedido.objects.get(id=pedido_id)

            # Verificar si el pedido ya está asignado
            if pedido.empleado:
                return Response({'error': 'El pedido ya está asignado a un empleado'}, status=400)

            # Verificar el permiso del usuario autenticado
            if not request.user.is_authenticated or request.user.tipo != 'employee':
                return Response({'error': 'No tienes permisos para asignar pedidos'}, status=403)

            # Obtener la lista de empleados disponibles para asignar el pedido
            empleados_disponibles = Empleado.objects.filter(foodtruck=pedido.foodtruck, usuario=request.user, usuario__is_active=True)

            # Asignar el pedido al primer empleado disponible (puedes personalizar la lógica según tus necesidades)
            if empleados_disponibles:
                empleado_asignado = empleados_disponibles[0]
                pedido.empleado = empleado_asignado
                pedido.save()

                return Response({'mensaje': f'Pedido asignado exitosamente'}, status=200)
            else:
                return Response({'error': 'No estás autorizado para asignar pedidos o no hay empleados disponibles'}, status=403)

        except Pedido.DoesNotExist:
            return Response({'error': 'Pedido no encontrado'}, status=404)

    return Response({'error': 'Se esperaba una solicitud POST'})


@api_view(['GET'])
def consultar_pedidos_asignados(request):
    if request.method == 'GET':
        try:
            # Verificar si el usuario autenticado es un empleado
            if request.user.is_authenticated and request.user.tipo == 'employee':
                # Obtener los pedidos asignados a ese empleado
                pedidos_asignados = Pedido.objects.filter(empleado=request.user.empleado)

                # Crear una lista de diccionarios con la información básica de los pedidos asignados
                pedidos_info = [
                    {
                        'precio_total': pedido.precio_total,
                        'fecha_pedido': pedido.fecha_pedido,
                        'estado': pedido.estado,
                        # Incluir cualquier otro campo que desees mostrar en la respuesta
                    }
                    for pedido in pedidos_asignados
                ]

                # Devolver la respuesta directamente sin serialización
                return Response(pedidos_info)
            else:
                return Response({'error': 'No tienes permisos para consultar pedidos asignados'}, status=403)

        except Exception as e:
            return Response({'error': 'Ocurrió un error al procesar la solicitud.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'error': 'Se esperaba una solicitud GET'})


