Name:       nemo-mobile-session
Summary:    Target for nemo systemd user session
Version:    13
Release:    0
Group:      System/Libraries
License:    Public Domain
URL:        https://github.com/nemomobile/nemo-mobile-session
Source0:    %{name}-%{version}.tar.gz
Requires:   systemd >= 187
Requires: systemd-user-session-targets
BuildRequires: systemd-user-session-targets
Requires:   xorg-launch-helper
Obsoletes:  uxlaunch
# mer release 0.20130605.1 changed login.defs
Requires: setup >= 2.8.56-1.1.33
BuildRequires: oneshot
Requires: oneshot
%{_oneshot_requires_post}
Requires(post): /bin/chgrp, /usr/sbin/groupmod

%description
Target for nemo systemd user session


%prep
%setup -q -n %{name}-%{version}

%install

mkdir -p %{buildroot}%{_libdir}/systemd/user/nemo-middleware.target.wants/
mkdir -p %{buildroot}%{_libdir}/systemd/user/nemo-mobile-session.target.wants/
mkdir -p %{buildroot}%{_libdir}/systemd/user/xorg.target.wants/
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
# temp transition phase towards new targets
ln -sf ../pre-user-session.target %{buildroot}%{_libdir}/systemd/user/xorg.target.wants/
ln -sf ../user-session.target %{buildroot}%{_libdir}/systemd/user/nemo-mobile-session.target.wants/
ln -sf ../post-user-session.target %{buildroot}%{_libdir}/systemd/user/nemo-mobile-session.target.wants/

# login.defs
mkdir -p %{buildroot}/%{_oneshotdir}
install -D -m 755 oneshot/correct-users %{buildroot}/%{_oneshotdir}

%post
if [ $1 -gt 1 ] ; then
  # known changes
  if [ ! "$(grep audio %{_sysconfdir}/group | cut -d: -f3)" -eq 1005 ]; then
    groupmod -g 1005 audio
  fi
  if [ ! "$(grep nobody %{_sysconfdir}/group | cut -d: -f3)" -eq 9999 ]; then
    groupmod -g 9999 nobody
  fi

  [ -f /usr/bin/ssh-agent ] && chgrp nobody %{_bindir}/ssh-agent

  # backup group and passwd
  mkdir -p %{_sharedstatedir}/misc
  [ ! -f %{_sharedstatedir}/misc/passwd.old ] && cp %{_sysconfdir}/passwd %{_sharedstatedir}/misc/passwd.old
  [ ! -f %{_sharedstatedir}/misc/group.old ] && cp %{_sysconfdir}/group %{_sharedstatedir}/misc/group.old

  # device specific changes
  %{_bindir}/add-oneshot correct-users

fi

%files
%defattr(-,root,root,-)
%config /var/lib/environment/nemo/50-nemo-mobile-ui.conf
%{_libdir}/tmpfiles.d/nemo-session-tmp.conf
%{_libdir}/systemd/user/nemo-mobile-session.target
%{_libdir}/systemd/user/nemo-mobile-session.target.wants/
%{_libdir}/systemd/user/nemo-middleware.target/
%{_libdir}/systemd/user/nemo-middleware.target.wants/
%{_libdir}/systemd/user/default.target
%{_libdir}/systemd/user/xorg.target.wants/pre-user-session.target
/lib/systemd/system/graphical.target.wants/start-user-session@USER.service
/lib/systemd/system/graphical.target.wants/init-done.service
/lib/systemd/system/user-session@.service
/lib/systemd/system/start-user-session@.service
/lib/systemd/system/init-done.service
%{_libdir}/startup/start-user-session
%{_libdir}/startup/init-done
%{_libdir}/startup/killx
%{_sysconfdir}/systemd/system/runlevel4.target 
%{_oneshotdir}/correct-users

