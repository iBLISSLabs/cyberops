terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  token = "TOKEN DA DIGITAL OCEAN"
}

resource "digitalocean_ssh_key" "ansible_ssh_key" {
  name       = "ansible_ssh_key"
  public_key = file("~/.ssh/id_rsa.pub")
}

resource "digitalocean_droplet" "web" {
  image  = "ubuntu-22-04-x64"
  name   = "zabbix"
  region = "nyc1"
  size   = "s-2vcpu-4gb"
  ssh_keys  = [digitalocean_ssh_key.ansible_ssh_key.fingerprint]
  user_data = <<-EOF
              #!/bin/bash
              apt update
              apt install -y python3 python3-pip
            EOF

  tags = ["monitoramento"]

  connection {
    type        = "ssh"
    user        = "root"
    private_key = file("~/.ssh/id_rsa")
    timeout     = "2m"
    host        = self.ipv4_address
  }

  provisioner "remote-exec" {
    inline = [
      "ufw allow 2222/tcp",
      "ufw allow 10050/tcp",
      "ufw allow 10051/tcp",
      "ufw --force enable",
    ]
  }
}