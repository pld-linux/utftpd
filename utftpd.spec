Summary: utftpd - a TFTP server
Name: utftpd
Version: 0.2.0
Release: 0
Copyright: GPL
Group: Applications/Communications
Source: ftp://ftp.ohse.de/uwe/releases/utftpd-0.2.0.tar.gz
BuildRoot: /var/tmp/utftpd-root

%description
A TFTP server.

%prep
%setup

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

make prefix=$RPM_BUILD_ROOT/usr install

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README README.cvs
/usr/bin/utftp
/usr/sbin/utftpd
/usr/sbin/utftpd_make
/usr/man/man8/utftpd_make.8
/usr/man/man8/utftpd.8
/usr/man/man5/utftpd.conf.5
/usr/man/man1/utftp.1

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon Apr 5 1999 Uwe Ohse <uwe@ohse.de>
- brought in line with utftpd-0.1.4 release
* Sun Mar 28 1999 Uwe Ohse <uwe@ohse.de>
- created it.
