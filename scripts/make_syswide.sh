sudo cp -r $PWD /usr/share
sudo cp -r others/kernel_auditor.service /etc/systemd/system
sudo systemctl enable --now kernel_auditor.service