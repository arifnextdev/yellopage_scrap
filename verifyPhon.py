# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
# import time

# class PhoneInfoFetcher:
#     def __init__(self, input_csv, output_csv):
#         self.input_csv = input_csv
#         self.output_csv = output_csv
#         self.base_url = "https://www.zabasearch.com/phone/"

#     def fetch_info(self, phone):
#         try:
#             url = f"{self.base_url}{phone}"
#             headers = {
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#             }
#             response = requests.get(url, headers=headers)
#             soup = BeautifulSoup(response.text, 'html.parser')

#             #Name Location: #phone-number-result #result-top #result-top-content h3

#             # Parse name
#             name_tag = soup.find("h3")
#             print(soup.get_text(strip=True))
#             name = name_tag.get_text(strip=True) if name_tag else "N/A"

#             # Parse other info (like location)
#             location = soup.find("div", class_="person-location")
#             location_text = location.get_text(strip=True) if location else "N/A"

#             # Note: Zabasearch doesn’t provide carrier or birth year directly unless linked to a deeper lookup.

#             return {
#                 "phone": phone,
#                 "name": name,
#                 "location": location_text,
#                 "carrier": "Not available",
#                 "birth_year": "Not available"
#             }

#         except Exception as e:
#             print(f"Error fetching {phone}: {e}")
#             return {
#                 "phone": phone,
#                 "name": "Error",
#                 "location": "Error",
#                 "carrier": "Error",
#                 "birth_year": "Error"
#             }

#     def process(self):
#         df = pd.read_csv(self.input_csv)
#         results = []

#         for index, row in df.iterrows():
#             phone = str(row['phone'])
#             print(f"Searching for phone: {phone}")
#             data = self.fetch_info(phone)
#             results.append(data)
#             time.sleep(3)  # Respectful delay

#         output_df = pd.DataFrame(results)
#         output_df.to_csv(self.output_csv, index=False)
#         print(f"Saved updated data to {self.output_csv}")

# # Run it
# fetcher = PhoneInfoFetcher("data.csv", "updated_data.csv")
# fetcher.process()



# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pandas as pd
# import time
# import re

# class PhoneInfoFetcher:
#     def __init__(self, input_csv, output_csv):
#         self.input_csv = input_csv
#         self.output_csv = output_csv
#         self.base_url = "https://www.zabasearch.com/phone/"
#         self.driver = self.configure_driver()
#         self.wait = WebDriverWait(self.driver, 15)

#     def configure_driver(self):
#         options = uc.ChromeOptions()
#         options.add_argument("--window-size=1200,900")
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         return uc.Chrome(options=options, headless=False)  # Run in visible mode for debugging

#     def clean_phone(self, phone):
#         """Format phone number to 10 digits only"""
#         return re.sub(r'[^0-9]', '', phone)[-10:]

#     def search_phone(self, phone):
#         try:
#             # 1. Load initial page
#             self.driver.get(self.base_url)
            
#             # 2. Wait for tabs to render
#             self.wait.until(EC.presence_of_element_located((By.ID, "tabs")))
            
#             # 3. Click on Phone tab (tab2)
#             phone_tab = self.wait.until(EC.element_to_be_clickable((By.ID, "tab2")))
#             phone_tab.click()
            
#             # 4. Find search input field
#             search_input = self.wait.until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "form.phone-search.active #phone-submit button.button-search"))
#             )
            
#             # 5. Enter phone number and submit
#             search_input.clear()
#             search_input.send_keys(phone)
#             search_input.submit()
            
#             # 6. Wait for results to load
#             self.wait.until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "#phone-number-result"))
#             )
            
#             # 7. Extract name from result
#             name_element = self.wait.until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "#phone-number-result #result-top #result-top-content h3"))
#             )
#             name = name_element.text.strip()
            
#             # 8. Extract location if available
#             try:
#                 location = self.driver.find_element(
#                     By.CSS_SELECTOR, "#phone-number-result .person-location"
#                 ).text.strip()
#             except:
#                 location = "N/A"
            
#             return {
#                 "phone": phone,
#                 "clean_phone": phone,
#                 "name": name,
#                 "location": location,
#                 "status": "Success"
#             }
            
#         except Exception as e:
#             print(f"Error processing {phone}: {str(e)}")
#             return {
#                 "phone": phone,
#                 "clean_phone": self.clean_phone(phone),
#                 "name": "Error",
#                 "location": "Error",
#                 "status": str(e)
#             }

#     def process(self):
#         df = pd.read_csv(self.input_csv)
#         results = []
        
#         for _, row in df.iterrows():
#             phone = str(row['phone']).strip()
#             print(f"Processing: {phone}")
            
#             result = self.search_phone(phone)
#             results.append(result)
            
#             # Add delay between searches
#             time.sleep(10)
            
#             # Save progress after each search
#             pd.DataFrame(results).to_csv(self.output_csv, index=False)
        
#         self.driver.quit()
#         print(f"Completed! Results saved to {self.output_csv}")

# if __name__ == "__main__":
#     fetcher = PhoneInfoFetcher("data.csv", "output_results.csv")
#     fetcher.process()


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_phone_number(number):
    driver = webdriver.Chrome()
    try:
        driver.get(f"https://www.zabasearch.com/")
        
        # Handle verification
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".verify"))
        )
        checkbox = driver.find_element(By.ID, "checkbox")
        checkbox.click()
        
        # Wait for tabs and click tabs2
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tab2"))
        )
        tab2 = driver.find_element(By.ID, "tab2")
        tab2.click()
        
        # Input phone number and search
        phone_input = driver.find_element(By.CLASS_NAME, "search-phone-number")
        print(f"Searching for: {number}")
        phone_input.clear()
        phone_input.send_keys(number)
        
        submit = driver.find_element(By.ID, "phone-submit")
        submit.click()
        
        # Check for results
        try:
            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".result-top-content"))
            )
            return result.text
        except:
            return "N/A"
            
    finally:
        driver.quit()

numbers = search_phone_number("(813) 915-7457")

print(numbers)

# Example usage with your data.csv
# You would read the numbers from CSV and process them