# A twitter bot with python using the selenium library and GeckoDriver
# Based on Dev Ed's video tutorial (https://www.youtube.com/watch?v=7ovFudqFB0Q)
# Just a comment to test Git Bash commit
# Just a second somment to test Git Bash commit

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time,random

# Your login data and the keyword you want to search for in Twitter
username = "youraccount"
password = "yourpass"
searchTerm = "whatyouwannasearch"
sq=['comment text1','comment text2']


class TwitterBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        chrome_options=Options()
        chrome_options.add_argument('incognito')
        chrome_options.add_argument('disable-extensions')
        self.bot = webdriver.Chrome(chrome_options=chrome_options)
        self.bot.maximize_window()

    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/login')
        time.sleep(3)
        username = bot.find_element_by_name("session[username_or_email]")
        password = bot.find_element_by_name("session[password]")
        # If anything is written inside the login forms, erase it
        username.clear()
        password.clear()
        username.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)  # click the ENTER key to login
        time.sleep(5)
        loginError = bot.find_elements_by_xpath(
            "//span[contains(text(), 'match our records')]")  # not the best solution, sometimes works with few words
        time.sleep(5)
        if not loginError:
            print("Login Successful!")
            return True
        else:
            print("Your credentials were incorrect...\nBot is dead!")
            bot.close()
            return False
        print(loginError)
        time.sleep(5)

    # Scroll until the element we want to interact with (Like button, Retweet button, etc.) is inside the viewport

    def scroll_shim(self, passed_in_driver, object):
        x = object.location['x']
        y = object.location['y']
        scroll_by_coord = 'window.scrollTo(%s,%s);' % (
            x,
            y
        )
        scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
        passed_in_driver.execute_script(scroll_by_coord)
        passed_in_driver.execute_script(scroll_nav_out_of_way)

    def like_tweet(self, term):
        links = list()
        counter = 1  # count the retrieved tweets
        bot = self.bot
        bot.get('https://twitter.com/search?q=' + term + '&src=typd')
        time.sleep(5)

        # Loop how many times we scroll down and new tweets are loaded
        for i in range(1, 5):
            # The tweet's url can be found in several positions in the DOM
            # tree, we fetch it once from the anchor tag containing the
            # word "status" (ex. https://twitter.com/tweet_author_name/status/some_digits)
            tweets = bot.find_elements_by_css_selector(
                'a[href*="status"]:not([href*=photo]):not([href*=retweets]):not([href*=likes]):not([href*=media_tags])')
            time.sleep(2)

            # Get the tweet's actual url and store them in a list
            tempLoopLinks = [elem.get_attribute("href") for elem in tweets]
            for x in tempLoopLinks:
                links.append(x)
            time.sleep(2)
            print("Loop " + str(i) + " complete!")

            # Scroll down in order to load new tweets
            bot.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(10)

        # Locate and click the Like button
        links = list(dict.fromkeys(links))  # Remove duplicates
        for link in links:
            print(counter, link)
            bot.get(link)
            time.sleep(10)
            try:
                # Find the Like button
                # [aria-label="Like"]
                toLike = bot.find_element_by_css_selector(
                    'div[role="button"][data-testid="like"]')
                # print(toLike)
                time.sleep(5)

                # Scroll so that it is in our viewport
                if 'firefox' in bot.capabilities['browserName']:
                    self.scroll_shim(bot, toLike)
                
                actions = ActionChains(bot)
                actions.move_to_element(toLike)
                actions.click()
                # actions.move_to_element(toReply)
                # actions.click()
                # actions.move_to_element(cominput)
                # actions.click()
                # actions.send_keys('promotion: deposite 0.03BTC will get 1000bits(0.001btc) now!')
                # actions.move_to_element(replybutton)
                # actions.click()
                actions.perform()

                # Show a confirmation in console
                time.sleep(random.randint(0,4))
                toReply=bot.find_element_by_css_selector('div[aria-label="Reply"][role="button"][data-testid="reply"]').click()
                cominput=bot.find_element_by_css_selector('div[role="textbox"][data-testid="tweetTextarea_0"]').send_keys(random.choice(sq))
                replybutton=bot.find_element_by_css_selector('div[role="button"][data-testid="tweetButton"]').click()
                print("Gave a LIKE to tweet " + str(counter))
                time.sleep(5)
            except Exception as ex:
                # At the moment, an exception will be thrown
                # when a tweet is already liked
                print("Exception...sleeping for a bit...")
                print(ex)
                time.sleep(10)

            counter = counter + 1
            time.sleep(1)


# Our bot's name is bix
bix = TwitterBot(username, password)
loginSuccess = bix.login()
if loginSuccess:
    bix.like_tweet(searchTerm)
