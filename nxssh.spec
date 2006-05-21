%define		_version_major	1.5.0
%define		_version_minor	23

%bcond_with     ldap            # with ldap support
%bcond_without  libedit         # without libedit (editline/history support in sftp client)
%bcond_without  kerberos5       # without kerberos5 support

Summary:	Modified openssh client, used by nxclient
Name:		nxssh
Version:	%{_version_major}.%{_version_minor}
Release:	1
License:	GPL
Group:		X11/Applications/Networking
#Source0Download: http://www.nomachine.com/sources.php
Source0:	http://web04.nomachine.com/download/%{_version_major}/sources/%{name}-%{_version_major}-%{_version_minor}.tar.gz
# Source0-md5:	86df9d5f03bd7e1e1930f129fe87347d
URL:		http://www.nomachine.com/
BuildRequires:	autoconf
%{?with_kerberos5:BuildRequires:	heimdal-devel >= 0.7}
%{?with_libedit:BuildRequires:  libedit-devel}
%{?with_selinux:BuildRequires:  libselinux-devel}
BuildRequires:	libwrap-devel
BuildRequires:	nx-devel
%{?with_ldap:BuildRequires:     openldap-devel}
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pam-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Modified openssh client, used by nxclient.

%prep
%setup -q -n %{name}

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
		%{?with_kerberos5:--with-kerberos5} \
		--with-privsep-path=%{_privsepdir} \
		--with-pid-dir=%{_localstatedir}/run \
		--with-xauth=%{_bindir}/xauth \
		--enable-utmpx \
		--enable-wtmpx

echo '#define LOGIN_PROGRAM		   "/bin/login"' >>config.h

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}

install %{name} $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
FIXME
