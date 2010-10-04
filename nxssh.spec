#
# Conditional build:
%bcond_without  kerberos5       # without kerberos5 support
#
%define		_version_major	3.3.0
%define		_version_minor	1
Summary:	Modified openssh client, used by nxclient
Summary(pl.UTF-8):	Zmodyfikowany klient openssh używany przez nxclienta
Name:		nxssh
Version:	%{_version_major}.%{_version_minor}
Release:	5
License:	GPL
Group:		X11/Applications/Networking
#Source0Download: http://www.nomachine.com/sources.php
Source0:	http://web04.nomachine.com/download/%{_version_major}/sources/%{name}-%{_version_major}-%{_version_minor}.tar.gz
# Source0-md5:	e9bb4c1cd61c42db9626894845fcf3f7
URL:		http://www.nomachine.com/
BuildRequires:	autoconf
%{?with_kerberos5:BuildRequires:	heimdal-devel}
BuildRequires:	libwrap-devel
BuildRequires:	nxcomp-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_privsepdir	/usr/share/empty

%description
Modified openssh client, used by nxclient.

%description -l pl.UTF-8
Zmodyfikowany klient openssh używany przez nxclienta.

%prep
%setup -q -n %{name}
# drop unused libraries
%{__sed} -e 's/ -lstdc++ -lpng -ljpeg / /' \
	-i configure.ac

%build
%{__autoconf}
%configure \
	PERL=%{__perl} \
	--with-dns \
	--with-pam \
	--with-mantype=man \
	--with-md5-passwords \
	--with-ipaddr-display \
	%{?with_libedit:--with-libedit} \
	--with-4in6 \
	--disable-suid-ssh \
	--with-tcp-wrappers \
	%{?with_ldap:--with-libs="-lldap -llber"} \
	%{?with_ldap:--with-cppflags="-DWITH_LDAP_PUBKEY"} \
	%{?with_kerberos5:--with-kerberos5=%{_prefix}} \
	--with-privsep-path=%{_privsepdir} \
	--with-pid-dir=%{_localstatedir}/run \
	--with-xauth=%{_bindir}/xauth \
	--enable-utmpx \
	--enable-wtmpx

echo '#define LOGIN_PROGRAM		   "/bin/login"' >>config.h

%{__make} nxssh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

install %{name} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
