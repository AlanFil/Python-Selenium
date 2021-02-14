from selenium import webdriver

driver = webdriver.Chrome('C:/Users/user/PycharmProjects/Adding-automating-products/Utilities/chromedriver.exe')

driver.get('https://matrixmedia.pl/nowosci/')
driver.implicitly_wait(5)
links_raw = driver.find_elements_by_xpath('//li[@class="item last"]/a')

links = [link.get_attribute('href') for link in links_raw]

for link in links:
    driver.get(link)
