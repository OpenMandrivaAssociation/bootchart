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
