import json
from unittest.mock import patch

from django.test import TestCase

from .consumer import ChatConsumer
from .views import build_conversation_flow
from landing.models import FAQ


class ChatbotRegressionTests(TestCase):
    @patch('chatbot.consumer.config', return_value='')
    def test_optional_api_key_and_malformed_payload(self, config):
        consumer = ChatConsumer()
        self.assertIn('not configured', consumer.generate_ai_response('Hello'))
        for payload in ('{', '[]', 'null'):
            with self.subTest(payload=payload), patch.object(consumer, 'send') as send:
                consumer.receive(text_data=payload)
                self.assertEqual(json.loads(send.call_args.kwargs['text_data'])['error'], 'Invalid message format.')
        self.assertFalse(consumer.is_valid_message(None))
        self.assertFalse(consumer.is_valid_message(''))
        self.assertTrue(consumer.is_valid_message('Bonjour — مرحبا'))

    def test_conversation_data_escapes_script_terminator(self):
        FAQ.objects.create(question='</script><script>alert(1)</script>', response='answer')
        self.assertIsInstance(build_conversation_flow(), dict)
        response = self.client.get('/chatbot_view/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '\\u003C/script\\u003E')
        self.assertNotContains(response, '</script><script>alert(1)</script>')
