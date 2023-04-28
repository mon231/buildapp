# buildapp
Corss-Platform script used to recompile APK that was decompiled by apktool <br/>
That way, you can decompile an application, patch it's smali-source / resources / manifest / libs / ... <br />
And rebuild it into a new apk you may install in your devices <br />
<br />
*NOTE* that you should use this tool for debugging / educational purposes only!

## Installation
After having all [requirements](#Requirements), simply
> pip install buildapp --upgrade

Make sure to have python scripts folder in your path, <br/>
And use the correct version of pip for python3

## Decompilation process
Use [`apktool`](https://ibotpeaches.github.io/Apktool/install/) to decompile your application.

Apktool decompilation syntax:
> apktool d <apk_path> -o <output_folder>

## Patching process
Just change anything you want, native-elfs in `/lib` folder, [smali-code](https://source.android.com/docs/core/runtime/dalvik-bytecode) from smali folders, manifest file `AndroidManifest.xml`, resources, assets and whatever's out there

## Recompilation process
Simply use our tool, the syntax is:
> buildapp -d <sources_folder> -o <outout_apk>

For additional flags, ran `buildapp -h` <br/>

- apktool build
    - Use apktool to rebuild the apk from the sources folder
    - > apktool b <sources_folder> -o <output_apk>
- zip-alignment
    - apk is implemented as a zip file which should have the correct alignment in order to be installed
    - implemented using [`zipalign`](https://developer.android.com/tools/zipalign)
- generate / obtain keystore
    - our tool will generate a keystore if you didn't provide any
    - implemented using [`keytool`](https://docs.oracle.com/javase/8/docs/technotes/tools/unix/keytool.html)
- apk signing
    - our tool will sign the apk using that keystore
    - implemented using [`apksigner`](https://developer.android.com/tools/apksigner)
- apk installation
    - if asked to, buildapp will install the signed apk on connected adb device (if there's only one) <br/>
    *NOTE* that if you won't provide the same keystore as the original app already installed on your device, you may not be able to install the apk you built by this script unless you'll uninstall the original app first.
    - implemented using [`adb`](https://developer.android.com/tools/adb)

And that's it! Now you have a new apk, waiting to be installed it on your android devices!

## Requirements
The project assumes that installer already has the following tools in his path:
- android SDK tools (installed from android-sdk online)
    - adb (default at SDK\platform_tools, only required if `-i` flag is used)
    - zipalign (default at SDK\build_tools)
    - apksigner (default at SDK\build_tools)
- apktool [installation manual](https://ibotpeaches.github.io/Apktool/install/)
- keytool (default at jdk or jre bin folders, only required if `-k` flag is missing)
