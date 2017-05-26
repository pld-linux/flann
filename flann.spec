# TODO: CUDA support, MPI (on bconds)
#
# Conditional build:
%bcond_without	openmp	# OpenMP support
#
Summary:	FLANN - Fast Library for Approximate Nearest Neighbours
Summary(pl.UTF-8):	FLANN - szybka biblioteka do przybliżonego wyszukiwania najbliższych sąsiadów
Name:		flann
Version:	1.9.1
Release:	2
License:	BSD
Group:		Libraries
Source0:	https://github.com/mariusmuja/flann/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	73adef1c7bf8e8b978987e7860926ea6
Patch0:		%{name}-python.patch
URL:		http://www.cs.ubc.ca/~mariusm/index.php/FLANN/FLANN
BuildRequires:	cmake >= 2.6
%{?with_openmp:BuildRequires:	gcc-c++ >= 6:4.2}
BuildRequires:	gtest-devel
BuildRequires:	hdf5-devel
BuildRequires:	latex2html
%{?with_openmp:BuildRequires:	libgomp-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	python >= 1:2.5
BuildRequires:	python-devel >= 1:2.5
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	texlive-format-pdflatex
BuildRequires:	texlive-latex
BuildRequires:	texlive-latex-bibtex
BuildRequires:	texlive-makeindex
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		octave_m_dir	%(octave-config --m-site-dir)
%define		octave_oct_dir	%(octave-config --oct-site-dir)

%description
FLANN is a library for performing fast approximate nearest neighbour
searches in high dimensional spaces. It contains a collection of
algorithms we found to work best for nearest neighbour search and a
system for automatically choosing the best algorithm and optimum
parameters depending on the dataset.

FLANN is written in C++ and contains bindings for the following
languages: C, MATLAB and Python.

%description -l pl.UTF-8
FLANN (Fast Library for Approximage Nearest Neighbours) to biblioteka
do wykonywania szybkich przybliżonych wyszukiwań najbliższych sąsiadów
w przestrzeniach o wielu wymiarach. Zawiera zbiór algorytmów, które
sprawdzają się najlepiej w tym zastosowaniu oraz system automatycznego
wyboru najlepszego algorytmu oraz optymalnych parametrów w zależności
od zbioru danych.

Biblioteka FLANN została napisana w C++ i zawiera dowiązania dla
następujących języków: C, MATLAB i Python.

%package devel
Summary:	Header files for FLANN libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek FLANN
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	hdf5-devel
Requires:	gtest-devel
Requires:	libstdc++-devel

%description devel
Header files for FLANN libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek FLANN.

%package static
Summary:	Static FLANN libraries
Summary(pl.UTF-8):	Statyczne biblioteki FLANN
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static FLANN libraries.

%description static -l pl.UTF-8
Statyczne biblioteki FLANN.

%package -n octave-flann
Summary:	Octave binding for FLANN library
Summary(pl.UTF-8):	Dowiązania języka Octave do biblioteki FLANN
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n octave-flann
Octave binding for FLANN library.

%description -n octave-flann -l pl.UTF-8
Dowiązania języka Octave do biblioteki FLANN.

%package -n python-flann
Summary:	Python binding for FLANN library
Summary(pl.UTF-8):	Dowiązania Pythona do biblioteki FLANN
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-flann
Python binding for FLANN library.

%description -n python-flann -l pl.UTF-8
Dowiązania Pythona do biblioteki FLANN.

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake .. \
	-DBUILD_CUDA_LIB=OFF \
	%{!?with_openmp:-DUSE_OPENMP=OFF}

%{__make}
%{__make} -C doc pdf

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_bindir}/flann_example_*
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -p examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/flann

install -d $RPM_BUILD_ROOT{%{octave_m_dir},%{octave_oct_dir}}
%{__rm} $RPM_BUILD_ROOT%{_datadir}/flann/octave/test*.m
%{__mv} $RPM_BUILD_ROOT%{_datadir}/flann/octave/*.m $RPM_BUILD_ROOT%{octave_m_dir}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/flann/octave/*.mex $RPM_BUILD_ROOT%{octave_oct_dir}

%{__mv} $RPM_BUILD_ROOT%{py_sitedir}/pyflann/lib/libflann.so $RPM_BUILD_ROOT%{py_sitedir}/pyflann

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_libdir}/libflann.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libflann.so.1.9
%attr(755,root,root) %{_libdir}/libflann_cpp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libflann_cpp.so.1.9

%files devel
%defattr(644,root,root,755)
%doc build/doc/manual.pdf
%attr(755,root,root) %{_libdir}/libflann.so
%attr(755,root,root) %{_libdir}/libflann_cpp.so
%{_includedir}/flann
%{_pkgconfigdir}/flann.pc
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libflann_s.a
%{_libdir}/libflann_cpp_s.a

%files -n octave-flann
%defattr(644,root,root,755)
%{octave_m_dir}/flann*.m
%attr(755,root,root) %{octave_oct_dir}/nearest_neighbors.mex

%files -n python-flann
%defattr(644,root,root,755)
%dir %{py_sitedir}/pyflann
%{py_sitedir}/pyflann/*.py[co]
%attr(755,root,root) %{py_sitedir}/pyflann/libflann.so
%{py_sitedir}/flann-%{version}-py*.egg-info
