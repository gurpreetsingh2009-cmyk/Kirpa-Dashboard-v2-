# Kirpa Firecracker Controller

This module adds Firecracker microVM sandboxing to Kirpa Dashboard v2.
It isolates each skill run inside a microVM for maximum security.

## Usage
- Install Firecracker binary and kernel images.
- Import and call `create_vm(skill_dir, inputs)` from orchestrator.

## Example
```bash
python orchestrator/firecracker_controller.py
```
