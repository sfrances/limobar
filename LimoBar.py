#!/usr/bin/env python3

import time
import pyotp

from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper

# import tokens from a separate file to avoid hardcoding them in the main app code
import json
with open("tokens.json") as f:
    TOKENS = json.load(f)

PERIOD = 30

class AppDelegate(NSObject):

    def applicationDidFinishLaunching_(self, notification):

        self.totps = {name: pyotp.TOTP(secret) for name, secret in TOKENS.items()}

        self.status_item = NSStatusBar.systemStatusBar().statusItemWithLength_(NSVariableStatusItemLength)
        self.status_item.button().setTitle_("🍋")

        self.menu = NSMenu.alloc().init()
        self.status_item.setMenu_(self.menu)

        self.update_menu()

        # refresh every second and update the text of the menu items
        NSTimer.scheduledTimerWithTimeInterval_target_selector_userInfo_repeats_(
            1.0, self, "tick:", None, True
        )

    def tick_(self, timer):
        self.update_menu()

    def update_menu(self):

        self.menu.removeAllItems()

        # get how many seconds are left until the next code is generated
        time_left = PERIOD - (int(time.time()) % PERIOD)
        #print(f"Time left: {time_left}s")

        for name, totp in self.totps.items():

            code = totp.now()

            item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                f"{name}: {code} ({time_left}s left)",
                "copyCode:",
                ""
            )

            item.setRepresentedObject_(code)
            self.menu.addItem_(item)

        self.menu.addItem_(NSMenuItem.separatorItem())

        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Quit", "quit:", "q")
        self.menu.addItem_(quit_item)

    def copyCode_(self, sender):

        code = sender.representedObject()

        pasteboard = NSPasteboard.generalPasteboard()
        pasteboard.clearContents()
        pasteboard.setString_forType_(code, NSPasteboardTypeString)

        print("Copied:", code)

    def quit_(self, sender):
        NSApplication.sharedApplication().terminate_(self)


if __name__ == "__main__":

    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)

    AppHelper.runEventLoop()