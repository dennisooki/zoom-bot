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

adm=[21,22,23]
rej_adm=[]
curr_adm=adm.pop()
m_id=0
m_pwd=0

delays={'ns':0,'wr':0}  #ns=  not started; wr=waiting room

driver=webdriver.Chrome(options=opt)
action = webdriver.ActionChains(driver)

class CurrentAdm:
    def __init__(self, adm):
        self.adm = adm
        self.delays = {'ns':0,'wr':0}

    def startTimer():   #timer to time delays
        self.start=time.time()

    def endTimer(typ):     #typ=type of timer;wr or ns
        self.delays[typ]=time.time()-self.start

    def markComplete():
        print('Successfully entered {}'.format(self.adm))
        if self.delays['ns']>0 or self.delays['wr']>0:
            print(self.delays)
        else:
            print('No delays encountered')

def preJoin():
            
    
    driver.get("https://zoom.us/wc/join/{}".format(m_id))
    driver.find_element(By.ID, "inputname").send_keys(curr_adm)
    driver.find_element(By.ID, "joinBtn").click()

    if 'not started' in driver.title:
        print('Meeting not started')
        start=time.time()
        while 'not started' in driver.title:
            time.sleep(5)
            #add logic to check total joining time
        delays['ns']=time.time()-start
        print('waited {}s for meeting 2 start'.format(int(delays['ns'])))
    # delays['wr']=0
    joinMeeting()


def joinMeeting():
    driver.find_element(By.ID, "inputpasscode").send_keys(m_pwd)
    driver.find_element(By.ID, "joinBtn").click()

    print('Entering Waiting Abyss')
    delays['wr']=time.time()
    waitingRoom()


def waitingRoom():
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
            waitingRoom()
        else:
            delays['wr']=time.time()-delays['wr']
    except:
        if delays['wr']==0:
            print('Probably waiting for host to admit')
        elif delays['wr']%30==0:
            print('About {} seconds elapsed in waiting room'.format(int(delays['wr'])))
        elif delays['wr']>300:
            print('5 mins wait surpassed on current adm no, Retrying with next')
            rej_adm.append(curr_adm)

        time.sleep(5)  #wait 5 secs then check if joined
        waitingRoom()

preJoin()
print(delays)





# driver.quit()