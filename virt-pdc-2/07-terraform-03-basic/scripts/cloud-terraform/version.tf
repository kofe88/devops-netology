terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  backend "s3" {
    endpoint   = "storage.yandexcloud.net"
    bucket     = "my-netology-bucket"
    region     = "ru-central1-a"
    key        = "./state.tfstate"
    workspace_key_prefix = ""
    access_key = "YCA*"
    secret_key = "YCM*"

    skip_region_validation      = true
    skip_credentials_validation = true
  }

}
