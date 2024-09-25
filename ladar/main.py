import argparse
import sys

from ladar.cmds import api  # , foo, bar


def main():
    parser = argparse.ArgumentParser(
        prog="ladar", description="Ladar command-line tool"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    api_parser = subparsers.add_parser(
        "api", help="Extract the API from a Python library"
    )
    api.add_arguments(api_parser)

    # foo_parser = subparsers.add_parser("foo", help="Example command foo")
    # foo.add_arguments(foo_parser)

    # bar_parser = subparsers.add_parser("bar", help="Example command bar")
    # bar.add_arguments(bar_parser)

    args = parser.parse_args()

    if args.command == "api":
        api.main(args)
    # elif args.command == "foo":
    #    foo.main(args)
    # elif args.command == "bar":
    #    bar.main(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
