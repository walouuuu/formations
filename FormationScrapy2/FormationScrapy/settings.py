# Scrapy settings for FormationScrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "FormationScrapy"

SPIDER_MODULES = ["FormationScrapy.spiders"]
NEWSPIDER_MODULE = "FormationScrapy.spiders"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0"
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.9"
# USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Retry policies
RETRY_ENABLED = True
RETRY_TIMES = 3  # Retry failed requests 3 times
# RETRY_HTTP_CODES = [500, 400, 429]
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 429]

# RETRY_PRIORITY_ADJUST = -1

DOWNLOADER_MIDDLEWARES = {
    # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "FormationScrapy.middlewares.FormationscrapySpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "FormationScrapy.middlewares.FormationscrapyDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "FormationScrapy.pipelines.FormationscrapyPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


FAKE_HEADERS = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

LINKS = [
'https://www.maformation.fr/formations/domaine_achat-vente.html',
'https://www.maformation.fr/formations/domaine_administrative.html',
'https://www.maformation.fr/formations/domaine_agroalimentaire.html',
'https://www.maformation.fr/formations/domaine_animation.html',
'https://www.maformation.fr/formations/domaine_animaux.html',
'https://www.maformation.fr/formations/domaine_architecture.html',
'https://www.maformation.fr/formations/domaine_artisanat.html',
'https://www.maformation.fr/formations/domaine_audit.html',
'https://www.maformation.fr/formations/domaine_automobile.html',
'https://www.maformation.fr/formations/domaine_banque-assurance.html',
'https://www.maformation.fr/formations/domaine_beaute.html',
'https://www.maformation.fr/formations/domaine_bien-etre.html',
'https://www.maformation.fr/formations/domaine_btp.html',
'https://www.maformation.fr/formations/domaine_bureautique.html',
'https://www.maformation.fr/formations/domaine_commerce.html',
'https://www.maformation.fr/formations/domaine_communication.html',
'https://www.maformation.fr/formations/domaine_comptabilite.html',
'https://www.maformation.fr/formations/domaine_culture.html',
'https://www.maformation.fr/formations/domaine_developpement-personnel.html',
'https://www.maformation.fr/formations/domaine_edition.html',
'https://www.maformation.fr/formations/domaine_electronique.html',
'https://www.maformation.fr/formations/domaine_enseignement.html',
'https://www.maformation.fr/formations/domaine_environnement.html',
'https://www.maformation.fr/formations/domaine_finance.html',
'https://www.maformation.fr/formations/domaine_fonction-publique.html',
'https://www.maformation.fr/formations/domaine_gestion.html',
'https://www.maformation.fr/formations/domaine_graphisme.html',
'https://www.maformation.fr/formations/domaine_hotellerie.html',
'https://www.maformation.fr/formations/domaine_immobilier.html',
'https://www.maformation.fr/formations/domaine_industrie.html',
'https://www.maformation.fr/formations/domaine_informatique.html',
'https://www.maformation.fr/formations/domaine_juridique.html',
'https://www.maformation.fr/formations/domaine_langues.html',
'https://www.maformation.fr/formations/domaine_logistique.html',
'https://www.maformation.fr/formations/domaine_management.html',
'https://www.maformation.fr/formations/domaine_marketing.html',
'https://www.maformation.fr/formations/domaine_nettoyage.html',
'https://www.maformation.fr/formations/domaine_petite-enfance.html',
'https://www.maformation.fr/formations/domaine_qualite.html',
'https://www.maformation.fr/formations/domaine_ressources-humaines.html',
'https://www.maformation.fr/formations/domaine_restauration.html',
'https://www.maformation.fr/formations/domaine_sante.html',
'https://www.maformation.fr/formations/domaine_secretariat.html',
'https://www.maformation.fr/formations/domaine_securite.html',
'https://www.maformation.fr/formations/domaine_social.html',
'https://www.maformation.fr/formations/domaine_sport.html',
'https://www.maformation.fr/formations/domaine_tourisme.html',
'https://www.maformation.fr/formations/domaine_transport.html',
'https://www.maformation.fr/formations/domaine_web.html'
] 
