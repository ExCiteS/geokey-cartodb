from django.test import TestCase

from projects.tests.model_factories import ProjectF
from categories.tests.model_factories import (
    CategoryFactory, TextFieldFactory, NumericFieldFactory
)
from contributions.tests.model_factories import ObservationFactory

from ..serializer import CartoDbSerializer


class SerializerTest(TestCase):
    def test_convert_value(self):
        observation = ObservationFactory.create()
        serializer = CartoDbSerializer(observation)

        self.assertIsNone(serializer.convert_value(None))
        self.assertEqual(type(serializer.convert_value('2.31')), float)
        self.assertEqual(type(serializer.convert_value('2')), int)
        self.assertEqual(type(serializer.convert_value('blah')), str)

    def test_serializer(self):
        project = ProjectF.create()
        category = CategoryFactory.create(**{'project': project})
        TextFieldFactory.create(**{'key': 'text', 'category': category})
        NumericFieldFactory.create(**{'key': 'float', 'category': category})
        NumericFieldFactory.create(**{'key': 'int', 'category': category})

        observation = ObservationFactory.create(**{
            'category': category,
            'attributes': {'text': 'Blah', 'float': 1.23, 'int': 2}
        })
        serializer = CartoDbSerializer(observation)
        self.assertEqual(
            serializer.data.get('properties'),
            {'text': 'Blah', 'float': 1.23, 'int': 2}
        )
