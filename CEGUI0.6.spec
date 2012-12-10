%define libname %mklibname CEGUI %{version}
%define develname %mklibname %{name} -d

Summary:	A free library providing windowing and widgets for graphics APIs / engines 
Name:		CEGUI0.6
Version:	0.6.2
Release:	%mkrel 7
License:	MIT
Group:		Development/C++
URL:		http://www.cegui.org.uk
Source0:	http://prdownloads.sourceforge.net/crayzedsgui/CEGUI-%{version}.tar.gz
Patch1:		cegui-0.6.0-userverso.patch
Patch2:		CEGUI-0.6.2-fix-underlinking.patch
Patch3:		CEGUI-0.6.2-release-as-so-ver.patch
Patch4:		cegui-0.6.2-new-DevIL.patch
Patch5:		CEGUI-0.6.2-install.patch
Patch6:		CEGUI-0.6.2-gcc46.patch
Patch7:		CEGUI-0.6.2-tinyxml.patch
BuildRequires:	libxml2-devel
BuildRequires:	mesagl-devel
BuildRequires:	mesaglu-devel
%if %{mdvver} >= 201200
BuildRequires:	freeglut-devel
%else
BuildRequires:	mesaglut-devel
%endif
BuildRequires:	freetype2-devel
BuildRequires:	pcre-devel
BuildRequires:	freeimage-devel
BuildRequires:	libexpat-devel
BuildRequires:	libxerces-c-devel
BuildRequires:	gtk2-devel
BuildRequires:	devil-devel
BuildRequires:	glew-devel
BuildRequires:	tinyxml-devel
BuildRequires:	tolua++-devel

%description
Crazy Eddie's GUI System is a free library providing windowing and widgets for 
graphics APIs / engines where such functionality is not natively available,
or severely lacking. The library is object orientated, written in C++, 
and targeted at games developers who should be spending their time creating 
great games, not building GUI sub-systems!

%package -n %{libname}
Summary:	CEGUI library
Group:		Games/Other
Obsoletes:	%mklibname %{name} 0
Obsoletes:	%mklibname %{name} 1
Obsoletes:	%mklibname %{name} 0.6.1

%description -n %{libname}
This is a library used by CEGUI.

%package -n %{develname}
Summary:	Development files for CEGUI
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname CEGUI 0 -d
Conflicts:	%{_lib}CEGUI-devel >= 0.7

%description -n  %{develname}
Development file for CEGUI.

%prep
%setup -qn CEGUI-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0
%patch6 -p1
%patch7 -p1

touch NEWS

%build
autoreconf -ifv

%configure2_5x \
	--with-gtk2 \
	--disable-samples \
	--disable-irrlicht-renderer \
	--enable-freeimage \
	--disable-directfb-renderer

# We do not want to get linked against a system copy of ourselves!
%__sed -i 's|-L%{_libdir}||g' RendererModules/OpenGLGUIRenderer/Makefile
# Don't use rpath!
%__sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
%__sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
%__rm -rf %{buildroot}
%makeinstall_std

%clean
%__rm -rf %{buildroot}

%files -n %{libname}
%{_libdir}/libCEGUI*-%{version}.so

%files -n %{develname}
%if %{mdvver} < 201200
%{_libdir}/*.la
%endif
%{_libdir}/*.so
%exclude %{_libdir}/libCEGUI*-%{version}.so
%{_includedir}/CEGUI
%{_libdir}/pkgconfig/*
%{_datadir}/CEGUI



%changelog
* Sun Mar 25 2012 Andrey Bondrov <abondrov@mandriva.org> 0.6.2-7mdv2012.0
+ Revision: 786687
- Improve gcc 4.6+ support, add patch to fix build with new tinyxml

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Fri Feb 05 2010 Funda Wang <fwang@mandriva.org> 0.6.2-5mdv2010.1
+ Revision: 501068
- fix obsoletes
- BR tolua++
- import CEGUI0.6


