#!/usr/bin/env python
# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2015, Numenta, Inc.  Unless you have purchased from
# Numenta, Inc. a separate commercial license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

"""
Purges old records from taurus_collectors.twitter_tweets table.

NOTE: this script may be configured as "console" app by the package
installer.
"""

import logging
from optparse import OptionParser
import sys

import sqlalchemy

from taurus.metric_collectors import collectorsdb, logging_support



g_log = logging.getLogger("purge_old_tweets")



def _parseArgs():
  """
  :returns: dict of arg names and values:
    days - Messages older than this number of days will be purged
  """
  helpString = (
    "%%prog [options]"
    "Purges old records from %s table.") % (collectorsdb.schema.twitterTweets,)

  parser = OptionParser(helpString)

  parser.add_option(
      "--days",
      action="store",
      type="int",
      dest="days",
      help="Messages older than this number of days will be purged")

  options, remainingArgs = parser.parse_args()
  if remainingArgs:
    parser.error("Unexpected remaining args: %r" % (remainingArgs,))

  if options.days is None:
    parser.error("Required \"--days\" option was not specified")

  return dict(
    days=options.days)



def main():
  """
  NOTE: main also serves as entry point for "console script" generated by setup
  """
  logging_support.LoggingSupport().initTool()

  try:
    options = _parseArgs()

    days = options["days"]

    g_log.info("Purging records from table=%s older than numDays=%s",
               collectorsdb.schema.twitterTweets, days)


    twitterTweetsSchema = collectorsdb.schema.twitterTweets

    query = twitterTweetsSchema.delete().where(
      twitterTweetsSchema.c.created_at <
      sqlalchemy.func.date_sub(
        sqlalchemy.func.utc_timestamp(),
        sqlalchemy.text("INTERVAL %i DAY" % (days,)))
    )
    with collectorsdb.engineFactory().begin() as conn:
      result = conn.execute(query)

    g_log.info("Purged numRows=%s from table=%s",
               result.rowcount, collectorsdb.schema.twitterTweets)
  except SystemExit as e:
    if e.code != 0:
      g_log.exception("Failed!")
    raise
  except Exception:
    g_log.exception("Failed!")
    raise


if __name__ == "__main__":
  main()
