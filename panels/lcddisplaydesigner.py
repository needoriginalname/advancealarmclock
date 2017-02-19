import math


class LCDDisplayDesigner:
    def __init__(self, max_width=20, top_left=None, top_right=None, bottom_left=None, bottom_right=None,
                 center_top=None, center_bottom=None, bottom=None, top=None):

        # check preconditions
        self._ensure_exclusive(top, center_top, [top_left, top_right], False)
        self._ensure_exclusive(bottom, center_bottom, [bottom_left, bottom_right], True)
        self.max_width = max_width

        self._top_left = None
        self._top_right = None
        self._center_top = None
        self._top = None
        self._bottom_left = None
        self._bottom_right = None
        self._center_bottom = None
        self._bottom = None

        if top_left:
            self.top_left = top_left
        if top_right:
            self.top_right = top_right
        if bottom_left:
            self.bottom_left = bottom_left
        if bottom_right:
            self.bottom_right = bottom_right
        if center_bottom:
            self.center_bottom = center_bottom
        if center_top:
            self.center_top = center_top
        if top:
            self.top = top
        if bottom:
            self.bottom = bottom

    @property
    def top_left(self):
        return self._top_left

    @top_left.setter
    def top_left(self, value):
        self._top_left = value
        self._center_top = None
        self._top = None

    @property
    def top_right(self):
        return self._top_right

    @top_right.setter
    def top_right(self, value):
        self._top_right = value
        self._center_top = None
        self._top = None

    @property
    def bottom_left(self):
        return self._bottom_left

    @bottom_left.setter
    def bottom_left(self, value):
        self._bottom_left = value
        self._center_bottom = None
        self._bottom = None

    @property
    def bottom_right(self):
        return self._bottom_right

    @bottom_right.setter
    def bottom_right(self, value):
        self._bottom_right = value
        self._center_bottom = None
        self._bottom = None

    @property
    def center_top(self):
        return self._center_top

    @center_top.setter
    def center_top(self, value):
        self._top_right = None
        self._top_left = None
        self._center_top = value
        self._top = None

    @property
    def center_bottom(self):
        return self._center_bottom

    @center_bottom.setter
    def center_bottom(self, value):
        self._bottom_right = None
        self._bottom_left = None
        self._center_bottom = value
        self._bottom = None

    @property
    def top(self):
        if self._top is not None:
            return self._top

        if self._center_top is not None:
            left_spacing, right_spacing = self._get_center_spacing(self.center_top)
            return " " * left_spacing + self.center_top + " " * right_spacing

        if self._top_left is not None or self._top_right is not None:
            return self._get_aligned_format(self.top_left, self.top_right)

        return ""

    @top.setter
    def top(self, value):
        self._top_right = None
        self._top_left = None
        self._center_top = None
        self._top = value

    @property
    def bottom(self):
        if self._bottom is not None:
            return self._bottom

        if self._center_bottom is not None:
            left_spacing, right_spacing = self._get_center_spacing(self.center_bottom)
            return " " * left_spacing + self.center_bottom + " " * right_spacing

        if self._bottom_left is not None or self._bottom_right is not None:
            return self._get_aligned_format(self.bottom_left, self.bottom_right)

        return ""

    @bottom.setter
    def bottom(self, value):
        self._bottom_right = None
        self._bottom_left = None
        self._center_bottom = None
        self._bottom = value

    @staticmethod
    def _ensure_exclusive(a, b, l, is_bottom):

        s = ""
        if is_bottom:
            s = "Only ether bottom_left and bottom_right, center_bottom, or bottom may be assigned"
        else:
            s = "Only ether top_left and top_right, center_top, or top may be assigned"
        has_content = False
        is_error = False

        if a is not None:
            has_content = True

        if b is not None:
            if not has_content:
                has_content = True
            elif has_content:
                is_error = True
        if l[0] is not None or l[1] is not None:
            if has_content:
                is_error = True

        if is_error:
            raise RuntimeError(s)

    def _get_center_spacing(self, center_text):
        n = (self.max_width - len(center_text)) / 2
        if n < 0:
            n = 0
        return math.ceil(n), math.floor(n)
        pass

    def _get_aligned_format(self, left_text, right_text):
        left_text = left_text if left_text is not None else ""
        right_text = right_text if right_text is not None else ""

        n = self.max_width - (len(left_text) + len(right_text))
        if n < 0:
            n = 0
        return left_text + " " * n + right_text

    def __str__(self):
        return "['" + self.top + "', '" + self.bottom + "']"

    def __getitem__(self, item):
        if item == 0:
            return self.top
        else:
            return self.bottom
