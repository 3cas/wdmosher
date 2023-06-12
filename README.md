# wdmosher

wDmosher is a datamosher and photo glitcher I am making created in Python [very WIP]

## Example usage

The following example opens MyFile.jpg and inserts the text "i want fuit gummy" in a random place, which slightly corrupts the image.

```py
glitch_me = Image("MyFile.jpg")
glitch_me.replace_position_random("i want fuit gummy")
glitch_me.save()
```

## Image class methods

- **`replace_position(start_position: int, fill)`** - Replaces data of the same length as `fill` starting at `start_position` after the headers with `fill`
- **`replace_position_random(fill)`** - Replaces data of the same length as `fill` at a random position after the headers with `fill`
- **`find_replace(find, replace, count: int = -1)`** - Finds and replaces data, right now they must be the same length. Count is optional.
- **`save(filename: str = None)`** - Saves the image. If a `filename` is not specified, it will save it where it was opened and overwrite the original. 

## Header detection

Header detection is very WIP. Right now, the program finds the largest "block" of data that is separate from repeated lines of unreadable characters. This seems to work well for JPEGs, as there is space between the header and the real data. The header cannot be edited because that will make the image unable to be opened. As of now, the data that is detected to be separate from the header is saved to a `moshable` attribute, which gets changed by the methods, and then gets put back where it belongs once the image is saved.