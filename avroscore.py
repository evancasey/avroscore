import fastavro as avro
from fastavro.six import json_dump
from sys import stdout
import subprocess
import pprint

import transform

encoding = stdout.encoding or "UTF-8"

def apply_transformation(records, indent, underscore_args):
    while len(underscore_args) > 0:
        if underscore_args[0] == '|':
            underscore_args.pop(0)
            continue
        if underscore_args[0] == 'pluck':
            # TODO: handle error case where next arg is '|'
            res = transform.pluck(records, underscore_args[1])
            underscore_args.pop(0)
            underscore_args.pop(0)
            records = res
            continue
        elif underscore_args[0] == 'size':
            res = transform.size(records)
            underscore_args.pop(0)
            records = res
            continue
        elif underscore_args[0] == 'first':
            res = transform.first(records)
            underscore_args.pop(0)
            records = res
            continue

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(records)

def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(
        description='iter over avro file, emit records as JSON')
    parser.add_argument('underscore', help='underscore arguments', nargs='*')
    parser.add_argument('-d', '--data', help='file(s) to parse')
    parser.add_argument('--schema', help='dump schema instead of records',
                        action='store_true', default=False)
    parser.add_argument('--codecs', help='print supported codecs',
                        action='store_true', default=False)
    parser.add_argument('--version', action='version',
                        version='fastavro {0}'.format(avro.__version__))
    parser.add_argument('-p', '--pretty', help='pretty print json',
                        action='store_true', default=False)
    args = parser.parse_args(argv[1:])

    if args.codecs:
        import fastavro
        print('\n'.join(sorted(fastavro._reader.BLOCK_READERS)))
        raise SystemExit

    filename = args.data 
    try:
        fo = open(filename, 'rb')
    except IOError as e:
        raise SystemExit(
            'error: cannot open {0} - {1}'.format(filename, e))

    try:
        reader = avro.reader(fo)
    except ValueError as e:
        raise SystemExit('error: {0}'.format(e))

    if args.schema:
        json_dump(reader.schema, True)
        sys.stdout.write('\n')

    indent = 4 if args.pretty else None
    try:
        all_records = []
        for record in reader:
            all_records.append(record)
        apply_transformation(all_records, indent, args.underscore)
    except (IOError, KeyboardInterrupt):
        pass

if __name__ == '__main__':
    main()
