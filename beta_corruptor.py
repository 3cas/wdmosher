import os
import random

DEBUG = False
STEP = False
LOG = None
FILE = None
FAKE_DIVIDER_SIZE = 35

def debug(message: str):
    if DEBUG:
        print(message)
    
    if LOG:
        with open(LOG, "a") as f:
            f.write("\n" + message)

def simple_hex(value: int) -> str:
    return hex(value)[2:].zfill(2)

def find_real_data(data: bytes) -> tuple:
    real_streak = 0
    fake_streak = 0
    last_real = None
    current_block_first =  None
    largest_block_first = None
    largest_block_last = None

    # cat += bytes(chr(7), "UTF-8")

    for pos in range(len(data)):
        dec = data[pos]

        debug(f"\npos: {pos}, dec: {dec}, hex: {simple_hex(dec)}")

        if 32 <= dec <= 126:
            fake_streak = 0
            real_streak += 1
            last_real = pos

            if not current_block_first:
                current_block_first = pos

            debug("REAL")

        else:
            real_streak = 0
            fake_streak += 1

            if current_block_first and fake_streak >= FAKE_DIVIDER_SIZE:
                if (largest_block_first is None) or (largest_block_last-largest_block_first < last_real-current_block_first):
                    largest_block_first = current_block_first
                    largest_block_last = last_real

                current_block_first = None

            debug("FAKE")

        debug(f"real streak: {real_streak}")
        debug(f"fake streak: {fake_streak}")
        if last_real: debug(f"last real at {last_real}")
        if current_block_first: debug(f"current block started at {current_block_first}")
        if largest_block_first: debug(f"largest block from {largest_block_first} to {largest_block_last}")

        if STEP: input("step>")

    if current_block_first and (largest_block_last-largest_block_first < last_real-current_block_first):
        largest_block_first = current_block_first
        largest_block_last = last_real

    if largest_block_first is not None:
        preview = " ... ".join([" ".join([simple_hex(data[position]) for position in range(*do_range)]) for do_range in [(largest_block_first, largest_block_first+5), (largest_block_last-4, largest_block_last+1)]])
        print(f"\nDone! The largest block is from position {largest_block_first} to position {largest_block_last} and looks like {preview}")
        return largest_block_first, largest_block_last

    else:
        print("Largest block not found!")
        return None
    
def fill_to_bytes(fill) -> bytes:
    if isinstance(fill, int):
        fill = chr(fill)
    if isinstance(fill, str):
        fill = bytes(fill, "UTF-8")
    if not isinstance(fill, bytes):
        raise TypeError("`fill` must be an int, str, or bytes")
    
    return fill

def replace_position(data: bytes, start_position: int, fill, skip_fail: bool = False) -> bytes:
    fill = fill_to_bytes(fill)

    changed_data = data[:start_position] + fill + data[(start_position + len(fill)):]

    if len(changed_data) != len(data):
        if skip_fail:
            return data

        else:
            raise Exception("Size of fill exceeds length of data when applied to start position")
        
    else:
        return changed_data
    
def replace_position_random(data: bytes, fill) -> bytes:
    fill = fill_to_bytes(fill)
    return replace_position(data, random.randint(0, len(data)-len(fill)), fill)


def main():
    if FILE:
        filename = FILE
    else:
        filename = input("file: ")

    if LOG:
        if os.path.isfile(LOG):
            os.remove(LOG)
        with open(LOG, "w") as f:
            f.write(f"Log for file {filename}")

    with open(filename, "rb") as f:
        data = f.read()

    real_data_start, real_data_end = real_data_area = find_real_data(data)
    real_data = data[real_data_start:(real_data_end+1)]

    real_data = test_distortions(real_data)

    data = replace_position(data, real_data_start, real_data)

    with open(filename, "wb") as f:
        f.write(data)

def test_distortions(real_data: bytes) -> bytes:
    for _ in range(100):
        real_data = replace_position_random(real_data, "doge")

    return real_data

if __name__ == "__main__":
    main()