#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define		pdir	Schedule
%define		pnam	Load
Summary:	Schedule::Load - load distribution and status across multiple host machines
Summary(pl.UTF-8):	Schedule::Load - rozkładanie i badanie obciążenia dla wielu maszyn
Name:		perl-Schedule-Load
Version:	3.040
Release:	2
License:	GPL or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	b66fd3df5fcbbcd083eb120ad98f15eb
BuildRequires:	perl-devel >= 1:5.8.0
%if %{with tests}
BuildRequires:	perl-IPC-Locker >= 1.410
BuildRequires:	perl-Proc-ProcessTable >= 0.40
BuildRequires:	perl-Unix-Processors >= 2.020
%endif
BuildRequires:	rpm-perlprov >= 4.1-13
Requires:	perl-IPC-Locker >= 1.410
Requires:	perl-Proc-ProcessTable >= 0.40
Requires:	perl-Unix-Processors >= 2.020
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides useful utilities for load distribution and
status across multiple machines in a network. To just see what is up
in the network, see the rschedule or rtop, rloads or rhosts commands.

%description -l pl.UTF-8
Ten pakiet udostępnia przydatne narzędzia do rozkładania obciążenia i
jego badania na wielu maszynach w sieci. Aby zobaczyć co się dzieje w
sieci, wystarczy popatrzeć na polecenia rschedule, rtop, rloads i
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
%doc README
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
