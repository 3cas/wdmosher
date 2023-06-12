import time
import random

DEBUG = False
STEP = False
LOG = None
FILE = None
FAKE_DIVIDER_SIZE = 35

def simple_hex(value: int) -> str:
    return hex(value)[2:].zfill(2)
    
def to_bytes(fill) -> bytes:
    if isinstance(fill, int):
        fill = chr(fill)
    if isinstance(fill, str):
        fill = bytes(fill, "UTF-8")
    if not isinstance(fill, bytes):
        raise TypeError("`fill` must be an int, str, or bytes")
    
    return fill

def replace_bytes(data: bytes, start_position: int, fill, *, skip_fail: bool = False) -> bytes:
        fill = to_bytes(fill)

        changed_data = data[:start_position] + fill + data[(start_position + len(fill)):]

        if len(changed_data) == len(data):
            return changed_data
            
        elif skip_fail:
            return data
        
        else:
            raise Exception("Size of fill exceeds length of data when applied to start position")

class Image:
    def __init__(self, filename: str, *, verbosity: int = 0):
        self.filename = filename
        self.verbosity = verbosity

        with open(self.filename, "rb") as f:
            self.data = f.read()

        self.moshable_start, self.moshable_end = self.find_moshable()
        self.moshable = self.data[self.moshable_start:(self.moshable_end+1)]

    def _log(self, message: str, level: int = 1):
        if self.verbosity >= level:
            print(message)

    def _apply_data(self):
        self.data = replace_bytes(self.data, self.moshable_start, self.moshable)
        
        self._log("Applied changed data to image", 2)

    def _write_data(self, filename: str):
        with open(filename, "wb") as f:
            f.write(self.data)
        
        self._log(f"Wrote changes to {filename}", 2)

    def find_moshable(self, data: bytes = None, *, step: bool = False) -> tuple:
        if not data:
            data = self.data

        real_streak = 0
        fake_streak = 0
        last_real = None
        current_block_first =  None
        largest_block_first = None
        largest_block_last = None

        for pos in range(len(data)):
            dec = data[pos]

            self._log(f"\npos: {pos}, dec: {dec}, hex: {simple_hex(dec)}", 3)

            if 32 <= dec <= 126:
                fake_streak = 0
                real_streak += 1
                last_real = pos

                if not current_block_first:
                    current_block_first = pos

                self._log("REAL", 3)

            else:
                real_streak = 0
                fake_streak += 1

                if current_block_first and fake_streak >= FAKE_DIVIDER_SIZE:
                    if (largest_block_first is None) or (largest_block_last-largest_block_first < last_real-current_block_first):
                        largest_block_first = current_block_first
                        largest_block_last = last_real

                    current_block_first = None

                self._log("FAKE", 3)

            self._log(f"real streak: {real_streak}", 3)
            self._log(f"fake streak: {fake_streak}", 3)
            if last_real: self._log(f"last real at {last_real}", 3)
            if current_block_first: self._log(f"current block started at {current_block_first}", 3)
            if largest_block_first: self._log(f"largest block from {largest_block_first} to {largest_block_last}", 3)

            if step: input("step>")

        if current_block_first and largest_block_first and (largest_block_last-largest_block_first < last_real-current_block_first):
            largest_block_first = current_block_first
            largest_block_last = last_real

        if largest_block_first is not None:
            preview = " ... ".join([" ".join([simple_hex(data[position]) for position in range(*do_range)]) for do_range in [(largest_block_first, largest_block_first+5), (largest_block_last-4, largest_block_last+1)]])
            self._log(f"Moshable data found from position {largest_block_first} to position {largest_block_last} and looks like {preview}", 1)
            return largest_block_first, largest_block_last

        else:
            self._log("Largest block not found! Setting general moshable data", 1)
            return 100, len(data)-1

    def replace_position(self, start_position: int, fill):
        self.moshable = replace_bytes(self.moshable, start_position, fill)
        
    def replace_position_random(self, fill):
        fill = to_bytes(fill)
        self.replace_position(random.randint(0, len(self.moshable)-len(fill)), fill)

    def find_replace(self, find, replace, count: int = -1, *, force_length: bool = False):
        find = to_bytes(find)
        replace = to_bytes(replace)
        
        if len(find) != len(replace) and not force_length:
            raise Exception("Find and replace parameters must be the same length")
        
        self.moshable = self.moshable.replace(find, replace, count)

    def save(self, filename: str = None):
        if not filename: 
            filename = self.filename

        self._apply_data()
        self._write_data(filename)

        self._log(f"Image has been saved as {filename}", 1)

def main():
    filename = "images/original_doge.jpg"
    image = Image(filename)

    while True:
        image.replace_position_random("doge was here")
        image.save()
        time.sleep(0.5)

if __name__ == "__main__":
    main()