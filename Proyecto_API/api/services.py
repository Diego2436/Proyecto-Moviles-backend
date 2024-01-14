import smtplib, secrets, string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendEmail(email, type, token_or_password=None):
    # Configuración del servidor SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'davidoconer555@gmail.com'
    smtp_password = 'cxcdngwlbfqeznii'

    # Direcciones de correo (puedes enviar a múltiples destinatarios separándolos por comas)
    from_email = 'davidoconer555@gmail.com'
    to_email = email

    # Configuración del mensaje
    if type == "register":
        subject = 'Verificacion de la cuenta FoodTrucks'
        body = f"Entras al siguiente enlace para verificar la cuenta: http://127.0.0.1:8000/api/cuenta/verificar/?token={token_or_password}"
    if type == "recover_password":
        subject = 'Recuerar password de la cuenta de FoodTrucks'
        body = f"Tu contraseña es la siguiente: {token_or_password}"

    # Construir el mensaje
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Conectar al servidor SMTP y enviar el correo
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, to_email, message.as_string())
        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"No se pudo enviar el correo. Error: {e}")

def random_password(longitud=6):
    caracteres = string.ascii_letters + string.digits  # letras y dígitos
    contrasena_plana = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    return contrasena_plana