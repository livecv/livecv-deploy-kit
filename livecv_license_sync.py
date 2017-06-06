import os
import sys
import io
from livecv.license import *
from livecv.filesystem import *

NEW_LICENSE = str('/****************************************************************************\n'
			'**\n'
			'** Copyright (C) 2014-2017 Dinu SV.\n'
			'** (contact: mail@dinusv.com)\n'
			'** This file is part of Live CV Application.\n'
			'**\n'
			'** GNU Lesser General Public License Usage\n'
			'** This file may be used under the terms of the GNU Lesser\n'
			'** General Public License version 3 as published by the Free Software\n'
			'** Foundation and appearing in the file LICENSE.LGPLv3 included in the\n'
			'** packaging of this file. Please review the following information to\n'
			'** ensure the GNU Lesser General Public License version 3 requirements\n'
			'** will be met: https://www.gnu.org/licenses/lgpl.html.\n'
			'**\n'
			'****************************************************************************/')

OLD_LICENSE = '\/\*{20,}.*Copyright\s\(C\)\s2014-2016\sDinu\sSV.*\*{20,}\/'


def main(argv):
    if ( len(argv) == 0 ):
        sourcedir = FileSystem.scriptdir() + '/..'
    elif ( argv[0] == '-h' ):
        print('Usage: livecv_license-set.py [source-dir]')
    else:
        sourcedir = argv[0]

    paths = [
        'application/src',
        'editor/lcveditor/src',
        'editor/qmljsparser/src',
        'plugins/live/src',
        'plugins/lcvcore/src',
        'plugins/lcvfeatures2d/src',
        'plugins/lcvimgproc/src',
		'plugins/lcvphoto/src',
        'plugins/lcvvideo/src',
        'tests'
    ]

    for path in paths:
        sourcePath = os.path.join(sourcedir, path)
        license = License(sourcePath, ['h', 'hpp', 'cpp', 'qml', 'js'])
        license.update(NEW_LICENSE, OLD_LICENSE)

if __name__ == "__main__":
    main(sys.argv[1:])
