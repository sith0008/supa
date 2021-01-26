import argparse

def main(init_sql, init_graph):
    if init_sql:
        # TODO: run init guideline method
        raise NotImplementedError

    if init_graph:
        # TODO: run init graph nodes methods
        raise NotImplementedError


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--sql",
        action='store_true',
        help="whether to initialise the MySQL database"
    )
    parser.add_argument(
        "-g",
        "--graph",
        action='store_true',
        help="whether to initialise the neo4j database"
    )
    args = parser.parse_args()
    main(args.sql, args.graph)