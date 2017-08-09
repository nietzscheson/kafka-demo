import unittest
import requests
import json
import os

producer_host = os.environ.get('JBHH_PCDEMO_PHOST') or 'localhost'
producer_port = os.environ.get('JBHH_PCDEMO_PPORT') or 8282
consumer_host = os.environ.get('JBHH_PCDEMO_PHOST') or 'localhost'
consumer_port = os.environ.get('JBHH_PCDEMO_PPORT') or 8283

producer_url = "http://{0}:{1}/events".format(producer_host, producer_port)
consumer_url = "http://{0}:{1}/events".format(consumer_host, consumer_port)

# These aren't really unit tests but the unittest package seems like a convenient way to run integration tests, too
class TestProducerConsumer(unittest.TestCase):

    def setUp(self):
        #drain the queue
        while requests.get(consumer_url).status_code == 200:
            pass

    def send_event(self, event):
        return requests.post(producer_url, json=json.dumps(event), headers={'Content-Type': 'application/json'})

    def test_post_an_event(self):
        #Just checks that we even have a connection.
        event = {'name': 'test', 'payload': 'rock and also roll'}
        response = self.send_event(event);
        self.assertTrue(response.ok)
        self.assertTrue(response.json(), '{"status": "success"}')

    def test_get_from_empty_queue(self):
        resp = requests.get(consumer_url)
        self.assertEqual(resp.status_code,204)
        self.assertEqual(resp.content, "")

    def test_get_single_event(self):
        event = {'name': 'test', 'payload': 'This is the best event'}
        response = self.send_event(event)
        self.assertTrue(response.ok)
        response= requests.get(consumer_url)
        self.assertTrue(response.ok)
        revent = json.loads(response.json())
        self.assertEqual(revent, event)

    def test_get_multiple_events(self):
        events = [
            {'name': 'test', 'payload': 'Potato Potato'},
            {'name': 'test', 'payload': 'Hampered Scarlet'},
            {'name': 'test', 'payload': 'twenty seven pennies'}]

        for event in events:
            response = self.send_event(event)
            self.assertTrue(response.ok)

        for event in events:
            response = requests.get(consumer_url)
            self.assertTrue(response.ok)
            revent = json.loads(response.json())
            self.assertEqual(revent, event)



if __name__ == '__main__':
    unittest.main()