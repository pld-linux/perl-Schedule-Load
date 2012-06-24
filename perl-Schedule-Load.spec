#
# Conditional build:
# _without_tests - do not perform "make test"
%include	/usr/lib/rpm/macros.perl
%define	pdir	Schedule
%define	pnam	Load
Summary:	Schedule::Load - Load distribution and status across multiple host machines
#Summary(pl):	
Name:		perl-Schedule-Load
Version:	2.100
Release:	1
License:	GPL/Artistic
Group:		Development/Languages/Perl
Source0:	ftp://ftp.cpan.org/pub/CPAN/modules/by-module/%{pdir}/%{pdir}-%{pnam}-%{version}.tar.gz
BuildRequires:	perl >= 5.6
BuildRequires:	rpm-perlprov >= 3.0.3-26
%if %{?_without_tests:0}%{!?_without_tests:1}
BuildRequires:	perl-Proc-ProcessTable
BuildRequires:	perl-Time-HiRes
BuildRequires:	perl-Unix-Processors >= 1.7
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides useful utilities for load distribution and status
across multiple machines in a network.  To just see what is up in the
network, see the C<rschedule> or C<rtop>, C<rloads> or C<rhosts> commands.

# %description -l pl
# TODO

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
perl Makefile.PL
%{__make}

find -type f -perm +100 | xargs perl -pi -e 's,/usr/local/bin/perl,/usr/bin/perl,'

%if %{?_without_tests:0}%{!?_without_tests:1}
%{__make} test
killall slreportd || true
killall slchoosed || true
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS README
%{perl_sitelib}/%{pdir}/*.pm
%{perl_sitelib}/%{pdir}/%{pnam}
%{_bindir}/*
%{_mandir}/man?/*
