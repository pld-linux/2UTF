Summary:	Translates char-sets and decodes MIME.
Summary(pl):	Translator tablic znaków oraz dekoder MIME.
Name:		2UTF
Version:	1.11
Release:	2
License:	BSD
Group:		Utilities/Text
Group(fr):	Utilitaires/Texte
Group(pl):	Narzêdzia/Tekst
Source:		ftp://sunsite.unc.edu/pub/Linux/utils/text/%{name}-%{version}.tar.gz
Patch:		2UTF-install.patch
URL:		http://www.angelfire.com/me/rch/ll.html#2UTF
BuildRoot:	/tmp/%{name}-%{version}-root

%define		_sysconfdir	/etc

%description
Filter for char-set translation to and from Unicode. Gets char-set
definitions from WG15 locales char-maps or similiar tables. Can decode
nested multi-part MIME messages and invoke external filters. Can display
char-maps and current console font.

%description -l pl
Translator tablic znaków do i z Unikodu. Pobiera definicje tablic znaków z
lokalnych WG15 tablic znaków lub podobnych. Mo¿e zdekodowaæ wiadomo¶ci
wieloczê¶ciowe MIME i uruchamiaæ zewnêtrzne filtry. Mo¿e wy¶wietlaæ tablice
znaków i aktualny font konsolowy.

%prep
%setup -q
chmod -R u+w .
%patch -p0

%build
make config
make GZIPDOCS=no \
	PREFIX=%{_prefix} \
	sysconfdir=%{_sysconfdir} \
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
	sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir} \
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
%config %{_sysconfdir}/2UTF.config
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/terminfo/l/*
