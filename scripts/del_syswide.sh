sudo systemctl disable --now kernel_auditor.service
sudo rm -rf /usr/share/kernel_auditor
sudo rm -rf /etc/systemd/system/kernel_auditor.service