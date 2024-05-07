import os
import re
import time
from pathlib import Path
from uuid import uuid4

import pytest

from foo import graveyard, ghosts, killers
from settings import EMAIL_1, EMAIL_2, EMAIL_3, PASSWORD_1, PASSWORD_2, PASSWORD_3

# Constants
TIMEOUT_IMAGE = 20000
TIMEOUT_VIDEO = 900000
PLACEHOLDER_PROMPT = "Type a prompt ..."
BUTTON_GENERATE = "Generate 2"
SAVE_PATH = "/Users/dmitryger/Desktop/LeonardoContent/"

image_1_locator = "div.css-1uhvlas > div:nth-child(2) > div.css-hoyejk > div > div.css-0 > div > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(2)"
image_2_locator = "div.css-1uhvlas > div:nth-child(2) > div.css-hoyejk > div > div:nth-child(3) > div > div:nth-child(2)> div:nth-child(1) > div > div > div:nth-child(2)"
video_1_locator = "div.css-1uhvlas > div:nth-child(2) > div.css-hoyejk > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(2)"


def login_and_get_page(login_page, login_name, email, password):
    leonardo_page = login_page(login_name)
    leonardo_page.page.get_by_role("button", name="Microsoft").click()
    leonardo_page.page.get_by_test_id("i0116").click()
    leonardo_page.page.get_by_test_id("i0116").fill(password)
    leonardo_page.page.get_by_test_id("i0116").dblclick()
    leonardo_page.page.get_by_test_id("i0116").press("Meta+a")
    leonardo_page.page.get_by_test_id("i0116").fill(email)
    leonardo_page.page.get_by_role("button", name="Next").click()
    leonardo_page.page.get_by_test_id("i0118").fill(password)
    leonardo_page.page.get_by_role("button", name="Sign in").click()
    leonardo_page.page.get_by_label("Stay signed in?").click(timeout=15000)
    time.sleep(3)
    if (
        leonardo_page.page.locator(
            '[placeholder="myawesomeusername"]',
        ).count()
        <= 0
    ):
        leonardo_page.page.goto("https://app.leonardo.ai/settings/account-management")
        leonardo_page.page.get_by_label("Close", exact=True).click()
        leonardo_page.page.get_by_role("button", name="Delete Account").click()
        name = leonardo_page.page.inner_text("p.chakra-text > span")
        leonardo_page.page.get_by_role("textbox").fill(name)
        leonardo_page.page.get_by_role("button", name="Delete My Account").click()
        leonardo_page.page.get_by_role("button", name="Sign in").wait_for(
            state="visible", timeout=6000
        )
        leonardo_page.page.get_by_role("button", name="Microsoft").click()
        time.sleep(3)
    leonardo_page.page.get_by_placeholder("myawesomeusername").click()
    leonardo_page.page.get_by_placeholder("myawesomeusername").fill(login_name)
    leonardo_page.page.get_by_role("button", name="advertising").click()
    return leonardo_page


def configure_image_settings(leonardo_page):
    leonardo_page.page.get_by_role("dialog", name="Welcome to Leonardo.Ai").locator(
        "span"
    ).nth(1).click()
    leonardo_page.page.get_by_role("button", name="Next").click()
    if leonardo_page.page.get_by_label("Close", exact=True).is_visible():
        leonardo_page.page.get_by_label("Close", exact=True).click()
    leonardo_page.page.get_by_role("link", name="Create New Image").click()
    leonardo_page.page.get_by_label("Close").nth(3).click()
    leonardo_page.page.get_by_text("1", exact=True).click()
    leonardo_page.page.get_by_role("button", name="3:2").click()
    leonardo_page.page.get_by_role("menuitem", name="16:9").click()
    leonardo_page.page.locator("div").filter(
        has_text=re.compile(r"^AlchemyV2Loading\.\.\.$")
    ).locator("span").nth(3).click()


def generate_and_download_video(
    leonardo_page, prompt, file_suffix, image_locator, save_dir
):
    leonardo_page.page.get_by_placeholder("Type a prompt ...").click()
    leonardo_page.page.get_by_placeholder("Type a prompt ...").fill(prompt)
    leonardo_page.page.get_by_role("button", name="Generate 2").click()
    image = leonardo_page.page.locator(image_locator)
    image.wait_for(state="visible", timeout=20000)
    image.hover()
    image.get_by_label("Generate Motion video").click()
    leonardo_page.page.locator(
        "footer > div > button.chakra-button.css-17emeou"
    ).click()
    video = leonardo_page.page.locator(
        "div.css-1uhvlas > div:nth-child(2) > div.css-hoyejk > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(2)"
    )
    video.wait_for(state="visible", timeout=600000)
    video.hover()
    leonardo_page.page.locator(
        "div.css-1uhvlas > div:nth-child(2) > div.css-hoyejk > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(1)"
    ).hover()
    Path(SAVE_PATH + save_dir + "/").mkdir(parents=True, exist_ok=True)

    with leonardo_page.page.expect_download() as download_info:
        leonardo_page.page.locator(
            "div.css-1uhvlas > div:nth-child(2) > div.css-hoyejk > div > div:nth-child(3) > div > div:nth-child(2) > div:nth-child(1) > div > div > div.css-1lpsa6b > div.css-1sg7dwz> div > button"
        ).click()

    download = download_info.value
    download.save_as(os.path.join(save_dir, file_suffix))


@pytest.mark.parametrize("prompt,file_suffix,dir", killers)
def test_leonardo_0(login_page, pages_manager, prompt, file_suffix, dir):
    login_name = uuid4().hex[:8]
    leonardo_page = login_and_get_page(login_page, login_name, EMAIL_1, PASSWORD_1)
    configure_image_settings(leonardo_page)
    # Generate and download videos
    generate_and_download_video(
        leonardo_page,
        prompt=prompt,
        file_suffix=f"{file_suffix}_{uuid4().hex[:8]}.mp4",
        image_locator=image_1_locator,
        save_dir=dir,
    )
    generate_and_download_video(
        leonardo_page,
        prompt=prompt,
        file_suffix=f"{file_suffix}_{uuid4().hex[:8]}.mp4",
        image_locator=image_2_locator,
        save_dir=dir,
    )
    generate_and_download_video(
        leonardo_page,
        prompt=prompt,
        file_suffix=f"{file_suffix}{uuid4().hex[:8]}.mp4",
        image_locator=image_2_locator,
        save_dir=dir,
    )
    generate_and_download_video(
        leonardo_page,
        prompt=prompt,
        file_suffix=f"{file_suffix}{uuid4().hex[:8]}.mp4",
        image_locator=image_2_locator,
        save_dir=dir,
    )
    generate_and_download_video(
        leonardo_page,
        prompt=prompt,
        file_suffix=f"{file_suffix}{uuid4().hex[:8]}.mp4",
        image_locator=image_2_locator,
        save_dir=dir,
    )


@pytest.mark.parametrize("prompt ,file_suffix,dir", ghosts)
def test_leonardo_2(login_page, pages_manager, prompt, file_suffix, dir):
    login_name = uuid4().hex[:8]
    leonardo_page = login_and_get_page(login_page, login_name, EMAIL_2, PASSWORD_2)
    configure_image_settings(leonardo_page)
    # Generate and download videos
    generate_and_download_video(
        leonardo_page,
        prompt=prompt,
        file_suffix=f"{file_suffix}_{uuid4().hex[:8]}.mp4",
        image_locator=image_1_locator,
        save_dir=dir,
    )
    generate_and_download_video(
        leonardo_page,
        prompt=prompt,
        file_suffix=f"{file_suffix}_{uuid4().hex[:8]}.mp4",
        image_locator=image_2_locator,
        save_dir=dir,
    )
    generate_and_download_video(
        leonardo_page,
        prompt=prompt,
        file_suffix=f"{file_suffix}{uuid4().hex[:8]}.mp4",
        image_locator=image_2_locator,
        save_dir=dir,
    )
    generate_and_download_video(
        leonardo_page,
        prompt=prompt,
        file_suffix=f"{file_suffix}{uuid4().hex[:8]}.mp4",
        image_locator=image_2_locator,
        save_dir=dir,
    )
    generate_and_download_video(
        leonardo_page,
        prompt=prompt,
        file_suffix=f"{file_suffix}{uuid4().hex[:8]}.mp4",
        image_locator=image_2_locator,
        save_dir=dir,
    )


@pytest.mark.parametrize("prompt ,file_suffix, dir", graveyard)
def test_leonardo_3(login_page, pages_manager, prompt, file_suffix, dir):
    login_name = uuid4().hex[:8]
    leonardo_page = login_and_get_page(login_page, login_name, EMAIL_3, PASSWORD_3)
    configure_image_settings(leonardo_page)
    # Generate and download videos
    generate_and_download_video(
        leonardo_page,
        prompt=prompt,
        file_suffix=f"{file_suffix}_{uuid4().hex[:8]}.mp4",
        image_locator=image_1_locator,
        save_dir=dir,
    )
    generate_and_download_video(
        leonardo_page,
        prompt=prompt,
        file_suffix=f"{file_suffix}_{uuid4().hex[:8]}.mp4",
        image_locator=image_2_locator,
        save_dir=dir,
    )
    generate_and_download_video(
        leonardo_page,
        prompt=prompt,
        file_suffix=f"{file_suffix}{uuid4().hex[:8]}.mp4",
        image_locator=image_2_locator,
        save_dir=dir,
    )
    generate_and_download_video(
        leonardo_page,
        prompt=prompt,
        file_suffix=f"{file_suffix}{uuid4().hex[:8]}.mp4",
        image_locator=image_2_locator,
        save_dir=dir,
    )
    generate_and_download_video(
        leonardo_page,
        prompt=prompt,
        file_suffix=f"{file_suffix}{uuid4().hex[:8]}.mp4",
        image_locator=image_2_locator,
        save_dir=dir,
    )
