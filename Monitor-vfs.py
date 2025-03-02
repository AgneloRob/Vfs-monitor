import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

# Configuração do e-mail
EMAIL_SENDER = "seuemail@gmail.com"
EMAIL_PASSWORD = "suasenha"
EMAIL_RECEIVER = "seuemail@gmail.com"

# URL da VFS Global (mude para o país e serviço que deseja monitorar)
URL = "https://visa.vfsglobal.com/ago/pt/por/agendar-um-compromisso"

def check_vfs_slots():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    # Verificar se há texto indicando que não há vagas
    if "Nenhuma vaga disponível" not in soup.text:
        send_email_alert()

def send_email_alert():
    subject = "Vaga disponível na VFS Global!"
    body = f"Encontre sua vaga agora: {URL}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

# Executar o monitoramento
check_vfs_slots()
