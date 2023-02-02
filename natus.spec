#
# Conditional build:
%bcond_without	spidermonkey	# SpiderMonkey engine (Mozilla/Firefox)
%bcond_without	v8		# V8 engine (Chrome/Chromium)
%bcond_without	webkit		# JavaScriptCore engine (WebKit/Safari)
#
Summary:	JavaScript meta-engine
Summary(pl.UTF-8):	Meta-silnik JavaScriptu
Name:		natus
Version:	0.2.1
%define	gitver	fcb732e
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/Natus/natus/tags
Source0:	http://github.com/Natus/natus/tarball/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	c707dadb76dc7cf6e4f8c95c0cc45ca5
Patch0:		%{name}-includes.patch
URL:		https://github.com/Natus/natus
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
%{?with_webkit:BuildRequires:	gtk-webkit3-devel}
%if %{with spidermonkey}
# libjs >= 1.8 / xulrunner >= 2
# builds with js185 with no modification
# js187 fails with two errors, each later is worse
BuildRequires:	js185-devel
%endif
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.0
BuildRequires:	sed >= 4.0
%{?with_v8:BuildRequires:	v8-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JavaScript meta-engine.

%description -l pl.UTF-8
Meta-silnik JavaScriptu.

%package devel
Summary:	Header files for Natus library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki Natus
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for Natus library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Natus.

%package engine-JavaScriptCore
Summary:	JavaScriptCore JavaScript engine for Natus
Summary(pl.UTF-8):	Silnik JavaScriptu JavaScriptCore dla Natusa
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description engine-JavaScriptCore
JavaScriptCore JavaScript engine (used in WebKit/Safari) for Natus.

%description engine-JavaScriptCore -l pl.UTF-8
Silnik JavaScriptu JavaScriptCore (używany w WebKicie/Safari) dla
Natusa.

%package engine-SpiderMonkey
Summary:	SpiderMonkey JavaScript engine for Natus
Summary(pl.UTF-8):	Silnik JavaScriptu SpiderMonkey dla Natusa
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description engine-SpiderMonkey
SpiderMonkey JavaScript engine (used in Mozilla-derived browsers like
Firefox or Seamonkey) for Natus.

%description engine-SpiderMonkey -l pl.UTF-8
Silnik JavaScriptu SpiderMonkey (używany w przeglądarkach wywodzących
się z Mozilli, np. Firefox czy Seamonkey) dla Natusa.

%package engine-v8
Summary:	V8 JavaScript engine for Natus
Summary(pl.UTF-8):	Silnik JavaScriptu V8 dla Natusa
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description engine-v8
V8 JavaScript engine (used in Google Chrome/Chromium) for Natus.

%description engine-v8 -l pl.UTF-8
Silnik JavaScriptu V8 (używany w przeglądarkach Google
Chrome/Chromium) dla Natusa.

%prep
%setup -q -n Natus-%{name}-%{gitver}
%patch0 -p1

%{__sed} -i -e 's/libjs >= 1\.8/mozjs185/' configure.ac

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# modules are dlopen()ed
%{__rm}	$RPM_BUILD_ROOT%{_libdir}/%{name}/%{version}/engines/*.la
# no static library, .pc file present
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnatus.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog
%attr(755,root,root) %{_bindir}/natus
%attr(755,root,root) %{_libdir}/libnatus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnatus.so.0
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{version}
%dir %{_libdir}/%{name}/%{version}/engines

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnatus.so
%{_includedir}/natus
%{_pkgconfigdir}/natus.pc

%if %{with webkit}
%files engine-JavaScriptCore
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/%{version}/engines/JavaScriptCore.so
%endif

%if %{with spidermonkey}
%files engine-SpiderMonkey
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/%{version}/engines/SpiderMonkey.so
%endif

%if %{with v8}
%files engine-v8
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}/%{version}/engines/v8.so
%endif
