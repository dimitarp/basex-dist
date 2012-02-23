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
BuildArch:      noarch
Requires:       java >= 1.6

%if 0%{?suse_version} > 1000
Suggests:       xml-commons-resolver = 1.2, tagsoup, lucene-contrib
%endif



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
%setup -q
%__cat > build.xml << EOF
<?xml version="1.0" encoding="UTF-8"?>
<project name="%{name}" default="package" basedir=".">
  <property name="name" value="%{name}"/>
  <property name="version" value="%{version}"/>
  <property name="sources" value = "src/main/java"/>
  <property name="resources" value = "src/main/resources"/>
  <property name="output" value = "target"/>
  <property name="classes" value="\${output}/classes"/>
  <target name="clean">
    <delete dir="\${output}"/>
  </target>
  <target name="compile">
    <mkdir dir="\${classes}"/>
    <javac destdir="\${classes}"
           optimize="true"
           target="1.6"
           verbose="false"
           fork="false"
           source="1.6">
      <src>
        <pathelement location="\${sources}"/>
      </src>
    </javac>
    <copy todir="\${classes}">
      <fileset dir="\${resources}"/>
    </copy>
  </target>
 <target name="javadoc">
    <javadoc sourcepath="\${sources}"
             packagenames="*"
             destdir="\${output}/apidocs"
             access="protected"
             old="false"
             verbose="false"
             version="true"
             use="true"
             author="true"
             splitindex="false"
             nodeprecated="false"
             nodeprecatedlist="false"
             notree="false"
             noindex="false"
             nohelp="false"
             nonavbar="false"
             serialwarn="false"
             charset="UTF-8"
             linksource="false"
             breakiterator="false"/>
  </target>
  <target name="package" depends="compile">
    <jar jarfile="\${output}/\${name}-\${version}.jar"
         compress="true"
         index="false"
         basedir="\${classes}"
         excludes="**/package.html">
        <manifest>
          <attribute name="Main-Class" value="org.basex.BaseXGUI"/>
        </manifest>
    </jar>
  </target>
</project>
EOF

%build
# mvn package -DskipTests=true
%ant
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
%{__install} -D -m 644 %{SOURCE13} %{buildroot}%{_datadir}/applications/%{name}.desktop

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

%clean
%{__rm} -rf %{buildroot}

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