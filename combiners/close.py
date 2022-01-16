from rich.live import Live
from selenium.webdriver.chrome.webdriver import WebDriver

from pages.base import BasePage
from pages.closerequest import CloseRequests
from pages.createrequest import CreateRequests
from pages.home import HomePage
from pages.login import LoginPage
from prettify.close_prettifier import ClosePrettify
from utilites import make_data
from utilites.static_data import StaticData


class Close(BasePage):
    def __init__(self, driver: WebDriver):
        """ Close NCR E2E Actions """
        super().__init__(driver)
        self.login_page = LoginPage(self._driver)
        self.home_page = HomePage(self._driver)
        self.close_requests = CloseRequests(self._driver)
        self.create_requests = CreateRequests(self.close_requests._driver)

    def closeRequest(self):
        # Login to the Page
        self.login_page.enter_username_textbox()
        self.login_page.enter_password_textbox()
        self.login_page.click_login_button()
        # Parse all the change number from home page
        all_changes_list = self.home_page.get_all_change_numbers()
        # Parse all the closing change request shared by user
        user_list_for_close = make_data.list_of_change(StaticData.CLOSE_CHANGE_TXT_FILE_PATH)
        tasks = len(user_list_for_close)
        ClosePrettify.make_layout()
        ClosePrettify.make_table()
        my_progress = ClosePrettify.progress_bar(tasks)
        ClosePrettify.merge_layout(my_progress, ClosePrettify.get_table())
        # Iterate through each user shared Change Number
        with Live(ClosePrettify.get_layout(), refresh_per_second=5, vertical_overflow="visible") as live:
            for job in my_progress.tasks:
                for _index, a_change in enumerate(user_list_for_close):
                    if a_change in all_changes_list:
                        # get the Index number for the change calculated by algorithm get_index_for_change()
                        index = self.close_requests.get_index_for_change_number(a_change, all_changes_list)
                        if index is not None:
                            # Select the change request shared by user
                            self.close_requests.find_the_change_request(a_change, index)
                            if not self.close_requests.is_change_status_closed():
                                # check if Change is opened
                                if not self.close_requests.is_status_scheduled_for_approval():
                                    # check if Change is Scheduled for approval
                                    actual_open_time = self.close_requests.get_actual_start_date()
                                    if actual_open_time is not None:
                                        # make closing time depending on Actual Open Time
                                        # actual_closing_time = make_data.make_downtime_from_open_time(
                                            # actual_open_time)
                                        # Grab the current sys time
                                        current_sys_time = make_data.get_current_system_time()
                                        self.close_requests.goto_task_page()
                                        # Close the 2nd task
                                        self.close_requests.close_service_downtime_duration_task(actual_open_time)
                                        # Close the 3rd task
                                        self.close_requests.close_service_downtime_window_task(actual_open_time,
                                                                                               current_sys_time)
                                        # Close the 4th task
                                        self.close_requests.close_system_downtime_duration_task(actual_open_time)
                                        self.create_requests.go_back_to_homepage()
                                        ClosePrettify.add_row_table(str(_index + 1),
                                                                    self.close_requests.get_change_number(),
                                                                    "[green]SUCCESS")
                                        live.update(ClosePrettify.get_layout())
                                    else:
                                        self.close_requests.add_change_to_invalid_list(a_change)
                                        self.create_requests.go_back_to_homepage()
                                        ClosePrettify.add_row_table(
                                            str(_index + 1), self.close_requests.get_change_number(),
                                            "[red]NCR NOT OPENED")
                                        live.update(ClosePrettify.get_layout())
                                else:
                                    self.close_requests.add_change_to_invalid_list(a_change)
                                    self.create_requests.go_back_to_homepage()
                                    ClosePrettify.add_row_table(
                                        str(_index + 1), self.close_requests.get_change_number(), "[red]SFA")

                                    live.update(ClosePrettify.get_layout())
                            else:
                                self.create_requests.go_back_to_homepage()
                                ClosePrettify.add_row_table(
                                    str(_index + 1), self.close_requests.get_change_number(), "[red]AC")
                                live.update(ClosePrettify.get_layout())
                        else:
                            self.close_requests.add_change_to_invalid_list(a_change)
                            ClosePrettify.add_row_table(
                                str(_index + 1), self.close_requests.get_change_number(), "[red]INVALID")
                            live.update(ClosePrettify.get_layout())
                    else:
                        self.close_requests.add_change_to_invalid_list(a_change)
                        ClosePrettify.add_row_table(
                            str(_index + 1), self.close_requests.get_change_number(), "[red]INVALID")
                        live.update(ClosePrettify.get_layout())
                if not job.finished:
                    my_progress.advance(job.id)

        self.home_page.click_logout_button()
