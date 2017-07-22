from . import Job
from ..database.query import Query
from flask import request
from flask_restful import Resource


class JobItem(Resource):
    """Job model item endpoint."""

    def get(self, job_id):
        """Gets a model given its id and outputs the serialized version."""
        job = Query.get_item_or_abort(Job, job_id, None)

        return job.serialize()


class JobIndex(Resource):
    """Job model index endpoint."""

    def get(self):
        """Outputs a serialized, paginated collection of models."""
        page = request.args.get('page', Query.DEFAULT_PAGE)
        max_results = request.args.get(
            'max_results', Query.DEFAULT_MAX_RESULTS)
        sort = request.args.get('sort', Query.DEFAULT_SORT)
        sort_direction = Query.get_sort_attribute(Job, sort)
        search = request.args.get('search', Query.DEFAULT_SEARCH)

        jobs = Job.get_permitted_models(
            None, sort_direction, page, max_results, search)

        return {
            'total': jobs['total'],
            'items': Job.serialize_list(jobs['items'])
        }
