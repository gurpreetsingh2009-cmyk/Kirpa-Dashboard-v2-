# Kirpa Dashboard v2 – Autonomous Skill Ecosystem
# Production Deployment — Kirpa Orchestrator Sandbox Guide

**Goal:** Run Kirpa orchestrator with strong isolation for untrusted skills.
Options:
- **Recommended (high-security):** Firecracker microVMs for each untrusted skill execution.
- **Balanced (performance + isolation):** gVisor or Kata Containers.
- **Dev (NOT for untrusted code):** Docker with seccomp/AppArmor (provided in repo).

## 1) Firecracker (recommended)
- Install Firecracker on Linux host (KVM required). See: https://github.com/firecracker-microvm/firecracker
- Build minimal rootfs image with required runtimes (python slim) for skill execution.
- Use `containerd` + `firecracker-containerd` or manage microVM lifecycle using a controller (e.g., Nomad/Custom).
- Each skill run: spawn microVM, copy skill bundle, run, capture stdout/stderr, destroy microVM.

### systemd service (controller example)
`/etc/systemd/system/kirpa-orchestrator.service`
