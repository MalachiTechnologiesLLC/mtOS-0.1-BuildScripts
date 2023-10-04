Name:           gcc-lfs-bootstrap
Version:        13.2.0
Release:        1%{?dist}
Summary:        Toolchain for building LFS
License:        GPL

%define         mpfr_version    4.2.0
%define         gmp_version     6.3.0
%define         mpc_version     1.3.1

Source0:        gcc-%{version}.tar.xz
Source1:        mpfr-%{mpfr_version}.tar.xz
Source2:        gmp-%{gmp_version}.tar.xz
Source3:        mpc-%{mpc_version}.tar.gz

%undefine       _auto_set_build_flags
%global         debug_package %{nil}

BuildRequires:  binutils-lfs-bootstrap


%description
Toolchain for building LFS


%prep
%setup -q -n gcc-%{version}

tar -xf %{SOURCE1}
tar -xf %{SOURCE2}
tar -xf %{SOURCE3}

mv mpfr-%{mpfr_version}  mpfr
mv gmp-%{gmp_version}    gmp
mv mpc-%{mpc_version}    mpc

case $(uname -m) in
  x86_64)
    sed -e '/m64=/s/lib64/lib/' \
        -i.orig gcc/config/i386/t-linux64
 ;;
esac


%build
export PATH=%{tools}/bin:${PATH}

mkdir build
cd build

../configure                  \
    --target=%{lfs_tgt}       \
    --prefix=%{lfs}/tools     \
    --with-glibc-version=2.38 \
    --with-sysroot=%{lfs}     \
    --with-newlib             \
    --without-headers         \
    --enable-default-pie      \
    --enable-default-ssp      \
    --disable-nls             \
    --disable-shared          \
    --disable-multilib        \
    --disable-threads         \
    --disable-libatomic       \
    --disable-libgomp         \
    --disable-libquadmath     \
    --disable-libssp          \
    --disable-libvtv          \
    --disable-libstdcxx       \
    --enable-languages=c,c++
make


%install
export PATH=%{tools}/bin:${PATH}
cd build
DESTDIR=%{buildroot} make install

cd ..
cat gcc/limitx.h gcc/glimits.h gcc/limity.h > \
  %{buildroot}/%{tools}/lib/gcc/%{lfs_tgt}/%{version}/include/limits.h

rm -rf %{buildroot}/%{tools}/share/info
rm -rf %{buildroot}/%{tools}/share/man*


%files
%{tools}/bin/*
%{tools}/lib/gcc/%{lfs_tgt}/%{version}
%{tools}/lib64/*
%{tools}/libexec/gcc/%{lfs_tgt}/%{version}


%changelog
* Tue Oct 3 2023 Mike McGann <mike.mcgann@blackchip.org> - 13.2.0-1
- Initial package
