import argparse
import sys
from typing import Sequence

import uvicorn


def init_argparse(args: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='nwta backend', formatter_class=argparse.RawTextHelpFormatter)

    add = parser.add_argument
    add('--host', type=str, default='0.0.0.0', help='Server host address.')
    add('-p', '--port', type=int, default=5000, help='Server port number.')

    return parser.parse_args(args)


def main():
    args = init_argparse(sys.argv[1:])

    uvicorn.run("v1.api:app", host=args.host, port=args.port, reload=True, debug=True)


if __name__ == '__main__':
    main()
