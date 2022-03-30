from datetime import datetime
from typing import List

from classic.app import validate_with_dto, DTO
from classic.aspects import PointCut

from adapters.interfaces import IssueServiceI
from domain.issue.dto import CreateIssueDTO, UpdateIssueDTO, PartiallyUpdateIssueDTO
from domain.issue.exceptions import IssueNotFoundException
from domain.issue.model import Issue
from domain.issue.storage import IssueStorageI

join_points = PointCut()
join_point = join_points.join_point

class IssueService(IssueServiceI):
    def __init__(self, storage: IssueStorageI):
        self.storage = storage

    @join_point
    def get_issues(self, limit: int, offset: int) -> List[Issue]:
        # in real life any filters or something else
        issues = self.storage.get_all(limit, offset)

        return issues

    @join_point
    def get_issue(self, issue_id) -> Issue:
        issue = self.storage.get_one(issue_id=issue_id)
        if issue is None:
            raise IssueNotFoundException('Issue not found')
        return issue

    @join_point
    @validate_with_dto
    def create_issue(self, issue: CreateIssueDTO) -> Issue:
        tags = self.storage.find_tags(issue.tags)
        issues_data = issue.__dict__
        issues_data['tags'] = tags
        issue = Issue(
            **issues_data,
            created_date=datetime.utcnow(),
            modified_date=datetime.utcnow())
        print(issue)
        return self.storage.create(issue=issue)

    @join_point
    def delete_issue(self, issue_id) -> None:
        self.storage.delete(issue_id=issue_id)

    @join_point
    def update_issue(self, issue: UpdateIssueDTO):
        tags = self.storage.find_tags(issue.tags)
        old_issue = self.get_issue(issue_id=issue.id)
        issue.tags = tags
        issue.created_date = old_issue.created_date
        issue.modified_date = datetime.utcnow()
        issue = Issue(**issue.__dict__)
        self.storage.update(issue=issue)

    @join_point
    def partially_update(self, issue: PartiallyUpdateIssueDTO):
        old_issue = self.get_issue(issue.id)
        if issue.status is not None:
            old_issue.status = issue.status
        if issue.title is not None:
            old_issue.title = issue.title
        if issue.text is not None:
            old_issue.text = issue.text
        if issue.assignee is not None:
            old_issue.assignee = issue.assignee
        if issue.tags is not None and len(issue.tags) > 0:
            old_issue.tags = issue.tags
        if issue.author is not None:
            old_issue.author = issue.author

        old_issue.modified_date = datetime.utcnow()
        self.storage.update(issue=old_issue)
