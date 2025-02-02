from celery import shared_task
from users.models import User


@shared_task
def cancel_code_activity(user_id):
    """Делает код неактивным"""
    user = User.objects.get(id=user_id)
    if not user.is_code_valid():
        user.clear_code()