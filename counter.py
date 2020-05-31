#!/usr/bin/env python3

__version__ = "1.0"

"""
----------
Changelog:
----------

- v1.0: Initial cli implementation.
"""

import csv
from collections import Counter
import glob
import sys
import os
from datetime import datetime

def convert_csvs():
    """
    Given we're in a directory containing .csv files with a column of countable
    values, count the number of times each value occurs and return a .csv file
    with those stats.
    """
    start_time = datetime.now()
    os.system('clear')

    filenames: set = get_files()

    for filename in filenames:
        grouped_values: list = read_csv(filename)
        output_filename: str = f"output_{filename}"
        write_csv(output_filename, grouped_values)

    end_time = datetime.now()
    delta = end_time - start_time
    processing_time = delta.total_seconds()
    print(f"🕉  Processed {len(filenames)} files in {processing_time} seconds.")

def get_files() -> set:
    """
    Return a set of all filenames in the current directory that we want to
    convert. If no matching filenames are found, exit.
    """
    all_filenames = glob.glob('*.csv')
    filenames = set(all_filenames) - set(glob.glob("output*"))

    if not filenames:
        print("No convertible .csv files found.")
        sys.exit()

    return filenames

def read_csv(filename: str) -> list:
    """
    Open a .csv file with the given filename, and create a dictionary counting
    each occurence of the same value in the csv's first column. Sort that csv
    by most common occurrence, and return it.
    """
    c: Counter = Counter()

    with open(filename, newline='') as csvfile:
        print(f"📜 Reading file '{filename}'...")
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        i: int = 0
        for row in spamreader:
            raw_num: str = row[0]
            if not raw_num:
                continue
            num: str = raw_num.strip()
            c[num] += 1
            i += 1

    print("🔀 Ordering by most common...")
    most_common = c.most_common(i)

    return most_common

def write_csv(output_filename: str, most_common: list) -> None:
    """
    Given an output_filename and list of unique value occurrences, make a .csv
    file containing those stats.
    """
    with open(output_filename, 'w', newline='') as f:
        print(f"🔄 Writing results to '{output_filename}'...")
        writer = csv.writer(f)
        writer.writerows(most_common)

    print(f"✅ Done creating {output_filename}!")

if __name__ == "__main__":
    convert_csvs()
