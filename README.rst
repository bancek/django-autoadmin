Django Autoadmin
================

Django Autoadmin is Django application that let's you have quick administration over your Django models. You can even use it to fake Django Auth when your're unable to create auth tables in your legacy database. You can also use AutoDatabrowser.

Installation
------------

#. Add ``autoadmin`` directory to your Python path.

#. Add ``autoadmin`` to ``INSTALLED_APPS`` in your ``settings.py`` file.

#. Add your application(s) to ``AUTOADMIN_APPS`` list in ``settings.py``.
   For example::

    AUTOADMIN_APPS = (
        'app1',
        'app2',
    )

Configuration
-------------

To use AutoDatabrowser add your application(s) to ``AUTOADMIN_BROWSER_APPS``.
For example::

    AUTOADMIN_BROWSER_APPS = (
        'app1',
    )

To use FakeAuth set ``AUTOADMIN_FAKEAUTH`` to ``True``. This will fake authentication backend to Django so you can login to your admin.

If you want to protect your admin, you can use ``AUTOADMIN_FAKEAUTH_USERNAME`` and ``AUTOADMIN_FAKEAUTH_PASSWORD``.

If you are already using ContentType app, you can disable fake ContentType by setting ``AUTOADMIN_FAKECONTENTTYPE`` to ``False``

Admin.py generator
------------------

To customize your admin you can generate admin.py file for your application.

  python manage.py gen_modeladmins your_app

  python manage.py gen_modeladmins your_app > your_app/admin.py
