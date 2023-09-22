import io
import re
import sys
import shutil
import os.path
import requests
from pathlib import Path
from zipfile import ZipFile
from os.path import expanduser


DOWNLOAD_SUCCEEDED = 200

APKTOOL_PATH = Path(expanduser('~/.reltools/third_party_apktool'))
PLATFORM_TOOLS_PATH = Path(expanduser('~/.reltools/third_party_platform_tools'))
BUILD_TOOLS_PATH = Path(expanduser('~/.reltools/third_party_android_build_tools'))

BUILD_TOOLS_PATTERN = r'Build Tools, Revision (\d+)\.(\d+)\.(\d+)'
BUILD_TOOLS_RELEASES_URL = 'https://developer.android.com/tools/releases/build-tools'

BUILD_TOOLS_DOWNLOAD_URL = 'https://dl.google.com/android/repository/build-tools_r{version}-{os}.zip'
PLATFORM_TOOLS_DOWNLOAD_URL = 'https://dl.google.com/android/repository/platform-tools-latest-{os}.zip'

APKTOOL_RELEASES_URL = 'https://bitbucket.org/iBotPeaches/apktool/downloads/'
PLATFORM_TO_APKTOOL_WRAPPER_URL = {
    'linux': 'https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool',
    'darwin': 'https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/osx/apktool',
    'win32': 'https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/windows/apktool.bat'
}

PLATFORM_TO_BUILD_TOOLS_OS = {
    'linux': 'linux',
    'darwin': 'macosx',
    'win32': 'windows',
}

PLATFORM_TO_PLATFORM_TOOLS_OS = {
    'linux': 'linux',
    'darwin': 'darwin',
    'win32': 'windows'
}

class ToolsFetcher:
    def __init__(self):
        self.__build_tools_os = PLATFORM_TO_BUILD_TOOLS_OS[sys.platform]
        self.__platform_tools_os = PLATFORM_TO_PLATFORM_TOOLS_OS[sys.platform]
        self.__build_tools_releases = requests.get(BUILD_TOOLS_RELEASES_URL).text

    def download_all_tools(self):
        if not BUILD_TOOLS_PATH.is_dir():
            print('downloading build tools ...')
            self.__download_build_tools()
            ToolsFetcher.__unpack_subfolder(BUILD_TOOLS_PATH)

        if not PLATFORM_TOOLS_PATH.is_dir():
            print('downloading platform tools ...')
            self.__download_platform_tools()
            ToolsFetcher.__unpack_subfolder(PLATFORM_TOOLS_PATH)

        if not APKTOOL_PATH.is_dir():
            print('downloading apktool ...')
            self.__download_apktool()

        print('downloading completed!')

    def __download_build_tools(self):
        for major, minor, patch in re.findall(BUILD_TOOLS_PATTERN, self.__build_tools_releases):
            resp = requests.get(BUILD_TOOLS_DOWNLOAD_URL.format(version=f'{major}', os=self.__build_tools_os))

            if resp.status_code != DOWNLOAD_SUCCEEDED:
                resp = requests.get(BUILD_TOOLS_DOWNLOAD_URL.format(version=f'{major}.{minor}.{patch}', os=self.__build_tools_os))

            if resp.status_code != DOWNLOAD_SUCCEEDED:
                continue

            BUILD_TOOLS_PATH.mkdir(parents=True, exist_ok=True)

            build_tools_zip = ZipFile(io.BytesIO(resp.content))
            build_tools_zip.extractall(str(BUILD_TOOLS_PATH))
            return

        raise RuntimeError('Error couldn\'t download build-tools')

    def __download_platform_tools(self):
        download_response = requests.get(PLATFORM_TOOLS_DOWNLOAD_URL.format(os=self.__platform_tools_os))

        if download_response.status_code != DOWNLOAD_SUCCEEDED:
            raise RuntimeError('Error couldn\'t download platform tools')

        PLATFORM_TOOLS_PATH.mkdir(parents=True, exist_ok=True)

        platform_tools_zip = ZipFile(io.BytesIO(download_response.content))
        platform_tools_zip.extractall(str(PLATFORM_TOOLS_PATH))

    def __download_apktool(self):
        apktool_wrapper = requests.get(PLATFORM_TO_APKTOOL_WRAPPER_URL[sys.platform])

        if apktool_wrapper.status_code != DOWNLOAD_SUCCEEDED:
            raise RuntimeError('Couldn\'t download apktool wrapper')

        apktool_releases = requests.get(APKTOOL_RELEASES_URL)
        APKTOOL_URL_PATTERN = r'(/iBotPeaches/apktool/downloads/apktool_\d+\.\d+\.\d+\.jar)'

        for download_path in re.findall(APKTOOL_URL_PATTERN, apktool_releases.text):
            resp = requests.get('https://bitbucket.org' + download_path)

            if resp.status_code != DOWNLOAD_SUCCEEDED:
                continue

            APKTOOL_PATH.mkdir(parents=True, exist_ok=True)
            wrapper_path = APKTOOL_PATH / ('apktool.bat' if sys.platform == 'win32' else 'apktool')

            (APKTOOL_PATH / 'apktool.jar').write_bytes(resp.content)
            (wrapper_path).write_bytes(apktool_wrapper.content)

            ToolsFetcher.__set_executable(wrapper_path)
            return

        raise RuntimeError('Error couldn\'t download build-tools')

    @staticmethod
    def __get_subfolder(root: Path) -> Path:
        subfolders = list(root.glob('./*'))

        if len(subfolders) != 1:
            raise RuntimeError('Error more than one folder')

        return subfolders[0]

    @staticmethod
    def __unpack_subfolder(root: Path) -> str:
        subfolder = ToolsFetcher.__get_subfolder(root)

        for old_path in subfolder.rglob('*'):
            if old_path.is_dir():
                continue

            fname_parts = list(old_path.parts)
            fname_parts.remove(subfolder.name)

            new_path = Path(os.path.join(*fname_parts))
            new_path.parent.mkdir(exist_ok=True, parents=True)

            print('Unpacking', new_path)
            shutil.copy(old_path, new_path)

            ToolsFetcher.__set_executable(new_path)

        shutil.rmtree(subfolder, ignore_errors=True)

    @staticmethod
    def __set_executable(file_path: Path):
        if os.name == 'posix':
            EXECUTE_PERMISSIONS = 0o111
            os.chmod(str(file_path), os.stat(str(file_path)).st_mode | EXECUTE_PERMISSIONS)


def main():
    tools_fetcher = ToolsFetcher()
    tools_fetcher.download_all_tools()


if __name__ == '__main__':
    main()
