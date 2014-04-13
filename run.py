import argparse
from bacon import importer, search, settings


def main():
    """The main runner file for the 'bacon' project."""
    parser = argparse.ArgumentParser(
        description='Find the shortest path between actors.'
    )

    subparsers = parser.add_subparsers(help='sub-command help')

    # Sub-command for importing initial data
    import_parser = subparsers.add_parser(
        'import', help='Import data from folder'
    )
    import_parser.add_argument(
        'directory',
        nargs='?',
        default=settings.IMPORT_DIRECTORY,
        help='Directory where film JSON files can be found.'
    )
    import_parser.set_defaults(func=importer.load_directory)

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
        default=settings.TARGET_ACTOR,
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