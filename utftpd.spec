Summary:	utftpd - a TFTP server
Summary(pl):	utftpd - serwer TFTP
Name:		utftpd
Version:	0.2.0
Release:	1
Copyright:	GPL
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source:		ftp://ftp.ohse.de/uwe/releases/utftpd-0.2.0.tar.gz
BuildRoot:	/tmp/%{name}-%{version}-root

%description
A TFTP server.

%description -l pl
Serwer TFTP.

%prep
%setup -q

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

gzip -9nf AUTHORS ChangeLog NEWS README README.cvs \
	$RPM_BUILD_ROOT/%{_mandir}/man{1,5,8}/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {AUTHORS,ChangeLog,NEWS,README,README.cvs}.gz
%attr(755,root,root) %{_bindir}/utftp
%attr(755,root,root) %{_sbindir}/utftpd
%attr(755,root,root) %{_sbindir}/utftpd_make
%{_mandir}/man8/utftpd_make.8.gz
%{_mandir}/man8/utftpd.8.gz
%{_mandir}/man5/utftpd.conf.5.gz
%{_mandir}/man1/utftp.1.gz
