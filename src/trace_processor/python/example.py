#!/usr/bin/env python3
# Copyright (C) 2020 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse

from trace_processor.api import TraceProcessor


def main():
  # Parse arguments passed from command line
  parser = argparse.ArgumentParser()
  parser.add_argument(
      "-a",
      "--address",
      help="Address at which trace_processor is being run, e.g. localhost:9001",
      type=str)
  parser.add_argument(
      "-b",
      "--binary",
      help="Absolute path to a trace processor binary",
      type=str)
  parser.add_argument("-f", "--file", help="Absolute path to trace", type=str)
  args = parser.parse_args()

  # Pass arguments into api to construct the trace processor and load the trace
  if args.address is None and args.file is None:
    raise Exception("You must specify an address or a file path to trace")
  elif args.address is None:
    tp = TraceProcessor(file_path=args.file, bin_path=args.binary)
  elif args.file is None:
    tp = TraceProcessor(addr=args.address)
  else:
    tp = TraceProcessor(
        addr=args.address, file_path=args.file, bin_path=args.binary)

  # Call functions on the loaded trace
  res_it = tp.query('select * from slice limit 10')
  for row in res_it:
    print(row.name)
  am_metrics = tp.metric(['android_mem'])
  tp.close()


if __name__ == "__main__":
  main()
