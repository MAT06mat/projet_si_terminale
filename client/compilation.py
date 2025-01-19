import sys, os
from colorama import init, Fore, Style


# Init Colorama
init(autoreset=True)


if sys.platform not in ("linux", "linux2"):
    raise Exception("Bad platform, try on linux")


commands = (
    "rm -rf bin",
    "rm -rf app",
    'echo "Update..."',
    "mkdir app",
    "cp -R /mnt/rcm/app/. app/.",
    "rm -rf buildozer.spec",
    "cp -R /mnt/rcm/buildozer.spec buildozer.spec",
    'echo "Update of buildozer.spec and app/ completed"',
    "buildozer --verbose android debug",
)

for command in commands:
    os.system(command)

from app.main import __version__

print(
    f"\n\n{Style.BRIGHT}{Fore.GREEN}#     Compilation finished !\n{Fore.BLACK}#     File rcm-{__version__}-armeabi-v7a_arm64-v8a-debug.apk is available in /bin directory !"
)
