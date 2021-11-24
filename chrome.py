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
        code = str(otp.get_totp(secret))
        if len(code) == 5:
            return '0' + code
    except Exception as e:
        return 0
    else:
        return code


def create_task(key,category="NoCaptchaTaskProxyless",link="https://coinlist.co"):
    url = "https://api.yescaptcha.com/createTask"

    data = {
        "clientKey": clientKey,
        "task": {
            "websiteURL": link,
            "websiteKey": key,
            "type": category
        }
    }
    try:
        # 发送JSON格式的数据
        result = requests.post(url, json=data).json()
        taskId = result.get('taskId')
        if taskId is not None:
            return taskId
        print('create task err:',result)

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

def get_callback_sitekey(driver):
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
    return base


def check_hcaptcha(driver):
    f = 'return (function (){ \
            if (window.hcaptcha) {\
                console.log("hcaptcha available, lets redefine render method");\
                window.originalRender = hcaptcha.render;\
                window.hcaptcha.render = (container, params) => {\
                    console.log(container);\
                    console.log(params);\
                    window.hcaptchaCallback = params.callback;\
                    return window.originalRender(container, params);\
                };\
                return 1;\
            } else {\
                console.log("hcaptcha not available yet");\
                return 0;\
            }})()'

    base =  driver.execute_script(f)
    print(base)
    return base


def check_captcha(driver):

    base = get_callback_sitekey(driver)
    if len(base) >0 :
        site_key = base[0].get('site_key')
        callback = base[0].get('callback')
        if site_key:
            task_id = create_task(site_key)
            resp = get_response(task_id)
            driver.execute_script(f'{callback}({resp})')
    # if check_hcaptcha(driver)==1:
    #     h_site_key = '73d09584-544c-4fe0-b048-ddf0b6bd3064'
    #     # h_site_key = '33f96e6a-38cd-421b-bb68-7806e1764460'
    #     # link = 'https://my.vultr.com'
    #     task_id = create_task(h_site_key,"HCaptchaTaskProxyless")
    #     resp = get_response(task_id)
    #     print(resp)
    #     driver.execute_script(f'document.getElementsByName("h-captcha-response")[0].value="{resp}"')
    #     # driver.execute_script('_cf_chl_hload()')
    #     driver.execute_script('_hcaptchaOnLoad()')
    #     time.sleep(3600)
    #     driver.execute_script('window.hcaptchaCallback('+f'"{resp}"'+')')


def waitAndSend(driver,xpath,val):
    element = WebDriverWait(driver,100).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    element.send_keys(val)

def waitAndClear(driver,xpath):
    element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    element.clear()

def registrySale(driver,link='https://coinlist.co/umee-option-1/onboarding'):
    driver.get(link)
    # 继续

    waitAndClick(driver, "/html/body/div[3]/div/div/div[2]/div/div/a")
    # 确认用户

    waitAndClick(driver, "/html/body/div[3]/div/div/div[2]/div/div/div[2]/a")

    WebDriverWait(driver,100).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="forms_offerings_participants_residence_residence_country"]'))
    )
    # 确认国家
    country = driver.find_element_by_xpath('//*[@id="forms_offerings_participants_residence_residence_country"]')
    country.send_keys("Hong Kong")
    # country.send_keys("Singapore")
    # country.send_keys("Philippines")
    waitAndClick(driver, '//*[@id="new_forms_offerings_participants_residence"]/div[4]/div/label')
    waitAndClick(driver, '//*[@id="new_forms_offerings_participants_residence"]/div[5]/a')
    time.sleep(3)

    # answer questions
    answers=['"Option 1: 300,000,000; Option 2: 200,000,000"','"Users in the waiting room for the sale will be given a random spot in the queue when the sale starts. Users who arrive after the sale starts for the sale will be placed behind those in the waiting room"',
            '"Multichain"','"Cross chain lending hub"','"BTC, ETH, USDC, USDT"','"Option 1: $0.06 per token, $500 limit. Option 2: $0.07 per token, $500 limit"','"The user\'s purchase may be cancelled and the user may be banned from future CoinList sales "','"CoinList.co"',
            '"The user\'s account will be terminated and all purchases will be cancelled"']
    # driver.find_element_by_xpath("//input[@value='00a925ae-ec5a-4baf-b01f-a754447c4bee']").click()
    # driver.find_element_by_xpath("//input[@value='c0f5a54e-0b74-4c6e-897c-2d68236102b5']").click()
    # driver.find_element_by_xpath("//input[@value='eeff322d-0c13-4159-9b3e-9310e949d53a']").click()
    #
    # driver.find_element_by_xpath("//input[@value='377d7601-db4c-407d-8fdc-fd32f9fd1cb9']").click()
    # driver.find_element_by_xpath("//input[@value='92bc7360-90e4-41e4-b2d7-470455972697']").click()
    #
    # driver.find_element_by_xpath("//input[@value='2ae9764b-8887-4869-abb1-8635f775acb1']").click()
    # driver.find_element_by_xpath("//input[@value='c2766d1c-c578-41c2-b45b-a2ac73cb5d02']").click()
    #
    # driver.find_element_by_xpath("//input[@value='bd37e044-ecc7-48be-92b1-4ae03ff4a272']").click()
    # driver.find_element_by_xpath("//input[@value='0812a1af-2f39-43ff-a891-c28d9df30274']").click()
    for answer in answers:
        time.sleep(1)
        driver.find_element_by_xpath("//label[contains(text(),{})]".format(answer)).click()
    # continue
    waitAndClick(driver, '/html/body/div[3]/div/div/div[2]/div/div/div[2]/form/div[3]/a')
    time.sleep(3)


def coinlist():
    # 1.实例化一个ChromeOptions对象
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument('--user-data-dir=D:\mychrome\chrome1')
    option.add_argument('--proxy-server=socks://45.76.192.110:5022')
    # 2.将ChromeOptions实例化的对象option作为参数传给Crhome对象
    # path = '/home/jonney/Downloads/chromedriver/chromedriver'
    # email = 'nissebn9v581@gmail.com'
    # password = 'ww3210231994'
    email = 'fu54777319880856@163.com'
    password = 'computer4411'
    links = ['https://coinlist.co/umee-option-1/onboarding','https://coinlist.co/umee-option-2/onboarding']

    path='chromedriver.exe'
    s = Service(path)
    driver = webdriver.Chrome(service=s, options=option)

    # 3.发起请求
    driver.get('https://coinlist.co/login')


    # driver.switch_to.window(all_handles[0])
    waitAndClear(driver,'//*[@id="user_email"]')
    waitAndClear(driver,'//*[@id="user_password"]')
    waitAndSend(driver, '//*[@id="user_email"]',email)
    waitAndSend(driver, '//*[@id="user_password"]',password)
    # time.sleep(10)
    # driver.find_element('xpath', '//*[@id="user_email"]').send_keys(email)
    # driver.find_element('xpath', '//*[@id="user_password"]').send_keys(password)
    hcaptch_link = 'https://newassets.hcaptcha.com/captcha/v1/b2f2cbc/hcaptcha-challenge.js'
    driver.execute_script('window.open("{}")'.format(hcaptch_link))
    driver.switch_to.window(driver.window_handles[1])
    print(driver.current_url)
    cookie = {'name': 'hc_accessibility',
              'value': '7Sl61hh/zJWSV1C5m0ynBsKrnrGZan5cAtVxTpHqM3xSvvOel8h++grOdYU3ZTjwLZYcUEGUAjlEaVxa4doxg7en2wv9sTlgatuMLjHOzLC9/kYBB9ow5/w4uAwODE4RLFwghkfpX8jVJwquqpCE3Svq+rqZypHgc2e6fiI+jOwjM22sFQI1ixxiDizKRJ0jUh09oDj7Y4p3b+ePzK65J0A8f7z92XKnU7JjcOMZ3dxe3fOb4y2L3qvSGhuvmsBDB8OjjEk74dVk5azEKIv34O11IeVsujHYbFjOyEZZhz61/otbwh6tT3S4LjAa1QO9ThYl7D2K4mJ6lMrWo76k7/joznqav5BV5aJALLepyifH51XO9A0WVw3Aom1HYko2hsT2x5I+PzSBjgPqG4zCwS2lhmmCTvYFd9dIdZkoIPcIsY1oL2KUXCQLO8tGOkOGpLnV1BYDUpsc1M9YCQwmZGY5/owVqN+krLIdZ668I1F4pSDq0tdGz45gfuX9ytKwT/yW2zFiTUnxB7ojH2Zcc2NAKIEToaU7EB/stVHZMD+oGHBuQugW9GOwNGs8GfbKyi72+eO1NZiujOqaOJoEy2dT1IXczFrxz091EoEGqqSPwnzNWyuJ5bEjY3zS9L5NpqIYtzX8tNvPoNp63RsBVrNSCJUrKeZgyNcDfbwEwxzOCd4CzPmPWyPtRic7W07KgLrkyjEojI9PeU8awW9PV++Se5kGU5o4VxQ4tU/CoJhH2+d6EiPvyo3KmDq3Kf7r6vGVmab/mYXvtEIVSGbdd/3WJtlhxkNwYK1bfpCkVobUFUoAAdMgmKNFXynKfkWKQb9RMB4/fYvzyy4TK4u8aAyFT/zxnN6cF7tJMr3OwggWhqaAKQiukIgX1lrxt1z8+nnoF/+X8hhlkRM94EwQB7pKh/xcjhS0jVEkYVUxYwphZOUQkLpsPRQTAKaYTRIR3XUnT7F8lVZ+uaAnfeouU+D4Cs80nmfp+W32UyM/q64hGmA0EX2+8tiFYs3kJOYTog+dOk2o3UHrndmiAS1XIA==g9qlWMo6H0UZfz+9',
              'path': '/', 'expires': '2021-11-24T20:44:31.225Z', 'secure': True,'sameSite':'None'}
    driver.add_cookie(cookie_dict=cookie)
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[0])
    waitAndClick(driver,'//*[@id="new_user"]/div/div[5]/input')
    # driver.find_element('xpath', '//*[@id="new_user"]/div/div[5]/input').click()

    # sercret = 't4436e6qkjtpo2tmk5ukjv33'
    sercret = 'qypchb2ukiexvyq7cwztfalt'
    code = googleAuth(sercret)
    waitAndSend(driver, '//*[@id="multi_factor_authentication_totp_otp_attempt"]', code)
    # driver.find_element('xpath', '//*[@id="multi_factor_authentication_totp_otp_attempt"]').send_keys(code)
    waitAndClick(driver, '//*[@id="new_multi_factor_authentication_totp"]/div/div[2]/input')
    # driver.find_element('xpath', '//*[@id="new_multi_factor_authentication_totp"]/div/div[2]/input').click()
    time.sleep(6)
    check_captcha(driver)
    registrySale(driver)
    time.sleep(3600)
    # link2 = 'https://newassets.hcaptcha.com/captcha/v1/364e801/stat'


def new_window():

    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # option.add_argument('--proxy-server=socks://45.76.192.110:5022')
    # path = '/home/jonney/Downloads/chromedriver/chromedriver'
    path = 'chromedriver.exe'
    s =Service(path)
    driver = webdriver.Chrome(service=s, options=option)
    driver.get('https://my.vultr.com/billing/?alipay')

    time.sleep(5)
    check_captcha(driver)
    time.sleep(3600)


if __name__ == '__main__':
    # print(googleAuth('t4436e6qkjtpo2tmk5ukjv33'))
    coinlist()
    # new_window()
