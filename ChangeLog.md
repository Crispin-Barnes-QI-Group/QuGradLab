# [QuGradLab](README.md) Change Log

## Release 0.2.0

- Added `SpinChain` within the rotating wave approximation: `systems.semiconducting.esr.rotating_wave_approximation.SpinChain`. The interface is the same as `systems.semiconducting.esr.SpinChain`.
- Updated the GitHub actions:
    - `actions/checkout@v4` -> `actions/checkout@v7`
    - `actions/setup-python@v5` -> `actions/setup-python@v6`
    - `actions/upload-artifact@v4` -> `actions/upload-artifact@v7`
    - `actions/download-artifact@v4` -> `actions/download-artifact@v8`

This release supports the article:

> Henrik Gothen, Christopher K. Long, Djamila Hiller, Yunming Qian, Crispin H. W. Barnes, Normann Mertig, and David R. M. Arvidsson-Shukur. Pulse-optimised circuit elements for scalable and noise-resilient quantum chemistry. 2026. doi: https://doi.org/10.48550/arXiv.2606.17357. arXiv: 2606.17357 [quant-ph]

### New contributor

- Henrik Gothen
    - https://github.com/hgothen
    - https://orcid.org/0009-0006-3764-4805

## Release 0.1.2

### Bug fixes
- Fixed bug in which the dependencies were not automatically installed.

### Continuous Integration (CI) updates
- Added CI build support for Python 3.13
    - 3.14 will be added in the future when [TensorFlow](https://www.tensorflow.org) has 3.14 support

### Updated Metadata
- Corrected author names
- Added additional package classifiers
- Added version pins to `README.md`
- Updated keywords in `pyproject.toml`

## Release 0.1.1

Fixed typo in README.

## Release 0.1.0

This is the initial release. Future changes to this release will be documented above. Note that all versions ``0.*`` may have unstable APIs.