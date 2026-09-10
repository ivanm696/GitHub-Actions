packer {
  required_plugins {
    qemu = {
      version = ">= 1.1.0"
      source  = "github.com/hashicorp/qemu"
    }
  }
}

variable "iso_url" {
  type    = string
  default = "https://cloud-images.ubuntu.com/releases/24.04/release/ubuntu-24.04-server-cloudimg-amd64.img"
}

variable "iso_checksum" {
  type    = string
  default = "none" # Replace with the real SHA256 from the Ubuntu cloud-images release page before real builds.
}

variable "disk_size" {
  type    = string
  default = "10240" # MB
}

variable "memory" {
  type    = number
  default = 2048
}

source "qemu" "remarka_base" {
  iso_url          = var.iso_url
  iso_checksum     = var.iso_checksum
  output_directory = "output/remarka-base"
  shutdown_command = "sudo shutdown -P now"
  disk_size        = var.disk_size
  format           = "qcow2"
  accelerator      = "kvm"
  memory           = var.memory
  cpus             = 2

  # cloud-init seed — Packer serves this over HTTP to the VM on first boot
  cd_files = [
    "./cloud-init/meta-data",
    "./cloud-init/user-data",
  ]
  cd_label = "cidata"

  ssh_username = "ubuntu"
  ssh_timeout  = "20m"

  vm_name = "remarka-base.qcow2"
}

build {
  name    = "remarka-base-image"
  sources = ["source.qemu.remarka_base"]

  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y docker.io docker-compose-plugin",
      "sudo systemctl enable docker",
    ]
  }

  provisioner "file" {
    source      = "../../apps/api"
    destination = "/tmp/remarka-api"
  }

  post-processor "checksum" {
    checksum_types = ["sha256"]
    output         = "output/remarka-base/remarka-base.{{.ChecksumType}}"
  }
}
