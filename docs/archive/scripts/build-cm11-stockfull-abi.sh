#!/bin/bash
set -o pipefail
cd /work/Tab3/cm11 || exit 1
export HOME=/home/airi USER=airi LOGNAME=airi
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64 ANDROID_JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
export OUT_DIR=/work/Tab3/cm11/out-stockfull-abi CRYSTAL_STOCK_GPU=true CRYSTAL_STOCK_FULL=true USE_CCACHE=0
source build/envsetup.sh
lunch cm_lt02wifi-user || exit $?
make -j8 bacon || exit $?
package="$OUT_DIR/target/product/lt02wifi/cm-11-$(date +%Y%m%d)-UNOFFICIAL-lt02wifi.zip"
unzip -p "$package" system/lib/modules/galcore.ko | strings | grep -F '$VERSION$4.6.9:8290$' > /dev/null || { echo 'ERROR: missing 8290 GPU module' >&2; exit 1; }
unzip -p "$package" system/build.prop | grep -Fx 'ro.crystal.stockgpu=1' > /dev/null || { echo 'ERROR: stock GPU compatibility switch missing' >&2; exit 1; }
unzip -p "$package" system/build.prop | grep -Fx 'ro.crystal.browser_h264_only=1' > /dev/null || { echo 'ERROR: browser H.264-only switch missing' >&2; exit 1; }
if cmp -s <(unzip -p "$package" system/lib/hw/audio.a2dp.default.so) /work/Tab3/stock-reference/full-system/lib/hw/audio.a2dp.default.so; then
    echo 'ERROR: package still contains the stock A2DP module' >&2
    exit 1
fi
