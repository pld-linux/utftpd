Summary:	utftpd - a TFTP server
Summary(pl):	utftpd - serwer TFTP
Name:		utftpd
Version:	0.2.4
Release:	19
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.ohse.de/uwe/releases/%{name}-%{version}.tar.gz
# Source0-md5:	3adf5d86c7b6d83d8ec4099e54e8dede
Source1:	%{name}.inetd
Source2:	%{name}.conf
URL:		http://www.ohse.de/uwe/software/utftpd.html
BuildRequires:	autoconf
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires:	rc-inetd
Provides:	tftpdaemon
Provides:	user(tftp)
Obsoletes:	atftpd
Obsoletes:	inetutils-tftpd
Obsoletes:	tftp-server
Obsoletes:	tftpd
Obsoletes:	tftpd-hpa
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
Pakiet utftpd zawiera serwer TFTP z kontrol� dost�pu wieksz� ni�
standardowy serwer tftpd.

Opis mo�liwo�ci serwera GNU utftpd:
- wsparcie dla kontroli dost�pu per IP. utftpd mo�e przypisywa� prawa
  zapisu, odczytu, tworzenia plik�w i ich nadpisywania bazuj�� na
  nazwach host�w z kt�rych s� wykonywane te operacje.
- wsparcie do system�w kontroli wersji jak RCS, SCCS czy CVS.
  Umo�liwia to np. odtworzenie poprzedniej wersji pliku np. z
  konfiguracj� routera jaka zosta�a zesk�adowana na serwerze z u�yciem
  TFTP. Jest to oczywi�cie cecha opcjonalna.
- wsparcie do opcji blksize (RFC 2348). Umo�liwia ona u�ywanie
  pakiet�w wi�kszych ni� standardowe 512 bajt�w co jest nieco bardziej
  efektywne (szczeg�lnie przy komunikacji bezpo�redniej).
- mo�liwo�ci ustalania opcji timeout (RFC 2349). Brak jednocze�nie na
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

%description client -l pl
Pakiet utftpd zawiera serwer TFTP z kontrol� dost�pu wi�ksz� ni�
standardowy serwer tftpd.

Opis mo�liwo�ci serwera GNU utftpd:
- wsparcie dla kontroli dost�pu per IP. utftpd mo�e przypisywa� prawa
  zapisu, odczytu, tworzenia plik�w i ich nadpisywania bazuj�c na
  nazwach host�w z kt�rych s� wykonywane te operacje.
- wsparcie do system�w kontroli wersji jak RCS, SCCS czy CVS.
  Umo�liwia to np. odtworzenie poprzedniej wersji pliku np. z
  konfiguracj� routera jaka zosta�a zesk�adowana na serwerze z u�yciem
  TFTP. Jest to oczywiscie cecha opcjonalna.
- wsparcie do opcji blksize (RFC 2348). Umozliwia ona u�ywanie
  pakiet�w wi�kszych ni� standardowe 512 bajt�w co jest nieco bardziej
  efektywne (szczeg�lnie przy komunikacji bezpo�redniej).
- mo�liwo�ci ustalania opcji timeout (RFC 2349). Brak jednocze�nie na
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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/utftpd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/utftpd.conf

touch $RPM_BUILD_ROOT%{_sysconfdir}/{utftpd.cdb,utftpd.conf}

%clean
rm -rf $RPM_BUILD_ROOT

%pre -n utftpd
%useradd -P utftpd -u 15 -r -d /var/lib/tftp -s /bin/false -c "TFTP User" -g ftp tftp

%post -n utftpd
echo -n "Rebuilding utftpd configuration... "
utftpd_make %{_sysconfdir}/utftpd.cdb %{_sysconfdir}/utftp.tmp %{_sysconfdir}/utftpd.conf
echo "done"
%service -q rc-inetd reload

%postun -n utftpd
if [ "$1" = 0 ]; then
	%service -q rc-inetd reload
	%userremove tftp
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README README.cvs sample.config
%attr(640,root,root) %ghost %{_sysconfdir}/utftpd.cdb
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/utftpd.conf
%attr(755,root,root) %{_sbindir}/utftpd
%attr(755,root,root) %{_sbindir}/utftpd_*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/utftpd
%{_mandir}/man5/utftpd*.5*
%{_mandir}/man8/utftpd*.8*
%attr(750,tftp,root) %dir /var/lib/tftp

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/utftp
%{_mandir}/man1/utftp.1*
