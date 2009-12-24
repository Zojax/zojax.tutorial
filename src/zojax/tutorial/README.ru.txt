================
Добавление форм
================

Эта глава содержит информацию о том как добавлять свои 
формы для контентных типов. 


Описание
=========

По умолчанию zojax.content создает форму добывления конента и 
форму редактирования. Для этого используется параметр `schema` из 
директивы регистрации типа `zojax:content`.


Переопределение формы добавления
===================================

При регестрации конентного типа создается уникальный интерфейс.
Получить доступ к интерфейсу можно так "zojax.content.`имя контетного типа`".
Т.е. для того чтобы переопределить форму добавления для `zojax.tutorial.Topic`
мы должны зарегестрировать browser:page с именем `index.html` для созданного
интерфейса.::

    <browser:page
       name="index.html"
       for="zojax.content.zojax_tutorial_Topic"
       class=".topicadd.AddTopicForm"
       permission="zojax.AddContent" />


Для нашего MessageBoard мы изменим форму добавления Topic. 
Одновременно с добавление топика мы будем добавлять первое сообщение
топика::

from zope.component import getUtility
from zojax.content.interfaces import IContentType
from zojax.content.browser.form import Fields, AddForm

from zojax.tutorial.interfaces import ITopic, IMessage


class AddTopicForm(AddForm):

    fields = Fields(ITopic, IMessage['body'])

    def create(self, data):
        topic = self.context.create(
            data.get('title'), data.get('description'))

        messageType = getUtility(IContentType, 'zojax.tutorial.Message')

        message = messageType.create(data['title'])
        message.body = data['body']
        self._message = message

        return topic

    def add(self, object):
        topic = super(AddTopicForm, self).add(object)
        
        topic[topic.nextId] = self._message
        return topic


Мы не можем добавить `message` на этапе создания топика, так как 
топик еще не сохранен в ZODB и мы получим `NotYet` exception.
Поэтому нам приходится переопределять `add` метот тоже.
Замете что контекст для этой формы будет IContentType object, который
содержит информацию о нашем типе и важные служебные методы.

Для более детальной информации о формах сморите документацию 
для пакета z3c.form


Форма редактирования
======================

Форма редактирвания ничем не отличатся от стандартных `browser:page`
вам просто нужно переопределить `browser:page` с именем `edit.html` 
для вашего контента.


Browser pages
=============

Для всех `page` мы используем BrowserPagelet из пакета zojax.layout
Вот краткое определение интерфейса IBrowserPagelet::

  class IPagelet(IBrowserPage):
      """ pagelet """

      def update():
          """Update the pagelet data."""

      def render():
          """Render the pagelet content w/o o-wrap."""

      def __call__():
          """ render pagelet """


update
  Этот метот вызывается перед всеми остальными, этот метот можно 
  использовать для инициализации `view`. На этапе вызова доступны 
  два атрибута `context` и `request`

render
  Этот метод вызавется для рендеринга этого `view`. Т.е. этот метод
  должен возвращать отрендеренный `view` без использования внешних 
  templates.

__call__
  Это последний этап, отрендеренный `view` оборачивается внешним template.
  В большинстве случаев переопределять этот метод не нужно.


Общий вид `browser:page` будет таким::

  from zope.app.pagetemplate import ViewPageTemplateFile
  from zojax.layout.pagelet import BrowserPagelet

  class MyView(BrowserPagelet):

     template = ViewPageTemplateFile('template.pt')

     def update(self):
        # Ваш код инициализации

     def render(self):
        return self.template()


Вот так выглядит `index.html` для сообщения::

    from zope import interface
    from zojax.layout.pagelet import BrowserPagelet
    from zojax.tutorial.interfaces import IMessage

    class MessageView(BrowserPagelet):
  
        def render(self):
            return IMessage['body'].render(self.context)


и регистрация::

   <browser:page
       name="index.html"
       for="..interfaces.IMessage"
       class=".message.MessageView"
       permission="zope.View" />


Т.е. `render` возвращает только `body` сообщения. При такой системе 
мы може использовать одни и теже `views` в разных views. 
И для отрисовки топика мы можем импользовать index.html view для сообщения::

  <tal:block tal:define="context topic/values">
    <h1 tal:content="context/title">Title</h1>

    <tal:block content="structure context/@@index.html/render" />
  </tal:block>
