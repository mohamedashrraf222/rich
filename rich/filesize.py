"""Functions for reporting filesizes. Borrowed from https://github.com/PyFilesystem/pyfilesystem2

The functions declared in this module should cover the different
use cases needed to generate a string representation of a file size
using several different units. Since there are many standards regarding
file size units, three different functions have been implemented.

See Also:
    * `Wikipedia: Binary prefix <https://en.wikipedia.org/wiki/Binary_prefix>`_

"""

__all__ = ["decimal"]

from typing import Iterable, List, Optional, Tuple


def _to_str(
    size: int,
    suffixes: Iterable[str],
    base: int,
    *,
    precision: Optional[int] = 1,
    separator: Optional[str] = " ",
) -> str:
    # Early exits for 1 and small numbers
    if size == 1:
        return "1 byte"
    elif size < base:
        return f"{size:,} bytes"

    # Convert suffixes to tuple to allow O(1) indexing and avoid repeated power calculations
    suffixes_tuple = tuple(suffixes)
    n_suffixes = len(suffixes_tuple)

    # Find the appropriate unit index
    # Start from i=2 consistent with original enumerate(..., 2)
    i = 2
    unit = base ** i
    for suffix in suffixes_tuple:
        if size < unit:
            # Efficient calculation of value without unnecessary use of format() for a single parameter
            value = base * size / unit
            return f"{value:,.{precision}f}{separator}{suffix}"
        i += 1
        unit *= base  # next power, faster than base**i

    # If size is extremely large, use the largest suffix
    value = base * size / unit
    return f"{value:,.{precision}f}{separator}{suffixes_tuple[-1]}"


def pick_unit_and_suffix(size: int, suffixes: List[str], base: int) -> Tuple[int, str]:
    """Pick a suffix and base for the given size."""
    for i, suffix in enumerate(suffixes):
        unit = base**i
        if size < unit * base:
            break
    return unit, suffix


def decimal(
    size: int,
    *,
    precision: Optional[int] = 1,
    separator: Optional[str] = " ",
) -> str:
    """Convert a filesize in to a string (powers of 1000, SI prefixes).

    In this convention, ``1000 B = 1 kB``.

    This is typically the format used to advertise the storage
    capacity of USB flash drives and the like (*256 MB* meaning
    actually a storage capacity of more than *256 000 000 B*),
    or used by **Mac OS X** since v10.6 to report file sizes.

    Arguments:
        int (size): A file size.
        int (precision): The number of decimal places to include (default = 1).
        str (separator): The string to separate the value from the units (default = " ").

    Returns:
        `str`: A string containing a abbreviated file size and units.

    Example:
        >>> filesize.decimal(30000)
        '30.0 kB'
        >>> filesize.decimal(30000, precision=2, separator="")
        '30.00kB'

    """
    return _to_str(
        size,
        ("kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"),
        1000,
        precision=precision,
        separator=separator,
    )
