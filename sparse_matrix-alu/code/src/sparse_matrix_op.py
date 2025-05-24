import os

class SparseMatrix:
    def __init__(self, filepath=None, rows=0, cols=0):
        self.rows = rows
        self.cols = cols
        self.elements = {}  # stores non-zero elements as (row, col): value
        if filepath:
            self._load_from_file(filepath)

    def _strip_whitespace(self, line):
        return ''.join(c for c in line if not c.isspace())

    def _is_valid_integer(self, s):
        return s.lstrip('-').isdigit()

    def _parse_entry(self, line):
        if not line.startswith('(') or not line.endswith(')'):
            raise ValueError("Each entry must be enclosed in parentheses.")
        line = line[1:-1]  # remove parentheses
        parts = line.split(',')
        if len(parts) != 3:
            raise ValueError("Each entry must have exactly three parts: row, col, value")
        r, c, v = [p.strip() for p in parts]
        if '.' in r or '.' in c or '.' in v:
            raise ValueError("Matrix entries must be integers only")
        if not (self._is_valid_integer(r) and self._is_valid_integer(c) and self._is_valid_integer(v)):
            raise ValueError("Invalid integer values in entry")
        return int(r), int(c), int(v)

    def _load_from_file(self, filepath):
        try:
            with open(filepath, 'r') as f:
                lines = [self._strip_whitespace(line) for line in f if line.strip()]
            if len(lines) < 2:
                raise ValueError("File must contain at least two lines for rows and cols")
            if not lines[0].startswith('rows=') or not lines[1].startswith('cols='):
                raise ValueError("First two lines must define matrix dimensions")
            self.rows = int(lines[0][5:])
            self.cols = int(lines[1][5:])
            for line in lines[2:]:
                r, c, v = self._parse_entry(line)
                self.set_element(r, c, v)
        except Exception as e:
            raise ValueError(f"Error loading matrix from file {filepath}: {e}")

    def set_element(self, row, col, value):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError(f"Invalid index ({row}, {col}) for matrix size {self.rows}x{self.cols}")
        if value != 0:
            self.elements[(row, col)] = value
        elif (row, col) in self.elements:
            del self.elements[(row, col)]

    def get_element(self, row, col):
        return self.elements.get((row, col), 0)

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match for addition")
        result = SparseMatrix(rows=self.rows, cols=self.cols)
        for (r, c), v in self.elements.items():
            result.set_element(r, c, v + other.get_element(r, c))
        for (r, c), v in other.elements.items():
            if (r, c) not in self.elements:
                result.set_element(r, c, v)
        return result

    def __sub__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match for subtraction")
        result = SparseMatrix(rows=self.rows, cols=self.cols)
        for (r, c), v in self.elements.items():
            result.set_element(r, c, v - other.get_element(r, c))
        for (r, c), v in other.elements.items():
            if (r, c) not in self.elements:
                result.set_element(r, c, -v)
        return result

    def __matmul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions do not match for multiplication")
        result = SparseMatrix(rows=self.rows, cols=other.cols)
        for (r1, c1), v1 in self.elements.items():
            for c2 in range(other.cols):
                v2 = other.get_element(c1, c2)
                if v2 != 0:
                    curr = result.get_element(r1, c2)
                    result.set_element(r1, c2, curr + v1 * v2)
        return result

    def print_matrix(self):
        for r in range(self.rows):
            for c in range(self.cols):
                print(self.get_element(r, c), end=' ')
            print()

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(f"rows={self.rows}\n")
            f.write(f"cols={self.cols}\n")
            for (r, c), v in sorted(self.elements.items()):
                f.write(f"({r}, {c}, {v})\n")


def main():
    base_path = "/dsa-sparse_matrix-alu/sparse_matrix-alu/sample_inputs/"
    print("Sparse Matrix Operation Menu")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Exit")
    choice = input("Enter your choice (1/2/3/4): ")
    if choice not in ['1', '2', '3', '4']:
        print("Invalid choice.")
        return
    elif choice == '4':
        print("Exiting...")
        return

    file1 = input("Enter first matrix file name (e.g: easy_sample_03_1.txt): ")
    file2 = input("Enter second matrix file name (e.g: easy_sample_03_2.txt): ")
    path1 = os.path.join(base_path, file1)
    path2 = os.path.join(base_path, file2)

    try:
        matrix1 = SparseMatrix(filepath=path1)
        matrix2 = SparseMatrix(filepath=path2)
        result = None
        if choice == '1':
            result = matrix1 + matrix2
        elif choice == '2':
            result = matrix1 - matrix2
        elif choice == '3':
            result = matrix1 @ matrix2
        else:
            print("Invalid choice.")
            return

        result_filename = f"result_{file1.split('.')[0]}_{file2.split('.')[0]}.txt"
        result_path = os.path.join(base_path, result_filename)
        result.save_to_file(result_path)
        print(f"\n Operation successful. Result saved to: {result_path}")

        print("\n Result matrix:")
        result.print_matrix()

    except Exception as e:
        print(f" Error: {e}")



if __name__ == "__main__":
    main()
