"""Tests for SocketExfiltrationGuard."""
import unittest
from agent_socket_exfiltration_guard.core import SocketExfiltrationGuard, EgressVerdict

class TestSocketExfiltrationGuard(unittest.TestCase):
    def setUp(self):
        self.guard = SocketExfiltrationGuard(allowed_domains={"api.github.com"})

    def test_allowed_request(self):
        res = self.guard.inspect_request("api.github.com", "/repos", "test data")
        self.assertEqual(res["verdict"], EgressVerdict.ALLOW)

    def test_blocked_domain(self):
        res = self.guard.inspect_request("data-collector.xyz", "/exfil", "some info")
        self.assertEqual(res["verdict"], EgressVerdict.BLOCKED_DOMAIN)

    def test_blocked_secret(self):
        res = self.guard.inspect_request("api.github.com", "/issues", "export ghp_123456789012345678901234567890123456")
        self.assertEqual(res["verdict"], EgressVerdict.BLOCKED_SECRET_LEAK)
