import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from datetime import datetime

class DataDrivenTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://practicetestautomation.com/practice-test-login/")  
        self.wait = WebDriverWait(self.driver, 10)

    def test_login_csv(self):
        driver = self.driver
        wait = self.wait

        results = []  # to store results

        # Read test data from CSV
        with open("testdata.csv", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                username = row['username']
                password = row['password']

                # Wait for username field
                user_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
                pass_field = wait.until(EC.presence_of_element_located((By.ID, "password")))
                login_btn = wait.until(EC.element_to_be_clickable((By.ID, "submit")))

                # Enter credentials
                user_field.clear()
                user_field.send_keys(username)

                pass_field.clear()
                pass_field.send_keys(password)

                login_btn.click()
                time.sleep(2)

                # Check success or failure
                if "Logged In Successfully" in driver.page_source:
                    print(f"✅ Login successful with: {username}")
                    results.append({"username": username, "password": password, "result": "Pass"})
                    driver.find_element(By.LINK_TEXT, "Log out").click()
                else:
                    print(f"❌ Login failed with: {username}")
                    results.append({"username": username, "password": password, "result": "Fail"})

                # Back to login page
                driver.get("https://practicetestautomation.com/practice-test-login/")

        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"results_{timestamp}.csv"

        # Write results into CSV with timestamp
        with open(filename, "w", newline="") as f:
            fieldnames = ["username", "password", "result"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

        print(f"📁 Test results saved in: {filename}")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
