from multiprocessing import Process
from scraper import BusinessScraper, ScraperConfig
import traceback

def run_scraper_task(config):
    try:
        print(f"🚀 Starting scrape: {config.output_file}")
        scraper = BusinessScraper(config)
        scraper.run()
        print(f"✅ Finished: {config.output_file}")
    except Exception as e:
        print(f"❌ Error in {config.output_file}: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    configs = [
        ScraperConfig(categories=["real estate"], states=["FL"], output_file="FL.csv"),
        ScraperConfig(categories=["consulting"], states=["CA"], output_file="CA.csv"),
        ScraperConfig(categories=["tax services"], states=["NY"], output_file="NY.csv"),
    ]

    processes = []
    for config in configs:
        p = Process(target=run_scraper_task, args=(config,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print("🎯 All scrapers finished.")