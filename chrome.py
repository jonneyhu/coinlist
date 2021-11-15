import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, subprocess

# options = webdriver.ChromeOptions()
# # options.add_argument(r'--user-data-dir=F:\coinlist\japan\noc\noc9')
# # options.add_argument('--proxy-server=socks5://45.32.44.116:6058')
# # options.add_experimental_option("excludeSwitches", ['enable-automation']);
# options.add_experimental_option("debuggerAddress", "127.0.0.1:12306")
#
#
def waitAndClick(driver, xpath):
    element = WebDriverWait(driver,100).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    element.click()
#
#
# def registrySale1(driver):
#     # 继续
#     time.sleep(1)
#     waitAndClick(driver, "/html/body/div[3]/div/div/div[2]/div/div/a")
#     # 确认用户
#     waitAndClick(driver, "/html/body/div[3]/div/div/div[2]/div/div/div[2]/a")
#     time.sleep(1)
#
#     WebDriverWait(driver,100).until(
#         EC.presence_of_element_located((By.XPATH, '//*[@id="forms_offerings_participants_residence_residence_country"]'))
#     )
#     # 确认国家
#     country = driver.find_element_by_xpath('//*[@id="forms_offerings_participants_residence_residence_country"]')
#     country.send_keys("Japan")
#     # country.send_keys("Singapore")
#     # country.send_keys("Philippines")
#     waitAndClick(driver, '//*[@id="new_forms_offerings_participants_residence"]/div[4]/div/label')
#     waitAndClick(driver, '//*[@id="new_forms_offerings_participants_residence"]/div[5]/a')
#     time.sleep(3)
#
#
#     driver.find_element_by_xpath("//input[@value='f1556b05-2b96-401c-9ba0-0e9dcf9f206c']").click()
#     driver.find_element_by_xpath("//input[@value='57bea716-85fe-4ba4-8462-3fcc6a6cf5ea']").click()
#     driver.find_element_by_xpath("//input[@value='5af28f06-1f4f-4536-b2fe-fc31c24e8914']").click()
#
#     driver.find_element_by_xpath("//input[@value='ef4316e3-f936-412f-a02c-d999bfb4268f']").click()
#     driver.find_element_by_xpath("//input[@value='ed3257a2-bd04-4852-8ae6-8a6dcdd67752']").click()
#
#     driver.find_element_by_xpath("//input[@value='de6a9ea6-b8de-47f6-9a30-be4f40eadeab']").click()
#     driver.find_element_by_xpath("//input[@value='06623d82-7adf-4a78-8efa-907fb5aa77c4']").click()
#
#     driver.find_element_by_xpath("//input[@value='53083dfd-6d56-49c4-9ce4-da54d959367e']").click()
#     driver.find_element_by_xpath("//input[@value='e6297d49-0a98-4688-b0f1-ace5e117840c']").click()
#     driver.find_element_by_xpath("//input[@value='6288539f-6b0a-4259-b405-d61e7157ba02']").click()
#
#     waitAndClick(driver, '/html/body/div[3]/div/div/div[2]/div/div/div[2]/form/div[3]/a')
#     time.sleep(3)
#
# def login(driver):
#     driver.get("https://coinlist.co/login")
#     time.sleep(2)
#
#
# def run():
#     driver = webdriver.Chrome(options = options)
#     # driver.get("https://coinlist.co/login")
#     try:
#         element = WebDriverWait(driver,100).until(
#             EC.presence_of_element_located((By.CLASS_NAME,"icon-user-outline"))
#         )
#     except Exception as e:
#         print(str(e))
#         driver.quit()
#
#     # 注册
#
#     registrySale(driver=driver)
#     driver.get("https://coinlist.co/immutable-x-option-2")
#     registrySale(driver=driver)


from selenium import webdriver
from selenium.webdriver import ChromeOptions
import onetimepass as otp

# clientKey：在个人中心获取
clientKey = "bdde1432474e498551b60de507d56af903ce80b4829"
# 目标参数：
# websiteURL = "https://www.google.com/recaptcha/api2/demo"


def googleAuth(secret):
    if secret == "":
        return 0
    try:
        code = otp.get_totp(secret)
        if len(code) == 5:
            return '0' + code
    except Exception as e:
        return 0
    else:
        return code


def create_task(key):
    url = "https://api.yescaptcha.com/createTask"
    data = {
        "clientKey": clientKey,
        "task": {
            "websiteURL": "https://coinlist.co",
            "websiteKey": key,
            "type": "NoCaptchaTaskProxyless"
        }
    }
    try:
        # 发送JSON格式的数据
        result = requests.post(url, json=data).json()
        taskId = result.get('taskId')
        if taskId is not None:
            return taskId
        print(result)

    except Exception as e:
        print(e)


def get_response(taskID: str):
    """
    第二步：使用taskId获取response
    :param taskID: string
    :return response: string 识别结果
    """

    # 循环请求识别结果，3秒请求一次
    times = 0
    while times < 120:
        try:
            url = f"https://api.yescaptcha.com/getTaskResult"
            data = {
                "clientKey": clientKey,
                "taskId": taskID
            }
            result = requests.post(url, json=data).json()
            solution = result.get('solution', {})
            if solution:
                response = solution.get('gRecaptchaResponse')
                if response:
                    return response
            print(result)
        except Exception as e:
            print(e)

        times += 3
        time.sleep(3)


def verify_website(driver, response):
    """
    第三步：提交给网站进行验证
    :param response: string
    :return html: string
    """

    # 如果报错：Message: 'geckodriver' executable needs to be in PATH
    # 参考解决：https://www.jianshu.com/p/1d177b266fd2
    # driver = webdriver.Firefox(executable_path=r'C:\Program Files\Mozilla Firefox\geckodriver.exe')

    # driver = webdriver.Firefox()
    # driver.get("https://www.google.com/recaptcha/api2/demo")

    # 每个网站的处理方式不同，但是大概思路是一样的
    # 无外乎拿到验证码识别结果，然后想办法提交
    # JS回调就是提交的一种
    # 以下步骤请先看看官方官网的代码，
    # 理解一下三个步骤

    # 在网页上执行JS，将获得的验证码写入网页
    driver.execute_script(f'document.getElementById("g-recaptcha-response").value="{response}"')

    # 执行回调函数，每个网站回调函数并不相同，需要自己找一下
    # 一般为data-callback=xxxx，这个xxxx就是回调函数
    f = 'return (function (){\
    if (typeof (___grecaptcha_cfg) !== "undefined") {\
    return Object.entries(___grecaptcha_cfg.clients).map(([cid, client]) => {\
      const data = { id: cid, version: cid >= 10000 ? "V3" : "V2" };\
      const objects = Object.entries(client).filter(([_, value]) => value && typeof value === "object");\
      objects.forEach(([toplevelKey, toplevel]) => {\
        const found = Object.entries(toplevel).find(([_, value]) => (\
          value && typeof value === "object" && "sitekey" in value && "size" in value\
        ));\
        if (typeof toplevel === "object" && toplevel instanceof HTMLElement && toplevel["tagName"] === "DIV"){\
            data.pageurl = toplevel.baseURI;\
        }\
        if (found) {\
          const [sublevelKey, sublevel] = found;\
          data.sitekey = sublevel.sitekey;\
          const callbackKey = data.version === "V2" ? "callback" : "promise-callback";\
          const callback = sublevel[callbackKey];\
          if (!callback) {\
            data.callback = null;\
            data.function = null;\
          } else {\
            data.function = callback;\
            const keys = [cid, toplevelKey, sublevelKey, callbackKey].map((key) => `["${key}"]`).join("");\
            data.callback = `___grecaptcha_cfg.clients${keys}`;\
          }\
        }\
      });\
      return data;\
    });\
  }\
  return [];\
})()'

    base = driver.execute_script(f)
    print(base)
    driver.execute_script(f"___grecaptcha_cfg.clients['0']['U']['U']['callback']('{response}')")

    # 点击提交
    # driver.find_element_by_id("recaptcha-demo-submit").click()
    return driver.page_source


def check_recaptcha(driver):
    anchor_link =WebDriverWait(driver,50).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="challenge-container"]/div/div/iframe'))
    )
    # anchor_link = driver.find_element('xpath', '//*[@id="challenge-container"]/div/div/iframe')
    title = anchor_link.get_attribute('src')
    if title:
        site_key = title.split('&')[1].split('=')[1]
        print(site_key)
        task_id = create_task(site_key)
        resp = get_response(task_id)
        verify_website(driver, resp)


def coinlist():
    # 1.实例化一个ChromeOptions对象
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument('--user-data-dir=/home/jonney/mychrome')
    # 2.将ChromeOptions实例化的对象option作为参数传给Crhome对象
    path = '/home/jonney/Downloads/chromedriver/chromedriver'
    driver = webdriver.Chrome(executable_path=path, options=option)

    # 3.发起请求
    driver.get('https://coinlist.co/login')
    time.sleep(10)
    email = 'nissebn9v581@gmail.com'
    password = 'ww3210231994'

    driver.find_element('xpath', '//*[@id="user_email"]').send_keys(email)
    driver.find_element('xpath', '//*[@id="user_password"]').send_keys(password)
    driver.find_element('xpath', '//*[@id="new_user"]/div/div[5]/input').click()
    time.sleep(5)
    sercret = 't4436e6qkjtpo2tmk5ukjv33'
    code = googleAuth(sercret)
    driver.find_element('xpath', '//*[@id="multi_factor_authentication_totp_otp_attempt"]').send_keys(code)
    driver.find_element('xpath', '//*[@id="new_multi_factor_authentication_totp"]/div/div[2]/input').click()

    # link2 = 'https://newassets.hcaptcha.com/captcha/v1/364e801/stat'


def new_window():

    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    path = '/home/jonney/Downloads/chromedriver/chromedriver'
    s =Service(path)
    driver = webdriver.Chrome(service=s, options=option)
    driver.get('https://coinlist.co')

    time.sleep(5)
    check_recaptcha(driver)
    time.sleep(3600)


if __name__ == '__main__':
    # print(googleAuth('t4436e6qkjtpo2tmk5ukjv33'))
    # coinlist()
    new_window()
