# Zabbix_menupopup_app ver 1.0b
- Требуется перевод на "Английския язык"
- Требуется лексическая переработка данного текста
- Для размещения перевода пишите в телеграм https://t.me/Dark_Ph0eNix

# Zabbix_menupopup_app
Данная доработка предназначена для упрощения работы пользователей Zabbix, путем добавления дополнительных пунктов во всплывающее меню Dashboard при нажатии на которые будет запускаться необходимое приложение.

# Принцип работы
```
Zabbix Dashboard --> Нажатие левой кнопкой мыши по Хосту --> Нажатие на добавленный вами пункт в меню -->
--> Передача 'hostid" в функцию "get_ip" в "menupopup.js" -->
--> **get_ip:** POST запрос c "hostid" к "get_ip_api.php" --> 
--> **get_ip_api.php:** POST запрос c "hostid" к "Zabbix_API" -->
--> **get_ip_api.php:** Получение "IP" от "Zabbix_API" и вывод его -->
--> **get_ip:** Получение "IP" и передача его в "код управления" созданного вами пункта меню -->
--> **"код управления:"** Открытие новой вкладки в адресе которой будет **"protocol://IP_адрес_хоста"** -->
--> Windows запускает связанную программу с протоколом и передает ей полный url **"protocol://IP_адрес_хоста"** -->
--> Связанная программа обрабатывает полный url деля его на "protocol", "ip" "port"* и если протокол описан в конфигурациионном файле, то запускает связанную с данным протоколом программу указанную в конфигурацинном файле
```

### Системные требования для установки и использования:
* Серверная часть: 
    - Zabbix 5.0 включающий в себя:
```
Веб сервер "nginx" или "apache"
php 5.4.0 или новее
@JQuery 3.3.1 или новее
**Пользователь для работы с API с соответствующими доступом к группам хостов**
```

* Клиентская часть (Windows):
    - Windows 7 или новее
    - Python 3.8 (возможно будет работать и на более старых версиях)
 
# Установка серверной части и пояснение изменений:
###### **menupopup.js**
- Создайте резервную копию "menupopup.js" из папки "/usr/share/zabbix/js/"
- Скопируйте загруженный "menupopup.js" в папку "/usr/share/zabbix/js/"
```
// Получаем IP адрес узла передав в функцию его hostid
var ip = get_ip(options.hostid);
// Если в опциях не указан раздел tools то показать (получилось только так)
if (!options.tools) {
    // Создаем список основного меню
    var vnc = {
        // Указываем название пункта меню
        label: t('VNC'),
        // Указываем по какой ссылке будет выполнен переход, в данном случае указан протокол и ip адрес узла
        url: 'vnc://' + ip,
        // Создаем подменю. По такому же принципу как и основное менб
        items: [{
            label: t('VNC port 5901'),
            url: 'vnc://' + ip + ':5901',
            target: '_blank'
        },{
            label: t('Sub Menu 2'),
            url: 'vnc://' + ip + ':5902',
            target: '_blank'
        }],
        target: '_blank'
    },
    ssh = {
        label: t('SSH'),
        url: 'ssh://' + ip,
        target: '_blank'
    },
    telnet = {
        label: t('Telnet'),
        url: 'telnet://' + ip,
        target: '_blank'
    },
    winbox = {
        label: t('Winbox'),
        url: 'winbox://' + ip,
        target: '_blank'
    };
    // Создаем список Items для основного меню
    var items = [
        vnc,
        ssh,
        telnet,
        winbox
    ];
    // Добавляем меню в массив из которого строится контекстное меню
    sections.push({
        label: t('Tools'),
        items: items
    });
}
```
**Выше описанный блок вставляется**
```
    // scripts
    if (typeof options.scripts !== 'undefined') {
        sections.push({
            label: t('Scripts'),
            items: getMenuPopupScriptData(options.scripts, options.hostid, trigger_elmnt)
        });
    }
//Вставить сюда
    return sections;
}
```
**В конец файла добавить**
```
//Function getip from API by hodtid
function get_ip(host_id){
  var ip_address = '';
  $.ajax({
    type:'POST',
    data:{hostid:host_id},
    url:'get_ip_api.php',
    async:false,
    success:function(text)
      {
        ip_address = text
      }
  });
  return ip_address;
}
```

###### **get_ip_api.php**
- Скопируйте загруженный "get_ip_api.php" в папку "/usr/share/zabbix/"

В скрипте измените логин и пароль на свои
```
$login = 'API_user';
$password = 'API_password';
```

**Перезапустите веб сервер**
```html
systemctl restart ngnix/apache
```

# Установка клиентской части и пояснение изменений:
- Установить **configparser** для python
    ```
    pip install configparser
    ```
- Создайте на диске "С" папку "web_protocol"
- Скопируйте загруженный "web_protocol.exe" и "web_protocol.cond" в созданную папку
    ```
    [vnc] - Наименование протокола
    path="C:\Program Files\TightVNC\tvnviewer.exe" - Путь до исполняемого файла
    port_settings="::" - параметры порта если он будет указан в протоколе

    [winbox]
    path="C:\Windows\System32\winbox.exe"

    [ssh]
    path="C:\Program Files\PuTTY\putty.exe" -ssh
    port_settings=" -P "

    [telnet]
    path="C:\Program Files\PuTTY\putty.exe" -telnet
    port_settings=" -P "
    ```
---
## **Учтите при указании параметра порта необходимо добавлять или убирать проблелы, смотрите документацию на запускаемою программу!!!**
Например:
```
[ssh]
path="C:\Program Files\PuTTY\putty.exe" -ssh
port_settings="-P"
```
Запустит "Putty" со следующими параметрами
```
C:\Program Files\PuTTY\putty.exe" -ssh-P1234
```
---

- Добавьте в реестр Windows необходимые протоколы
```
web_protocol_vnc.reg
web_protocol_winbox.reg
web_protocol_ssh.reg
web_protocol_telnet.reg
```
---
Для регистрация собственного протокола необходимо создать файл со следующим содержимым и расширением ".reg"
```
Windows Registry Editor Version 5.00
[HKEY_CLASSES_ROOT\new_protocol]
@="Run new_protocol"
"URL Protocol"=""

[HKEY_CLASSES_ROOT\new_protocol\DefaultIcon]
@="C:\\web_protocol\\web_protocol.exe,0"

[HKEY_CLASSES_ROOT\new_protocol\shell]

[HKEY_CLASSES_ROOT\new_protocol\shell\open]

[HKEY_CLASSES_ROOT\new_protocol\shell\open\command]
@="\"C:\\web_protocol\\web_protocol.exe\" \"%1\""
```
После чего данный файл добавить в реестр Windows
***
