import unittest
import pymacaroons
import responses
import canonicalwebteam.snapstoreapi.public_api as public_api
import canonicalwebteam.snapstoreapi.publisher_api as publisher_api
import canonicalwebteam.snapstoreapi.exceptions as exceptions


# Make sure tests fail on stray responses.
responses.mock.assert_all_requests_are_fired = True


class SimpleTestsApi(unittest.TestCase):

    @responses.activate
    def test_public_api(self):
        url = (
            'https://api.snapcraft.io/api/v1/snaps/search'
            '?confinement=strict,classic&q=&section=featured.'
        )

        payload = {'api': 'works'}
        responses.add(
            responses.GET, url,
            json=payload, status=200)

        toto = public_api.get_searched_snaps('toto', 1, 1)

        self.assertEqual(toto, payload)

    @responses.activate
    def test_publisher_api(self):
        snap_name = "test-snap"

        api_url = 'https://dashboard.snapcraft.io/dev/api/snaps/info/{}'
        api_url = api_url.format(
            snap_name
        )

        payload = {'api': 'yolo'}
        responses.add(
            responses.GET, api_url,
            json=payload, status=200)

        root = pymacaroons.Macaroon('test', 'testing', 'a_key')
        root.add_third_party_caveat('3rd', 'a_caveat-key', 'a_ident')
        discharge = pymacaroons.Macaroon('3rd', 'a_ident', 'a_caveat_key')
        response = publisher_api.get_snap_info('test-snap', {
            'macaroon_root': root.serialize(),
            'macaroon_discharge': discharge.serialize(),
        })

        self.assertEqual(payload, response)

    @responses.activate
    def test_publisher_api_execption(self):
        snap_name = "test-snap"

        api_url = 'https://dashboard.snapcraft.io/dev/api/snaps/info/{}'
        api_url = api_url.format(
            snap_name
        )

        payload = {
            'error_list': [
                {
                    'code': 'user-not-ready',
                    'message': 'missing namespace'
                }
            ]
        }
        responses.add(
            responses.GET, api_url,
            json=payload, status=500)

        root = pymacaroons.Macaroon('test', 'testing', 'a_key')
        root.add_third_party_caveat('3rd', 'a_caveat-key', 'a_ident')
        discharge = pymacaroons.Macaroon('3rd', 'a_ident', 'a_caveat_key')

        with self.assertRaises(exceptions.MissingUsername):
            publisher_api.get_snap_info(
                'test-snap',
                {
                    'macaroon_root': root.serialize(),
                    'macaroon_discharge': discharge.serialize(),
                },
            )


if __name__ == '__main__':
    unittest.main()
