Name:           gzip-lfs-tools
Version:        1.12
Release:        1%{?dist}
Summary:        Toolchain for building LFS
License:        GPL

Source0:        gzip-%{version}.tar.xz

%undefine       _auto_set_build_flags
%global         debug_package %{nil}


%description
Toolchain for building LFS


%prep
%setup -q -n gzip-%{version}


%build
%lfs_path
./configure --prefix=/usr --host=%{lfs_tgt}
make


%install
%lfs_path
make DESTDIR=%{buildroot}/%{lfs} install
%lfs_remove_docs


%files
%{lfs}/usr/bin/*


%changelog
* Wed Oct 4 2023 Mike McGann <mike.mcgann@blackchip.org> - 1.12-1
- Initial package


