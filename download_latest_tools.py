import io
import re
import sys
import requests
from pathlib import Path
from zipfile import ZipFile
from os.path import expanduser

BUILD_TOOLS_PATH = Path(expanduser('~/.reltools/builadpp_build_tools'))

BUILD_TOOLS_PATTERN = r'Build Tools, Revision (\d+)\.(\d+)\.(\d+)'
BUILD_TOOLS_RELEASES = 'https://developer.android.com/tools/releases/build-tools'
BUILD_TOOLS_DOWNLOAD_URL = 'https://dl.google.com/android/repository/build-tools_r{version}-{os}.zip'

PLATFORM_TO_OS = {
    'linux': 'linux',
    'darwin': 'macosx',
    'win32': 'windows',
}


def main():
    platform_os = PLATFORM_TO_OS[sys.platform]
    releases = requests.get(BUILD_TOOLS_RELEASES)

    for major, minor, patch in re.findall(BUILD_TOOLS_PATTERN, releases.text):
        download_responses = list(filter(
            lambda response: response.status_code == 200,
            (
                requests.get(BUILD_TOOLS_DOWNLOAD_URL.format(version=f'{major}', os=platform_os)),
                requests.get(BUILD_TOOLS_DOWNLOAD_URL.format(version=f'{major}.{minor}.{patch}', os=platform_os))
            )
        ))

        if download_responses:
            BUILD_TOOLS_PATH.mkdir(parents=True, exist_ok=True)

            build_tools_zip = ZipFile(io.BytesIO(download_responses[0].content))
            build_tools_zip.extractall(str(BUILD_TOOLS_PATH))
            break
    else:
        raise Exception('Error couldn\'t download build-tools')


if __name__ == '__main__':
    main()
