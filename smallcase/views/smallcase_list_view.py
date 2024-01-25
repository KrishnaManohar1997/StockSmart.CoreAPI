from django.core.cache import cache

from common.base_view import PublicBaseView
from smallcase.serializers import AllSmallcaseSerializer
from smallcase.services import SmallcaseService


class SmallcaseListView(PublicBaseView):
    smallcase_service = SmallcaseService()
    serializer = AllSmallcaseSerializer
    CACHE_KEY = "SMALLCASE_LIST"
    CACHE_TTL = 10_800

    def get(self, request):
        smallcases = cache.get(self.CACHE_KEY)
        if smallcases:
            return self.data_response(message="Smallcases", data=smallcases)
        smallcase_queryset = self.smallcase_service.get_all_smallcases()
        smallcases_data = self.serializer(smallcase_queryset, many=True).data
        cache.set(
            self.CACHE_KEY,
            smallcases_data,
            timeout=self.CACHE_TTL,
        )
        return self.data_response(message="Smallcases", data=smallcases_data)
