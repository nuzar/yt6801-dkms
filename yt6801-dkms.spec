%define module yt6801

Name:           %{module}-dkms

Version:        1.0.28
License:        GPL2
Release:        1%{?dist}
Summary:        Kernel module for Motorcomm YT6801 Ethernet controller (DKMS)

Group:          System Environment/Kernel
URL:            https://deb.tuxedocomputers.com/ubuntu/pool/main/t/tuxedo-yt6801/
Source0:        https://deb.tuxedocomputers.com/ubuntu/pool/main/t/tuxedo-yt6801/tuxedo-%{module}_%{version}.orig.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      x86_64

Requires:       dkms
Requires:       kernel-devel, gcc, make
Requires(post): gcc, make
BuildRequires:  dos2unix
Provides:       %{module}-kmod = %{version}
AutoReqProv:    no

%description
Kernel module for Motorcomm YT6801 Ethernet controller (DKMS)

%prep
%setup -c -n %{module}-%{version}
# change dkms.conf to CRLF
find . -type f -exec dos2unix {} \;
find . -type f -name '*.c' -exec chmod 644 {} \;
find . -type f -name '*.h' -exec chmod 644 {} \;
# Filter out REMAKE_INITRD from dkms.conf
awk '{ if ($0 !~ "REMAKE_INITRD") print }' dkms.conf > dkms_filtered.conf
mv dkms_filtered.conf dkms.conf

%install
mkdir -p $RPM_BUILD_ROOT/usr/src/
cp -rf ${RPM_BUILD_DIR}/%{module}-%{version}/ $RPM_BUILD_ROOT/usr/src/

%files
%defattr(-,root,root)
/usr/src/%{module}-%{version}

%post
echo "Adding %{module} dkms modules version %{version} to dkms."
dkms add -m %{module} -v %{version}
echo "Installing %{module} dkms modules version %{version} for the current kernel."
dkms install --force -m %{module} -v %{version}

%changelog
* Tue May 31 2016 Adam Miller <maxamillion@fedoraproject.org> - 1.0.28-1
- First package