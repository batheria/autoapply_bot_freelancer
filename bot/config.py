from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class DriverActions:
    def __init__(self):
        pass

    def init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.freelancer.com.ar")
        return driver

    def close_driver(self, driver):
        """Cierra el controlador de Selenium."""
        driver.quit()
