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
License:        BSD-2-Clause or Ruby
#
Summary:        An Interpreted Object-Oriented Scripting Language
#
Url:            http://www.ruby-lang.org/
Group:          Development/Languages/Ruby
Source:         ftp://ftp.ruby-lang.org/pub/ruby/1.9/ruby-%{pkg_version}-%{patch_level}.tar.bz2
Source6:        ruby19.macros
Source7:        gem_install_wrapper.sh
Patch0:         rubygems-1.5.0_buildroot.patch
Patch1:         ruby-1.9.2p290_tcl_no_stupid_rpaths.patch
Patch2:         ruby19-export_init_prelude.patch
BuildRequires:  ca-certificates
BuildRequires:  gdbm-devel
BuildRequires:  libffi-devel
BuildRequires:  libyaml-devel
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  pkg-config
BuildRequires:  readline-devel
BuildRequires:  zlib-devel
#BuildRequires:  ca-certificates-cacert
#
Provides:       rubygem-rake = 0.9.2.2
Provides:       ruby(abi) = %{rb_ver}
%define run_tests 0
#
#
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

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
Requires:       ruby-common
Provides:       rubygems19 = 1.3.7
Provides:       rubygems19_with_buildroot_patch

%description devel
Development files to link against Ruby.

%package doc-ri
Summary:        Ruby Interactive Documentation
Group:          Development/Languages/Ruby
Requires:       %{name} = %{version}
%if 0%{?suse_version} >= 1120
BuildArch:      noarch
%endif
%description doc-ri
This package contains the RI docs for ruby

%package doc-html
Summary:        This package contains the HTML docs for ruby
Group:          Development/Languages/Ruby
Requires:       %{name} = %{version}
%if 0%{?suse_version} >= 1120
BuildArch:      noarch
%endif
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
Summary:        An Interpreted Object-Oriented Scripting Language
Group:          Development/Languages/Ruby
Requires:       %{name} = %{version}
%if 0%{?suse_version} >= 1120
BuildArch:      noarch
%endif
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
%patch0
%patch1
%patch2 -p1
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
make all V=1

%install
%make_install V=1
install -D -m 0644 %{SOURCE6} %{buildroot}%{_sysconfdir}/rpm/macros.ruby19
install -D -m 0755 %{SOURCE7} %{buildroot}/usr/lib/rpm/gem_install_wrapper.sh

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
%config(noreplace) %{_sysconfdir}/rpm/macros.ruby19
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
%{_libdir}/rpm/gem_install_wrapper.sh
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
