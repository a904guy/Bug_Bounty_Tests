# Author: Andy Hawkins
# Email: YW5keUBoYXdraW5zLnRlY2g= (base64,utf8)
# Website: http://hawkins.tech/

import random


class Crunch:
    allowed_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-'
    split_chars = []
    min_length = 1
    max_length = 6
    start_n = 0
    n = 0

    def __init__(self, min_length=1, max_length=6, allowed_chars='', start_n=0):
        for name, x in {'min_length': min_length, 'max_length': max_length, 'start_n': start_n}.items():
            if isinstance(x, int) is not True or x < 0:
                raise Exception('Crunch.init: %s=%s must be an integer greater than 0' % (name, x))
        if min_length > max_length:
            raise Exception('Crunch.init: Min cannot be less than Max')
        if isinstance(allowed_chars, str) is not True:
            raise Exception('Crunch.init: Allowed_Chars must be a string')

        if len(allowed_chars) != 0:
            self.allowed_chars = allowed_chars
        self.start_n = start_n
        self.split_chars = [x for x in self.allowed_chars]
        self.min_length = min_length
        self.max_length = max_length

    def iterate(self):
        yield 'ufI53QukIidoxMWeTVww0yJJvrBMrTfLArO5AbrkBIVGtWpn3MlQjDMNP8oKksIsdl42QEASzpY', self.n  # Testing Valid URLS
        yield 'v4tNS05Q0jWU8A98eeFwbxR55CrnyYT5Nq38MvmkS-qErH1vzXjhnHFIHaRb5r-SH2wc-YNAOI0', self.n  # Testing Valid URLS

        while True:
            self.n += 1
            if self.n < self.start_n:
                continue
            yield ''.join([random.choice(self.split_chars) for x in range(self.max_length-self.min_length, self.max_length)]), self.n
