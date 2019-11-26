import ftplib


ftp = ftplib.FTP()


if __name__ == '__main__':

	print('Connect to FTP-server ...')
	print(ftp.connect('192.168.25.222'))

	print('Login in FTP-server ...')
	ftp.login('ftp-admin', 'Flvby66!')

	ftp.set_debuglevel(2)
	ftp.set_pasv(False)
	# ftp.sendcmd('PORT 195,70,215,179,78,89')
	
	print(ftp.nlst())

	ftp.quit()
