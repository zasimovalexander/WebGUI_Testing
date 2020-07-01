from time import sleep as pause
from pytest import skip
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as e_c
from selenium.common.exceptions import\
    TimeoutException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.common.by import By
# noinspection PyUnresolvedReferences
import tmp


class Options:
    browser = tmp.browser
    screensize = tmp.screensize
    path = tmp.path
    date_time = tmp.date_time
    cook = tmp.cook
    _messaging = {'flag': True,
                  'fail_info': '',
                  'mode': '(+) There is used the cooke mode (+)'}


class Base(Options):

    def __init__(self, wd):
        self.wd = wd
        self.wait = WebDriverWait(self.wd, 5)

    def _fail_info(self, module, value, exception):
        self._messaging['fail_info'] = '(+) "%s" method + "%s" value => "%s" (+)' % (module, value, exception)
        if self._messaging['flag']:
            print(self._messaging['fail_info'])
        else:
            self._messaging['flag'] = True

    def wait_until(self, method, value, name_add):
        element = None
        try:
            element = self.wait.until(method(*value))
        except TimeoutException:
            self._fail_info('.'.join((self.__module__, name_add)), value[-1], TimeoutException.__name__)
        return element

    def find(self, locator):
        return self.wait_until(e_c.presence_of_element_located, (locator,),
                               '.'.join((self.__class__.__name__, self.find.__name__)))

    def find_visible(self, locator):
        return self.wait_until(e_c.visibility_of_element_located, (locator,),
                               '.'.join((self.__class__.__name__, self.find_visible.__name__)))

    def find_invisible(self, locator):
        return self.wait_until(e_c.invisibility_of_element_located, (locator,),
                               '.'.join((self.__class__.__name__, self.find_invisible.__name__)))

    def find_and_click(self, locator):
        status = False
        element = self.wait_until(e_c.element_to_be_clickable, (locator,),
                                  '.'.join((self.__class__.__name__, self.find_and_click.__name__)))
        if element:
            try:
                element.click()
                try:  # knowing about a new window allows will made logical branching, instead a wait and an intercept
                    WebDriverWait(self.wd, 1).until(e_c.number_of_windows_to_be(2))
                    self.wd.close()
                    self.wd.switch_to_window(self.wd.window_handles[-1])
                except TimeoutException:
                    pass
                status = True
            except ElementClickInterceptedException:
                self._fail_info('.'.join((self.__module__, self.__class__.__name__, self.find_and_click.__name__)),
                                locator, ElementClickInterceptedException.__name__)
            except ElementNotInteractableException:
                self._fail_info('.'.join((self.__module__, self.__class__.__name__, self.find_and_click.__name__)),
                                locator, ElementNotInteractableException.__name__)
        return status

    def scrolling(self, element, position):
        ActionChains(self.wd).move_to_element(element).click_and_hold().move_by_offset(*position).release().perform()
        pause(0.5)

    def wait_attribute_is(self, element, attr_name, value):
        try:
            return self.wait.until(lambda it_self_wd: element.get_attribute(attr_name) == value)
        except TimeoutException:
            return False

    def url(self, url):
        return self.wait_until(e_c.url_matches, (url,), '.'.join((self.__class__.__name__, self.url.__name__)))

    def title(self, title):
        return self.wait_until(e_c.title_is, (title,), '.'.join((self.__class__.__name__, self.title.__name__)))

    def text(self, text):
        return self.wait_until(e_c.text_to_be_present_in_element, text,
                               '.'.join((self.__class__.__name__, self.text.__name__)))

    def link_check(self, data):
        status = True
        for pair in ((self.url, data[0]), (self.title, data[1]), (self.text, data[2])):
            if not pair[0](pair[1]):
                status = False
                break
        return status

    def load_and_valid_page(self, data):
        self.wd.get(data[0])
        return self.link_check(data)

    def smoke_load_and_valid_page(self, data):
        self.wd.get(data[0])
        self._messaging['flag'] = False
        if not self.link_check(data):
            self.stopping(self._messaging['fail_info'])
        else:
            self._messaging['flag'] = True

    def cookies_activate(self):
        self._messaging['flag'] = False
        if not self.find_and_click(self.Cookies['Ok_button']):
            self.stopping(self._messaging['fail_info'])
        else:
            self._messaging['flag'] = True

    def stopping(self, message):
        self.wd.quit()
        skip(message)

    def screen_shot(self, module_name, class_name, test_name):
        self.wd.get_screenshot_as_file('%s\\%s__%s__%s__%s-%s-%s.png'
                                       % ('\\'.join(self.path), self.date_time, self.wd.name.title(), self.cook[1],
                                          module_name, class_name, test_name))

    Cookies = {'Popup': (By.ID, 'cookie-popup'),
               'Policy': (By.ID, 'cookie-popup-link'),
               'Policy_page': ('https://ivypanda.com/privacy-policy#cookie-policy',
                               'IvyPanda | Privacy Policy | Cookies Policy',
                               ((By.ID, 'cookie-policy'), 'Cookie Policy')),
               'Ok_button': (By.ID, 'cookie-popup-button'),
               'Popup_class': {'before_ok': 'cookie-popup cookie-popup--showed',
                               'after_ok': 'cookie-popup'}}
    About = {'About': (By.XPATH, '//*[@id="header-wrapper"]/div/nav/div[1]/ul[2]/li[1]'),
             'About_page': ('https://ivypanda.com/about-us',
                            'IvyPanda | About Us | 24/7 Homework Help, Free Essays',
                            ((By.XPATH, '/html/body/div[3]/main/section[1]/div/h1'),
                             'Just Because We are the Best'))}

    Contact = {'Contact': (By.XPATH, '//*[@id="header-wrapper"]/div/nav/div[1]/ul[2]/li[2]'),
               'Contact_page': ('https://ivypanda.com/contact',
                                'IvyPanda | Contact Us | 24/7 Homework Help, Free Essays',
                                ((By.XPATH, '/html/body/div[3]/main/section[2]/h2'),
                                 'Customers Support'))}

    Hamburger = {'Toggle': (By.ID, 'header-toggle'),
                 'Body': (By.XPATH, '/html/body'),
                 'Body_class': {'is': 'main overflow-hidden',
                                'no': 'main'},
                 'Tools': (By.ID, 'drop-down-toggle'),
                 'Tools_ddm_list': (By.XPATH, '//*[@id="header-wrapper"]/div/nav/div[1]/ul[1]/li[4]/div/div/div'),
                 'Tools_class': {'closed': 'header__nav-link header__nav-link--drop-down',
                                 'dropped': 'header__nav-link header__nav-link--drop-down header__nav-link--drop-down--'
                                            'open'}}
