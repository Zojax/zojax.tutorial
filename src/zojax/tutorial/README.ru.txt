================================
Создание конетных типов в zojax
================================

Эта глава содержит базовую информацию о контентной системе zojax.
Разработчик должен быть знаком с основными концепциями и иметь 
опыт работы с zope3. Здесь используется MessageBoard пакет который
используется в "Zope Developer's Book" Stephen Ritcher.
Мы создадим версию MessageBoard для zojax.


Описание
=========

Вся система работы с контентными типами находится в пакете `zojax.content.type
<http://pypi.python.org/pypi/zojax.content.type/>`_.
Контентная система является одной из базовых состовляющих системы zojax и
используется во множестве сотовляющих подсистем.

Цель этого tutorial'а создать простой и функциональный
MessageBoard, при этом задействовать множество сервисов предоставляемых zojax.
`Весь код для данной главы находится в svn <http://zojax.svn.sourceforge.net/viewvc/zojax/sources/zojax.tutorial/branches/step1/src/zojax/tutorial/>`_


Определение интерфейсов
=========================

Начнем с определния интерфейсов для нашего `MessageBoard`::

    from zojax.content.interfaces import IItem
   
    class IMessageBoard(IItem):
       """The message board is the base object for our package. It can only
          contain IMessage objects."""


В большинстве случаев наш интерфес должен наследовать IItem интервейс из
`zojax.content.type`. `IItem <http://zojax.svn.sourceforge.net/viewvc/zojax/sources/zojax.content.type/trunk/src/zojax/content/type/interfaces.py?view=markup>`_ определяет два поля, `title` и `description`. 
Это очень важно чтобы каждый контентный тип имел эти поля, потому 
что они используютя во различных частях системы. Как вы видите интерфейс 
очень простой. Наш `MessageBoard` клас будет иметь только `title` и `description`.

Теперь интерфейс для `Message`::

    from zope import schema, interface
    from zojax.richtext.field import RichText
    
    class IMessage(interface.Interface):
        """A message object."""
   
        title = schema.TextLine(
            title=u"Title/Subject",
            description=u"Title and/or subject of the message.",
            default=u"",
            required=True)
   
        body = RichText(
            title=u"Message Body",
            description=u"This is the actual message. Type whatever you wish.",
            default=u"",
            required=True)

Для этого интерфейса мы не исползуем IItem, но мы все равно должны 
предоставить доступ к `description`. Для `body` мы используем `RichText field
<http://zojax.svn.sourceforge.net/viewvc/zojax/sources/zojax.richtext/trunk/src/zojax/richtext/field.py?view=markup>`_
из пакета `zojax.richtext <http://pypi.python.org/pypi/zojax.richtext/>`_,
RichText field позволяет использовать различные
форматы для текста и к тому же позволяет использовать разные `Visual editor` 
например `extjs` или `tinymce`. Так же каждый пользователь может выбрать 
`editor` конкретно для себя.

В отличии от стандартной практики zope3 где в интерфейсах определяются 
`contraints` (preconditions) в zojax этого делать не нужно. `constraints` 
определяютя на более высоком уровне. И со временем `zojax.content` позволит
изменять `contraints` в `runtime`.

Так же мы определим интерфейс для темы, вы можете посмотреть польное 
определение интрефейсов `MessageBoard` в файле `interfaces.py <http://zojax.svn.sourceforge.net/viewvc/zojax/sources/zojax.tutorial/branches/step1/src/zojax/tutorial/interfaces.py?view=markup>`_


Реализация класов
=================

Начнем с простого клаcса `MessageBoard`::

    from zope import interface
    from zojax.content.container import ContentContainer
    from zojax.tutorial.interfaces import IMessageBoard
    
    class MessageBoard(ContentContainer):
        """A very simple implementation of a message board """
        interface.implements(IMessageBoard)

Этот клас очень простой, единственно нужно пояснение по поводу `ContentContainer`.
Наследование от ContentContainer сделанно просто чтобы упростить реализацию. 
`ContentContainer <http://zojax.svn.sourceforge.net/viewvc/zojax/sources/zojax.content.type/trunk/src/zojax/content/type/container.py?view=markup>`_ 
есть не что иное как `BTreeContainer` из `zope.app.container`. Также он реализует
интерфейс `IContentContainer <http://zojax.svn.sourceforge.net/viewvc/zojax/sources/zojax.content.type/trunk/src/zojax/content/type/interfaces.py?view=markup>`_.
В отличае от стандартного контейнера в котором если есть доступ к
методу `__delitem__`, можно удалить любой элемент контейнера,
в `ContentContainer` нужно еще иметь permission `zojax.DeleteContent` для самого
удаляемого элемента. Несмотря на то что клас очень простой этого достаточно
для создания достаточно сложных приложений.

Теперь клас для `Message`::

    from zope import interface
    from zojax.content.item import PeristentItem
    from zojax.tutorial.interfaces import IMessage
    
    class Message(PersistentItem):
        """A simple implementation of a message."""
        interface.implements(IMessage)

Этот клас использует `PersistentItem`. Что примечательного в 
`Item <http://zojax.svn.sourceforge.net/viewvc/zojax/sources/zojax.content.type/trunk/src/zojax/content/type/item.py?view=markup>`_. Этот клас использует несколько интерфейсов 
маркеров, `IAttributeAnnotatable` и `IOwnerAware <http://svn.zope.org/zojax.ownership/trunk/src/zojax/ownership/interfaces.py?view=markup>`_. 
И хранит значения в title и description в `ICMFDublinCore`.

Немного информации о владелце обьекта `IOwnership <http://svn.zope.org/zojax.ownership/trunk/src/zojax/ownership/interfaces.py?view=markup>`_. 
object ownership реализуется в пакете 
`zojax.ownership <http://pypi.python.org/pypi/zojax.ownership/>`.
По умолчанию владелец присвается обьекту на этапе создания. 
Пользователь который является владельцем обьекта имеет специальную
роль `content.Owner`, но только но этом обьекте. Что это значит? Например
пользователь1 создал MessageBoard а пользователь2 создал тему в этом 
MessageBoard, теперь пользователь1 является владельцем MessageBoard и имеет 
роль `content.Owner` но он не является владельцем темы созданной пользователем2
и в этой теме у него нет роли `content.Owner` хотя тема находится в MessageBoard, 
в zope3 в такой ситуации пользователь1 будет иметь роль `content.Owner` и в 
MessageBoard и в теме пользователя2.

Для польной реализации смотрите файлы `message.py <http://zojax.svn.sourceforge.net/viewvc/zojax/sources/zojax.tutorial/branches/step1/src/zojax/tutorial/message.py?view=markup>`_,
`messageboard.py <http://zojax.svn.sourceforge.net/viewvc/zojax/sources/zojax.tutorial/branches/step1/src/zojax/tutorial/messageboard.py?view=markup>`_,
`topic.py <http://zojax.svn.sourceforge.net/viewvc/zojax/sources/zojax.tutorial/branches/step1/src/zojax/tutorial/topic.py?view=markup>`_


Регистрация контентных типов в zojax
=====================================

Последний шаг в реализации контентного типа это регистрация в zojax. Это 
делается с помощью директивы `zojax:content`.

Регистрация для `Message`, контент тип называется `zojax.tutorial.Message`::

  <zojax:content
     title="Message"
     name="zojax.tutorial.Message"
     schema=".interfaces.IMessage"
     description="Message for MessageBoard" 
     class=".message.Message"
     containers="zojax.tutorial.Topic"
     permission="zojax.AddMessage" />

Детальное описание директивы `zojax:content
<http://zojax.svn.sourceforge.net/viewvc/zojax/sources/zojax.content.type/trunk/src/zojax/content/type/README.txt?view=markup>`_

name
  Имя регистрируемого типа, уникально в системе.

title
  Название типа используемого для пользовательского интерфейса

description
  Краткое описание типа используемого для пользовательского интерфейса

schema
  Интерфейс который описывает контент тип, также используется для 
  генерации `add form` и `edit form`

class
  Класс обьекта

contains
  Список типов которые может содержать данный тип

containers
  Контент типы которые могут содержать данный тип

contenttype
  `custom` реализация `IContentType`

permission
  Permission который позволяет добавлять данный контент тип в контекст


Что происходит в процесе регистрации контент типа в zojax. Во первых
происходит создание специального обьекта который реализует интерфейс 
IContentType. Так же для каждого типа происходит создание интерфейса.
Название интерфейса генерится из имени контент типа, например для 
нашего типа 'zojax.tutorial.Message' сгенерится интерфейс zojax_tutorial_Message
Этот интерфейс будет доступен таким образом::

   zojax.content.zojax_tutorial_Message

Также созданный IContentType обьект будет реализовывать этот интерфейс.

IContentType обьект контролирует множество аспектов жизни контент типа.
Создание обьекта, проверка permissions, contraints, формы добавления, и много
другое. Вы можете предоставить вашу собственную реализацию этого 
обьекта и это открывает намного больше возможновтей. Допустим при добавлении
обьекта вы можете добавлять его в другое место отльчное от того где 
создается контент. Так же с помощиью этого обьекты вы можете создавать 
контент в питоновском коде. Этот обьект регистрируется в системе как утилита 
с таким же именем как и конент тип. т.е. вы можете получить этот 
обьект таким образом::

   from zope.component import getUtility
   from zojax.content.interfaces import IContentType

   getUtility(IContentType name='zojax.tutorial.Message')

И создать контентный обьект так::

   contenttype = getUtility(IContentType name='zojax.tutorial.Message')
   message = contenttype.create()

Можно также добавить контент тип в контексте, на этом этапе происходит проверка
permission, также проверяется `contraints` (containers, contains)::

   # вам нужен контекст `context`
   contenttype = contenttype.__bind__(context)
   contenttype.add(content, name='object name')

Теперь регистрация для `MessageBoard`. Единственное отличие аттрибут `contains`,
который указывает, что `MessageBoard` может содержать только 
`zojax.tutorial.Topic` обьекты.::

  <zojax:content
     title="MessageBoard"
     name="zojax.tutorial.MessageBoard"
     schema=".interfaces.IMessageBoard"
     class=".messageboard.MessageBoard"
     description="Very simple MessageBoard"
     contains="zojax.tutorial.Topic"
     permission="zojax.AddContent" />


Подводя итоги
=============

Весь процес создания контент тиапов сводится к нескольким шагам

1. Создание интерфейсов
 
2. Реализация класов

3. Регистрация конент типов с помощью `zojax:content` директивы


Замечания по реализации
========================

Мы используем IContainerNamesContainer для MessageBoard и Topic, чтобы програмно
выбирать `id` для топиков и сообщений.


Links
~~~~~

* Egg `zojax.content.type <http://pypi.python.org/pypi/zojax.content.type/>`_

* Egg `zojax.richtext <http://pypi.python.org/pypi/zojax.richtext/>`_

* Egg `zojax.ownership <http://pypi.python.org/pypi/zojax.ownership/>`_

* `Исходный код zojax.tutorial глава 1 <http://zojax.svn.sourceforge.net/viewvc/zojax/sources/zojax.tutorial/branches/step1/src/zojax/tutorial/>`_

* `Исходный код zojax.content.type <http://zojax.svn.sourceforge.net/viewvc/zojax/sources/zojax.content.type/trunk/>`_
