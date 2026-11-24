"""Core Socket Exfiltration Guard implementation."""
import re
from typing import Dict, Any, List, Set, Optional

class EgressVerdict:
    ALLOW = "allow"
    BLOCKED_DOMAIN = "blocked_domain"
    BLOCKED_SECRET_LEAK = "blocked_secret_leak"

class SocketExfiltrationGuard:
    SECRET_PATTERNS = [
        r"(?i)ghp_[a-zA-Z0-9]{36}",
        r"(?i)sk-[a-zA-Z0-9]{32,}",
        r"(?i)aws_secret_access_key",
        r"(?i)bearer\s+[a-zA-Z0-9_\-\.]{30,}"
    ]

    def __init__(self, allowed_domains: Optional[Set[str]] = None):
        self.allowed_domains = allowed_domains or {"api.github.com", "huggingface.co", "api.openai.com"}
        self.secret_regexes = [re.compile(p) for p in self.SECRET_PATTERNS]

    def inspect_request(self, domain: str, path: str, body: str) -> Dict[str, Any]:
        if domain not in self.allowed_domains:
            return {"verdict": EgressVerdict.BLOCKED_DOMAIN, "reason": f"Domain '{domain}' is not on approved whitelist"}

        for r in self.secret_regexes:
            if r.search(body):
                return {"verdict": EgressVerdict.BLOCKED_SECRET_LEAK, "reason": "Request payload contains sensitive API key or token pattern"}

        return {"verdict": EgressVerdict.ALLOW, "reason": "Passed security inspection"}
