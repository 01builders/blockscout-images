# Blockscout images

This repository builds and pushes Blockscout Docker images to GitHub Container
Registry.

The current workflow builds upstream Blockscout `v10.2.6` at commit
`90f7dd8e9348123b74dfd23f69ab7da76191a820` and pushes:

```text
ghcr.io/01builders/blockscout:10.2.6-01
```

The image is built for `linux/amd64` and includes an SBOM and build provenance.

## Rebuilds

The workflow runs on its initial merge to `main` and can be rerun manually.
Changing the upstream ref or commit requires a reviewed workflow change.
