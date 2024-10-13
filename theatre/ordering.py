from rest_framework.request import Request

class PerformancePlayOrdering:
    ordering_param = "ordering"
    default_param = "id"

    @classmethod
    def get_ordering_fields(cls, request: Request, fields: list[str]) -> list[str]:
        ordering = request.query_params.get(cls.ordering_param, cls.default_param)
        ordering_fields = ordering.split(",")
        all_fields = set(["-" + field for field in fields] + fields)
        processed_ordering_fields = [field for field in ordering_fields if field in all_fields]
        if not processed_ordering_fields:
            return [cls.default_param]
        return processed_ordering_fields
