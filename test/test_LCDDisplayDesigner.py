from unittest import TestCase
from panels.lcddisplaydesigner import LCDDisplayDesigner
import math


class TestLCDDisplayDesigner(TestCase):

    def test_direct_setting(self):
        n = "a"
        n2 = "a2"

        lcd = LCDDisplayDesigner(top=n, bottom=n2)
        self.assertEqual(lcd.top, n)
        self.assertEqual(lcd.bottom, n2)

    def test_direct_empty(self):
        n = ""
        n2 = ""
        lcd = LCDDisplayDesigner(top=n, bottom=n2)
        self.assertEqual(lcd.top, n)
        self.assertEqual(lcd.bottom, n2)

    def test_direct_none(self):
        n = None
        n2 = None
        lcd = LCDDisplayDesigner(top=n, bottom=n2)
        self.assertEqual(lcd.top, "")
        self.assertEqual(lcd.bottom, "")

    def test_center_empty(self):
        n = ""
        n2 = ""
        lcd = LCDDisplayDesigner(center_top=n, center_bottom=n2)
        self.assertEqual(lcd.top, "")
        self.assertEqual(lcd.bottom, "")

    def test_center_single(self):
        n = "a"
        n2 = "bc"
        lcd = LCDDisplayDesigner(center_top=n, center_bottom=n2)
        na = math.ceil((lcd.max_width - len(n)) / 2)
        nb = math.floor((lcd.max_width - len(n))/2)
        nc = math.ceil((lcd.max_width - len(n2)) / 2)
        nd = math.floor((lcd.max_width - len(n2))/2)
        self.assertEqual(lcd.top, " "*na + n + " "*nb)
        self.assertEqual(lcd.bottom, " "*nc + n2 + " "*nd)


    def test_combo(self):
        n = "test"
        b1 = "a"
        b2 = "b"
        lcd = LCDDisplayDesigner(center_top=n, bottom_left=b1, bottom_right=b2)
        topSpaceA = math.ceil((lcd.max_width - len(n))/2)
        topSpaceB = math.floor((lcd.max_width - len(n))/2)
        bottomSpace = lcd.max_width - len(b1) - len(b2)
        self.assertEqual(lcd.top, " "*topSpaceA + n + " "*topSpaceB)
        self.assertEqual(lcd.bottom, b1 + " "* bottomSpace + b2)


    def test_access(self):
        n="t"
        lcd = LCDDisplayDesigner(center_top=n, bottom_left=n, bottom_right=n)
        topleft_space = math.ceil((lcd.max_width - len(n))/2)
        topright_space = math.floor((lcd.max_width - len(n))/2)
        bottom_space = lcd.max_width - len(n)*2
        self.assertEqual(lcd[0], " "*topleft_space + n + " "*topright_space)
        self.assertEqual(lcd[1], n+" "*bottom_space+n)
