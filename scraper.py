import os
import time
import csv
import random
import pyautogui
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Remove the download directory configuration from chrome_options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
# Open the target URL
driver.get('https://apps.usgs.gov/hivis/camera/MO_Missouri_River_at_Hermann')

# Wait for the page to load, use random delay to avoid bot detection
time.sleep(random.uniform(10, 15))

# Define download directory
download_dir = "C://Users//jocel//OneDrive//Desktop//water"


# Step 1: Click the "Open Date Selection Panel" button
try:
    date_selection_panel_button = driver.find_element(By.XPATH, "//span[@aria-label='Open Date Selection Panel']//button[@type='button']//*[name()='svg']")
    time.sleep(random.uniform(1, 3))  # Randomized delay
    date_selection_panel_button.click()
    time.sleep(random.uniform(2, 4))  # Randomized delay for the panel to open
except NoSuchElementException:
    print("Error: Could not find the 'Open Date Selection Panel' button.")
    driver.quit()

# Hardcoded values for year, month, day, and hour ranges
years = ['2022', '2023', '2024']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
days = list(range(1, 32))
hours = list(range(0, 24))

missing_file = 'missing_images.csv'

# Initialize CSV file
with open(missing_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Year', 'Month', 'Day', 'Hour'])

def log_missing(year, month, day, hour):
    with open(missing_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([year, month, day, hour])
    print(f"Logged missing image for {year}-{month}-{day} hour {hour}")

def select_button_by_value(value):
    try:
        button_xpath = f"//button[normalize-space()='{value}']"
        button = driver.find_element(By.XPATH, button_xpath)
        time.sleep(random.uniform(1, 2))
        button.click()
        time.sleep(random.uniform(1, 3))
        return True
    except NoSuchElementException:
        print(f"Skipping - Button with text '{value}' not found.")
        return False


def save_file(year, month, day, hour):
    time.sleep(2)  # Wait for the save dialog to appear
    folder_path = f"C:\\Users\\jocel\\Downloads\\temp_water\\water_image\\year={year}\\month={month}\\day={str(day).zfill(2)}\\hour={str(hour).zfill(2)}"
    file_name = f"MO_Missouri_River_at_Hermann___{year}_{month}_{str(day).zfill(2)}_{str(hour).zfill(2)}.png"
    full_path = os.path.join(folder_path, file_name)

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    # Type the full path into the file name field
    pyautogui.write(full_path)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)  # Wait for the save operation to complete

def select_button_by_text_in_section(section_name, value):
    try:
        button_xpath = f"//h6[normalize-space()='{section_name}']/following-sibling::div//button[normalize-space()='{value}' and contains(@class, 'MuiButtonBase-root')]"
        button = driver.find_element(By.XPATH, button_xpath)
        time.sleep(random.uniform(0.5, 2))
        button.click()
        time.sleep(random.uniform(1, 3))
        return True
    except NoSuchElementException:
        print(f"Skipping - Button with text '{value}' not found in {section_name}")
        return False


def find_next_available(value_list, value_type, section_name):
    time.sleep(random.uniform(1, 2))
    for value in value_list:
        if select_button_by_text_in_section(section_name, str(value)):
            print(f"Selected {value_type}: {value}")
            return value
    print(f"No available {value_type} found.")
    return None

def download_image():
    for year in years:
        if not select_button_by_value(year):
            continue
        for month in months:
            if not select_button_by_value(month):
                continue
            for day in days:
                if find_next_available([day], 'day', 'Day') is None:
                    continue
                for hour in hours:
                    if find_next_available([hour], 'hour', 'Hour') is None:
                        continue
                    try:
                        download_button = driver.find_element(By.XPATH,
                                                              "//div[@aria-label='Download']//button[@type='button']//*[name()='svg']")
                        time.sleep(random.uniform(2, 3))
                        download_button.click()
                        print(f"Downloading image for {year}-{month}-{day} hour {hour}")
                        save_file(year, month, day, hour)
                    except NoSuchElementException:
                        print(f"Skipping - Download icon not found for {year}-{month}-{day} hour {hour}")
                        log_missing(year, month, day, hour)
                        continue


# Call the function to start downloading images
download_image()

# Close the browser after completing tasks
driver.quit()