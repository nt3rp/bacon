import argparse
from bacon import importer, search

def main():
    parser = argparse.ArgumentParser(
        description='Find the shortest path between actors.'
    )

    subparsers = parser.add_subparsers(help='sub-command help')

    # Sub-command for importing initial data
    import_parser = subparsers.add_parser(
        'import', help='Imports data from films folder'
    )
    import_parser.set_defaults(func=importer.import_data)

    # Sub-command for search data
    search_parser = subparsers.add_parser(
        'search', help='Find how actors are connected.'
    )
    search_parser.add_argument(
        'actor', help='Name of actor to start search from'
    )
    search_parser.add_argument(
        'target_actor',
        nargs='?',
        default='Kevin Bacon',
        help='Name of actor to find connection to.'
    )
    search_parser.set_defaults(func=search.find)

    # Process Arguments
    args, unknown = parser.parse_known_args()
    kwargs = vars(args)

    # Run whichever sub-command is necessary
    args.func(**kwargs)

if __name__ == '__main__':
    main()