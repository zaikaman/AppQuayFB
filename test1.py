from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementNotInteractableException

def show_menu():
    print("ỨNG DỤNG QUẬY FB")
    print("1. Gửi tin nhắn")
    print("2. Bình luận")
    print("3. Spam phẫn nộ")
    print("4. Thoát")
    choice = input("Chọn một tùy chọn: ")
    return choice

# Khởi tạo đối tượng ChromeOptions
options = Options()

# Thêm tùy chọn để tắt thông báo
options.add_argument("--disable-notifications")

# Thêm tùy chọn để loại bỏ thông báo lỗi
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Khởi tạo trình duyệt Chrome với các tùy chọn đã thiết lập
driver = webdriver.Chrome(options=options)

try:
    # Mở trang web Facebook
    driver.get('http://www.facebook.com')

    # Giả sử bạn đã có biến username và password
    username = 'codedi4756@jalunaki.com'
    password = 'lovelybaby'

    # Đợi cho đến khi phần tử 'email' xuất hiện
    wait = WebDriverWait(driver, 10)
    email_box = wait.until(EC.presence_of_element_located((By.NAME, 'email')))

    # Điền thông tin đăng nhập
    email_box.send_keys(username)

    # Đợi cho đến khi phần tử 'pass' xuất hiện
    password_box = wait.until(EC.presence_of_element_located((By.NAME, 'pass')))
    password_box.send_keys(password)

    # Nhấn nút đăng nhập
    wait = WebDriverWait(driver, 10)
    login_button = wait.until(EC.element_to_be_clickable((By.NAME, 'login')))
    login_button.click()

    # Đợi trang tải xong
    time.sleep(5)

    def extract_user_id(user_input):
        # Check if the input is a Facebook profile URL
        if "facebook.com/" in user_input:
            # Extract the user ID from the URL using a regular expression
            match = re.search(r'facebook\.com/.*?id=(\d+)', user_input)
            if match:
                user_id = match.group(1)
                print(f"Extracted user ID from URL: {user_id}")  # Debug message
                return user_id
        # If the input is not a URL, assume it's a user ID
        print(f"Input is not a URL, assuming it's a user ID: {user_input}")  # Debug message
        return user_input

    while True:
        choice = show_menu()
        if choice == '4':
            break

        user_input = input("Nhập ID người dùng bạn muốn tương tác (Có thể vào web https://findidfb.com/# để lấy)): ")
        user_id = extract_user_id(user_input)

        if choice == '1':
            # Hỏi người dùng về số lần họ muốn gửi tin nhắn
            num_messages = int(input("Bạn muốn gửi tin nhắn bao nhiêu lần? "))

            # Truy cập vào trang cụ thể
            driver.get(f'https://www.facebook.com/messages/t/{user_id}')

            time.sleep(5)

            # Đợi cho đến khi hộp thoại xuất hiện
            message_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Tin nhắn'][@role='textbox']"))
            )

            # Tìm phần tử chứa tên người dùng
            user_name_element = driver.find_element(By.CSS_SELECTOR, f"a[href='/{user_id}/']")
            user_name = user_name_element.text

            # Gửi tin nhắn số lần tương ứng
            for _ in range(num_messages):
                # Gõ "Xin chào" vào hộp thoại
                message_box.send_keys(f"Đụ má {user_name}")

                # Nhấn phím Enter để gửi tin nhắn
                message_box.send_keys(Keys.RETURN)

                time.sleep(1)  # Đợi một chút trước khi gửi tin nhắn tiếp theo

        elif choice == '2':
            try:
                # Truy cập vào trang cụ thể
                driver.get(f'https://www.facebook.com/{user_id}')

                # Tìm phần tử SVG chứa họ tên người dùng
                time.sleep(5)
                user_name_element = driver.find_element(By.CSS_SELECTOR, "h1.x1heor9g.x1qlqyl8.x1pd3egz.x1a2a7pz")

                # Lấy họ tên từ thuộc tính 'aria-label'
                user_name = user_name_element.text

                # Khởi tạo last_height
                last_height = driver.execute_script("return document.body.scrollHeight")

                # Scroll xuống trang để tải tất cả các bài đăng
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)  # Đợi một chút để trang tải thêm nội dung
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                # Tìm tất cả các ô nhập liệu
                input_boxes = driver.find_elements(By.XPATH, "//div[@aria-label='Viết bình luận...'][@role='textbox']")
                for box in input_boxes:
                    try:
                        # Nhập "Xin chào" + họ tên người dùng và nhấn Enter
                        box.send_keys(f"Đụ má {user_name}")
                        box.send_keys(Keys.RETURN)
                        time.sleep(3)  # Đợi một chút sau mỗi lần bình luận
                    except ElementNotInteractableException:
                        # Nếu không thể tương tác với phần tử, quay lại menu chính
                        break

            except Exception as e:
                print(f"Đã xảy ra lỗi: {e}")

        elif choice == '3':
            try:
                # Truy cập vào trang cụ thể
                driver.get(f'https://www.facebook.com/{user_id}')

                # Khởi tạo last_height
                last_height = driver.execute_script("return document.body.scrollHeight")

                # Scroll xuống trang để tải tất cả các bài đăng
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)  # Đợi một chút để trang tải thêm nội dung
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                # Tìm tất cả các nút "Like"
                like_buttons = driver.find_elements(By.XPATH, "//div[@aria-label='Thích'][@role='button']")

                for like_button in like_buttons:
                    try:
                        # Hover over the "Like" button
                        hover = ActionChains(driver).move_to_element(like_button)
                        hover.perform()

                        # Now the reactions should be visible, find the "Angry" reaction button by its XPath
                        angry_button = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Phẫn nộ'][@role='button']"))
                        )

                        # Click on the "Angry" reaction button
                        angry_button.click()
                        time.sleep(3)  # Đợi một chút sau mỗi lần nhấn
                    except ElementNotInteractableException:
                        # Nếu không thể tương tác với phần tử, quay lại menu chính
                        break

            except Exception as e:
                print(f"Đã xảy ra lỗi: {e}")

except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")

finally:
    # Đóng trình duyệt
    driver.quit()
