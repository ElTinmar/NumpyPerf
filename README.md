# NumpyPerf


# Enable 1G hugepages

edit /etc/default/grub
```
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash default_hugepagesz=2MB hugepagesz=1G hugepages=2 hugepagesz=2M hugepages=20"
```
run update-grub and reboot
