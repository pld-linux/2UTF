Summary:	Translates char-sets and decodes MIME.
Name:		2UTF
Version:	1.10
Release:	1
Copyright:	BSD
Group:		Utilities/Text
Group(pl):	Narzêdzia/Tekst
Source:		ftp://sunsite.unc.edu/pub/Linux/utils/text/%{name}-%{version}.tar.gz
Patch:		2UTF-install.patch
URL:		http://www.angelfire.com/me/rch/ll.html#2UTF
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Filter for char-set translation to and from Unicode.
Gets char-set definitions from WG15 locales char-maps or similiar tables.
Can decode nested multi-part MIME messages and invoke external filters.
Can display char-maps and current console font.  

%prep
%setup -q
%patch -p0

%build
make config
make GZIPDOCS=no \
	PREFIX=%{_prefix} \
	sysconfdir=/etc \
	docsdir=%{_docdir}/%{name}-%{version} \
	var_prefix=/var \
	ALIASES=/var/state/2UTF.aliases \
	charmaps_localdatadir=%{_datadir}/i18n/charmaps \
	man1dir=%{_mandir}/man1 \
	OPT="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make GZIPDOCS=no \
	PREFIX=$RPM_BUILD_ROOT/%{_prefix} \
	sysconfdir=$RPM_BUILD_ROOT/etc \
	var_prefix=$RPM_BUILD_ROOT/var \
	ALIASES=$RPM_BUILD_ROOT/var/state/2UTF.aliases \
	docsdir=$RPM_BUILD_ROOT/%{_docdir}/%{name}-%{version} \
	charmaps_localdatadir=$RPM_BUILD_ROOT/%{_datadir}/i18n/charmaps \
	TERMINFO=$RPM_BUILD_ROOT/%{_datadir}/terminfo \
	man1dir=$RPM_BUILD_ROOT/%{_mandir}/man1 \
	tmpdir_install=yes \
	owner=`id -ur` \
	group=`id -gr` \
	install

rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/{fromUTF.1,toUTF.1}
echo ".so 2UTF.1" > $RPM_BUILD_ROOT/%{_mandir}/man1/toUTF.1
echo ".so 2UTF.1" > $RPM_BUILD_ROOT/%{_mandir}/man1/fromUTF.1

ln -sf 2UTF $RPM_BUILD_ROOT%{_bindir}/toUTF

gzip -9nf $RPM_BUILD_ROOT/%{_mandir}/man1/* examples/* \
	BSD_style_license TODO changelog copyright || :

%post
%{_bindir}/2UTF --create-aliases

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {BSD_style_license,TODO,changelog,copyright}.gz examples
%config /etc/2UTF.config
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/terminfo/l/*
