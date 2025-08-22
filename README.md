# copper-spack

This is a spack environment for copper.

## How to install Copper with local spack

This assume that you have a valid `spack` in your path

```
module load cmake
spack install mochi-thallium%oneapi
git clone https://github.com/argonne-lcf/copper-spack.git
spack repo add ./copper-spack/
spack install copper%oneapi
```

Then you can simply load copper  via

```
spack load copper
```

* Default build is **with checksum enabled** (`+checksum`), pulling `mercury@2.4:+checksum`.
* If you run `spack install copper ~checksum`, it disables checksum in both Copper and Mercury.

## How to load Copper on Aurora


```
module load copper
```
