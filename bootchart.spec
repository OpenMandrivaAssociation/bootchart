%define pybootchartgui_rev r124

%define bootchart2_version 0.11.4

Name:           bootchart
Version:        2.%{bootchart2_version}
Release:        %mkrel 2
Summary:        Boot Process Performance Visualization
License:        GPLv3
Url:            http://www.bootchart.org/
Source0:        http://github.com/mmeeks/bootchart/%{name}2-%{bootchart2_version}.tar.bz2
Group:          Monitoring
BuildRoot:      %_tmppath/%name-%version-buildroot
BuildRequires: python-devel
Obsoletes:	bootchart-logger < 2.0.0.9
Provides:	bootchart-logger = %{version}-%{release}


%description
Bootchart is a tool for performance analysis and visualization of the GNU/Linux
boot process.  Resource utilization and process information are collected
during the boot process and can later be displayed in a PNG, SVG or EPS-encoded
chart.


%prep
%setup -q -n %{name}2-%{bootchart2_version}

%build
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std PY_LIBDIR=%py_platlibdir 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,)
%doc COPYING README.* TODO README
%_bindir/pybootchartgui
%py_platsitedir/pybootchartgui
/sbin/bootchartd
%config(noreplace) %_sysconfdir/bootchartd.conf
%dir /lib/bootchart
%dir /lib/bootchart/tmpfs
%dir /lib/bootchart/bootchart-collector


%changelog
* Tue Nov 02 2010 Michael Scherer <misc@mandriva.org> 2.0.11.4-2mdv2011.0
+ Revision: 592374
- rebuild for python 2.7

* Mon May 31 2010 Frederic Crozat <fcrozat@mandriva.com> 2.0.11.4-1mdv2010.1
+ Revision: 546733
- Release 2.0.11.4
- Remove patch0 (merged upstream)

* Wed Mar 10 2010 Frederic Crozat <fcrozat@mandriva.com> 2.0.0.9-2mdv2010.1
+ Revision: 517444
-fix build on x86-64
- Release 2.0.0.9, based on Michael Meeks bootchart2 rewrite
- Remove all patches (obsolete or merged upstream)
- Drop pybootchart tarball, merged upstream
- Patch0 (GIT): update to latest git checkout

* Sat Nov 28 2009 Olivier Blin <oblin@mandriva.com> 0.9-10mdv2010.1
+ Revision: 470984
- fix ty(ti)po (from dedoimedo.com review)

* Fri Sep 25 2009 Frederic Crozat <fcrozat@mandriva.com> 0.9-9mdv2010.0
+ Revision: 448668
- Fix build on x86-64
- Add documentation for pybootchartgui
- Fix buildrequires
- Replace java graph generator with pybootchargui
- Patch8 (SUSE): monitor threads
- Patch9 (SUSE): enforce bash for bootchartd
- Patch10 (SUSE): use /lib/bootchartd/mnt for tmpfs
- Patch11 (SUSE):  enable auto-render
- Patch12 (SUSE):  handle unknown runlevel
- Patch13 (SUSE):  Fix max-y in pybootchargui
- Patch14 (SVN): update to latest SVN of pybootchartgui (r136)
- Patch15: fix defaults for pybootchartgui to be similar to java bootchart
- Patch16:  fix format argument handling on command line

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 0.9-8mdv2010.0
+ Revision: 436870
- rebuild

* Thu Jan 22 2009 Frederic Crozat <fcrozat@mandriva.com> 0.9-7mdv2009.1
+ Revision: 332531
- Update patch0, some files were missing
- Patch2: fix bootchart when rootfs is readonly
- Patch3: detect ldm as display manager
- Patch4: fix runlevel parsing in inittab
- Patch5: fix autostoplogger
- Patch6: enable process accouting
- Patch7: enable early_login detection on Mandriva

* Mon Oct 27 2008 Frederic Crozat <fcrozat@mandriva.com> 0.9-6mdv2009.1
+ Revision: 297724
- Patch0 : upgrade bootchart to svn version (support for initrd)
- Patch1 (rtp): fix initrd support for Mandriva
- Add manpages from SVN
- Fix java build (akurtakov)

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 0.9-5mdv2009.0
+ Revision: 266339
- rebuild early 2009.0 package (before pixel changes)

* Tue May 27 2008 Thierry Vignaud <tv@mandriva.org> 0.9-4mdv2009.0
+ Revision: 211746
- suggests psacct
- renderer needs java
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0.9-3mdv2008.1
+ Revision: 120838
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Wed Aug 22 2007 Thierry Vignaud <tv@mandriva.org> 0.9-2mdv2008.0
+ Revision: 69057
- add builrequires jakarta-commons-cli
- rebuild
- Import bootchart



* Tue Nov 15 2005 Frederic Crozat <fcrozat@mandriva.com> 0.9-1mdk
- Release 0.9

* Mon Aug 08 2005 Thierry Vignaud <tvignaud@mandriva.com> 0.8-1mdk
- initial release
