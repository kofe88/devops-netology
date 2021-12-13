# Домашнее задание к занятию «2.4. Инструменты Git»

1. Найдите полный хеш и комментарий коммита, хеш которого начинается на `aefea`.

```bash
git show aefea
```

```bash
commit aefead2207ef7e2aa5dc81a34aedf0cad4c32545
Author: Alisdair McDiarmid <alisdair@users.noreply.github.com>
Date:   Thu Jun 18 10:29:58 2020 -0400

    Update CHANGELOG.md

diff --git a/CHANGELOG.md b/CHANGELOG.md
index 86d70e3e0..588d807b1 100644
--- a/CHANGELOG.md
+++ b/CHANGELOG.md
@@ -27,6 +27,7 @@ BUG FIXES:
 * backend/s3: Prefer AWS shared configuration over EC2 metadata credentials by default ([#25134](https://github.com/hashicorp/terraform/issues/25134))
 * backend/s3: Prefer ECS credentials over EC2 metadata credentials by default ([#25134](https://github.com/hashicorp/terraform/issues/25134))
 * backend/s3: Remove hardcoded AWS Provider messaging ([#25134](https://github.com/hashicorp/terraform/issues/25134))
+* command: Fix bug with global `-v`/`-version`/`--version` flags introduced in 0.13.0beta2 [GH-25277]
 * command/0.13upgrade: Fix `0.13upgrade` usage help text to include options ([#25127](https://github.com/hashicorp/terraform/issues/25127))
 * command/0.13upgrade: Do not add source for builtin provider ([#25215](https://github.com/hashicorp/terraform/issues/25215))
 * command/apply: Fix bug which caused Terraform to silently exit on Windows when using absolute plan path ([#25233](https://github.com/hashicorp/terraform/issues/25233))
```

2. Какому тегу соответствует коммит `85024d3`?

Тегу `v0.12.23` :

```bash
git show 85024d3
```

```bash
commit 85024d3100126de36331c6982bfaac02cdab9e76 (tag: v0.12.23)
Author: tf-release-bot <terraform@hashicorp.com>
Date:   Thu Mar 5 20:56:10 2020 +0000

    v0.12.23
```

3. Сколько родителей у коммита `b8d720`? Напишите их хеши.

Два родителя `Merge: 56cd7859e 9ea88f22f` , т.к. это мерж коммит:

```bash
git show b8d720
```

```bash
commit b8d720f8340221f2146e4e4870bf2ee0bc48f2d5
Merge: 56cd7859e 9ea88f22f
Author: Chris Griggs <cgriggs@hashicorp.com>
Date:   Tue Jan 21 17:45:48 2020 -0800

    Merge pull request #23916 from hashicorp/cgriggs01-stable
    
    [Cherrypick] community links
```

Родитель 1, который является тоже мерж коммитом :

```bash
git show b8d720^1
```

```bash
commit 56cd7859e05c36c06b56d013b55a252d0bb7e158
Merge: 58dcac4b7 ffbcf5581
Author: Chris Griggs <cgriggs@hashicorp.com>
Date:   Mon Jan 13 13:19:09 2020 -0800

    Merge pull request #23857 from hashicorp/cgriggs01-stable
    
    [cherry-pick]add checkpoint links
```

Родитель 2 :

```bash
git show b8d720^2
```

```bash
commit 9ea88f22fc6269854151c571162c5bcf958bee2b
Author: Chris Griggs <cgriggs@hashicorp.com>
Date:   Tue Jan 21 17:08:06 2020 -0800

    add/update community provider listings
```

4. Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами  v0.12.23 и v0.12.24.

```bash
git log v0.12.23..v0.12.24 --oneline
```

```bash
33ff1c03b (tag: v0.12.24) v0.12.24
b14b74c49 [Website] vmc provider links
3f235065b Update CHANGELOG.md
6ae64e247 registry: Fix panic when server is unreachable
5c619ca1b website: Remove links to the getting started guide's old location
06275647e Update CHANGELOG.md
d5f9411f5 command: Fix bug when using terraform login on Windows
4b6d06cc5 Update CHANGELOG.md
dd01a3507 Update CHANGELOG.md
225466bc3 Cleanup after v0.12.23 release
```

5. Найдите коммит в котором была создана функция `func providerSource`, ее определение в коде выглядит 
так `func providerSource(...)` (вместо троеточего перечислены аргументы).

```bash
git log -S 'func providerSource(' --oneline
```

```bash
8c928e835 main: Consult local directories as potential mirrors of providers
```

```bash
git show 8c928e835
```

```bash
commit 8c928e83589d90a031f811fae52a81be7153e82f
Author: Martin Atkins <mart@degeneration.co.uk>
Date:   Thu Apr 2 18:04:39 2020 -0700

    main: Consult local directories as potential mirrors of providers
```

6. Найдите все коммиты в которых была изменена функция `globalPluginDirs`.

Найдем файл, где определение функции:

```bash
git grep -n 'globalPluginDirs'
```

```bash
commands.go:88:         GlobalPluginDirs: globalPluginDirs(),
commands.go:430:        helperPlugins := pluginDiscovery.FindPlugins("credentials", globalPluginDirs())
internal/command/cliconfig/config_unix.go:34:           // FIXME: homeDir gets called from globalPluginDirs during init, before
plugins.go:12:// globalPluginDirs returns directories that should be searched for
plugins.go:18:func globalPluginDirs() []string {
```

Видим что это файл `plugins.go`.

Теперь посмотрим как функция менялась:

```bash
git log --no-patch --oneline -L :globalPluginDirs:plugins.go
```

```bash
78b122055 Remove config.go and update things using its aliases
52dbf9483 keep .terraform.d/plugins for discovery
41ab0aef7 Add missing OS_ARCH dir to global plugin paths
66ebff90c move some more plugin search path logic to command
8364383c3 Push plugin discovery down into command package
```

7. Кто автор функции `synchronizedWriters`? 

```bash
git log -S'synchronizedWriters' --pretty=format:"%H %an %ad %s" --reverse | head -1
```

```bash
5ac311e2a91e381e2f52234668b49ba670aa0fe5 Martin Atkins Wed May 3 16:25:41 2017 -0700 main: synchronize writes to VT100-faker on Windows
```


