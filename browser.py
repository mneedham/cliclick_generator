import time
from selenium.webdriver.common.by import By

class PinotBrowser:
    def __init__(self, driver):
        self.driver = driver

    def run_query(self):
        buttons = self.driver.find_elements(By.CSS_SELECTOR, ".MuiButton-label")
        self.move_cursor(buttons[0])
        self.driver.execute_script("arguments[0].click()", buttons[0])

    def resize_textarea(self, query):
        textarea_height = len(query.strip().split("\n")) * 40
        height_str = f"height:{textarea_height}px;"

        div = self.driver.find_elements(By.CSS_SELECTOR, ".MuiGrid-root .MuiGrid-item .MuiGrid-grid-xs-12")[0].find_element(By.CSS_SELECTOR, "div")
        self.driver.execute_script("arguments[0].setAttribute('style', '" + height_str + "')", div)

    # def update_query(self, query):
    #     self.driver.execute_script("arguments[0].CodeMirror.setValue(\"""\");", code_mirror);
    #     time.sleep(0.2)
    #     self.driver.execute_script(
    #         "arguments[0].CodeMirror.setValue(\"" + query.strip().replace("\n", "\\n").replace('"', '\\"') + "\");", 
    #         code_mirror
    #     );
    #     time.sleep(0.5)

        
    def move_cursor(self, element):
        self.driver.execute_script("document.cursor.moveToTarget(arguments[0],speed = 3, offsetX = 0.35, offsetY = 0.20 )", element);
        time.sleep(1.5)

    def scroll_down_and_up(self, pixels, wait):
        iterations = list(range(0, pixels, 100))
        for _ in iterations:
            self.driver.execute_script("window.scrollBy(0,arguments[0])", pixels / (len(iterations)));
            time.sleep(0.05)
        time.sleep(wait)
        for _ in iterations:
            self.driver.execute_script("window.scrollBy(0,arguments[0])", -(pixels / (len(iterations))));
            time.sleep(0.05)
        time.sleep(wait)
