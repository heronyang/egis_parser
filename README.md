# egis_parser

A parser for grabbing data from the EGIS website for researches in Envinronmental Engineering.

## Description

The parser written in Python parses 高壓用電 and 包制用電 data of 臺中 from 2012.01 to 2014.12 into two CSV files. `PHighStatistics.csv` contains 高壓用電 data, and `PItemStatistics` 包制用電 data.

## Usage

    $ python parser.py

If you placed your `parser.py` on the desktop, please use following command:

    $ python ~/Desktop/parser.py

## Notice

- Please avoid running the program intensely, it could potentially overload the EGIS web server.
- The CSV files can be opened by Microsoft Excel or Apple Numbers. Please use UTF-8 encoding to view Chinese contents.
