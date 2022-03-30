from sqlalchemy import Table, Column, Integer, MetaData, String, DateTime, ForeignKey

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
    }

metadata = MetaData(naming_convention=naming_convention, schema='app')

user_table = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(128), nullable=False),
    Column('age', Integer, nullable=False)
    )

issues_table = Table(
    'issue',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('status', Integer),
    Column('title', String),
    Column('text', String),
    Column('created_date', DateTime),
    Column('assignee_id', Integer, ForeignKey('assignee.id')),
    Column('author_id', Integer, ForeignKey('author.id')),
    Column('modified_date', DateTime)
    )

tags_table = Table(
    'tag',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String)
    )

authors_table = Table(
    'author',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String)
    )

assignees_table = Table(
    'assignee',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String)
    )

tag_to_issue = Table(
    'tag_to_issue',
    metadata,
    Column('tag_id', Integer, ForeignKey('tag.id')),
    Column('issue_id', Integer, ForeignKey('issue.id'))
    )

notes_table = Table(
    'note',
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("likes", Integer, nullable=False),
    Column("comments", Integer, nullable=False),
    Column("color", Integer, nullable=False),
    Column("header", String(128), nullable=False),
    Column("text", String(256), nullable=False),
    Column("created_date", DateTime, nullable=False),
    Column("author_id", Integer, ForeignKey("author.id")),
    Column("modified_date", DateTime, nullable=False)
    )

tag_to_note = Table(
    'tag_to_note',
    metadata,
    Column('tag_id', Integer, ForeignKey("tag.id")),
    Column('note_id', Integer, ForeignKey('note.id'))
    )

messages_table = Table(
    'message',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('text', String(256), nullable=False),
    Column('author_id', Integer, ForeignKey('user.id')),
    Column('created_time', DateTime)
    )