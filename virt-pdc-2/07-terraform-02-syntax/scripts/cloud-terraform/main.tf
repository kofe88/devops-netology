provider "yandex" {
  cloud_id  = "${var.yandex_cloud_id}"
  folder_id = "${var.yandex_folder_id}"
}

resource "yandex_compute_image" "root-node01-image" {
  name         = "root-node01-image"
  source_image = "${var.centos-7-base}"
  }

data "yandex_iam_user" "kofe88" {
  login = "fedorov.kofe88"
}

data "yandex_iam_service_account" "kofe88" {
  service_account_id = "ajesg66dg5r1ahte7mqd"
}

resource "yandex_compute_instance" "node01" {
  name                      = "node01"
  zone                      = "ru-central1-a"
  hostname                  = "node01.netology.cloud"
  allow_stopping_for_update = true

  resources {
    cores  = 2
    memory = 4
  }

boot_disk {
    initialize_params {
      image_id    = "${var.centos-7-base}"
      name        = "root-node01"
      type        = "network-nvme"
      size        = "50"
    }
  }

  network_interface {
    subnet_id = "${yandex_vpc_subnet.default.id}"
    nat       = true
  }

}
