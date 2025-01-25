import sys, os
from colorama import init, Fore, Style


# Init Colorama
init(autoreset=True)

# Raise error if script isn't launch on linux
if sys.platform not in ("linux", "linux2"):
    raise Exception("Bad platform, try on linux")


def update_files():
    # Update code on vm
    os.system("rm -rf bin")
    os.system("rm -rf app")
    print("Update ...")
    os.system("mkdir app")
    os.system("cp -R /mnt/rcm/app/. app/.")
    os.system("mkdir app/mods")
    os.system("cp -R /mnt/rcm/mods/. app/mods/.")
    os.system("rm -rf buildozer.spec")
    os.system("cp -R /mnt/rcm/buildozer.spec buildozer.spec")
    print("Update of buildozer.spec and app/ completed")

    from app.main import __version__

    return __version__


def add_requirements():
    # Add requirements on buildozer.spec file
    with open("app/mods/buildozer_requirements.txt") as req_file:
        dependencies = req_file.read().strip().replace("\n", ",")

    with open("buildozer.spec", "r") as spec_file:
        content = spec_file.readlines()

    for i, line in enumerate(content):
        if line.startswith("requirements ="):
            content[i] = (
                f"requirements = python3==3.11.2,hostpython3==3.11.2,kivy,{dependencies}\n"
            )
            break

    with open("buildozer.spec", "w") as spec_file:
        spec_file.writelines(content)


def start_compilation():
    # Start buildozer compilation
    os.system("buildozer --verbose android debug")

    print(f"\n\n{Style.BRIGHT}{Fore.GREEN}     Compilation finished !\n\n{Fore.BLACK}")


def copy_apk(version):
    rep = input("Do you want a copy out of the vm ? (y/n) ")
    if rep.lower() == "y":
        os.system(
            f"cp -R ./bin/rcm-{version}-armeabi-v7a_arm64-v8a-debug.apk /mnt/rcm/rcm-{version}-armeabi-v7a_arm64-v8a-debug.apk"
        )
        print(f"{Style.BRIGHT}{Fore.GREEN}Copy done !{Fore.BLACK}")


def main():
    version = update_files()
    add_requirements()
    start_compilation()
    copy_apk(version)


if __name__ == "__main__":
    main()
