# sitelib
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%define dir /usr/libexec/argo/probes/oidc

Name: argo-probe-oidc
Summary: ARGO probes for handling of OIDC tokens.
Version: 0.1.1
Release: 1%{?dist}
License: ASL 2.0
Source0: %{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: python-requests, python-argparse, python-jwt

%description
This package includes probes for fetching OIDC access token and checking refresh token validity.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot} --record=INSTALLED_FILES
install -d -m 755 %{buildroot}/%{dir}
install -d -m 755 %{buildroot}/%{python_sitelib}/argo_probe_oidc

%clean
rm -rf %{buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root,-)
%{python_sitelib}/argo_probe_oidc
%{dir}


%changelog
* Thu Jun 29 2022 Katarina Zailac <kzailac@srce.hr> - 0.1.1-1%{?dist}
- ARGO-3872 Improve probe return message when refresh token has expired
* Thu Jun 9 2022 Katarina Zailac <kzailac@gmail.com> - 0.1.0-1%{?dist}
- Initial version
