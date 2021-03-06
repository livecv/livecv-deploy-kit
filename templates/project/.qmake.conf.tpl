
# Configuration paths for Live CV
#   LIVEKEYS_BIN_PATH -
#      The path where Live CV binaries reside.
#      In case you are building Live CV from source, together with this project, then you
#      can configure it as $$shadowed($$PWD)/livekeys/bin, which is equivalent
#      to the $$OUT_PWD (or output directory) of this project), concatenated with the
#      dependency subproject
#
#   LIVEKEYS_DEV_PATH -
#      The path to Live CV dev directory.
#      In case Live CV is build from source, this is basically Live CVs source directory
#      (required for 'include' and 'qmake project' files).
#
#    PROJECT_ROOT -
#      The path to the source code root of this project
#
#    BUILD_LIVEKEYS -
#      In case you are using a source from Live CV, you need to build it first
#
#    DEPLOY_TO_LIVEKEYS -
#      The plugin will be deployed to Live CV's plugins directory, so it can be instantly
#      imported and used.
#
# Note: The deployment and output paths of this project are configured automatically in the
# 'package.pri' file included from Live CV's dev dir

LIVEKEYS_BIN_PATH = $$shadowed($$PWD)/livekeys/bin
LIVEKEYS_DEV_PATH = $$PWD/livekeys

PROJECT_ROOT = $$PWD

BUILD_DEPENDENCIES = true
DEPLOY_TO_LIVEKEYS = true

exists($$PWD/config.pri):include($$PWD/config.pri)
include($$LIVEKEYS_DEV_PATH/project/package.pri)
