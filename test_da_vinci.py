import re
from uuid import uuid4

from settings import PASSWORD, EMAIL

# Constants
TIMEOUT_IMAGE = 20000
TIMEOUT_VIDEO = 600000
PLACEHOLDER_PROMPT = "Type a prompt ..."
BUTTON_GENERATE = "Generate 2"
SAVE_PATH = "/Users/dmitryger/PycharmProjects/leonardoai_automation/"

image_1_locator = "div.css-1uhvlas > div:nth-child(2) > div.css-hoyejk > div > div.css-0 > div > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(2)"
image_2_locator = "div.css-1uhvlas > div:nth-child(2) > div.css-hoyejk > div > div:nth-child(3) > div > div:nth-child(2)> div:nth-child(1) > div > div > div:nth-child(2)"
video_1_locator = "div.css-1uhvlas > div:nth-child(2) > div.css-hoyejk > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(2)"


def login_and_get_page(login_page, login_name):
    leonardo_page = login_page(login_name)
    leonardo_page.page.get_by_role("button", name="Microsoft").click()
    leonardo_page.page.get_by_test_id("i0116").click()
    leonardo_page.page.get_by_test_id("i0116").fill(PASSWORD)
    leonardo_page.page.get_by_test_id("i0116").dblclick()
    leonardo_page.page.get_by_test_id("i0116").press("Meta+a")
    leonardo_page.page.get_by_test_id("i0116").fill(EMAIL)
    leonardo_page.page.get_by_role("button", name="Next").click()
    leonardo_page.page.get_by_test_id("i0118").fill(PASSWORD)
    leonardo_page.page.get_by_role("button", name="Sign in").click()
    leonardo_page.page.get_by_label("Stay signed in?").click()
    leonardo_page.page.get_by_placeholder("myawesomeusername").click()
    leonardo_page.page.get_by_placeholder("myawesomeusername").fill(login_name)
    leonardo_page.page.get_by_role("button", name="advertising").click()
    return leonardo_page


def configure_image_settings(leonardo_page):
    leonardo_page.page.get_by_role("dialog", name="Welcome to Leonardo.Ai").locator("span").nth(1).click()
    leonardo_page.page.get_by_role("button", name="Next").click()
    leonardo_page.page.get_by_label("Close", exact=True).click()
    leonardo_page.page.get_by_role("link", name="Create New Image").click()
    leonardo_page.page.get_by_label("Close").nth(3).click()
    leonardo_page.page.get_by_text("1", exact=True).click()
    leonardo_page.page.get_by_role("button", name="3:2").click()
    leonardo_page.page.get_by_role("menuitem", name="16:9").click()
    leonardo_page.page.locator("div").filter(has_text=re.compile(r"^AlchemyV2Loading\.\.\.$")).locator("span").nth(3).click()


def generate_and_download_video(leonardo_page, prompt, file_suffix, image_locator):
    leonardo_page.page.get_by_placeholder("Type a prompt ...").click()
    leonardo_page.page.get_by_placeholder("Type a prompt ...").fill(prompt)
    leonardo_page.page.get_by_role("button", name="Generate 2").click()
    image = leonardo_page.page.locator(image_locator)
    image.wait_for(state='visible', timeout=20000)
    image.hover()
    image.get_by_label("Generate Motion video").click()
    leonardo_page.page.locator("footer > div > button.chakra-button.css-17emeou").click()
    video = leonardo_page.page.locator("div.css-1uhvlas > div:nth-child(2) > div.css-hoyejk > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(2)")
    video.wait_for(state='visible', timeout=600000)
    video.hover()
    leonardo_page.page.locator(
        "div.css-1uhvlas > div:nth-child(2) > div.css-hoyejk > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(1)").hover()

    with leonardo_page.page.expect_download() as download_info:
        leonardo_page.page.locator(
            "div.css-1uhvlas > div:nth-child(2) > div.css-hoyejk > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(1) > div > div > div.css-1lpsa6b > div.css-1sg7dwz> div > button").click()

    download = download_info.value
    download.save_as("/Users/dmitryger/PycharmProjects/leonardoai_automation/" + file_suffix)


def test_leonardo(login_page, pages_manager):
    login_name = uuid4().hex[:8]
    leonardo_page = login_and_get_page(login_page, login_name)
    configure_image_settings(leonardo_page)

    # Generate and download videos
    generate_and_download_video(leonardo_page, "house", "house_video.mp4", image_1_locator)
    generate_and_download_video(leonardo_page, "mother", "mother_video.mp4", image_2_locator)
    generate_and_download_video(leonardo_page, "father", "father_video.mp4", image_2_locator)
    generate_and_download_video(leonardo_page, "car", "father_video.mp4", image_2_locator)
    generate_and_download_video(leonardo_page, "ship", "father_video.mp4", image_2_locator)
