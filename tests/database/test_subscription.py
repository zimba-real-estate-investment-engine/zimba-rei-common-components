import pytest
from datetime import datetime
from sqlalchemy import text, inspect
import uuid
from database.models import Subscription

def test_subscription_table_creation(clean_db, engine):
    """Test that the subscription table is created correctly"""
    inspector = inspect(engine)
    
    # Verify table exists
    assert 'subscription' in inspector.get_table_names(schema='zimba_rei_micro')
    
    # Get columns info
    columns = {
        col['name']: col 
        for col in inspector.get_columns('subscription', schema='zimba_rei_micro')
    }
    
    # Verify all columns exist with correct properties
    assert 'id' in columns
    assert columns['id']['type'].__class__.__name__ == 'String'
    assert columns['id']['primary_key']
    assert not columns['id']['nullable']
    
    assert 'email' in columns
    assert columns['email']['type'].__class__.__name__ == 'String'
    assert not columns['email']['nullable']
    
    assert 'name' in columns
    assert columns['name']['type'].__class__.__name__ == 'String'
    assert columns['name']['nullable']
    
    assert 'service_subscribed_to' in columns
    assert 'source_url' in columns
    assert 'subscribed' in columns
    assert 'form_id' in columns
    assert 'unsubscribed_date' in columns
    assert 'unsubscribe_token' in columns
    assert 'created_date' in columns

def test_subscription_crud_operations(clean_db, session_factory):
    """Test CRUD operations for Subscription model"""
    Session = session_factory()
    
    # Create test subscription
    test_sub = Subscription(
        id=str(uuid.uuid4()),
        email='test@example.com',
        name='Test User',
        service_subscribed_to='newsletter',
        source_url='https://example.com',
        subscribed=True,
        form_id='form123',
        unsubscribe_token='token123'
    )
    
    # Test Create
    with Session.begin():
        Session.add(test_sub)
    
    # Test Read
    with Session.begin():
        saved_sub = Session.query(Subscription).filter_by(email='test@example.com').first()
        assert saved_sub is not None
        assert saved_sub.name == 'Test User'
        assert saved_sub.subscribed == True
        assert saved_sub.service_subscribed_to == 'newsletter'
    
    # Test Update
    with Session.begin():
        saved_sub.subscribed = False
        saved_sub.unsubscribed_date = datetime.utcnow()
        Session.merge(saved_sub)
    
    # Verify Update
    with Session.begin():
        updated_sub = Session.query(Subscription).filter_by(email='test@example.com').first()
        assert updated_sub.subscribed == False
        assert updated_sub.unsubscribed_date is not None
    
    # Test Delete
    with Session.begin():
        Session.delete(updated_sub)
    
    # Verify Delete
    with Session.begin():
        deleted_sub = Session.query(Subscription).filter_by(email='test@example.com').first()
        assert deleted_sub is None

def test_subscription_constraints(clean_db, session_factory):
    """Test model constraints and validation"""
    Session = session_factory()
    
    # Test required fields
    with pytest.raises(Exception):
        invalid_sub = Subscription(
            email='test@example.com'  # Missing required id field
        )
        with Session.begin():
            Session.add(invalid_sub)
    
    with pytest.raises(Exception):
        invalid_sub = Subscription(
            id=str(uuid.uuid4())  # Missing required email field
        )
        with Session.begin():
            Session.add(invalid_sub)

def test_timestamp_defaults(clean_db, session_factory):
    """Test that timestamps are set correctly"""
    Session = session_factory()
    
    # Create subscription
    test_sub = Subscription(
        id=str(uuid.uuid4()),
        email='test@example.com',
        subscribed=True
    )
    
    with Session.begin():
        Session.add(test_sub)
        Session.flush()
        
        # Verify timestamps are set
        assert test_sub.created_date is not None
        # Note: unsubscribed_date might be None depending on your DB default setting

def test_subscription_representation(clean_db):
    """Test the string representation of the model"""
    sub = Subscription(
        id='test-id',
        email='test@example.com',
        subscribed=True
    )
    
    expected_repr = "<Subscription(id=test-id, email=test@example.com, subscribed=True)>"
    assert str(sub) == expected_repr

# Migration-specific tests
def test_migration_idempotency(clean_db, engine, alembic_config):
    """Test that migrations are idempotent"""
    from alembic import command
    
    # Run migrations twice
    command.upgrade(alembic_config, "head")
    command.upgrade(alembic_config, "head")
    
    # Verify schema is correct
    inspector = inspect(engine)
    columns = {
        col['name']: col 
        for col in inspector.get_columns('subscription', schema='zimba_rei_micro')
    }
    
    # Verify critical columns
    assert 'id' in columns
    assert 'email' in columns
    assert 'subscribed' in columns

def test_data_persistence_across_migrations(clean_db, session_factory, alembic_config):
    """Test that data persists correctly across migrations"""
    Session = session_factory()
    
    # Create test data
    test_sub = Subscription(
        id=str(uuid.uuid4()),
        email='migration@test.com',
        name='Migration Test',
        subscribed=True
    )
    
    # Save test data
    with Session.begin():
        Session.add(test_sub)
    
    # Run a migration cycle
    from alembic import command
    command.downgrade(alembic_config, "-1")
    command.upgrade(alembic_config, "head")
    
    # Verify data persisted
    with Session.begin():
        persisted_sub = Session.query(Subscription).filter_by(email='migration@test.com').first()
        assert persisted_sub is not None
        assert persisted_sub.name == 'Migration Test'
        assert persisted_sub.subscribed == True

# Utility function for other tests
@pytest.fixture
def create_test_subscription(session_factory):
    """Fixture to create a test subscription"""
    def _create_subscription(**kwargs):
        Session = session_factory()
        subscription_data = {
            'id': str(uuid.uuid4()),
            'email': 'default@test.com',
            'subscribed': True,
            **kwargs
        }
        subscription = Subscription(**subscription_data)
        with Session.begin():
            Session.add(subscription)
            Session.flush()
            return subscription
    return _create_subscription