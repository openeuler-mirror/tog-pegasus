%global PEGASUS_BUILD_TEST_RPM 1
%global srcname pegasus
%global major_ver 2.14
%global pegasus_gid 65
%global pegasus_uid 66

Name:           tog-pegasus
Version:        %{major_ver}.1
Release:        53
Epoch:          2
Summary:        OpenPegasus WBEM Services for Linux
License:        MIT
URL:            http://www.openpegasus.org
Source0:        https://collaboration.opengroup.org/pegasus/documents/32572/pegasus-%{version}.tar.gz
Source1:        tog-pegasus.tmpfiles
Source2:        tog-pegasus.service
Source3:        access.conf
Source4:        cim_schema_2.38.0Experimental-MOFs.zip
Source5:       generate-certs

Patch1:         pegasus-2.9.0-no-rpath.patch
Patch2:         pegasus-2.7.0-PIE.patch
Patch3:         pegasus-2.9.0-redhat-config.patch
Patch4:         pegasus-2.9.0-cmpi-provider-lib.patch
Patch5:         pegasus-2.5.1-pam-wbem.patch
Patch6:         pegasus-2.7.0-no-snmp-tests.patch 
Patch7:         pegasus-2.9.0-local-or-remote-auth.patch
Patch8:         pegasus-2.9.1-getpagesize.patch
Patch9:        pegasus-2.10.0-dont-strip.patch
Patch10:        pegasus-2.12.0-null_value.patch
Patch11:        pegasus-2.12.0-empty_arrays.patch
Patch12:        pegasus-2.12.0-cimmofl-allow-experimental.patch
Patch13:        pegasus-2.12.0-schema-version-and-includes.patch
Patch14:        pegasus-2.13.0-enable-subscriptions-for-nonprivileged-users.patch
Patch15:        pegasus-2.13.0-gcc5-build.patch
Patch16:        pegasus-2.14.1-build-fixes.patch
Patch17:        pegasus-2.14.1-ssl-include.patch
Patch18:        pegasus-2.14.1-openssl-1.1-fix.patch
Patch19:        add-loongarch64-support.patch

BuildRequires:  procps libstdc++ pam-devel openssl openssl-devel
BuildRequires:  bash sed grep coreutils procps gcc gcc-c++ libstdc++
BuildRequires:  make pam-devel net-snmp-devel openslp-devel systemd-units
Requires:       net-snmp-libs openssl ca-certificates
Requires(pre):  %{_sbindir}/useradd %{_sbindir}/groupadd
Requires(post): /sbin/ldconfig /sbin/restorecon
Conflicts:      libcmpiCppImpl0

Provides:       cim-server = 1
Provides:       %{name}-libs = %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-libs < %{epoch}:%{version}-%{release}

%description
OpenPegasus WBEM Services for Linux enables management solutions that deliver
increased control of enterprise resources. WBEM is a platform and resource
independent DMTF standard that defines a common information model and
communication protocol for monitoring and controlling resources from diverse
sources.

%package        devel
Summary:        Header files for tog-pegasus
Requires:       %{name} >= %{version}-%{release} make

Provides:       %{name}-test = %{epoch}:%{version}-%{release}
Obsoletes:      %{name}-test < %{epoch}:%{version}-%{release}

%description devel
Header files for tog-pegasus

%package_help

%ifarch x86_64
%global PEGASUS_HARDWARE_PLATFORM LINUX_X86_64_GNU
%endif
%ifarch %{arm}
%global PEGASUS_HARDWARE_PLATFORM LINUX_XSCALE_GNU
%endif
%ifarch aarch64
%global PEGASUS_HARDWARE_PLATFORM LINUX_AARCH64_GNU
%endif
%ifarch loongarch64
%global PEGASUS_HARDWARE_PLATFORM LINUX_LOONGARCH64_GNU
%endif

%global PEGASUS_ARCH_LIB %{_lib}
%global OPENSSL_HOME %{_prefix}
%global OPENSSL_BIN %{_bindir}
%global PEGASUS_PEM_DIR %{_sysconfdir}/Pegasus
%global PEGASUS_SSL_CERT_FILE server.pem
%global PEGASUS_SSL_KEY_FILE file.pem
%global PEGASUS_SSL_TRUSTSTORE client.pem
%global PAM_CONFIG_DIR %{_sysconfdir}/pam.d
%global PEGASUS_CONFIG_DIR %{_sysconfdir}/Pegasus
%global PEGASUS_VARDATA_DIR /var/lib/Pegasus
%global PEGASUS_VARDATA_CACHE_DIR /var/lib/Pegasus/cache
%global PEGASUS_LOCAL_DOMAIN_SOCKET_PATH  /var/run/tog-pegasus/socket/cimxml.socket
%global PEGASUS_CIMSERVER_START_FILE /var/run/tog-pegasus/cimserver.pid
%global PEGASUS_TRACE_FILE_PATH /var/lib/Pegasus/cache/trace/cimserver.trc
%global PEGASUS_CIMSERVER_START_LOCK_FILE /var/run/tog-pegasus/cimserver_start.lock
%global PEGASUS_REPOSITORY_DIR /var/lib/Pegasus/repository
%global PEGASUS_PREV_REPOSITORY_DIR_NAME prev_repository
%global PEGASUS_REPOSITORY_PARENT_DIR /var/lib/Pegasus
%global PEGASUS_PREV_REPOSITORY_DIR /var/lib/PegasusXXX/prev_repository
%global PEGASUS_SBIN_DIR %{_sbindir}
%global PEGASUS_DOC_DIR %{_datadir}/doc/%{name}-%{version}
%global PEGASUS_RPM_ROOT $RPM_BUILD_DIR/%{srcname}
%global PEGASUS_RPM_HOME %PEGASUS_RPM_ROOT/build
%global PEGASUS_INSTALL_LOG /var/lib/Pegasus/log/install.log

%prep
%setup -q -n %{srcname}
export PEGASUS_ROOT=%PEGASUS_RPM_ROOT
yes | mak/CreateDmtfSchema 238 %{SOURCE4} cim_schema_2.38.0
%patch1 -p1 -b .no-rpath
%patch2 -p1 -b .PIE
%patch3 -p1 -b .redhat-config
%patch4 -p1 -b .cmpi-provider-lib
%patch5 -p1 -b .pam-wbem
%patch6 -p1 -b .snmp-tests
%patch7 -p1 -b .local-or-remote-auth
%patch8 -p1 -b .getpagesize
%patch9 -p1 -b .dont-strip
%patch10 -p1 -b .null_value
%patch11 -p1 -b .empty_arrays
%patch12 -p1 -b .cimmofl-allow-experimental
%patch13 -p1 -b .schema-version-and-includes
%patch14 -p1 -b .enable-subscriptions-for-nonprivileged-users
%patch15 -p1 -b .gcc5-build
%patch16 -p1 -b .build-fixes
%patch17 -p1 -b .ssl-include
%patch18 -p1 -b .openssl-1.1-fix
%patch19 -p1 -b .add-loongarch64-support

%build
cp -fp %SOURCE3 rpm

export PEGASUS_ROOT=%PEGASUS_RPM_ROOT
export PEGASUS_HOME=%PEGASUS_RPM_HOME
export PEGASUS_PLATFORM=%PEGASUS_HARDWARE_PLATFORM
export PEGASUS_ARCH_LIB=%PEGASUS_ARCH_LIB
export PEGASUS_ENVVAR_FILE=$PEGASUS_ROOT/env_var_Linux.status

export OPENSSL_HOME=%OPENSSL_HOME
export OPENSSL_BIN=%OPENSSL_BIN
export LD_LIBRARY_PATH=$PEGASUS_HOME/lib
export PATH=$PEGASUS_HOME/bin:$PATH

export PEGASUS_EXTRA_C_FLAGS="$RPM_OPT_FLAGS -fPIC -g -Wall -Wno-unused -fno-strict-aliasing"
export PEGASUS_EXTRA_CXX_FLAGS="$PEGASUS_EXTRA_C_FLAGS"
%if "%toolchain" == "clang"
	export PEGASUS_EXTRA_C_FLAGS="$PEGASUS_EXTRA_C_FLAGS -Wno-error=reserved-user-defined-literal"
	export PEGASUS_EXTRA_CXX_FLAGS="$PEGASUS_EXTRA_CXX_FLAGS -Wno-error=reserved-user-defined-literal"
%endif
export PEGASUS_EXTRA_LINK_FLAGS="$RPM_OPT_FLAGS"
export PEGASUS_EXTRA_PROGRAM_LINK_FLAGS="-g -pie -Wl,-z,relro,-z,now,-z,nodlopen,-z,noexecstack"
export SYS_INCLUDES=-I/usr/kerberos/include

%make_build -f ${PEGASUS_ROOT}/Makefile.Release create_ProductVersionFile
%make_build -f ${PEGASUS_ROOT}/Makefile.Release create_CommonProductDirectoriesInclude
%make_build -f ${PEGASUS_ROOT}/Makefile.Release create_ConfigProductDirectoriesInclude
%make_build -f ${PEGASUS_ROOT}/Makefile.Release all
%make_build -f ${PEGASUS_ROOT}/Makefile.Release repository


%install

export PEGASUS_ROOT=%PEGASUS_RPM_ROOT
export PEGASUS_HOME=%PEGASUS_RPM_HOME
export PEGASUS_PLATFORM=%PEGASUS_HARDWARE_PLATFORM
export PEGASUS_ARCH_LIB=%PEGASUS_ARCH_LIB
export PEGASUS_ENVVAR_FILE=$PEGASUS_ROOT/env_var_Linux.status
export OPENSSL_BIN=%OPENSSL_BIN
export LD_LIBRARY_PATH=$PEGASUS_HOME/lib
export PATH=$PEGASUS_HOME/bin:$PATH
export PEGASUS_STAGING_DIR=%{buildroot}

make -f $PEGASUS_ROOT/Makefile.Release stage \
    PEGASUS_STAGING_DIR=$PEGASUS_STAGING_DIR \
    PEGASUS_BUILD_TEST_RPM=%{PEGASUS_BUILD_TEST_RPM}

mkdir -p %{buildroot}/%{_tmpfilesdir}
install -p -D -m 644 %{SOURCE1} %{buildroot}/%{_tmpfilesdir}/tog-pegasus.conf
mkdir -p %{buildroot}%{_datadir}/Pegasus/scripts
install -p -m 755 %{SOURCE5} %{buildroot}%{_datadir}/Pegasus/scripts/generate-certs
rm -f %{buildroot}%{_sysconfdir}/Pegasus/ssl.cnf
mkdir -p %{buildroot}%{_sysconfdir}/Pegasus/crl

rm -f %{buildroot}%{_sysconfdir}/init.d/tog-pegasus
mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/tog-pegasus.service
mkdir -p %{buildroot}/%{_docdir}/%{name}
mv %{buildroot}%{_datadir}/doc/%{name}-%{major_ver}/* %{buildroot}/%{_docdir}/%{name}
rm -rf %{buildroot}%{_datadir}/doc/%{name}-%{major_ver}
pushd %{buildroot}%{_libdir}
ln -s libcmpiCppImpl.so.1 libcmpiCppImpl.so
ln -s libpeglistener.so.1 libpeglistener.so
popd
mkdir -p %{buildroot}/%{_libexecdir}/pegasus
mv %{buildroot}/%{_sbindir}/cimprovagt %{buildroot}/%{_libexecdir}/pegasus
install -m 644 src/Pegasus/Common/Platform_LINUX_XSCALE_GNU.h %{buildroot}/%{_includedir}/Pegasus/Common
mkdir -p %{buildroot}/%{_includedir}/Pegasus/Listener
install -m 644 src/Pegasus/Listener/Linkage.h %{buildroot}/%{_includedir}/Pegasus/Listener
install -m 644 src/Pegasus/Listener/CIMListener.h %{buildroot}/%{_includedir}/Pegasus/Listener
install -m 644 src/Pegasus/Client/CIMEnumerationContext.h %{buildroot}/%{_includedir}/Pegasus/Client
install -m 644 src/Pegasus/Common/UintArgs.h %{buildroot}/%{_includedir}/Pegasus/Common

install -p Schemas/CIM238/DMTF/Core/CIM_AbstractComponent.mof %{buildroot}%{_datadir}/Pegasus/samples/Providers/Load/CIM238/DMTF/Core/
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man1/

%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
cd %{buildroot}%{_datadir}/Pegasus/test
make prestarttests
rm %{buildroot}%{_datadir}/Pegasus/test/log.trace.0
rm %{buildroot}%{_datadir}/Pegasus/test/testtracer4.trace.0

%pre
if [ $1 -gt 1 ]; then
   if [ -d /var/lib/Pegasus/repository ]; then
        if [ -d /var/lib/Pegasus/prev_repository ]; then
           rm -rf /var/lib/Pegasus/prev_repository
        fi
        cp -r /var/lib/Pegasus/repository /var/lib/Pegasus/prev_repository
   fi
fi
:;

if [ $1 -eq 1 ]; then
    %{_sbindir}/groupadd -g %{pegasus_gid} -f -r pegasus >/dev/null 2>&1 || :;
    %{_sbindir}/useradd -u %{pegasus_uid} -r -N -M -g pegasus -s /sbin/nologin -d /var/lib/Pegasus \
    -c "tog-pegasus OpenPegasus WBEM/CIM services" pegasus >/dev/null 2>&1 || :;
fi
:;

%post
install -d -m 1750 -o root -g pegasus /var/run/tog-pegasus
restorecon /var/run/tog-pegasus
/sbin/ldconfig;
%systemd_post tog-pegasus.service
if [ $1 -ge 1 ]; then
   echo `date` >>  /var/lib/Pegasus/log/install.log 2>&1 || :;
   if [ $1 -gt 1 ]; then
      if [ -d /var/lib/Pegasus/prev_repository ]; then
         %{_sbindir}/repupgrade 2>> /var/lib/Pegasus/log/install.log || :;
      fi
      /bin/systemctl try-restart tog-pegasus.service >/dev/null 2>&1 || :;
   fi
fi
:;

if [ $1 -eq 1 ]; then
   ln -sf libpegclient.so.1 %{_prefix}/%PEGASUS_ARCH_LIB/libpegclient.so
   ln -sf libpegcommon.so.1 %{_prefix}/%PEGASUS_ARCH_LIB/libpegcommon.so
   ln -sf libpegprovider.so.1 %{_prefix}/%PEGASUS_ARCH_LIB/libpegprovider.so
   ln -sf libDefaultProviderManager.so.1 %{_prefix}/%PEGASUS_ARCH_LIB/libDefaultProviderManager.so
   ln -sf libCIMxmlIndicationHandler.so.1 %{_prefix}/%PEGASUS_ARCH_LIB/libCIMxmlIndicationHandler.so
   ln -sf libsnmpIndicationHandler.so.1 %{_prefix}/%PEGASUS_ARCH_LIB/libsnmpIndicationHandler.so

   ln -sf libComputerSystemProvider.so.1 %{_prefix}/%PEGASUS_ARCH_LIB/Pegasus/providers/libComputerSystemProvider.so
   ln -sf libOSProvider.so.1 %{_prefix}/%PEGASUS_ARCH_LIB/Pegasus/providers/libOSProvider.so
   ln -sf libProcessProvider.so.1 %{_prefix}/%PEGASUS_ARCH_LIB/Pegasus/providers/libProcessProvider.so
   ln -sf libCMPIProviderManager.so.1 %{_prefix}/%PEGASUS_ARCH_LIB/Pegasus/providerManagers/libCMPIProviderManager.so

   /bin/chgrp -h pegasus %{_libdir}/libpegclient.so
   /bin/chgrp -h pegasus %{_libdir}/libpegcommon.so
   /bin/chgrp -h pegasus %{_libdir}/libpegprovider.so
   /bin/chgrp -h pegasus %{_libdir}/libDefaultProviderManager.so
   /bin/chgrp -h pegasus %{_libdir}/libCIMxmlIndicationHandler.so
   /bin/chgrp -h pegasus %{_libdir}/libsnmpIndicationHandler.so
   /bin/chgrp -h pegasus %{_libdir}/Pegasus/providers/libComputerSystemProvider.so
   /bin/chgrp -h pegasus %{_libdir}/Pegasus/providers/libOSProvider.so
   /bin/chgrp -h pegasus %{_libdir}/Pegasus/providers/libProcessProvider.so
   /bin/chgrp -h pegasus %{_libdir}/Pegasus/providerManagers/libCMPIProviderManager.so
fi
:;
/sbin/ldconfig

%preun
%systemd_preun tog-pegasus.service
if [ $1 -eq 0 ]; then
   rm -rf /var/run/tog-pegasus
fi
:;

%postun
/sbin/ldconfig
%systemd_postun_with_restart tog-pegasus.service

%preun devel
if [ $1 -eq 0 ] ; then
   make --directory %{_datadir}/Pegasus/samples -s clean >/dev/null 2>&1 || :;
fi
:;

%files
%defattr(0644, root, pegasus, 0755)
%doc doc/Admin_Guide_Release.pdf doc/PegasusSSLGuidelines.htm doc/SecurityGuidelinesForDevelopers.html
%license doc/license.txt OpenPegasusNOTICE.txt
%defattr(0755, root, pegasus, 0755)
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/*
%{_libexecdir}/pegasus/
%defattr(0640, root, pegasus, 0750)
%verify(not md5 size mtime mode group) /var/lib/Pegasus/repository
%defattr(0644, root, pegasus, 0755)
%dir %{_datadir}/Pegasus
%{_datadir}/Pegasus/mof
%defattr(0755, root, pegasus, 0750)
%{_datadir}/Pegasus/scripts
%defattr(0640, root, pegasus, 0750)
%dir /var/lib/Pegasus
/var/lib/Pegasus/cache
%dir /var/lib/Pegasus/log
%dir %{_sysconfdir}/Pegasus
%{_tmpfilesdir}/tog-pegasus.conf
%defattr(0640, root, pegasus, 1750)
%ghost /var/run/tog-pegasus
%ghost %attr(0600, root, root) /var/run/tog-pegasus/cimserver.pid
%ghost %attr(0600, root, root) /var/run/tog-pegasus/cimserver_start.lock
%ghost %attr(0777 ,root, root) /var/run/tog-pegasus/cimxml.socket
%attr(0644, root, pegasus) %{_unitdir}/tog-pegasus.service
%defattr(0640, root, pegasus, 0750)
%ghost %attr(0644, root, root) %config(noreplace) %{_sysconfdir}/Pegasus/cimserver_current.conf
%ghost %attr(0644, root, root) %config(noreplace) %{_sysconfdir}/Pegasus/cimserver_planned.conf
%config(noreplace) %{_sysconfdir}/Pegasus/access.conf
%config(noreplace) %{_sysconfdir}/pam.d/wbem
%defattr(0444, root, root)
%ghost %{_sysconfdir}/Pegasus/client.pem
%ghost %{_sysconfdir}/Pegasus/server.pem
%defattr(0400, root, root)
%ghost %{_sysconfdir}/Pegasus/file.pem
%defattr(0644, root, root)
%ghost %{_sysconfdir}/Pegasus/ca.crt
%ghost %{_sysconfdir}/Pegasus/ca.srl
%ghost %{_sysconfdir}/Pegasus/client.srl
%defattr(0400, root, root)
%ghost %{_sysconfdir}/Pegasus/ssl-ca.cnf
%ghost %{_sysconfdir}/Pegasus/ssl-service.cnf
%defattr(0644, root, root)
%ghost %{_sysconfdir}/ca-trust/source/anchors/localhost-pegasus.pem
%ghost %attr(0640, root, pegasus) %{_sysconfdir}/Pegasus/cimserver_trust
%ghost %attr(0640, root, pegasus) %{_sysconfdir}/Pegasus/indication_trust
%dir %attr(0640, root, pegasus) %{_sysconfdir}/Pegasus/crl
%ghost %attr(0644, root, root) %verify(not md5 size mtime) /var/lib/Pegasus/log/install.log
%ghost %attr(0640, root, pegasus) %verify(not md5 size mtime) /var/lib/Pegasus/cache/trace/cimserver.trc
%exclude %{_prefix}/lib/debug
%exclude %{_pkgdocdir}/OpenPegasusNOTICE.txt
%exclude %{_pkgdocdir}/license.txt

%files devel
%defattr(0644,root,pegasus,0755)
%{_includedir}/Pegasus
%{_datadir}/Pegasus/html
%{_datadir}/Pegasus/samples
%defattr(0750,root,pegasus,0755)
%{_datadir}/Pegasus/test/bin
%{_datadir}/Pegasus/test/%PEGASUS_ARCH_LIB
%defattr(0644,root,pegasus,0755)
%dir %{_datadir}/Pegasus/test
%{_datadir}/Pegasus/test/mak
%{_datadir}/Pegasus/test/Makefile
%dir %{_datadir}/Pegasus/test/tmp
%ghost %{_datadir}/Pegasus/test/tmp/procIdFile
%ghost %{_datadir}/Pegasus/test/tmp/trapLogFile
%ghost %{_datadir}/Pegasus/test/tmp/IndicationStressTestLog
%ghost %{_datadir}/Pegasus/test/tmp/oldIndicationStressTestLog
%verify(not md5 size mtime) /var/lib/Pegasus/testrepository

%files help
%defattr(0644, root, root, 0755)
%doc src/Clients/repupgrade/doc/repupgrade.html
%{_mandir}/man8/*
%{_mandir}/man1/*

%changelog
* Thu May 25 2023 yoo <sunyuechi@iscas.ac.cn> - %{major_ver}.1-53
- fix clang build error

* Thu Dec  8 2022 huajingyun <huajingyun@loongson.cn> - 2:2.14.1-52
-  Add loongarch64 support

* Tue Aug 31 2021 caodongxia <caodongxia@huawei.com> - 2:2.14.1-51
- Fix help package install warning 

* Thu May 28 2020 Guoshuai Sun <sunguoshuai@huawei.com> - 2:2.14.1-49
- Modify spec for unreasonable disable stop.service when removing pack.

* Sat Feb 29 2020 Senlin Xia <xiasenlin1@huawei.com> - 2:2.14.1-48
- Package init
