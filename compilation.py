import importlib, sys, os
from colorama import init, Fore, Style


# Init Colorama
init(autoreset=True)

# Raise error if script isn't launch on linux
if sys.platform not in ("linux", "linux2"):
    raise Exception("Bad platform, try on linux")


class CustomCommands:
    before_build = ["mkdir app/mods", "cp -R /mnt/rcm/mods/. app/mods/."]
    after_build = []


class Config:
    name = "rcm"
    version_file = "app/main.py"
    shared_dir = "/mnt/rcm/"
    updates = ["app", "buildozer.spec"]
    clean_bin = True
    custom_commands = CustomCommands()
    requirements = "app/mods/buildozer_requirements.txt"
    archs = "armeabi-v7a_arm64-v8a"


class Compiler:
    def __init__(self):
        self.config = Config()
        self.green = Style.BRIGHT + Fore.GREEN
        self.gray = Style.BRIGHT + Fore.BLUE

    def update_requirements(self):
        # Add requirements on buildozer.spec file
        with open(self.config.requirements) as req_file:
            requirements = req_file.read().strip().replace("\n", ",")

        with open("buildozer.spec", "r") as spec_file:
            content = spec_file.readlines()

        for i, line in enumerate(content):
            if line.startswith("requirements ="):
                content[i] = f"requirements = {requirements}\n"
                break

        with open("buildozer.spec", "w") as spec_file:
            spec_file.writelines(content)

    def prebuild(self):
        version_file = self.config.version_file.replace("/", ".").replace("\\", ".")
        self.version = importlib.import_module(version_file.strip(".py")).__version__

        if self.config.clean_bin:
            os.system("rm -rf bin")
            print(f"{self.gray}# bin/ removed")

        for file in self.config.updates:
            os.system(f"rm -rf {file}")
            file += "/." if os.path.isdir(file) else ""
            os.system(f"cp -R {self.config.shared_dir}{file} {file}")
            print(f"{self.gray}# {file} updated")

        for command in self.config.custom_commands.before_build:
            os.system(command)

        self.update_requirements()

    def postbuild(self, ext):
        print(f"\n\n{self.green}     Compilation finished !\n\n")
        rep = input(f"{self.gray}Do you want a copy out of the vm ? (y/n) ")
        if rep.lower() == "y":
            apk_vars = [self.config.name, self.version, self.config.archs, ext]
            apk_name = "-".join(apk_vars)
            os.system(f"cp -R bin/{apk_name} {self.config.shared_dir}{apk_name}")
            print(f"{self.green}Copy done !")

    def debug(self):
        self.prebuild()
        os.system("buildozer --verbose android debug")
        self.postbuild("debug.apk")

    def release(self):
        self.prebuild()
        os.system("buildozer --verbose android release")
        self.postbuild("release.aab")


if __name__ == "__main__":
    Compiler().debug()
