import time

from rest_framework import serializers

from wallet.mixins import DynamicFieldsSerializerMixin
from wallet.models import Transactions, Wallet
from wallet.utils import postpone


class WalletSerializer(DynamicFieldsSerializerMixin,serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    enabled_at = serializers.SerializerMethodField()
    disabled_at = serializers.SerializerMethodField()

    def get_disabled_at(self,obj):
        if not obj.is_enabled and obj.status_updated_on:
            return obj.status_updated_on.strftime("%Y-%m-%d %H:%M %p")
        return ''

    def get_status(self,obj):
        if obj.is_enabled:
            return 'Enabled'
        else:return 'Disabled'

    def get_enabled_at(self,obj):
        if obj.is_enabled and obj.status_updated_on:
            return obj.status_updated_on.strftime("%Y-%m-%d %H:%M %p")
        return ''

    class Meta:
        model = Wallet
        fields = ('id','status','owned_by','enabled_at','balance','disabled_at')


class AddTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transactions
        fields = ('wallet','amount','reference_id','transaction_type','transacted_on')

    @postpone
    def upgrade_wallet(self, wallet_obj, trans_obj, amount):
        time.sleep(5)
        wallet_obj.balance += amount
        wallet_obj.save()
        trans_obj.status = 'success'
        trans_obj.save()

    @postpone
    def downgrade_wallet(self, wallet_obj, trans_obj, amount):
        time.sleep(5)
        wallet_obj.balance -= amount
        wallet_obj.save()
        trans_obj.status = 'success'
        trans_obj.save()

    def create(self, validated_data):
        amount = validated_data.get('amount')
        wallet = validated_data.get('wallet')
        transaction_type = validated_data.get('transaction_type')
        trans_obj = Transactions.objects.create(**validated_data)
        if transaction_type == 'deposit':
            self.upgrade_wallet(wallet, trans_obj, amount)
        elif transaction_type == 'withdrawal':
            self.downgrade_wallet(wallet, trans_obj, amount)
        return trans_obj

class TransacationSerializer(DynamicFieldsSerializerMixin,serializers.ModelSerializer):
    deposited_by = serializers.SerializerMethodField()
    deposited_at = serializers.SerializerMethodField()
    withdrawn_by = serializers.SerializerMethodField()
    withdrawn_at = serializers.SerializerMethodField()

    def get_withdrawn_at(self, obj):
        if obj.transacted_on:
            return obj.transacted_on.strftime("%Y-%m-%d %H:%M %p")
        return ''

    def get_withdrawn_by(self, obj):
        if obj.wallet and obj.wallet.owned_by:
            return obj.wallet.owned_by.id
        return ''

    def get_deposited_by(self, obj):
        if obj.wallet and obj.wallet.owned_by:
            return obj.wallet.owned_by.id
        return ''

    def get_deposited_at(self,obj):
        if obj.transacted_on:
            return obj.transacted_on.strftime("%Y-%m-%d %H:%M %p")
        return ''
        
    class Meta:
        model = Transactions
        fields = ('id','deposited_by','status','deposited_at','amount',
                    'reference_id','withdrawn_by','withdrawn_at')
