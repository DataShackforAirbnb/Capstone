# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import time
import random
import pandas as pd
import numpy as np
import pickle
import os
import urllib2
import json




class SendOffer(unittest.TestCase):

    def login(self ,user_name, signin_password ):
        self.driver.get(self.base_url + "")
        time.sleep(random.uniform(0.5, 1)+1)
        self.driver.find_element_by_link_text("Accedi").click()
        time.sleep(random.uniform(0.5, 1)+1)
        self.driver.find_element_by_id("signin_email").clear()
        time.sleep(random.uniform(0.5, 1))
        self.driver.find_element_by_id("signin_email").send_keys(user_name)
        time.sleep(random.uniform(0.5, 1))
        self.driver.find_element_by_id("signin_password").clear()
        time.sleep(random.uniform(0.5, 1))
        self.driver.find_element_by_id("signin_password").send_keys(signin_password)
        time.sleep(random.uniform(0.5, 3)+1)
        self.driver.find_element_by_id("user-login-btn").click()
        
        
    
    
    def setUp(self):
        #self.driver = webdriver.Firefox()
        chromedriver = "C:\Users\user\Desktop\Harvard\chromedriver.exe"
        os.environ["webdriver.chrome.driver"] = chromedriver        
        self.driver = webdriver.Chrome(chromedriver)
        #self.driver.implicitly_wait(0)
        self.base_url = "https://www.airbnb.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_send_offer(self):
        driver = self.driver        
        user_name = "michelebernardi1990@gmail.com"
        signin_password = "LastPassEver2016"       
        bucket = "orphan_3d_advance_2w"
        test = pd.read_json('final_messages/'+bucket+'.json')
        count = 0         
        ids= []
        successfuls= []
        reasons= []        
        outputFile= bucket + '.json'                

        #for starting at position "starting" in the list
        starting = 0
        test = test.ix[starting:]  
        test = test[:2]      
        self.login(user_name,signin_password)
        time.sleep(5)
        driver.get(self.base_url)
        time.sleep(random.uniform(0.5, 2))                
        for index, row in test.iterrows():
            print count
            count= count+1    
	        
            try:
                driver.get(str(row['listing_url'])+ "?check_in="+ str(row['Start'])+ "&guests="+str(row['beds'])+"&check_out="+str(row['End']))            
                time.sleep(random.uniform(0.5, 6))
                time.sleep(3)
                exit= False
                
                #id updating
                ids.append(row['listing_url'])
                
                exit = self.is_element_present(By.XPATH,"//p[contains(.,'These dates are not available')]" )
                exit = exit or self.is_element_present(By.XPATH,"//p[contains(.,'Queste date non sono disponibili')]" )
                if exit:
                    #reason updating
                    reasons.append("These dates are not available") 
                    successfuls.append(False)
                    res_df = pd.DataFrame({'id': ids, 'successfuls': successfuls, 'reasons': reasons})                
                    res_df.to_json(outputFile)                                                        
                    continue                

                exit =  self.is_element_present(By.XPATH,"//p[contains(.,'Minimum stay is')]" )
                exit = exit or self.is_element_present(By.XPATH,"//p[contains(.,'Il minimo numero di notti')]" )                
                if exit:
                    #reason updating
                    reasons.append("Minimum stay is")
                    successfuls.append(False)
                    res_df = pd.DataFrame({'id': ids, 'successfuls': successfuls, 'reasons': reasons})                
                    res_df.to_json(outputFile)                                    
                    continue                
                #if self.is_alert_present():
                #    print self.close_alert_and_get_its_text()
                time.sleep(1)
                driver.find_element_by_css_selector("a > strong > span").click()
                time.sleep(random.uniform(0.5, 5)+5)              
                exit = self.is_element_present(By.CLASS_NAME,"contacted-before" )
                
                if exit:
                    exit=driver.find_element(by=By.CLASS_NAME, value="contacted-before").is_displayed()
                if exit:                                        
                    reasons.append("contacted-before")
                    successfuls.append(False) 
                    res_df = pd.DataFrame({'id': ids, 'successfuls': successfuls, 'reasons': reasons})                
                    res_df.to_json(outputFile)                
                    continue
                print "Iteration number " + str(count)

                driver.find_element_by_xpath("//textarea[@name='question']").clear()
               
                time.sleep(random.uniform(0.5, 1)+1)
                driver.find_element_by_xpath("//textarea[@name='question']").send_keys(row['messages'])
                time.sleep(random.uniform(0.5, 5)+5)
                print "Successful"                                
                #driver.find_element_by_xpath("(//button[@type='submit'])[4]").click()                                
                time.sleep(random.uniform(0.5, 6)+2)
                successfuls.append(True)
                reasons.append("")                                  
                res_df = pd.DataFrame({'id': ids, 'successfuls': successfuls, 'reasons': reasons})
                res_df.to_json(outputFile)                
                
            #except urllib2.URLError as e:
            except Exception as e:
                print "exception" + str(e.args)
                reasons.append(str(e.printStackTrace())) #e.args
                successfuls.append(False) 
                res_df = pd.DataFrame({'id': ids, 'successfuls': successfuls, 'reasons': reasons})
                res_df.to_json(outputFile)                
                pass
 
 
    
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
