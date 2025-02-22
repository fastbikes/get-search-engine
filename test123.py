<PYTHON>
from selenium import webdriver

# 使用 Chrome 驱动
driver = webdriver.Chrome()

# 打开网页
driver.get("https://www.google.com")

# 打印网页标题
print(driver.title)

# 关闭浏览器
driver.quit()