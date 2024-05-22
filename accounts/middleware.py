

class AccountMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        account_info = request.META.get('HTTP_ACCOUNT_INFO')
        request.account_id = account_info
        response = self.get_response(request)
        return response
