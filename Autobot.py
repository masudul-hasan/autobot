from rich import print

from actions.action import CreateNewChangeRequest, CloseChangeRequest, CancelChangeRequests, ParserLDMA
from prettify import prettify_ldma
from prettify.driver_prettify import MenuLayout, get_menu_choice
from sys import exit

"""
Module Name: Autobot.py
----------------------
This is the main class for running the application. From here
all the functions can be called. This will be the user interface
from here. User's will choose the actions to do on BMC Remedy.

written by: jiaul_islam
"""


def main():
    """ The typical main function to start the program """
    try:
        while True:
            print(MenuLayout())
            choice: int = get_menu_choice()
            if choice == 1:
                # Create Change Request
                create = CreateNewChangeRequest()
                create.createRequest()
                create.tearDownDriver()
                break
            elif choice == 2:
                # Close Change Request
                close = CloseChangeRequest()
                close.closeRequest()
                close.tearDownDriver()
                break
            elif choice == 3:
                # Cancel Change Request
                cancel = CancelChangeRequests()
                cancel.cancelRequests()
                cancel.tearDownDriver()
                break
            elif choice == 0:
                break
    except KeyboardInterrupt:
        exit()


if __name__ == "__main__":
    main()
