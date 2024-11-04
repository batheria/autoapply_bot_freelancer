import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from bot.openai_helper import OpenaiService

class ActionsForScript:
    def __init__(self):
        pass

    ## PARAMETERS FOR DISCOUNT, IN DEFAULT IS 0.05
    def calcular_descuento_10_por_ciento(total):
        total = int(float(total))  
        descuento = total * 0.05 ## THIS IS THE DISCOUNT
        total_con_descuento = total - descuento
        return str(total_con_descuento)
    
    def send_text(texto, text_area):
        for letra in texto:
            text_area.send_keys(letra)
            time.sleep(0.0712) 

    def send_price(texto, price_area_text):
        price_area_text.send_keys(Keys.CONTROL + "a")
        price_area_text.send_keys(Keys.DELETE)
        for letra in texto:
            price_area_text.send_keys(letra)
            time.sleep(0.0712)

    def job_browser(driver):
        browser_btn = driver.find_element(By.TAG_NAME, '/html/body/app-root/app-logged-in-shell/div/div[1]/div/app-navigation/app-navigation-primary/div/fl-container/fl-callout[1]/fl-callout-trigger/fl-button')
        action = ActionChains(driver)
        action.move_to_element(browser_btn).perform()


class BotFreelancerActions(ActionsForScript):
    def __init__(self):
        pass

    def scrape_projects(driver):
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
    
    def apply_to_a_job(driver, skills_prompt):
        try:
            time.sleep(5)
            send_place = driver.find_element(By.CLASS_NAME, 'BidFormBtn')
            send_button = send_place.find_element(By.CLASS_NAME, 'BidFormBtn')
            time.sleep(5)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            price_area_text = driver.find_element(By.XPATH, '//*[@id="bidAmountInput"]')
            price = price_area_text.get_attribute('value')
            price = ActionsForScript.calcular_descuento_10_por_ciento(price)
            print(price)
            ActionsForScript.send_price(price, price_area_text)
            time.sleep(10)
            job_description = soup.find('div', {'class':'CardContainer'}).text
            text_area = driver.find_elements(By.TAG_NAME, 'textarea')
            text_area = text_area[-1]
            texto = OpenaiService.job_proposal(job_description,skills_prompt)
            ActionsForScript.send_text(texto, text_area)
            time.sleep(2)
            send_button.click()
            time.sleep(5)
            current_url = driver.current_url
            print(current_url)
            time.sleep(5)
        except:
            print('No existe el boton de PRECIO')
            