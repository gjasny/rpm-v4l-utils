Name:           v4l-utils
Version:        1.6.0
Release:        1%{?dist}
Summary:        Utilities for video4linux and DVB devices
Group:          Applications/System
# libdvbv5, dvbv5 utils, ir-keytable and v4l2-sysfs-path are GPLv2 only
License:        GPLv2+ and GPLv2
URL:            http://www.linuxtv.org/downloads/v4l-utils/
Source0:        http://linuxtv.org/downloads/v4l-utils/v4l-utils-%{version}.tar.bz2
BuildRequires:  libjpeg-devel qt4-devel kernel-headers desktop-file-utils
BuildRequires:  alsa-lib-devel doxygen
# For /lib/udev/rules.d ownership
Requires:       udev
Requires:       libv4l%{?_isa} = %{version}-%{release}

%description
v4l-utils is a collection of various video4linux (V4L) and DVB utilities. The
main v4l-utils package contains cx18-ctl, ir-keytable, ivtv-ctl, v4l2-ctl and
v4l2-sysfs-path.


%package        devel-tools
Summary:        Utilities for v4l2 / DVB driver development and debugging
# decode_tm6000 is GPLv2 only
License:        GPLv2+ and GPLv2
Requires:       libv4l%{?_isa} = %{version}-%{release}

%description    devel-tools
Utilities for v4l2 / DVB driver authors: decode_tm6000, v4l2-compliance and
v4l2-dbg.


%package -n     qv4l2
Summary:        QT v4l2 test control and streaming test application
License:        GPLv2+
Requires:       libv4l%{?_isa} = %{version}-%{release}

%description -n qv4l2
QT v4l2 test control and streaming test application.


%package -n     libv4l
Summary:        Collection of video4linux support libraries 
Group:          System Environment/Libraries
# Some of the decompression helpers are GPLv2, the rest is LGPLv2+
License:        LGPLv2+ and GPLv2
URL:            http://hansdegoede.livejournal.com/3636.html

%description -n libv4l
libv4l is a collection of libraries which adds a thin abstraction layer on
top of video4linux2 devices. The purpose of this (thin) layer is to make it
easy for application writers to support a wide variety of devices without
having to write separate code for different devices in the same class. libv4l
consists of 3 different libraries: libv4lconvert, libv4l1 and libv4l2.

libv4lconvert offers functions to convert from any (known) pixel-format
to V4l2_PIX_FMT_BGR24 or V4l2_PIX_FMT_YUV420.

libv4l1 offers the (deprecated) v4l1 API on top of v4l2 devices, independent
of the drivers for those devices supporting v4l1 compatibility (which many
v4l2 drivers do not).

libv4l2 offers the v4l2 API on top of v4l2 devices, while adding for the
application transparent libv4lconvert conversion where necessary.


%package -n     libdvbv5
Summary:        Libraries to control, scan and zap on Digital TV channels
Group:          Development/Libraries
License:        GPLv2

%description -n libdvbv5
Libraries to control, scan and zap on Digital TV channels

%package -n     libv4l-devel
Summary:        Development files for libv4l
Group:          Development/Libraries
License:        LGPLv2+
URL:            http://hansdegoede.livejournal.com/3636.html
Requires:       libv4l%{?_isa} = %{version}-%{release}

%description -n libv4l-devel
The libv4l-devel package contains libraries and header files for
developing applications that use libv4l.


%package -n     libdvbv5-devel
Summary:        Development files for libdvbv5
Group:          Development/Libraries
License:        GPLv2
Requires:       libdvbv5%{?_isa} = %{version}-%{release}

%description -n libdvbv5-devel
The libdvbv5-devel package contains libraries and header
files for developing applications that use libdvbv5.


%prep
%setup -q


%build
%configure --disable-static --enable-libdvbv5 --enable-doxygen-man
# Don't use rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}
make doxygen-run


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rm $RPM_BUILD_ROOT%{_libdir}/{v4l1compat.so,v4l2convert.so}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3/
cp -arv %{_builddir}/%{name}-%{version}/doxygen-doc/man/man3 $RPM_BUILD_ROOT%{_mandir}/
rm $RPM_BUILD_ROOT%{_mandir}/man3/_*3
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/qv4l2.desktop


%post -n libv4l -p /sbin/ldconfig

%postun -n libv4l -p /sbin/ldconfig

%post -n libdvbv5 -p /sbin/ldconfig

%postun -n libdvbv5 -p /sbin/ldconfig

%post -n qv4l2
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun -n qv4l2
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans -n qv4l2
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc README
%dir %{_sysconfdir}/rc_keymaps
%config(noreplace) %{_sysconfdir}/rc_maps.cfg
%{_udevrulesdir}/70-infrared.rules
%{_prefix}/lib/udev/rc_keymaps/*
%{_bindir}/cx18-ctl
%{_bindir}/dvb*
%{_bindir}/ir-keytable
%{_bindir}/ivtv-ctl
%{_bindir}/media-ctl
%{_bindir}/rds-ctl
%{_bindir}/v4l2-ctl
%{_bindir}/v4l2-sysfs-path
%{_mandir}/man1/*.1*

%files devel-tools
%doc README
%{_bindir}/decode_tm6000
%{_bindir}/v4l2-compliance
%{_sbindir}/v4l2-dbg

%files -n qv4l2
%doc README
%{_bindir}/qv4l2
%{_datadir}/applications/qv4l2.desktop
%{_datadir}/icons/hicolor/*/apps/qv4l2.*

%files -n libv4l
%doc COPYING.libv4l COPYING ChangeLog README.libv4l TODO
%{_libdir}/libv4l
%{_libdir}/libv4l*.so.*

%files -n libv4l-devel
%doc README.lib-multi-threading
%{_includedir}/libv4l*.h
%{_libdir}/libv4l*.so
%{_libdir}/pkgconfig/libv4l*.pc

%files -n libdvbv5
%doc COPYING ChangeLog lib/libdvbv5/README
%{_libdir}/libdvbv5*.so.*

%files -n libdvbv5-devel
%{_includedir}/libdvbv5/*.h
%{_libdir}/libdvbv5*.so
%{_libdir}/pkgconfig/libdvbv5*.pc
%{_mandir}/man3/*.3*


%changelog
* Sun Oct 05 2014 Mauro Carvalho Chehab - 1.6.0-1
- Upgrade to version 1.6.0

* Mon Sep 08 2014 Mauro Carvalho Chehab - 1.4.0-1
- Upgrade to version 1.4.0

* Fri Aug 22 2014 Mauro Carvalho Chehab - 1.2.1-3
- Add ALSA support on qv4l2 and fix a couple issues at spec file

* Thu Aug 21 2014 Mauro Carvalho Chehab - 1.2.1-2
- Update to version 1.2.1 and add package for libdvbv5

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug  3 2013 Hans de Goede <hdegoede@redhat.com> - 1.0.0-1
- New upstream release 1.0.0 final
- Drop libdvb5 (made private upstream for now)

* Fri Jun 14 2013 Hans de Goede <hdegoede@redhat.com> - 0.9.5-2
- Add a few libv4l2rds patches from upstream, which bring libv4l2rds to its
  final API / ABI, so that apps build against it won't need a rebuild in the
  future

* Sun Jun  9 2013 Hans de Goede <hdegoede@redhat.com> - 0.9.5-1
- New upstream release 0.9.5 (rhbz#970412)
- Modernize specfile a bit

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 0.8.8-5
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.8.8-4
- rebuild against new libjpeg

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  9 2012 Hans de Goede <hdegoede@redhat.com> - 0.8.8-2
- Cherry-pick 2 patches from upstream git fixing an exotic crash (rhbz#838279)

* Tue May 22 2012 Hans de Goede <hdegoede@redhat.com> - 0.8.8-1
- New upstream release 0.8.8
- Add patches from upstream git to improve Pixart JPEG decoding
- Add patch from upstream git to fix building with latest kernels (rhbz#823863)

* Mon Apr  9 2012 Hans de Goede <hdegoede@redhat.com> - 0.8.7-1
- New upstream release 0.8.7
- Fixes rhbz#807656

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 17 2011 Hans de Goede <hdegoede@redhat.com> 0.8.5-1
- New upstream release 0.8.5
- Fixes rhbz#711492

* Wed Jun  1 2011 Hans de Goede <hdegoede@redhat.com> 0.8.4-1
- New upstream release 0.8.4

* Sat Mar 12 2011 Hans de Goede <hdegoede@redhat.com> 0.8.3-2
- Add a .desktop file for qv4l2
- Add fully versioned Requires on libv4l to other (sub)packages

* Thu Feb 10 2011 Hans de Goede <hdegoede@redhat.com> 0.8.3-1
- New upstream release 0.8.3

* Wed Jan 26 2011 Hans de Goede <hdegoede@redhat.com> 0.8.2-3
- Add missing BuildRequires: kernel-headers

* Mon Jan 24 2011 Hans de Goede <hdegoede@redhat.com> 0.8.2-2
- Change tarbal to official upstream 0.8.2 release
- This fixes multiple Makefile issues pointed out in the review (#671883)
- Add ir-keytable config files
- Explicitly specify CXXFLAGS so that qv4l2 gets build with rpm_opt_flags too

* Sat Jan 22 2011 Hans de Goede <hdegoede@redhat.com> 0.8.2-1
- Initial Fedora package
