Summary:	utftpd - a TFTP server
Summary(pl):	utftpd - serwer TFTP
Name:		utftpd
Version:	0.2.4
Release:	13
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.ohse.de/uwe/releases/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Source2:	%{name}.conf
URL:		http://www.ohse.de/uwe/software/utftpd.html
BuildRequires:	autoconf
PreReq:		rc-inetd
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/userdel
Provides:	tftpdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	tftpa-hpa
Obsoletes:	tftpd
Obsoletes:	tftp-server

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
Pakiet utftpd zawiera serwer TFTP z kontrol± dostêpu wieksz± ni¿
standardowy serwer tftpd.

Opis mo¿liwo¶ci serwera GNU utftpd:
 - wsparcie dla kontroli dostêpu per IP. utftpd mo¿e przypisywaæ prawa
   zapisu, odczytu, tworzenia plików i ich nadpisywania bazuj±æ na
   nazwach hostów z których s± wykonywane te operacje.
 - wsparcie do systemów kontroli wersji jak RCS, SCCS czy CVS.
   Umo¿liwia to np. odtworzenie poprzedniej wersji pliku np. z
   konfiguracj± routera jaka zosta³a zesk³adowana na serwerze z u¿yciem
   TFTP. Jest to oczywiscie cecha opcjonalna.
 - wsparcie do opcji blksize (RFC 2348). Umozliwia ona u¿ywanie
   pakietów wiêkszych ni¿ standardowe 512 bajtów co jest nieco bardziej
   efektywne (szczególnie przy komunikacji bezpo¶eniej).
 - mo¿liwo¶ci ustalania opcji timeout (RFC 2349). Brak jednocze¶nie na
   razie ustawiania opcji tsize (RFC 2349).

%package client
Summary:	utftpd - a TFTP client
Summary(pl):	utftpd - klient TFTP
Group:		Networking/Utilities

%description client
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

This package contains utftp client only.

%description -l pl client
Pakiet utftpd zawiera serwer TFTP z kontrol± dostêpu wieksz± ni¿
standardowy serwer tftpd.

Opis mo¿liwo¶ci serwera GNU utftpd:
 - wsparcie dla kontroli dostêpu per IP. utftpd mo¿e przypisywaæ prawa
   zapisu, odczytu, tworzenia plików i ich nadpisywania bazuj±æ na
   nazwach hostów z których s± wykonywane te operacje.
 - wsparcie do systemów kontroli wersji jak RCS, SCCS czy CVS.
   Umo¿liwia to np. odtworzenie poprzedniej wersji pliku np. z
   konfiguracj± routera jaka zosta³a zesk³adowana na serwerze z u¿yciem
   TFTP. Jest to oczywiscie cecha opcjonalna.
 - wsparcie do opcji blksize (RFC 2348). Umozliwia ona u¿ywanie
   pakietów wiêkszych ni¿ standardowe 512 bajtów co jest nieco bardziej
   efektywne (szczególnie przy komunikacji bezpo¶eniej).
 - mo¿liwo¶ci ustalania opcji timeout (RFC 2349). Brak jednocze¶nie na
   razie ustawiania opcji tsize (RFC 2349).

Ten pakiet zawiera tylko klienta utftp.

%prep
%setup -q

%build
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/sysconfig/rc-inetd,var/lib/tftp}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/utftpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/utftpd.conf

touch $RPM_BUILD_ROOT%{_sysconfdir}/{utftpd.cdb,utftpd.conf}

%clean
rm -rf $RPM_BUILD_ROOT

%pre -n utftpd
if [ -n "`id -u tftp 2>/dev/null`" ]; then
	if [ "`id -u tftp`" != "15" ]; then
		echo "Error: user tftp doesn't have uid=15. Correct this before installing utftpd." 1>&2
		exit 1
	fi
else
	echo "Adding user tftp UID=15."
	/usr/sbin/useradd -u 15 -r -d /var/lib/tftp -s /bin/false -c "TFTP User" -g ftp tftp 1>&2
fi

%post -n utftpd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server." 1>&2
fi
echo -n "Rebuilding utftpd configuration... "
utftpd_make /etc/utftpd.cdb /etc/utftp.tmp /etc/utftpd.conf
echo "done"

%postun -n utftpd
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart
fi

if [ "$1" = "0" ]; then
	echo "Removing user tftp."
	/usr/sbin/userdel tftp
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README README.cvs sample.config
%attr(640,root,root) %ghost %{_sysconfdir}/utftpd.cdb
%attr(644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/utftpd.conf
%attr(755,root,root) %{_sbindir}/utftpd
%attr(755,root,root) %{_sbindir}/utftpd_*
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/rc-inetd/utftpd
%{_mandir}/man5/utftpd*.5*
%{_mandir}/man8/utftpd*.8*
%attr(750,tftp,root) %dir /var/lib/tftp

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/utftp
%{_mandir}/man1/utftp.1*
