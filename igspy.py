from instagrapi import Client
from plyer import notification
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("""

  ___   ____   _      ____  ____     ___       _____ ____  __ __  ⣿⡿⠋⠀⠀⢀⣠⣤⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣦⣤⣤⣀⠀⠀⠈⢻⣿
 /   \ |    \ | |    |    ||    \   /  _]     / ___/|    \|  |  | ⡿⠁⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠻⢿⣷⡄⠀⠀⢻
|     ||  _  || |     |  | |  _  | /  [_     (   \_ |  o  )  |  | ⠇⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⠿⠿⢿⣿⣿⣿⡇⠀⠀⢈⣿⣿⡀⠀⠘
|  O  ||  |  || |___  |  | |  |  ||    _]     \__  ||   _/|  ~  | ⠀⠀⠀⣿⣿⣿⣿⣿⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣦⣴⣾⣿⣿⡇
|     ||  |  ||     | |  | |  |  ||   [_      /  \ ||  |  |___, | ⠀⠀⢸⣿⣿⣿⣿⣿⠏⠀⠀⢀⣴⣾⣿⣿⣷⣦⣄⠀⠀⠙⣿⣿⣿⣿⣿⡇
|     ||  |  ||     | |  | |  |  ||     |     \    ||  |  |     | ⠀⠀⢸⣿⣿⣿⣿⡏⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⢸⣿⣿⣿⣿⡇
 \___/ |__|__||_____||____||__|__||_____|      \___||__|  |____/   ⠀⢸⣿⣿⣿⣿⡇⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢀⣿⣿⣿⣿⡇⠀
                                                                  ⠀⠀⢸⣿⣿⣿⣿⣇⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢸⣿⣿⣿⣿⡇
   ______  __   __       ______ _______ _     _  _____             ⠀⠸⣿⣿⣿⣿⣿⣆⠀⠀⠙⠻⢿⣿⣿⣿⠿⠋⠀⠀⣠⣿⣿⣿⣿⣿⡇
   |_____]   \_/        |  ____ |______ |____/  |     |              ⣿⣿⣿⣿⣿⣿⣷⣄⡀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⣿⡇⠀
   |_____]    |         |_____| |______ |    \_ |_____|          ⡇⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣤⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁
                                                                 ⣷⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⣼
                                                                 ⣿⣷⡀⠀⠀⠉⠛⠛⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠛⠛⠉⠀⠀⢀⣼⣿
""")

def send_notification(message):
    notification.notify(
        title='Instagram Notification',
        message=message,
        timeout=10
    )

def send_email(subject, body, to_email):
    from_email = "tu_email@gmail.com"   #Poner correo el cual envie las notificaciones 
    from_password = "tu_contraseña_de_gmail"  #Poner contraseña de aplicacion

    # Crear el mensaje de correo electrónico
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Establecer conexión con el servidor de Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print(f'Correo enviado a {to_email}')
    except Exception as e:
        print(f'Error al enviar correo: {e}')

def check_online_status(username, password, target_username, to_email):
    client = Client()
    client.login(username, password)
    
    target_user_id = client.user_id_from_username(target_username)

    previous_status = None

    while True:
        user_info = client.user_info(target_user_id)
        current_status = user_info.is_online

        if current_status != previous_status:
            if current_status:
                message = f'{target_username} se ha conectado'
                send_email(
                    subject='Instagram Notification',
                    body=message,
                    to_email=to_email
                )
            else:
                message = f'{target_username} se ha desconectado'
                send_email(
                    subject='Instagram Notification',
                    body=message,
                    to_email=to_email
                )
            send_notification(message)
            print(message)

        previous_status = current_status
        time.sleep(60)  # Chequear cada minuto

if __name__ == "__main__":
    # Reemplaza con tus credenciales de Instagram
    username = input("[+] Ingrese tu usuario de Instagram: ")
    password = input("[+] Ingrese su contraseña de Instagram: ")
    # Reemplaza con el nombre de usuario de la cuenta que quieres monitorear
    target_username = input("[+] Ingrese el usuario a monitorear: ")
    # Reemplaza con tu correo electrónico
    to_email = input("[+] Ingrese el correo al cual enviar las notificaciones: ")

    check_online_status(username, password, target_username, to_email)
