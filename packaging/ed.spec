#specfile originally created for Fedora, modified for Moblin Linux
Summary: The GNU line editor
Name: ed
Version: 1.4
Release: 1
License: GPLv3+
Group:  Applications/Text
Source: ftp://ftp.gnu.org/gnu/ed/%{name}-%{version}.tar.gz
URL:    http://www.gnu.org/software/ed/
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Ed is a line-oriented text editor, used to create, display, and modify
text files (both interactively and via shell scripts).  For most
purposes, ed has been replaced in normal usage by full-screen editors
(emacs and vi, for example).

Ed was the original UNIX editor, and may be used by some programs.  In
general, however, you probably don't need to install it and you probably
won't use it.

%prep
%setup -q
rm -f stamp-h.in

%build
%configure --exec-prefix=/
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
make install DESTDIR=$RPM_BUILD_ROOT \
    bindir=/bin mandir=%{_mandir}/man1

rm -f $RPM_BUILD_ROOT%{_infodir}/dir*
gzip -9qnf  $RPM_BUILD_ROOT%{_infodir}/*
install -p -m0644 doc/ed.1 $RPM_BUILD_ROOT%{_mandir}/man1

%post
[ -e %{_infodir}/ed.info.gz ] && /sbin/install-info %{_infodir}/ed.info.gz %{_infodir}/dir --entry="* ed: (ed).                  The GNU Line Editor." || :

%preun
if [ $1 = 0 ] ; then
  [ -e %{_infodir}/ed.info.gz ] && /sbin/install-info --delete %{_infodir}/ed.info.gz %{_infodir}/dir --entry="* ed: (ed).                  The GNU Line Editor." || :
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ChangeLog NEWS README TODO AUTHORS COPYING
/bin/*
%doc %{_infodir}/ed.info.gz
%doc %{_mandir}/*/*
