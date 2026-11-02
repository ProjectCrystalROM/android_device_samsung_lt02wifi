# Project Crystal SM-T210/T210R bring-up snapshot

This branch records experimental CM11 device work as a reference for future Android bring-up. It is not a release or a self-contained CM11 manifest. The original device tree comes from T210-dev/android_device_samsung_lt02wifi at 04023cf7f742e7d03e556822b58c061638c1f9ff; its history and contributors are preserved.

## Configurations

- `CRYSTAL_STOCK_FULL=true` selects the stock-aligned vendor tree at `vendor/samsung/lt02wifi-stockfull` and its stock audio policy; `CRYSTAL_STOCK_GPU=true` selects `kernel/samsung/lt02-stockgpu`.
- The stock-full baseline was extracted from Samsung firmware T210RUEU0COI1/T210RXAR0COI1. Stock GPU userspace is Vivante 4.6.9 build 8290.
- The experimental `CRYSTAL_STOCK_GPU=true` without stock-full selects the separate `vendor/samsung/lt02wifi-stockgpu` experiment. These paths intentionally coexist with the original upstream device/vendor/kernel paths.
- Recovery device assertions accept `lt02` and `lt02wifi`.

The Project Crystal vendor fork carries `crystal-cm11-stockfull` for checkout at `vendor/samsung/lt02wifi-stockfull` and `crystal-cm11-stockgpu` for checkout at `vendor/samsung/lt02wifi-stockgpu`. The companion kernel fork branch `crystal-cm11-snapshot` belongs at `kernel/samsung/lt02-stockgpu`. Original upstream paths remain available for the unmodified baseline. The Vivante 8290 driver was sourced from asasoft/lt02wifi-kk-kernel commit 85f33f385873da9f3f07f960e72805bc9a3a4c87, then adapted to the T210-dev CM kernel. Its license notices remain in the source.

## Results and porting cautions

On the owner's device, display composition and colors were corrected, Wi-Fi toggles worked, Bluetooth paired and produced headset audio, and a 360p local H.264 video played. Chromium 81 standalone improved browser usability. These are reported results on specific experimental builds, not qualification of every feature or future platform.

CM11 platform changes were also needed: legacy Marvell hwcomposer layer layout and EGL handles; native window query 1000; original T210-era SurfaceFlinger compatibility; ION userspace diagnostics; Wi-Fi socket cleanup; Bluetooth audio module selection; stock audio policy routing; software H.264 selection and frame conversion; and a browser H.264 capability experiment. Speaker mixer-volume changes, including a no-burst follow-up, were under test at this snapshot and are not established as fixed. Camera, performance, hardware video decode, other device functions and cross-version compatibility remain open. These platform changes are not contained in the device/vendor/kernel repositories and require separate adaptation or reimplementation on another Android version.

The proprietary files are firmware-derived; preserve origin and device compatibility when changing the baseline. No assertion is made that all blobs or code are redistributable under the same terms as this device repository.

## Preserved Marvell dependencies

The original T210-dev manifest also uses these unmodified tablet-related repositories. Project Crystal forks preserve the exact commits used by this checkout on `crystal-cm11-baseline`:

- `ProjectCrystalROM/android_hardware_marvell`: `ec52501666c6861855942fded6a558c22917a878`, checkout `hardware/marvell`.
- `ProjectCrystalROM/android_vendor_marvell_generic`: `cda3d6f6a61148184ceb23c6028be44b3e830c7f`, checkout `vendor/marvell/generic`.
- `ProjectCrystalROM/android_vendor_marvell_external`: `400989390bf0f0ff285556f238e397b298ef07a6`, checkout `vendor/marvell/external`.

`docs/archive/` preserves the original local build and blob preparation scripts and the vendor selection inventory for reference. They contain machine-specific absolute paths, rely on unpublished local firmware and platform modifications, and some write into the source tree. They are not portable or a complete reproduction recipe; review before running.
