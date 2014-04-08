import argparse
import models

def main():
    parser = argparse.ArgumentParser(
        description='Find the shortest path between actors.'
    )

    subparsers = parser.add_subparsers(help='sub-command help')

    create_parser = subparsers.add_parser(
        'initialize', help='Initializes the application'
    )
    create_parser.set_defaults(func=models.create_database)

    args, unknown = parser.parse_known_args()

    args.func(args)

if __name__ == '__main__':
    main()