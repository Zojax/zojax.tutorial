==========================================================
Использование Control Panel для конфигурации приложения
==========================================================
Вcя реализация `Control Panel` находится в пакете
`zojax.controlpanel <http://pypi.python.org/pypi/zojax.controlpanel/>`_.

Введение
========

Эта глава содержит информацию о `Control Panel`. Практически все 
аспекты работы системы zojax конигурируются с помощью `Control 
Panel`. Мы создадим `configlet` который будет контролировать глобальные 
настрйки нашего `MessageBoard`. 

Рано или поздно практически для каждого приложения появляются глобальные 
настройки. Чтобы решить эту задачу стандартными возможностями zope3 
разработчику приходится создавать `local utility` котороя и будет хранить
это настройки. При этом приходится создавать специальные методы инсталяции
этой утилиты в сайт, и существует вероятность при деинсталяции продукта
получить `broker` обьект в ZODB.


Интерфейс для `Configlet`'а
-----------------------------

В zojax конфигурация происходит с помощью `Configlet`'ов. В первую
очередь нам нужно определить интерфейс который описывает данные.

Мы определим `Configlet` который бодет содержать только один параматер
`forum_page_size`::

  from zope import interface
  
  class IMessageBoardConfiglet(interface.Interface):
  
      forum_page_size = schema.Int(
          title = u'Forum page size',
          description = u'Number of topic per page.',
          default = 20,
          required = False)

Мы должны использовать `default` аттрибут для всех полей интерфейса,
потому что это значение будет использоватся по умолчанию для нашего `Configlet`


Регистрация `Configlet`'а
-------------------------

Мы должны зарегестрировать конфиглет в zojax. Это делается с помощью 
директивы `zojax:cofiglet`::

  <zojax:configlet
     name="system.messageboard"
     schema=".interfaces.IMessageBoardConfiglet"
     title="MessageBoard settings"
     description="Configure global `MessageBoard` settings." />

В общем-то это все, теперь менеджер сайта может изменять параметры. 
И разработчик может использовать это конфиглет через интерфейс,
не задумываясь о создании утилиты и методе хранении информации::

  from zope.component import getUtility
  from zojax.tutorial.interfaces import IMessageBoardConfiglet

  # это код
  configlet = getUtility(IMessageBoardConfiglet)

  configlet.forum_page_size = 25

или по имени::

  from zope.component import getUtility
  from zojax.controlpanel.interfaces import IConfiglet

  # это код
  configlet = getUtility(IConfiglet, name='system.messageboard`)

  configlet.forum_page_size = 25


Описание директивы `zojax:configlet`
-------------------------------------

name
  Имя конфиглета, уникально в системе

schema
  Интерфейс который описывает конфиглет

title
  Название для пользовательского интерфейса

description
  Краткое описание конфиглета

class
  `custom` раализация для конфиглета

provides
  Дополнительные интерфейсы которые должен реализовывать конфиглет

permission
  Permission для доступа к полям конфиглета

tests
  Тесты которые проверяют доступность этого конфиглета для дользовательского
  интерфейса


Регистрация конфиглета, детальное описание
--------------------------------------------

В процессе регистрации создается новый клас который описывает конфиглет.
Как metaclass используется `ConfigletType <http://zojax.svn.sourceforge.net/viewvc/zojax/zojax.controlpanel/trunk/src/zojax/controlpanel/configlettype.py?view=markup>`_.
Для базового класа используется класс `Configlet <http://zojax.svn.sourceforge.net/viewvc/zojax/zojax.controlpanel/trunk/src/zojax/controlpanel/configlet.py?view=markup>`_.
Для каждого `schema field` в интерфейсе конфиглета создается специальное
`property` `ConfigletProperty <http://zojax.svn.sourceforge.net/viewvc/zojax/zojax.controlpanel/trunk/src/zojax/controlpanel/configlettype.py?view=markup>`_.
Который берет значение поля не из аттрибутов обьекта а из специального атрибута
`data <http://zojax.svn.sourceforge.net/viewvc/zojax/zojax.controlpanel/trunk/src/zojax/controlpanel/configlet.py?view=markup>`_,
который в свою очередь использует утилиту `IDataStorage <http://zojax.svn.sourceforge.net/viewvc/zojax/zojax.controlpanel/trunk/src/zojax/controlpanel/interfaces.py?view=markup>`_
чтобы получить доступ к хранилищу со всеми данными. Вы можете изменить 
поведение конфиглета или добавить дополнительную функциональность, предоставив
свой клас в атрибуте `class` директивы `zojax:configlet`. Для примера можно
посмотреть `Mail configlet <http://zojax.svn.sourceforge.net/viewvc/zojax/zojax.mail/trunk/src/zojax/mail/mailer.py?view=markup>`_ который кроме настроек smtp host
реализует IMailer из zope.sendmail

Также создается `security declarations` для нового класа, по умолчанию
используется `permissions` из директивы, но вы можете изменить это.
Вам нужно добавить `security declarations` в описание директивы, так же как
для директивы `class`. Например::

  <zojax:configlet
     name="system.messageboard"
     schema=".interfaces.IMessageBoardConfiglet"
     title="MessageBoard settings"
     description="Configure global `MessageBoard` settings.">
    <require
       permission="zope.Public"
       interface=".interfaces.IMessageBoardConfiglet" />
  </zojax:configlet>

Имя конфиглета не случайно использует '.' 
Имя конфиглета используется чтобы построить дерево конфиклетов. Например
`system.messageboard` будет находится в категории `system`, а `system` в главном
конфиглете без имени. Из каждой категории можно получить доступ к вложенным
конфиглетам::

   from zope.component import getUtility
   from zojax.controlpanel.interfaces import IConfiglet

   root = getUtility(IConfiglet)

   mesasgecoard_configlet = root['system']['messageboard']

MessageBoard конфиглет сам может являтся категорией конфиглетов. Также 
имя конфиглета используется для пользовательского интерфейса, для 
`system.messageboard` путь будет::

   /settings/system/messageboard



Ссылки
~~~~~~~

* Egg `zojax.content <http://pypi.python.org/pypi/zojax.controlpanel/>`_

* `Исходный код zojax.tutorial глава 3 <http://zojax.svn.sourceforge.net/viewvc/zojax/zojax.tutorial/branches/step3/src/zojax/tutorial/>`_

* `Исходный код zojax.controlpanel <http://zojax.svn.sourceforge.net/viewvc/zojax/zojax.controlpanel />`_
