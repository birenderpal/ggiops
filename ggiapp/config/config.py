class BaseConfig(object):
    DEBUG=True
    SECRET_KEY="random"
    LDAP_PROVIDER_URL="ldap://viridmdmm03.domm.sdp.net.nz:389/"
    LDAP_PROVIDER_VERSION = 3 
    SESSION_PROTECTION="strong"   
class ProductionConfig(BaseConfig):
    DEBUG=False    