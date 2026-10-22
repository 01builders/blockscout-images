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

## Frontend Node security rebuild

The frontend workflow keeps upstream `v2.10.3` at commit
`10d8428db2f3b5a832640ea2e68ddcc33eff3a49` and builds the reviewed packaging
revision `ghcr.io/01builders/blockscout-frontend:2.10.3-02`. Before building, it
checks the original Dockerfile SHA-256 and exact three Node base stages, then
changes only `node:22.14.0-alpine` to `node:22.23.4-alpine` for dependencies,
building and runtime. The patch refuses changed input before writing. This
keeps upstream revision verification and SBOM/provenance enabled.

The [October Node security advisory](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases)
sets 22.23.4 as the patched release. An approved merge/manual build publishes
this new image tag; this source PR does not build, publish, or deploy it. Existing
deployments using `2.10.3-01` must explicitly adopt the new image after build and
startup validation. Upstream repositories and the backend image recipes are
unchanged. GitHub Actions' embedded Node runtime is controlled by the runner
and must also be patched independently of the image base.
