Summary:	A system documentation reader from the GNOME project
Name:		yelp
Version:	3.10.2
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/yelp/3.10/%{name}-%{version}.tar.xz
# Source0-md5:	26b380fad5e8e0414db6ebc384493505
URL:		http://projects.gnome.org/yelp/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk-doc
BuildRequires:	gtk+3-webkit-devel >= 2.2.0
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	xz-devel
BuildRequires:	pkg-config
BuildRequires:	yelp-xsl >= 3.10.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib-gio-gsettings
Requires:	%{name}-libs = %{version}-%{release}
Requires:	gnome-icon-theme
Requires:	libxslt-progs
Requires:	yelp-xsl >= 3.10.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Yelp is the default help browser for the GNOME desktop. Yelp provides
a simple graphical interface for viewing DocBook, HTML, man, and info
formatted documentation.

%package libs
Summary:	yelp library
Group:		Libraries

%description libs
yelp library.

%package devel
Summary:	Header files for yelp library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for yelp library.

%package apidocs
Summary:	yelp library API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
yelp library API documentation.

%prep
%setup -q

# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g' configure.ac

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-compile \
	--disable-silent-rules \
	--disable-static \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post
%update_gsettings_cache

%postun
%update_desktop_database_postun
%update_gsettings_cache

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README ChangeLog NEWS TODO AUTHORS
%attr(755,root,root) %{_bindir}/gnome-help
%attr(755,root,root) %{_bindir}/yelp
%{_datadir}/glib-2.0/schemas/org.gnome.yelp.gschema.xml
%{_datadir}/yelp
%{_datadir}/yelp-xsl/xslt/common/domains/yelp.xml
%{_desktopdir}/yelp.desktop

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libyelp.so.?
%attr(755,root,root) %{_libdir}/libyelp.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libyelp.so
%{_includedir}/libyelp

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libyelp

