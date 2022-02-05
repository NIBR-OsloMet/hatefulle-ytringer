#!/usr/bin/env python3

from csv import reader, writer, QUOTE_ALL
from hashlib import md5

def main():
    with(open('./comments.csv', 'r')) as infile:
        with(open('/tmp/comments.csv', 'w')) as outfile:
            csv_reader = reader(infile)
            csv_writer = writer(outfile, quoting = QUOTE_ALL)

            header = ['post_id', 'comment_id', 'author_id', 'time', 'text', 'answers']
            csv_writer.writerow(header)

            for row in csv_reader:
                row[2] = md5(row[2].encode()).hexdigest()
                csv_writer.writerow(row)

if __name__ == '__main__':
    main()
