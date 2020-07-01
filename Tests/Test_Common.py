from pytest import mark, fixture
import Pages.HomePage as HomePage


class TestCookies:

    def setup_method(self):
        self.wd = HomePage.Home.browser()
        self.home_page = HomePage.Home(self.wd)
        self.home_page.smoke_load_and_valid_page(self.home_page.Parameters)

    def teardown_method(self):
        self.wd.quit()

    @mark.skipif(HomePage.Home.cook[0], reason=HomePage.Home._messaging['mode'])
    def test_policy(self):
        assert self.home_page.find_and_click(self.home_page.Cookies['Policy'])
        assert self.home_page.link_check(self.home_page.Cookies['Policy_page'])
        self.home_page.load_and_valid_page(self.home_page.Parameters)
        assert self.home_page.find_visible(self.home_page.Cookies['Popup'])
        assert self.home_page.find(self.home_page.Cookies['Popup']).get_attribute('className') == self.home_page\
            .Cookies['Popup_class']['before_ok']

    @mark.skipif(HomePage.Home.cook[0], reason=HomePage.Home._messaging['mode'])
    def test_cookies_ok(self):
        assert self.home_page.find_and_click(self.home_page.Cookies['Ok_button'])
        assert self.home_page.find_invisible(self.home_page.Cookies['Popup'])
        assert self.home_page.find(self.home_page.Cookies['Popup']).get_attribute('className') == self.home_page\
            .Cookies['Popup_class']['after_ok']


class TestHead:

    def setup_class(self):
        self.wd = HomePage.Home.browser()
        self.home_page = HomePage.Home(self.wd)
        self.wd.set_window_size(self.home_page.screensize[0], self.home_page.screensize[1])
        self.home_page.smoke_load_and_valid_page(self.home_page.Parameters)
        if self.home_page.cook[0]:
            self.home_page.cookies_activate()

    def teardown_class(self):
        self.wd.quit()

    @fixture()
    def settings(self, record_xml_attribute):
        record_xml_attribute('usermode', self.home_page.cook[1])
        self.home_page.load_and_valid_page(self.home_page.Parameters)

    def test_contact(self, settings):
        assert self.home_page.find_and_click(self.home_page.Contact['Contact'])
        assert self.home_page.link_check(self.home_page.Contact['Contact_page'])

    def test_about(self, settings):
        assert self.home_page.find_and_click(self.home_page.About['About'])
        assert self.home_page.link_check(self.home_page.About['About_page'])


class TestHeadHamburger:

    def setup_class(self):
        self.wd = HomePage.Home.browser()
        self.home_page = HomePage.Home(self.wd)
        self.wd.set_window_size(self.home_page.screensize[0]//2, self.home_page.screensize[1])
        self.home_page.smoke_load_and_valid_page(self.home_page.Parameters)
        if self.home_page.cook[0]:
            self.home_page.cookies_activate()

    def teardown_class(self):
        self.wd.quit()

    @fixture()
    def settings(self, record_xml_attribute):
        record_xml_attribute('user_mode', self.home_page.cook[1])
        self.home_page.load_and_valid_page(self.home_page.Parameters)
        self.home_page.find_and_click(self.home_page.Hamburger['Toggle'])

    def test_opened(self, settings):
        assert self.home_page.find(self.home_page.Hamburger['Body']).get_attribute('className') == self.home_page\
            .Hamburger['Body_class']['is']

    def test_exit(self, settings):
        assert self.home_page.find_and_click(self.home_page.Hamburger['Toggle'])
        assert self.home_page.find(self.home_page.Hamburger['Body']).get_attribute('className') == self.home_page\
            .Hamburger['Body_class']['no']

    def test_tools_menu(self, settings):
        assert self.home_page.find_and_click(self.home_page.Hamburger['Tools'])
        assert self.home_page.find_visible(self.home_page.Hamburger['Tools_ddm_list'])
        assert self.home_page.find(self.home_page.Hamburger['Tools']).get_attribute('className') == self.home_page\
            .Hamburger['Tools_class']['dropped']
        self.home_page.screen_shot(self.__module__, self.__class__.__name__, self.test_tools_menu.__name__+'-dropped')
        assert self.home_page.find_and_click(self.home_page.Hamburger['Tools'])
        assert self.home_page.find_invisible(self.home_page.Hamburger['Tools_ddm_list'])
        assert self.home_page.find(self.home_page.Hamburger['Tools']).get_attribute('className') == self.home_page\
            .Hamburger['Tools_class']['closed']
        self.home_page.screen_shot(self.__module__, self.__class__.__name__, self.test_tools_menu.__name__+'-closed')
