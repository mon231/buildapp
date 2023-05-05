import argparse
import subprocess
from os import environ
from sys import platform
from pathlib import Path
from base64 import b64decode
from os.path import expanduser


KEYSTORE_ALIAS = 'defkeystorealias'
KEYSTORE_PASSWORD = 'defkeystorepass'
DEFAULT_KEYSTORE = b64decode(b'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')

RELTOOLS_ROOT = Path(expanduser('~/.reltools/'))
KEYSTORE_PATH = Path(RELTOOLS_ROOT / 'buildapp-keystore.jks')


class CompileApp:
    def __init__(self, decompiled_path, output_apk_path):
        self.prealigned_file = f'{output_apk_path}_prealign'
        self.decompiled_path = decompiled_path

    def __enter__(self):
        run_process(f'apktool b {self.decompiled_path} -o {self.prealigned_file}', input_string='\n')

    def __exit__(self, exc_type, exc_val, exc_tb):
        Path(self.prealigned_file).unlink()

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
        KEYSTORE_PASSWORD = input(f'Enter keystore password: ')

    @staticmethod
    def obtain_default_keystore():
        if not KEYSTORE_PATH.is_file():
            KEYSTORE_PATH.write_bytes(DEFAULT_KEYSTORE)

class SignApk:
    def __init__(self, output_apk_path):
        self.output_apk_path = output_apk_path
        run_process(f'apksigner sign --ks-key-alias {KEYSTORE_ALIAS} --ks {KEYSTORE_PATH} {output_apk_path}', input_string=f'{KEYSTORE_PASSWORD}\n')

    def __del__(self):
        Path(f'{self.output_apk_path}.idsig').unlink()

class InstallApk:
    def __init__(self, apk_path):
        run_process(f'adb install -r {apk_path}')


def run_process(cmdline, input_string='', ignore_stderr=False):
    reltools_env = environ.copy()
    PATH_SEP_CHAR = ';' if platform == 'win32' else ':'

    if 'PATH' not in reltools_env:
        reltools_env['PATH'] = ''
    elif reltools_env['PATH']:
        reltools_env['PATH'] += PATH_SEP_CHAR

    reltools_env['PATH'] += PATH_SEP_CHAR.join(
        str(tools_path)
        for tools_path in RELTOOLS_ROOT.glob('*')
        if tools_path.is_dir()
    )

    print(f'Executing `{cmdline}`')

    subprocess.run(
        cmdline,
        shell=True,
        check=True,
        env=reltools_env,
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
