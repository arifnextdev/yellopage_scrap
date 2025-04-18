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
#         options.headless = True  # Faster without UI
#         options.add_argument("--window-size=1200,900")
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         return uc.Chrome(options=options)

#     def wait_for_page(self):
#         try:
#             self.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
#             if "Status: 404, NOT FOUND" in self.driver.page_source or "No results found" in self.driver.page_source:
#                 return False
#             return True
#         except:
#             return False


#     def clean_phone(self, phone):
#         return re.sub(r'\D', '', phone)[-10:]

#     def agree_to_checkbox(self):
#         try:
#             print("🔒 Waiting for modal with checkbox...")
#             self.wait.until(EC.presence_of_element_located((By.ID, "checkbox")))
#             checkbox = self.driver.find_element(By.ID, "checkbox")
#             self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
#             time.sleep(1)
#             self.driver.execute_script("arguments[0].click();", checkbox)
#             print("✅ Checkbox clicked!")
#         except Exception as e:
#             print("⏭️ Checkbox skipped or modal issue:", str(e))
#             self.driver.save_screenshot("checkbox_fail.png")
#             with open("debug.html", "w", encoding="utf-8") as f:
#                 f.write(self.driver.page_source)


#     def get_table_info(self, label):
#         try:
#             return self.driver.find_element(
#                 By.XPATH, f"//th[contains(text(), '{label}')]/following-sibling::td"
#             ).text.strip()
#         except:
#             return "N/A"

#     def visit_and_scrape(self, phone, conpany_name, address, website, category):
#         number = self.clean_phone(phone)
#         url = self.base_url + number
#         print(f"🌐 Visiting: {url}")
#         self.driver.get(url)

#         # Wait for full page load
#         if not self.wait_for_page():
#             print("❌ Page load failed or not found.")
#             return {
#                 "name": "N/A",
#                 "phone": phone,
#                 "location": "N/A",
#                 "carrier": "N/A",
#                 "company_name": conpany_name,
#                 "address": address,
#                 "website": website,
#                 "category": category,
#                 "status": "Not Found"
#             }

#         # Checkbox handling
#         if self.first_visit:
#             self.agree_to_checkbox()
#             self.first_visit = False

#         # Continue only if results exist
#         if "Status: 404, NOT FOUND" in self.driver.page_source or "No results found" in self.driver.page_source:
#             print("❌ Not found.")
#             return {
#                 "name": "N/A",
#                 "phone": phone,
#                 "location": "N/A",
#                 "carrier": "N/A",
#                 "company_name": conpany_name,
#                 "address": address,
#                 "website": website,
#                 "category": category,
#                 "status": "Not Found"
#             }

#         try:
#             self.wait.until(EC.presence_of_element_located((By.ID, "result-top-content")))
#             name = self.driver.find_element(By.CSS_SELECTOR, "#result-top-content h3").text.strip()
#         except:
#             name = "N/A"

#         carrier = self.get_table_info("Carrier")
#         location = self.get_table_info("Location")

#         return {
#             "name": name,
#             "phone": phone,
#             "location": location,
#             "carrier": carrier,
#             "company_name": conpany_name,
#             "address": address,
#             "website": website,
#             "category": category,
#             "status": "Success" if name != "N/A" else "No Name"
#         }


#     def process(self):
#         df = pd.read_csv(self.input_csv)
#         results = []

#         for _, row in df.iterrows():
#             phone = str(row['phone']).strip()
#             company_name = str(row['company_name']).strip()
#             address = str(row['address']).strip()
#             website = str(row['website']).strip()
#             category = str(row['category']).strip()

#             print(f"\n📞 Processing: {phone}")
#             result = self.visit_and_scrape(phone, company_name, address, website, category)
#             print(f"✅ Result: {result}")
#             results.append(result)
#             pd.DataFrame(results).to_csv(self.output_csv, index=False)

#         # Write to CSV once at the end
#         self.driver.quit()
#         print(f"\n✅ Done! Data saved to ➤ {self.output_csv}")


# if __name__ == "__main__":
#     scraper = ZabaPhoneScraper("CA.csv", "TEST_CA_output_results.csv")
#     scraper.process()







# import undetected_chromedriver as uc
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pandas as pd
# import time
# import re
# import sys
# from selenium.common.exceptions import WebDriverException


# class ZabaPhoneScraper:
#     def __init__(self, input_csv, output_csv):
#         self.input_csv = input_csv
#         self.output_csv = output_csv
#         self.driver = None
#         self.initialize_driver()
#         self.wait = WebDriverWait(self.driver, 20)
#         self.base_url = "https://www.zabasearch.com/phone/"
#         self.first_visit = True

#     def initialize_driver(self, max_attempts=3):
#         for attempt in range(max_attempts):
#             try:
#                 self.driver = self.configure_driver()
#                 return
#             except Exception as e:
#                 print(f"Attempt {attempt + 1} failed: {str(e)}")
#                 if attempt == max_attempts - 1:
#                     raise
#                 time.sleep(2)
#                 self.cleanup_resources()

#     def cleanup_resources(self):
#         if self.driver:
#             try:
#                 self.driver.quit()
#             except:
#                 pass
#             self.driver = None

#     def configure_driver(self):
#     # Create fresh options object for each attempt
#         options = uc.ChromeOptions()
        
#         # Basic options
#         options.add_argument("--window-size=1200,900")
#         options.add_argument('--disable-blink-features=AutomationControlled')
#         options.add_argument("--disable-extensions")
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-dev-shm-usage")
        
#         # User agent and profile
#         options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
#         options.add_argument("--user-data-dir=./chrome_profile")
        
#         # FIXED: Corrected the typo in "excludeSwitches"
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         options.add_experimental_option("useAutomationExtension", False)
        
#         try:
#             # Try with default settings
#             return uc.Chrome(
#                 options=options,
#                 headless=False,
#                 use_subprocess=True
#             )
#         except Exception as e:
#             print(f"Standard initialization failed: {e}")
#             print("Trying alternative approach...")
            
#             # Create NEW options object for the alternative attempt
#             new_options = uc.ChromeOptions()
#             new_options.add_argument("--no-sandbox")
#             new_options.add_argument("--disable-dev-shm-usage")
            
#             return uc.Chrome(
#                 options=new_options,
#                 version_main=114,  # Adjust to your Chrome version
#                 driver_executable_path=None,
#                 browser_executable_path=None
#             )

#     def wait_for_page(self):
#         try:
#             self.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
#             if "Status: 404, NOT FOUND" in self.driver.page_source or "No results found" in self.driver.page_source:
#                 return False
#             return True
#         except:
#             return False

#     def clean_phone(self, phone):
#         return re.sub(r'\D', '', phone)[-10:]

#     def handle_captcha(self):
#         if "Verify you are human" in self.driver.page_source:
#             print("⚠️ CAPTCHA Detected! Please solve it manually in browser.")
#             self.driver.save_screenshot("captcha_screen.png")
#             input("✅ Press Enter after solving CAPTCHA...")
#             return True
#         return False

#     def agree_to_checkbox(self):
#         try:
#             print("🔒 Waiting for modal with checkbox...")
#             checkbox = self.wait.until(EC.element_to_be_clickable((By.ID, "checkbox")))
#             self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
#             time.sleep(1)
#             self.driver.execute_script("arguments[0].click();", checkbox)
#             print("✅ Checkbox clicked!")
#             return True
#         except Exception as e:
#             print("⏭️ Checkbox not found or not clickable:", str(e))
#             return False

#     def get_table_info(self, label):
#         try:
#             return self.driver.find_element(
#                 By.XPATH, f"//th[contains(text(), '{label}')]/following-sibling::td"
#             ).text.strip()
#         except:
#             return "N/A"

#     def scrape_page(self):
#         result = {
#             "name": "N/A",
#             "phone": "N/A",
#             "location": "N/A",
#             "carrier": "N/A",
#             "company_name": "N/A",
#             "address": "N/A",
#             "website": "N/A",
#             "category": "N/A",
#             "status": "Failed"
#         }
        
#         try:
#             self.wait.until(EC.presence_of_element_located((By.ID, "result-top-content")))
#             result['name'] = self.driver.find_element(By.CSS_SELECTOR, "#result-top-content h3").text.strip()
#             result['carrier'] = self.get_table_info("Carrier")
#             result['location'] = self.get_table_info("Location")
#             result['status'] = "Success"
#         except Exception as e:
#             print(f"Scraping error: {str(e)}")
#             result['status'] = "Scraping Failed"
        
#         return result

#     def visit_and_scrape(self, phone, company_name, address, website, category):
#         number = self.clean_phone(phone)
#         if not number:
#             print("❌ Invalid phone number format")
#             return {
#                 "name": "N/A",
#                 "phone": phone,
#                 "location": "N/A",
#                 "carrier": "N/A",
#                 "company_name": company_name,
#                 "address": address,
#                 "website": website,
#                 "category": category,
#                 "status": "Invalid Phone"
#             }

#         url = self.base_url + number
#         print(f"🌐 Visiting: {url}")
        
#         try:
#             self.driver.get(url)
            
#             # Handle CAPTCHA if present
#             if self.handle_captcha():
#                 # After CAPTCHA, reload the page
#                 self.driver.get(url)
            
#             # Wait for page load
#             if not self.wait_for_page():
#                 print("❌ Page load failed or not found.")
#                 return {
#                     "name": "N/A",
#                     "phone": phone,
#                     "location": "N/A",
#                     "carrier": "N/A",
#                     "company_name": company_name,
#                     "address": address,
#                     "website": website,
#                     "category": category,
#                     "status": "Not Found"
#                 }

#             # Handle first-visit checkbox
#             if self.first_visit:
#                 if self.agree_to_checkbox():
#                     self.first_visit = False

#             # Check for 404 or no results
#             if "Status: 404, NOT FOUND" in self.driver.page_source or "No results found" in self.driver.page_source:
#                 print("❌ Not found.")
#                 return {
#                     "name": "N/A",
#                     "phone": phone,
#                     "location": "N/A",
#                     "carrier": "N/A",
#                     "company_name": company_name,
#                     "address": address,
#                     "website": website,
#                     "category": category,
#                     "status": "Not Found"
#                 }

#             # Scrape the page data
#             result = self.scrape_page()
#             result.update({
#                 "phone": phone,
#                 "company_name": company_name,
#                 "address": address,
#                 "website": website,
#                 "category": category
#             })
            
#             return result
            
#         except Exception as e:
#             print(f"❌ Error during scraping: {str(e)}")
#             self.driver.save_screenshot("error_screenshot.png")
#             return {
#                 "name": "N/A",
#                 "phone": phone,
#                 "location": "N/A",
#                 "carrier": "N/A",
#                 "company_name": company_name,
#                 "address": address,
#                 "website": website,
#                 "category": category,
#                 "status": f"Error: {str(e)}"
#             }

#     def process(self):
#         try:
#             df = pd.read_csv(self.input_csv)
#             results = []
            
#             for index, row in df.iterrows():
#                 phone = str(row['phone']).strip()
#                 company_name = str(row.get('company_name', '')).strip()
#                 address = str(row.get('address', '')).strip()
#                 website = str(row.get('website', '')).strip()
#                 category = str(row.get('category', '')).strip()

#                 print(f"\n📞 Processing {index + 1}/{len(df)}: {phone}")
#                 result = self.visit_and_scrape(phone, company_name, address, website, category)
#                 print(f"✅ Result: {result['status']} - Name: {result['name']}")
#                 results.append(result)
                
#                 # Save progress after each record
#                 pd.DataFrame(results).to_csv(self.output_csv, index=False)
                
#                 # Add delay between requests
#                 time.sleep(2)

#         except Exception as e:
#             print(f"❌ Fatal error in processing: {str(e)}")
#             raise
#         finally:
#             self.cleanup_resources()
#             print(f"\n✅ Done! Data saved to ➤ {self.output_csv}")


# if __name__ == "__main__":
#     scraper = ZabaPhoneScraper("input.csv", "output_results.csv")
#     scraper.process()


import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import re
import sys
import random
from selenium.common.exceptions import (WebDriverException, 
                                      TimeoutException, 
                                      NoSuchElementException)


class ZabaPhoneScraper:
    def __init__(self, input_csv, output_csv):
        self.input_csv = input_csv
        self.output_csv = output_csv
        self.driver = None
        self.initialize_driver()
        self.wait = WebDriverWait(self.driver, 15)  # Reduced from 20
        self.base_url = "https://www.zabasearch.com/phone/"
        self.first_visit = True
        self.captcha_solved = False
        self.request_delay = (2, 5)  # Random delay between requests

    def initialize_driver(self, max_attempts=3):
        for attempt in range(max_attempts):
            try:
                self.driver = self.configure_driver()
                # Set implicit wait to avoid unnecessary delays
                self.driver.implicitly_wait(5)  
                return
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                self.cleanup_resources()
                if attempt == max_attempts - 1:
                    raise
                time.sleep(3)  # Increased sleep between attempts

    def configure_driver(self):
        options = uc.ChromeOptions()
        
        # Optimized options
        options.add_argument("--window-size=1200,900")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-infobars")
        
        # User agent and profile
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        options.add_argument("--user-data-dir=./chrome_profile")
        
        # Correct experimental options
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        
        try:
            return uc.Chrome(
                options=options,
                headless=False,
                use_subprocess=True,
                version_main=114  # Set to your Chrome version
            )
        except Exception as e:
            print(f"Standard initialization failed: {e}")
            print("Trying with minimal options...")
            
            # Fallback with minimal options
            minimal_options = uc.ChromeOptions()
            minimal_options.add_argument("--no-sandbox")
            minimal_options.add_argument("--disable-dev-shm-usage")
            
            return uc.Chrome(
                options=minimal_options,
                headless=False
            )

    def random_delay(self):
        """Add random delay between requests to appear more human-like"""
        delay = random.uniform(*self.request_delay)
        time.sleep(delay)

    def wait_for_page(self, timeout=15):
        """More efficient page load waiting"""
        try:
            self.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
            
            # Quick checks for common failure indicators
            page_text = self.driver.page_source
            if any(msg in page_text for msg in ["Status: 404", "No results found", "Not Found"]):
                return False
            return True
        except TimeoutException:
            return False

    def clean_phone(self, phone):
        """More robust phone number cleaning"""
        digits = re.sub(r'\D', '', str(phone))
        return digits[-10:] if len(digits) >= 10 else None

    def handle_captcha(self):
        """Improved CAPTCHA handling with timeout"""
        if self.captcha_solved:
            return False
            
        try:
            # Wait briefly for CAPTCHA to appear
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Verify you are human')]"))
            )
            print("⚠️ CAPTCHA Detected! Please solve it manually in browser.")
            self.driver.save_screenshot("captcha_screen.png")
            input("✅ Press Enter after solving CAPTCHA...")
            self.captcha_solved = True
            return True
        except TimeoutException:
            return False

    def agree_to_checkbox(self):
        """More reliable checkbox handling"""
        if not self.first_visit:
            return False
            
        try:
            print("🔒 Checking for consent modal...")
            checkbox = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "checkbox"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
            time.sleep(0.5)  # Reduced from 1 second
            checkbox.click()
            print("✅ Consent given!")
            self.first_visit = False
            return True
        except Exception as e:
            print(f"⏭️ Checkbox not required or not found: {str(e)}")
            return False

    def get_table_info(self, label):
        """More efficient element finding with fallback"""
        try:
            return self.driver.find_element(
                By.XPATH, f"//th[contains(., '{label}')]/following-sibling::td"
            ).text.strip() or "N/A"
        except NoSuchElementException:
            return "N/A"

    def scrape_page(self):
        """Optimized scraping with combined waits"""
        result = {
            "name": "N/A",
            "phone": "N/A",
            "location": "N/A",
            "carrier": "N/A",
            "status": "Failed"
        }
        
        try:
            # Combined wait for multiple elements
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#result-top-content")))
            
            # Get name if available
            try:
                result['name'] = self.driver.find_element(
                    By.CSS_SELECTOR, "#result-top-content h3"
                ).text.strip()
            except NoSuchElementException:
                pass
                
            # Get table info
            result['carrier'] = self.get_table_info("Carrier")
            result['location'] = self.get_table_info("Location")
            
            result['status'] = "Success" if result['name'] != "N/A" else "No Name"
        except TimeoutException:
            result['status'] = "Timeout"
        except Exception as e:
            print(f"Scraping error: {str(e)}")
            result['status'] = f"Error: {str(e)}"
        
        return result

    def visit_and_scrape(self, phone, company_name, address, website, category):
        """Optimized visit and scrape with better error recovery"""
        number = self.clean_phone(phone)
        if not number:
            print("❌ Invalid phone number format")
            return self.create_result(phone, company_name, address, website, category, "Invalid Phone")
        
        url = self.base_url + number
        print(f"🌐 Visiting: {url}")
        
        try:
            # First attempt
            self.driver.get(url)
            
            # Handle CAPTCHA only once per session
            if not self.captcha_solved and self.handle_captcha():
                self.driver.get(url)  # Reload after CAPTCHA
                
            # Check page load
            if not self.wait_for_page():
                return self.create_result(phone, company_name, address, website, category, "Page Load Failed")
                
            # Handle first-visit checkbox
            self.agree_to_checkbox()
            
            # Check for no results
            if any(msg in self.driver.page_source for msg in ["Status: 404", "No results found"]):
                return self.create_result(phone, company_name, address, website, category, "Not Found")
                
            # Scrape data
            result = self.scrape_page()
            result.update({
                "phone": phone,
                "company_name": company_name,
                "address": address,
                "website": website,
                "category": category
            })
            
            return result
            
        except Exception as e:
            print(f"❌ Error during scraping: {str(e)}")
            self.driver.save_screenshot(f"error_{number}.png")
            return self.create_result(phone, company_name, address, website, category, f"Error: {str(e)}")

    def create_result(self, phone, company_name, address, website, category, status):
        """Helper to create consistent result dict"""
        return {
            "name": "N/A",
            "phone": phone,
            "location": "N/A",
            "carrier": "N/A",
            "company_name": company_name,
            "address": address,
            "website": website,
            "category": category,
            "status": status
        }

    def process(self):
        """Optimized processing with batch saving"""
        try:
            df = pd.read_csv(self.input_csv)
            results = []
            batch_size = 10  # Save every 10 records
            
            for index, row in df.iterrows():
                if index > 0:
                    self.random_delay()  # Add delay between requests
                
                phone = str(row['phone']).strip()
                company_name = str(row.get('company_name', '')).strip()
                address = str(row.get('address', '')).strip()
                website = str(row.get('website', '')).strip()
                category = str(row.get('category', '')).strip()

                print(f"\n📞 Processing {index + 1}/{len(df)}: {phone}")
                result = self.visit_and_scrape(phone, company_name, address, website, category)
                print(f"✅ Status: {result['status']} | Name: {result['name']}")
                results.append(result)
                
                # Save progress in batches
                if (index + 1) % batch_size == 0:
                    pd.DataFrame(results).to_csv(self.output_csv, index=False)
                    print(f"💾 Saved batch up to record {index + 1}")

            # Final save
            pd.DataFrame(results).to_csv(self.output_csv, index=False)

        except Exception as e:
            print(f"❌ Fatal error in processing: {str(e)}")
            raise
        finally:
            self.cleanup_resources()
            print(f"\n✅ Done! Data saved to ➤ {self.output_csv}")

    def cleanup_resources(self):
        """More thorough cleanup"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None


if __name__ == "__main__":
    try:
        if len(sys.argv) > 2:
            input_file = sys.argv[1]
            output_file = sys.argv[2]
        else:
            input_file = "input.csv"
            output_file = "output.csv"
            
        print(f"Starting scraper with:\nInput: {input_file}\nOutput: {output_file}")
        
        scraper = ZabaPhoneScraper(input_file, output_file)
        scraper.process()
        
    except Exception as e:
        print(f"❌ Main execution error: {str(e)}")
        sys.exit(1)