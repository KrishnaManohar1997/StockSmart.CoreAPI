import csv
from os.path import exists
from typing import Optional
from uuid import UUID

import django.utils.timezone as dj_datetime
import structlog
from pydantic import BaseModel

from common.base_view import PublicBaseView

logger = structlog.getLogger("django.server")
LEAD_DETAILS_CSV = "lead_details.csv"


class LeadDetails(BaseModel):
    lead_id: int
    status: str
    user_id: Optional[UUID]
    timestamp = str(dj_datetime.now())


class SmallcaseAccountLeadView(PublicBaseView):
    def post(self, request):
        lead_details = request.data
        if not lead_details:
            return self.bad_request_response("Invalid Lead Details")
        try:
            lead_obj = LeadDetails(**lead_details)
        except Exception as e:
            logger.info(f"Wrong Lead details {e}")
            return self.bad_request_response("Invalid Lead Details")
        lead_dict = lead_obj.dict()

        file_mode = "a" if exists(LEAD_DETAILS_CSV) else "w"
        # writing to csv file
        with open(LEAD_DETAILS_CSV, file_mode, newline="") as csvfile:
            # creating a csv dict writer object
            writer = csv.writer(csvfile)
            if file_mode == "w":
                writer.writerow(lead_dict.keys())
            # writing data rows
            writer.writerow(lead_dict.values())

        return self.data_response("Ok", "")
