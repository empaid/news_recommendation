from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest

class ReactAppTestCase(unittest.TestCase):
    base_url = 'http://localhost:3000/React'

    @classmethod
    def setUpClass(cls):
        # Setup Chrome WebDriver
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.driver.get(cls.base_url)

    @classmethod
    def tearDownClass(cls):
        # Close the browser window
        cls.driver.quit()

    def test_homepage_reachable(self):
        # Verify the homepage is reachable
        self.driver.get(self.base_url)
        self.assertTrue("News" in self.driver.title or "Home" in self.driver.title)

    def test_business_page_reachable(self):
        # Verify the business page is reachable
        self.driver.get(f'{self.base_url}/business')
        self.assertTrue("Business" in self.driver.page_source)

    def test_entertainment_page_reachable(self):
        # Verify the entertainment page is reachable
        self.driver.get(f'{self.base_url}/entertainment')
        self.assertTrue("Entertainment" in self.driver.page_source)

    def test_general_page_reachable(self):
        # Verify the general page is reachable
        self.driver.get(f'{self.base_url}/general')
        self.assertTrue("General" in self.driver.page_source)

    def test_health_page_reachable(self):
        # Verify the health page is reachable
        self.driver.get(f'{self.base_url}/health')
        self.assertTrue("Health" in self.driver.page_source)

    def test_science_page_reachable(self):
        # Verify the science page is reachable
        self.driver.get(f'{self.base_url}/science')
        self.assertTrue("Science" in self.driver.page_source)

    def test_sports_page_reachable(self):
        # Verify the sports page is reachable
        self.driver.get(f'{self.base_url}/sports')
        self.assertTrue("Sports" in self.driver.page_source)

    def test_technology_page_reachable(self):
        # Verify the technology page is reachable
        self.driver.get(f'{self.base_url}/technology')
        self.assertTrue("Technology" in self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
