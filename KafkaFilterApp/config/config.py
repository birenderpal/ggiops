class BaseConfig(object):
    DEBUG=True
    SECRET_KEY="random"
    LDAP_PROVIDER_URL="ldap://viridmdmm03.domm.sdp.net.nz:389/"
    LDAP_PROVIDER_VERSION = 3 
    SESSION_PROTECTION="strong"
    KAFKA_API_ENDPOINT="localhost:8000"   
    BCRYPT_LOG_ROUNDS=13
    KAFKA_FILTER_TOPIC="filter-topic" 
class ProductionConfig(BaseConfig):
    DEBUG=False

class TestConfig(BaseConfig):    
    BOOTSTRAP_SERVERS=['capltda28:9092']
    SQLALCHEMY_DATABASE_URI='sqlite:///KafkaFilterApp.db'
    BCRYPT_LOG_ROUNDS=4