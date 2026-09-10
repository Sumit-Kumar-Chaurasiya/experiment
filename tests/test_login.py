from selenium import webdriver


def test_google_title():
    driver = webdriver.Chrome()

    try:
        driver.get("https://www.google.com")

        assert "Google" in driver.title

    finally:
        driver.quit()