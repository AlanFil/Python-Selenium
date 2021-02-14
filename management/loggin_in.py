import pyautogui
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('C:/Users/user/PycharmProjects/Adding-automating-products/Utilities/chromedriver.exe')


def logging_in():
    pyautogui.hotkey('Win', 'up')
    driver.implicitly_wait(3)

    driver.get('https://matrixmedia.pl/mpanel')

    driver.find_element_by_name('login[username]').send_keys('py_bot')
    driver.find_element_by_name('login[password]').send_keys('M7qH7Pr%#3DFMzgX')
    driver.find_element_by_name('login[password]').send_keys(Keys.ENTER)

    try:
        driver.find_element_by_link_text('zamknij').click()
    except NoSuchElementException:
        pass

    driver.get(
        driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[3]/ul/li[3]/ul/li[1]/a').get_attribute('href')
    )

    return
