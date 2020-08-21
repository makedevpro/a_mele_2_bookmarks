from django.contrib.contenttypes.models import ContentType

from .models import Action


def create_action(user, verb, target=None):
    """ Создаем пользовательское действие и связываем его с объектом target """

    action = Action(user=user, verb=verb, target=target)
    action.save()
