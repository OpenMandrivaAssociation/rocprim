# HIP parallel primitives (header-only) (TheRock 7.14)
%global debug_package %{nil}

Name:		rocprim
Version:	7.14.0
Release:	2
Summary:	HIP parallel primitives (header-only)
License:	MIT
Group:		Development/C++
URL:		https://github.com/ROCm/rocm-libraries
Source0:	https://github.com/ROCm/rocm-libraries/releases/download/therock-7.14/rocprim.tar.gz#/rocprim-%{version}.tar.gz

BuildRequires:	rocm-rpm-macros
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	rocm-cmake
BuildRequires:	hipcc
BuildRequires:	rocminfo
BuildRequires:	clang-tools
BuildRequires:	rocm-hip-devel
BuildRequires:	clang >= %{rocm_llvm_maj_ver}


%description
rocPRIM provides device-side parallel primitives for HIP. Header-only;
consumers compile for %the stack GPU targets (includes gfx803).

%package devel
Summary:	Development files for rocprim
Group:		Development/C++
Requires:	%{name} = %{version}-%{release}
Requires:	rocm-hip-devel

Provides:	rocprim-devel = %{EVRD}

%description devel
Headers and CMake package for rocprim.

%prep
%autosetup -n rocprim

export CXX=hipcc
export CC=clang
# Strip host-only -mfpmath (hipcc forwards flags to amdgcn device compiles)
CXXFLAGS=$(printf '%s' "%{optflags}" | sed 's/-mfpmath=sse//g')
export CXXFLAGS
export CFLAGS="$CXXFLAGS"
%cmake %{rocm_cmake_fhs} %{rocm_cmake_gpu_targets_prim} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DCMAKE_CXX_FLAGS="$CXXFLAGS" \
	-DBUILD_TEST=OFF \
	-DBUILD_BENCHMARK=OFF \
	-DBUILD_EXAMPLE=OFF \
	-DBUILD_DOCS=OFF \
	-DROCM_PATH=%{_prefix} \
	-DCMAKE_PREFIX_PATH=%{_prefix} \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

%files
%license LICENSE.md
%doc README.md
%exclude %{_docdir}/rocprim/LICENSE.md


%files devel
%{_includedir}/rocprim/
%{_libdir}/cmake/rocprim/
