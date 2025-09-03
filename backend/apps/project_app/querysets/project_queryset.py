from apps.core.querysets import BaseQuerySet
from apps.core.choices import Roles

class ProjectQuerySet(BaseQuerySet):

    def get_user_projects(self, user):
        query = query.all()
        if user.role != Roles.ADMIN:
            query = query.filter(assignees__in=[user])
        return query.distinct()
