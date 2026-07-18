from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class BlogPerson(Base):
    """
    Link table: blog <-> person (many-to-many)
    """

    __tablename__ = "blog_person"

    blog_id = Column(
        UUID(as_uuid=True),
        ForeignKey("blog.blog_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    person_id = Column(
        UUID(as_uuid=True),
        ForeignKey("person.person_id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    # ----------------------------------------
    # RELATIONSHIPS
    # ----------------------------------------
    blog = relationship("Blog", back_populates="blog_person_links")
    person = relationship("Person", back_populates="blog_person_links")
    

    def __repr__(self):
        return f"<BlogPerson(person_id={self.person_id!r}, blog_id={self.blog_id!r})>"
