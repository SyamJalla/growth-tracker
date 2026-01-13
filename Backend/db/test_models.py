from sqlalchemy import Column, Integer, String, Index
from db.database import Base


class TestTable(Base):
    __tablename__ = "test_table"
    # __table_args__ = (
    #     Index('index_audittable_application_id_request_type', 'application_id', 'request_type'),
    # )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150))


class StudentInfo(Base):
    __tablename__ = "student_info"
    # __table_args__ = (
    #     Index('index_student_info_mobile_surge_id', 'mobile', 'surge_id'),
    # )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150))
    branch = Column(String(15))
    mobile = Column(String(15))
    email = Column(String(50))
    college = Column(String(150))
    surge_id = Column(String(50))
