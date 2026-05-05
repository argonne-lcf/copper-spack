# copper-spack

Spack packaging and installation instructions for Copper.

This assumes `spack` is already available in your `PATH`. For general Copper build and usage details, see the main project README:

[https://github.com/argonne-lcf/copper/blob/main/README.md](https://github.com/argonne-lcf/copper/blob/main/README.md)

## Install Copper With a Local Spack Repo

```bash
module load cmake
git clone https://github.com/argonne-lcf/copper-spack.git
spack repo add ./copper-spack
spack install copper%oneapi
```

After installation, load Copper with Spack or with the site module:

```bash
spack load copper
```

For deployed environment modules, the common load commands are:

```bash
module load copper            # Aurora
module load ums ums046 copper # Frontier
```

## Variants

The current package intentionally tracks the simplified build interface used by
the recent Copper CMake configuration. The supported variants are:

- ``+block_redundant_rpcs`` / ``~block_redundant_rpcs``
- ``+checksum`` / ``~checksum``

Example:

```bash
spack install copper%oneapi ~block_redundant_rpcs +checksum
```

The ``checksum`` variant is preserved because some deployments want an
explicit choice between ``mercury+checksum`` and ``mercury~checksum``. In the
current package, it controls the Mercury dependency selection rather than a
Copper-specific CMake definition.

## Installed Runtime Layout

The package exports ``PATH`` with the installed ``build/`` runtime directory,
and sets:

- ``COPPER_ROOT``
- ``CUPATH``

The installed ``build/`` directory is expected to contain:

- ``cu_fuse``
- ``cu_fuse_shutdown``
- ``launch_copper_aurora.sh``
- ``launch_copper_frontier.sh``
- ``stop_copper_aurora.sh``
- ``stop_copper_frontier.sh``
- ``aggregate_profiling.py``
- ``list_cxi_hsn_thallium`` when the helper is built
- ``olcf_frontier_copper_addressbook.txt``
- ``alcf_aurora_copper_addressbook.txt``

The launch wrappers choose their facility defaults directly:

- ``launch_copper_aurora.sh`` uses ``alcf_aurora_copper_addressbook.txt``,
  ``cxi``, and service cores ``48,49,50,51``
- ``launch_copper_frontier.sh`` uses ``olcf_frontier_copper_addressbook.txt``,
  ``cxi://cxi1``, and service cores ``1,2``

Use ``-F`` to pass a different facility address-book file.

## Load Copper

If Copper is provided through environment modules, load it with:

```bash
module load copper            # Aurora
module load ums ums046 copper # Frontier
```

If you installed Copper directly with Spack, use:

```bash
spack load copper
```

After loading Copper, the launch wrappers follow the same runtime layout used by
the source tree: ``${COPPER_ROOT}/build`` contains the main Copper binary,
shutdown tool, helper scripts, and staged address-book files.

## Start and Stop Copper

```bash
launch_copper_aurora.sh  [-d log_dir_base] [-v CU_FUSE_MNT_VIEWDIR]
launch_copper_frontier.sh [-d log_dir_base] [-v CU_FUSE_MNT_VIEWDIR]

stop_copper_aurora.sh  [-d log_dir_base] [-v CU_FUSE_MNT_VIEWDIR]
stop_copper_frontier.sh [-d log_dir_base] [-v CU_FUSE_MNT_VIEWDIR]
```
