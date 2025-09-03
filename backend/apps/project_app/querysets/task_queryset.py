from apps.core.querysets import BaseQuerySet


class TaskQuerySet(BaseQuerySet):

    def get_tasks_by_project(self, project_id):
        query = self.filter(project_id=project_id)
        return query
