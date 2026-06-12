import requests


def get_tor_session():
    """
    Create a requests session routed through Tor SOCKS proxy.
    """

    session = requests.Session()

    session.proxies = {
        "http": "socks5h://127.0.0.1:9050",
        "https": "socks5h://127.0.0.1:9050"
    }

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (CTI-Tor-Crawler)"
    })

    return session


def test_tor_connection():
    """
    Verify Tor is working correctly.
    """

    session = get_tor_session()

    try:
        r = session.get("http://httpbin.org/ip", timeout=20)
        print("[TOR IP] ->", r.text)

    except Exception as e:
        print("[ERROR TOR] ->", e)


def test_public_ip():
    """
    Compare with real IP (no Tor)
    """
    r = requests.get("http://httpbin.org/ip", timeout=20)
    print("[PUBLIC IP] ->", r.text)
