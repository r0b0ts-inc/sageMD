import pytest
from hypothesis.extra.django import TestCase
from mixer.backend.django import mixer
from hypothesis import strategies as st, given  # This is to help test for all form of edge cases we may have
# missed, that a random user might enter into the system

from ..models import IwiseUser

# This line below tells pytest not to save data we generate here to the database and should just hold it in memory
# and destroy after test runs
pytestmark = pytest.mark.django_db


class TestBaseUserAccount(TestCase):
    def test_user_account_creation(self):
        model_object = mixer.blend(IwiseUser)
        assert model_object.pk == 1, 'Should create a Base User Instance'
        assert model_object.username is not None, "No username allowed for this model"
        assert str(model_object) == "{0}".format(model_object.email)
