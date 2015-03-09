from django.test import TestCase

from projects.tests.model_factories import ProjectF
from categories.tests.model_factories import CategoryFactory, TextFieldFactory
from contributions.tests.model_factories import ObservationFactory

from ..serializer import CartoDbSerializer


class SerializerTest(TestCase):
    def test_serializer(self):
        project = ProjectF.create()
        category = CategoryFactory.create(**{'project': project})
        TextFieldFactory.create(**{'key': 'text', 'category': category})
        observation = ObservationFactory.create(**{
            'category': category,
            'attributes': {'text': 'Blah'}
        })
        serializer = CartoDbSerializer(observation)
        self.assertEqual(serializer.data.get('properties'), {'text': 'Blah'})
