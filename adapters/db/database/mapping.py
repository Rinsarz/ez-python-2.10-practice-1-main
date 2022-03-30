from sqlalchemy.orm import registry, relationship
from domain.user import model as user_models
from domain.issue import model as issue_models
from domain.note import model as note_models
from domain.message import model as message_model
from adapters.db.database import tables

mapper = registry()
mapper.map_imperatively(
    user_models.User,
    tables.user_table
    )

mapper.map_imperatively(issue_models.Author, tables.authors_table)
mapper.map_imperatively(message_model.Message, tables.messages_table)
mapper.map_imperatively(issue_models.Tag, tables.tags_table)
mapper.map_imperatively(issue_models.Assignee, tables.assignees_table)
mapper.map_imperatively(
    issue_models.Issue,
    tables.issues_table,
    properties={
        'assignee': relationship(
            issue_models.Assignee,
            backref='issue',
            uselist=False,
            lazy='joined',
            join_depth=1
            ),
        'author': relationship(
            issue_models.Author,
            backref='issue',
            uselist=False,
            lazy='joined',
            join_depth=1
            ),

        'tags': relationship(
            issue_models.Tag,
            secondary=tables.tag_to_issue
            )
        }
    )
mapper.map_imperatively(
    note_models.Note,
    tables.notes_table,
    properties={
        'tags': relationship(
            issue_models.Tag,
            secondary=tables.tag_to_note
            )
        }
    )