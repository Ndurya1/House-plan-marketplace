from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from users.models import User
from catalogue.models import Catalogue


class CataloguePermissionsTests(TestCase):
    def setUp(self):
        # Create users and profiles
        self.seller_a = User.objects.create_user(
            username='sellerA@example.com',
            email='sellerA@example.com',
            password='Password123!',
            role=User.UserChoices.SELLER,
            name='Seller A'
        )

        self.seller_b = User.objects.create_user(
            username='sellerB@example.com',
            email='sellerB@example.com',
            password='Password123!',
            role=User.UserChoices.SELLER,
            name='Seller B'
        )

        self.buyer = User.objects.create_user(
            username='buyer@example.com',
            email='buyer@example.com',
            password='Password123!',
            role=User.UserChoices.BUYER,
            name='Buyer'
        )

        self.admin = User.objects.create_user(
            username='admin@example.com',
            email='admin@example.com',
            password='Password123!',
            role=User.UserChoices.ADMIN,
            name='Admin'
        )

        # Create a catalog item owned by seller A
        self.plan = Catalogue.objects.create(
            title='Mansion Plan',
            category='Mansion',
            category_group=Catalogue.CategoryGroup.RESIDENTIAL,
            price=15000.00,
            seller=self.seller_a.sellerprofile
        )

    def test_anonymous_can_list_and_retrieve_plans(self):
        # List plans
        url = reverse('catalogue-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Retrieve plan detail
        url_detail = reverse('catalogue-detail', kwargs={'pk': self.plan.pk})
        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def get_auth_header(self, user):
        from rest_framework_simplejwt.tokens import AccessToken
        token = AccessToken.for_user(user)
        return {'HTTP_AUTHORIZATION': f'Bearer {token}'}

    def test_buyer_cannot_create_plan(self):
        url = reverse('catalogue-list')
        response = self.client.post(
            url,
            {
                'title': 'New Plan',
                'category': 'Villa',
                'category_group': Catalogue.CategoryGroup.RESIDENTIAL,
                'price': '20000.00'
            },
            content_type='application/json',
            **self.get_auth_header(self.buyer)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_seller_can_create_plan(self):
        url = reverse('catalogue-list')
        response = self.client.post(
            url,
            {
                'title': 'Modern Villa',
                'category': 'Villa',
                'category_group': Catalogue.CategoryGroup.RESIDENTIAL,
                'price': '35000.00'
            },
            content_type='application/json',
            **self.get_auth_header(self.seller_a)
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_seller_can_update_own_plan(self):
        url = reverse('catalogue-detail', kwargs={'pk': self.plan.pk})
        response = self.client.put(
            url,
            {
                'title': 'Mansion Plan Updated',
                'category': 'Mansion',
                'category_group': Catalogue.CategoryGroup.RESIDENTIAL,
                'price': '16000.00'
            },
            content_type='application/json',
            **self.get_auth_header(self.seller_a)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.plan.refresh_from_db()
        self.assertEqual(self.plan.title, 'Mansion Plan Updated')

    def test_seller_cannot_update_other_seller_plan(self):
        url = reverse('catalogue-detail', kwargs={'pk': self.plan.pk})
        response = self.client.put(
            url,
            {
                'title': 'Hacked Plan',
                'category': 'Mansion',
                'category_group': Catalogue.CategoryGroup.RESIDENTIAL,
                'price': '10.00'
            },
            content_type='application/json',
            **self.get_auth_header(self.seller_b)
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_any_seller_plan(self):
        url = reverse('catalogue-detail', kwargs={'pk': self.plan.pk})
        response = self.client.put(
            url,
            {
                'title': 'Admin Plan Fix',
                'category': 'Mansion',
                'category_group': Catalogue.CategoryGroup.RESIDENTIAL,
                'price': '15000.00'
            },
            content_type='application/json',
            **self.get_auth_header(self.admin)
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
