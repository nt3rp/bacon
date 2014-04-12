import argparse
from bacon import importer
from bacon import models

def main():
    parser = argparse.ArgumentParser(
        description='Find the shortest path between actors.'
    )

    subparsers = parser.add_subparsers(help='sub-command help')

    create_parser = subparsers.add_parser(
        'initialize', help='Initializes the application'
    )
    create_parser.set_defaults(func=models.create_database)

    import_parser = subparsers.add_parser(
        'import', help='Imports data from films folder'
    )
    import_parser.set_defaults(func=importer.import_data)

    search_parser = subparsers.add_parser(
        'find', help='Find link from actor to Kevin Bacon'
    )
    search_parser.add_argument('actor_name', help='name of actor to start search from')
    search_parser.set_defaults(func=models.find)

    args, unknown = parser.parse_known_args()
    kwargs = vars(args)
    args.func(**kwargs)

if __name__ == '__main__':
    main()