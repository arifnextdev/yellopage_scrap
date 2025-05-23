import scrapy
from scrapy.crawler import CrawlerProcess

# Define a base configuration class for reusability
class ScraperConfig:
    def __init__(self, categories, states, output_file='business_data.csv'):
        self.categories = categories  # List of categories (e.g., ['real estate', 'restaurants'])
        self.states = states          # List of states (e.g., ['FL', 'TX'])
        self.output_file = output_file
        self.base_url = 'https://www.yellowpages.com/search?search_terms={category}&geo_location_terms={state}'

    def generate_start_urls(self):
        """Generate start URLs dynamically based on categories and states."""
        urls = []
        for category in self.categories:
            for state in self.states:
                url = self.base_url.format(category=category.replace(' ', '+'), state=state)
                urls.append(url)
        return urls

    def get_settings(self):
        """Return Scrapy settings for the crawler."""
        return {
            'FEED_FORMAT': 'csv',               # Save as CSV
            'FEED_URI': self.output_file,       # Output file name
            'DOWNLOAD_DELAY': 2,                # Polite scraping
            'USER_AGENT': 'BusinessScraper 1.0 (+http://example.com)',  # Custom user agent
            'FEED_EXPORT_ENCODING': 'utf-8',    # Ensure proper encoding
        }

# Define the Spider class
class BusinessSpider(scrapy.Spider):
    name = 'business_spider'

    def __init__(self, config=None, *args, **kwargs):
        super(BusinessSpider, self).__init__(*args, **kwargs)
        if config is None:
            raise ValueError("Config object must be provided")
        self.config = config
        self.start_urls = self.config.generate_start_urls()

    def parse(self, response):
        """Parse business listings from the page."""
        for business in response.css('div.result'):
            yield {
                'company_name': business.css('h2.n a.business-name span::text').get(default='N/A'),
                'phone': business.css('div.phones.phone.primary::text').get(default='N/A'),
                'address': ' '.join(business.css('div.street-address::text').getall()) or 'N/A',
                'website': business.css('a.track-visit-website::attr(href)').get(default='N/A'),
                'page_link': business.css('h2.n a.business-name::attr(href)').get(default='N/A'),
                'category': business.css('div.categories a::text').get(default='N/A'),
            }

        # Handle pagination
        next_page = response.css('a.next.ajax-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

# Main class to orchestrate the scraping process
class BusinessScraper:
    def __init__(self, categories, states, output_file='business_data.csv'):
        self.config = ScraperConfig(categories, states, output_file)

    def run(self):
        """Start the Scrapy crawler process."""
        process = CrawlerProcess(self.config.get_settings())
        process.crawl(BusinessSpider, config=self.config)
        process.start()

        print(f"Business data saved to {self.config.output_file}")