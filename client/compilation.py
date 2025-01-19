import sys, os
from colorama import init, Fore, Style


# Init Colorama
init(autoreset=True)

# Raise error if script isn't launch on linux
if sys.platform not in ("linux", "linux2"):
    raise Exception("Bad platform, try on linux")

# Update code on vm
os.system("rm -rf bin")
os.system("rm -rf app")
print("Update ...")
os.system("mkdir app")
os.system("cp -R /mnt/rcm/app/. app/.")
os.system("rm -rf buildozer.spec")
os.system("cp -R /mnt/rcm/buildozer.spec buildozer.spec")
print("Update of buildozer.spec and app/ completed")

# Start buildozer compilation
os.system("buildozer --verbose android debug")
from app.main import __version__

print(f"\n\n{Style.BRIGHT}{Fore.GREEN}#     Compilation finished !\n{Fore.BLACK}#")

rep = input("Do you want a copy out of the vm ? (y/n) ")
if rep.lower() == "y":
    os.system(
        f"cp -R ./bin/rcm-{__version__}-armeabi-v7a_arm64-v8a-debug.apk /mnt/rcm/rcm-{__version__}-armeabi-v7a_arm64-v8a-debug.apk"
    )
    print("Copy done !")
