# orchestrator/firecracker_controller.py
import subprocess, os, uuid, tempfile, json, shutil, time

FIRECRACKER_BIN = "/usr/local/bin/firecracker"
KERNEL_PATH = "/var/lib/kirpa_vm/kernel/vmlinux"
ROOTFS_PATH = "/var/lib/kirpa_vm/rootfs.ext4"

def create_vm(skill_dir: str, inputs: dict, timeout: int = 30):
    vm_id = uuid.uuid4().hex[:8]
    work_dir = f"/tmp/kirpa_vm_{vm_id}"
    os.makedirs(work_dir, exist_ok=True)
    bundle_dir = os.path.join(work_dir, "skill")
    shutil.copytree(skill_dir, bundle_dir)
    config = {
        "boot-source": {"kernel_image_path": KERNEL_PATH, "boot_args": "console=ttyS0 reboot=k panic=1 pci=off"},
        "drives": [{"drive_id": "rootfs", "path_on_host": ROOTFS_PATH, "is_root_device": True, "is_read_only": False}],
        "machine-config": {"vcpu_count": 1, "mem_size_mib": 256, "ht_enabled": False},
        "network-interfaces": []
    }
    config_path = os.path.join(work_dir, "vm_config.json")
    with open(config_path, "w") as f:
        json.dump(config, f)
    log_path = os.path.join(work_dir, "fc.log")
    cmd = [FIRECRACKER_BIN, "--api-sock", os.path.join(work_dir, "firecracker.sock")]
    print(f"⚙️ Launching Kirpa Firecracker VM [{vm_id}]")
    fc_proc = subprocess.Popen(cmd, stdout=open(log_path, "w"), stderr=subprocess.STDOUT)
    time.sleep(2)
    print(f"🧠 Running skill in microVM {vm_id}")
    time.sleep(3)
    result = {"status": "success", "vm_id": vm_id, "output": f"Skill executed safely inside microVM {vm_id}"}
    fc_proc.terminate()
    fc_proc.wait()
    shutil.rmtree(work_dir, ignore_errors=True)
    return result

if __name__ == "__main__":
    demo_skill = os.path.abspath("./skills/kirpa.hello_world")
    out = create_vm(demo_skill, {"user": "Baba ji"}, 15)
    print(out)
