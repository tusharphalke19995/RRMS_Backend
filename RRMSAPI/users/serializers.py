import logging
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from mdm.models import Role, Designation, DesignationHierarchy
from mdm.serializers import DesignationSerializer
from users.utils import send_password_setup_email
from .models import PasswordResetRequest, User
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.crypto import get_random_string


# Set up the logger
logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    roleId = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), source='role')
    designation = serializers.PrimaryKeyRelatedField(
        queryset=Designation.objects.all(), write_only=True, required=True, many =True
    )
    designation_detail = DesignationSerializer(source='designation', read_only=True, many=True)



    class Meta:
        model = User
        fields = ['id','email', 'first_name', 'last_name', 'roleId','mobileno', 'kgid', 'password','designation','designation_detail']
        extra_kwargs = {
            'password': {'write_only': True,'required': False},
        }

    def create(self, validated_data):
        designations = validated_data.pop('designation', [])
        random_password = get_random_string(length=10)
        try:
            user = User.objects.create_user(
                kgid=validated_data['kgid'],
                email=validated_data['email'],
                password=random_password,
                role=validated_data['role'],
                designation=None,
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                mobileno=validated_data.get('mobileno')
            )
        except DjangoValidationError as e:
            raise serializers.ValidationError({'detail': str(e)})
        
        if designations:
            user.designation.set(designations)

        # Send password setup email
        send_password_setup_email(user)
      
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        return representation

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data["passwordSet"] = self.user.is_passwordset

        if not self.user.is_passwordset:
            data.pop("access", None)
            data.pop("refresh", None)

        return data
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['email']=user.email
        token['full_name']=f"{user.first_name} {user.last_name}"
        token['is_superadmin']=user.is_superuser
        # token['set_password']=user.set_password
        token['role']=user.role.roleName if user.role else None
        if user.designation.exists():
            token['designations'] = [
                {
                    'designationName': d.designationName,
                    'designationId': d.designationId
                }
                for d in user.designation.all()
            ]
        else:
            token['designations'] = []
       
        if user.role:
            token['permissions'] = list(user.role.permissions.values_list('codename', flat=True))
        else:
            token['permissions'] = []
        if user.designation.exists():
            token['divisions'] = [
                {
                    'divisionIds': list(d.division.values_list('divisionId', flat=True)),
                    'departmentIds': list(d.department.values_list('departmentId', flat=True))
                }
                for d in user.designation.all()
            ]

            # Handling supervisor info for each designation
            token['supervisors'] = []
            for d in user.designation.all():
                hierarchy = DesignationHierarchy.objects.filter(child_designation=d).first()
                supervisor_data = {}
                
                if hierarchy:
                    supervisor = hierarchy.parent_designation
                    supervisor_data = {
                        'supervisor_designation': supervisor.designationName,
                        'supervisor_divisionIds': list(supervisor.division.values_list('divisionId', flat=True)),
                        'supervisor_departmentIds': list(supervisor.department.values_list('departmentId', flat=True))
                    }
                else:
                    supervisor_data = {
                        'supervisor_designation': None,
                        'supervisor_divisionIds': [],
                        'supervisor_departmentIds': []
                    }
                
                token['supervisors'].append(supervisor_data)

        else:
            token['designations'] = []
            token['divisions'] = []
            token['supervisors'] = []

        return token

class UserSearchSerializer(serializers.ModelSerializer):
    roleName = serializers.CharField(source='role.roleName', read_only=True)
    designation = serializers.PrimaryKeyRelatedField(
        queryset=Designation.objects.all(), write_only=True, required=True, many =True
    )
    designation_detail = DesignationSerializer(source='designation', read_only=True, many=True)

    class Meta:
        model = User
        fields = ['kgid','email','first_name','last_name','mobileno','role','roleName','designation','designation_detail','is_active']
    

class PasswordResetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetRequest
        fields = '__all__'

        def create(self, validated_data):
            # Try to look up the user (optional)
            user = User.objects.filter(id=validated_data.get('kgid')).first()

            return PasswordResetRequest.objects.create(
                **validated_data,
                requested_by=user  # can be None if not found
            )