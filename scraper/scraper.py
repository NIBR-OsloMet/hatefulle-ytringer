#!/usr/bin/env python3

from csv import writer, QUOTE_ALL
# from os import system
from random import seed, random, normalvariate
from re import findall
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep, time as t
from webdriver_manager.chrome import ChromeDriverManager

TARGET_URL                 = 'https://m.facebook.com/nrk/posts'
TIMEOUT                    = 5
SCROLLS                    = 10
SCROLL_DELAY_MEAN          = 1
SCROLL_DELAY_STDEV         = 0.2

ACCEPT_COOKIE_BUTTON_XPATH = '//button[@id="accept-cookie-banner-label"]'
STORY_XPATH                = '//article'
STORY_AUTHOR_XPATH         = './/header//h3//a'
STORY_ID_XPATH             = './/footer//a'
STORY_TIME_XPATH           = './/header//abbr'
STORY_TEXT_1_XPATH         = './/p'
STORY_TEXT_2_XPATH         = ''
STORY_LIKES_XPATH          = './/span[contains(@class, "like_def")]'
STORY_COMMENTS_XPATH       = './/span[contains(@class, "cmt_def")]'
STORY_SHARES_XPATH         = './/a[@data-sigil="feed-ufi-trigger"]/span[2]'

PLACEHOLDER                = 'n/a'

options = Options()
options.page_load_strategy = 'eager'
# options.add_argument('--headless')
options.add_experimental_option(
    'prefs',
    {
        'profile.managed_default_content_settings.ads'          : 2,
        'profile.managed_default_content_settings.images'       : 2,
        'profile.managed_default_content_settings.media_stream' : 2
    }
)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
wait = WebDriverWait(driver, TIMEOUT)

def delay():
    return normalvariate(SCROLL_DELAY_MEAN, SCROLL_DELAY_STDEV)

def main():
    urls = []
    with open('./urls.txt', 'r') as f:
        urls = f.readlines()

    i = 0
    urls = urls[i:]

    for url in urls:
        post_id = url.split('/')[5].strip()
        
        print('Gathering comments under post', i)
        i += 1

        try:
            driver.get(url)
        except:
            print('Could not load URL. Skipping story.')
            continue

        sleep(delay())
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        sleep(delay())
      
        # video posts are skipped
        try:
            # story = driver.find_element(By.XPATH, '//div[contains(@data-sigil, "story-div")]')
            story = driver.find_element(By.XPATH, '//div[@id="m_story_permalink_view"]')
        except:
            print('No comment container found. Skipping story.')
            continue
       
        try:
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@id="popup_xout"]')))
            button.click()
        except:
            pass
        
        # expand comments
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            try:
                see_prev_button = story.find_element(By.XPATH, './/div[@id="see_prev_' + post_id + '"]/a')
                see_prev_button.click()
                print('Expanding previous comments')
            except:
                pass
            try:
                see_next_button = story.find_element(By.XPATH, './/div[@id="see_next_' + post_id + '"]/a')
                see_next_button.click()
                print('Expanding next comments')
            except:
                pass
            
            sleep(delay())
        
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        sleep(delay())

        # extract fields
        comments = []
        try:
            # comments = top_post.find_elements(By.XPATH, './/div[@data-sigil="comment"]')
            comments = story.find_elements(By.XPATH, './/div[@data-sigil="comment"]')
        except:
            pass
        
        xpaths = {
            'comment_id' : './/div[@data-sigil="comment-body"]',
            'author'     : './div[2]/div/div/div',
            'time'       : './/abbr',
            'text'       : './/div[@data-sigil="comment-body"]',
            'answers'    : './/span[@class="_4ayk"]'
        }

        entries = []
        for comment in comments:
            entry = [post_id]
            for key in xpaths:
                xpath = xpaths[key]

                try:
                    element = comment.find_element(By.XPATH, xpath)

                    if key == 'comment_id':
                        data = element.get_attribute('data-commentid')
                    else:
                        data = element.text

                except:
                    data = PLACEHOLDER
                finally:
                    entry.append(data)
            
            entries.append(entry)

        # write to file
        
        with open('./comments.csv', 'a', newline = '', encoding = 'utf-8') as f:
            csv_writer = writer(f, quoting = QUOTE_ALL)
            csv_writer.writerows(entries)
        
        sleep(delay())
    
    driver.quit()

if __name__ == '__main__':
    main()
