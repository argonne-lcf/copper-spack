import os

from spack_repo.builtin.build_systems.cmake import CMakePackage
from spack.package import *


class Copper(CMakePackage):
    """Copper: Cooperative Caching Layer for Scalable Data Loading in Exascale Supercomputers."""

    homepage = "https://github.com/argonne-lcf/copper"
    url = "https://github.com/argonne-lcf/copper.git"
    git = "https://github.com/argonne-lcf/copper.git"

    maintainers("kaushikvelusamy", "kevin-harms")

    version("main", branch="main")

    variant(
        "block_redundant_rpcs",
        default=True,
        description="Enable duplicate-RPC suppression in Copper forwarding paths",
    )
    variant(
        "checksum",
        default=True,
        description="Build against checksum-enabled Mercury",
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("cmake", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("fuse@3")
    depends_on("mercury@2.4:+checksum", when="+checksum")
    depends_on("mercury@2.4:~checksum", when="~checksum")
    depends_on("cereal@1.3:")
    depends_on("mochi-margo@0.18:")
    depends_on("mochi-thallium@0.14:")
    depends_on("mpi")

    def cmake_args(self):
        return [
            self.define("CMAKE_VERBOSE_MAKEFILE", True),
            self.define("CMAKE_EXPORT_COMPILE_COMMANDS", True),
            self.define_from_variant("BLOCK_REDUNDANT_RPCS", "block_redundant_rpcs"),
        ]

    def install(self, spec, prefix):
        super().install(spec, prefix)

        runtime_build_dir = join_path(prefix, "build")
        mkdirp(runtime_build_dir)

        # Copper launch wrappers expect a build-style runtime layout with the
        # binaries, helper scripts, and staged address-book files under
        # ${COPPER_ROOT}/build.
        runtime_artifacts = [
            "cu_fuse",
            "cu_fuse_shutdown",
            "list_cxi_hsn_thallium",
            "launch_copper.sh",
            "stop_copper.sh",
            "aggregate_profiling.py",
            "olcf_frontier_copper_addressbook.txt",
            "alcf_aurora_copper_addressbook.txt",
        ]

        for artifact in runtime_artifacts:
            source_path = join_path(self.build_directory, artifact)
            if os.path.exists(source_path):
                install(source_path, join_path(runtime_build_dir, artifact))

    def setup_run_environment(self, env):
        runtime_build_dir = join_path(self.prefix, "build")

        env.set("COPPER_ROOT", self.prefix)
        env.set("CUPATH", join_path(runtime_build_dir, "cu_fuse"))
        env.set(
            "facility_address_book",
            join_path(runtime_build_dir, "olcf_frontier_copper_addressbook.txt"),
        )
        env.prepend_path("PATH", runtime_build_dir)
