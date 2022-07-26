output "internal_ip_address_node01_yandex_cloud" {
  value = "${yandex_compute_instance.node01.*.network_interface.0.ip_address}"
}

output "internal_ip_address_node02_yandex_cloud" {
  value = "${values(yandex_compute_instance.node02).*.network_interface.0.ip_address}"
}


output "external_ip_address_node01_yandex_cloud" {
  value = "${yandex_compute_instance.node01.*.network_interface.0.nat_ip_address}"
}

output "external_ip_address_node02_yandex_cloud" {
  value = "${values(yandex_compute_instance.node02).*.network_interface.0.nat_ip_address}"
}

output "yc_account_ID" {
  value = "${data.yandex_iam_service_account.my-netology.service_account_id}"
}

output "yc_user_ID" {
  value = "${data.yandex_iam_user.kofe88.user_id}"
}

output "node01_zone" {
  value = "${yandex_compute_instance.node01.*.zone}"
}

output "internal_subnet_id_node01_yandex_cloud" {
  value = "${yandex_compute_instance.node01.*.network_interface.0.subnet_id}"
}

output "workspace" {
  value = "${terraform.workspace}"
}
