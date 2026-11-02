#!/bin/bash
set -o pipefail
cd /work/Tab3/cm11 || exit 1
export HOME=/home/airi USER=airi LOGNAME=airi
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
export ANDROID_JAVA_HOME="$JAVA_HOME"
export OUT_DIR=/work/Tab3/cm11/out-diagnostic
export USE_CCACHE=0
source build/envsetup.sh
lunch cm_lt02wifi-userdebug || exit $?
make -j8 bacon
