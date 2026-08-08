# Blockscout images

This repository builds the Blockscout backend image used by 01builders infrastructure.

## Current image

The workflow builds upstream Blockscout `v10.2.6` at commit
`90f7dd8e9348123b74dfd23f69ab7da76191a820` and publishes:

```text
ghcr.io/01builders/blockscout:10.2.6-01
```

The image is built only for `linux/amd64`, which is the architecture of the
Collect Testnet web host. The image includes an SBOM and build provenance.

## Deployment

After the workflow succeeds, retrieve the published digest and pin it in the
explorer Compose file:

```yaml
image: ghcr.io/01builders/blockscout:10.2.6-01@sha256:<digest>
```

Do not deploy the mutable tag without its digest. Before updating a host,
confirm that the package permits unauthenticated pulls; the testnet currently
does not supply GHCR credentials.

## Rebuilds

The workflow runs on its initial merge to `main` and can be rerun manually.
Changing the upstream ref or commit requires a reviewed workflow change.
