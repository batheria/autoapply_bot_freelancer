import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from bot.openai_helper import OpenaiService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import logging
import requests

logging.basicConfig(
    filename='proposal_sended.log',  # Archivo donde se guardan los resultados
    level=logging.INFO,  # Nivel INFO para registrar datos del scrape
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato de log
)


logging.basicConfig(
    filename='scraping_errors.log',  # Nombre del archivo de log
    level=logging.ERROR,  # Nivel de error para registrar solo errores
    format='%(asctime)s - %(levelname)s - %(message)s'  # Formato de los mensajes
)

class ActionsForScript:
    def __init__(self):
        pass

    ## PARAMETERS FOR DISCOUNT, IN DEFAULT IS 0.05
    def calcular_descuento_10_por_ciento(self, price):
        total = int(float(price))  
        descuento = total * 0.05 ## THIS IS THE DISCOUNT
        total_con_descuento = total - descuento
        return str(total_con_descuento)
        


    def job_browser(self, driver):
        browser_btn = driver.find_element(By.TAG_NAME, '/html/body/app-root/app-logged-in-shell/div/div[1]/div/app-navigation/app-navigation-primary/div/fl-container/fl-callout[1]/fl-callout-trigger/fl-button')
        action = ActionChains(driver)
        action.move_to_element(browser_btn).perform()


class BotFreelancerActions():
    def __init__(self):
        pass

    def scrape_projects(self, driver):
        
        while True:
            time.sleep(10)
            projects_urls = []
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser') 

            projects_a = soup.find_all('a')

            for project_a in projects_a:
                project_a = project_a['href']
                if '/projects/' in project_a:
                    project_url = f'https://www.freelancer.com.ar{project_a}'
                    projects_urls.append(project_url)
                    print(project_url)
            try:
                next_page_button = driver.find_element(By.XPATH, "//button[@aria-label='Next page']")
                next_page_button.click()
                time.sleep(5)
            except:
                break

        return projects_urls
    
    def apply_to_a_job(self, driver, skills_prompt):
        try:
            time.sleep(5)
            instance_actions = ActionsForScript()
            send_place = driver.find_element(By.CLASS_NAME, 'BidFormBtn')
            send_button = send_place.find_element(By.CLASS_NAME, 'BidFormBtn')
            price_area_text = driver.find_element(By.ID, 'bidAmountInput')
            if send_button and price_area_text:
                price = price_area_text.get_attribute('value')
                price = instance_actions.calcular_descuento_10_por_ciento(price)
                price_area_text.send_keys(Keys.CONTROL + "a")
                price_area_text.send_keys(Keys.DELETE)
                for letra in price:
                    price_area_text.send_keys(letra)
                    time.sleep(0.0712)

                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                job_description = soup.find('div', {'class':'CardContainer'}).text
                text_area = driver.find_element(By.ID, 'descriptionTextArea')
                instance_openai_service = OpenaiService()
                
                text_by_ia = instance_openai_service.job_proposal(job_description,skills_prompt)

                for letra in text_by_ia:
                    text_area.send_keys(letra)
                    time.sleep(0.0712) 

                send_button.click()
                time.sleep(5)
                current_url = driver.current_url
                print(current_url)

                logging.info(f"Price: {price}")
                logging.info(f"URL Proposal sent: {current_url}")
                logging.info(f"Project Description: {job_description}")
                logging.info(f"Proposal sent: {text_by_ia}")
                logging.info("------")  # Separador visual para cada propuesta

        except Exception as e:
            # Captura cualquier otro tipo de excepción
            logging.error(f"Error inesperado: {e}")
            print(f"Ocurrió un error inesperado")
