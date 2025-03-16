import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("media/conf/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def send_push_to_topic(topic, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        topic=topic
    )
    response = messaging.send(message)
    return response