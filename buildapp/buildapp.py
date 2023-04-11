import os
import argparse
import subprocess

KEYSTORE_ALIAS = 'defkeystorealias'
KEYSTORE_PASSWORD = 'defkeystorepass'
KEYSTORE_PATH = os.path.expanduser('~/buildapp-keystore.jks')


class CompileApp:
    def __init__(self, decompiled_path, output_apk_path):
        self.prealigned_file = f'{output_apk_path}_prealign'
        self.decompiled_path = decompiled_path

    def __enter__(self):
        run_process(f'apktool b {self.decompiled_path} -o {self.prealigned_file}', input_string='\n')

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.unlink(self.prealigned_file)

class AlignApk:
    def __init__(self, output_apk_path):
        run_process(f'zipalign -p -f -v 4 {output_apk_path}_prealign {output_apk_path}')

class ObtainKeystore:
    def __init__(self, keystore_path):
        if not keystore_path:
            ObtainKeystore.obtain_default_keystore()
            return

        global KEYSTORE_ALIAS, KEYSTORE_PASSWORD, KEYSTORE_PATH

        KEYSTORE_PATH = keystore_path
        KEYSTORE_ALIAS = input(f'Enter keystore alias: ')
        KEYSTORE_PASSWORD = input(f'Enter alias for password: ')

    @staticmethod
    def obtain_default_keystore():
        if not os.path.isfile(KEYSTORE_PATH):
            run_process(f'keytool -genkey -v -keystore {KEYSTORE_PATH} -alias {KEYSTORE_ALIAS} -keyalg RSA -keysize 2048 -validity 10000', input_string=f'{KEYSTORE_PASSWORD}\n{KEYSTORE_PASSWORD}\n\n\n\n\n\n\nyes', ignore_stderr=True)

class SignApk:
    def __init__(self, output_apk_path):
        self.output_apk_path = output_apk_path
        run_process(f'apksigner sign --ks-key-alias {KEYSTORE_ALIAS} --ks {KEYSTORE_PATH} {output_apk_path}', input_string=f'{KEYSTORE_PASSWORD}\n')

    def __del__(self):
        os.unlink(f'{self.output_apk_path}.idsig')

class InstallApk:
    def __init__(self, apk_path):
        run_process(f'adb install {apk_path}')


def run_process(cmdline, input_string='', ignore_stderr=False):
    print(f'Executing `{cmdline}`')

    subprocess.run(
        cmdline,
        shell=True,
        check=True,
        stdout=subprocess.DEVNULL,
        input=input_string.encode(),
        stderr=subprocess.DEVNULL if ignore_stderr else subprocess.PIPE
    )


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output-apk-path', required=True, help='path of output apk file')
    parser.add_argument('-d', '--decompiled-path', required=True, help='decompiled apk directory')
    parser.add_argument('-i', '--install', action='store_true', help='install on the adb device')
    parser.add_argument('-k', '--keystore-path', required=False, help='optional keystore final to sign the apk with')

    return parser.parse_args()


def build_app(output_apk_path, decompiled_folder, keystore_path=None, install_after_build=False):
    with CompileApp(decompiled_folder, output_apk_path):
        AlignApk(output_apk_path)
        ObtainKeystore(keystore_path)
        SignApk(output_apk_path)

        if install_after_build:
            InstallApk(output_apk_path)


def main():
    args = parse_arguments()
    build_app(args.output_apk_path, args.decompiled_path, args.keystore_path, args.install)

    print('buildapp completed successfully!')

if __name__ == "__main__":
    main()
