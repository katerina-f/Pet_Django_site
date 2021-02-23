from channels.generic.websocket import JsonWebsocketConsumer

from .models import Realty


class ChatConsumer(JsonWebsocketConsumer):
    """Consumer for work with json messages in chat"""

    def receive_json(self, data: dict) -> None:
        message: str = data['message']
        response_message: str = get_response_message(message)
        self.send_json({'message': response_message})


def get_response_message(message: str) -> str:
    """
    Function takes realty name and return saller data,
    if it exists
    """

    dash_index: int = message.find('#')
    if dash_index == -1:
        return 'Пожалуйста, укажите название объекта после #'

    realty_name: str = message[dash_index + 1:].strip()
    try:
        saller: int = Realty.objects.get(name=realty_name).saller
    except Realty.DoesNotExist:
        return 'Ничего не найдено'
    return f'Контактные данные продавца: - Имя :{str(saller)}, Email: {saller.email}'
