%define _default_patch_fuzz 2

Name:           smpeg
Version:        0.4.4
Release:        13%{?dist}
Summary:        MPEG library for SDL

Group:          System Environment/Libraries
License:        LGPL
URL:            http://icculus.org/smpeg/
Source0:        ftp://sunsite.dk/pub/os/linux/loki/open-source/smpeg/smpeg-0.4.4.tar.gz
Patch0:         smpeg-0.4.4-gcc32.patch
Patch1:         smpeg-0.4.4-fixes.patch
Patch2:         smpeg-0.4.4-version.patch
Patch3:         smpeg-0.4.4-cvs-byteorder.patch
Patch4:         smpeg-0.4.4-cvs-createyuvoverlay.patch
Patch5:         smpeg-0.4.4-aclocal18.patch
Patch6:         smpeg-0.4.4-optflags.patch
#http://cvs.icculus.org/cvs/smpeg/MPEGaudio.h?r1=1.24&r2=1.25&sortby=date&makepatch=1&diff_format=u
Patch7:         smpeg-0.4.4-gcc41.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  SDL-devel
BuildRequires:  gtk+-devel
BuildRequires:  automake14
BuildRequires:  autoconf

%description
SMPEG is based on UC Berkeley's mpeg_play software MPEG decoder
and SPLAY, an MPEG audio decoder created by Woo-jae Jung. SMPEG has
completed the initial work to wed these two projects in order to 
create a general purpose MPEG video/audio player for the Linux OS. 


%package devel
Summary:        Header files and static libraries for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       SDL-devel

%description devel
This package contains header files and static libraries for %{name}.


%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p1
%{__perl} -pi -e 's|\s*\@SMPEG_RLD_FLAGS\@||' smpeg-config.in
aclocal-1.4
automake-1.4 -a
autoconf


%build
%configure --disable-debug --disable-opengl-player --disable-static
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT 
make install DESTDIR=$RPM_BUILD_ROOT
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
%{_libdir}/libsmpeg-0.4.so.*
%{_mandir}/man[^3]/*

%files devel
%defattr(-,root,root,-)
%{_bindir}/smpeg-config
%{_includedir}/smpeg
%{_libdir}/libsmpeg.so
%{_datadir}/aclocal/smpeg.m4


%changelog
* Sun Aug 17 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.4.4-13
- added _default_patch_fuzz define to make it build for rawhide

* Mon Aug 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.4.4-12
- rebuild

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
