"""
    Copyright (C) 2017, ContraxSuite, LLC

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    You can also be released from the requirements of the license by purchasing
    a commercial license from ContraxSuite, LLC. Buying such a license is
    mandatory as soon as you develop commercial activities involving ContraxSuite
    software without disclosing the source code of your own applications.  These
    activities include: offering paid services to customers as an ASP or "cloud"
    provider, processing documents on the fly in a web application,
    or shipping ContraxSuite within a closed source product.
"""
# -*- coding: utf-8 -*-

import asyncio
from typing import Optional, Set, Dict, Iterable

import redis
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer
from channels_redis.core import RedisChannelLayer
from django.conf import settings
from django.db.models import QuerySet
from django.db import connection
from rest_framework.authtoken.models import Token

from apps.common.singleton import Singleton
from apps.task.utils.logger import get_django_logger
from apps.users.models import User
from apps.websocket.channel_message import ChannelMessage

__author__ = "ContraxSuite, LLC; LexPredict, LLC"
__copyright__ = "Copyright 2015-2020, ContraxSuite, LLC"
__license__ = "https://github.com/LexPredict/lexpredict-contraxsuite/blob/1.6.0/LICENSE"
__version__ = "1.6.0"
__maintainer__ = "LexPredict, LLC"
__email__ = "support@contraxsuite.com"


USER = 'user'
ALL = 'all'
USER_GROUP_PREFIX = 'user_'
ASGI_GROUP_PREFIX = 'asgi::group:'


@Singleton
class Websockets:
    """
    Common endpoint for operations related to websockets:
    - sending messages to connected users;
    - listing connected users.
    """

    def __init__(self) -> None:
        super().__init__()
        self.r = redis.Redis.from_url(settings.CELERY_CACHE_REDIS_URL)

    def user_id_to_group_name(self, user_id: int) -> str:
        """
        Convert user id to django-channels 2 group name.
        Django channels operates on the "groups" concept. To manage connected users and not groups the
        connected channels are added to the groups named in a specific format based on the user id.
        This way we cen get user id by group name and vice versa.

        :param user_id:
        :return:
        """
        return USER_GROUP_PREFIX + str(user_id)

    def group_name_to_user_id(self, group_name: str) -> Optional[int]:
        """
        Convert django-channels 2 group name to user id.
        Django channels operates on the "groups" concept. To manage connected users and not groups the
        connected channels are added to the groups named in a specific format based on the user id.
        This way we cen get user id by group name and vice versa.

        :param group_name:
        :return:
        """
        if group_name and group_name.startswith(USER_GROUP_PREFIX):
            try:
                return int(group_name[len(USER_GROUP_PREFIX):])
            except:
                return None
        else:
            return None

    def send_to_all_users(self, message_obj: ChannelMessage):
        """
        Send the message to all connected users.
        Each authenticated user is added to a special ALL group and this method sends the message into this group.
        :param message_obj:
        :return:
        """
        layer = get_channel_layer()  # type: RedisChannelLayer
        async_to_sync(layer.group_send)(ALL, {'type': 'send_to_client', 'message': message_obj.to_dict()})

    async def _send_to_users(self, qs_users: QuerySet, message_obj: ChannelMessage):
        """
        Send the message to the users returned by the specified Django query set.

        This is an async method made private for calling it from the sync public method.
        :param qs_users: Django query set returning User models. Pk field will be requested via values_list(..).
        :param message_obj: Message to send.
        :return:
        """
        connected_user_ids = self.get_connected_users()
        if not connected_user_ids:
            return

        # A workaround for "connection already closed" problem.
        # Looks like this code is being executed in a way that
        # the "connection" object it accesses is re-used for a long time and appears broken after some long delay.
        connection.close()

        layer = get_channel_layer()  # type: RedisChannelLayer
        msg = {'type': 'send_to_client', 'message': message_obj.to_dict()}
        coros = list()
        for user_id in qs_users.filter(pk__in=connected_user_ids).values_list('pk', flat=True):
            send_to_user_coro = layer.group_send(self.user_id_to_group_name(user_id), msg)
            coros.append(send_to_user_coro)
        await asyncio.gather(*coros)

    def send_to_users(self, qs_users: QuerySet, message_obj: ChannelMessage):
        """
        Send the message to the users returned by the specified Django query set.

        :param qs_users: Django query set returning User models. Pk field will be requested via values_list(..).
        :param message_obj: Message to send.
        :return:
        """
        async_to_sync(self._send_to_users)(qs_users, message_obj)

    def send_to_user(self, user_id, message_obj: ChannelMessage):
        """
        Send the message to the specified user.
        :param user_id: ID of the user.
        :param message_obj: Message to send.
        :return:
        """
        layer = get_channel_layer()  # type: RedisChannelLayer
        async_to_sync(layer.group_send)(self.user_id_to_group_name(user_id),
                                        {'type': 'send_to_client', 'message': message_obj.to_dict()})

    def _list_groups(self) -> Iterable[str]:
        """
        List all django channel groups by reading Redis keys.
        :return:
        """
        for key in self.r.scan_iter(ASGI_GROUP_PREFIX + '*'):
            yield key.decode('utf-8')[len(ASGI_GROUP_PREFIX):]

    def get_connected_users(self) -> Set[int]:
        """
        List all connected users.

        Users are represented by groups named with a special prefix.
        On each websocket connect and user authentication its channel is added to the user's group.
        On each disconnect - the channel is removed.
        Django channels 2 adds/removes the corresponding keys in Redis.
        As tested - when two users are connected from different browsers and next one of them disconnects the
        corresponding group is still present. Next when the last user disconnects the group is removed.
        :return:
        """
        res = set()
        for key in self._list_groups():
            user_id = self.group_name_to_user_id(key)
            if user_id:
                res.add(user_id)
        return res


class ContraxsuiteWSConsumer(AsyncJsonWebsocketConsumer):
    """
    Consumer class for django-channels 2. Handles single Websocket connection.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = get_django_logger()
        self.ws = Websockets()

    async def connect(self):
        user = self.scope.get(USER)
        if user and not user.is_anonymous:
            await self._add_to_groups(user)
        self.logger.info(f'Client connection: {self.scope.get("client")}. User: {user}')
        return await super().connect()

    async def receive_json(self, content, **kwargs):
        """
        Handle websocket message in JSON format coming from the client.
        :param content:
        :param kwargs:
        :return:
        """
        user = self.scope[USER]
        if user is None or user.is_anonymous:
            user = await self.authenticate(content.get('token'))
            self.logger.info(f'{self.scope.get("client")} | Authenticated as: {user}')
            if not user:
                self.logger.info(f'{self.scope.get("client")} | User not authenticated. Closing connection.')
                await self.close()
                return

    async def _add_to_groups(self, user: User):
        channel_layer = self.channel_layer  # type: RedisChannelLayer
        user_group_name = self.ws.user_id_to_group_name(user.pk)
        self.logger.info(
            f'{self.scope.get("client")} | Adding channel {self.channel_name} to groups: {ALL}, {user_group_name}')
        await channel_layer.group_add(user_group_name, self.channel_name)
        await channel_layer.group_add(ALL, self.channel_name)

    async def authenticate(self, token_key: str) -> Optional[User]:
        """
        Authenticate user by the specified token.
        :param token_key:
        :return: Either user found by the token or None if token is invalid.
        """
        if not token_key:
            return None
        token_key = token_key.replace('Token ', '').strip()
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
            if not user or user.is_anonymous:
                self.logger.error(
                    f'{self.scope.get("client")} | User of token {token_key} is not specified or anonymous')
                return None
            self.scope[USER] = user
            await self._add_to_groups(user)
            return user
        except Exception as e:
            self.logger.error(f'{self.scope.get("client")} | Could not find token by key ({token_key})', exc_info=e)
            return None

    async def send_to_client(self, message: Dict):
        """
        Handle "send_to_client" message type for messages sent via layer.group_send(..)
        :param message:
        :return:
        """
        await self.send_json(content=message.get('message'))

    async def disconnect(self, code):
        """
        Handle correct websocket disconnect - remove this channel from the groups.
        :param code:
        :return:
        """
        user = self.scope[USER]
        self.logger.info(f'{self.scope.get("client")} | User disconnected: {user}')
        if user and not user.is_anonymous:
            channel_layer = self.channel_layer  # type: RedisChannelLayer
            await channel_layer.group_discard(self.ws.user_id_to_group_name(user.pk), self.channel_name)
            await channel_layer.group_discard(ALL, self.channel_name)
        return await super().disconnect(code)
