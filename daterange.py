#!/usr/bin/env python3

"""A simple daterange tool."""

import argparse
import datetime
import logging
import os
import re
import sys
import time


def defineFlags():
  parser = argparse.ArgumentParser(description=__doc__)
  # See: http://docs.python.org/2/library/argparse.html
  parser.add_argument(
      '-v', '--verbosity',
      action='store',
      default=20,
      metavar='LEVEL',
      type=int,
      help='the logging verbosity')
  # See: http://docs.python.org/library/datetime.html#strftime-strptime-behavior
  parser.add_argument(
      '-f', '--format',
      action='store',
      default='%Y/%m/%d',
      metavar='FORMAT',
      type=str,
      help='the format of the resulting date')
  parser.add_argument(
      '-s', '--start',
      action='store',
      default=None,
      metavar='DATETIME',
      type=str,
      help='the start date/time which follows the format defined by --format')
  parser.add_argument(
      '-e', '--end',
      action='store',
      default=None,
      metavar='DATETIME',
      type=str,
      help='the end date/time which follows the format defined by --format')
  parser.add_argument(
      '-c', '--count',
      action='store',
      default=7,
      metavar='COUNT',
      type=int,
      help='the number iterations, ignored when --end is defined')
  parser.add_argument(
      '-d', '--delimeter',
      action='store',
      default='\n',
      metavar='CHAR',
      type=str,
      help='the delimeter to print between dates')
  parser.add_argument(
      '-i', '--interval',
      action='store',
      default=-1,
      metavar='INTERVAL',
      type=int,
      help='the interval when counting days')
  parser.add_argument(
      '-r', '--reverse',
      action='store_true',
      default=False,
      help='reverse the output')

  args = parser.parse_args()
  checkFlags(parser, args)
  return args


def checkFlags(parser, args):
  # See: http://docs.python.org/2/library/argparse.html#exiting-methods
  return


def getDaysAgo(date_string):
  if date_string == 'today':
    return 0

  if date_string == 'yesterday':
    return 1

  match = re.match(r'^(\d+)days?ago$', date_string)
  if match:
    return int(match.group(1))

  return None


def today():
  return datetime.datetime.now().replace(
      hour=0, minute=0, second=0, microsecond=0)


def parseDate(date_string, fmt):
  days = getDaysAgo(date_string)
  if days is not None:
    return today() - datetime.timedelta(days=days)

  for f in (fmt, '%Y-%m-%d', '%Y/%m/%d', '%Y%m%d'):
    try:
      return datetime.datetime.strptime(date_string, f)
    except ValueError:
      continue

  raise ValueError(
      'time data %r does not match any known formats' % date_string)


def main(args):
  if args.start:
    start = parseDate(args.start, args.format)
  else:
    # The start of today's date is used.
    start = today()

  if args.end:
    end = parseDate(args.end, args.format)
    if (start < end and args.interval < 0) or (
        start > end and args.interval > 0):
      args.interval = -args.interval
  else:
    end = None

  output = []

  i = 0
  delta = datetime.timedelta(days=args.interval)
  while (end and ((args.interval > 0 and start <= end) or
                  (args.interval < 0 and start >= end))) or (
                      not end and i < args.count):
    output.append(start.strftime(args.format))
    start += delta
    i += 1

  if args.reverse:
    output.reverse()

  print(args.delimeter.join(output))

  return os.EX_OK


if __name__ == '__main__':
  a = defineFlags()
  logging.basicConfig(
      level=a.verbosity,
      datefmt='%Y/%m/%d %H:%M:%S',
      format='[%(asctime)s] %(levelname)s: %(message)s')
  sys.exit(main(a))
