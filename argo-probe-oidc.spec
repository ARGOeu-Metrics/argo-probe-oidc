%define dir /usr/libexec/argo/probes/oidc
%define underscore() %(echo %1 | sed 's/-/_/g')

Name:      argo-probe-oidc
Summary:   ARGO probes for handling of OIDC tokens.
Version:   0.2.0
Release:   1%{?dist}
License:   ASL 2.0
Group:     Development/System
Source0:   %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Prefix:    %{_prefix}
BuildArch: noarch

BuildRequires: python3-devel

%if 0%{?el7}
Requires: python36-requests
Requires: python36-jwt

%else
Requires: python3-requests
Requires: python3-jwt

%endif

%description
This package includes probes for fetching OIDC access token and checking refresh token validity.

%prep
%setup -q


%build
%{py3_build}


%install
%{py3_install "--record=INSTALLED_FILES" }


%clean
rm -rf $RPM_BUILD_ROOT


%files -f INSTALLED_FILES
%defattr(-,root,root,-)
%{python3_sitelib}/%{underscore %{name}}/
%{dir}


%changelog
* Thu Oct 5 2023 Katarina Zailac <kzailac@srce.hr> - 0.2.0-1%{?dist}
- ARGO-4389 Set username as parameter to probe fetching OIDC token
* Thu Jun 30 2022 Katarina Zailac <kzailac@srce.hr> - 0.1.1-1%{?dist}
- ARGO-3872 Improve probe return message when refresh token has expired
* Thu Jun 9 2022 Katarina Zailac <kzailac@gmail.com> - 0.1.0-1%{?dist}
- Initial version
