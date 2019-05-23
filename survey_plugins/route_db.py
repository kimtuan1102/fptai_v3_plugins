class AuthRouter:
    """
    A router to control all database operations on models in the
    auth application.
    """

    def db_for_read(self, model, **hints):
        """
        Cho phep doc co so du lieu auth_db khi ung dung truy cap vao cac model 'user', 'logentry', 'session', 'contenttype'
        """
        auth_model_list = ('user', 'logentry', 'session', 'contenttype',)
        if model._meta.model_name in auth_model_list:
            return 'auth_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Cho phep ghi co so du lieu auth_db khi ung dung truy cap vao cac model 'user', 'logentry', 'session', 'contenttype'
        """
        auth_model_list = ('user', 'logentry', 'session', 'contenttype')
        if model._meta.model_name in auth_model_list:
            return 'auth_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Cho phep quan he co so du lieu khi ung dung su dung model 'user'
        """
        if obj1._meta.model_name == 'user' or \
           obj2._meta.model_name == 'user':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label == 'admin':
            return db == 'auth_db'
        return None


class SurveyRouter:

    def db_for_read(self, model, **hints):
        """
        Cho phep doc co so du lieu survey_db neu khong su dung co so du lieu auth_db
        """
        return 'survey_db'

    def db_for_write(self, model, **hints):
        """
        Cho phep ghi co so du lieu survey_db neu khong su dung co so du lieu auth_db
        """
        return 'survey_db'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Cho phep quan he tren co so du lieu neu app la surveyapi
        """
        if obj1._meta.app_label == 'survey_plugins' or \
                obj2._meta.app_label == 'survey_plugins':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Cho phep migrate co so du lieu neu khong su dung co so du lieu auth_db
        """
        return True