import time
from RPA.Browser.Selenium import Selenium

from util import (
    write_csv_data,
    download_image_from_url,
    check_for_dollar,
    check_phrases,
    create_image_folder,
)

URL = "https://latimes.com/"
SEARCH_PHRASE = "artificial intelligence"
CATEGORY = ["00000168-865c-d5d8-a76d-efddd6550000", "00000168-8683-d2cb-a969-de8b247e0000"] # Business, Food

class SeleniumScraper:
    def __init__(self):
        self.browser_lib = Selenium()

    def close_browser(self):
        self.browser_lib.close_browser()

    def open_website(self, url: str):
        self.browser_lib.open_available_browser(url)
        self.browser_lib.maximize_browser_window()

    def begin_search(self, phrase: str):
        try:
            search_path = "//button[@data-element='search-button']"
            self.browser_lib.click_button_when_visible(locator=search_path)
            search_field_path = "//input[@data-element='search-form-input']"
            self.browser_lib.input_text(locator=search_field_path, text=phrase)
            search_button_path = "//button[@data-element='search-submit-button']"
            self.browser_lib.click_element_if_visible(locator=search_button_path)
        except ValueError as e:
            raise f"Error on execution of begin_search -> {e}"

    def select_category(self, categorys) -> None:
        if len(categorys) == 0:
            return
        else:
            for value in categorys:
                try:
                    see_all_button = "//button[@data-toggle-trigger='see-all']"
                    self.browser_lib.click_button_when_visible(locator=see_all_button)
                    time.sleep(0.1)
                    topics_list = "//*[@data-name='Topics']//li"
                    self.browser_lib.wait_until_page_contains_element(locator=topics_list)
                    topic = f"//input[contains(@type,'checkbox') and contains(@value,'{value}')]"
                    self.browser_lib.click_element_when_visible(locator=topic)
                except ValueError as e:
                    print(f"Error on catergory selection -> {e}")

    def sort_newest_news(self, list_value="1") -> None:
        try:
            sort_by_dropdow_btn = "//select[@name='s']"
            self.browser_lib.select_from_list_by_value(sort_by_dropdow_btn, list_value)

        except ValueError as e:
            raise f"Error on execution of sort_newest_news -> {e}"

    def get_element_value(self, path: str) -> str:
        if self.browser_lib.does_page_contain_element(path):
            return self.browser_lib.get_text(path)
        return ""

    def get_image_value(self, path: str) -> str:
        if self.browser_lib.does_page_contain_element(path):
            return self.browser_lib.get_element_attribute(path, "src")
        else:
            self.browser_lib.wait_until_page_contains_element(path)
            return self.browser_lib.get_element_attribute(path, "src")
        return ""

    def get_element_value(self, path: str) -> str:
        if self.browser_lib.does_page_contain_element(path):
            return self.browser_lib.get_text(path)
        return ""

    def get_image_value(self, path: str) -> str:
        if self.browser_lib.does_page_contain_element(path):
            return self.browser_lib.get_element_attribute(path, "src")
        return ""

    def extract_website_data(self, phrase: str) -> None:
        element_list = "//ul[@class='search-results-module-results-menu']//li"
        news_list_elements = self.browser_lib.get_webelements(element_list)
        extracted_data = []
        for value in range(1, len(news_list_elements) + 1):
            date = self.get_element_value(f"{element_list}[{value}]//p[@class='promo-timestamp']")
            print(date)
            title = self.get_element_value(f"{element_list}[{value}]//h3")
            description = self.get_element_value(f"{element_list}[{value}]//p[@class='promo-description']")
            print(description)
            image = download_image_from_url(
                self.get_image_value(f"{element_list}[{value}]//img")
            )

            is_title_dollar = check_for_dollar(title)
            is_description_dollar = check_for_dollar(description)
            phrases_count = check_phrases(text_pattern=phrase, text=title)

            extracted_data.append(
                [
                    date,
                    title,
                    description,
                    image,
                    is_title_dollar,
                    is_description_dollar,
                    check_phrases(
                        text_pattern=phrase,
                        text=description,
                        count=phrases_count,
                    ),
                ]
            )
        write_csv_data(extracted_data)

    def main(self) -> None:
        try:
            create_image_folder()            
            self.open_website(url=URL)
            self.begin_search(phrase=SEARCH_PHRASE)
            self.select_category(categorys=CATEGORY)
            self.sort_newest_news()
            self.extract_website_data(SEARCH_PHRASE)
            
        finally:
            self.close_browser()


if __name__ == "__main__":
    obj = SeleniumScraper()
    obj.main()
