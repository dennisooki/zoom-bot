import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 2, 
    "profile.default_content_setting_values.media_stream_camera": 2,
    "profile.default_content_setting_values.geolocation": 2, 
    "profile.default_content_setting_values.notifications": 2 
})

adm=[21777]

curr_adm=adm.pop()
m_id=0    #meeting id
m_pwd=0    #meeting pwd

delays={'ns':0,'wr':0}  #ns=  not started; wr=waiting room

driver=webdriver.Chrome(options=opt)
action = webdriver.ActionChains(driver)

class CurrentAdm:
    def __init__(self, adm):
        self.adm = adm
        self.delays = {'ns':0,'wr':0}
        # self.start=0 #for timer
        self.complete=False

    def startTimer(self):   #timer to time delays
        self.start=time.time()

    def endTimer(self,typ):     #typ=type of timer;wr or ns
        self.delays[typ]=time.time()-self.start

    def markComplete(self):
        self.complete=True
        print('Successfully entered {}'.format(self.adm))
        if self.delays['ns']>0 or self.delays['wr']>0:
            print(self.delays)
        else:
            print('No delays encountered')

    def preJoin(self):
        
        driver.get("https://zoom.us/wc/join/{}".format(m_id))
        driver.find_element(By.ID, "inputname").send_keys(curr_adm)
        driver.find_element(By.ID, "joinBtn").click()

        if 'not started' in driver.title:
            print('Meeting not started')
            # start=time.time()
            self.startTimer()
            while 'not started' in driver.title:
                time.sleep(5)
               
            # delays['ns']=time.time()-start
            self.endTimer('ns')
            print('waited {}s for meeting 2 start'.format(int(self.delays['ns'])))
        
        self.joinMeeting()


    def joinMeeting(self):
        driver.find_element(By.ID, "inputpasscode").send_keys(m_pwd)
        driver.find_element(By.ID, "joinBtn").click()

        print('Entering Waiting Abyss')
        self.startTimer()
        self.waitingRoom()


    def waitingRoom(self):
        # delays['wr']=delays['wr']-time.time()
        try:
            WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.CSS_SELECTOR, ".footer-chat-button > .footer-button-base__button path"))
            # time.sleep(20)  
            try:
                action.move_by_offset(10, 20)
                action.perform()
                driver.find_element(By.CSS_SELECTOR, ".footer-chat-button > .footer-button-base__button path").click()
                driver.find_element(By.CSS_SELECTOR, ".chat-box__chat-textarea").send_keys('Success'+Keys.RETURN)
                print('We r in, first adm entered successfully')
            except:
                self.waitingRoom()
            
        except:
            elapsed_time=time.time()-self.start
            if elapsed_time==0:
                print('Probably waiting for host to admit')
            elif elapsed_time>=30:
                print('About {} seconds elapsed in waiting room'.format(elapsed_time))
            elif elapsed_time>300:
                print('5 mins wait surpassed on current adm no, Retrying with next')
                

            time.sleep(5)  #wait 5 secs then check if joined
            self.waitingRoom()

        self.endTimer('wr')

test=CurrentAdm(23)
test.preJoin()
# preJoin()
# print(delays)





# driver.quit()