from types import SimpleNamespace
import unittest
from unittest.mock import patch, Mock
import requests
import pwd
import grp


from argo_probe_oidc.fetch_token import utils, NagiosResponse


class MockResponse:
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code

    def json(self):
        return self.data

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.exceptions.RequestException("Error has occured")


def mock_response_json(*args, **kwargs):
    return MockResponse(
        data={
            'access_token': 'mock_hash_access_token',
            'expires_in': 43200,
            'refresh_expires_in': 0,
            'token_type': 'mock_Bearer',
            'id_token': 'mock_id_token',
            'not-before-policy': 0,
            'session_state': 'mock_session_state',
            'scope': 'openid email profile eduperson_entitlement'
        },
        status_code=200
    )


def mock_fail_response_json(*args, **kwargs):
    return MockResponse(
        data={'not_access_token': 'mock_hash_access_token'},
        status_code=200
    )


class ArgoProbeOidcTests(unittest.TestCase):
    def setUp(self) -> None:
        arguments = {"url": "https://mock_path/mock_oidc/mock_token", "client_id": "mock_id", "client_secret": "mock_secret",
                     "refresh_token": "mock_refresh", "token_file": "/etc/mock_nagios/mock_globus/mock_oidc", "timeout": 60}
        self.arguments = SimpleNamespace(**arguments)

    def tearDown(self) -> None:
        NagiosResponse._msgBagCritical = []

    @patch("builtins.print")
    @patch("argo_probe_oidc.fetch_token.requests.post")
    def test_all_passed(self, mock_requests, mock_print):
        mock_requests.side_effect = mock_response_json

        with self.assertRaises(SystemExit) as e:
            utils(self.arguments)

        mock_print.assert_called_once_with(
            'OK - Access token fetched successfully.')
        self.assertEqual(e.exception.code, 0)

    @patch("builtins.print")
    @patch("argo_probe_oidc.fetch_token.requests.post")
    def test_raise_sysexit_on_connection_error(self, mock_requests, mock_print):
        mock_requests.side_effect = mock_fail_response_json

        with self.assertRaises(SystemExit) as e:
            utils(self.arguments)

        mock_print.assert_called_once_with("CRITICAL - 'access_token'")
        self.assertEqual(e.exception.code, 2)

    @patch("builtins.print")
    @patch("argo_probe_oidc.fetch_token.requests.post")
    def test_raise_sysexit_on_ioerror(self, mock_requests, mock_print):
        self.arguments.token_file = "/etcs_mock/mock_nagios/mock_globus/mock_oidc"
        mock_requests.side_effect = mock_response_json

        with self.assertRaises(SystemExit) as e:
            utils(self.arguments)

        mock_print.assert_called_once_with(
            "CRITICAL - Error creating file: [Errno 20] Not a directory: '/etcs_mock/mock_nagios/mock_globus/mock_oidc'")
        self.assertEqual(e.exception.code, 2)

    @patch("builtins.print")
    @patch("argo_probe_oidc.fetch_token.grp.getgrnam")
    @patch("argo_probe_oidc.fetch_token.requests.post")
    def test_raise_sysexit_on_exception(self, mock_requests, mock_grp_getgrnam, mock_print):
        mock_requests.side_effect = mock_response_json
        mock_grp_getgrnam.return_value = "foo_grp"

        with self.assertRaises(SystemExit) as e:
            utils(self.arguments)

        mock_print.assert_called_once_with(
            "CRITICAL - 'str' object has no attribute 'gr_gid'")
        self.assertEqual(e.exception.code, 2)

    @patch("builtins.print")
    @patch('pwd.getpwnam', Mock(auto_spec=True))
    @patch("argo_probe_oidc.fetch_token.requests.post")
    def test_raise_sysexit_on_uid_keyerror(self, mock_requests, mock_print):
        mock_requests.side_effect = mock_response_json
        pwd.getpwnam.side_effect = KeyError

        with self.assertRaises(SystemExit) as e:
            utils(self.arguments)

        mock_print.assert_called_once_with("CRITICAL - No user named 'nagios'")
        self.assertEqual(e.exception.code, 2)

    @patch("builtins.print")
    @patch('grp.getgrnam', Mock(auto_spec=True))
    @patch("argo_probe_oidc.fetch_token.requests.post")
    def test_raise_sysexit_on_gid_keyerror(self, mock_requests, mock_print):
        mock_requests.side_effect = mock_response_json
        grp.getgrnam.side_effect = KeyError

        with self.assertRaises(SystemExit) as e:
            utils(self.arguments)

        mock_print.assert_called_once_with(
            "CRITICAL - No group named 'nagios'")
        self.assertEqual(e.exception.code, 2)


if __name__ == '__main__':
    unittest.main()
