from ftplib import FTP

ftp = FTP()
ftp.connect('46.149.233.52', 30)
ftp.login("ftp-admin", "Flvby66!")
print(ftp.login())
print(ftp.dir())

ftp.quit()