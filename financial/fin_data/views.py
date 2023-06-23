import re

from .models import financial_data

from django.core.paginator import Paginator, EmptyPage

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

def check_query_format(
        **data
    ):
    """Check the format of the date string and determine whether the variables 'page' and 'limit' are integers or not.
    
    Optional Parameters:
        symbol: Str.
        dates: Dict, optional({'start_date': 'yyyy-mm-dd', 'end_date': 'yyyy-mm-dd'}).
        page: Int.
        limit: Int.

    Returns:
        status: Bool - True if all input parameters are in right format else False.
        message: Str - "" if status is True else return error messages.
    """
    result = {
        "status": True,
        "message": "",
    }

    if "symbol" in data:
        if not "symbol":
            result["status"] = False
            result["message"] += f"symbol cannot be null. "

    if "dates" in data:
        for key, date in data["dates"].items():
            if len(date) != 10:
                result["status"] = False
                result["message"] += f"{key}({date}), length/format error, format should be yyyy-mm-dd. "
                continue
            match = re.search(r'\d{4}-\d{2}-\d{2}', date)
            if not match:
                result["status"] = False
                result["message"] += f"{key}({date}), format error, format should be yyyy-mm-dd. "
    
    if "page" in data:
        try:
            page = int(data["page"])
        except ValueError:
            result["status"] = False
            result["message"] += f"page({data['page']}), value error, should be integer. "

    if "limit" in data:
        try:
            limit = int(data["limit"])
        except ValueError:
            result["status"] = False
            result["message"] += f"limit({data['limit']}), value error, should be integer. "

    return result

def check_required_query_params(**data):
    """Check if the required query parameters are exist.
    
    Optional Parameters:
        symbol: Str.
        start_date: Str.
        end_date: Str.

    Returns:
        status: Bool - True if all input parameters are in right format else False.
        message: Str - "" if status is True else return error messages.
    """
    result = {
        "status": True,
        "message": "Query parameter(s) required: ",
    }

    if "symbol" in data and not data["symbol"]:
        result["status"] = False
        result["message"] += "symbol, "

    if "start_date" in data and not data["start_date"]:
        result["status"] = False
        result["message"] += "start_date, "

    if "end_date" in data and not data["end_date"]:
        result["status"] = False
        result["message"] += "end_date, "

    if not result["status"]:
        result["message"] += "please check again."
    else:
        result["message"] = ""

    return result

class FinancialDataView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        """Get the financial data.

        Parameters:
            symbol: IBM or AAPL(Apple Inc.) or null(return the data inclued IBM and AAPL).
            start_date: yyyy-mm-dd.
            end_date: yyyy-mm-dd.
            limit: Int - The limit of records that can be retrieved for a single page. If no limit is given, the default limit for one page is 5.
            page: Int - The current page index. If no page is given, the default page is 1.
        
        Returns:
            data: List of dictionaries - The financial data from start_date to end_date.
            pagination: The pagination data, such as count, limit, page and pages.
            info: The error message if there is an error.
        """
        result = {
            "data": [],
            "pagination": {
                "count": 0,
                "page": 0,
                "limit": 0,
                "pages": 0,
            },
            "info": {
                "error": "",
            },
        }
        
        # Get query parameters
        symbol = request.query_params.get("symbol", "")
        query_start_date = request.query_params.get("start_date", "")
        query_end_date = request.query_params.get("end_date", "")
        limit = request.query_params.get("limit", 5)
        page = request.query_params.get("page", 1)

        start_date = query_start_date if query_start_date else "0000-06-19"
        end_date = query_end_date if query_end_date else "9999-06-19"

        # Check query format(start_date, end_date, page, limit)
        dates_check = check_query_format(
            dates={
                "start_date": start_date, 
                "end_date": end_date,
            }, 
            page=page, 
            limit=limit
        )
        if not dates_check["status"]:
            result["info"]["error"] = f"{dates_check['message']}"
            return Response(result)

        # Get the finanical data
        fin_data = financial_data.objects.filter(date__gte=start_date, date__lte=end_date).order_by('date') if not symbol else financial_data.objects.filter(symbol=symbol, date__gte=start_date, date__lte=end_date).order_by('date')
        try:
            paginator = Paginator(fin_data, limit)
            paginator_data = paginator.page(page).object_list
            result["pagination"]["page"] = int(page)
        except EmptyPage:   # If the page number exceeds the total number of pages, return the data of the last page.
            paginator_data = paginator.page(paginator.num_pages).object_list
            result["pagination"]["page"] = paginator.num_pages

        result["pagination"]["count"] = paginator.count
        result["pagination"]["limit"] = int(limit)
        result["pagination"]["pages"] = paginator.num_pages
        result["data"] = [ {
            "symbol": data.symbol,
            "open_price": data.open_price,
            "close_price": data.close_price,
            "date": data.date,
            "volume": data.volume,
        } for data in paginator_data ]
        
        return Response(result)

class StatisticsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        """Get the statistics data.
        
        Parameters:
            symbol: IBM or AAPL(Apple Inc.).
            start_date: yyyy-mm-dd.
            end_date: yyyy-mm-dd.
        
        Returns:
            data: The calculated statistic results.
            info: The error message if there is an error.
        """
        result = {
            "data": {
                "start_date": "",
                "end_date": "",
                "symbol": "",
                "average_daily_open_price": 0,
                "average_daily_close_price": 0,
                "average_daily_volume": 0
            },
            "info": {
                "error": "",
            },
        }

        # Get query parameters
        symbol = request.query_params.get("symbol", "")
        start_date = request.query_params.get("start_date", "")
        end_date = request.query_params.get("end_date", "")

        # Check required parameters(symbol, start_date, end_date).
        required_params_check = check_required_query_params(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
        )
        if not required_params_check["status"]:
            result["info"]["error"] = f"{required_params_check['message']}"
            return Response(result)
        
        # Check query format(symbol, start_date, end_date).
        dates_check = check_query_format(
            symbol=symbol,
            dates={
                "start_date": start_date, 
                "end_date": end_date,
            }
        )
        if not dates_check["status"]:
            result["info"]["error"] = f"{dates_check['message']}"
            return Response(result)

        fin_data = financial_data.objects.filter(symbol=symbol, date__gte=start_date, date__lte=end_date).values('open_price', 'close_price', 'volume')
        for data in fin_data:
            result["data"]["average_daily_open_price"] += data["open_price"]
            result["data"]["average_daily_close_price"] += data["close_price"]
            result["data"]["average_daily_volume"] += data["volume"]

        total_day = len(fin_data)
        result["data"]["symbol"] = symbol
        result["data"]["start_date"] = start_date
        result["data"]["end_date"] = end_date
        result["data"]["average_daily_open_price"] = round(result["data"]["average_daily_open_price"]/total_day, 2)
        result["data"]["average_daily_close_price"] = round(result["data"]["average_daily_close_price"]/total_day, 2)
        result["data"]["average_daily_volume"] = int(round(result["data"]["average_daily_volume"]/total_day, 0))

        return Response(result)
