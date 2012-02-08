%define svn 20080916

Name:           smpeg
Version:        0.4.5
Release:        0.4%{?dist}
Summary:        MPEG library for SDL

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://icculus.org/smpeg/
Source0:        http://rpm.kwizart.net/fedora/SOURCES/smpeg-%{svn}.tar.gz
Source10:       smpeg-snapshot.sh
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gtk+-devel >= 1.2.1
BuildRequires:  libGL-devel, libGLU-devel
BuildRequires:  SDL-devel >= 1.2.0

# Needed for the snapshot
#BuildRequires:  automake17
#BuildRequires:  autoconf
Requires:       %{name}-libs = %{version}-%{release}

%description
SMPEG is based on UC Berkeley's mpeg_play software MPEG decoder
and SPLAY, an MPEG audio decoder created by Woo-jae Jung. SMPEG has
completed the initial work to wed these two projects in order to 
create a general purpose MPEG video/audio player for the Linux OS. 


%package libs
Summary:        Libraries for %{name}
Group:          System Environment/Libraries

%description libs
The %{name}-libs package contains shared libraries for %{name}.


%package devel
Summary:        Header files and static libraries for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Obsoletes:      %{name} < 0.4.5
Requires:       SDL-devel

%description devel
This package contains header files and static libraries for %{name}.


%prep
%setup -q
sed -i -e 's|\@SMPEG_RLD_FLAGS\@||' smpeg-config.in

#aclocal-1.7
#automake-1.7 --foreign
#autoconf


%build
%configure --enable-debug --enable-shared --disable-static --with-PIC \
  --enable-threaded-system

# remove rpath from libtool
sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# clean unused-direct-shlib-dependencies
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags}



%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p -c"
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc CHANGES COPYING README TODO
%{_bindir}/plaympeg
%{_bindir}/gtv
%{_bindir}/glmovie
%{_mandir}/man1/*.gz

%files libs
%defattr(-,root,root,-)
%{_libdir}/libsmpeg-0.4.so.*

%files devel
%defattr(-,root,root,-)
%{_bindir}/smpeg-config
%{_includedir}/smpeg/
%{_libdir}/libsmpeg.so
%{_datadir}/aclocal/smpeg.m4


%changelog
* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.4.5-0.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.4.5-0.3
- rebuild for new F11 features

* Tue Sep 16 2008 kwizart < kwizart at gmail.com > - 0.4.5-0.2
- snapshot made again against 20080916svn (r370) 
  but removed from release tag since it hasn't changed since the previous version
- Multilib compliance

* Mon Oct 22 2007 kwizart < kwizart at gmail.com > - 0.4.5-0.1.20071022svn
- Add smpeg-snashot.sh
- Update snapshot 0.4.5 20071022svn

* Fri Oct  6 2006 Dams <anvil[AT]livna.org> - 0.4.4-11
- libsmpeg-0.4.so -> libsmpeg.so

* Fri Oct  6 2006 Dams <anvil[AT]livna.org> - 0.4.4-10
- Small cleanup
- Disabled static libraries

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field
- drop Epoch

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Fri Jan 20 2006 Adrian Reber <adrian@lisas.de> - 0.4.4-0.lvn.9
- Added patch from CVS to fix gcc 4.1 errors
- Dropped 0 Epoch

* Sat Dec  4 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.4-0.lvn.8
- Honor $RPM_OPT_FLAGS.
- Avoid aclocal >= 1.8 warnings from smpeg.m4.

* Sun May 23 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.4.4-0.lvn.7
- Added bug-fixes from CVS: smpeg-0.4.4-cvs-byteorder.patch,
  smpeg-0.4.4-cvs-createyuvoverlay.patch.

* Thu May 20 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.4.4-0.lvn.6
- Avoid rpath in smpeg-config.

* Thu Oct 16 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.4.4-0.fdr.5
- smpeg-devel requires SDL-devel.
- Brought in line with Fedora's spec template.
- Added version number patch.

* Sun May 11 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.4.4-0.fdr.4
- Corrected description text.
- Added TODO to documentation.
- Use RPM_BUILD_ROOT instead of macro.

* Sat May  3 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.4.4-0.fdr.3
- Added epoch to -devel requires.

* Sat Apr 26 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.4.4-0.fdr.2
- Added epoch.
- Bug-fixes from CVS.
- Added full path of source.

* Thu Mar  6 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0.4.4-0.fdr.1
- Initial Fedora RPM release.

* Tue Oct 29 2002 Marius L. Jøhndal <mariuslj at ifi.uio.no>
- Changed configure invocation to macro.
- Modified installation paths to use bindir, libdir etc.
- Patch for strange g++ 3.2 build errors.

* Fri Mar  3 2000 Sam Lantinga <hercules@lokigames.com>
- Split package into development and runtime packages
