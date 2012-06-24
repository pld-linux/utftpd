Summary:	utftpd - a TFTP server
Summary(pl):	utftpd - serwer TFTP
Name:		utftpd
Version:	0.2.4
Release:	5
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.ohse.de/uwe/releases/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Buildrequires:	autoconf
Prereq:		rc-inetd
Provides:	tftpdaemon
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
Pakiet utftpd zawiera serwer TFTP z
kontrol� dosrepu wieksz� ni� standardowy serwer tftpd.

Opis mo�liwo�ci serwera GNU utftpd:
 - wsparcie d okontrli dosepu per IP. utftpd moze przypisywa�
   prawa zapisu, odczytu, terzenai plik�w i ich nadpisywania bazuja�
   na nazwach host�w z kt�rych s� wykonywane te operacje.
 - wsparcie do system�w rontroli wersji jak RCS, SCCS czy CVS. Umo�liwia
   to np. odtorzenie poprzeniej wersji pliku np. z konfiguraj� routera
   jaka zosta�a zesk�adowana na zserwerze z u�yciem TFTP. Jest to
   oczywiscie cecha opcjonalna.
 - wsparcie do opcji blksize (RFC 2348). Umozliwia ona u�ywanie pakiet�w
   wiekszych ni� standardowe 512 bajt�w co jest nieco bardziej efektywne
   (szczeg�lnie przy komunikacji bezpo�eniej).
 - mo�liwo�ci ustalania opcji timeout (RFC 2349). Brak jednocze�nie na razie
   ustawiania opcji tsize (RFC 2349).

%prep
%setup -q

%build
autoconf
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/sysconfig/rc-inetd,var/lib/tftp}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/utftpd

touch $RPM_BUILD_ROOT%{_sysconfdir}/utftpd.cdb

gzip -9nf AUTHORS ChangeLog NEWS README README.cvs sample.config

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
%{_mandir}/man8/utftpd*.8.gz
%{_mandir}/man1/utftp.1.gz
%dir /var/lib/tftp
