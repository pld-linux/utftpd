Summary: utftpd - a TFTP server
Name: utftpd
Version: 0.2.0
Release: 0
Copyright: GPL
Group: Applications/Communications
Source: ftp://ftp.ohse.de/uwe/releases/utftpd-0.2.0.tar.gz
BuildRoot:	/tmp/%{name}-%{version}-root

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
%{_bindir}/utftp
%{_sbindir}/utftpd
%{_sbindir}/utftpd_make
%{_mandir}/man8/utftpd_make.8
%{_mandir}/man8/utftpd.8
%{_mandir}/man5/utftpd.conf.5
%{_mandir}/man1/utftp.1

%clean
rm -rf $RPM_BUILD_ROOT
