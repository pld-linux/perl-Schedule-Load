#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Schedule
%define		pnam	Load
Summary:	Schedule::Load - load distribution and status across multiple host machines
Summary(pl):	Schedule::Load - rozk³adanie i badanie obci±¿enia dla wielu maszyn
Name:		perl-Schedule-Load
Version:	2.102
Release:	3
License:	GPL or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	a63ef8d71bc7db34654b48aee0d12467
BuildRequires:	perl-devel >= 1:5.8.0
%if %{with tests}
BuildRequires:	perl-Proc-ProcessTable
BuildRequires:	perl-Unix-Processors >= 1.7
%endif
BuildRequires:	rpm-perlprov >= 4.1-13
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides useful utilities for load distribution and
status across multiple machines in a network. To just see what is up
in the network, see the rschedule or rtop, rloads or rhosts commands.

%description -l pl
Ten pakiet udostêpnia przydatne narzêdzia do rozk³adania obci±¿enia i
jego badania na wielu maszynach w sieci. Aby zobaczyæ co siê dzieje w
sieci, wystarczy popatrzeæ na polecenia rschedule, rtop, rloads i
rhosts.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

find -type f -perm +100 | xargs perl -pi -e 's,/usr/local/bin/perl,/usr/bin/perl,'

%if %{with tests}
%{__make} test
killall slreportd || true
killall slchoosed || true
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS README
%{perl_vendorlib}/Schedule/*.pm
%{perl_vendorlib}/Schedule/Load
%dir %{perl_vendorlib}/auto/Schedule/Load
%dir %{perl_vendorlib}/auto/Schedule/Load/Hosts
# empty autosplit.ix files
#%dir %{perl_vendorlib}/auto/Schedule/Load/Hosts/Host
#%%{perl_vendorlib}/auto/Schedule/Load/Hosts/Host/autosplit.ix
#%dir %{perl_vendorlib}/auto/Schedule/Load/Hosts/Proc
#%%{perl_vendorlib}/auto/Schedule/Load/Hosts/Proc/autosplit.ix
%{_bindir}/*
%{_mandir}/man?/*
