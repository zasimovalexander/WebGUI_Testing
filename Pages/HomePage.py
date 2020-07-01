import Pages.basePage as basePage


class Home(basePage.Base):
    Parameters = ('https://ivypanda.com',
                  '≡ Ivypanda - 24/7 Homework Help | Free Essays | Study Hub',
                  ((basePage.By.XPATH, '/html/body/div[2]/main/section[1]/div/h1'),
                   'Need help with a college/uni task?'))
    Slider = {'Slick': (basePage.By.XPATH, '/html/body/div[2]/main/section[2]'),
              'Arrow_right': (basePage.By.XPATH, '//*[@id="slickProcess"]/button[2]'),
              'Arrow_left': (basePage.By.XPATH, '//*[@id="slickProcess"]/button[1]'),
              'Image_1': (basePage.By.XPATH, '//*[@id="slickProcess"]/div/div/div[2]'),
              'Image_2': (basePage.By.XPATH, '//*[@id="slickProcess"]/div/div/div[3]'),
              'Image_3': (basePage.By.XPATH, '//*[@id="slickProcess"]/div/div/div[4]'),
              'Image_4': (basePage.By.XPATH, '//*[@id="slickProcess"]/div/div/div[5]'),
              'Image_class': {'active': 'slick-process__item slick-slide slick-current slick-active'}}
