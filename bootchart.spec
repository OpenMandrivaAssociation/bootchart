%define pybootchart_rev r124

Name:           bootchart
Version:        0.9
Release:        %mkrel 9
Summary:        Boot Process Performance Visualization
License:        GPL
Url:            http://www.bootchart.org/
Source0:        http://www.bootchart.org/dist/SOURCES/%name-%version.tar.bz2
Source2:	bootchartd.1
Source3:	bootchartd.conf.5
Source4:	http://pybootchartgui.googlecode.com/files/pybootchartgui-%{pybootchart_rev}.tar.bz2
# (fc) 0.9-6mdv upgrade bootchartd to latest svn release
Patch0:		bootchart-0.9-svn.patch
# (fc) 0.9-6mdv fix initrd support (rtp)
Patch1:		bootchart-0.9-initrd.patch
# (fc) 0.9-7mdv fix bootchart when root fs is readonly
Patch2:		bootchart-0.9-readonly.patch
# (fc) 0.9-7mdv detect more programs as a display manager (or to stop login)
Patch3:		bootchart-0.9-detect-more-programs-to-stop-early-login.patch
# (fc) 0.9-7mdv fix runlevel parsing in inittab
Patch4:		bootchart-0.9-fixrunlevel.patch
# (fc) 0.9-7mdv fix autostoplogger 
Patch5:		bootchart-0.9-autostoplogger.patch
# (fc) 0.9-7mdv enable process accounting
Patch6:		bootchart-0.9-accounting.patch
# (fc) 0.9-7mdv enable early_login detection on Mandriva
Patch7:		bootchart-0.9-early.patch
# (fc) 0.9-9mdv monitor threads (SUSE)
Patch8:		bootchart-0.9-monitor-threads.patch
# (fc) 0.9-9mdv enforce bash for bootchartd (SUSE)
Patch9:		bootchart-0.9-bash.patch
# (fc) 0.9-9mdv use /lib/bootchartd/mnt for tmpfs (SUSE)
Patch10:	bootchart-0.9-libmnt.patch
# (fc) 0.9-9mdv enable auto-render (SUSE)
Patch11:	bootchart-0.9-autorender.patch
# (fc) 0.9-9mdv handle unknown runlevel (SUSE)
Patch12:	bootchart-0.9-unknown-runlevel.patch
# (fc) 0.9-9mdv Fix max-y (SUSE)
Patch13:	pybootchartgui-r124.diff
# (fc) 0.9-9mdv update to latest SVN (r136)
Patch14:	pybootchartgui-r124-svnfixes.patch
# (fc) 0.9-9mdv fix defaults
Patch15:	pybootchartgui-r124-fixdefaults.patch
# (fc) 0.9-9mdv fix format argument handling on command line
Patch16:	pybootchartgui-r124-fixformat.patch
Group:          Monitoring
BuildRoot:      %_tmppath/%name-%version-buildroot
BuildRequires: python-devel


%description
Bootchart is a tool for performance analysis and visualization of the GNU/Linux
boot process.  Resource utilization and process information are collected
during the boot process and can later be displayed in a PNG, SVG or EPS-encoded
chart.

%package logger
Summary:        Boot logging script for %{name}
Group:          System/Kernel and hardware
Suggests:	psacct

%description logger
The boot logging script for %{name} cant be used through adding
"init=/sbin/bootchartd" to the kernel command line in GRUB or LILO boot menu.
It collects data about the boot process that can later be processed
by %name.

%prep
%setup -q -a4
%patch0 -p1 -b .svn
%patch1 -p1 -b .initrd
%patch2 -p1 -b .readonly
%patch3 -p1 -b .detect-more-programs
%patch4 -p1 -b .runlevel
%patch5 -p1 -b .autostoplogger
%patch6 -p1 -b .accounting
%patch7 -p1 -b .early
%patch8 -p1 -b .monitor-threads
%patch9 -p1 -b .bash
%patch10 -p1 -b .libmnt
%patch11 -p1 -b .autorender
%patch12 -p1 -b .unknown-runlevel
cd pybootchartgui-%{pybootchart_rev}
%patch13 -p1 -b .fix-maxy
%patch14 -p1 -b .svnfixes
%patch15 -p1 -b .fixdefaults
%patch16 -p1 -b .fixformat
cd -

%build


%install
rm -rf $RPM_BUILD_ROOT

# logger
install -D -m 755 script/bootchartd $RPM_BUILD_ROOT/sbin/bootchartd
install -D -m 644 script/bootchartd.conf $RPM_BUILD_ROOT/etc/bootchartd.conf
install -d -m 755 $RPM_BUILD_ROOT/lib/bootchartd/mnt

# manpages
install -d -m 755 $RPM_BUILD_ROOT/%{_mandir}/man1 $RPM_BUILD_ROOT/%{_mandir}/man5
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/%{_mandir}/man1/
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_mandir}/man5/

# pybootchart

cd pybootchartgui-%{pybootchart_rev}
install -d $RPM_BUILD_ROOT%py_sitedir/pybootchartgui
cp pybootchartgui/*.py $RPM_BUILD_ROOT%py_sitedir/pybootchartgui
install -D -m 755 pybootchartgui.py $RPM_BUILD_ROOT%_bindir/pybootchartgui
pushd $RPM_BUILD_ROOT%py_sitedir/pybootchartgui
python %py_libdir/py_compile.py *.py
PYTHONOPTIMIZE=1 python %py_libdir/py_compile.py *.py
popd

ln -s pybootchartgui $RPM_BUILD_ROOT%{_bindir}/bootchart

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,)
%doc ChangeLog COPYING INSTALL README TODO lib/LICENSE.cli.txt lib/LICENSE.compress.txt lib/LICENSE.epsgraphics.txt lib/NOTICE.txt
%_bindir/pybootchartgui
%_bindir/bootchart
%py_sitedir/pybootchartgui

%files logger
%defattr(-,root,root,)
%doc README.logger
/sbin/bootchartd
%config(noreplace) %_sysconfdir/bootchartd.conf
%dir /lib/bootchartd
%dir /lib/bootchartd/mnt
%{_mandir}/man*/bootchartd*

