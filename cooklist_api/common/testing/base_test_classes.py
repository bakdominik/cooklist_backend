import json
from typing import Optional

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from cooklist_api.users.tests.factories import UserFactory


class BaseTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        token, _ = Token.objects.get_or_create(user=self.user)

    def _post(self, url: str, data: Optional[dict] = None):
        self.client.force_authenticate(user=self.user)
        return self.client.post(
            url,
            data=json.dumps(data) if data else None,
            content_type="application/json",
        )

    def _get(self, url: str, user=None):
        if user:
            self.client.force_authenticate(user=user)
        return self.client.get(url, content_type="application/json")

    def _put(self, url: str, data: Optional[dict] = None):
        self.client.force_authenticate(user=self.user)
        return self.client.put(
            url,
            data=json.dumps(data) if data else None,
            content_type="application/json",
        )

    def _patch(self, url: str, data: Optional[dict] = None):
        self.client.force_authenticate(user=self.user)
        return self.client.patch(
            url,
            data=json.dumps(data) if data else None,
            content_type="application/json",
        )

    def _delete(self, url: str, user=None):
        if user:
            self.client.force_authenticate(user=user)
        return self.client.delete(url, content_type="application/json")
