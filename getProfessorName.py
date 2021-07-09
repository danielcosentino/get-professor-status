from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from twilio.rest import Client


username = ""
password = ""
twilio_account_sid = ''
twilio_auth_token = ''
# use the format (123) 456-7890 -> +11234567890
twilio_phone_number = '+1##########'
my_phone_number = '+1##########'
PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(PATH)

driver.get("https://my.ucf.edu/psp/IHPROD/EMPLOYEE/EMPL/h/?tab=DEFAULT&cmd=login")

# enters username and password and clicks sign on
username_field = driver.find_element_by_name("j_username")
username_field.clear()
username_field.send_keys(username)
password_field = driver.find_element_by_name("j_password")
password_field.clear()
password_field.send_keys(password)
driver.find_element_by_name("_eventId_proceed").click()

# opens student center then calendar 
driver.get("https://my.ucf.edu/psp/IHPROD/EMPLOYEE/CSPROD/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?pt_fname=FX_STUDENT_SLFSRV_MENU_90&FolderPath=PORTAL_ROOT_OBJECT.FX_STUDENT_SLFSRV_MENU_90&IsFolder=true")
driver.get("https://my.ucf.edu/psp/IHPROD/EMPLOYEE/CSPROD/c/SA_LEARNER_SERVICES.SSR_SSENRL_SCHD_W.GBL?FolderPath=PORTAL_ROOT_OBJECT.FX_STUDENT_SLFSRV_MENU_90.FX_HE90_SR.FX_HE90_SR_ENROLLMENT.FX90_SR_WEEKLY_SCHD&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder")

driver.switch_to.frame('TargetContent')

# list view button id clicker
driver.find_element_by_id('DERIVED_REGFRM1_SSR_SCHED_FORMAT$258$').click()
time.sleep(1)

# switch from and back to the iframe
driver.switch_to.default_content()
driver.switch_to.frame('ptifrmtgtframe')

# fall 2021 xpath button clicker
driver.find_element_by_xpath('//*[@id="SSR_DUMMY_RECV1$sels$1$$0"]').click()

# term continue xpath button clicker
driver.find_element_by_xpath('//*[@id="DERIVED_SSS_SCT_SSR_PB_GO"]').click()

# switch from and back to the iframe
driver.switch_to.default_content()
driver.switch_to.frame('TargetContent')

# waits for the site to load, then scrapes the professor's name
professor_name = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.ID, 'DERIVED_CLS_DTL_SSR_INSTR_LONG$4'))).text
driver.quit()

# send twilio text if professors are updated, output to console otherwise
if (professor_name != 'Staff'):
    client = Client(twilio_account_sid, twilio_auth_token)

    message = client.messages \
                    .create(
                         body="Your Professor is " + professor_name,
                         from_=twilio_phone_number,
                         to=my_phone_number
                     )
else:
    print('Still Staff')
