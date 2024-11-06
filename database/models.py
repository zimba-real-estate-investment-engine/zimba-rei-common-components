
from sqlalchemy import Boolean, Column, String, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Subscription(Base):
    __tablename__ = 'subscription'
    __table_args__ = {'schema': 'zimba-rei-micro'}

    id = Column(String(255), primary_key=True, nullable=False)
    email = Column(String(255), nullable=False)
    name = Column(String(255))
    service_subscribed_to = Column(String(255))
    source_url = Column(String(255))
    subscribed = Column(Boolean)
    form_id = Column(String(255))
    unsubscribed_date = Column(
        TIMESTAMP, 
        server_default=text('CURRENT_TIMESTAMP')
    )
    unsubscribe_token = Column(String(255))
    created_date = Column(
        TIMESTAMP, 
        server_default=text('CURRENT_TIMESTAMP')
    )

    def __repr__(self):
        return f"<Subscription(id={self.id}, email={self.email}, subscribed={self.subscribed})>"