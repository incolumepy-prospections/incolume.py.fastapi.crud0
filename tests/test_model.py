import pytest
from incolume.py.fastapi.crud0 import models


__author__ = '@britodfbr'  # pragma: no cover


class TestModels:
    @pytest.mark.parametrize(
        'instance class_model'.split(),
        (
            (models.UserModel(username='user@example.com', email='user@email.com', full_name='user@example.com'), models.UserModel),
            (models.ItemModel(title='abc', description='abc'), models.ItemModel),
        )
    )
    def test_instance(self, instance, class_model):
        assert isinstance(instance, class_model)

    @pytest.mark.parametrize(
        'entrance expected'.split(),
        (
            (
                models.UserModel(username='user@example.com', email='user@email.com', full_name='user@example.com'),
                'UserModel(id=None, username=user@example.com, email=user@email.com, is_active=None, roles=None)'
            ),
            pytest.param(models.ItemModel(title='abc', description='abc'), models.ItemModel, marks=pytest.mark.skip(reason='Not implemented.')),
        )
    )
    def test_str(self, entrance, expected):
        assert expected in str(entrance)
