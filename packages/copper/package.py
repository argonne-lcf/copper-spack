import os

from spack.package import *
from llnl.util import tty

class Copper(CMakePackage):
    """Copper: Cooperative Caching Layer for Scalable Data Loading in Exascale Supercomputers"""

    # Replace this with the actual URL to download your source code
    homepage = "https://github.com/argonne-lcf/copper"
    url      = "https://github.com/argonne-lcf/copper.git"
    git      = "https://github.com/argonne-lcf/copper.git"
    
    maintainers("kaushikvelusamy", "kevin-harms")

    # Add versions of your software here
    version("main", branch="main")

    # Variants
    variant("block_redundant_rpcs", default=True, description="On off block_redundant_rpcs ")
    variant("checksum", default=True, description="Enable checksum support")

    # Add the dependencies your software requires
    depends_on('pkgconfig')
    depends_on('fuse@3')
    
    # Dependencies — propagate checksum setting to Mercury
    depends_on("mercury@2.4:+checksum", when="+checksum")
    depends_on("mercury@2.4:~checksum", when="~checksum")

    depends_on('cereal@1.3:')
    depends_on('mochi-margo@0.18:')
    depends_on('mochi-thallium@0.14:')
    depends_on('mpi')
    

    def cmake_args(self):
        args = []

        # hardcoded flags
        args.extend([
            self.define('CMAKE_VERBOSE_MAKEFILE', True),
            self.define('CMAKE_EXPORT_COMPILE_COMMANDS', True),
        ])

        # from variants
        args.extend([
            self.define_from_variant("BLOCK_REDUNDANT_RPCS", "block_redundant_rpcs"),
            self.define_from_variant("ENABLE_CHECKSUM", "checksum"),
        ])

        # Warnings to user
        if self.spec.satisfies("+checksum"):
            tty.warn("Checksum support is ENABLED — stronger data integrity, may reduce performance.")
        else:
            tty.warn("Checksum support is DISABLED — faster, but less safe.")

        return args
