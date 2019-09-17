import string

class Convert:
    
    def __init__(self):
        self.chars = string.digits + string.ascii_uppercase
        self.chars_len = len(self.chars)

    def print(self):
        print(self.chars)
        print(self.chars_len)

    def num2dec(self, num):
        num = str(num)
        num_len = len(num)
        dec = 0
        for i in range(num_len):
            tmp = self.get_nth_of_digit(num[i]) * pow(self.chars_len, num_len-i-1)
            dec = dec + tmp
        return dec

    def dec2num(self, dec):
        dec = int(dec)
        num = ''
        while dec > 0:
            tmp = dec % self.chars_len
            num = str(self.chars[tmp]) + num
            dec = dec - tmp
            dec = int(dec / self.chars_len)
        return num

    def get_nth_of_digit(self, digit):
        for i in range(self.chars_len):
            if self.chars[i] == digit:
                return i
        return -1

    def dec2num_n_digit(self, dec, n):
        num = self.dec2num(dec)
        n = int(n)
        while len(num) < n:
            num = "0" + num
        return num

    def max_dec_from_n_digit(self, n):
        return pow(self.chars_len, int(n))

    # def check(self):
    #     max_num = pow(self.chars_len, 4)
    #     print(max_num)
    #     print('START')
    #     for i in range(max_num):
    #         a = i
    #         b = self.dec2num(a)
    #         c = self.dec2num_4digit(a)
    #         d = self.num2dec(b)
    #         e = self.num2dec(c)
    #         if a != d or d != e:
    #             print(a, b, c, d, e, sep='\t')
    #         if i < 100:
    #             print(a, b, c, d, e, sep='\t')
    #     print('FINISH')
