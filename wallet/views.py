
from datetime import datetime

from customer.messages import CustomMessage
from customer.models import Customer
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from wallet.models import Transactions, Wallet
from wallet.serializers import (AddTransactionSerializer,
                                TransacationSerializer, WalletSerializer)

from wallet.utils import reference_id_gernerator


class EnableWalletAPIView(generics.GenericAPIView):
    """
        Enable customer account.
    
    """
    model = Wallet
    msg_ob = CustomMessage()
    permission_classes = (IsAuthenticated,)
    serializer_class = WalletSerializer

    def get_object(self):
        try:
            cutomer_obj = Customer.objects.get(user=self.request.user)
        except:cutomer_obj = None
        return cutomer_obj

        
    def post(self, *args, **kwargs):
        customer_obj = self.get_object()
        if not customer_obj:
            return Response({"status":'fail', "msg":self.msg_ob.invalid_user, "data":{}},
                status=status.HTTP_400_BAD_REQUEST)

        if customer_obj.customer_wallet:wallet_obj = customer_obj.customer_wallet
        else:wallet_obj = Wallet.objects.create(owned_by=customer_obj)
        wallet_obj.is_enabled = True
        wallet_obj.status_updated_on = datetime.now()
        wallet_obj.save()
        serializer = self.get_serializer(wallet_obj,fields = ('id','status','owned_by','balance','enabled_at')).data
        return Response({"status":'success', 
            "msg": self.msg_ob.wallet_enabled,
            "data":{'wallet':serializer}},status=status.HTTP_200_OK)


class AddVirtualMoneyAPIView(generics.GenericAPIView):
    """
        Deposit amount to customer account.
    """
    model = Wallet
    msg_ob = CustomMessage()
    permission_classes = (IsAuthenticated,)
    serializer_class = AddTransactionSerializer

    def post(self, *args, **kwargs):
        post_data = self.request.data.copy()
        try:customer_obj = Customer.objects.get(user=self.request.user)
        except:
            return Response({"status":'fail', "msg":self.msg_ob.invalid_user, "data":{}},
                status=status.HTTP_400_BAD_REQUEST)
        wallet_obj = customer_obj.customer_wallet
        if not wallet_obj or not wallet_obj.is_enabled:
            return Response({"status":'fail', "msg":self.msg_ob.wallet_incative, "data":{}},
                status=status.HTTP_400_BAD_REQUEST)
        post_data['wallet'] = wallet_obj.id
        post_data['transaction_type'] = 'deposit'
        post_data['transacted_on'] = datetime.now()
        post_data['reference_id'] = reference_id_gernerator()
        serialier = self.get_serializer(data=post_data)
        if serialier.is_valid():
            trans_obj = serialier.create(validated_data=serialier.validated_data)
    


            deposit_data = TransacationSerializer(trans_obj,fields = ('id','deposited_by','status',
                                'deposited_at','amount','reference_id')).data

    
            return Response({"status":'success', 
                "msg": self.msg_ob.transaction_success,
                "data":{'deposit':deposit_data}},status=status.HTTP_200_OK)
        else:
            return Response({"status":'fail', "msg":self.msg_ob.invalid_data, "errors":serialier.errors},
                status=status.HTTP_400_BAD_REQUEST)


class WithdrawMoneyAPIView(generics.GenericAPIView):
    """
        Withdraw amount from customer account.
    """

    model = Wallet
    msg_ob = CustomMessage()
    permission_classes = (IsAuthenticated,)
    serializer_class = AddTransactionSerializer

    def post(self, *args, **kwargs):
        post_data = self.request.data.copy()
        amount = post_data.get("amount")

        try:customer_obj = Customer.objects.get(user=self.request.user)
        except:
            return Response({"status":'fail', "msg":self.msg_ob.invalid_user, "data":{}},
                status=status.HTTP_400_BAD_REQUEST)
        wallet_obj = customer_obj.customer_wallet
        if not wallet_obj or not wallet_obj.is_enabled:
            return Response({"status":'fail', "msg":self.msg_ob.wallet_incative, "data":{}},
                status=status.HTTP_400_BAD_REQUEST)
        if int(amount) > int(wallet_obj.balance):
            return Response({"status":'fail', "msg":self.msg_ob.insufficient_balance, "data":{}},
                status=status.HTTP_400_BAD_REQUEST)

        post_data['wallet'] = wallet_obj.id
        post_data['transaction_type'] = 'withdrawal'
        post_data['transacted_on'] = datetime.now()
        post_data['reference_id'] = reference_id_gernerator()
        serialier = self.get_serializer(data=post_data)
        if serialier.is_valid():
            trans_obj = serialier.create(validated_data=serialier.validated_data)
            withdrawal_data = TransacationSerializer(trans_obj,fields = ('id','status',
                    'withdrawn_by','withdrawn_at', 'amount','reference_id')).data
            return Response({"status":'success', 
                "msg": self.msg_ob.transaction_success,
                "data":{'withdrawal':withdrawal_data}},status=status.HTTP_200_OK)
        else:
            return Response({"status":'fail', "msg":self.msg_ob.invalid_data, "errors":serialier.errors},
                status=status.HTTP_400_BAD_REQUEST)


class DisableWalletAPIView(generics.GenericAPIView):
    """
        Disable customer account.
    """
    model = Wallet
    msg_ob = CustomMessage()
    permission_classes = (IsAuthenticated,)
    serializer_class = WalletSerializer

    def get_object(self):
        try:
            cutomer_obj = Customer.objects.get(user=self.request.user)
        except:cutomer_obj = None
        return cutomer_obj

        
    def post(self, *args, **kwargs):
        customer_obj = self.get_object()
        if not customer_obj:
            return Response({"status":'fail', "msg":self.msg_ob.invalid_user, "data":{}},
                status=status.HTTP_400_BAD_REQUEST)

        if customer_obj.customer_wallet:wallet_obj = customer_obj.customer_wallet
        else:wallet_obj = Wallet.objects.create(owned_by=customer_obj)
        wallet_obj.is_enabled = False
        wallet_obj.status_updated_on = datetime.now()
        wallet_obj.save()
        serializer = self.get_serializer(wallet_obj, fields = ('id','status','owned_by','balance','disabled_at')).data
        return Response({"status":'success', 
            "msg": self.msg_ob.wallet_disabled,
            "data":{'wallet':serializer}},status=status.HTTP_200_OK)

