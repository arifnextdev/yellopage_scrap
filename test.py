

# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pandas as pd
# import time
# import re

# class ZabaPhoneScraper:
#     def __init__(self, input_csv, output_csv):
#         self.input_csv = input_csv
#         self.output_csv = output_csv
#         self.driver = self.configure_driver()
#         self.wait = WebDriverWait(self.driver, 20)
#         self.base_url = "https://www.zabasearch.com/phone/"
#         self.first_visit = True

#     def configure_driver(self):
#         options = uc.ChromeOptions()
#         options.add_argument("--window-size=1200,900")
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         return uc.Chrome(options=options, headless=False)

#     def clean_phone(self, phone):
#         return re.sub(r'[^0-9]', '', phone)[-10:]

#     def agree_to_checkbox(self):
#         try:
#             print("Waiting for verification checkbox...")
#             checkbox = self.wait.until(EC.element_to_be_clickable((By.ID, "checkbox")))
#             ActionChains(self.driver).move_to_element(checkbox).click().perform()
#             print("Checkbox clicked!")
#             time.sleep(3)
#         except Exception as e:
#             print("No checkbox found or already passed:", str(e))

#     def visit_and_scrape(self, phone):
#         try:
#             number = self.clean_phone(phone)
#             url = self.base_url + number
#             print(f"Visiting {url}")
#             self.driver.get(url)

#             # Only on first visit
#             if self.first_visit:
#                 self.agree_to_checkbox()
#                 self.first_visit = False

#             # Check for 404 or "NOT FOUND"
#             time.sleep(2)
#             body_text = self.driver.page_source
#             if "Status: 404, NOT FOUND" in body_text or "No results found" in body_text:
#                 print("❌ Number not found.")
#                 return {
#                     "phone": phone,
#                     "name": "N/A",
#                     "location": "N/A",
#                     "status": "Not Found"
#                 }

#             # Wait for result if available
#             try:
#                 self.wait.until(EC.presence_of_element_located((By.ID, "result-top-content")))
#                 name = self.driver.find_element(By.CSS_SELECTOR, "#result-top-content h3").text.strip()

#                 try:
#                     location = self.driver.find_element(By.XPATH, "//th[contains(text(), 'Location')]/following-sibling::td").text.strip()
#                     carrier = self.driver.find_element(By.XPATH, "//th[contains(text(), 'Carrier')]/following-sibling::td").text.strip()
#                 except:
#                     location = "N/A"

#                 return {
#                     "phone": phone,
#                     "name": name,
#                     "location": location,
#                     "carrier": carrier,
#                     "status": "Success"
#                 }

#             except:
#                 return {
#                     "phone": phone,
#                     "name": "N/A",
#                     "location": "N/A",
#                     "carrier": "N/A",
#                     "status": "No result section"
#                 }

#         except Exception as e:
#             print(f"Error for phone {phone}: {e}")
#             return {
#                 "phone": phone,
#                 "name": "Error",
#                 "location": "Error",
#                 "carrier": "Error",
#                 "status": str(e)
#             }

#     def process(self):
#         df = pd.read_csv(self.input_csv)
#         results = []

#         for _, row in df.iterrows():
#             phone = str(row['phone']).strip()
#             print(f"\n📞 Checking number: {phone}")
#             result = self.visit_and_scrape(phone)
#             results.append(result)

#             # Save progress every request
#             pd.DataFrame(results).to_csv(self.output_csv, index=False)

#             time.sleep(5)  # Delay to avoid rate limit

#         self.driver.quit()
#         print(f"\n✅ Done! Results saved to {self.output_csv}")


# if __name__ == "__main__":
#     scraper = ZabaPhoneScraper("data.csv", "output_results.csv")
#     scraper.process()


import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re


class ZabaPhoneScraper:
    def __init__(self, input_csv, output_csv):
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.driver = self.configure_driver()
        self.wait = WebDriverWait(self.driver, 20)
        self.base_url = "https://www.zabasearch.com/phone/"
        self.first_visit = True

    def configure_driver(self):
        options = uc.ChromeOptions()
        options.headless = False  # Explicitly show browser
        options.add_argument("--window-size=1200,900")
        options.add_argument('--disable-blink-features=AutomationControlled')
        return uc.Chrome(options=options)

    def clean_phone(self, phone):
        return re.sub(r'\D', '', phone)[-10:]

    def agree_to_checkbox(self):
        try:
            print("🔒 Waiting for checkbox...")
            checkbox = self.wait.until(EC.element_to_be_clickable((By.ID, "checkbox")))
            ActionChains(self.driver).move_to_element(checkbox).click().perform()
            print("✅ Checkbox clicked!")
            time.sleep(3)
        except Exception as e:
            print("⏭️ Checkbox skipped:", str(e))

    def get_table_info(self, label):
        try:
            return self.driver.find_element(
                By.XPATH, f"//th[contains(text(), '{label}')]/following-sibling::td"
            ).text.strip()
        except:
            return "N/A"

    def visit_and_scrape(self, phone):
        number = self.clean_phone(phone)
        url = self.base_url + number
        print(f"🌐 Visiting: {url}")
        self.driver.get(url)

        if self.first_visit:
            self.agree_to_checkbox()
            self.first_visit = False

        time.sleep(2)
        if "Status: 404, NOT FOUND" in self.driver.page_source or "No results found" in self.driver.page_source:
            print("❌ Not found.")
            return {
                "phone": phone,
                "name": "N/A",
                "location": "N/A",
                "carrier": "N/A",
                "status": "Not Found"
            }

        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "result-top-content")))
            name = self.driver.find_element(By.CSS_SELECTOR, "#result-top-content h3").text.strip()
        except:
            name = "N/A"

        # Get additional info
        carrier = self.get_table_info("Carrier")
        location = self.get_table_info("Location")

        return {
            "phone": phone,
            "name": name,
            "location": location,
            "carrier": carrier,
            "status": "Success" if name != "N/A" else "No Name"
        }

    def process(self):
        df = pd.read_csv(self.input_csv)
        results = []

        for _, row in df.iterrows():
            phone = str(row['phone']).strip()
            print(f"\n📞 Processing: {phone}")
            result = self.visit_and_scrape(phone)
            results.append(result)

            # Save after each attempt
            pd.DataFrame(results).to_csv(self.output_csv, index=False)
            time.sleep(2)

        self.driver.quit()
        print(f"\n✅ Done! Data saved to ➤ {self.output_csv}")


if __name__ == "__main__":
    scraper = ZabaPhoneScraper("data.csv", "output_results.csv")
    scraper.process()
