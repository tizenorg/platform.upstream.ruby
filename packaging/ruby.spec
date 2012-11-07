Name:           ruby
Version:        1.9.3.p194
Release:        0
#
%define pkg_version 1.9.3
%define patch_level p194
# keep in sync with macro file!
%define rb_binary_suffix 1.9
%define rb_ver  1.9.1
%define rb_arch %(echo %{_target_cpu}-linux | sed -e "s/ppc/powerpc/")
%define rb_libdir                         %{_libdir}/ruby/%{rb_ver}/
%define rb_archdir                        %{_libdir}/ruby/%{rb_ver}/%{rb_arch}
# keep in sync with macro file!
#
# from valgrind.spec
%ifarch %ix86 x86_64 ppc ppc64
%define use_valgrind 1
%endif
%define run_tests 0
#
#
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  gdbm-devel
BuildRequires:  libffi-devel
BuildRequires:  libyaml-devel
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  pkg-config
BuildRequires:  readline-devel
BuildRequires:  zlib-devel
BuildRequires:  ca-certificates
#BuildRequires:  ca-certificates-cacert
#
Provides:       rubygem-rake = 0.9.2.2
Provides:       ruby(abi) = %{rb_ver}
#
Url:            http://www.ruby-lang.org/
Source:         ftp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-%{pkg_version}-%{patch_level}.tar.bz2
Source6:        ruby.macros
Source7:        gem_install_wrapper.sh
#
Summary:        An Interpreted Object-Oriented Scripting Language
License:        BSD-2-Clause or Ruby
Group:          Development/Languages/Ruby

%description
Ruby is an interpreted scripting language for quick and easy
object-oriented programming.  It has many features for processing text
files and performing system management tasks (as in Perl).  It is
simple, straight-forward, and extensible.

* Ruby features:

- Simple Syntax

- *Normal* Object-Oriented features (class, method calls, for
   example)

- *Advanced* Object-Oriented features(Mix-in, Singleton-method, for
   example)

- Operator Overloading

- Exception Handling

- Iterators and Closures

- Garbage Collection

- Dynamic Loading of Object Files (on some architectures)

- Highly Portable (works on many UNIX machines; DOS, Windows, Mac,
BeOS, and more)


%package devel
Summary:        Development files to link against Ruby
Group:          Development/Languages/Ruby
Requires:       %{name} = %{version}
Provides:       rubygems19 = 1.3.7
Provides:       rubygems19_with_buildroot_patch
Requires:       ruby-common

%description devel
Development files to link against Ruby.


%package doc-ri
Summary:        Ruby Interactive Documentation
Group:          Development/Languages/Ruby
Requires:       %{name} = %{version}
BuildArch:      noarch
%description doc-ri
This package contains the RI docs for ruby

%package doc-html
Summary:        This package contains the HTML docs for ruby
Group:          Development/Languages/Ruby
Requires:       %{name} = %{version}
BuildArch:      noarch
%description doc-html
This package contains the HTML docs for ruby

%package examples
Summary:        Example scripts for ruby
Group:          Development/Languages/Ruby
Requires:       %{name} = %{version}
BuildArch:      noarch
%description examples
Example scripts for ruby

%package test-suite
Requires:       %{name} = %{version}
Summary:        An Interpreted Object-Oriented Scripting Language
Group:          Development/Languages/Ruby
BuildArch:      noarch
%description test-suite
Ruby is an interpreted scripting language for quick and easy
object-oriented programming.  It has many features for processing text
files and performing system management tasks (as in Perl).  It is
simple, straight-forward, and extensible.

* Ruby features:

- Simple Syntax

- *Normal* Object-Oriented features (class, method calls, for
   example)

- *Advanced* Object-Oriented features(Mix-in, Singleton-method, for
   example)

- Operator Overloading

- Exception Handling

- Iterators and Closures

- Garbage Collection

- Dynamic Loading of Object Files (on some architectures)

- Highly Portable (works on many UNIX machines; DOS, Windows, Mac,
BeOS, and more)

%prep
%setup -q -n ruby-%{pkg_version}-%{patch_level}

%if 0%{?needs_optimization_zero}
touch -r configure configure.timestamp
perl -p -i.bak -e 's|-O2|-O0|g' configure
diff -urN configure{.bak,} ||:
touch -r configure.timestamp configure
%endif
find sample -type f -print0 | xargs -r0 chmod a-x
grep -Erl '^#! */' benchmark bootstraptest ext lib sample test \
  | xargs -r perl -p -i -e 's|^#!\s*\S+(\s+.*)?$|#!/usr/bin/ruby1.9$1|'

%build
%if 0%{?needs_optimization_zero}
export CFLAGS="%{optflags}"
export CFLAGS="${CFLAGS//-O2/}"
export CXXFLAGS="$CFLAGS"
export FFLAGS="$CFLAGS"
%endif
%configure \
  --target=%{_target_platform} \
  --with-mantype=man \
  --enable-shared \
  --disable-static \
  --disable-rpath
%{__make} all V=1

%install
%make_install V=1
%{__install} -D -m 0644 %{S:6} %{buildroot}/etc/rpm/macros.ruby19
%{__install} -D -m 0755 %{S:7} %{buildroot}/usr/lib/rpm/gem_install_wrapper.sh

%if 0%{?run_tests}
%check
export LD_LIBRARY_PATH="$PWD"
# we know some tests will fail when they do not find a /usr/bin/ruby
make check V=1 ||:
%endif

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/rpm/macros.ruby19
%{_bindir}/erb
%{_bindir}/gem
%{_bindir}/irb
%{_bindir}/rake
%{_bindir}/rdoc
%{_bindir}/ri
%{_bindir}/ruby
%{_bindir}/testrb
%{_libdir}/libruby.so.1.9*
%{_libdir}/ruby/
/usr/lib/rpm/gem_install_wrapper.sh
%{_mandir}/man1/ri.1*
%{_mandir}/man1/irb.1*
%{_mandir}/man1/erb.1*
%{_mandir}/man1/rake.1*
%{_mandir}/man1/ruby.1*
%doc COPYING  COPYING.ja  GPL

%files devel
%defattr(-,root,root,-)
%{_includedir}/ruby-%{rb_ver}
%{_libdir}/libruby.so
%{_libdir}/pkgconfig/ruby-1.9.pc


%files doc-ri
%defattr(-,root,root,-)
%dir %{_datadir}/ri/
%{_datadir}/ri/%{rb_ver}/

%changelog
