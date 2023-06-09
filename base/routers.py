class MainDBRouter:
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read attribute models go to administration.
        """
        if model._meta.app_label == 'construct':
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write attribute models go to administration.
        """
        if model._meta.app_label == 'construct':
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'construct' or \
           obj2._meta.app_label == 'construct':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'administration'
        database.
        """
        if app_label == 'construct':
            return db == 'default'
        return None