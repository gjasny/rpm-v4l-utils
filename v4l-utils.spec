Name:           v4l-utils
Version:        0.8.8
Release:        6%{?dist}
Summary:        Utilities for video4linux and DVB devices
Group:          Applications/System
# ir-keytable and v4l2-sysfs-path are GPLv2 only
License:        GPLv2+ and GPLv2
URL:            http://www.linuxtv.org/downloads/v4l-utils/
Source0:        http://linuxtv.org/downloads/v4l-utils/v4l-utils-%{version}.tar.bz2
# Bugfixes from upstream git, these can all be dropped with the next release
Patch1:         0001-dvb-Fix-spelling-errors-found-by-lintian.patch
Patch2:         0002-libv4lconvert-Fix-decoding-of-160x120-Pixart-JPEG-im.patch
Patch3:         0003-Revert-tinyjpeg-Better-luminance-quantization-table-.patch
Patch4:         0004-libv4lconvert-Dynamic-quantization-tables-for-Pixart.patch
Patch5:         0005-libv4lconvert-Drop-Pixart-JPEG-frames-with-changing-.patch
Patch6:         0006-libv4lconvert-Further-Pixart-JPEG-decompression-twea.patch
Patch7:         0007-libv4lconvert-Fix-interpretation-of-bit-7-of-the-Pix.patch
Patch8:         0008-libv4lcontrol-Add-another-USB-ID-to-ASUS-table.patch
Patch9:         0009-libv4lcontrol-Add-Lenovo-Thinkpad-X220-Tablet-to-ups.patch
Patch10:        0010-libv4l2-Improve-VIDIOC_-_FMT-logging.patch
Patch11:        0011-libv4lconvert-replace-strndupa-with-more-portable-st.patch
Patch12:        0012-libdvbv5-Add-missing-includes.patch
Patch13:        0013-libv4l2-Ensure-we-always-set-buf-length-when-convert.patch
Patch14:        0014-libv4l2-dqbuf-Don-t-requeue-buffers-which-we-are-ret.patch
BuildRequires:  libjpeg-devel qt4-devel kernel-headers desktop-file-utils
# For /lib/udev/rules.d ownership
Requires:       udev
Requires:       libv4l = %{version}-%{release}

%description
v4l-utils is a collection of various video4linux (V4L) and DVB utilities. The
main v4l-utils package contains cx18-ctl, ir-keytable, ivtv-ctl, v4l2-ctl and
v4l2-sysfs-path.


%package        devel-tools
Summary:        Utilities for v4l2 / DVB driver development and debugging
# decode_tm6000 is GPLv2 only
License:        GPLv2+ and GPLv2
Requires:       libv4l = %{version}-%{release}

%description    devel-tools
Utilities for v4l2 / DVB driver authors: decode_tm6000, v4l2-compliance and
v4l2-dbg.


%package -n     qv4l2
Summary:        QT v4l2 test control and streaming test application
License:        GPLv2+
Requires:       libv4l = %{version}-%{release}

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


%package -n     libv4l-devel
Summary:        Development files for libv4l
Group:          Development/Libraries
License:        LGPLv2+
URL:            http://hansdegoede.livejournal.com/3636.html
Requires:       libv4l = %{version}-%{release}

%description -n libv4l-devel
The libv4l-devel package contains libraries and header files for
developing applications that use libv4l.


%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1


%build
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" \
  PREFIX=%{_prefix} LIBDIR=%{_libdir}


%install
make install PREFIX=%{_prefix} LIBDIR=%{_libdir} DESTDIR=$RPM_BUILD_ROOT
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/qv4l2.desktop


%post -n libv4l -p /sbin/ldconfig

%postun -n libv4l -p /sbin/ldconfig

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
%defattr(-,root,root,-)
%doc README
%dir %{_sysconfdir}/rc_keymaps
%config(noreplace) %{_sysconfdir}/rc_keymaps/*
%config(noreplace) %{_sysconfdir}/rc_maps.cfg
/lib/udev/rules.d/70-infrared.rules
%{_bindir}/cx18-ctl
%{_bindir}/dvb*
%{_bindir}/ir-keytable
%{_bindir}/ivtv-ctl
%{_bindir}/v4l2-ctl
%{_bindir}/v4l2-sysfs-path
%{_mandir}/man1/ir-keytable.1*

%files devel-tools
%defattr(-,root,root,-)
%doc README
%{_bindir}/decode_tm6000
%{_bindir}/v4l2-compliance
%{_sbindir}/v4l2-dbg

%files -n qv4l2
%defattr(-,root,root,-)
%doc README
%{_bindir}/qv4l2
%{_datadir}/applications/qv4l2.desktop
%{_datadir}/icons/hicolor/*/apps/qv4l2.*

%files -n libv4l
%defattr(-,root,root,-)
%doc COPYING.LIB COPYING ChangeLog README.lib TODO
%{_libdir}/libv4l*.so.*
%{_libdir}/libv4l

%files -n libv4l-devel
%defattr(-,root,root,-)
%doc README.lib-multi-threading
%{_includedir}/libv4l*.h
%{_libdir}/libv4l*.so
%{_libdir}/pkgconfig/libv4l*.pc


%changelog
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
