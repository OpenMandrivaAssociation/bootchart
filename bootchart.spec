Name:           bootchart
Version:        0.9
Release:        %mkrel 6
Summary:        Boot Process Performance Visualization
License:        GPL
Url:            http://www.bootchart.org/
Source0:        http://www.bootchart.org/dist/SOURCES/%name-%version.tar.bz2
Source1:	bootchart.1
Source2:	bootchartd.1
Source3:	bootchartd.conf.5
# (fc) 0.9-6mdv upgrade bootchartd to latest svn release
Patch0:		bootchart-0.9-svn.patch
# (fc) 0.9-6mdv fix initrd support (rtp)
Patch1:		bootchart-0.9-initrd.patch
Group:          Monitoring
Requires:       jpackage-utils, jakarta-commons-cli, java
BuildRequires:  ant, java-rpmbuild jakarta-commons-cli
BuildArch:      noarch
BuildRoot:      %_tmppath/%name-%version-buildroot


%description
Bootchart is a tool for performance analysis and visualization of the GNU/Linux
boot process.  Resource utilization and process information are collected
during the boot process and can later be displayed in a PNG, SVG or EPS-encoded
chart.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Books/Computer books

%description javadoc
This is the java documentation for %{name}.

%package logger
Summary:        Boot logging script for %{name}
Group:          System/Kernel and hardware
Suggests:		psacct

%description logger
The boot logging script for %{name} cant be used through adding
"init=/sbin/bootchartd" to the kernel command line in GRUB or LILO boot menu.
It collects data about the boot process that can later be processed
by %name.

%prep
%setup -q
%patch0 -p1 -b .svn
%patch1 -p1 -b .initrd

%build
# Remove the bundled commons-cli
rm -rf lib/org/apache/commons/cli lib/org/apache/commons/lang
CLASSPATH=%{_javadir}/commons-cli.jar %ant

%install
rm -rf $RPM_BUILD_ROOT

# jar
install -D -m 644 %{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# script
install -D -m 755 script/%{name} $RPM_BUILD_ROOT%{_bindir}/%{name}

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# logger
install -D -m 755 script/bootchartd $RPM_BUILD_ROOT/sbin/bootchartd
install -D -m 644 script/bootchartd.conf $RPM_BUILD_ROOT/etc/bootchartd.conf
install -d -m 755 $RPM_BUILD_ROOT/mnt/bootchartd

# manpages
install -d -m 755 $RPM_BUILD_ROOT/%{_mandir}/man1 $RPM_BUILD_ROOT/%{_mandir}/man5
install -m 644 %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT/%{_mandir}/man1/
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/%{_mandir}/man5/

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(-,root,root,)
%doc ChangeLog COPYING INSTALL README TODO lib/LICENSE.cli.txt lib/LICENSE.compress.txt lib/LICENSE.epsgraphics.txt lib/NOTICE.txt
%{_javadir}/*
%dir %attr(0755,root,root) %{_bindir}/bootchart
%{_mandir}/man1/bootchart.1*

%files javadoc
%defattr(-,root,root,)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files logger
%defattr(-,root,root,)
%doc README.logger
/sbin/bootchartd
%config(noreplace) %_sysconfdir/bootchartd.conf
%dir /mnt/bootchartd
%{_mandir}/man*/bootchartd*
