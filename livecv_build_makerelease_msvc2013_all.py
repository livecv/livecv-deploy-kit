import livecv_build_msvc2013_32 as build32
import livecv_makerelease_msvc2013_32 as makerelease32
import livecv_build_msvc2013_64 as build64
import livecv_makerelease_msvc2013_64 as makerelease64

build64.build_msvc2013_64()
makerelease64.makerelease_msvc2013_64()
build32.build_msvc2013_32()
makerelease32.makerelease_msvc2013_32()