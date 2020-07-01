from os import listdir
from pytest import mark


@mark.hookwrapper
def pytest_runtest_makereport(item):  # for name in dir(item): print(name, eval('item.'+name))
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call':
        plugin_html = item.config.pluginmanager.getplugin('html')
        extra = getattr(report, 'extra', [])
        file_name = report.nodeid.split('::')
        file_name[0] = file_name[0][6:-3]
        if report.failed:
            item.instance.home_page.screen_shot(file_name[0], file_name[1], file_name[2]+'-FAIL')
        file_name = '%s__%s__%s__%s' % (item.instance.home_page.date_time, item.instance.wd.name.title(),
                                        item.instance.home_page.cook[1], '-'.join(file_name))
        file_list = listdir('\\'.join(item.instance.home_page.path))
        if len(file_list):
            file_list.reverse()
            for file in file_list:
                if file_name in file:
                    extra.append(plugin_html.extras.html('<div class="image" style="width:200px;">'
                                                         '<h4>%s</h4>'
                                                         '<a href="%s/%s">'
                                                         '<img src="%s/%s" style="width:200px;"'
                                                         '/></a></div>'
                                                         % (file.split('--')[-1][:-4],
                                                            item.instance.home_page.path[2], file,
                                                            item.instance.home_page.path[2], file)))
            report.extra = extra
