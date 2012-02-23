Name:           basex
Summary:        XML database and XPath/XQuery processor
Version:        7.1.1
Release:        1
License:        BSD
Group:          Productivity/Database
URL:            http://basex.org
Source0:        basex-%{version}.tar
Source1:        https://raw.github.com/BaseXdb/basex-dist/master/linux/debian/man/basex.1
Source2:        https://raw.github.com/BaseXdb/basex-dist/master/linux/debian/man/basexclient.1
Source3:        https://raw.github.com/BaseXdb/basex-dist/master/linux/debian/man/basexserver.1
Source4:        https://raw.github.com/BaseXdb/basex-dist/master/linux/debian/man/basexgui.1
Source5:        https://github.com/BaseXdb/basex-dist/raw/master/images/BaseX_16px.png
Source6:        https://github.com/BaseXdb/basex-dist/raw/master/images/BaseX_32px.png
Source7:        https://github.com/BaseXdb/basex-dist/raw/master/images/BaseX_48px.png
Source8:        https://github.com/BaseXdb/basex-dist/raw/master/images/BaseX_64px.png
Source9:        https://github.com/BaseXdb/basex-dist/raw/master/images/BaseX_128px.png
Source10:       https://github.com/BaseXdb/basex-dist/raw/master/images/BaseX_256px.png
Source11:       https://github.com/BaseXdb/basex-dist/raw/master/images/BaseX_512px.png
Source12:       https://raw.github.com/BaseXdb/basex-dist/master/images/BaseX.svg
Source13:       https://raw.github.com/BaseXdb/basex-dist/master/linux/basex.desktop
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  java-devel >= 1.6
BuildRequires:  ant
BuildRequires:  desktop-file-utils
BuildArch:      noarch
Requires:       java >= 1.6


%description
BaseX is a very fast and light-weight, yet powerful XML database and
XPath/XQuery processor, including support for the latest W3C Full Text and
Update Recommendations. It supports large XML instances and offers a highly
interactive front-end (basexgui). Apart from two local standalone modes, BaseX
offers a client/server architecture.

%package javadoc
License:        BSD
PreReq:         coreutils
Summary:        XML database and XPath/XQuery processor
Group:          Productivity/Database
 
%description javadoc
Javadoc for BaseX.

%prep

%build
# mvn package -DskipTests=true
%ant -Dname="%{name}" -Dversion="%{version}"
%ant javadoc

%install
# jars
%{__install} -d -m 0755 %{buildroot}%{_javadir}
%{__install} -m 0644 target/%{name}-%{version}.jar %{buildroot}%{_javadir}

# lib
# TODO: add igo
# %{__cp} -rp lib "%{buildroot}%{_datadir}/%{name}/"

# javadoc
%{__install} -d -m 0755 %{buildroot}%{_javadocdir}
%__mkdir_p %{buildroot}%{_javadocdir}/%{name}-%{version}
%__cp -a target/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%__ln_s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# manpages
%{__install} -d -m 0755 %{buildroot}%{_mandir}/man1/
%{__install} -D -m 644 %{SOURCE1} %{buildroot}%{_mandir}/man1/basex.1
%{__install} -D -m 644 %{SOURCE2} %{buildroot}%{_mandir}/man1/basexclient.1
%{__install} -D -m 644 %{SOURCE3} %{buildroot}%{_mandir}/man1/basexserver.1
%{__install} -D -m 644 %{SOURCE4} %{buildroot}%{_mandir}/man1/basexgui.1

# icons
%{__install} -D -m 644 %{SOURCE5} %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{__install} -D -m 644 %{SOURCE6} %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{__install} -D -m 644 %{SOURCE7} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{__install} -D -m 644 %{SOURCE8} %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{__install} -D -m 644 %{SOURCE9} %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{__install} -D -m 644 %{SOURCE10} %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
%{__install} -D -m 644 %{SOURCE11} %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png
%{__install} -D -m 644 %{SOURCE12} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# desktop file
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications %{Source13}

# start scripts
%{__install} -d -m 0755 %{buildroot}%{_bindir}

%__cat > %{buildroot}%{_bindir}/basex << EOF
#!/bin/sh
. %{_datadir}/java-utils/java-functions
MAIN_CLASS=org.basex.BaseX
BASE_FLAGS="-mx512m"
BASE_JARS="tagsoup xml-commons-resolver lucene-contrib/analyzers lucene-contrib/snowball %{name}-%{version}"
# TODO: add igo
set_jvm
set_classpath \$BASE_JARS
set_flags \$BASE_FLAGS
run "\$@"
EOF

%__cat > %{buildroot}%{_bindir}/basexgui << EOF
#!/bin/sh
. %{_datadir}/java-utils/java-functions
MAIN_CLASS=org.basex.BaseXGUI
BASE_FLAGS="-mx512m"
BASE_JARS="tagsoup xml-commons-resolver lucene-contrib/analyzers lucene-contrib/snowball %{name}-%{version}"
# TODO: add igo
set_jvm
set_classpath \$BASE_JARS
set_flags \$BASE_FLAGS
run "\$@"
EOF

%__cat > %{buildroot}%{_bindir}/basexserver << EOF
#!/bin/sh
. %{_datadir}/java-utils/java-functions
MAIN_CLASS=org.basex.BaseXServer
BASE_FLAGS="-mx512m"
BASE_JARS="tagsoup xml-commons-resolver lucene-contrib/analyzers lucene-contrib/snowball %{name}-%{version}"
# TODO: add igo
set_jvm
set_classpath \$BASE_JARS
set_flags \$BASE_FLAGS
run "\$@"
EOF

%__cat > %{buildroot}%{_bindir}/xquery << EOF
#!/bin/sh
. %{_datadir}/java-utils/java-functions
MAIN_CLASS=org.basex.BaseX
BASE_FLAGS="-mx512m"
BASE_JARS="tagsoup xml-commons-resolver lucene-contrib/analyzers lucene-contrib/snowball %{name}-%{version}"
# TODO: add igo
set_jvm
set_classpath \$BASE_JARS
set_flags \$BASE_FLAGS
run -q "\$@"
EOF

%__cat > %{buildroot}%{_bindir}/basexclient << EOF
#!/bin/sh
. %{_datadir}/java-utils/java-functions
MAIN_CLASS=org.basex.BaseXClient
BASE_JARS="%{name}-%{version}"
set_jvm
set_classpath \$BASE_JARS
run "\$@"
EOF

%__cat > %{buildroot}%{_bindir}/basexserverstop << EOF
#!/bin/sh
. %{_datadir}/java-utils/java-functions
MAIN_CLASS=org.basex.BaseXServer
BASE_JARS="%{name}-%{version}"
set_jvm
set_classpath \$BASE_JARS
run "\$@" stop
EOF

%files
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/basex
%attr(0755,root,root) %{_bindir}/basexclient
%attr(0755,root,root) %{_bindir}/basexgui
%attr(0755,root,root) %{_bindir}/basexserver
%attr(0755,root,root) %{_bindir}/basexserverstop
%attr(0755,root,root) %{_bindir}/xquery

%{_javadir}/%{name}-%{version}.jar

%{_mandir}/man1/basex.1*
%{_mandir}/man1/basexclient.1*
%{_mandir}/man1/basexserver.1*
%{_mandir}/man1/basexgui.1*

%{_datadir}/icons/hicolor

%{_datadir}/applications/%{name}.desktop

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%changelog
