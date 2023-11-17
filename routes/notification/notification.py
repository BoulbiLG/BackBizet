from flask import Blueprint, request, jsonify
from webpush import WebPusher
import json

notification = Blueprint('notification', __name__)

@notification.route('/abonnementNotification', methods=['POST'])
def save_subscription():
    subscription = request.json['subscription']
    return jsonify({'success': True}), 201

@notification.route('/envoieNotification', methods=['POST'])
def send_notification():
    subscription = {
        'endpoint': 'https://fcm.googleapis.com/fcm/send/[token]',
        'keys': {
            'p256dh': '[your_p256dh_key]',
            'auth': '[your_auth_key]'
        }
    }
    
    webpush = WebPusher(subscription)
    
    notification_payload = {
        'title': 'Notification title',
        'body': 'Notification body',
        'icon': 'https://example.com/icon.png'
    }

    try:
        webpush.send(json.dumps(notification_payload))
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
