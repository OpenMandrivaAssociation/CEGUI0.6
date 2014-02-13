%define libname %mklibname CEGUI %{version}
%define devname %mklibname %{name} -d

Summary:	A free library providing windowing and widgets for graphics APIs / engines 
Name:		CEGUI0.6
Version:	0.6.2
Release:	8
License:	MIT
Group:		Development/C++
Url:		http://www.cegui.org.uk
Source0:	http://prdownloads.sourceforge.net/crayzedsgui/CEGUI-%{version}.tar.gz
Patch1:		cegui-0.6.0-userverso.patch
Patch2:		CEGUI-0.6.2-fix-underlinking.patch
Patch3:		CEGUI-0.6.2-release-as-so-ver.patch
Patch4:		cegui-0.6.2-new-DevIL.patch
Patch5:		CEGUI-0.6.2-install.patch
Patch6:		CEGUI-0.6.2-gcc46.patch
Patch7:		CEGUI-0.6.2-tinyxml.patch
BuildRequires:	freeimage-devel
BuildRequires:	tinyxml-devel
BuildRequires:	tolua++-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glew)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(IL)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(xerces-c)

%description
Crazy Eddie's GUI System is a free library providing windowing and widgets for 
graphics APIs / engines where such functionality is not natively available,
or severely lacking. The library is object orientated, written in C++, 
and targeted at games developers who should be spending their time creating 
great games, not building GUI sub-systems!

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	CEGUI library
Group:		Games/Other

%description -n %{libname}
This is a library used by CEGUI.

%files -n %{libname}
%{_libdir}/libCEGUI*-%{version}.so

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for CEGUI
Group:		Development/C++
Requires:	%{libname} = %{EVRD}
Provides:	lib%{name}-devel = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Conflicts:	%{_lib}CEGUI-devel >= 0.7

%description -n  %{devname}
Development file for CEGUI.

%files -n %{devname}
%{_libdir}/*.so
%exclude %{_libdir}/libCEGUI*-%{version}.so
%{_includedir}/CEGUI
%{_libdir}/pkgconfig/*
%{_datadir}/CEGUI

#----------------------------------------------------------------------------

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
sed -i 's|-L%{_libdir}||g' RendererModules/OpenGLGUIRenderer/Makefile
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
%makeinstall_std

