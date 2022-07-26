provider "yandex" {
  cloud_id  = "${var.yandex_cloud_id}"
  folder_id = "${var.yandex_folder_id}"
  zone                      = "ru-central1-a"
}

data "yandex_iam_user" "kofe88" {
  login = "fedorov.kofe88"
}

data "yandex_iam_service_account" "my-netology" {
  service_account_id = "ajesg66dg5r1ahte7mqd"
}

resource "yandex_compute_instance" "node01" {

  platform_id = local.platform_type[terraform.workspace]

  count = local.vm_count[terraform.workspace]

  name                      = "node01-${count.index+1}-${terraform.workspace}"
  zone                      = "ru-central1-a"
  hostname                  = "node01-${count.index+1}-${terraform.workspace}.netology.cloud"
  allow_stopping_for_update = true

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id    = "${var.ubuntu-base}"
      name        = "root-node01-${count.index+1}-${terraform.workspace}"
      type        = "network-nvme"
      size        = "10"
    }
  }

  network_interface {
    subnet_id = "${yandex_vpc_subnet.default.id}"
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  }

}

resource "yandex_compute_instance" "node02" {

  for_each = {for index, vm in local.prod: index => vm
  if vm.work == terraform.workspace}


  platform_id = each.value.type

  name                      = "node02-${each.value.index+1}-${terraform.workspace}"
  zone                      = "ru-central1-a"
  hostname                  = "node02-${each.value.index+1}-${terraform.workspace}.netology.cloud"
  allow_stopping_for_update = true

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id    = "${var.ubuntu-base}"
      name        = "root-node02-${each.value.index+1}-${terraform.workspace}"
      type        = "network-nvme"
      size        = "15"
    }
  }

  network_interface {
    subnet_id = "${yandex_vpc_subnet.default.id}"
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  }

}

