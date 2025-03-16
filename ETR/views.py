from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.trainings.models import Training
from .firebase import send_push_to_topic

@api_view(["POST"])
def publish_training(request, id):
    
    train = Training.objects.get(id=id)
    if not train:
        return Response({"error": "the training not found."}, status=404)

    response = send_push_to_topic("all_users", f"{train.name} telah terpublish", train.desc)
    return Response({"message": "Notification sent to all users", "response": response})

