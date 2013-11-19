import time
import pytest
from unittestzero import Assert
from tests.ui import Base_UI_Test

@pytest.mark.usefixtures("maximized")
@pytest.mark.nondestructive
class Test_Navigation(Base_UI_Test):
    def test_tab_navigation(self, home_page_logged_in):
        home_pg = home_page_logged_in

        # FIXME - assert default active tab

        # Click through tabs
        for tab_name in ['Organizations', 'Users', 'Teams', 'Credentials', 'Projects', 'Inventories', 'Job Templates', 'Jobs']:
            org_pg = home_pg.header.site_navigation_menu(tab_name).click()
            assert org_pg.is_the_current_tab
