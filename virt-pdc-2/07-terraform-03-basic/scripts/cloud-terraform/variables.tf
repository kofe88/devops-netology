# https://console.cloud.yandex.ru/cloud?section=overview
variable "yandex_cloud_id" {
  default = "b1gg2ftubre1m9grd2id"
}

# https://console.cloud.yandex.ru/cloud?section=overview
variable "yandex_folder_id" {
  default = "b1g7sa087ssu373i3ubo"
}

# ID yc compute image list
variable "ubuntu-base" {
  default = "fd8kam7tt1fqoc8iv4bq"
}

locals {
  platform_type = {
       stage = "standard-v1"
       prod = "standard-v2"
     }
  vm_count = {
    stage = 1
    prod = 2
  }
}

locals {
  prod = [
    {
    type = "standard-v2"
    work = "prod"
    index = 1
    },
    {
    type = "standard-v2"
    work = "prod"
    index = 2
    },
    {
    type = "standard-v1"
    work = "stage"
    index = 3
    }

  ]
}
