Name:       nemo-mobile-session
Summary:    Target for nemo systemd user session
Version:    13
Release:    0
Group:      System/Libraries
License:    Public Domain
URL:        https://github.com/nemomobile/nemo-mobile-session
Source0:    %{name}-%{version}.tar.gz
Requires:   systemd >= 187
Requires:   xorg-launch-helper
Obsoletes:  uxlaunch

%description
Target for nemo systemd user session


%prep
%setup -q -n %{name}-%{version}

%install

mkdir -p %{buildroot}%{_libdir}/systemd/user/nemo-middleware.target.wants/
mkdir -p %{buildroot}%{_libdir}/systemd/user/nemo-mobile-session.target.wants/
mkdir -p %{buildroot}/lib/systemd/system/graphical.target.wants/
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/
mkdir -p %{buildroot}/var/lib/environment/nemo
mkdir -p %{buildroot}%{_sysconfdir}/systemd/system/

# User services
install -m 0644 services/nemo-mobile-session.target %{buildroot}%{_libdir}/systemd/user/
install -m 0644 services/nemo-middleware.target %{buildroot}%{_libdir}/systemd/user/

# Root services
install -m 0644 services/user-session@.service %{buildroot}/lib/systemd/system/
install -m 0644 services/start-user-session@.service %{buildroot}/lib/systemd/system/
install -m 0644 services/init-done.service %{buildroot}/lib/systemd/system/

# conf
install -m 0644 conf/50-nemo-mobile-ui.conf %{buildroot}/var/lib/environment/nemo/
install -D -m 0644 conf/nemo-session-tmp.conf %{buildroot}%{_libdir}/tmpfiles.d/nemo-session-tmp.conf

# bin
install -D -m 0744 bin/start-user-session %{buildroot}%{_libdir}/startup/start-user-session
install -D -m 0744 bin/init-done %{buildroot}/%{_libdir}/startup/init-done
install -D -m 0744 bin/killx %{buildroot}/%{_libdir}/startup/killx

ln -sf ../start-user-session@.service %{buildroot}/lib/systemd/system/graphical.target.wants/start-user-session@USER.service
ln -sf ../init-done.service %{buildroot}/lib/systemd/system/graphical.target.wants/
# In nemo actdead is not (yet) supported. We define actdead (runlevel4) to poweroff
ln -sf /lib/systemd/system/poweroff.target %{buildroot}%{_sysconfdir}/systemd/system/runlevel4.target

# nemo-mobile-session dependencies
ln -sf nemo-mobile-session.target %{buildroot}%{_libdir}/systemd/user/default.target
ln -sf ../lipstick.service %{buildroot}%{_libdir}/systemd/user/nemo-mobile-session.target.wants/
ln -sf ../mapplauncherd.target %{buildroot}%{_libdir}/systemd/user/nemo-mobile-session.target.wants/
ln -sf ../pulseaudio.service %{buildroot}%{_libdir}/systemd/user/nemo-mobile-session.target.wants/
ln -sf ../contactsd.service %{buildroot}%{_libdir}/systemd/user/nemo-mobile-session.target.wants/
ln -sf ../tracker-miner-fs.service %{buildroot}%{_libdir}/systemd/user/nemo-mobile-session.target.wants/
ln -sf ../voicecall-ui-prestart.service %{buildroot}%{_libdir}/systemd/user/nemo-mobile-session.target.wants/
ln -sf ../qmlpinquery.service %{buildroot}%{_libdir}/systemd/user/nemo-mobile-session.target.wants/
ln -sf ../maliit-server.service %{buildroot}%{_libdir}/systemd/user/nemo-mobile-session.target.wants/
ln -sf ../mcompositor.service %{buildroot}%{_libdir}/systemd/user/nemo-mobile-session.target.wants/
ln -sf ../mthemedaemon.service %{buildroot}%{_libdir}/systemd/user/nemo-mobile-session.target.wants/
ln -sf ../ngfd.service %{buildroot}%{_libdir}/systemd/user/nemo-mobile-session.target.wants/
ln -sf ../ohm-session-agent.service %{buildroot}%{_libdir}/systemd/user/nemo-mobile-session.target.wants/

%files
%defattr(-,root,root,-)
%config /var/lib/environment/nemo/50-nemo-mobile-ui.conf
%{_libdir}/tmpfiles.d/nemo-session-tmp.conf
%{_libdir}/systemd/user/nemo-mobile-session.target
%{_libdir}/systemd/user/nemo-mobile-session.target.wants/
%{_libdir}/systemd/user/nemo-middleware.target/
%{_libdir}/systemd/user/nemo-middleware.target.wants/
%{_libdir}/systemd/user/default.target
/lib/systemd/system/graphical.target.wants/start-user-session@USER.service
/lib/systemd/system/graphical.target.wants/init-done.service
/lib/systemd/system/user-session@.service
/lib/systemd/system/start-user-session@.service
/lib/systemd/system/init-done.service
%{_libdir}/startup/start-user-session
%{_libdir}/startup/init-done
%{_libdir}/startup/killx
%{_sysconfdir}/systemd/system/runlevel4.target 

