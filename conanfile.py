from conans import ConanFile, CMake, tools
import os


class LibqrencodeConan(ConanFile):
    name = "libqrencode"
    version = "4.0.0"
    url = "https://github.com/bincrafters/conan-libqrencode"
    homepage = "https://github.com/fukuchi/libqrencode"
    description = "A fast and compact QR Code encoding library"
    topics = ("conan", "libqrencode")
    license = ("LGPL-2.1, LGPL-3.0")
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "sources.patch"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, 'fPIC': True}
    requires = (
        "libiconv/1.15", 
        "libpng/1.6.37"
    )
    
    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        tools.patch(base_path=extracted_dir, patch_file="sources.patch")
        #Rename to "sources" is a convention to simplify later steps
        os.rename(extracted_dir, "sources")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["WITH_TOOLS"] = False
        cmake.definitions["WITH_TESTS"] = False
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy(pattern="qrencode.h", dst="include", src="sources", keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="lib", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
