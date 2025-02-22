from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 配置 Chrome 选项
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')  # 如果需要无头模式，可以添加这行

# 启动 Chrome
driver = webdriver.Chrome(options=chrome_options)

# 打开网页
driver.get("https://www.google.com")

# 打印网页标题
print(driver.title)

# 关闭浏览器
driver.quit()
