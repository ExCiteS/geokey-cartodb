from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect

from rest_framework.test import APIRequestFactory

from geokey.users.tests.model_factories import UserFactory
from geokey.projects.tests.model_factories import ProjectFactory
from geokey.contributions.tests.model_factories import ObservationFactory

from ..views import IndexPage, ProjectDataView
from ..models import CartoDbProject


class CartoDBProjectsTest(TestCase):
    def test_get_with_user(self):
        view = IndexPage.as_view()
        url = reverse('geokey_cartodb:index')
        request = APIRequestFactory().get(url)
        request.user = UserFactory.create(**{'is_superuser': False})
        response = view(request).render()
        self.assertEqual(response.status_code, 200)

    def test_get_with_anonymous(self):
        view = IndexPage.as_view()
        url = reverse('geokey_cartodb:index')
        request = APIRequestFactory().get(url)
        request.user = AnonymousUser()
        response = view(request)
        self.assertTrue(isinstance(response, HttpResponseRedirect))

    def test_post_with_anonymous(self):
        project_1 = ProjectFactory.create()
        view = IndexPage.as_view()
        url = reverse('geokey_cartodb:index')
        request = APIRequestFactory().post(url, data={'form': [project_1.id]})
        request.user = AnonymousUser()
        response = view(request)
        self.assertTrue(isinstance(response, HttpResponseRedirect))

    def test_post_with_user(self):
        project_1 = ProjectFactory.create()
        view = IndexPage.as_view()
        url = reverse('geokey_cartodb:index')
        request = APIRequestFactory().post(url, data={'form': [project_1.id]})
        request.user = UserFactory.create(**{'is_superuser': False})
        response = view(request).render()
        self.assertEqual(response.status_code, 200)

    def test_update_projects(self):
        project_1 = ProjectFactory.create()
        project_2 = ProjectFactory.create()
        project_3 = ProjectFactory.create()

        CartoDbProject.objects.create(project=project_1, enabled=True)
        CartoDbProject.objects.create(project=project_2, enabled=True)

        view = IndexPage()
        view.update_projects(
            [project_1, project_2, project_3],
            [project_1, project_2],
            form=[str(project_1.id), str(project_3.id)]
        )

        enabled = [prj.project for prj in CartoDbProject.objects.all()]
        self.assertIn(project_1, enabled)
        self.assertNotIn(project_2, enabled)
        self.assertIn(project_3, enabled)


class APITest(TestCase):
    def test_project(self):
        project = ProjectFactory.create()
        ObservationFactory.create_batch(2, **{'project': project})
        CartoDbProject.objects.create(project=project, enabled=True)
        factory = APIRequestFactory()
        url = reverse('geokey_cartodb:project_data', kwargs={
            'project_id': project.id
        })
        request = factory.get(url)

        view = ProjectDataView.as_view()
        response = view(request, project_id=project.id).render()
        self.assertEqual(response.status_code, 200)

    def test_project_not_enabled(self):
        project = ProjectFactory.create()
        ObservationFactory.create_batch(2, **{'project': project})

        factory = APIRequestFactory()
        url = reverse('geokey_cartodb:project_data', kwargs={
            'project_id': project.id
        })
        request = factory.get(url)

        view = ProjectDataView.as_view()
        response = view(request, project_id=project.id).render()
        self.assertEqual(response.status_code, 404)
