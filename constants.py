HEADLESS_MODE=False

OPTIONS = {
    'args': [
        '--disable-gpu',
        '--disable-dev-shm-usage',
        '--disable-setuid-sandbox',
        '--no-first-run',
        '--no-sandbox',
        '--no-zygote',
        '--ignore-certificate-errors',
        '--disable-extensions',
        '--disable-infobars',
        '--disable-notifications',
        '--disable-popup-blocking',
        # '--remote-debugging-port=9201',
        "--deterministic-fetch",
        "--disable-features=IsolateOrigins,site-per-process",
        "--disable-site-isolation-trials",
        "--disable-web-security",
        "--disable-blink-features=AutomationControlled",
        "--disable-component-extensions-with-background-pages"
    ],
    'headless': HEADLESS_MODE  # Set headless option here
}