from flask import Flask, request, jsonify, Blueprint
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

mailEnvoie = Blueprint('mailEnvoie', __name__)

@mailEnvoie.route('/mailEnvoie', methods=['POST'])
def send_email():
    data = request.get_json()

    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    print('email : ', email)
    print('subject : ', subject)
    print('message : ', message)

    if not email or not subject or not message:
        return jsonify({'error': 'Tous les champs doivent être remplis'}), 400

    smtp_server = 'smtp.example.com'
    smtp_port = 587
    smtp_username = 'your_username'
    smtp_password = 'your_password'
    sender_email = 'your_email@example.com'
    receiver_email = 'destination@example.com'

    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        return jsonify({'success': 'E-mail envoyé avec succès'}), 200

    except Exception as e:
        return jsonify({'error': f'Erreur lors de l\'envoi de l\'e-mail: {str(e)}'}), 500