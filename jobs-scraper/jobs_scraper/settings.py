# Scrapy settings for jobs_scraper project

BOT_NAME = "jobs_scraper"
SPIDER_MODULES = ["jobs_scraper.spiders"]
NEWSPIDER_MODULE = "jobs_scraper.spiders"

# User-Agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0"
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.9"
# USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Concurrent Requests
CONCURRENT_REQUESTS = 6

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Download settings
# DOWNLOAD_DELAY = 1
# DOWNLOAD_TIMEOUT = 60
RANDOMIZE_DOWNLOAD_DELAY = True

# Cookies
COOKIES_ENABLED = False

# Retry policies
RETRY_ENABLED = True
RETRY_TIMES = 3  # Retry failed requests 3 times
# RETRY_HTTP_CODES = [500, 400, 429]
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 429]

# RETRY_PRIORITY_ADJUST = -1

# AutoThrottle extension
# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_START_DELAY = 1 # 5
# AUTOTHROTTLE_MAX_DELAY = 60
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# AUTOTHROTTLE_DEBUG = False


# ROTATING_PROXY_LIST_PATH = "/home/mohammed/Projects/vscode/s3/jobs-scraper/proxy_list1.txt"

DOWNLOADER_MIDDLEWARES = {
    # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

ITEM_PIPELINES = {
    'jobs_scraper.cleaningpipline.JobPreprocessingPipeline': 250,
    'jobs_scraper.pipelines.JobsScraperPipeline': 300,

}

# MYSQL_HOST = '127.0.0.1:33061'  # Replace with your MySQL host
MYSQL_HOST = '127.0.0.1'  # Replace with your MySQL host
MYSQL_USER = 'username'  # Replace with your MySQL username
MYSQL_PASSWORD = 'password'  # Replace with your MySQL password
MYSQL_DB = 'db_name'  # Replace with your MySQL database name

# Deprecated settings
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


# Spider configuration
SPIDER_PAUSED = False

# KEYWORDS = "Machine Learning Engineer, Artificial Intelligence Engineer, Computer Vision Engineer, Data Scientist, Data Analyst, Data Engineer, Cloud Engineer, Software Developer, Web Developer, Computer Systems Analyst, Database Administrator, Information Security Analyst, Network Administrator"
# LOCATIONS = "Morocco,Canada,France,United Kingdom,United States,China,united arab emirates,Qatar,Japan,belgium,Germany"

KEYWORDS = "Network Administrator, Information Security Analyst, Database Administrator, Computer Systems Analyst, Web Developer, Software Developer, Cloud Engineer, Data Engineer, Data Analyst, Data Scientist, Computer Vision Engineer, Artificial Intelligence Engineer, Machine Learning Engineer"
LOCATIONS = "Germany,belgium,Japan,Qatar,united arab emirates,China,United States,United Kingdom,France,Canada,Morocco"

# KEYWORDS = "Data Engineer"
# LOCATIONS = "United States"
PAST_DAYS = 1

# KEYWORDS = "Data Scientist"
# LOCATIONS = "Morocco"
# PAST_DAYS = 15

HTTPERROR_ALLOWED_CODES = [999]  # Allow handling of status 999

LOG_LEVEL = 'INFO'  # or 'WARNING' if you want to suppress more messages
