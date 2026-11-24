"""CLI for Socket Exfiltration Guard."""
import argparse
from .core import SocketExfiltrationGuard

def main():
    parser = argparse.ArgumentParser(description="Agent Socket Exfiltration Guard CLI")
    parser.add_argument("--domain", default="evil-server.com", help="Destination domain")
    parser.add_argument("--payload", default="safe query text", help="Payload content")
    args = parser.parse_args()

    guard = SocketExfiltrationGuard()
    res = guard.inspect_request(args.domain, "/upload", args.payload)
    print(f"Verdict: {res['verdict']} - {res['reason']}")

if __name__ == "__main__":
    main()
