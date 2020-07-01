from pytest import fixture
import Pages.HomePage as HomePage


class TestHome:

    def setup_class(self):
        self.wd = self.wd = HomePage.Home.browser()
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

    def test_slick_arrow(self, settings):
        assert self.home_page.find(self.home_page.Slider['Slick']).location_once_scrolled_into_view
        images = [(self.home_page.Slider['Image_2'], 'image2'), (self.home_page.Slider['Image_3'], 'image3'),
                  (self.home_page.Slider['Image_4'], 'image4'), (self.home_page.Slider['Image_1'], 'image1')]
        i = 1
        for arrow in ((self.home_page.Slider['Arrow_right'], 'right'), (self.home_page.Slider['Arrow_left'], 'left')):
            for img in images:
                assert self.home_page.find_and_click(arrow[0])
                element = self.home_page.find_visible(img[0])
                assert element
                assert self.home_page.wait_attribute_is(element, 'className',
                                                        self.home_page.Slider['Image_class']['active'])
                self.home_page.screen_shot(self.__module__, self.__class__.__name__,
                                           self.test_slick_arrow.__name__+'-s%s-%s-%s' % (i, arrow[1], img[1]))
                i += 1
            images.reverse()
            images.append(images.pop(0))

    def test_slick_screen(self, settings):
        assert self.home_page.find(self.home_page.Slider['Slick']).location_once_scrolled_into_view
        images = [(self.home_page.Slider['Image_2'], 'image2'), (self.home_page.Slider['Image_3'], 'image3'),
                  (self.home_page.Slider['Image_4'], 'image4'), (self.home_page.Slider['Image_1'], 'image1')]
        element = self.home_page.find_visible(images[-1][0])
        offset = int(element.get_attribute('clientWidth')) // 4
        for orient in ((-1*offset, 'right'), (1*offset, 'left')):
            for img in images:
                self.home_page.scrolling(element, (orient[0], 0))
                element = self.home_page.find_visible(img[0])
                assert element
                assert self.home_page.wait_attribute_is(element, 'className',
                                                        self.home_page.Slider['Image_class']['active'])
            images.reverse()
            images.append(images.pop(0))
