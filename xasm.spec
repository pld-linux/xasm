#
# Conditional build:
%bcond_with	gdc	# use GDC instead of DMD

Summary:	6502 cross-assembler with original syntax extensions
Summary(pl.UTF-8):	Asembler skrośny dla procesorów 6502 z oryginalnymi rozszerzeniami składni
Name:		xasm
Version:	3.2.1
Release:	1
License:	Poetic
Group:		Development/Languages
#Source0Download: https://github.com/pfusik/xasm/releases
Source0:	https://github.com/pfusik/xasm/archive/%{name}-%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	01f9c9d73bc1ae32ce7039d56a5a17f5
Patch0:		%{name}-gdc.patch
URL:		https://github.com/pfusik/xasm
BuildRequires:	asciidoc
%if %{with gdc}
BuildRequires:	gcc-d
%else
BuildRequires:	dmd >= 2.101
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		filterout_c	-Werror=.* -Wformat.*

%description
xasm is a 6502 cross-assembler with original syntax extensions.

By default it generates binaries for Atari 8-bit computers.

%description -l pl.UTF-8
xasm to asembler skrośny dla procesorów 6502 z oryginalnymi
rozszerzeniami składni.

Domyślnie tworzy binaria dla 8-bitowych komputerów Atari.

%prep
%setup -q -n %{name}-%{name}-%{version}
%patch -P0 -p1

%build
%if %{with gdc}
gdc %{rpmldflags} %{rpmcflags} -shared-libphobos -o xasm source/app.d
%else
%{__make}
%endif

%{__make} xasm.1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/xasm
%{_mandir}/man1/xasm.1*
