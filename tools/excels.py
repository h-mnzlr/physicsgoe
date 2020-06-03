import xlrd
import numpy as np


class ExcelSheet:

    def __init__(self, file_name, **kwargs):
        """Initialises the ExcelSheet-Object by parsing the Sheet int a list.

        """
        try:
            sheet_index = kwargs['sheet_index']
        except KeyError:
            sheet_index = 0
        try:
            wb = xlrd.open_workbook(file_name)
        except FileNotFoundError:
            print(f'File {file_name} not found')
            raise FileNotFoundError

        sheet = wb.sheet_by_index(sheet_index)
        self.data = []

        for i in range(sheet.nrows):
            row = []
            for j, cell in enumerate(sheet.row_values(i)):
                row.append(cell)
            self.data.append(row)

    def __iter__(self):
        """Return the iterator of the raw data."""
        return iter(self.data)

    def iter_row(self, row_index):
        return iter(self.data[row_index])

    def iter_col(self, col_index):
        column = []
        for row in self.data:
            column.append(row[col_index])
        return iter(column)

    def get_data(self):
        return self.data

    # def get_box(self, col, row, shape):
    #     col, row = self.resolve_index([col, row])
    #     return self.data[row-1:shape[1]][-1]

    def get_float_box(self, c, r, **kwargs):
        """Return a numpy-array of float values with (c,r) top left corner."""
        c, r = self.resolve_index([c, r])
        start = self.get_cell_value_unresolved(c, r)
        if not isinstance(start, float):
            raise TypeError(f'{start} is not an float-Object.')
        shape = self.get_float_box_shape(c, r)
        # print(shape)
        f_box = np.zeros(shape, dtype=float)
        # print(f_box)
        for rnum in range(shape[0]):
            for cnum in range(shape[1]):
                try:
                    # print(self.get_cell_value_unresolved(
                        # c+cnum, r+rnum))
                    f_box[rnum, cnum] = self.get_cell_value_unresolved(
                        c+cnum, r+rnum)
                except TypeError:
                    print(f'\"{self.get_cell_value_unresolved(c+cnum, r+rnum)}\" cannot be converted to float')
                    f_box[rnum, cnum] = None
                except ValueError:
                    print(f'\"{self.get_cell_value_unresolved(c+cnum, r+rnum)}\" cannot be converted to float')
                    f_box[rnum, cnum] = None
        try:
            header_shape = [shape[0], 1]
            header_shape[1] = kwargs['header_shape']
            header = self.get_header(c, r, header_shape)
            return f_box, header
        except KeyError:
            return f_box

    def get_header(self, c, r, h_shape):
        print(h_shape)
        header = np.zeros(h_shape, dtype='<U32')
        for rnum in range(h_shape[1]):
            for cnum in range(h_shape[0]):
                header[cnum, rnum] = str(
                    self.get_cell_value_unresolved(c+cnum, r-1-rnum))
        return header

    def get_float_box_shape(self, c, r):
        start = self.get_cell_value_unresolved(c, r)
        val = start
        cnum = 0
        while isinstance(val, float):
            cnum += 1
            try:
                val = self.get_cell_value_unresolved(c+cnum, r)
            except IndexError:
                val = None
        val = start
        rnum = 0
        while isinstance(val, float):
            rnum += 1
            try:
                val = self.get_cell_value_unresolved(c, r+rnum)
            except IndexError:
                val = None
        return [rnum, cnum]

    def get_cell_value(self, c, r):
        c, r = self.resolve_index([c, r])
        return self.get_cell_value_unresolved(c, r)

    def get_cell_value_unresolved(self, c, r):
        # print(self.data[r-1][c-1])
        return self.data[r-1][c-1]

    def resolve_index(self, list):
        out = []
        for item in list:
            if isinstance(item, str):
                item_split = self.split_string_into_chars(item)
                i = self.char_to_alphabet_index(item_split[-1])
                for c in item_split[:-1]:
                    i += self.char_to_alphabet_index(c)*26
                out.append(i+1)
            elif isinstance(item, int):
                out.append(item)
            else:
                raise TypeError
        return out

    def split_string_into_chars(self, s):
        return [char for char in s]

    def char_to_alphabet_index(self, char):
        ascii_char = ord(char)
        if ascii_char >= 97 and ascii_char <= 122:
            return ascii_char-97
        elif ascii_char >= 65 and ascii_char <= 90:
            return ascii_char-65
        else:
            raise TypeError(f'{char} is not a valid character.')

    def __str__(self):
        s = ''
        for row in self.data:
            s += str(row[0])
            for cell in row[1:]:
                s += ',' + str(cell)
            s += '\n'
        return s


def main():
    es = ExcelSheet('Diffusion.xlsx')
    data = es.get_float_box('A', 8)
    print(data)


if __name__ == '__main__':
    main()
