Name:          taskjuggler
Version:       2.4.3
Release:       5%{?dist}
Summary:       Project management tool

Group:         Applications/Productivity
License:       GPLv2
URL:           http://www.taskjuggler.org
Source0:       http://www.taskjuggler.org/download/%{name}-%{version}.tar.bz2
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?fedora} < 10 && 0%{?rhel} < 6
BuildRequires: kdepim-devel
%else
BuildRequires: kdepim3-devel
BuildRequires: kdelibs3-devel
%endif
# need gettext for untranslated .po files
Buildrequires: gettext
Buildrequires: qt3 qt3-devel
Buildrequires: xmlto
Requires: %{name}-libs = %{version}-%{release}
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%description
TaskJuggler is a modern and powerful project management tool. Its new approach
to project planning and tracking is far superior to the commonly used Gantt
chart editing tools. It has already been successfully used in many projects
and scales easily to projects with hundreds of resources and thousands of
tasks. It covers the complete spectrum of project management tasks from the
first idea to the completion of the project. It assists you during project
scoping, resource assignment, cost and revenue planning, and risk and
communication management.

%package libs
Summary: Libraries for %{name}
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description libs
Libraries for TaskJuggler package.

%prep
%setup -q

%build
[ -n "$QTDIR" ] || . %{_sysconfdir}/profile.d/qt.sh
%configure --with-qt-includes=%{_libdir}/qt-3.3/include --with-qt-libraries=%{_libdir}/qt-3.3/lib --with-kde-support=yes --disable-rpath
# doc build fails with -j4

#/foo/bar timezone is completely valid and interpreted as UTC,skipping test
rm -f TestSuite/Syntax/Errors/Timezone.tjp
make

#generate manpages with xmlto
xmlto man --skip-validation man/en/taskjuggler.xml
xmlto man --skip-validation man/en/TaskJugglerUI.xml


%install
rm -rf $RPM_BUILD_ROOT
export DESTDIR="$RPM_BUILD_ROOT"
make install

desktop-file-install --vendor fedora \
        --delete-original \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
        --add-category X-Fedora --add-category Application \
        --add-category Office \
        ${RPM_BUILD_ROOT}/%{_datadir}/applications/kde/taskjuggler.desktop

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cp -p *.1 $RPM_BUILD_ROOT%{_mandir}/man1
rm $RPM_BUILD_ROOT%{_libdir}/libtaskjuggler.{la,so}
mv $RPM_BUILD_ROOT%{_docdir}/packages/* $RPM_BUILD_ROOT%{_docdir}
rm -rf $RPM_BUILD_ROOT%{_docdir}/packages

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post
/sbin/ldconfig
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/{crystalsvg,hicolor} || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/crystalsvg || :
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%post libs -p /sbin/ldconfig

%postun
/sbin/ldconfig
update-desktop-database &> /dev/null ||:
touch --no-create %{_datadir}/icons/{crystalsvg,hicolor} || :
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/crystalsvg || :
   %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog README TODO
%{_bindir}/TaskJugglerUI
%{_bindir}/taskjuggler
%{_datadir}/applications/fedora-taskjuggler.desktop
%{_datadir}/applications/kde
%{_datadir}/apps/*
%{_datadir}/config/taskjugglerrc
%{_docdir}/HTML/en/*
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/*
%{_datadir}/icons/*
%{_datadir}/mimelnk/application/*.desktop
%{_mandir}/man1/*


%files libs
%defattr(-,root,root,-)
%{_libdir}/libtaskjuggler*

%changelog
* Thu May 20 2010 Radek Novacek <rnovacek@redhat.com> - 2.4.3-5
- Remove duplicit gtk-update-icon-cache from post sections
- Resolves: #593056

* Thu Jan 28 2010 Radek Novacek <rnovacek@redhat.com> - 2.4.3-4
- Changed licence from GPL+ to GPLv2
- Fixed mixed tabs and spaces in specfile
- Add %%post and %%postun sections for libs subpackage

* Fri Nov 13 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.4.3-3.1
- Fix conditional for RHEL

* Fri Aug 28 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.3-3
- generate and ship manpages for taskjuggler and taskjugglerUI
- add disttag

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.3-1
- New upstream release 2.4.3

* Mon Jul 13 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.2-1
- New upstream release 2.4.2

* Thu Jun 18 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.2-0.2.beta2
- upstream beta2 release candidate

* Mon May 25 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.2-0.1.beta1
- upstream beta1 release candidate

* Tue Mar 10 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.1-8
- Remove obsoletes, use Requires (#489496)

* Mon Mar 09 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.1-7
- build with ICal support again (#488347, #467136)

* Tue Mar 03 2009 Ondrej Vasik <ovasik@redhat.com> - 2.4.1-6
- fix build requires, rebuild for F11

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 04 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.1-4
- install taskjuggler documentation in docdir and do own
  that dir (#474600) , removed trailing spaces in spec file

* Mon Jun  9 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.1-3
- disable kdepim support on F10+, kdepim 3 no longer available

* Tue May 20 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.1-2
- kdepim broken dependencies rebuild

* Wed May 14 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.1-1
- new upstream release

* Tue May 13 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.1-0.2.beta2
- fixed typo in libs subpackage obsolete (which caused installation
  troubles)

* Mon Apr 28 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.1-0.1.beta2
- upstream beta2 release candidate

* Thu Mar  6 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.0-7
- separate libs subpackage (#343251, multiarch conflicts)

* Wed Feb 13 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.0-6
- gcc43 rebuild + resolving issues

* Thu Jan 10 2008 Ondrej Vasik <ovasik@redhat.com> - 2.4.0-5
- Fixed crash when zooming a report after a non-embedded 
  report has been viewed last(upstream).  

* Fri Oct  5 2007 Ondrej Vasik <ovasik@redhat.com> - 2.4.0-4
- fixed serious bug in floating point formatter(upstream)

* Mon Aug 27 2007 Ondrej Vasik <ovasik@redhat.com> - 2.4.0-3
- fixed License tag
- rebuilt for F8

* Tue Jul  3 2007 Ondrej Vasik <ovasik@redhat.com> - 2.4.0-2
- new tarball from upstream(previous had one blocker included)

* Fri Jun 22 2007 Ondrej Vasik <ovasik@redhat.com> - 2.4.0-1
- update to latest stable upstream version(2.4.0)
- removed patches included in 2.4.0

* Fri Jun  8 2007 Jens Petersen <petersen@redhat.com> - 2.3.1-3
- setup QTDIR and use find_lang macro to fix build
- buildrequire gettext for untranslated .po file

* Thu Jun  7 2007 Ondrej Vasik  <ovasik@redhat.com> -2.3.1-2
- fixed number of memory leaks (from upstream)
- removed _smp_mflags to avoid build failures with 4+ cpus (#233028)

* Thu Mar  8 2007 Jens Petersen <petersen@redhat.com> - 2.3.1-1
- update to 2.3.1
- improve taskjuggler-2.1.1-docbook.patch to remove explicit systemid (#231422)

* Wed Sep 27 2006 Jens Petersen <petersen@redhat.com> - 2.3.0-1
- update to 2.3.0

* Mon May  8 2006 Jens Petersen <petersen@redhat.com> - 2.2.0-1
- packaging fixes from John Mahowald (#166470)

* Tue Mar 28 2006 Jens Petersen <petersen@redhat.com>
- package for Fedora Extras
