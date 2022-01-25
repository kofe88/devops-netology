# Домашнее задание к занятию "3.3. Операционные системы, лекция 1"

#### 1. Какой системный вызов делает команда `cd`? В прошлом ДЗ мы выяснили, что `cd` не является самостоятельной  программой, это `shell builtin`, поэтому запустить `strace` непосредственно на `cd` не получится. Тем не менее, вы можете запустить `strace` на `/bin/bash -c 'cd /tmp'`. В этом случае вы увидите полный список системных вызовов, которые делает сам `bash` при старте. Вам нужно найти тот единственный, который относится именно к `cd`. Обратите внимание, что `strace` выдаёт результат своей работы в поток stderr, а не в stdout.

Т.к. `strace` выдаёт результат в `stderr`, перенаправим его в `stdout` и в нем уже будем искать нужный системный вызов, для этого используем конструкцию `strace /bin/bash -c 'cd /tmp' 2>&1 | grep /tmp` :

```bash
21:39:13 with vagrant in ~ at vagrant
➜ strace /bin/bash -c 'cd /tmp' 2>&1 | grep /tmp
execve("/bin/bash", ["/bin/bash", "-c", "cd /tmp"], 0x7ffd9aa62ba0 /* 27 vars */) = 0
stat("/tmp", {st_mode=S_IFDIR|S_ISVTX|0777, st_size=4096, ...}) = 0
chdir("/tmp")                           = 0
```

Соответственно нужный нам системный вызов `chdir("/tmp")`.

```bash
CHDIR(2)                                        Linux Programmer's Manual                                        CHDIR(2)

NAME
       chdir, fchdir - change working directory

SYNOPSIS
       #include <unistd.h>

       int chdir(const char *path);
       int fchdir(int fd);

   Feature Test Macro Requirements for glibc (see feature_test_macros(7)):

       fchdir():
           _XOPEN_SOURCE >= 500
               || /* Since glibc 2.12: */ _POSIX_C_SOURCE >= 200809L
               || /* Glibc up to and including 2.19: */ _BSD_SOURCE

DESCRIPTION
       chdir() changes the current working directory of the calling process to the directory specified in path.

       fchdir() is identical to chdir(); the only difference is that the directory is given as an open file descriptor.

RETURN VALUE
       On success, zero is returned.  On error, -1 is returned, and errno is set appropriately.

ERRORS
       Depending on the filesystem, other errors can be returned.  The more general errors for chdir() are listed below:

 Manual page chdir(2) line 1 (press h for help or q to quit)
```

#### 2. Попробуйте использовать команду `file` на объекты разных типов на файловой системе. Например:

    ```bash
    vagrant@netology1:~$ file /dev/tty
    /dev/tty: character special (5/0)
    vagrant@netology1:~$ file /dev/sda
    /dev/sda: block special (8/0)
    vagrant@netology1:~$ file /bin/bash
    /bin/bash: ELF 64-bit LSB shared object, x86-64
    ```
    
#### Используя `strace` выясните, где находится база данных `file` на основании которой она делает свои догадки.

На самом деле получился интересный вопрос =)

Запустим команды из примера:

```bash
21:51:53 with vagrant in ~ at vagrant
➜ file /dev/tty
/dev/tty: character special (5/0)

21:51:55 with vagrant in ~ at vagrant
➜ file /dev/sda
/dev/sda: block special (8/0)

21:52:05 with vagrant in ~ at vagrant
➜ file /bin/bash
/bin/bash: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=a6cb40078351e05121d46daa768e271846d5cc54, for GNU/Linux 3.2.0, stripped
```

Если вызвать `strace file /dev/tty` и посмотреть все системные вызовы, то по всей видимости база данных file находится в файле `/usr/share/misc/magic.mgc` :

```bash
stat("/home/vagrant/.magic.mgc", 0x7ffe78e3a7d0) = -1 ENOENT (No such file or directory)
stat("/home/vagrant/.magic", 0x7ffe78e3a7d0) = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/magic.mgc", O_RDONLY) = -1 ENOENT (No such file or directory)
stat("/etc/magic", {st_mode=S_IFREG|0644, st_size=111, ...}) = 0
openat(AT_FDCWD, "/etc/magic", O_RDONLY) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=111, ...}) = 0
read(3, "# Magic local data for file(1) c"..., 4096) = 111
read(3, "", 4096)                       = 0
close(3)
openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=5811536, ...}) = 0
mmap(NULL, 5811536, PROT_READ|PROT_WRITE, MAP_PRIVATE, 3, 0) = 0x7f0c91646000
close(3)
```

Аналогично с `strace file /dev/sda` и `file /bin/bash`

Проверим это:

```bash
22:26:41 with vagrant in ~ at vagrant
➜ file /usr/share/file/magic.mgc
/usr/share/file/magic.mgc: symbolic link to ../../lib/file/magic.mgc
```

Но команда `file` говорит что `/usr/share/misc/magic.mgc` символическая ссылка на `../../lib/file/magic.mgc`, т.е. на `/lib/file/magic.mgc`, проверим:

```bash
22:26:52 with vagrant in ~ at vagrant
➜ file /lib/file/magic.mgc
/lib/file/magic.mgc: magic binary file for file(1) cmd (version 14) (little endian)
```

Значит ответ на вопрос задания, база данных `file` находится тут `/lib/file/magic.mgc`, но в системном вызове используется символическая ссылка `/usr/share/misc/magic.mgc`

Хотя `man 5 magic` говорит что база данных лежит тут `/usr/share/misc/magic.mgc`

```bash
MAGIC(5)                                         BSD File Formats Manual                                         MAGIC(5)

NAME
     magic — file command's magic pattern file

DESCRIPTION
     This manual page documents the format of magic files as used by the file(1) command, version 5.38.  The file(1) com‐
     mand identifies the type of a file using, among other tests, a test for whether the file contains certain “magic
     patterns”.  The database of these “magic patterns” is usually located in a binary file in /usr/share/misc/magic.mgc
     or a directory of source text magic pattern fragment files in /usr/share/misc/magic.  The database specifies what
     patterns are to be tested for, what message or MIME type to print if a particular pattern is found, and additional
     information to extract from the file.
```

Но даже по выводу `ls` это не так:

```bash
22:33:36 with vagrant in ~ at vagrant took 47s
➜ ls -al /usr/share/misc/
total 1192
drwxr-xr-x   2 root root    4096 Aug 24 08:45 .
drwxr-xr-x 105 root root    4096 Dec 19 19:45 ..
lrwxrwxrwx   1 root root      13 Jan 16  2020 magic -> ../file/magic
lrwxrwxrwx   1 root root      24 Jan 16  2020 magic.mgc -> ../../lib/file/magic.mgc
-rw-r--r--   1 root root 1210291 Mar 20  2020 pci.ids
```

### База данных `file` находится тут `/lib/file/magic.mgc`

#### 3. Предположим, приложение пишет лог в текстовый файл. Этот файл оказался удален (deleted в lsof), однако возможности сигналом сказать приложению переоткрыть файлы или просто перезапустить приложение – нет. Так как приложение продолжает писать в удаленный файл, место на диске постепенно заканчивается. Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла (чтобы освободить место на файловой системе).

Получить `pid` процесса:

```bash
23:40:30 with vagrant in ~ at vagrant
➜ python3 test.py &
[1] 10176
```

Удостоверимся что процесс "работает" и данные в файл пишутся:

```bash
23:41:09 with vagrant in ~ at vagrant
✦ ➜ ps aux | grep 10176
vagrant    10176  0.0  0.2  15620  9332 pts/1    SN   23:41   0:00 python3 test.py```

```bash
23:43:35 with vagrant in ~ at vagrant
✦ ➜ wc -l test.txt
2 test.txt

23:43:43 with vagrant in ~ at vagrant
✦ ➜ wc -l test.txt
3 test.txt

23:43:50 with vagrant in ~ at vagrant
✦ ➜ cat test.txt

Sat Jan 22 23:43:30 2022
Sat Jan 22 23:43:40 2022
```

Как видим ему присвоен дескриптор `3`. Теперь удалим файл `/home/vagrant/test.txt`:

```bash
23:45:48 with vagrant in ~ at vagrant
✦ ➜ rm test.txt

23:47:45 with vagrant in ~ at vagrant
✦ ➜ lsof -p 10176
COMMAND   PID    USER   FD   TYPE DEVICE SIZE/OFF    NODE NAME
python3 10176 vagrant  cwd    DIR  253,0     4096 1051845 /home/vagrant
python3 10176 vagrant  rtd    DIR  253,0     4096       2 /
python3 10176 vagrant  txt    REG  253,0  5490488 1835435 /usr/bin/python3.8
python3 10176 vagrant  mem    REG  253,0  3035952 1835290 /usr/lib/locale/locale-archive
python3 10176 vagrant  mem    REG  253,0   108936 1841721 /usr/lib/x86_64-linux-gnu/libz.so.1.2.11
python3 10176 vagrant  mem    REG  253,0   182560 1841498 /usr/lib/x86_64-linux-gnu/libexpat.so.1.6.11
python3 10176 vagrant  mem    REG  253,0  1369352 1841579 /usr/lib/x86_64-linux-gnu/libm-2.31.so
python3 10176 vagrant  mem    REG  253,0    14848 1841706 /usr/lib/x86_64-linux-gnu/libutil-2.31.so
python3 10176 vagrant  mem    REG  253,0    18816 1841486 /usr/lib/x86_64-linux-gnu/libdl-2.31.so
python3 10176 vagrant  mem    REG  253,0   157224 1841646 /usr/lib/x86_64-linux-gnu/libpthread-2.31.so
python3 10176 vagrant  mem    REG  253,0  2029224 1841468 /usr/lib/x86_64-linux-gnu/libc-2.31.so
python3 10176 vagrant  mem    REG  253,0    27002     682 /usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache
python3 10176 vagrant  mem    REG  253,0   191472 1841428 /usr/lib/x86_64-linux-gnu/ld-2.31.so
python3 10176 vagrant    0u   CHR  136,1      0t0       4 /dev/pts/1
python3 10176 vagrant    1u   CHR  136,1      0t0       4 /dev/pts/1
python3 10176 vagrant    2u   CHR  136,1      0t0       4 /dev/pts/1
python3 10176 vagrant    3w   REG  253,0      626 1053714 /home/vagrant/test.txt (deleted)
```

Как видим файл удален `python3 10176 vagrant    3w   REG  253,0      626 1053714 /home/vagrant/test.txt (deleted)`, но по прежнему используется процессом.

Варианты очистки файла:

- Командой `true > /proc/10176/fd/3`
- Командой `echo > /proc/10176/fd/3` или `echo "" > /proc/10176/fd/3`
- Командой `cat /dev/null > /proc/10176/fd/3`
- или `truncate -s 0 /proc/10176/fd/3`, в приведенной команде `-s` используется для установки/настройки размера (в байтах) файла. `-s 0`, это означает, что мы изменили размер файла до 0 байт.

#### 4. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?


Процессы зомби, не являются реальными процессами. Это просто записи в таблице процессов ядра. Это единственный ресурс, который они потребляют. Они не потребляют ни CPU, ни RAM. Единственная опасность наличия зомби - это нехватка места в таблице процессов (можно использовать `cat /proc/sys/kernel/threads-max` чтобы узнать, сколько записей разрешено в системе).

```bash
00:10:39 with vagrant in ~ at vagrant
➜ cat /proc/sys/kernel/threads-max
30783
```

#### 5. В iovisor BCC есть утилита `opensnoop`:

    ```bash
    root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
    /usr/sbin/opensnoop-bpfcc
    ```

#### На какие файлы вы увидели вызовы группы `open` за первую секунду работы утилиты? Воспользуйтесь пакетом `bpfcc-tools` для Ubuntu 20.04. Дополнительные [сведения по установке](https://github.com/iovisor/bcc/blob/master/INSTALL.md).

```bash
00:59:04 with vagrant in ~ at vagrant
✦ ➜ sudo /usr/sbin/opensnoop-bpfcc
PID    COMM               FD ERR PATH
881    vminfo              5   0 /var/run/utmp
652    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
652    dbus-daemon        21   0 /usr/share/dbus-1/system-services
652    dbus-daemon        -1   2 /lib/dbus-1/system-services
652    dbus-daemon        21   0 /var/lib/snapd/dbus-1/system-services/
881    vminfo              5   0 /var/run/utmp
652    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
652    dbus-daemon        21   0 /usr/share/dbus-1/system-services
652    dbus-daemon        -1   2 /lib/dbus-1/system-services
652    dbus-daemon        21   0 /var/lib/snapd/dbus-1/system-services/
1451   python3             3   0 test.txt
657    irqbalance          6   0 /proc/interrupts
657    irqbalance          6   0 /proc/stat
657    irqbalance          6   0 /proc/irq/20/smp_affinity
657    irqbalance          6   0 /proc/irq/0/smp_affinity
657    irqbalance          6   0 /proc/irq/1/smp_affinity
657    irqbalance          6   0 /proc/irq/8/smp_affinity
657    irqbalance          6   0 /proc/irq/12/smp_affinity
657    irqbalance          6   0 /proc/irq/14/smp_affinity
657    irqbalance          6   0 /proc/irq/15/smp_affinity
881    vminfo              5   0 /var/run/utmp
652    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
652    dbus-daemon        21   0 /usr/share/dbus-1/system-services
652    dbus-daemon        -1   2 /lib/dbus-1/system-services
652    dbus-daemon        21   0 /var/lib/snapd/dbus-1/system-services/
```

#### 6. Какой системный вызов использует `uname -a`? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в `/proc`, где можно узнать версию ядра и релиз ОС.

```bash
01:02:12 with vagrant in ~ at vagrant
✦ ➜ strace uname -a
execve("/usr/bin/uname", ["uname", "-a"], 0x7ffc3865d5d8 /* 27 vars */) = 0
brk(NULL)                               = 0x55c41e458000
arch_prctl(0x3001 /* ARCH_??? */, 0x7ffe525d4ef0) = -1 EINVAL (Invalid argument)
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=26017, ...}) = 0
mmap(NULL, 26017, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f02a93a8000
close(3)                                = 0
openat(AT_FDCWD, "/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\360q\2\0\0\0\0\0"..., 832) = 832
pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 784, 64) = 784
pread64(3, "\4\0\0\0\20\0\0\0\5\0\0\0GNU\0\2\0\0\300\4\0\0\0\3\0\0\0\0\0\0\0", 32, 848) = 32
pread64(3, "\4\0\0\0\24\0\0\0\3\0\0\0GNU\0\t\233\222%\274\260\320\31\331\326\10\204\276X>\263"..., 68, 880) = 68
fstat(3, {st_mode=S_IFREG|0755, st_size=2029224, ...}) = 0
mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f02a93a6000
pread64(3, "\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0"..., 784, 64) = 784
pread64(3, "\4\0\0\0\20\0\0\0\5\0\0\0GNU\0\2\0\0\300\4\0\0\0\3\0\0\0\0\0\0\0", 32, 848) = 32
pread64(3, "\4\0\0\0\24\0\0\0\3\0\0\0GNU\0\t\233\222%\274\260\320\31\331\326\10\204\276X>\263"..., 68, 880) = 68
mmap(NULL, 2036952, PROT_READ, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7f02a91b4000
mprotect(0x7f02a91d9000, 1847296, PROT_NONE) = 0
mmap(0x7f02a91d9000, 1540096, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x25000) = 0x7f02a91d9000
mmap(0x7f02a9351000, 303104, PROT_READ, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x19d000) = 0x7f02a9351000
mmap(0x7f02a939c000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1e7000) = 0x7f02a939c000
mmap(0x7f02a93a2000, 13528, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7f02a93a2000
close(3)                                = 0
arch_prctl(ARCH_SET_FS, 0x7f02a93a7580) = 0
mprotect(0x7f02a939c000, 12288, PROT_READ) = 0
mprotect(0x55c41ce90000, 4096, PROT_READ) = 0
mprotect(0x7f02a93dc000, 4096, PROT_READ) = 0
munmap(0x7f02a93a8000, 26017)           = 0
brk(NULL)                               = 0x55c41e458000
brk(0x55c41e479000)                     = 0x55c41e479000
openat(AT_FDCWD, "/usr/lib/locale/locale-archive", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=3035952, ...}) = 0
mmap(NULL, 3035952, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f02a8ece000
close(3)                                = 0
uname({sysname="Linux", nodename="vagrant", ...}) = 0
fstat(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(0x88, 0), ...}) = 0
uname({sysname="Linux", nodename="vagrant", ...}) = 0
uname({sysname="Linux", nodename="vagrant", ...}) = 0
write(1, "Linux vagrant 5.4.0-91-generic #"..., 106Linux vagrant 5.4.0-91-generic #102-Ubuntu SMP Fri Nov 5 16:31:28 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
) = 106
close(1)                                = 0
close(2)                                = 0
exit_group(0)                           = ?
+++ exited with 0 +++
```

Используется системный вызов `uname({sysname="Linux", nodename="vagrant", ...})`

Обратимся к `man 2 uname`:

```bash
01:02:17 with vagrant in ~ at vagrant
✦ ➜ man 2 uname | grep /proc/
       Part of the utsname information is also accessible via /proc/sys/kernel/{ostype, hostname, osrelease, version, domainname}.
```

Сравним выводы:

```bash
01:05:49 with vagrant in ~ at vagrant
✦ ➜ uname -a
Linux vagrant 5.4.0-91-generic #102-Ubuntu SMP Fri Nov 5 16:31:28 UTC 2021 x86_64 x86_64 x86_64 GNU/Linux
```

```bash
01:08:03 with vagrant in ~ at vagrant
✦ ➜ cat /proc/sys/kernel/{ostype,hostname,osrelease,version,domainname}
Linux
vagrant
5.4.0-91-generic
#102-Ubuntu SMP Fri Nov 5 16:31:28 UTC 2021
(none)
```

#### 7. Чем отличается последовательность команд через `;` и через `&&` в bash? Например:
 
```bash
    root@netology1:~# test -d /tmp/some_dir; echo Hi
    Hi
    root@netology1:~# test -d /tmp/some_dir && echo Hi
    root@netology1:~#
```

#### Есть ли смысл использовать в bash `&&`, если применить `set -e`?

При использовании `;` следующая команда выполняется независимо от того, успешно ли выполнилась предыдущая.

При использовании `&&` следующая команда выполняется только если предыдущая выполнилась успешно, т.е. возвратила `0`

```bash
01:14:22 with vagrant in ~ at vagrant
✦ ➜ test -d /tmp/some_dir && echo Hi

01:14:28 with vagrant in ~ at vagrant
✦ ➜ test -d /tmp && echo Hi
Hi
```
<s>Использовать одновременно в bash `&&` и `set -e` в одной строке смысла нет, о чем сказано в `man bash`:</s>

Комментарий преподавателя:

> Алексей Федин
> 
> 24 января 2022 17:46
> 
> Добрый день!
> 
> Задание 7
> 
> С параметром -e оболочка завершится только при ненулевом коде возврата простой команды. Если ошибочно завершится одна из команд, разделённых &&, то выхода из шелла не произойдёт. Так что, смысл есть.
> 
> В man это поведение описано:
> 
> The shell does not exit if the command that fails is . . . part of any command executed in a && or || list except the command following the final &&

Осознал, спасибо, видимо я не так понял смысл фразы.


```bash
set [--abefhkmnptuvxBCEHPT] [-o option-name] [arg ...]
set [+abefhkmnptuvxBCEHPT] [+o option-name] [arg ...]
              Without options, the name and value of each shell variable are displayed in a format that can be reused as input for setting or resetting  the  currently-set  vari‐
              ables.   Read-only  variables cannot be reset.  In posix mode, only shell variables are listed.  The output is sorted according to the current locale.  When options
              are specified, they set or unset shell attributes.  Any arguments remaining after option processing are treated as values for the positional parameters and are  as‐
              signed, in order, to $1, $2, ...  $n.  Options, if specified, have the following meanings:
              
              -a      Each variable or function that is created or modified is given the export attribute and marked for export to the environment of subsequent commands.
              
              -b      Report  the  status  of  terminated background jobs immediately, rather than before the next primary prompt.  This is effective only when job control is en‐
                      abled.
             
              -e      Exit immediately if a pipeline (which may consist of a single simple command), a list, or a compound command (see SHELL GRAMMAR above), exits  with  a  non-
                      zero status.  The shell does not exit if the command that fails is part of the command list immediately following a while or until keyword, part of the test
                      following the if or elif reserved words, part of any command executed in a && or || list except the command following the final && or ||, any command  in  a
                      pipeline but the last, or if the command's return value is being inverted with !.  If a compound command other than a subshell returns a non-zero status be‐
                      cause a command failed while -e was being ignored, the shell does not exit.  A trap on ERR, if set, is executed before the shell exits.  This option applies
                      to  the shell environment and each subshell environment separately (see COMMAND EXECUTION ENVIRONMENT above), and may cause subshells to exit before execut‐
                      ing all the commands in the subshell.

                      If a compound command or shell function executes in a context where -e is being ignored, none of the commands executed within the compound command or  func‐
                      tion  body  will  be  affected by the -e setting, even if -e is set and a command returns a failure status.  If a compound command or shell function sets -e
                      while executing in a context where -e is ignored, that setting will not have any effect until the compound command or the command  containing  the  function
                      call completes.
```

#### 8. Из каких опций состоит режим bash `set -euxo pipefail` и почему его хорошо было бы использовать в сценариях?

`-e` - прекращает выполнение скрипта если команда завершилась ошибкой, выводит в `stderr` строку с ошибкой. Обойти эту проверку можно добавив в `pipeline` к команде `true`: `mycommand | true`.

`-u` - прекращает выполнение скрипта, если встретилась несуществующая переменная.

`-x` - выводит выполняемые команды в `stdout` перед выполнением.

`-o pipefail` - прекращает выполнение скрипта, даже если одна из частей `pipe` завершилась ошибкой. В этом случае bash-скрипт завершит выполнение, если `mycommand` вернёт ошибку, не смотря на `true` в конце `pipeline`: `mycommand | true`.


Считаю что, при работе с bash будет хорошим тоном начинать каждый сценарий с set -euxo pipefail

#### 9. Используя `-o stat` для `ps`, определите, какой наиболее часто встречающийся статус у процессов в системе. В `man ps` ознакомьтесь (`/PROCESS STATE CODES`) что значат дополнительные к основной заглавной буквы статуса процессов. Его можно не учитывать при расчете (считать S, Ss или Ssl равнозначными).

```bash
01:51:30 with vagrant in ~ at vagrant took 27m 4s
➜ ps -o stat
STAT
Ss
R+
```
 
Наиболее часто встречающийся `S` (обычный спящий процесс, который может быть прерван, ожидает какого-то события)и `R` (исполняется или ожидает исполнения)

```bash
01:51:56 with vagrant in ~ at vagrant
➜ man ps
```

```bash
PROCESS STATE CODES
       Here are the different values that the s, stat and state output specifiers (header "STAT" or "S") will display to describe the state of a process:

               D    uninterruptible sleep (usually IO)
               I    Idle kernel thread
               R    running or runnable (on run queue)
               S    interruptible sleep (waiting for an event to complete)
               T    stopped by job control signal
               t    stopped by debugger during the tracing
               W    paging (not valid since the 2.6.xx kernel)
               X    dead (should never be seen)
               Z    defunct ("zombie") process, terminated but not reaped by its parent

       For BSD formats and when the stat keyword is used, additional characters may be displayed:

               <    high-priority (not nice to other users)
               N    low-priority (nice to other users)
               L    has pages locked into memory (for real-time and custom IO)
               s    is a session leader
               l    is multi-threaded (using CLONE_THREAD, like NPTL pthreads do)
               +    is in the foreground process group
```
 ---

## Как сдавать задания

Обязательными к выполнению являются задачи без указания звездочки. Их выполнение необходимо для получения зачета и диплома о профессиональной переподготовке.

Задачи со звездочкой (*) являются дополнительными задачами и/или задачами повышенной сложности. Они не являются обязательными к выполнению, но помогут вам глубже понять тему.

Домашнее задание выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Также вы можете выполнить задание в [Google Docs](https://docs.google.com/document/u/0/?tgif=d) и отправить в личном кабинете на проверку ссылку на ваш документ.
Название файла Google Docs должно содержать номер лекции и фамилию студента. Пример названия: "1.1. Введение в DevOps — Сусанна Алиева".

Если необходимо прикрепить дополнительные ссылки, просто добавьте их в свой Google Docs.

Перед тем как выслать ссылку, убедитесь, что ее содержимое не является приватным (открыто на комментирование всем, у кого есть ссылка), иначе преподаватель не сможет проверить работу. Чтобы это проверить, откройте ссылку в браузере в режиме инкогнито.

[Как предоставить доступ к файлам и папкам на Google Диске](https://support.google.com/docs/answer/2494822?hl=ru&co=GENIE.Platform%3DDesktop)

[Как запустить chrome в режиме инкогнито ](https://support.google.com/chrome/answer/95464?co=GENIE.Platform%3DDesktop&hl=ru)

[Как запустить  Safari в режиме инкогнито ](https://support.apple.com/ru-ru/guide/safari/ibrw1069/mac)

Любые вопросы по решению задач задавайте в чате учебной группы.

---
