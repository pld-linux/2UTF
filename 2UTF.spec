Summary:	Translates char-sets and decodes MIME
Summary(pl):	Translator tablic znaków oraz dekoder MIME
Name:		2UTF
Version:	1.22
Release:	8
License:	BSD
Group:		Applications/Text
Source0:	ftp://sunsite.unc.edu/pub/Linux/utils/text/%{name}-%{version}.tar.gz
# Source0-md5:	883da4c858570d9d434d23e702304a5a
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-known_charsets_no_tcs.patch
URL:		http://x-lt.richard.eu.org/me/rch/ll.html
#URL:		http://www.angelfire.com/me/rch/ll.html#2UTF
Requires:	localedb-src
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc
%define		aliasdir	/var/lib/misc

%description
Filter for char-set translation to and from Unicode. Gets char-set
definitions from WG15 locales char-maps or similiar tables. Can decode
nested multi-part MIME messages and invoke external filters. Can
display char-maps and current console font.

%description -l pl
Translator tablic znaków do i z Unikodu. Pobiera definicje tablic
znaków z lokalnych WG15 tablic znaków lub podobnych. Mo¿e zdekodowaæ
wiadomo¶ci wieloczê¶ciowe MIME i uruchamiaæ zewnêtrzne filtry. Mo¿e
wy¶wietlaæ tablice znaków i aktualny font konsolowy.

%prep
%setup -q
%patch0 -p0
%patch1 -p1

%build
CCFLAGS="%{rpmcflags} -L/usr/lib/gconv"; export CCFLAGS
%{__make} config ICONV_DIR=%{_prefix}
LDFLAGS="%{rpmcflags} -L/usr/lib/gconv"; export LDFLAGS
%{__make} \
	GZIPDOCS=no \
	PREFIX=%{_prefix} \
	sysconfdir=%{_sysconfdir} \
	docsdir=%{_docdir}/%{name}-%{version} \
	var_prefix=/var \
	ALIASES=%{aliasdir}/2UTF.aliases \
	charmaps_localdatadir=%{_datadir}/i18n/charmaps \
	man1dir=%{_mandir}/man1 \
	OPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/i18n/charmaps
%{__make} GZIPDOCS=no \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir} \
	var_prefix=$RPM_BUILD_ROOT/var \
	ALIASES=$RPM_BUILD_ROOT%{aliasdir}/2UTF.aliases \
	docsdir=$RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} \
	charmaps_localdatadir=$RPM_BUILD_ROOT%{_datadir}/i18n/charmaps \
	TERMINFO=$RPM_BUILD_ROOT%{_datadir}/terminfo \
	man1dir=$RPM_BUILD_ROOT%{_mandir}/man1 \
	tmpdir_install=yes \
	owner=`id -ur` \
	group=`id -gr` \
	install

rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{fromUTF.1,toUTF.1}
echo ".so 2UTF.1" > $RPM_BUILD_ROOT%{_mandir}/man1/toUTF.1
echo ".so 2UTF.1" > $RPM_BUILD_ROOT%{_mandir}/man1/fromUTF.1

ln -sf 2UTF $RPM_BUILD_ROOT%{_bindir}/toUTF

%post
if [ -f /var/lib/2UTF.aliases ]; then
	mv -f /var/lib/2UTF.aliases %{aliasdir}/2UTF.aliases
fi
%{_bindir}/2UTF --create-aliases

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc examples/* BSD_style_license TODO changelog copyright
%config %{_sysconfdir}/2UTF.config
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/terminfo/l/*
%attr(644,root,root) %ghost %{aliasdir}/2UTF.aliases
