from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Configuration: LeetCode credentials
accounts = [
    {"email": "your_email2@gmail.com", "password": "your_password2"},
    {"email": "your_email3@gmail.com", "password": "your_password3"},
    {"email": "your_email4@gmail.com", "password": "your_password4"},
    {"email": "your_email4@gmail.com", "password": "your_password4"}
]

# Function to login to LeetCode
def login(driver, email, password):
    driver.get("https://leetcode.com/accounts/login/")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "login")))
    
    email_input = driver.find_element(By.NAME, "login")
    password_input = driver.find_element(By.NAME, "password")
    
    email_input.send_keys(email)
    password_input.send_keys(password)
    
    # Check for iframe (in case of CAPTCHA challenge)
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if len(iframes) > 0:
        driver.switch_to.frame(iframes[0])
    
    # Wait for the login button to be clickable and click it
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary')]"))
    )
    login_button.click()
    
    time.sleep(15)  # Wait for login to complete and manually solve CAPTCHA if required

# Function to get the daily problem link
def get_daily_problem(driver):
    driver.get("https://leetcode.com/problemset/all/")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    try:
        daily_problem = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Daily')]"))
        )
        return daily_problem.get_attribute("href")
    except:
        print("Could not find the daily problem.")
        return None

# Function to get the C++ solution
def get_cpp_solution(driver, problem_url):
    driver.get(problem_url)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    
    try:
        # Check Editorial Section
        editorial_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Editorial"))
        )
        editorial_link.click()
        time.sleep(3)
        cpp_solution = driver.find_element(By.XPATH, "//code[contains(text(), 'cpp')]").text
        return cpp_solution
    except:
        pass  # If no solution in editorial, check the discussion section
    
    try:
        # Check Discussion Section
        solution_tab = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Solution"))
        )
        solution_tab.click()
        time.sleep(3)
        cpp_solution = driver.find_element(By.XPATH, "//code[contains(text(), 'cpp')]").text
        return cpp_solution
    except:
        return "No C++ solution available."

# Main execution loop
def main():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Open in full screen
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(options=options)
    solutions = []
    
    for account in accounts:
        print(f"Logging in with {account['email']}")
        login(driver, account["email"], account["password"])
        problem_link = get_daily_problem(driver)
        
        if problem_link:
            solution = get_cpp_solution(driver, problem_link)
            solutions.append({"account": account["email"], "problem_link": problem_link, "solution": solution})
        
        time.sleep(5)  # Avoid rapid logins
    
    driver.quit()
    
    # Save solutions to a file
    with open("leetcode_solutions.json", "w") as f:
        json.dump(solutions, f, indent=4)
    print("Solutions saved!")

if __name__ == "__main__":
    main()

