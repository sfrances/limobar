#!/usr/bin/env python3

import time
import pyotp
import os

from AppKit import *
from Foundation import *
from PyObjCTools import AppHelper

# import tokens from a separate file to avoid hardcoding them in the main app code
import json
# check if the tokens.json file exists, if not exit
if not os.path.exists("tokens.json"):
    print("Error: tokens.json file not found. Please create it with your OTP tokens.")
    exit(1)
with open("tokens.json") as f:
    TOKENS = json.load(f)
    # check the format - it has to be a simple dictionary with string keys and values
    if not isinstance(TOKENS, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in TOKENS.items()):
        print("Error: tokens.json file format is invalid. It should be a dictionary with string keys and values.")
        exit(1)

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
        timer = NSTimer.timerWithTimeInterval_target_selector_userInfo_repeats_(
            1.0, self, "tick:", None, True)

        NSRunLoop.currentRunLoop().addTimer_forMode_(timer, NSRunLoopCommonModes)

    def tick_(self, timer):
        self.update_menu()

    def update_menu(self):

        # get how many seconds are left until the next code is generated
        time_left = PERIOD - (int(time.time()) % PERIOD)

        # check if menu items already exist, if not create them, otherwise update the existing ones
        nElements = self.menu.numberOfItems()
        if nElements == 0:
            for name, totp in self.totps.items():

                code = totp.now()

                item = self.create_totp_menu_item(
                        name,
                        code,
                        time_left / PERIOD,
                        self,
                        "copyCode:"
                    )

                self.menu.addItem_(item)

            # separator
            self.menu.addItem_(NSMenuItem.separatorItem())

            quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Quit", "quit:", "q")
            self.menu.addItem_(quit_item)
        else:
            # update the existing otp items (the first n-2)
            for index, (name, totp) in enumerate(self.totps.items()):

                code = totp.now()
                title = f"{name}: {code} ({time_left}s left)"

                # update the existing item
                item = self.menu.itemAtIndex_(index)
                item.setRepresentedObject_(code)
                item.setImage_(self.create_pie_image(time_left / PERIOD))

                # update the attributed title
                attributed_title = NSMutableAttributedString.alloc().init()

                name_part = NSAttributedString.alloc().initWithString_attributes_(
                    name + "\n",
                    {NSFontAttributeName: NSFont.boldSystemFontOfSize_(13)}
                )
                code_part = NSAttributedString.alloc().initWithString_attributes_(
                    code,
                    {NSFontAttributeName: NSFont.monospacedDigitSystemFontOfSize_weight_(13, NSFontWeightRegular)}
                )

                attributed_title.appendAttributedString_(name_part)
                attributed_title.appendAttributedString_(code_part)

                item.setAttributedTitle_(attributed_title)

    def copyCode_(self, sender):

        code = sender.representedObject()

        pasteboard = NSPasteboard.generalPasteboard()
        pasteboard.clearContents()
        pasteboard.setString_forType_(code, NSPasteboardTypeString)

        #print("Copied:", code)

    def quit_(self, sender):
        NSApplication.sharedApplication().terminate_(self)


    def create_totp_menu_item(self, name, code, fraction, target, action):

        item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(name, action, "")
        item.setTarget_(target)
        item.setRepresentedObject_(code)

        # ---- pie icon ----
        item.setImage_(self.create_pie_image(fraction))

        # ---- two-line attributed title: bold name / monospaced code ----
        attributed_title = NSMutableAttributedString.alloc().init()

        name_part = NSAttributedString.alloc().initWithString_attributes_(
            name + "\n",
            {NSFontAttributeName: NSFont.boldSystemFontOfSize_(13)}
        )
        code_part = NSAttributedString.alloc().initWithString_attributes_(
            code,
            {NSFontAttributeName: NSFont.monospacedDigitSystemFontOfSize_weight_(13, NSFontWeightRegular)}
        )

        attributed_title.appendAttributedString_(name_part)
        attributed_title.appendAttributedString_(code_part)

        item.setAttributedTitle_(attributed_title)

        return item
    
    def create_pie_image(self, fraction, size=18):

        image = NSImage.alloc().initWithSize_((size,size))
        image.lockFocus()

        center = size/2
        radius = size/2 - 1

        # background
        NSColor.quaternaryLabelColor().set()
        NSBezierPath.bezierPathWithOvalInRect_(NSMakeRect(0,0,size,size)).fill()

        # progress wedge
        NSColor.systemBlueColor().set()
        path = NSBezierPath.bezierPath()
        path.moveToPoint_((center,center))

        path.appendBezierPathWithArcWithCenter_radius_startAngle_endAngle_clockwise_(
            (center,center),
            radius,
            90,
            90 - 360*fraction,
            True
        )

        path.closePath()
        path.fill()

        image.unlockFocus()

        return image


if __name__ == "__main__":

    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)

    AppHelper.runEventLoop()