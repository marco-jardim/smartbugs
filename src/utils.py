from solidity_parser import parser
from src.logger import logs
from typing import Dict
#from semantic_version import NpmSpec
from src.solc_versions import solc_available_versions_str
import re

BLACK = '\x1b[1;30m'
RED = '\x1b[1;31m'
GREEN = '\x1b[1;32m'
YELLOW = '\x1b[1;33m'
BLUE = '\x1b[1;34m'
MAGENTA = '\x1b[1;35m'
CYAN = '\x1b[1;36m'
WHITE = '\x1b[1;37m'
COLRESET = '\x1b[0m'
COLSUCCESS = GREEN
COLERR = RED
COLWARN = YELLOW
COLINFO = BLUE
COLSTATUS = WHITE

def get_solc_suitable_version(file: str):
    """
    get solidity compiler version, assuming that first line of file
    is pragma with version; if ^ is used, it gets the latest version from the
    same major version; otherwise, it returns the first three numbers separated
    by a dot
    """
    try:
        with open(file, 'r', encoding='utf-8') as fd:
            sourceUnit = parser.parse(fd.read())

        # Get first version mentioned. This assumes that: 
        # 1) there is a numeric version specified
        # 2) the version is of the form x.y.z or ^x.y.z, where x, y and z are numbers
        # 3) the first version is always included (i.e. it excludes
        #    pragma versions such as '>0.5.1')
        # In the future, we want to fully support npm version specifications;
        # however, the current version of the solidity parser does not support
        # them properly.
 
        # Assume that first line is pragma with version
        first_line = sourceUnit['children'][0]['value']
        if len(first_line) > 0 and first_line[0] == '^':
            # Get latest version from the same major version

            # Get major version
            major_version = first_line.split('.')[1]

            # Filter available versions with same major version
            same_major_version = list(filter(lambda v: len(v)==3 and v[1]==major_version, \
                    map(lambda v: v.split('.'), solc_available_versions_str)))

            # Sort by minor version; latest comes first
            same_major_version.sort(reverse=True, key=(lambda e: int(e[2])))
            
            solc_version = '.'.join(same_major_version[0])
        else:
            solc_version = re.search('\d+\.\d+\.\d+', first_line).group()
        return solc_version
    except:
        msg = 'WARNING: could not parse solidity file to get solc version'
        logs.print(f"{COLWARN}{msg}{COLRESET}", msg)
    return None
