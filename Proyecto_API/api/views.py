from django.shortcuts import render
import secrets

# Elementos necesarios para que el API REST funcione 
from rest_framework import status
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Importando Modelos
from api.models import Usuario, Cliente

@api_view(['POST'])
def registro(request):
    if request.method == 'POST':
        # Obtener los datos del cuerpo de la solicitud POST
        data = request.data

        # Hacer algo con los datos (por ejemplo, imprimirlos)
        print("Datos recibidos:", data)

        # Salvar datos de JSON en un modelo (osea en la base de datos)
        nuevo_usuario = Usuario.objects.create_user(password = data['password'],
                                                is_superuser=0,
                                                username = data['usuario'],
                                                email = data['correo'],
                                                is_staff = 0,
                                                is_active = 1,
                                                codigo = secrets.token_hex(int(15/2)),
                                                verificacion = "NO",
                                                tipo = "user")
        # Salvar en la tabla Cliente
        cliente = Cliente(nombre = data['nombre'], apellido = data['apellido'], usuario_id = nuevo_usuario.id)
        cliente.save()

        # Enviar una respuesta JSON de vuelta
        respuesta = {'mensaje': '¡Se ha registrado correctamente el usuario, para verificar la cuenta se ha enviado un enlace a tu correo!'}
        return Response(respuesta, status=status.HTTP_200_OK)

    # Si la solicitud no es POST, devolver un error
    return Response({'error': 'Se esperaba una solicitud POST'}, status=status.HTTP_400_BAD_REQUEST)

