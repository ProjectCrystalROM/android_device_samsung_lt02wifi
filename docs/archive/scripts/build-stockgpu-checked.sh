#!/bin/bash
set -o pipefail
cd /work/Tab3/cm11 || exit 1
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
make -j8 -C kernel/samsung/lt02-stockgpu O=/work/Tab3/cm11/out-stockgpu/target/product/lt02wifi/obj/KERNEL_OBJ ARCH=arm CROSS_COMPILE=/work/Tab3/cm11/prebuilts/gcc/linux-x86/arm/arm-eabi-4.7/bin/arm-eabi- modules || exit $?
module=out-stockgpu/target/product/lt02wifi/obj/KERNEL_OBJ/drivers/marvell/graphics/galcore_4x/galcore.ko
strings "$module" | grep -F '$VERSION$4.6.9:8290$' > /dev/null || exit 1
exec /bin/bash /work/Tab3/scripts/build-cm11-stockgpu.sh
