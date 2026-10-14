from unittest.mock import patch

import requests
from constance.test import override_config
from django.test import TestCase, override_settings
from django.urls import reverse

from isterlab.unfold.views import get_ga4_last_30_days_metrics
from .views import verify_recaptcha


class WebsiteRegressionTests(TestCase):
    def test_missing_details_return_404(self):
        for name, kwargs in [
            ('service_details', {'name': 'missing'}),
            ('solution_details', {'name': 'missing'}),
            ('blog_details', {'slug': 'missing'}),
        ]:
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name, kwargs=kwargs)).status_code, 404)

    @override_config(RECAPTCHA_SECRET_KEY='test-secret')
    @patch('landing.views.requests.post', side_effect=requests.Timeout)
    def test_recaptcha_timeout_fails_closed(self, post):
        self.assertFalse(verify_recaptcha('test-token'))
        self.assertEqual(post.call_args.kwargs['timeout'], 10)
        for url in ('contact', 'become_a_partner'):
            response = self.client.post(reverse(url), {'g-recaptcha-response': 'test-token'})
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'reCAPTCHA verification failed')

    @override_config(G4_GOOGLE_ANAYTICS_PROPERTY_ID='')
    def test_dashboard_without_analytics_configuration(self):
        self.assertEqual(get_ga4_last_30_days_metrics()['last_30_days_visitors'], 0)

    @override_config(G4_GOOGLE_ANAYTICS_PROPERTY_ID='missing-test-property')
    @patch('isterlab.unfold.views.BetaAnalyticsDataClient.from_service_account_file', side_effect=FileNotFoundError)
    def test_dashboard_without_credentials(self, client):
        self.assertEqual(get_ga4_last_30_days_metrics()['last_30_days_visitors'], 0)

    @override_settings(SECURE_SSL_REDIRECT=True, ALLOWED_HOSTS=['example.com'])
    def test_internal_healthcheck_survives_https_redirect(self):
        response = self.client.get('/healthz/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})

    @override_config(G4_GOOGLE_ANAYTICS_PROPERTY_ID='')
    def test_dashboard_chart_aligns_days_without_contacts(self):
        import json
        from django.test import RequestFactory
        from isterlab.unfold.views import dashboard_callback
        context = dashboard_callback(RequestFactory().get('/admin/'), {})
        chart = json.loads(context['chart'])
        self.assertEqual(len(chart['labels']), 30)
        for dataset in chart['datasets']:
            self.assertEqual(dataset['data'], [0] * 30)
