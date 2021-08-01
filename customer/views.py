from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from wallet.models import Wallet

from customer.messages import CustomMessage
from customer.models import Customer


class InitializeWalletAcoountAPIView(generics.GenericAPIView):
    """
        Initialize customer wallet account.
    """
    model = Customer
    msg_ob = CustomMessage()

    def get_object(self):
        try:instance = self.model.objects.get(id=self.request.data.get('customer_xid'))
        except:instance = None
        return instance
        
    def post(self, *args, **kwargs):
        customer_obj = self.get_object()
        if not customer_obj:
            return Response({"status":'fail', "msg":self.msg_ob.invalid_data, "data":{}},
                status=status.HTTP_400_BAD_REQUEST)
        
        wallet_obj,created = Wallet.objects.get_or_create(owned_by=customer_obj)
        if not created:
            wallet_obj.is_enabled = False
            wallet_obj.save()
        token_obj,tcreated = Token.objects.get_or_create(user=customer_obj.user)
        return Response({"status":'success', 
            "msg": self.msg_ob.wallet_activated,
            "data":{'token':token_obj.key}},status=status.HTTP_200_OK)
