from fastapi import FastAPI, Response, status, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

import api.db as DB

from api.table_names import TABLE_NAMES as TABLE_NAMES

from api import queries as QUERY

import re
import json

from typing import Optional,List,Annotated

from pydantic import BaseModel, Field
   
from datetime import datetime    
from datetime import date
from datetime import time
    
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=['*']
)
    
@app.get('/db',tags=['db'],description="Get the Open Knesset's database table names and their columns")
async def db_tables(request: Request,
    limit: int = 0,
    offset: int = 0
    ):
    table_columns={}
    tables = DB.get_data_tables(limit, offset)
    for table in tables:
        table_name = table['table_name']
        columns = DB.get_data_columns(table_name)
        column_names = [column['column_name'] for column in columns]
        table_columns[table_name] = column_names

    result = {'success': True, 'data': table_columns}
    return result


# Route for list"bills_kns_billunion" table
@app.get("/bills_kns_billunion/list", status_code=200,tags=['bills_kns_billunion'])
async def get_billunion_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    MainBillID: Optional[int] = None,
    UnionBillID: Optional[int] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM bills_kns_billunion"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "bills_kns_billunion" table
@app.get('/bills_kns_billunion/{BillUnionID}',tags=['bills_kns_billunion'])
async def get_bill_union(BillUnionID: int):
    data = DB.get_single_data('bills_kns_billunion', 'BillUnionID', BillUnionID)
    return {'success': True, 'data': data}
     
 
# Route for list knesset_kns_govministry table
@app.get("/knesset_kns_govministry/list", status_code=200,tags=["knesset_kns_govministry"])
async def get_govministry_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    Name: Optional[str] = None,
    IsActive: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM knesset_kns_govministry"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "knesset_kns_govministry" table
@app.get('/knesset_kns_govministry/{GovMinistryID}',tags=["knesset_kns_govministry"])
async def get_gov_ministry(GovMinistryID: int):
    data = DB.get_single_data('knesset_kns_govministry', 'GovMinistryID', GovMinistryID)
    return {'success': True, 'data': data}

# Route for list plenum_kns_documentplenumsession table
@app.get("/plenum_kns_documentplenumsession/list", status_code=200,tags=["plenum_kns_documentplenumsession"])
async def get_documentplenumsession_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    PlenumSessionID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM plenum_kns_documentplenumsession"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}


# Route for single "plenum_kns_documentplenumsession" table
@app.get('/plenum_kns_documentplenumsession/{DocumentPlenumSessionID}',tags=["plenum_kns_documentplenumsession"])
async def get_document_plenum_session(DocumentPlenumSessionID: int):
    data = DB.get_single_data('plenum_kns_documentplenumsession', 'DocumentPlenumSessionID', DocumentPlenumSessionID)
    return {'success': True, 'data': data}
    
# Route for list members_mk_individual_faction_chairpersons table
@app.get("/members_mk_individual_faction_chairpersons/list", status_code=200,tags=["members_mk_individual_faction_chairpersons"])
async def get_faction_chairpersons_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    faction_id: Optional[int] = None,
    faction_name: Optional[str] = None,
    start_date: Optional[date] = None,
    finish_date: Optional[date] = None,
    knesset: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_mk_individual_faction_chairpersons"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for "members_mk_individual_faction_chairpersons" table
@app.get('/members_mk_individual_faction_chairpersons/{mk_individual_id}',tags=["members_mk_individual_faction_chairpersons"])
async def get_faction_chairperson(mk_individual_id: int):
    data = DB.get_single_data('members_mk_individual_faction_chairpersons', 'mk_individual_id', mk_individual_id)
    return {'success': True, 'data': data}
    
# Route for list members_mk_individual_govministries table
@app.get("/members_mk_individual_govministries/list", status_code=200,tags=["members_mk_individual_govministries"])
async def get_individual_govministries_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    govministry_id: Optional[int] = None,
    govministry_name: Optional[str] = None,
    position_id: Optional[int] = None,
    position_name: Optional[str] = None,
    start_date: Optional[date] = None,
    finish_date: Optional[date] = None,
    knesset: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_mk_individual_govministries"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}    

# Route for single "members_mk_individual_govministries" table
@app.get('/members_mk_individual_govministries/{mk_individual_id}',tags=["members_mk_individual_govministries"])
async def get_gov_ministry_member(mk_individual_id: int):
    data = DB.get_single_data('members_mk_individual_govministries', 'mk_individual_id', mk_individual_id)
    return {'success': True, 'data': data}
    
# Route for list bills_kns_billsplit table
@app.get("/bills_kns_billsplit/list", status_code=200,tags=["bills_kns_billsplit"])
async def get_billsplit_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    MainBillID: Optional[int] = None,
    SplitBillID: Optional[int] = None,
    Name: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM bills_kns_billsplit"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for "bills_kns_billsplit" table
@app.get('/bills_kns_billsplit/{BillSplitID}',tags=["bills_kns_billsplit"])
async def get_bill_split(BillSplitID: int):
    data = DB.get_single_data('bills_kns_billsplit', 'BillSplitID', BillSplitID)
    return {'success': True, 'data': data}
    
# Route for list bills_kns_billinitiator table
@app.get("/bills_kns_billinitiator/list", status_code=200,tags=["bills_kns_billinitiator"])
async def get_billinitiator_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    BillID: Optional[int] = None,
    PersonID: Optional[int] = None,
    IsInitiator: Optional[bool] = None,
    Ordinal: Optional[int] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM bills_kns_billinitiator"
    data = DB.get_data_list(query, limit, offset,order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}   

# Route for single "bills_kns_billinitiator" table
@app.get('/bills_kns_billinitiator/{BillInitiatorID}',tags=["bills_kns_billinitiator"])
async def get_bill_initiator(BillInitiatorID: int):
    data = DB.get_single_data('bills_kns_billinitiator', 'BillInitiatorID', BillInitiatorID)
    return {'success': True, 'data': data}
    
# Route for list people_plenum_session_voters_stats table
@app.get("/people_plenum_session_voters_stats/list", status_code=200,tags=["people_plenum_session_voters_stats"])
async def get_voters_stats_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    knesset: Optional[int] = None,
    plenum: Optional[int] = None,
    assembly: Optional[int] = None,
    pagra: Optional[int] = None,
    faction_id: Optional[int] = None,
    mk_id: Optional[int] = None,
    voted_sessions: Optional[int] = None,
    total_sessions: Optional[int] = None,
    voted_sessions_percent: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_plenum_session_voters_stats"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}
    
# Route for list bills_kns_billname table
@app.get("/bills_kns_billname/list", status_code=200,tags=["bills_kns_billname"])
async def get_billname_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    BillID: Optional[int] = None,
    Name: Optional[str] = None,
    NameHistoryTypeID: Optional[int] = None,
    NameHistoryTypeDesc: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM bills_kns_billname"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}
    
# Route for list members_mk_individual_committees table
@app.get("/members_mk_individual_committees/list", status_code=200,tags=["members_mk_individual_committees"])
async def get_individual_committees_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    mk_individual_id: Optional[int] = None,
    committee_id: Optional[int] = None,
    committee_name: Optional[str] = None,
    position_id: Optional[int] = None,
    position_name: Optional[str] = None,
    start_date: Optional[date] = None,
    finish_date: Optional[date] = None,
    knesset: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_mk_individual_committees"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}    
    
# Route for list votes_view_vote_rslts_hdr_approved table
@app.get("/votes_view_vote_rslts_hdr_approved/list", status_code=200,tags=["votes_view_vote_rslts_hdr_approved"])
async def get_vote_rslts_hdr_approved_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    knesset_num: Optional[int] = None,
    session_id: Optional[int] = None,
    sess_item_nbr: Optional[int] = None,
    sess_item_id: Optional[int] = None,
    sess_item_dscr: Optional[str] = None,
    vote_item_id: Optional[int] = None,
    vote_item_dscr: Optional[str] = None,
    vote_date: Optional[date] = None,
    vote_time: Optional[time] = None,
    is_elctrnc_vote: Optional[int] = Query(None, ge=0, le=1),
    vote_type: Optional[int] = None,
    is_accepted: Optional[int] = None,
    total_for: Optional[int] = None,
    total_against: Optional[int] = None,
    total_abstain: Optional[int] = None,
    vote_stat: Optional[int] = None,
    session_num: Optional[int] = None,
    vote_nbr_in_sess: Optional[int] = None,
    reason: Optional[int] = None,
    modifier: Optional[str] = None,
    remark: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM votes_view_vote_rslts_hdr_approved"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "votes_view_vote_rslts_hdr_approved" table
@app.get('/votes_view_vote_rslts_hdr_approved/{id}',tags=["votes_view_vote_rslts_hdr_approved"])
async def get_voter_result(id: int):
    data = DB.get_single_data('votes_view_vote_rslts_hdr_approved', 'id', id)
    return {'success': True, 'data': data}
    
# Route for list committees_kns_documentcommitteesession_dataservice table
@app.get("/committees_kns_documentcommitteesession_dataservice/list", status_code=200,tags=["committees_kns_documentcommitteesession_dataservice"])
async def get_documentcommitteesession_dataservice_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_kns_documentcommitteesession_dataservice"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "committees_kns_documentcommitteesession_dataservice" table
@app.get('/committees_kns_documentcommitteesession_dataservice/{DocumentCommitteeSessionID}',tags=["committees_kns_documentcommitteesession_dataservice"])
async def get_document_committee_session(DocumentCommitteeSessionID: int):
    data = DB.get_single_data('committees_kns_documentcommitteesession_dataservice', 'DocumentCommitteeSessionID', DocumentCommitteeSessionID)
    return {'success': True, 'data': data}
    
# Route for list committees_kns_jointcommittee table
@app.get("/committees_kns_jointcommittee/list", status_code=200,tags=["committees_kns_jointcommittee"])
async def get_jointcommittee_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeID: Optional[int] = None,
    ParticipantCommitteeID: Optional[int] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_kns_jointcommittee"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "committees_kns_jointcommittee" table
@app.get('/committees_kns_jointcommittee/{JointCommitteeID}',tags=["committees_kns_jointcommittee"])
async def get_joint_committee(JointCommitteeID: int):
    data = DB.get_single_data('committees_kns_jointcommittee', 'JointCommitteeID', JointCommitteeID)
    return {'success': True, 'data': data}
    
# Route for list votes_vote_rslts_kmmbr_shadow_extra table
@app.get("/votes_vote_rslts_kmmbr_shadow_extra/list", status_code=200,tags=["votes_vote_rslts_kmmbr_shadow_extra"])
async def get_vote_rslts_kmmbr_shadow_extra_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    vote_id: Optional[int] = None,
    kmmbr_id: Optional[int] = None,
    kmmbr_name: Optional[str] = None,
    vote_result: Optional[int] = None,
    knesset_num: Optional[int] = None,
    faction_id: Optional[int] = None,
    faction_name: Optional[str] = None,
    reason: Optional[int] = None,
    modifier: Optional[str] = None,
    remark: Optional[str] = None,
    result_type_name: Optional[str] = None,
    mk_individual_id: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM votes_vote_rslts_kmmbr_shadow_extra"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}
    
# Route for list plenum_kns_plenumsession table
@app.get("/plenum_kns_plenumsession/list", status_code=200,tags=["plenum_kns_plenumsession"])
async def get_plenumsession_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    PlenumSessionID: Optional[int] = None,
    Number: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    Name: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    IsSpecialMeeting: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM plenum_kns_plenumsession"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}


# Route for "plenum_kns_plenumsession" table
@app.get('/bills_kns_plenumsession/{PlenumSessionID}',tags=["plenum_kns_plenumsession"])
async def get_plenum_session(PlenumSessionID: int):
    data = DB.get_single_data('plenum_kns_plenumsession', 'PlenumSessionID', PlenumSessionID)
    return {'success': True, 'data': data}
    
# Route for list bills_kns_documentbill table
@app.get("/bills_kns_documentbill/list", status_code=200,tags=["bills_kns_documentbill"])
async def get_documentbill_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    BillID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM bills_kns_documentbill"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "bills_kns_documentbill" table
@app.get('/bills_kns_documentbill/{DocumentBillID}',tags=["bills_kns_documentbill"])
async def get_document_bill(DocumentBillID: int):
    data = DB.get_single_data('bills_kns_documentbill', 'DocumentBillID', DocumentBillID)
    return {'success': True, 'data': data}
    
# Route for list bills_kns_bill__airflow table
@app.get("/bills_kns_bill__airflow/list", status_code=200,tags=["bills_kns_bill__airflow"])
async def get_bill__airflow_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    KnessetNum: Optional[int] = None,
    Name: Optional[str] = None,
    SubTypeID: Optional[int] = None,
    SubTypeDesc: Optional[str] = None,
    PrivateNumber: Optional[int] = None,
    CommitteeID: Optional[int] = None,
    StatusID: Optional[int] = None,
    Number: Optional[int] = None,
    PostponementReasonID: Optional[int] = None,
    PostponementReasonDesc: Optional[str] = None,
    PublicationDate: Optional[datetime] = None,
    MagazineNumber: Optional[int] = None,
    PageNumber: Optional[int] = None,
    IsContinuationBill: Optional[bool] = None,
    SummaryLaw: Optional[str] = None,
    PublicationSeriesID: Optional[int] = None,
    PublicationSeriesDesc: Optional[str] = None,
    PublicationSeriesFirstCall: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM bills_kns_bill__airflow"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "bills_kns_bill__airflow" table
@app.get('/bills_kns_bill__airflow/{BillID}',tags=["bills_kns_bill__airflow"])
async def get_bill_airflow(BillID: int):
    data = DB.get_single_data('bills_kns_bill__airflow', 'BillID', BillID)
    return {'success': True, 'data': data}
    
# Route for list members_presence table
@app.get("/members_presence/list", status_code=200,tags=["members_presence"])
async def get_members_presence_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    mk_id: Optional[int] = None,
    mk_name: Optional[str] = None,
    date: Optional[date] = None,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    year_week_number: Optional[int] = None,
    total_attended_hours: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_presence"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for list committees_kns_committee__airflow table
@app.get("/committees_kns_committee__airflow/list", status_code=200,tags=["committees_kns_committee__airflow"])
async def get_committee__airflow_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    Name: Optional[str] = None,
    CategoryID: Optional[int] = None,
    CategoryDesc: Optional[str] = None,
    KnessetNum: Optional[int] = None,
    CommitteeTypeID: Optional[int] = None,
    CommitteeTypeDesc: Optional[str] = None,
    Email: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    AdditionalTypeID: Optional[int] = None,
    AdditionalTypeDesc: Optional[str] = None,
    ParentCommitteeID: Optional[int] = None,
    CommitteeParentName: Optional[str] = None,
    IsCurrent: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_kns_committee__airflow"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "committees_kns_committee__airflow" table
@app.get('/committees_kns_committee__airflow/{CommitteeID}',tags=["committees_kns_committee__airflow"])
async def get_single_data_airflow(CommitteeID: int):
    data = DB.get_single_data('committees_kns_committee__airflow', 'CommitteeID', CommitteeID)
    return {'success': True, 'data': data}
    
# Route for list committees_build_build_meetings table
@app.get("/committees_build_build_meetings/list", status_code=200,tags=["committees_build_build_meetings"])
async def get_build_meetings_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    Number: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    TypeID: Optional[int] = None,
    TypeDesc: Optional[str] = None,
    CommitteeID: Optional[int] = None,
    Location: Optional[str] = None,
    SessionUrl: Optional[str] = None,
    BroadcastUrl: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    Note: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    protocol_extension: Optional[str] = None,
    text_filename: Optional[str] = None,
    parts_filename: Optional[str] = None,
    topics: Optional[str] = None,
    mks: Optional[str] = None,
    invitees_name: Optional[str] = None,
    invitees_role: Optional[str] = None,
    legal_advisors: Optional[str] = None,
    manager: Optional[str] = None,
    attended_mk_individual_ids: List[int] = Query([], alias="attended_mk_individual_ids",example=[736], list=True)
):            
    query_params = request.query_params.items()
    qs_parts = []
    arrays_number_val=[attended_mk_individual_ids]
    arrays_number_names=["attended_mk_individual_ids"]
    arrays_val=[[topics],[mks],[legal_advisors],[manager]]
    arrays_name = ["topics","mks","legal_advisors","manager"] 
    objects_val=[invitees_name,invitees_role]
    objects_name=["invitees_name","invitees_role"]        
    for key, value in query_params:
        if key in arrays_number_names:
            elemts=arrays_number_val[arrays_number_names.index(key)]  
            qs_parts.append(f"{key}={elemts}")    
        elif key not in ['limit', 'offset', 'order_by'] and key not in arrays_name and key not in objects_name:
            qs_parts.append(f"{key}={value}")
    
    for name, val in zip(arrays_name, arrays_val):
        if val[0]:
            qs_parts.append(f"{name}={val}")
    for name, val in zip(objects_name, objects_val):
        if val:
            qs_parts.append(f"{name}=<{val}>")    
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_build_build_meetings"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "committees_build_build_meetings" table
@app.get('/committees_build_build_meetings/{CommitteeSessionID}',tags=["committees_build_build_meetings"])
async def get_build_meeting(CommitteeSessionID: int):
    data = DB.get_single_data('committees_build_build_meetings', 'CommitteeSessionID', CommitteeSessionID)
    return {'success': True, 'data': data}
    
# Route for list people_committees_joined_meetings table
@app.get("/people_committees_joined_meetings/list", status_code=200,tags=["people_committees_joined_meetings"])
async def get_committees_joined_meetings_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    Number: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    TypeID: Optional[int] = None,
    TypeDesc: Optional[str] = None,
    CommitteeID: Optional[int] = None,
    Location: Optional[str] = None,
    SessionUrl: Optional[str] = None,
    BroadcastUrl: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    Note: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    text_file_name: Optional[str] = None,
    text_file_size: Optional[int] = None,
    topics: List[str] = Query([], alias="topics",example=['שינויים בתקציב לשנת 2003'], list=True),
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays=[topics]
    var_names = ["topics"]
    for key, value in query_params:
        if key in var_names:
            elemts=arrays[var_names.index(key)]  
            qs_parts.append(f"{key}={elemts}")    
        elif key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")   
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_committees_joined_meetings"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "people_committees_joined_meetings" table
@app.get('/people_committees_joined_meetings/{CommitteeSessionID}',tags=["people_committees_joined_meetings"])
async def get_joined_meeting(CommitteeSessionID: int):
    data = DB.get_single_data('people_committees_joined_meetings', 'CommitteeSessionID', CommitteeSessionID)
    return {'success': True, 'data': data}
    
# Route for list bills_kns_billhistoryinitiator table
@app.get("/bills_kns_billhistoryinitiator/list", status_code=200,tags=["bills_kns_billhistoryinitiator"])
async def get_billhistoryinitiator_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    BillID: Optional[int] = None,
    PersonID: Optional[int] = None,
    IsInitiator: Optional[bool] = None,
    StartDate: Optional[datetime] = None,
    EndDate: Optional[datetime] = None,
    ReasonID: Optional[int] = None,
    ReasonDesc: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM bills_kns_billhistoryinitiator"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "bills_kns_billhistoryinitiator" table
@app.get('/bills_kns_billhistoryinitiator/{BillHistoryInitiatorID}',tags=["bills_kns_billhistoryinitiator"])
async def get_bill_history_initiator(BillHistoryInitiatorID: int):
    data = DB.get_single_data('bills_kns_billhistoryinitiator', 'BillHistoryInitiatorID', BillHistoryInitiatorID)
    return {'success': True, 'data': data}
    
# Route for list committees_document_background_material_titles table
@app.get("/committees_document_background_material_titles/list", status_code=200,tags=["committees_document_background_material_titles"])
async def get_document_background_material_titles_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    CommitteeID: Optional[int] = None,
    FilePath: Optional[str] = None,
    title: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_document_background_material_titles"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "committees_document_background_material_titles" table
@app.get('/committees_document_background_material_titles/{DocumentCommitteeSessionID}',tags=["committees_document_background_material_titles"])
async def get_background_material_title(DocumentCommitteeSessionID: int):
    data = DB.get_single_data('committees_document_background_material_titles', 'DocumentCommitteeSessionID', DocumentCommitteeSessionID)
    return {'success': True, 'data': data}
    
# Route for list people_committees_meeting_attendees table
@app.get("/people_committees_meeting_attendees/list", status_code=200,tags=["people_committees_meeting_attendees"])
async def get_committees_meeting_attendees_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    Number: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    TypeID: Optional[int] = None,
    TypeDesc: Optional[str] = None,
    CommitteeID: Optional[int] = None,
    Location: Optional[str] = None,
    SessionUrl: Optional[str] = None,
    BroadcastUrl: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    Note: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    download_crc32c: Optional[str] = None,
    download_filename: Optional[str] = None,
    download_filesize: Optional[int] = None,
    parts_crc32c: Optional[str] = None,
    parts_filesize: Optional[int] = None,
    parts_parsed_filename: Optional[str] = None,
    text_crc32c: Optional[str] = None,
    text_filesize: Optional[int] = None,
    text_parsed_filename: Optional[str] = None,
    item_ids: List[int] = Query([], alias="item_ids",example=[74814], list=True),
    item_type_ids: List[int] = Query([], alias="item_type_ids",example=[11], list=True),
    topics: Optional[str] = None,
    committee_name: Optional[str] = None,
    bill_names: Optional[str] = None,
    bill_types: Optional[str] = None,
    related_to_legislation: Optional[bool] = None,
    mks: Optional[str] = None,
    invitees_name: Optional[str] = None,
    legal_advisors: Optional[str] = None,
    manager: Optional[str] = None,
    financial_advisors: Optional[str] = None,
    attended_mk_individual_ids: List[int] = Query([], alias="attended_mk_individual_ids",example=[], list=True)
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays_number_val=[item_ids,item_type_ids,attended_mk_individual_ids]
    arrays_number_names=["item_ids","item_type_ids","attended_mk_individual_ids"]
    arrays_val=[[topics],[bill_names],[bill_types],[mks],[legal_advisors],[manager],[financial_advisors]]
    arrays_name = ["topics","bill_names","bill_types","mks","legal_advisors","manager","financial_advisors"] 
    objects_val=[invitees_name]
    objects_name=["invitees_name"]        
    for key, value in query_params:
        if key in arrays_number_names:
            elemts=arrays_number_val[arrays_number_names.index(key)]  
            qs_parts.append(f"{key}={elemts}")    
        elif key not in ['limit', 'offset', 'order_by'] and key not in arrays_name and key not in objects_name:
            qs_parts.append(f"{key}={value}")
    
    for name, val in zip(arrays_name, arrays_val):
        if val[0]:
            qs_parts.append(f"{name}={val}")
    for name, val in zip(objects_name, objects_val):
        if val:
            qs_parts.append(f"{name}=<{val}>")    
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_committees_meeting_attendees"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "people_committees_meeting_attendees" table
@app.get('/people_committees_meeting_attendees/{CommitteeSessionID}',tags=["people_committees_meeting_attendees"])
async def get_meeting_attendees(CommitteeSessionID: int):
    data = DB.get_single_data('people_committees_meeting_attendees', 'CommitteeSessionID', CommitteeSessionID)
    return {'success': True, 'data': data}
    
# Route for list knesset_kns_knessetdates table
@app.get("/knesset_kns_knessetdates/list", status_code=200,tags=["knesset_kns_knessetdates"])
async def get_knessetdates_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    KnessetNum: Optional[int] = None,
    Name: Optional[str] = None,
    Assembly: Optional[int] = None,
    Plenum: Optional[int] = None,
    PlenumStart: Optional[str] = None,
    PlenumFinish: Optional[str] = None,
    IsCurrent: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM knesset_kns_knessetdates"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "knesset_kns_knessetdates" table
@app.get('/knesset_kns_knessetdates/{KnessetDateID}',tags=["knesset_kns_knessetdates"])
async def get_knesset_dates(KnessetDateID: int):
    data = DB.get_single_data('knesset_kns_knessetdates', 'KnessetDateID', KnessetDateID)
    return {'success': True, 'data': data}
    
# Route for list votes_view_vote_mk_individual table
@app.get("/votes_view_vote_mk_individual/list", status_code=200,tags=["votes_view_vote_mk_individual"])
async def get_vote_mk_individual_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    mk_individual_id: Optional[int] = None,
    mk_individual_name: Optional[str] = None,
    mk_individual_name_eng: Optional[str] = None,
    mk_individual_first_name: Optional[str] = None,
    mk_individual_first_name_eng: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM votes_view_vote_mk_individual"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "votes_view_vote_mk_individual" table
@app.get('/votes_view_vote_mk_individual/{vip_id}',tags=["votes_view_vote_mk_individual"])
async def get_vote_mk_individual(vip_id: int):
    data = DB.get_single_data('votes_view_vote_mk_individual', 'vip_id', vip_id)
    return {'success': True, 'data': data}
    
# Route for list bills_kns_bill table
@app.get("/bills_kns_bill/list", status_code=200,tags=["bills_kns_bill"])
async def get_bill_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    KnessetNum: Optional[int] = None,
    Name: Optional[str] = None,
    SubTypeID: Optional[int] = None,
    SubTypeDesc: Optional[str] = None,
    PrivateNumber: Optional[int] = None,
    CommitteeID: Optional[int] = None,
    StatusID: Optional[int] = None,
    Number: Optional[int] = None,
    PostponementReasonID: Optional[int] = None,
    PostponementReasonDesc: Optional[str] = None,
    PublicationDate: Optional[datetime] = None,
    MagazineNumber: Optional[int] = None,
    PageNumber: Optional[int] = None,
    IsContinuationBill: Optional[bool] = None,
    SummaryLaw: Optional[str] = None,
    PublicationSeriesID: Optional[int] = None,
    PublicationSeriesDesc: Optional[str] = None,
    PublicationSeriesFirstCall: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM bills_kns_bill"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}


# Route for single "bills_kns_bill" table
@app.get('/bills_kns_bill/{BillID}',tags=["bills_kns_bill"])
async def get_bill(BillID: int):
    data = DB.get_single_data('bills_kns_bill', 'BillID', BillID)
    return {'success': True, 'data': data}
    
# Route for list members_kns_person__airflow table
@app.get("/members_kns_person__airflow/list", status_code=200,tags=["members_kns_person__airflow"])
async def get_person__airflow_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    LastName: Optional[str] = None,
    FirstName: Optional[str] = None,
    GenderID: Optional[int] = None,
    GenderDesc: Optional[str] = None,
    Email: Optional[str] = None,
    IsCurrent: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_kns_person__airflow"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "members_kns_person__airflow" table
@app.get('/members_kns_person__airflow/{PersonID}',tags=["members_kns_person__airflow"])
async def get_person_airflow(PersonID: int):
    data = DB.get_single_data('members_kns_person__airflow', 'PersonID', PersonID)
    return {'success': True, 'data': data}
    
# Route for committees_joined_meetings table
@app.get("/committees_joined_meetings/list", status_code=200,tags=["committees_joined_meetings"])
async def get_joined_meetings_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    Number: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    TypeID: Optional[int] = None,
    TypeDesc: Optional[str] = None,
    CommitteeID: Optional[int] = None,
    Location: Optional[str] = None,
    SessionUrl: Optional[str] = None,
    BroadcastUrl: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    Note: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    protocol_extension: Optional[str] = None,
    text_filename: Optional[str] = None,
    parts_filename: Optional[str] = None,
    topics: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays=[[topics]]
    var_names = ["topics"]
    for key, value in query_params:
        if key in var_names:
            elemts=arrays[var_names.index(key)]  
            qs_parts.append(f"{key}={elemts}")    
        elif key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")   
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_joined_meetings"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "committees_joined_meetings" table
@app.get('/committees_joined_meetings/{CommitteeSessionID}',tags=["committees_joined_meetings"])
async def get_joined_meeting(CommitteeSessionID: int):
    data = DB.get_single_data('committees_joined_meetings', 'CommitteeSessionID', CommitteeSessionID)
    return {'success': True, 'data': data}
    
# Route for list people_mk_party_discipline_stats table
@app.get("/people_mk_party_discipline_stats/list", status_code=200,tags=["people_mk_party_discipline_stats"])
async def get_mk_party_discipline_stats_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    knesset: Optional[int] = None,
    plenum: Optional[int] = None,
    assembly: Optional[int] = None,
    pagra: Optional[int] = None,
    faction_id: Optional[int] = None,
    mk_id: Optional[int] = None,
    undisciplined_votes: Optional[int] = None,
    disciplined_votes: Optional[int] = None,
    total_votes: Optional[int] = None,
    undisciplined_votes_percent: Optional[int] = None,
    disciplined_votes_percent: Optional[int] = None
):    
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_mk_party_discipline_stats"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for list knesset_kns_status table
@app.get("/knesset_kns_status/list", status_code=200,tags=["knesset_kns_status"])
async def get_knesset_status_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    Desc: Optional[str] = None,
    TypeID: Optional[int] = None,
    TypeDesc: Optional[str] = None,
    OrderTransition: Optional[int] = None,
    IsActive: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):    
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM knesset_kns_status"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "knesset_kns_status" table
@app.get('/knesset_kns_status/{StatusID}',tags=["knesset_kns_status"])
async def get_status(StatusID: int):
    data = DB.get_single_data('knesset_kns_status', 'StatusID', StatusID)
    return {'success': True, 'data': data}
    
# Route for list votes_vote_rslts_kmmbr_shadow table
@app.get("/votes_vote_rslts_kmmbr_shadow/list", status_code=200,tags=["votes_vote_rslts_kmmbr_shadow"])
async def get_vote_rslts_kmmbr_shadow_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    vote_id: Optional[int] = None,
    kmmbr_id: Optional[int] = None,
    kmmbr_name: Optional[str] = None,
    vote_result: Optional[int] = None,
    knesset_num: Optional[int] = None,
    faction_id: Optional[int] = None,
    faction_name: Optional[str] = None,
    reason: Optional[int] = None,
    modifier: Optional[str] = None,
    remark: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM votes_vote_rslts_kmmbr_shadow"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for list people_committees_meeting_attendees_mks_full_stats table
@app.get("/people_committees_meeting_attendees_mks_full_stats/list", status_code=200,tags=["people_committees_meeting_attendees_mks_full_stats"])
async def get_attendees_mks_full_stats_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    knesset: Optional[int] = None,
    plenum: Optional[int] = None,
    assembly: Optional[int] = None,
    pagra: Optional[int] = None,
    committee_id: Optional[int] = None,
    faction_id: Optional[int] = None,
    mk_id: Optional[int] = None,
    attended_meetings: Optional[int] = None,
    protocol_meetings: Optional[int] = None,
    open_meetings: Optional[int] = None,
    attended_meetings_percent: Optional[int] = None,
    attended_meetings_relative_percent: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_committees_meeting_attendees_mks_full_stats"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for list people_committees_meeting_speaker_stats table
@app.get("/people_committees_meeting_speaker_stats/list", status_code=200,tags=["people_committees_meeting_speaker_stats"])
async def get_meeting_speaker_stats_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    parts_crc32c: Optional[str] = None,
    part_index: Optional[int] = None,
    header: Optional[str] = None,
    body_length: Optional[int] = None,
    body_num_words: Optional[int] = None,
    part_categories: Optional[str] = None,
    name_role: Optional[str] = None,
    mk_individual_id: Optional[int] = None,
    mk_individual_faction: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
             qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_committees_meeting_speaker_stats"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for list committees_kns_cmtsitecode table
@app.get("/committees_kns_cmtsitecode/list", status_code=200,tags=["committees_kns_cmtsitecode"])
async def get_cmtsitecode_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    KnsID: Optional[int] = None,
    SiteId: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_kns_cmtsitecode"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "committees_kns_cmtsitecode" table
@app.get('/committees_kns_cmtsitecode/{CmtSiteCode}',tags=["committees_kns_cmtsitecode"])
async def get_cmt_site_code(CmtSiteCode: int):
    data = DB.get_single_data('committees_kns_cmtsitecode', 'CmtSiteCode', CmtSiteCode)
    return {'success': True, 'data': data}
    
# Route for list laws_kns_document_law table
@app.get("/laws_kns_document_law/list", status_code=200,tags=["laws_kns_document_law"])
async def get_document_law_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    LawID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM laws_kns_document_law"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for "laws_kns_document_law" table
@app.get('/laws_kns_document_law/{DocumentLawID}',tags=["laws_kns_document_law"])
async def get_document_law(DocumentLawID: int):
    data = DB.get_single_data('laws_kns_document_law', 'DocumentLawID', DocumentLawID)
    return {'success': True, 'data': data}


# Route for list committees_meeting_protocols_parts table
@app.get("/committees_meeting_protocols_parts/list", status_code=200,tags=["committees_meeting_protocols_parts"])
async def get_meeting_protocols_parts_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    KnessetNum: Optional[int] = None,
    protocol_extension: Optional[str] = None,
    parsed_filename: Optional[str] = None,
    filesize: Optional[int] = None,
    crc32c: Optional[str] = None,
    error: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_meeting_protocols_parts"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "committees_meeting_protocols_parts" table
@app.get('/committees_meeting_protocols_parts/{DocumentCommitteeSessionID}',tags=["committees_meeting_protocols_parts"])
async def get_meeting_protocols_parts(DocumentCommitteeSessionID: int):
    data = DB.get_single_data('committees_meeting_protocols_parts', 'DocumentCommitteeSessionID', DocumentCommitteeSessionID)
    return {'success': True, 'data': data}
    
# Route for list votes_view_vote_rslts_hdr_approved_extra table
@app.get("/votes_view_vote_rslts_hdr_approved_extra/list", status_code=200,tags=["votes_view_vote_rslts_hdr_approved_extra"])
async def get_vote_rslts_hdr_approved_extra_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    knesset_num: Optional[int] = None,
    session_id: Optional[int] = None,
    sess_item_nbr: Optional[int] = None,
    sess_item_id: Optional[int] = None,
    sess_item_dscr: Optional[str] = None,
    vote_item_id: Optional[int] = None,
    vote_item_dscr: Optional[str] = None,
    vote_date: Optional[date] = None,
    vote_time: Optional[time] = None,
    is_elctrnc_vote: Optional[int] = None,
    vote_type: Optional[int] = None,
    is_accepted: Optional[int] = None,
    total_for: Optional[int] = None,
    total_against: Optional[int] = None,
    total_abstain: Optional[int] = None,
    vote_stat: Optional[str] = None,
    session_num: Optional[int] = None,
    vote_nbr_in_sess: Optional[int] = None,
    reason: Optional[int] = None,
    modifier: Optional[str] = None,
    remark: Optional[str] = None,
    mk_ids_pro: List[int] = Query([],example=[],list=True),
    mk_ids_against: List[int] = Query([],example=[],list=True),
    mk_ids_abstain: List[int] = Query([],example=[],list=True),
    knesset: Optional[int] = None,
    plenum: Optional[int] = None,
    assembly: Optional[int] = None,
    pagra: Optional[bool] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays=[mk_ids_pro,mk_ids_against,mk_ids_abstain]
    var_names = ["mk_ids_pro","mk_ids_against","mk_ids_abstain"]
    for key, value in query_params:
        if key in var_names:
            elemts=arrays[var_names.index(key)]  
            qs_parts.append(f"{key}={elemts}")    
        elif key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")   
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM votes_view_vote_rslts_hdr_approved_extra"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for "votes_view_vote_rslts_hdr_approved_extra" table
@app.get('/votes_view_vote_rslts_hdr_approved_extra/{id}',tags=["votes_view_vote_rslts_hdr_approved_extra"])
async def get_vote_rslts_hdr_approved_extra(id: int):
    data = DB.get_single_data('votes_view_vote_rslts_hdr_approved_extra', 'id', id)
    return {'success': True, 'data': data}
    
# Route for list committees_build_rendered_meetings_stats table
@app.get("/committees_build_rendered_meetings_stats/list", status_code=200,tags=["committees_build_rendered_meetings_stats"])
async def get_build_rendered_meetings_stats_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    num_speech_parts: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_build_rendered_meetings_stats"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "committees_build_rendered_meetings_stats" table
@app.get('/committees_build_rendered_meetings_stats/{CommitteeSessionID}',tags=["committees_build_rendered_meetings_stats"])
async def get_rendered_meetings_stats(CommitteeSessionID: int):
    data = DB.get_single_data('committees_build_rendered_meetings_stats', 'CommitteeSessionID', CommitteeSessionID)
    return {'success': True, 'data': data}
    
# Route for list plenum_kns_plmsessionitem table
@app.get("/plenum_kns_plmsessionitem/list", status_code=200,tags=["plenum_kns_plmsessionitem"])
async def get_plmsessionitem_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    ItemID: Optional[int] = None,
    PlenumSessionID: Optional[int] = None,
    ItemTypeID: Optional[int] = None,
    ItemTypeDesc: Optional[str] = None,
    Ordinal: Optional[int] = None,
    Name: Optional[str] = None,
    StatusID: Optional[int] = None,
    IsDiscussion: Optional[int] = Query(None, ge=0, le=1),
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM plenum_kns_plmsessionitem"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}    

# Route for single "plenum_kns_plmsessionitem" table
@app.get('/plenum_kns_plmsessionitem/{plmPlenumSessionID}',tags=["plenum_kns_plmsessionitem"])
async def get_plmsessionitem(plmPlenumSessionID: int):
    data = DB.get_single_data('plenum_kns_plmsessionitem', 'plmPlenumSessionID', plmPlenumSessionID)
    return {'success': True, 'data': data}
    
# Route for list lobbyists_v_lobbyist_clients table
@app.get("/lobbyists_v_lobbyist_clients/list", status_code=200,tags=["lobbyists_v_lobbyist_clients"])
async def get_lobbyist_clients_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    LobbyistID: Optional[int] = None,
    ClientID: Optional[int] = None,
    Name: Optional[str] = None,
    ClientsNames: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM lobbyists_v_lobbyist_clients"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for list laws_kns_israel_law table
@app.get("/laws_kns_israel_law/list", status_code=200,tags=["laws_kns_israel_law"])
async def get_israel_law_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    KnessetNum: Optional[int] = None,
    Name: Optional[str] = None,
    IsBasicLaw: Optional[bool] = None,
    IsFavoriteLaw: Optional[bool] = None,
    IsBudgetLaw: Optional[bool] = None,
    PublicationDate: Optional[datetime] = None,
    LatestPublicationDate: Optional[str] = None,
    LawValidityID: Optional[int] = None,
    LawValidityDesc: Optional[str] = None,
    ValidityStartDate: Optional[datetime] = None,
    ValidityStartDateNotes: Optional[str] = None,
    ValidityFinishDate: Optional[datetime] = None,
    ValidityFinishDateNotes: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM laws_kns_israel_law"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "laws_kns_israel_law" table
@app.get('/laws_kns_israel_law/{IsraelLawID}',tags=["laws_kns_israel_law"])
async def get_israel_law(IsraelLawID: int):
    data = DB.get_single_data('laws_kns_israel_law', 'IsraelLawID', IsraelLawID)
    return {'success': True, 'data': data}
    
# Route for votes_vote_result_type table
@app.get("/votes_vote_result_type/list", status_code=200,tags=["votes_vote_result_type"])
async def get_vote_result_type_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    result_type_name: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM votes_vote_result_type"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "votes_vote_result_type" table
@app.get('/votes_vote_result_type/{result_type_id}',tags=["votes_vote_result_type"])
async def get_vote_result_type(result_type_id: int):
    data = DB.get_single_data('votes_vote_result_type', 'result_type_id', result_type_id)
    return {'success': True, 'data': data}
    
# Route for list committees_kns_documentcommitteesession table
@app.get("/committees_kns_documentcommitteesession/list", status_code=200,tags=["committees_kns_documentcommitteesession"])
async def get_documentcommitteesession_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    DocumentCommitteeSessionID: Optional[int] = None,
    CommitteeSessionID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    download_filename: Optional[str] = None,
    download_filesize: Optional[int] = None,
    download_crc32c: Optional[str] = None,
    download_error: Optional[str] = None,
    text_protocol_extension: Optional[str] = None,
    text_parsed_filename: Optional[str] = None,
    text_filesize: Optional[int] = None,
    text_crc32c: Optional[str] = None,
    text_error: Optional[str] = None,
    parts_protocol_extension: Optional[str] = None,
    parts_parsed_filename: Optional[str] = None,
    parts_filesize: Optional[int] = None,
    parts_crc32c: Optional[str] = None,
    parts_error: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_kns_documentcommitteesession"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for lobbyists_v_lobbyist table
@app.get("/lobbyists_v_lobbyist/list", status_code=200,tags=["lobbyists_v_lobbyist"])
async def get_lobbyist_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    IdentityNumber: Optional[str] = None,
    FullName: Optional[str] = None,
    PermitTypeValue: Optional[str] = None,
    Key: Optional[int] = None,
    CorporationName: Optional[str] = None,
    IsIndependent: Optional[bool] = None,
    CorpNumber: Optional[int] = None,
    PracticeFramework: Optional[str] = None,
    IsMemberInFaction: Optional[str] = None,
    MemberInFaction: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM lobbyists_v_lobbyist"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "lobbyists_v_lobbyist" table
@app.get('/lobbyists_v_lobbyist/{LobbyistID}',tags=["lobbyists_v_lobbyist"])
async def get_lobbyist(LobbyistID: int):
    data = DB.get_single_data('lobbyists_v_lobbyist', 'LobbyistID', LobbyistID)
    return {'success': True, 'data': data}
    
# Route for list laws_kns_israel_law_binding table
@app.get("/laws_kns_israel_law_binding/list", status_code=200,tags=["laws_kns_israel_law_binding"])
async def get_israel_law_binding_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    IsraelLawID: Optional[int] = None,
    IsraelLawReplacedID: Optional[int] = None,
    LawID: Optional[int] = None,
    LawTypeID: Optional[int] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM laws_kns_israel_law_binding"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "laws_kns_israel_law_binding" table
@app.get('/laws_kns_israel_law_binding/{IsraelLawBinding}',tags=["laws_kns_israel_law_binding"])
async def get_israel_law_binding(IsraelLawBinding: int):
    data = DB.get_single_data('laws_kns_israel_law_binding', 'IsraelLawBinding', IsraelLawBinding)
    return {'success': True, 'data': data}
    
# Route for list people_plenum_session_voters table
@app.get("/people_plenum_session_voters/list", status_code=200,tags=["people_plenum_session_voters"])
async def get_plenum_session_voters_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    Number: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    Name: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    IsSpecialMeeting: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None,
    voter_mk_ids: List[int] = Query([],example=[],list=True)
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays=[voter_mk_ids]
    var_names = ["voter_mk_ids"]
    for key, value in query_params:
        if key in var_names:
            elemts=arrays[var_names.index(key)]  
            qs_parts.append(f"{key}={elemts}")    
        elif key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")   
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_plenum_session_voters"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "people_plenum_session_voters" table
@app.get('/people_plenum_session_voters/{PlenumSessionID}',tags=["people_plenum_session_voters"])
async def get_plenum_session_voters(PlenumSessionID: int):
    data = DB.get_single_data('people_plenum_session_voters', 'PlenumSessionID', PlenumSessionID)
    return {'success': True, 'data': data}
    
# Route for list people_mk_voted_against_majority table
@app.get("/people_mk_voted_against_majority/list", status_code=200,tags=["people_mk_voted_against_majority"])
async def get_mk_voted_against_majority_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    vote_id: Optional[int] = None,
    mk_id: Optional[int] = None,
    faction_id: Optional[int] = None,
    vote_knesset: Optional[int] = None,
    vote_plenum: Optional[int] = None,
    vote_assembly: Optional[int] = None,
    vote_pagra: Optional[bool] = None,
    vote_datetime: Optional[datetime] = None,
    vote_majority: Optional[str] = None,
    voted_against_majority: Optional[bool] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_mk_voted_against_majority"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for list committees_kns_cmtsessionitem table
@app.get("/committees_kns_cmtsessionitem/list", status_code=200,tags=["committees_kns_cmtsessionitem"])
async def get_cmtsessionitem_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    ItemID: Optional[int] = None,
    CommitteeSessionID: Optional[int] = None,
    Ordinal: Optional[int] = None,
    StatusID: Optional[int] = None,
    Name: Optional[str] = None,
    ItemTypeID: Optional[int] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_kns_cmtsessionitem"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for "committees_kns_cmtsessionitem" table
@app.get('/committees_kns_cmtsessionitem/{CmtSessionItemID}',tags=["committees_kns_cmtsessionitem"])
async def get_cmtsessionitem(CmtSessionItemID: int):
    data = DB.get_single_data('committees_kns_cmtsessionitem', 'CmtSessionItemID', CmtSessionItemID)
    return {'success': True, 'data': data}
    
# Route for list laws_kns_israel_law_ministry table
@app.get("/laws_kns_israel_law_ministry/list", status_code=200,tags=["laws_kns_israel_law_ministry"])
async def get_israel_law_ministry_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    IsraelLawID: Optional[int] = None,
    GovMinistryID: Optional[int] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM laws_kns_israel_law_ministry"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "laws_kns_israel_law_ministry" table
@app.get('/laws_kns_israel_law_ministry/{LawMinistryID}',tags=["laws_kns_israel_law_ministry"])
async def get_israel_law_ministry(LawMinistryID: int):
    data = DB.get_single_data('laws_kns_israel_law_ministry', 'LawMinistryID', LawMinistryID)
    return {'success': True, 'data': data}
    
# Route for list people_mk_party_discipline_knesset_20 table
@app.get("/people_mk_party_discipline_knesset_20/list", status_code=200,tags=["people_mk_party_discipline_knesset_20"])
async def get_mk_party_discipline_knesset_20_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    vote_id: Optional[int] = None,
    vote_url: Optional[str] = None,
    vote_datetime: Optional[datetime] = None,
    vote_knesset: Optional[int] = None,
    vote_plenum: Optional[int] = None,
    vote_assembly: Optional[int] = None,
    vote_pagra: Optional[bool] = None,
    mk_id: Optional[int] = None,
    mk_name: Optional[str] = None,
    faction_id: Optional[int] = None,
    faction_name: Optional[str] = None,
    vote_majority: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_mk_party_discipline_knesset_20"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}


# Route for list committees_kns_committeesession table
@app.get("/committees_kns_committeesession/list", status_code=200,tags=["committees_kns_committeesession"])
async def get_committeesession_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    Number: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    TypeID: Optional[int] = None,
    TypeDesc: Optional[str] = None,
    CommitteeID: Optional[int] = None,
    Location: Optional[str] = None,
    SessionUrl: Optional[str] = None,
    BroadcastUrl: Optional[str] = None,
    StartDate: Optional[date] = None,
    FinishDate: Optional[datetime] = None,
    Note: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    download_crc32c: Optional[str] = None,
    download_filename: Optional[str] = None,
    download_filesize: Optional[int] = None,
    parts_crc32c: Optional[str] = None,
    parts_filesize: Optional[int] = None,
    parts_parsed_filename: Optional[str] = None,
    text_crc32c: Optional[str] = None,
    text_filesize: Optional[int] = None,
    text_parsed_filename: Optional[str] = None,
    item_ids: List[int] = Query([],example=[],list=True),
    item_type_ids: List[int] = Query([],example=[],list=True),
    topics: Optional[str] = None,
    committee_name: Optional[str] = None,
    bill_names: Optional[str] = None,
    bill_types: Optional[str] = None,
    related_to_legislation: Optional[bool] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays=[item_ids,item_type_ids,[topics],[bill_names],[bill_types]]
    var_names = ["item_ids","item_type_ids","topics","bill_names","bill_types"]
    for key, value in query_params:
        if key in var_names:
            elemts=arrays[var_names.index(key)]  
            qs_parts.append(f"{key}={elemts}")    
        elif key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")   
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_kns_committeesession"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}


# Route for list members_kns_mksitecode table
@app.get("/members_kns_mksitecode/list", status_code=200,tags=["members_kns_mksitecode"])
async def get_mksitecode_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    KnsID: Optional[int] = None,
    SiteId: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_kns_mksitecode"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "members_kns_mksitecode" table
@app.get('/members_kns_mksitecode/{MKSiteCode}',tags=["members_kns_mksitecode"])
async def get_mksitecode(MKSiteCode: int):
    data = DB.get_single_data('members_kns_mksitecode', 'MKSiteCode', MKSiteCode)
    return {'success': True, 'data': data}
    
# Route for list people_committees_meeting_attendees_mks_stats table
@app.get("/people_committees_meeting_attendees_mks_stats/list", status_code=200,tags=["people_committees_meeting_attendees_mks_stats"])
async def get_committee_attendees_mks_stats_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    knesset_num: Optional[int] = None,
    committee_id: Optional[int] = None,
    committee_name: Optional[str] = None,
    meeting_start_date: Optional[datetime] = None,
    meeting_topics: Optional[str] = None,
    mk_id: Optional[int] = None,
    mk_name: Optional[str] = None,
    mk_membership_committee_names: Optional[str] = None,
    mk_faction_id: Optional[int] = None,
    mk_faction_name: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_committees_meeting_attendees_mks_stats"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for laws_kns_law table
@app.get("/laws_kns_law/list", status_code=200,tags=["laws_kns_law"])
async def get_law_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    TypeID: Optional[int] = None,
    TypeDesc: Optional[str] = None,
    SubTypeID: Optional[int] = None,
    SubTypeDesc: Optional[str] = None,
    KnessetNum: Optional[int] = None,
    Name: Optional[str] = None,
    PublicationDate: Optional[datetime] = None,
    PublicationSeriesID: Optional[int] = None,
    PublicationSeriesDesc: Optional[str] = None,
    MagazineNumber: Optional[str] = None,
    PageNumber: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM laws_kns_law"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "laws_kns_law" table
@app.get('/laws_kns_law/{LawID}',tags=["laws_kns_law"])
async def get_law(law_id: int):
    data = DB.get_single_data('laws_kns_law', 'LawID', LawID)
    return {'success': True, 'data': data}
    
# Route for list committees_document_committee_sessions_for_parsing table
@app.get("/committees_document_committee_sessions_for_parsing/list", status_code=200,tags=["committees_document_committee_sessions_for_parsing"])
async def get_committee_sessions_for_parsing_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    KnessetNum: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_document_committee_sessions_for_parsing"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "committees_document_committee_sessions_for_parsing" table
@app.get('/committees_document_committee_sessions_for_parsing/{DocumentCommitteeSessionID}',tags=["committees_document_committee_sessions_for_parsing"])
async def get_document_committee_sessions_for_parsing(DocumentCommitteeSessionID: int):
    data = DB.get_single_data('committees_document_committee_sessions_for_parsing', 'DocumentCommitteeSessionID', DocumentCommitteeSessionID)
    return {'success': True, 'data': data}
    
# Route for people_committees_meeting_attendees_mks_stats_errors table
@app.get("/people_committees_meeting_attendees_mks_stats_errors/list", status_code=200,tags=["people_committees_meeting_attendees_mks_stats_errors"])
async def get_committee_attendees_mks_stats_errors_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_committees_meeting_attendees_mks_stats_errors"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}


# Route for list committees_download_document_committee_session table
@app.get("/committees_download_document_committee_session/list", status_code=200,tags=["committees_download_document_committee_session"])
async def get_download_document_committee_session_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    KnessetNum: Optional[int] = None,
    filename: Optional[str] = None,
    filesize: Optional[int] = None,
    crc32c: Optional[str] = None,
    error: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_download_document_committee_session"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "committees_download_document_committee_session" table
@app.get('/committees_download_document_committee_session/{DocumentCommitteeSessionID}',tags=["committees_download_document_committee_session"])
async def get_download_document_committee_session(DocumentCommitteeSessionID: int):
    data = DB.get_single_data('committees_download_document_committee_session', 'DocumentCommitteeSessionID', DocumentCommitteeSessionID)
    return {'success': True, 'data': data}

# Route for list laws_kns_israel_law_name table
@app.get("/laws_kns_israel_law_name/list", status_code=200,tags=["laws_kns_israel_law_name"])
async def get_israel_law_name_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    IsraelLawID: Optional[int] = None,
    LawID: Optional[int] = None,
    LawTypeID: Optional[int] = None,
    Name: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM laws_kns_israel_law_name"
    data = DB.get_data_list(query, limit,offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "laws_kns_israel_law_name" table
@app.get('/laws_kns_israel_law_name/{IsraelLawNameID}',tags=["laws_kns_israel_law_name"])
async def get_israel_law_name(IsraelLawNameID: int):
    data = DB.get_single_data('laws_kns_israel_law_name', 'IsraelLawNameID', IsraelLawNameID)
    return {'success': True, 'data': data}
    
# Route for list people_members_joined_mks table
@app.get("/people_members_joined_mks/list", status_code=200,tags=["people_members_joined_mks"])
async def get_joined_mks_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    mk_status_id: Optional[int] = None,
    mk_individual_name: Optional[str] = None,
    mk_individual_name_eng: Optional[str] = None,
    mk_individual_first_name: Optional[str] = None,
    mk_individual_first_name_eng: Optional[str] = None,
    mk_individual_email: Optional[str] = None,
    mk_individual_photo: Optional[str] = None,
    PersonID: Optional[int] = None,
    LastName: Optional[str] = None,
    FirstName: Optional[str] = None,
    GenderID: Optional[int] = None,
    GenderDesc: Optional[str] = None,
    Email: Optional[str] = None,
    IsCurrent: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None,
    positions_gender: Optional[str] = None,
    positions_position: Optional[str] = None,
    positions_KnessetNum: Optional[int] = None,
    positions_start_date: Optional[datetime] = None,
    positions_finish_date: Optional[datetime] = None,
    positions_position_id: Optional[int] = None,
    positions_FactionID: Optional[int] = None,
    positions_FactionName: Optional[str] = None,
    positions_CommitteeID: Optional[int] = None,
    positions_CommitteeName: Optional[str] = None,
    positions_DutyDesc: Optional[str] = None,
    positions_GovMinistryID: Optional[int] = None,
    positions_GovernmentNum: Optional[int] = None,
    positions_GovMinistryName: Optional[str] = None,
    altnames: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays_val=[[altnames]]
    arrays_name=["altnames"]
    objects_val=[positions_gender,positions_position,positions_KnessetNum,positions_start_date,positions_finish_date,
                 positions_position_id,positions_FactionID,positions_FactionName,positions_CommitteeID,
                 positions_CommitteeName,positions_DutyDesc,positions_GovMinistryID,positions_GovernmentNum,positions_GovMinistryName]
    objects_name=["positions_gender","positions_position","positions_KnessetNum","positions_start_date","positions_finish_date",
                  "positions_position_id","positions_FactionID","positions_FactionName","positions_CommitteeID",
                  "positions_CommitteeName","positions_DutyDesc","positions_GovMinistryID","positions_GovernmentNum","positions_GovMinistryName"]
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by'] and key not in objects_name and key not in arrays_name:
            qs_parts.append(f"{key}={value}")
    for name, val in zip(arrays_name, arrays_val):
        if val[0]:
            qs_parts.append(f"{name}={val}")
    for name, val in zip(objects_name, objects_val):
        if val:
            qs_parts.append(f"{name}=<{val}>")    
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_members_joined_mks"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "people_members_joined_mks" table
@app.get('/people_members_joined_mks/{mk_individual_id}',tags=["people_members_joined_mks"])
async def get_members_joined_mks(mk_individual_id: int):
    data = DB.get_single_data('people_members_joined_mks', 'mk_individual_id', mk_individual_id)
    return {'success': True, 'data': data}
    
# Route for list laws_kns_law_binding table
@app.get("/laws_kns_law_binding/list", status_code=200,tags=["laws_kns_law_binding"])
async def get_law_binding_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    LawID: Optional[int] = None,
    LawTypeID: Optional[int] = None,
    IsraelLawID: Optional[int] = None,
    ParentLawID: Optional[int] = None,
    LawParentTypeID: Optional[int] = None,
    BindingType: Optional[int] = None,
    BindingTypeDesc: Optional[str] = None,
    PageNumber: Optional[str] = None,
    AmendmentType: Optional[int] = None,
    AmendmentTypeDesc: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM laws_kns_law_binding"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "laws_kns_law_binding" table
@app.get('/laws_kns_law_binding/{LawBindingID}',tags=["laws_kns_law_binding"])
async def get_law_binding(LawBindingID: int):
    data = DB.get_single_data('laws_kns_law_binding', 'LawBindingID', LawBindingID)
    return {'success': True, 'data': data}
    
# Route for list knesset_kns_itemtype table
@app.get("/knesset_kns_itemtype/list", status_code=200,tags=["knesset_kns_itemtype"])
async def get_knesset_itemtype_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    Desc: Optional[str] = None,
    TableName: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM knesset_kns_itemtype"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "knesset_kns_itemtype" table
@app.get('/knesset_kns_itemtype/{ItemTypeID}',tags=["knesset_kns_itemtype"])
async def get_itemtype(ItemTypeID: int):
    data = DB.get_single_data('knesset_kns_itemtype', 'ItemTypeID', ItemTypeID)
    return {'success': True, 'data': data}
    
# Route for list committees_meeting_protocols_text table
@app.get("/committees_meeting_protocols_text/list", status_code=200,tags=["committees_meeting_protocols_text"])
async def get_committee_meeting_protocols_text_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    GroupTypeID: Optional[int] = None,
    GroupTypeDesc: Optional[str] = None,
    ApplicationID: Optional[int] = None,
    ApplicationDesc: Optional[str] = None,
    FilePath: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    KnessetNum: Optional[int] = None,
    protocol_extension: Optional[str] = None,
    parsed_filename: Optional[str] = None,
    filesize: Optional[str] = None,
    crc32c: Optional[str] = None,
    error: Optional[str] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_meeting_protocols_text"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "committees_meeting_protocols_text" table
@app.get('/committees_meeting_protocols_text/{DocumentCommitteeSessionID}',tags=["committees_meeting_protocols_text"])
async def get_meeting_protocols_text(DocumentCommitteeSessionID: int):
    data = DB.get_single_data('committees_meeting_protocols_text', 'DocumentCommitteeSessionID', DocumentCommitteeSessionID)
    return {'success': True, 'data': data}
    
# Route for list people_committees_meeting_attendees_mks table
@app.get("/people_committees_meeting_attendees_mks/list", status_code=200,tags=["people_committees_meeting_attendees_mks"])
async def get_committee_attendees_mks_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    CommitteeSessionID: Optional[int] = None,
    Number: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    TypeID: Optional[int] = None,
    TypeDesc: Optional[str] = None,
    CommitteeID: Optional[int] = None,
    Location: Optional[str] = None,
    SessionUrl: Optional[str] = None,
    BroadcastUrl: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    Note: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None,
    protocol_extension: Optional[str] = None,
    text_filename: Optional[str] = None,
    parts_filename: Optional[str] = None,
    topics: Optional[str] = None,
    mks: Optional[str] = None,
    invitees_name: Optional[str] = None,
    invitees_role: Optional[str] = None,
    legal_advisors: Optional[str] = None,
    manager: Optional[str] = None,
    attended_mk_individual_ids: List[int] = Query([], alias="attended_mk_individual_ids",example=[736], list=True)
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays_number_val=[attended_mk_individual_ids]
    arrays_number_names=["attended_mk_individual_ids"]
    arrays_val=[[topics],[mks],[legal_advisors],[manager]]
    arrays_name = ["topics","mks","legal_advisors","manager"] 
    objects_val=[invitees_name,invitees_role]
    objects_name=["invitees_name","invitees_role"]        
    for key, value in query_params:
        if key in arrays_number_names:
            elemts=arrays_number_val[arrays_number_names.index(key)]  
            qs_parts.append(f"{key}={elemts}")    
        elif key not in ['limit', 'offset', 'order_by'] and key not in arrays_name and key not in objects_name:
            qs_parts.append(f"{key}={value}")
    
    for name, val in zip(arrays_name, arrays_val):
        if val[0]:
            qs_parts.append(f"{name}={val}")
    for name, val in zip(objects_name, objects_val):
        if val:
            qs_parts.append(f"{name}=<{val}>")    
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM people_committees_meeting_attendees_mks"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}


# Route for list members_kns_person table
@app.get("/members_kns_person/list", status_code=200,tags=["members_kns_person"])
async def get_person_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    PersonID: Optional[int] = None,
    LastName: Optional[str] = None,
    FirstName: Optional[str] = None,
    GenderID: Optional[int] = None,
    GenderDesc: Optional[str] = None,
    Email: Optional[str] = None,
    IsCurrent: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_kns_person"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "members_kns_person" table
@app.get('/members_kns_person/{PersonID}',tags=["members_kns_person"])
async def get_person(PersonID: int):
    data = DB.get_single_data('members_kns_person', 'PersonID', PersonID)
    return {'success': True, 'data': data}
    
# Route for list members_mk_individual table
@app.get("/members_mk_individual/list", status_code=200,tags=["members_mk_individual"])
async def get_mk_individual_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    mk_status_id: Optional[int] = None,
    mk_individual_name: Optional[str] = None,
    mk_individual_name_eng: Optional[str] = None,
    mk_individual_first_name: Optional[str] = None,
    mk_individual_first_name_eng: Optional[str] = None,
    mk_individual_email: Optional[str] = None,
    mk_individual_photo: Optional[str] = None,
    PersonID: Optional[int] = None,
    LastName: Optional[str] = None,
    FirstName: Optional[str] = None,
    GenderID: Optional[int] = None,
    GenderDesc: Optional[str] = None,
    Email: Optional[str] = None,
    IsCurrent: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None,
    altnames: Optional[str] = None,
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays_val=[[altnames]]
    arrays_name = ["altnames"] 
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by'] and key not in arrays_name:
            qs_parts.append(f"{key}={value}")
    for name, val in zip(arrays_name, arrays_val):
        if val[0]:
            qs_parts.append(f"{name}={val}")        
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_mk_individual"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "members_mk_individual" table
@app.get('/members_mk_individual/{mk_individual_id}',tags=["members_mk_individual"])
async def get_individual(mk_individual_id: int):
    data = DB.get_single_data('members_mk_individual', 'mk_individual_id', mk_individual_id)
    return {'success': True, 'data': data}
    
# Route for list members_factions table
@app.get("/members_factions/list", status_code=200,tags=["members_factions"])
async def get_factions_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    name: Optional[str] = None,
    start_date: Optional[date] = None,
    finish_date: Optional[date] = None,
    knessets: List[int] = Query([], alias="knessets",example=[], list=True),
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays_number_val=[knessets]
    arrays_number_names=["knessets"]
    for key, value in query_params:
        if key in arrays_number_names:
            elemts=arrays_number_val[arrays_number_names.index(key)]  
            qs_parts.append(f"{key}={elemts}")    
        elif key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_factions"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for "members_factions" table
@app.get('/members_factions/{id}',tags=["members_factions"])
async def get_factions(id: int):
    data = DB.get_single_data('members_factions', 'id', id)
    return {'success': True, 'data': data}
    

# Route for list laws_kns_israel_law_classification table
@app.get("/laws_kns_israel_law_classification/list", status_code=200,tags=["laws_kns_israel_law_classification"])
async def get_israel_law_classification_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    IsraelLawID: Optional[int] = None,
    ClassificiationID: Optional[int] = None,
    ClassificiationDesc: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM laws_kns_israel_law_classification"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "laws_kns_israel_law_classification" table
@app.get('/laws_kns_israel_law_classification/{LawClassificiationID}',tags=["laws_kns_israel_law_classification"])
async def get_israel_law_classification(LawClassificiationID: int):
    data = DB.get_single_data('laws_kns_israel_law_classification', 'LawClassificiationID', LawClassificiationID)
    return {'success': True, 'data': data}
    
# Route for list members_mk_individual_names table
@app.get("/members_mk_individual_names/list", status_code=200,tags=["members_mk_individual_names"])
async def get_mk_individual_names_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    names: Optional[str] = None,
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays_val=[[names]]
    arrays_name = ["names"] 
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by'] and key not in arrays_name:
            qs_parts.append(f"{key}={value}")
    for name, val in zip(arrays_name, arrays_val):
        if val[0]:
            qs_parts.append(f"{name}={val}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_mk_individual_names"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "members_mk_individual_names" table
@app.get('/members_mk_individual_names/{mk_individual_id}',tags=["members_mk_individual_names"])
async def get_individual_names(mk_individual_id: int):
    data = DB.get_single_data('members_mk_individual_names', 'mk_individual_id', mk_individual_id)
    return {'success': True, 'data': data}
    
# Route for list members_faction_memberships table
@app.get("/members_faction_memberships/list", status_code=200,tags=["members_faction_memberships"])
async def get_members_faction_memberships_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    faction_id: Optional[int] = None,
    faction_name: Optional[str] = None,
    start_date: Optional[date] = None,
    finish_date: Optional[date] = None,
    member_mk_ids: List[int] = Query([], alias="member_mk_ids",example=[], list=True),
    knesset: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    arrays_number_val=[member_mk_ids]
    arrays_number_names=["member_mk_ids"]
    for key, value in query_params:
        if key in arrays_number_names:
            elemts=arrays_number_val[arrays_number_names.index(key)]  
            qs_parts.append(f"{key}={elemts}")    
        elif key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_faction_memberships"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "members_faction_memberships" table
@app.get('/members_faction_memberships/{faction_id}',tags=["members_faction_memberships"])
async def get_faction_memberships(faction_id: int):
    data = DB.get_single_data('members_faction_memberships', 'faction_id', faction_id)
    return {'success': True, 'data': data}

# Route for list members_kns_persontoposition table
@app.get("/members_kns_persontoposition/list", status_code=200,tags=["members_kns_persontoposition"])
async def get_person_to_position_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    PersonID: Optional[int] = None,
    PositionID: Optional[int] = None,
    KnessetNum: Optional[int] = None,
    GovMinistryID: Optional[int] = None,
    GovMinistryName: Optional[str] = None,
    DutyDesc: Optional[str] = None,
    FactionID: Optional[int] = None,
    FactionName: Optional[str] = None,
    GovernmentNum: Optional[int] = None,
    CommitteeID: Optional[int] = None,
    CommitteeName: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    IsCurrent: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_kns_persontoposition"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}


# Route for single "members_kns_persontoposition" table
@app.get('/members_kns_persontoposition/{PersonToPositionID}',tags=["members_kns_persontoposition"])
async def get_persontoposition(PersonToPositionID: int):
    data = DB.get_single_data('members_kns_persontoposition', 'PersonToPositionID', PersonToPositionID)
    return {'success': True, 'data': data}
    
# Route for list committees_kns_committee table
@app.get("/committees_kns_committee/list", status_code=200,tags=["committees_kns_committee"])
async def get_committee_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    Name: Optional[str] = None,
    CategoryID: Optional[int] = None,
    CategoryDesc: Optional[str] = None,
    KnessetNum: Optional[int] = None,
    CommitteeTypeID: Optional[int] = None,
    CommitteeTypeDesc: Optional[str] = None,
    Email: Optional[str] = None,
    StartDate: Optional[datetime] = None,
    FinishDate: Optional[datetime] = None,
    AdditionalTypeID: Optional[int] = None,
    AdditionalTypeDesc: Optional[str] = None,
    ParentCommitteeID: Optional[int] = None,
    CommitteeParentName: Optional[str] = None,
    IsCurrent: Optional[bool] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM committees_kns_committee"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "committees_kns_committee" table
@app.get('/committees_kns_committee/{CommitteeID}',tags=["committees_kns_committee"])
async def get_single_data(CommitteeID: int):
    data = DB.get_single_data('committees_kns_committee', 'CommitteeID', CommitteeID)
    return {'success': True, 'data': data}
    
# Route for list members_mk_individual_factions table
@app.get("/members_mk_individual_factions/list", status_code=200,tags=["members_mk_individual_factions"])
async def get_mk_individual_factions_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    mk_individual_id: Optional[int] = None,
    faction_id: Optional[int] = None,
    faction_name: Optional[str] = None,
    start_date: Optional[date] = None,
    finish_date: Optional[date] = None,
    knesset: Optional[int] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_mk_individual_factions"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': True, 'data': data})
    return {'success': True, 'data': data}    


# Route for list members_kns_position table
@app.get("/members_kns_position/list", status_code=200,tags=["members_kns_position"])
async def get_position_list(
    request: Request,
    limit: int = 0,
    offset: int = 0,
    order_by: Optional[str] = None,
    Description: Optional[str] = None,
    GenderID: Optional[int] = None,
    GenderDesc: Optional[str] = None,
    LastUpdatedDate: Optional[datetime] = None
):
    query_params = request.query_params.items()
    qs_parts = []
    for key, value in query_params:
        if key not in ['limit', 'offset', 'order_by']:
            qs_parts.append(f"{key}={value}")
    qs = '&'.join(qs_parts)
    query = "SELECT * FROM members_kns_position"
    data = DB.get_data_list(query, limit, offset, order_by, qs)
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return JSONResponse(content={'success': False, 'data': str(data)}, status_code=response_status)
    return {'success': True, 'data': data}

# Route for single "members_kns_position" table
@app.get('/members_kns_position/{PositionID}',tags=["members_kns_position"])
async def get_position(PositionID: int):
    data = DB.get_single_data('members_kns_position', 'PositionID', PositionID)
    return {'success': True, 'data': data}


#################aggragate
@app.get('/minister_by_individual/{id}', status_code=200,tags=['Special Aggravations'], description="Get current minister")
@app.get('/minister_by_personal/{id}', status_code=200,tags=['Special Aggravations'], description="Get current minister")
def get_minister(id: int, request: Request):
    request_path = request.scope['path']
    id_field = (
        "mk_individual_id"
        if request_path == f'/minister_by_individual/{str(id)}' else 'PersonID'
    )
    query = QUERY.get_minister_query(id_field)
    data = DB.get_fully_today_member(query, (id,))
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return {'success': False, 'data': str(data)}
    return {'success': True, 'data': data}

@app.get('/member_kns_by_individual/{id}', status_code=200,tags=['Special Aggravations'], description="Get current member knesset")
@app.get('/member_kns_by_personal/{id}', status_code=200,tags=['Special Aggravations'], description="Get current member knesset")
def get_member_kns(id: int, request: Request):
    request_path = request.scope['path']
    id_field = (
        "mk_individual_id"
        if request_path == f'/member_kns_by_individual/{str(id)}' else 'PersonID'
    )
    query = QUERY.get_member_kns_query(id_field)
    data = DB.get_fully_today_member(query, (id,))
    if isinstance(data, Exception):
        response_status = status.HTTP_404_NOT_FOUND if str(data) == 'No row found' else status.HTTP_400_BAD_REQUEST
        return {'success': False, 'data': str(data)}
    return {'success': True, 'data': data}



