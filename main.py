from bot.actions import BotFreelancerActions
from bot.config import DriverActions

def main():
    # Inicializa el controlador
    skills = []
    links = []
    categories = []
    print("\n------------------------------------------------------------")
    print("\nFreelancer Auto-Apply Bot")
    print("\n   By @Batheria")
    print("\nVersion 1.0")
    print("\nPlease give me a star in the repository")
    print("")
    print("\n------------------------------------------------------------")
    print("\n\nInserts your skills, one by one ...")
    while True:
        skill = input("Insert your skill, for finish insert 'q' ... :")
        if skill == 'q':
            skills_prompt = " ".join(skills)
            break
        skills.append(skill)
        
        print("\n\nSkills Choosed: ")
        for sk in skills: 
            print(' * ',sk)

    
    print('\n\n *Option 1: Enter categories of freelance jobs, then the URLS of jobs from these categories will be scraped... ')
    print(' *Option 2: Enter the job URLs, one by one... ')
    print(' *Option q: Close... ')
    choice = input("\n\nOption: ")

    if choice == "1":
        while True:
            category = input("\nEnter a job category or q for finish: ")
            if 'q' in category:
                instance_driver = DriverActions()
                driver = instance_driver.init_driver()
                print('Log in in your Freelancer Account, and press Enter for continue...')
                input()
                for category in categories:
                    query_category = category.replace(' ', '%20')
                    driver.get(f'https://www.freelancer.com.ar/search/projects?q={query_category}')
                    projects_urls = BotFreelancerActions.scrape_projects(driver)
                    for project_url in projects_urls:
                        driver.get(project_url)
                        BotFreelancerActions.apply_to_a_job(driver, skills_prompt)
                break
            categories.append(category)
            print(f"Category '{category}' add.")

    elif choice == "2":
        while True:
            link = input("Enter the job url, for finish enter 'q': ")
            if 'q' == link:
                instance_driver = DriverActions()
                driver = instance_driver.init_driver()
                print('Log in in your Freelancer Account, and press Enter for continue...')
                input()
                for url in links:
                    driver.get(url)
                    BotFreelancerActions.apply_to_a_job(driver, skills_prompt)
                break

            if not 'www.freelancer.com' in link:
                print("Please enter a Freelancer url ...")
            else:
                links.append(link)
                print(f"URL '{link}' add.")

    elif choice == "q":
        exit
    else:
        print("Invalid option. Please choose 1, 2 or 'q'.")

if __name__ == "__main__":
    main()