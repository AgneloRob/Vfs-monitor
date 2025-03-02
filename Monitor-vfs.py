import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

# Configuração do e-mail
EMAIL_SENDER = "seuemail@gmail.com"
EMAIL_PASSWORD = "SENHA_DE_APLICATIVO"  # Gere uma senha de aplicativo no Gmail
EMAIL_RECEIVER = "seuemail@gmail.com"

# URL da VFS Global (modifique conforme necessário)
URL = "https://visa.vfsglobal.com/ago/pt/por/agendar-um-compromisso"

# Cabeçalhos para evitar bloqueios
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def check_vfs_slots():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Garante que a requisição foi bem-sucedida

        soup = BeautifulSoup(response.text, "html.parser")

        # Verificar se há texto indicando vagas disponíveis
        if "Nenhuma vaga disponível" in soup.text:
            print("Nenhuma vaga disponível no momento.")
        else:
            print("Vaga encontrada! Enviando alerta...")
            send_email_alert()
    
    except requests.RequestException as e:
        print(f"Erro ao acessar a página da VFS: {e}")

def send_email_alert():
    try:
        subject = "Vaga disponível na VFS Global!"
        body = f"Encontre sua vaga agora: {URL}"
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())

        print("Alerta enviado com sucesso!")
    
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# Executar o monitoramento
check_vfs_slots()
