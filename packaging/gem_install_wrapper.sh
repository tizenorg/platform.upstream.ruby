#! /bin/sh

set -e 
/usr/bin/gem1.9 install --verbose --local --build-root=$RPM_BUILD_ROOT "$@"
if test -d $RPM_BUILD_ROOT/usr/bin; then
  cd $RPM_BUILD_ROOT/usr/bin 
  bins=`ls -1 *1.9 2> /dev/null`
  if test -n "$bins"; then
    for bin in $bins; do 
      mv -v $bin $(echo "$bin" | sed -e 's,1.9$,,')
    done
  fi
fi

