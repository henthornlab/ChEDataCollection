"""
Class LabArea
These are the permitted areas that can be queried.
"""


class LabArea:
    def __init__(self, area_num):
        # These are the permitted areas. Add them as a key pair with area number:search term
        # For example, all tags on area 150 would fit the pattern of *150*, so the key pair is '150':'*150*'
        self.allowed_areas = {'100': '*100*', '150': '*150*', '200': '*200*', '250': '*250*', '300': '*-3*',
                              '400': '*400*', '500': '*500*', '525': '*525*', '600': '*600*', '650': '*650*',
                              '700': '*700*', '800': '*800*'}

        self.search_term = self.allowed_areas.get(area_num)
        if self.search_term is None:
            self.allowed = False
        else:
            self.allowed = True
        return
