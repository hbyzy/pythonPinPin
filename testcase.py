# coding udt-8
import unittest

import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

from atools import preparetest
from atools import fileoprate


class TestCase:
    pathRoot = os.path.dirname(os.path.abspath(__file__))
    prepare = preparetest.TestTools()
    countinu = False

    def __init__(self):
        url = "https://pinpineat.com/#!/login"
        self.prepare.driverchoice('chrome', url, self.pathRoot)
        self.driver = self.prepare.getDriver()
        self.wait = WebDriverWait(self.driver, 30)

    def test_para_xls1(self):
        path = self.pathRoot + r'\resources\parameter.xlsx'
        file = fileoprate.fileoperate
        parameter = file.read_xls(path, 1)
        for i in range(0, len(parameter)):
            self.login_negtive(parameter[i][0], str(parameter[i][1]))

    def test_para_xls2(self):
        path = self.pathRoot + r'\resources\parameter.xlsx'
        file = fileoprate.fileoperate
        parameter = file.read_xls(path, 1)
        for i in range(0, len(parameter)):
            self.test_login_null(parameter[i][2], str(parameter[i][3]))

    def login_negtive(self, email, password):
        wait = self.wait
        print("test with parameter:", email, password, ">>>>>>>>>>",end ='')
        self.longin_action(email, password)
        wrong_message = wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@id='loginDiv']/div[2]/div/p")))
        # wrong_message=self.driver.find_element_by_xpath("//*[@id='loginDiv']/div[2]/div/p")
        assert "Wrong username or password" in wrong_message.text
        print("test success")
        self.driver.get("https://pinpineat.com/#!/login")

    def login_null(self, email, password):
        print("test with parameter:", email, password, ">>>>>>>>",end='')
        self.longin_action(email, password)
        login_btn = self.driver.find_element_by_xpath("//*[@id='loginDiv']/div[2]/div/form/div[3]/button")
        if login_btn.get_attribute("diasabled") != "":
            print("login button disabled, test success")
        # if (!(loginPage.loginButton.getAttribute("disabled") == null)) {
        self.driver.get("https://pinpineat.com/#!/login")

    def test_login_positive(self):
        driver = self.driver
        wait = self.wait
        self.longin_action("12@12.com","123456")
        # assert change to user page
        user_btn = wait.until(ec.element_to_be_clickable((By.XPATH, "//*[@id='myNavBar']/ul/li[2]/a/span/span[2]")))
        # user_btn = driver.find_element_by_xpath("//*[@id='myNavBar']/ul/li[2]/a/span/span[2]")
        assert "User" in user_btn.text
        print(user_btn.text)
        user_btn.click()
        user_ver = wait.until(ec.presence_of_element_located((By.XPATH, "//*[@id='view']/div/div[2]/div/h3")))
        print(user_ver.text)
        assert "12@12.com" in user_ver.text
        cookies = driver.get_cookies()
        self.assert_cookies(cookies)

    def test_login_stay(self):
        driver = self.driver
        user_email = driver.find_element_by_xpath("//*[@id='username']")
        user_pass = driver.find_element_by_xpath("//*[@id='password']")
        login_btn = driver.find_element_by_xpath("//*[@id='loginDiv']/div[2]/div/form/div[3]/button")
        stay_login=driver.find_element_by_xpath("//*[@id='loginDiv']/div[2]/div/form/div[3]/div/label/p")
        # operation on webpage
        user_email.send_keys("12@12.com")
        user_pass.send_keys("123456")
        stay_login.click()
        login_btn.click()
        time.sleep(3)
        cookies = driver.get_cookies()
        print (cookies)
        print(self.assert_cookies(cookies))

    def tearDown(self):
        self.driver.quit()

    def longin_action(self, email, password):
        driver = self.driver
        user_email = driver.find_element_by_xpath("//*[@id='username']")
        user_pass = driver.find_element_by_xpath("//*[@id='password']")
        login_btn = driver.find_element_by_xpath("//*[@id='loginDiv']/div[2]/div/form/div[3]/button")
        # operation on webpage
        user_email.send_keys(email)
        user_pass.send_keys(password)
        login_btn.click()


    def assert_cookies(self,cookies):
        expiry = 0
        for cookie in cookies:
            for key in cookie:
                if key == "expiry":
                    expiry = cookie['expiry']
        i = round((expiry - time.time()) / (3600 * 24))
        print("didferent is :",i)
        if round((expiry - time.time()) / (3600 * 24)) == 1:
            print("login expiry time is :", i, " day")
        return i

if __name__ == "__main__":
    t = TestCase()
    # t.test_login_positive()
    # t.test_para_xls2()
    t.test_login_stay()
    t.tearDown()
