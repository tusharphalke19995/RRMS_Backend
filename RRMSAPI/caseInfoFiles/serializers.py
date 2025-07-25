from .models import CaseInfoDetails, FileDetails, FavouriteFiles, Notification, FileAccessRequest,FileUploadApproval
from rest_framework import serializers
import hashlib
import os
from mdm.serializers import DivisionSerializer
from users.serializers import UserSerializer
from mdm.models import StateMaster, DistrictMaster, UnitMaster, GeneralLookUp
from cryptography.fernet import Fernet



class CaseInfoDetailsSerializer(serializers.ModelSerializer):
    file_details = serializers.SerializerMethodField()
    stateName = serializers.SerializerMethodField()
    districtName = serializers.SerializerMethodField()
    unitName = serializers.SerializerMethodField()
    caseTypeName = serializers.SerializerMethodField()
    caseDate = serializers.DateTimeField(format="%d-%m-%Y",required=False,allow_null=True)
    caseStatusName = serializers.SerializerMethodField()

    class Meta:
        model = CaseInfoDetails
        fields = "__all__"
        read_only_fields = ['submitted_at', 'lastmodified_Date']
    
    def get_file_details(self, obj):
        files = FileDetails.objects.filter(caseDetails=obj)
        if files.exists():
            return FileDetailsSerializer(files, many=True).data
        return []
    
    def validate_caseNo(self,value):
        instance = self.instance
        print("instance",instance)
        if instance and str(instance.caseNo) == str(value):
            return value
        
        qs = CaseInfoDetails.objects.filter(caseNo=value)

        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("(CMS)Case No/ Enquiry No already exists")

        return value
    
    def get_caseStatusName(self, obj):
        try:
            state = GeneralLookUp.objects.get(lookupId = obj.caseType)
            return state.lookupName
        except GeneralLookUp.DoesNotExist:
            return None
        
    def get_stateName(self, obj):
        try:
            state = StateMaster.objects.get(stateId = obj.stateId)
            return state.stateName
        except StateMaster.DoesNotExist:
            return None

    def get_districtName(self, obj):
        try:
            dist = DistrictMaster.objects.get(districtId = obj.districtId)
            return dist.districtName
        except DistrictMaster.DoesNotExist:
            return None

    def get_unitName(self, obj):
        try:
            unit = UnitMaster.objects.get(unitId = obj.unitId)
            return unit.unitName
        except UnitMaster.DoesNotExist:
            return None
        
    def get_caseTypeName(self, obj):
        try:
            caseType = GeneralLookUp.objects.get(lookupId = obj.caseType)
            return caseType.lookupName
        except GeneralLookUp.DoesNotExist:
            return None

class FileDetailsSearchSerializer(serializers.ModelSerializer):
    CaseInfoDetailsId = serializers.IntegerField(source='CaseInfoDetails.CaseInfoDetailsId',read_only = True)
    is_favourited = serializers.BooleanField(read_only=True)
    is_access_request_approved = serializers.BooleanField()
    is_request_raised = serializers.BooleanField()
    classificationName = serializers.SerializerMethodField()
    filetypeName = serializers.SerializerMethodField()
    documentTypeName = serializers.SerializerMethodField()
    
    class Meta:
        model = FileDetails
        fields = ['fileId','CaseInfoDetailsId','fileName','filePath','fileHash','hashTag','subject','fileType','filetypeName','classification','classificationName','uploaded_by','is_approved','is_favourited','is_access_request_approved','is_request_raised','documentType','documentTypeName','comments','isArchieved']
    
    def get_classificationName(self, obj):
        return getattr(obj.classification, 'lookupName', None)
        
    
    def get_filetypeName(self, obj):
        return getattr(obj.fileType, 'lookupName', None)
    
    def get_documentTypeName(self, obj):
        return getattr(obj.documentType, 'lookupName', None)
    
class FileDetailsSerializer(serializers.ModelSerializer):
    CaseInfoDetailsId = serializers.IntegerField(source='CaseInfoDetails.CaseInfoDetailsId',read_only = True)
    is_favourited = serializers.BooleanField(read_only=True)
    classificationName = serializers.SerializerMethodField()
    filetype_name = serializers.CharField(source='fileType.fileTypeName', read_only=True)

    class Meta:
        model = FileDetails
        fields = ['fileId','CaseInfoDetailsId','fileName','filePath','fileHash','hashTag','subject','fileType','classification','uploaded_by','documentType','classificationName','is_favourited', 'filetype_name']  
        # 'classification_name','is_favourited', 'filetype_name'
    
    def get_classificationName(self, obj):
        return getattr(obj.classification, 'lookupName', None)

class FavouriteFileDetailsSerializer(serializers.ModelSerializer):
    caseInfoDetailsId = serializers.SerializerMethodField()
    is_favourited = serializers.BooleanField(read_only=True)
    classificationName = serializers.SerializerMethodField()
    filetypeName = serializers.SerializerMethodField()
    documentTypeName = serializers.SerializerMethodField()
    class Meta:
        model = FileDetails
        fields = ['fileId','caseInfoDetailsId','fileName','filePath','fileHash','hashTag','subject','fileType','classification','uploaded_by','documentType','is_favourited', 'filetypeName','is_favourited','classificationName','documentTypeName']

    def get_caseInfoDetailsId(self, obj):
        return getattr(obj.caseDetails, 'CaseInfoDetailsId', None)
    
    def get_classificationName(self, obj):
        return getattr(obj.classification, 'lookupName', None)
        
    
    def get_filetypeName(self, obj):
        return getattr(obj.fileType, 'lookupName', None)
    
    def get_documentTypeName(self, obj):
        return getattr(obj.documentType, 'lookupName', None)

    
class FileUploadApprovalSerializer(serializers.ModelSerializer):
    division_name = serializers.CharField(source='division.divisionName', read_only=True)
    requested_by_first_name = serializers.CharField(source='requested_by.first_name', read_only=True)
    requested_by_last_name = serializers.CharField(source='requested_by.last_name', read_only=True)
    reviewed_by_first_name = serializers.CharField(source='reviewed_by.first_name', read_only=True)
    reviewed_by_last_name = serializers.CharField(source='reviewed_by.last_name', read_only=True)
    file_name = serializers.CharField(source='file.fileName', read_only=True)
    case_no = serializers.CharField(source='case_details_id.caseNo', read_only=True)
    file = FileDetailsSerializer()
    class Meta:
        model = FileUploadApproval
        fields = [
            'id','status','file','file_name','case_details_id','case_no','requested_by','requested_by_first_name',
            'requested_by_last_name','reviewed_by','reviewed_by_first_name','reviewed_by_last_name','reviewed_at',
            'department','division','division_name','is_approved','comments','created_at'
        ]

class FileDetailsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileDetails
        fields = ['fileId', 'classification', 'documentType', 'fileType', 'hashTag','subject']
        extra_kwargs = {
            'classification': {'required': False},
            'documentType': {'required': False},
            'fileType': {'required': False},
            'hashTag': {'required': False},
            'subject':{'required' : False}
        }

class CaseInfoSearchSerializers(serializers.ModelSerializer):
    stateName = serializers.SerializerMethodField()
    districtName = serializers.SerializerMethodField()
    unitName = serializers.SerializerMethodField()
    caseTypeName = serializers.SerializerMethodField()
    caseDate = serializers.DateTimeField(format="%d-%m-%Y")
    caseStatusName = serializers.SerializerMethodField()

    files = FileDetailsSearchSerializer(many= True, read_only= True)

    class Meta:
        model = CaseInfoDetails
        fields = ['CaseInfoDetailsId','stateId','stateName','year','districtId','districtName','unitId','unitName','Office','caseDate','caseNo','firNo','letterNo','caseType','caseTypeName','author','toAddr','caseStatus','caseStatusName','files']

    def get_caseStatusName(self, obj):
        try:
            state = GeneralLookUp.objects.get(lookupId = obj.caseType)
            return state.lookupName
        except GeneralLookUp.DoesNotExist:
            return None
        
    def get_stateName(self, obj):
        try:
            state = StateMaster.objects.get(stateId = obj.stateId)
            return state.stateName
        except StateMaster.DoesNotExist:
            return None

    def get_districtName(self, obj):
        try:
            dist = DistrictMaster.objects.get(districtId = obj.districtId)
            return dist.districtName
        except DistrictMaster.DoesNotExist:
            return None

    def get_unitName(self, obj):
        try:
            unit = UnitMaster.objects.get(unitId = obj.unitId)
            return unit.unitName
        except UnitMaster.DoesNotExist:
            return None
        
    def get_caseTypeName(self, obj):
        try:
            caseType = GeneralLookUp.objects.get(lookupId = obj.caseType)
            return caseType.lookupName
        except GeneralLookUp.DoesNotExist:
            return None

class FavouriteSerializer(serializers.ModelSerializer):
    file = FavouriteFileDetailsSerializer(read_only = True)

    class Meta:
        model = FavouriteFiles
        fields = ['id','file','added_at']


class NotificationSerializer(serializers.ModelSerializer):
    # file = FileDetailsSerializer()
    division = DivisionSerializer()
    requestedBy = UserSerializer()
    recipient = UserSerializer()
    redirect_url = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = "__all__"
        extra_fields = ['redirect_url', 'status','reference_object_data']

    def get_status(self, obj):
        if obj.reference_object and hasattr(obj.reference_object, 'status'):
            return obj.reference_object.status.lower()
        return "all"

    def get_redirect_url(self, obj):
        ref_obj = obj.reference_object
        if ref_obj:
            print(f"Reference object: {ref_obj}")
            if hasattr(ref_obj, "get_absolute_url"):
                base_url = ref_obj.get_absolute_url()
                tab = self.get_status(obj)
                return f"{base_url}?tab={tab}"
            else:
                print("Reference object does not have get_absolute_url()")
        else:
            print("Reference object is None")
        return "/notifications"

class FileAccessRequestSerializer(serializers.ModelSerializer):
    division_name = serializers.CharField(source='division.divisionName', read_only=True)
    requested_by_first_name = serializers.CharField(source='requested_by.first_name', read_only=True)
    requested_by_last_name = serializers.CharField(source='requested_by.last_name', read_only=True)
    reviewed_by_first_name = serializers.CharField(source='reviewed_by.first_name', read_only=True)
    reviewed_by_last_name = serializers.CharField(source='reviewed_by.last_name', read_only=True)
    approved_by_first_name = serializers.CharField(source='approved_by.first_name', read_only=True)
    approved_by_last_name = serializers.CharField(source='approved_by.last_name', read_only=True)
    file_name = serializers.CharField(source='file.fileName', read_only=True)
    case_no = serializers.CharField(source='case_details_id.caseNo', read_only=True)
    file = FileDetailsSerializer()
    class Meta:
        model = FileAccessRequest
        fields = [
            'id',
            'division',
            'division_name',
            'file',
            'file_name',
            'requested_by',
            'requested_by_first_name',
            'requested_by_last_name',
            'reviewed_by',
            'reviewed_by_first_name',
            'reviewed_by_last_name',
            'approved_by',
            'approved_by_first_name',
            'approved_by_last_name',
            'case_no',
            'is_approved',
            'comments',
            'created_at',
            'approved_at',
            'status'
        ]