chars = "!" + '"' + "#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ "
Group1other = "!" + '"' + "#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
Group2_digits = "0123456789"
Group3_uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
Group4_lowercase = "abcdefghijklmnopqrstuvwxyz"

class String():
    def __init__(self, string="", rules=[]):
        super().__init__()
        self.string = string
        self.rules = rules
        self.group = self.findGroup()
        self.groupCurrentIndex = 0

    def __str__(self):
        return str(self.string)

    def list_to_string(self, lst):
        new_string=""
        for i in lst:
            new_string += i
        return new_string

    def __add__(self, other):
        return String(self.string + str(other))

    def __radd__(self, other):
        return String(other+str(self))

    def __eq__(self, other):
        return self.string == str(other)

    def __mul__(self, other):
        return String(self.string * int(other))

    def __rmul__(self, other):
        return String(str(self)+other)

    def __getitem__(self, item):
        return self.string.__getitem__(item)

    def len(self):
        return len(str(self))

    def __iter__(self):
        return self

    def count(self, x: str, __start: int = None, __end: int =None):
        return self.string.count(x, __start,__end)

    def isupper(self):
        return self.string.isupper()

    def islower(self):
        return self.string.islower()

    def base64(self) -> 'String':
        # convert string to 8 binary in list
        # converting list to sring
        # splits the string to 6 bit pieces and converting each piece to decimal
        # adding the last bits with zeroes and converting them to decimal
        # attaching the numbers to the base64 dictionary
        binary_lst = []
        dict_b64 = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I", 9: "J", 10: "K", 11: "L",
                    12: "M", 13: "N",
                    14: "O", 15: "P", 16: "Q", 17: "R", 18: "S", 19: "T", 20: "U", 21: "V", 22: "W", 23: "X", 24: "Y",
                    25: "Z",
                    26: "a", 27: "b", 28: "c", 29: "d", 30: "e", 31: "f", 32: "g", 33: "h", 34: "i", 35: "j", 36: "k",
                    37: "l", 38: "m", 39: "n", 40: "o", 41: "p", 42: "q", 43: "r", 44: "s", 45: "t", 46: "u", 47: "v",
                    48: "w", 49: "x",
                    50: "y", 51: "z", 52: "0", 53: "1", 54: "2", 55: "3", 56: "4"
            , 57: "5", 58: "6", 59: "7", 60: "8", 61: "9", 62: "+", 63: "/"}
        for i in self.string:
            binary_lst.append("".join(format(ord(i), '08b')))
        binary_word = self.list_to_string(binary_lst)
        new_letter = ''
        for i in range(len(binary_word) // 6):
            single_b64_letter = ''
            for k in range(6):
                single_b64_letter += binary_word[6 * i + k]
            deci = int(single_b64_letter, 2)
            new_letter += " " + str(deci)
        if len(binary_word) % 6 != 0:
            last_b64_letter = ''
            for j in range(1, 6, 1):
                if len(binary_word) % 6 == j:
                    last_b64_letter += binary_word[-j:] + (6 - j) * '0'
                    decim = int(last_b64_letter, 2)
                    new_letter += " " + str(decim)
        new_deci_list = list(new_letter.split(" "))
        value_list = []
        for i in new_deci_list:
            for k in range(0, 64):
                if str(k) == i:
                    value_list.append(dict_b64[k])
        new_string = self.list_to_string(value_list)
        return String(new_string)

        '''
        Encode the String (self) to a base64 string
        :return: a new instance of String with the encoded string.
        '''
        raise NotImplemented

    def byte_pair_encoding(self) -> 'String':
        rules=[]
        a = 2
        b = 3
        c = 4
        d = 5
        for i in self.string:
            if i in Group1other:
                a=1
            elif i in Group2_digits:
                b=1
            elif i in Group3_uppercase:
                c=1
            elif i in Group4_lowercase:
                d=1
            if a==b and b==c and c==d and d==a:
                raise BytePairError
        self.new_string=self.string
        while True:
            pairs = []
            # making the pairs
            for i in range(len(self.new_string)-1):
                if self.new_string[i]+self.new_string[i+1] not in pairs:
                    pairs.append(self.new_string[i] + self.new_string[i + 1])
            repetitions = {}
            # counting the pairs
            for i in pairs:
                count = self.new_string.count(i)
                repetitions.update({i: count})
            maximum_appearances = max(repetitions.values())
            repetitions_over_2 = {key: val for key, val in repetitions.items() if val > 1}
            if len(repetitions_over_2) == 0:
                return String(self.new_string, rules)
            repetitions = { key: val for key, val in repetitions.items() if val == maximum_appearances}
            lowest_pair = list(repetitions.keys())[0]
            replacement, new_rules = self.getReplacement(lowest_pair)
            rules.append(new_rules)
            self.new_string = self.new_string.replace(lowest_pair, replacement)
        # Encode the String (self) to a byte pair string
        # :return: a new instance of String with the encoded string.
        # :exception: BytePairError
        #
        # raise NotImplemented

    def getReplacement(self, old_pair):
        replacment = self.group[self.groupCurrentIndex]
        temp = ""
        self.groupCurrentIndex += 1
        dict={replacment: old_pair}
        for key, value in dict.items():
            temp = key +" = "+ value
        return (replacment, temp)

    def findGroup(self):
        if 0 == len(list(filter(lambda x: x in Group1other, self.string))):
            return Group1other
        elif 0 == len(list(filter(lambda x: x in Group2_digits, self.string))):
            return Group2_digits
        elif 0 == len(list(filter(lambda x: x in Group3_uppercase, self.string))):
            return Group3_uppercase
        else:
            return Group4_lowercase


    def cyclic_bits(self, num: int) -> 'String':
        binary_lst = []
        for i in self.string:
            binary_lst.append("".join(format(ord(i), '08b')))
        binary_word = self.list_to_string(binary_lst)
        new_binary_word = binary_word[num:] + binary_word[:num]
        new_word = ''
        for i in range(len(new_binary_word) // 8):
            single_binar_letter = ''
            for k in range(8):
                single_binar_letter += new_binary_word[8 * i + k]
            deci = int(single_binar_letter, 2)
            new_chr = chr(deci)
            new_word += new_chr
        return String(new_word)

        '''
        Encode the String (self) to a cyclic bits string
        :return: a new instance of String with the encoded string.
        '''
        raise NotImplemented

    def cyclic_chars(self, num: int) -> 'String':
        deci_list = []
        new_lst = []
        for i in self.string:
            if ord(i) < 32 or ord(i) > 126:
                raise CyclicCharsError
        for i in self.string:
            deci_number = ord(i)
            deci_list.append(deci_number)
        for new_deci_number in deci_list:
            new_deci_number += num
            while new_deci_number > 126:
                new_deci_number-=95
            asci_number = chr(new_deci_number)
            new_lst.append(asci_number)
        c = self.list_to_string(new_lst)
        return String(c.__str__())

        '''
        Encode the String (self) to a cyclic chars string
        :return: a new instance of String with the encoded string.
        :exception: CyclicCharsError
        '''
        raise NotImplemented

    def histogram_of_chars(self) -> dict:
        dict={}
        control_code_counter=0
        digits_counter = 0
        lower_case_counter = 0
        upper_case_counter = 0
        other_printable_counter = 0
        higher_that_128_counter = 0
        for i in self.string:
            if ord(i)<32 or ord(i)==127:
                control_code_counter+=1
            elif i in Group2_digits:
                digits_counter += 1
            elif i in Group3_uppercase:
                upper_case_counter += 1
            elif i in Group4_lowercase:
                lower_case_counter += 1
            elif ord(i)>127:
                higher_that_128_counter +=1
            else:
                other_printable_counter += 1
        dict['control_code_counter'] = control_code_counter
        dict['digits_counter'] = digits_counter
        dict['lower_case_counter'] = lower_case_counter
        dict['upper_case_counter'] = upper_case_counter
        dict['other_printable_counter'] = other_printable_counter
        dict['higher_that_128_counter'] = higher_that_128_counter
        return dict



        '''
        calculate the histogram of the String (self). The bins are
        "control code", "digits", "upper", "lower" , "other printable"
        and "higher than 128".
        :return: a dictonery of the histogram. keys are bins.
        '''
        raise NotImplemented

    def decode_base64(self) -> 'String':
        binary_list = []
        dict_b64 = {'000000': 'A', '000001': 'B', '000010': 'C', '000011': 'D', '000100': 'E',
                    '000101': 'F'
            , '000110': 'G', '000111': 'H', '001000': 'I', '001001': 'J', '001010': 'K', '001011': 'L', '001100': 'M',
                    '001101': 'N'
            , '001110': 'O', '001111': 'P', '010000': 'Q', '010001': 'R', '010010': 'S', '010011': 'T', '010100': 'U',
                    '010101': 'V'
            , '010110': 'W', '010111': 'X', '011000': 'Y', '011001': 'Z', '011010': 'a', '011011': 'b', '011100': 'c',
                    '011101': 'd'
            , '011110': 'e', '011111': 'f', '100000': 'g', '100001': 'h', '100010': 'i', '100011': 'j', '100100': 'k',
                    '100101': 'l'
            , '100110': 'm', '100111': 'n', '101000': 'o', '101001': 'p', '101010': 'q', '101011': 'r', '101100': 's',
                    '101101': 't'
            , '101110': 'u', '101111': 'v', '110000': 'w', '110001': 'x', '110010': 'y', '110011': 'z', '110100': '0',
                    '110101': '1'
            , '110110': '2', '110111': '3', '111000': '4', '111001': '5', '111010': '6', '111011': '7', '111100': '8',
                    '111101': '9'
            , '111110': '+', '111111': '/'}
        key_list = list(dict_b64.keys())
        val_list = list(dict_b64.values())
        for i in self.string:
            if i not in val_list:
                raise Base64DecodeError
        for i in self.string:
            for k in range(0, 64):
                if k == val_list.index(i):
                    binary_list.append(key_list[k])
        binary_string = self.list_to_string(binary_list)
        new_word = ''
        for i in range(len(binary_string) // 8):
            single_binar_letter = ''
            for k in range(8):
                single_binar_letter += binary_string[8 * i + k]
            deci = int(single_binar_letter, 2)
            new_chr = chr(deci)
            new_word += new_chr
        return String(new_word)

        # convert string to 8 binary in list
        # converting list to sring
        # splits the string to 6 bit pieces and converting each piece to decimal
        # adding the last bits with zeroes and converting them to decimal
        # attaching the numbers to the base64 dictionary
        '''
        Decode the String (self) to its original base64 string.
        :return: a new instance of String with the endecoded string.
        :exception: Base64DecodeError
        '''


    def decode_byte_pair(self) -> 'String':
        if len(self.rules)==0:
            raise BytePairDecodeError("rules list is empty")
        reversed_rules = sorted(self.rules, reverse=True)
        string=self.string
        new_string = string
        for i in reversed_rules:
            for j in new_string:
                if i[0] == j:
                    new_string=string.replace(j, i[-2:])
                    string = new_string
        return String(string)


        '''
        Decode the String (self) to its original byte pair string.
        Uses the property rules.
        :return: a new instance of String with the endecoded string.
        :exception: BytePairDecodeError
        '''
        raise NotImplemented

    def decode_cyclic_bits(self, num: int) -> 'String':
        binary_lst = []
        for i in self.string:
            binary_lst.append("".join(format(ord(i), '08b')))
        binary_word = self.list_to_string(binary_lst)
        new_binary_word = binary_word[(-num):] + binary_word[:(-num)]
        new_word = ''
        for i in range(len(new_binary_word) // 8):
            single_binar_letter = ''
            for k in range(8):
                single_binar_letter += new_binary_word[8 * i + k]
            deci = int(single_binar_letter, 2)
            new_chr = chr(deci)
            new_word += new_chr
        return String(new_word)

        '''
        Decode the String (self) to its original cyclic bits string.
        :return: a new instance of String with the endecoded string.
        '''
        raise NotImplemented

    def decode_cyclic_chars(self, num: int) -> 'String':
        deci = []
        new_lst = []
        for i in self.string:
            if ord(i) < 32 or ord(i) > 126:
                raise CyclicCharsDecodeError
        for i in self.string:
            a = ord(i)
            deci.append(a)
        for new_deci_number in deci:
            new_deci_number -= num
            while new_deci_number<32:
                new_deci_number+=95
            asci_number = chr(new_deci_number)
            new_lst.append(asci_number)
        c = self.list_to_string(new_lst)
        return String(c.__str__())
        '''
        Decode the String (self) to its original cyclic chars string.
        :return: a new instance of String with the endecoded string.
        :exception: CyclicCharsDecodeError
        '''
        raise NotImplemented


class Base64DecodeError(Exception):
    pass


class CyclicCharsError(Exception):
    pass


class CyclicCharsDecodeError(Exception):
    pass


class BytePairDecodeError(Exception):
    pass


class BytePairError(Exception):
    pass



