Summary:	utftpd - a TFTP server
Summary(pl):	utftpd - serwer TFTP
Name:		utftpd
Version:	0.2.4
Release:	3
License:	GPL
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.ohse.de/uwe/releases/%{name}-%{version}.tar.gz
Source1:	utftpd.inetd
Prereq:		rc-inetd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
utftpd is a server for the trivial file transfer protocol (TFTP) with
finer grained access control then the standard UNIX tftpd.

Description with the features GNU utftpd has:
 - support for IP based access control. utftpd can assign the right to
   read, create or overwrite a file (or files in a directory) on a
   per-host base.
 - support for revision control. utftpd can checkin/out files under
   SCCS or RCS version control. This was one of the main reasons to write
   it: version control is the easiest way to restore the configuration
   our IP routers (Ascends, Ciscos) had yesterday or some weeks ago. This
   is, of course, optional.
 - support for the blksize option (RFC 2348). Allows packets larger
   than the usual 512 bytes, and is _somewhat_ more efficient (especially
   on a directly connected network).
 - support for the timeout option (RFC 2349) No support for the tsize
   option of RFC 2349 now.

%description -l pl
Serwer TFTP.

%prep
%setup -q

%build
LDFLAGS="-s" ;export LDFLAGS
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/sysconfig/rc-inetd,var/lib/tftp}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/utftpd

touch $RPM_BUILD_ROOT%{_sysconfdir}/utftpd.cdb

gzip -9nf AUTHORS ChangeLog NEWS README README.cvs sample.config \
	$RPM_BUILD_ROOT/%{_mandir}/man{1,5,8}/*

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi
touch /etc/utftpd.cdb
chmod 640 /etc/utftpd.cdb

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *gz
%attr(640,root,root) %ghost %{_sysconfdir}/utftpd.cdb
%attr(755,root,root) %{_bindir}/utftp
%attr(755,root,root) %{_sbindir}/utftpd
%attr(755,root,root) %{_sbindir}/utftpd_make
%attr(640,root,root) /etc/sysconfig/rc-inetd/utftpd
%{_mandir}/man8/utftpd_make.8.gz
%{_mandir}/man8/utftpd.8.gz
%{_mandir}/man5/utftpd.conf.5.gz
%{_mandir}/man1/utftp.1.gz
%dir /var/lib/tftp
