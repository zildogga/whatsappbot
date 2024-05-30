from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import schedule
import time
import random

# Path to your WebDriver
webdriver_path = 'C:\\Users\\Omer\\Downloads\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe'  # Replace with your actual path
contact_name = 'myself'
message_text = ['שיהיה יום טוב מאמי, אוהב המון ❤', 'מקווה שעובר עלייך יום טוב ואוהב אותך ❤', 'איך עובר היום מאמי? אוהב מלא ❤', 'חושב עלייך ואוהב אותך ❤', 'מקווה שעובר יום טוב יפה שלי ❤' 'אהבה שלי, איך עובר עלייך היום? אוהב מלא ❤', 'רק להגיד שאני אוהב אותך ושיהיה המשך יום טוב ❤', 'אוהב אותך המון יפה שלי ושיהיה המשך יום נהדר ❤', ]

# Set up Chrome options
E_PROFILE_PATH = "user-data-dir=C:\\Users\\Omer\\Desktop\\test\\SessionSaver"

options = webdriver.ChromeOptions()
options.add_argument(E_PROFILE_PATH)
driver = webdriver.Chrome(options=options)

def random_time():
    time_str = '{:02d}:{:02d}'.format(random.randint(15, 19), random.randint(0, 59))
    print("Scheduled for {}".format(time_str))
    return time_str

def send_whatsapp_message():
    driver.get('https://web.whatsapp.com')
    try:
        # Search for the contact
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        search_box.send_keys(contact_name)
        search_box.send_keys(Keys.ENTER)

        # Wait for chat to open
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )

        # Type the message
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        message_box.click()
        message_number = random.randint(0, len(message_text))
        message_box.send_keys(message_text[message_number])
        message_box.send_keys(Keys.ENTER)
        print("Message sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

def schedule_daily_message():
    schedule.clear('daily-job')  # Clear any previous daily job
    random_time_str = random_time()
    schedule.every().day.at(random_time_str).do(send_whatsapp_message).tag('daily-job')
    print(f"New message scheduled for {random_time_str}")

if __name__ == "__main__":
    # Schedule the first job
    # testing
    # send_whatsapp_message()

    schedule_daily_message()

    # Schedule the rescheduler to run at midnight
    schedule.every().day.at("00:00").do(schedule_daily_message)

    print("WhatsApp bot started. Waiting to send messages at scheduled times.")

    while True:
        schedule.run_pending()
        time.sleep(1)
