Summary: Translates char-sets and decodes MIME.
Name: 2UTF
Version: 1.10
Release: 0
Copyright: BSD style
URL: http://www.angelfire.com/me/rch/ll.html#2UTF
BuildRoot: /tmp/2UTF-root
Group: Utilities/Text
Source: sunsite.unc.edu:/pub/Linux/utils/text/2UTF-1.10.tar.gz
%description
 Filter for char-set translation to and from Unicode.
 Gets char-set definitions from WG15 locales char-maps or similiar tables.
 Can decode nested multi-part MIME messages and invoke external filters.
 Can display char-maps and current console font.  

%prep
%setup
[ $RPM_BUILD_ROOT != / ] && rm -R -f $RPM_BUILD_ROOT

%build
make config
make GZIPDOCS=yes prefix=/usr sysconfdir=/etc docsdir=/usr/doc/2UTF \
		var_prefix=/var OPT="$RPM_OPT_FLAGS"

%install
make GZIPDOCS=yes prefix=$RPM_BUILD_ROOT/usr sysconfdir=$RPM_BUILD_ROOT/etc \
	var_prefix=$RPM_BUILD_ROOT/var \
	docsdir=$RPM_BUILD_ROOT/usr/doc/2UTF \
	tmpdir_install=yes install
chown -R root.root	$RPM_BUILD_ROOT/
chmod -R g-ws		$RPM_BUILD_ROOT/
find $RPM_BUILD_ROOT -type f -or -type l \
	|sed -e 's!^'"$RPM_BUILD_ROOT"'!!; s!/etc!%config &!' >filelist

%files
%files -f filelist
%dir /usr/doc/2UTF
%dir /usr/doc/2UTF/examples

%post
set -o errexit
test -e /usr/local/share/i18n/charmaps \
    || install -c -d -o root -g staff -m 2775	/usr/local/share/i18n/charmaps
/usr/bin/2UTF --create-aliases
